# 📚 Study RAG Assistant

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green.svg)
![Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-orange.svg)

**A context-aware Research Assistant for deep technical document analysis.** This tool is designed to aid the consumption of documents for students and researchers studying dense materials by providing structural awareness and persistent conversation memory.

## 🌟 Key Technical Features

- **Structural Context Buffer**: Unlike standard RAG systems, this assistant extracts and caches the first 30 pages of documents to understand the "global structure" (Table of Contents, Introduction, and Chapters), allowing it to answer high-level structural questions.
- **Persistent Multi-Book Workspace**: Switch between different research subjects in your library without losing your specific chat history for each book.
- **High-Speed Streaming**: Optimized "typewriter-style" response delivery using Gemini 1.5 Flash for a seamless, ChatGPT-like user experience.
- **Security-First**: Fully integrated with `python-dotenv` to ensure API keys remain private and are never leaked to version control.

## 🛠 Tech Stack

- **LLM**: Google Gemini 2.5 Flash
- **Embeddings**: Google `text-embedding-004`
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Orchestration**: LangChain
- **UI Framework**: Streamlit

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone [https://github.com/cyrexez/study-rag-assistant.git](https://github.com/cyrexez/study-rag-assistant.git)
cd study-rag-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Key
   Create a .env file in the root directory:
   GOOGLE_API_KEY=your_gemini_api_key_here 

   
### 3. Run the Assistant
```bash
python -m streamlit run app.py
```

## 📂 Project Structure
app.py: Streamlit frontend and session state management.

rag_backend.py: Core RAG logic, structural indexing, and retrieval chains.

data/: Local directory for your academic PDFs (excluded from Git).

vectorstore/: Local FAISS index storage (excluded from Git).

---

## 💡 Credits & Inspiration

This project was inspired by the original [RAG-with-Langchain-and-FastAPI](https://github.com/anarojoecheburua/RAG-with-Langchain-and-FastAPI) repository by [Ana Rojo-Echeburúa](https://github.com/anarojoecheburua).

I have modified and extended the original concept to better suit academic research needs by implementing:

- **Streamlit-based Interactive UI**: Replaced the FastAPI backend with a dedicated researcher dashboard.
- **Google Gemini 1.5 Flash Integration**: Transitioned from OpenAI to Gemini for high-speed, cost-effective analysis.
- **Structural Context Retrieval**: Added specialized logic to index Table of Contents and document structure for better global awareness.
- **Persistent Chat History**: Enabled per-book session management to keep multiple research threads organized.
