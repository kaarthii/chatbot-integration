import pandas as pd
import numpy as np
from flask import Flask, request, jsonify,render_template
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModelForCausalLM , AutoTokenizer, pipeline
import os
import ollama
from collections import deque
from speechToText import recognize_speech
from textToSpeech import speak


app=Flask(__name__)
model=SentenceTransformer('all-MiniLM-L6-v2')
df=pd.read_csv('faq_questions1_answered (1).csv')

df['Embedding']=df['questions'].apply(lambda x:model.encode([x])[0])
df['Embedding']=df['Embedding'].apply(lambda x:x/np.linalg.norm(x))

session_memory={}

summarizer=pipeline("summarization",model="t5-small")

def mistral_response(prompt):
    response=ollama.chat(model="mistral:7b",messages=[{"role":"user","content":prompt}])
    return response["message"]["content"]

def find_top_matches(user_question,top_k=3):
    user_embedding=model.encode([user_question])[0]
    user_embedding=user_embedding/np.linalg.norm(user_embedding)
    df['Score']=df['Embedding'].apply(lambda x:cosine_similarity([x],[user_embedding])[0][0])
    return df.sort_values('Score',ascending=False).head(top_k)



def summarize_context(session_id, query_type="all"):
    if session_id not in session_memory or not session_memory[session_id]:
        return "I don't have any previous interactions stored for this session."
    
    previous_interactions = list(session_memory[session_id])  

    if query_type == "previous_question":
        return f"Your previous question was: {previous_interactions[-1]['question']}" if previous_interactions else "No previous questions."
    
    elif query_type == "all":
        questions = [interaction["question"] for interaction in previous_interactions]
        return "Your previous questions in this session: " + ", ".join(questions)
    
    return ""
    
def update_memory(session_id, user_question, answer):
    if session_id not in session_memory:
        session_memory[session_id] = deque(maxlen=5)  
    
    interaction = {"question": user_question, "answer": answer}  
    session_memory[session_id].append(interaction)

def get_answer(user_question,session_id,threshold=0.55):
    query_type=None
    if "previous question" in user_question.lower():
        query_type = "previous_question"
    elif "past questions" in user_question.lower() or "history" in user_question.lower():
        query_type = "all"

    if query_type:
        return summarize_context(session_id, query_type)
    
    top_matches=find_top_matches(user_question)
    best_score=top_matches.iloc[0]['Score']

    if best_score>=threshold:
        path="FAQ"
        answer=top_matches.iloc[0]['Answers']
    else:
        path="Mistral"
        summarized_context = summarize_context(session_id)
        refined_prompt=f"question:{user_question}\ncontext:{summarized_context[:500]}\nanswer:"
        answer= mistral_response(refined_prompt)
    update_memory(session_id,user_question,answer)
    print(f"Generated Answer: {answer}")
    with open("log_used_method.csv","a") as f:
        f.write(f"{user_question},{path},{best_score}\n")
    return answer
 
@app.route('/ask', methods=['POST'])
def ask():
    print("request came1")
    data= request.get_json(force=True)
    print("Raw data:", request.data)
    if not data or 'question' not in data or 'session_id' not in data:
        response= jsonify({"error": "Invalid input"}), 400
        response.headers['Content-Type'] = 'application/json' 
        return response, 400
    user_question = data['question']
    session_id=data['session_id']

    answer= get_answer(user_question,session_id)
    print("data is sent")
    response= jsonify({"answer": answer})
    response.headers['Content-Type']='application/json'

    return response

@app.route('/voice',methods=['GET'])
def voice():
    session_id=request.args.get('session_id','default')
    user_question=recognize_speech()
    if not user_question:
        return jsonify({"error":"Could not recognize speech"}),400
    
    answer=get_answer(user_question,session_id)
    speak(answer)

    return jsonify({answer})

@app.route('/')
def home():
    return render_template("index.html")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)