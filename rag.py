from dotenv import load_dotenv
import os

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
import asyncio

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


#Configuartions
PDF_PATH = 'data/multivariable_feedback.pdf'
DB_FAISS_PATH = 'vectorstore/db_faiss'

# Initialize the LLM (using OpenAI)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    temperature=0.1
)

# Function to set up the RAG system
def setup_rag_system():
    # Load the document
    loader = PyPDFLoader('data/multivariable_feedback.pdf')
    documents = loader.load()

    # Split the document into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    document_chunks = splitter.split_documents(documents)

    # Initialize embeddings with Google API key
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=google_api_key
    )

    # Create FAISS vector store from document chunks and embeddings
    vector_store = FAISS.from_documents(document_chunks, embeddings)

    # Return the retriever for document retrieval with specified search_type
    retriever = vector_store.as_retriever(
        search_type="similarity",  # or "mmr" or "similarity_score_threshold"
        search_kwargs={"k": 15}  # Adjust the number of results if needed
    )
    return retriever

# Function to get the response from the RAG system
async def get_rag_response(query: str):
    retriever = setup_rag_system()

    # Retrieve the relevant documents
    retrieved_docs = retriever.invoke(query)

    # Combine context
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # --- FIX STARTS HERE ---
    
    # 1. Create a simple string (Do NOT put this inside a list brackets [])
    prompt = f"Use the following information to answer the question:\n\n{context}\n\nQuestion: {query}"

    # 2. Use .invoke() instead of .generate()
    # .invoke() automatically converts your string into the correct Message format
    response_message = llm.invoke(prompt)
    
    # 3. Return the text content directly
    return response_message.content




if __name__ == "__main__":
    question = "What is chapter two about?"
    response = asyncio.run(get_rag_response(question))
    print("\nANSWER:\n", response)











