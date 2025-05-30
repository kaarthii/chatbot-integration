import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI  
import os

app=Flask(__name__)
model=SentenceTransformer('all-MiniLM-L6-v2')
df=pd.read_csv('faq_questions1_answered (1).csv')

df['Embedding']=df['questions'].apply(lambda x:model.encode([x])[0])
df['Embedding']=df['Embedding'].apply(lambda x:x/np.linalg.norm(x))

client=OpenAI(api_key="YOUR-API-KEY")

def find_top_matches(user_question,top_k=3):
    user_embedding=model.encode([user_question])[0]
    user_embedding=user_embedding/np.linalg.norm(user_embedding)
    df['Score']=df['Embedding'].apply(lambda x:cosine_similarity([x],[user_embedding])[0][0])
    return df.sort_values('Score',ascending=False).head(top_k)
    

def gpt_answer(user_question,top_matches,context=""):
    prompt = f"""
You are a helpful, creative assistant that always tries to give a useful answer — even if the user's question is unrelated to the context provided.
Use the chat history below if relevant to infer things like the user's name, preferences, or previous questions.
Also use the FAQ context if it helps.
If the question is general, technical, or personal in nature, answer it independently using your best ability.
Never say "I don't know". If unsure, provide 2-3 helpful suggestions, clarifications, or next steps.

Chat History:
{context}

FAQ Context:
{context}

User's Current Question: {user_question}
Answer:"""
    client=OpenAI(api_key="YOUR-API-KEY")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.6,
        
    )
    answer = response.choices[0].message.content.strip()
    return answer

def get_answer(user_question,context="",use_gpt=True,threshold=0.55):
    top_matches=find_top_matches(user_question)
    best_score=top_matches.iloc[0]['Score']

    if best_score>=threshold:
        path="FAQ"
        answer=top_matches.iloc[0]['Answers']
    else:
        path="GPT"
        return gpt_answer(user_question, top_matches,context=context)
    with open("log_used_method.csv","a") as f:
        f.write(f"{user_question},{path},{best_score}\n")
    return answer
 
@app.route('/ask', methods=['POST'])
def ask():
    print("request came1")
    data= request.get_json(force=True)
    print("Raw data:", request.data)
    if not data or 'question' not in data:
        response= jsonify({"error": "Invalid input"}), 400
        response.headers['Content-Type'] = 'application/json' 
        return response, 400
    user_question = data['question']
    context=data.get('context',"")

    answer= get_answer(user_question,context=context)
    print("data is sent")
    response= jsonify({"answer": answer})
    response.headers['Content-Type']='application/json'

    return response
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
