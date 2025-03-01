
# **RAG-Based Chatbot with Wix Integration**  

This project implements a **Retrieval-Augmented Generation (RAG) model** to build an intelligent chatbot that fetches relevant information from a website and generates contextual responses. The chatbot can be integrated into a **Wix website** or queried via the **command line**.  

## **📌 Project Overview**  

- **Web Scraping**: Extracts content from multiple pages of a website.  
- **Vector Storage**: Uses **Pinecone** for storing text embeddings.  
- **Query Processing**: Retrieves relevant content based on user queries.  
- **Backend API**: Flask-based API for answering queries.  
- **Frontend**: Wix **HTML Embed** integration for chatbot UI.  

---

## **📂 Project Structure**  

```
📂 chatbot-rag
│── 📄 app.py             # Flask API to handle user queries
│── 📄 web_scrape.py      # Web scraper & Pinecone integration
│── 📂 templates
│   ├── 📄 chatbot.html   # Wix chatbot frontend (optional)
│── 📄 README.md          # Documentation
│── 📄 requirements.txt   # Dependencies
```

---

## **🚀 Setup & Installation**  

### **Step 1: Clone the Repository**  
```sh
git clone https://github.com/yourusername/chatbot-rag.git
cd chatbot-rag
```

### **Step 2: Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **Step 3: Set Up Pinecone API Key**  
1. Create a Pinecone account at [Pinecone.io](https://www.pinecone.io/).  
2. Generate an **API key**.  
3. Store the key as an environment variable:  
   ```sh
   export PINECONE_API_KEY="your-api-key"
   ```

---

## **📊 Web Scraping & Storing Data**  

Run `web_scrape.py` to extract website content and store it in **Pinecone**.  

```sh
python web_scrape.py
```

This script will:  
✔ Scrape multiple pages from your website  
✔ Convert text into vector embeddings  
✔ Upload embeddings to Pinecone  

---

## **🖥️ Deploying the API**  

Run `app.py` to start the chatbot API.  

```sh
python app.py
```

By default, it runs on **http://127.0.0.1:5000**. To make it accessible externally, use **ngrok**:  

```sh
ngrok http 5000
```

This provides a **public URL** that can be used in Wix.  

---

## **💬 Querying the Chatbot**  

### **Method 1: Command Line (Without Frontend)**  
```sh
curl -X POST "http://127.0.0.1:5000/chat" -H "Content-Type: application/json" -d '{"query": "What is this project about?"}'
```

### **Method 2: Wix Website Integration**  

1. Open **Wix Editor**.  
2. Add **Custom Embed** > `Embed a Website`.  
3. Paste the **ngrok public URL**.  
4. Publish the site.  

Alternatively, you can use `chatbot.html` for embedding a chatbot UI.  

---

## **🎯 Conclusion**  

This project demonstrates the power of **RAG models** in fetching **dynamic, context-aware** responses. By integrating **Flask, Pinecone, and Wix**, we create an **interactive, intelligent chatbot** for answering queries efficiently. 🚀  

---
