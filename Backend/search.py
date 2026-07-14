import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss


# INITIALIZATION STEP (Happens ONLY ONCE when script starts up)

FAISS_INDEX_FILE = "vector_store.index"
METADATA_CSV_FILE = "data_with_embeddings_meta.csv"

print("--- System Startup: Loading Resources ---")

# A. Load FAISS index
print("Loading FAISS index...")
index = faiss.read_index(FAISS_INDEX_FILE)

# B. Load Metadata CSV & convert to optimized lists/dicts for fast lookup
print("Loading metadata...")
df = pd.read_csv(METADATA_CSV_FILE)

# Pre-extracting columns into lists avoids slow Pandas .iloc lookups during loops
unit_ids = df['_unit_id'].tolist()
names = df['name'].tolist()
description = df['description'].tolist()
df_len = len(df)

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("--- Startup Complete. System Ready for Queries ---\n")


def search_vector_store(query, top_k):
    
    # 1. Convert the user's text query into a vector embedding
    query_embedding = model.encode([query]).astype('float32') #must be float32
    faiss.normalize_L2(query_embedding) # normalize the query
    
    # 4. Perform the similarity search
    distances, indices = index.search(query_embedding, top_k)
    
    # 5. Display the results by mapping indices back to the dataframe
    print(f"Searching for: '{query}'\n")
    print("-" * 50)
    for i, idx in enumerate(indices[0]):
        if idx < len(df): # Safety check to ensure index exists in dataframe
            
            # Distance: Lower is better (closer match) in IndexFlatL2
            print(f"Result #{i+1} | Distance Score: {distances[0][i]:.4f}")
            print(f"Unit ID: {unit_ids[idx]}")
            print(f"Name: {names[idx]}")
            print(f"Bio: {description[idx]}")
            print("-" * 50)

# --- Execution ---
if __name__ == "__main__":
    
    # Test the search with a sample query
    user_query = "bio: technology | post: i have knowledge about space"
    
    search_vector_store(
        query=user_query,
        top_k=10  # Change this number to get more or fewer results
    )