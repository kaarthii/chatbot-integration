import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import euclidean_distances

df=pd.read_csv("data.csv")
lines=df["text"].astype(str).tolist()

model = SentenceTransformer('all-MiniLM-L6-v2')

line_embeddings = model.encode(lines)

def is_similar(user_input,threshold=0.80):
    user_embedding = model.encode([user_input])
    similarities= euclidean_distances(user_embedding,line_embeddings)[0]
    best_score=min(similarities)
    best_index=similarities.argmin()

    if best_score>= threshold:
        print(f"Similar score: {best_score:.2f}")
        print(f"Matched Line: {lines[best_index]}")
        return True
   
    else:
        print(f"Not Similar: {best_score:.2f}")
        return False
   
user_input=input("Enter a string:")
is_similar(user_input)
