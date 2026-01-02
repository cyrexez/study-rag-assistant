import subprocess
import sys

def install_requirements():
    modules = [
        "streamlit", 
        "pypdf", 
        "langchain", 
        "langchain-community", 
        "langchain-google-genai", 
        "langchain-text-splitters", 
        "faiss-cpu", 
        "python-dotenv"
    ]
    
    print("--- Starting Environment Setup ---")
    for module in modules:
        print(f"Installing {module}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
    print("--- Setup Complete! Run 'python -m streamlit run app.py' to test. ---")

if __name__ == "__main__":
    install_requirements()