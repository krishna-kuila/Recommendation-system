from flask import Flask, render_template, jsonify, request
from Backend import extract_x_profile_data, search_vector_store
import os
import faiss
from sentence_transformers import SentenceTransformer
import pandas as pd
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "..", "Backend", "data_with_embeddings_meta.csv")
index_path = os.path.join(BASE_DIR, '..', "Backend", "vector_store.index")
print("--- System Startup: Loading Resources ---")

# A. Load FAISS index
print("Loading FAISS index...")
index = faiss.read_index(index_path)

# B. Load Metadata CSV & convert to optimized lists/dicts for fast lookup
print("Loading metadata...")
df = pd.read_csv(csv_path)

# Pre-extracting columns into lists avoids slow Pandas .iloc lookups during loops
unit_ids = df['_unit_id'].tolist()
names = df['name'].tolist()
description = df['description'].tolist()
comments = df['text'].to_list()
df_len = len(df)

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("--- Startup Complete. System Ready for Queries ---\n")


app = Flask(__name__)

def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def get_user():
	if request.method == 'POST':
		query = request.get_json()
		url = "https://x.com/"+query
		print(query)
		user = extract_x_profile_data(url) #comment out this link for actual api call
		if not user:
			return jsonify({
				"Message" : "User Not Found"
			})
		n_user = {
			"name" : user.get("name", 'NA'),
			"handle" : user.get("handle", 'NA'),
			"bio" : user.get("bio", 'NA'),
			"location" : user.get("location", 'NA'),
			"comments" : user.get("comments", 'NA')
		}

		#predicted users
		res = search_vector_store(
					query=f"bio : {n_user['bio']} | post : {n_user['comments']}",
					top_k=10,
					model=model,
					index=index,
					unit_ids=unit_ids,
					names=names,
					description=description,
					comments=comments,
					df_len=df_len
				)
		print(res)
		res = clean(res)
		print(res)

	return jsonify({
			"user" : n_user,
			"users" : res
		}
	), 200

@app.route('/new-user', methods=['GET', 'POST'])
def get_new_user():
    if request.method == 'POST':
        new_user_details = request.get_json()
        bio = new_user_details.get('bio', 'NA')
        res = search_vector_store(
					query=f"bio : {bio} | post : NA",
					top_k=10,
					model=model,
     				index=index,
					unit_ids=unit_ids,
					names=names,
					description=description,
					comments=comments,
					df_len=df_len
				)
        res = clean(res)
    return jsonify({
		"users" : res
	})

if __name__ == "__main__":
	app.run(debug=True)