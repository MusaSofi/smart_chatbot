from langchain_ollama import OllamaEmbeddings
from rag import config

def get_embedding_function():
    embeddings = OllamaEmbeddings(model=config.EMPEDINGS_MODEL, base_url=config.OLLAMA_BASE_URL)
    return embeddings
