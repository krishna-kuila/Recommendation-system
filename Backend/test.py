import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

def create_vector_store(csv_path, output_index_path, output_csv_path):
    # 1. Load the CSV file
    print("Loading CSV file...")
    # pandas will automatically handle the quoted strings and commas in your data
    df = pd.read_csv(r'C:\Users\Prateek2402\Recommendation-system\dataset.csv')
    
    # 2. Clean and handle missing values for the columns we want to merge
    # We use fillna('') just in case some rows are missing a name or text
    df['name'] = df['name'].fillna('')
    df['text'] = df['text'].fillna('')
    
    # 3. Merge the 'name' and 'text' columns
    print("Merging columns...")
    df['combined_text'] = "Name: " + df['name'] + " | Text: " + df['text']
    
    # Extract the combined text as a list for the transformer
    text_list = df['combined_text'].tolist()
    
    # 4. Load the Sentence Transformer model
    print("Loading Sentence Transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 5. Convert text to vector embeddings
    print("Generating embeddings (this may take a moment)...")
    embeddings = model.encode(text_list, show_progress_bar=True)
    
    # Convert to float32 numpy array, which is strictly required by FAISS
    embeddings = np.array(embeddings).astype('float32')
    
    # 6. Initialize FAISS index
    dimension = embeddings.shape[1]  # 384 dimensions for all-MiniLM-L6-v2
    index = faiss.IndexFlatL2(dimension)
    
    # 7. Add embeddings to the vector store
    print("Adding embeddings to FAISS index...")
    index.add(embeddings)
    
    # 8. Save the FAISS index and the modified dataframe
    print("Saving vector store and metadata...")
    faiss.write_index(index, output_index_path)
    
    # Save the dataframe (this will include _unit_id, description, name, text, and combined_text)
    df.to_csv(output_csv_path, index=False)
    print("Process complete!")

# --- Execution ---
if __name__ == "__main__":
    # Replace these with your actual filenames if different
    CSV_INPUT = "your_data.csv" 
    FAISS_OUTPUT = "my_vector_store.index"
    METADATA_OUTPUT = "data_with_embeddings_meta.csv"
    
    create_vector_store(CSV_INPUT, FAISS_OUTPUT, METADATA_OUTPUT)