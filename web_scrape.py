import os
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
api_key = os.getenv("PINECONE_API_KEY")  
index_name = "wix-index"  

pc = Pinecone(api_key=api_key)
if index_name not in pc.list_indexes():
    pc.create_index(index_name, dimension=384, metric="cosine", spec=ServerlessSpec(cloud="aws", region="us-east-1"))
index = pc.Index(index_name)

# Load embedding model
embedder = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

# List of pages to scrape
pages_to_scrape = [
    "https://ajithvernekar.wixsite.com/data-analyst",
    "https://ajithvernekar.wixsite.com/data-analyst/resume",
    "https://ajithvernekar.wixsite.com/data-analyst/contact",
    "https://ajithvernekar.wixsite.com/data-analyst/blog",
    "https://ajithvernekar.wixsite.com/data-analyst/projects"
]

# Step 1: Scrape Website Content from multiple pages
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")  # Extracting text from <p> tags
        text = " ".join([p.get_text() for p in paragraphs])
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return ""

# Scrape content from all pages
website_text = ""
for page in pages_to_scrape:
    print(f"Scraping {page}...")
    page_text = scrape_website(page)
    website_text += page_text  # Append content from each page

# Step 2: Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
chunks = text_splitter.split_text(website_text)

# Step 3: Convert text to vector embeddings and upload to Pinecone
for i, chunk in enumerate(chunks):
    vector = embedder.encode(chunk).tolist()
    index.upsert(vectors=[(f"chunk-{i}", vector, {"text": chunk})])

print("✅ Data uploaded to Pinecone successfully!")
