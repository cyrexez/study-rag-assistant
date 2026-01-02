from setuptools import setup, find_packages

setup(
    name="rag-research-assistant",
    version="0.1.0",
    author="Emmanuel",
    description="A high-performance RAG system for academic PDF research using Gemini 2.5 Flash",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-community",
        "langchain-google-genai",
        "langchain-text-splitters",
        "faiss-cpu",
        "pypdf",
        "python-dotenv",
    ],
    python_requires=">=3.9",
)