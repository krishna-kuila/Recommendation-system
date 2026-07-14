import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict


def search_vector_store(query, top_k, model, index, unit_ids, names, description, comments, df_len)->List[Dict]:
    
    # 1. Convert the user's text query into a vector embedding
    query_embedding = model.encode([query]).astype('float32') #must be float32
    faiss.normalize_L2(query_embedding) # normalize the query
    
    # 4. Perform the similarity search
    distances, indices = index.search(query_embedding, top_k)
    
    # 5. Display the results by mapping indices back to the dataframe
    print(f"Searching for: '{query}'\n")
    print("-" * 50)
    res = []
    for i, idx in enumerate(indices[0]):
        if idx < df_len: # Safety check to ensure index exists in dataframe
            res.append({
                    "id" : unit_ids[idx],
                    "name" : names[idx],
                    "bio" : description[idx],
                    "comments" : comments[idx],
                    "score" : f"{distances[0][i]:.4f}"
                }
            )
            # Distance: Lower is better (closer match) in IndexFlatL2
            # print(f"Result #{i+1} | Distance Score: {distances[0][i]:.4f}")
            # print(f"Unit ID: {unit_ids[idx]}")
            # print(f"Name: {names[idx]}")
            # print(f"Bio: {description[idx]}")
            # print("-" * 50)
    return res