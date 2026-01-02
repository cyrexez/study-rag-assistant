import os
import pypdf
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

DATA_DIR = 'data/'
DB_FAISS_PATH = 'vectorstore/db_faiss'
_toc_cache = {}
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Check if the key exists (good for debugging)
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, google_api_key=api_key, streaming=True)

def get_structural_info(filename):
    if filename == "All" or not filename: return ""
    if filename in _toc_cache: return _toc_cache[filename]
    path = os.path.join(DATA_DIR, filename)
    try:
        reader = pypdf.PdfReader(path)
        text = "\n".join([reader.pages[i].extract_text() for i in range(min(30, len(reader.pages)))])
        _toc_cache[filename] = text 
        return text
    except: return ""

def get_vector_store(force_rebuild=False):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    if os.path.exists(DB_FAISS_PATH) and not force_rebuild:
        return FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    loader = DirectoryLoader(DATA_DIR, glob="./*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(DB_FAISS_PATH)
    return vector_store

def stream_query(query, vector_store, chat_history, selected_book):
    search_kwargs = {"k": 10} 
    if selected_book != "All":
        search_kwargs["filter"] = {"source": os.path.join(DATA_DIR, selected_book)}
    
    retriever = vector_store.as_retriever(search_kwargs=search_kwargs)
    docs = retriever.invoke(query)
    
    structural_context = get_structural_info(selected_book)
    content_context = "\n\n".join([f"[Page {d.metadata.get('page',0)+1}]: {d.page_content}" for d in docs])

    prompt = f"""
    SYSTEM: You are a high-level academic researcher. Reviewing: {selected_book}.
    GLOBAL STRUCTURE: {structural_context}
    RELEVANT EXCERPTS: {content_context}
    HISTORY: {chat_history[-3:]}
    QUESTION: {query}
    """
    
    # Using the native stream method
    for chunk in llm.stream(prompt):
        if chunk.content:
            yield chunk.content