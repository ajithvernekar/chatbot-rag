import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS for handling cross-origin requests
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from transformers import pipeline

# Initialize Flask app
app = Flask(__name__)

# Load models
embedder = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize Pinecone
api_key = os.getenv("PINECONE_API_KEY")
index_name = "wix-index"
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

# Function to query Pinecone
def query_pinecone(query, top_k=5):
    query_embedding = embedder.encode(query).tolist()
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return [match["metadata"]["text"] for match in results["matches"]]

# Function to generate response
def generate_response(query):
    retrieved_docs = query_pinecone(query)
    if not retrieved_docs:
        return "I couldn't find any relevant information."

    context = "\n".join(retrieved_docs)
    response = summarizer(context, max_length=150, min_length=50, do_sample=False)
    return response[0]["summary_text"]


# Enable CORS for all domains (or specify your Wix domain if you want to restrict it)
CORS(app)

# Your existing chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query", "")
    print(f"Received query: {user_query}")  # Debugging line
    if not user_query:
        return jsonify({"error": "Query missing"}), 400

    # You would call the function to generate a response to the user's query here.
    answer = generate_response(user_query)
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
