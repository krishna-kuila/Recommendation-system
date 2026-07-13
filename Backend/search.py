import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

def search_vector_store(query, index_path, metadata_path, top_k=3):
    # 1. Load the saved FAISS index and Metadata CSV
    print("Loading FAISS index and metadata...")
    index = faiss.read_index(index_path)
    df = pd.read_csv(metadata_path)
    
    # 2. Load the EXACT same Sentence Transformer model used for creation
    print("Loading model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 3. Convert the user's text query into a vector embedding
    # It must be cast to float32 to match the FAISS index format
    query_embedding = model.encode([query]).astype('float32')
    
    # 4. Perform the similarity search
    print(f"Searching for: '{query}'\n")
    distances, indices = index.search(query_embedding, top_k)
    
    # 5. Display the results by mapping indices back to the dataframe
    print("-" * 50)
    for i, idx in enumerate(indices[0]):
        if idx < len(df): # Safety check to ensure index exists in dataframe
            row = df.iloc[idx]
            
            # Distance: Lower is better (closer match) in IndexFlatL2
            print(f"Result #{i+1} | Distance Score: {distances[0][i]:.4f}")
            print(f"Unit ID: {row['_unit_id']}")
            print(f"Name: {row['name']}")
            print(f"Text: {row['text']}")
            print("-" * 50)

# --- Execution ---
if __name__ == "__main__":
    # THE PATHS ARE IMPLEMENTED HERE:
    FAISS_INDEX_FILE = "my_vector_store.index"
    METADATA_CSV_FILE = "data_with_embeddings_meta.csv"
    
    # Test the search with a sample query
    user_query = "technology"
    
    search_vector_store(
        query=user_query, 
        index_path=FAISS_INDEX_FILE, 
        metadata_path=METADATA_CSV_FILE,
        top_k=3  # Change this number to get more or fewer results
    )