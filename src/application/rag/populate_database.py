import json
import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader, WebBaseLoader, PyMuPDFLoader, UnstructuredXMLLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from rag.get_embedding_function import get_embedding_function
from langchain_chroma import Chroma
from rag import config
import glob
import re


CHROMA_PATH = config.CHROMA_PATH
SOURCES_FILE = config.SOURCES_FILE

def main():
    sources = load_sources()
    documents = load_all_documents(sources)
    chunks = split_documents(documents)
    add_to_chroma(chunks)
    print(f"✅ Populating database is done")

def load_sources():
    with open(SOURCES_FILE, "r") as f:
        return json.load(f)
    
def clean_text(text: str) -> str:
    # Collapse multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_documents(documents: list[Document]) -> list[Document]:
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)
    return documents


def load_all_documents(sources: list):
    all_documents = []
    for source in sources:
        if source["type"] == "md":
            print(f"📄 Loading markdown: {source['path']}")
            loader = UnstructuredMarkdownLoader(source["path"])
            all_documents.extend(loader.load())
        elif source["type"] == "url":
            print(f"🌐 Loading URL: {source['url']}")
            loader = WebBaseLoader(source["url"])
            all_documents.extend(loader.load())
        elif source["type"] == "pdf":
            print(f"📄 Loading pdf: {source['path']}")
            loader = PyMuPDFLoader(source["path"])
            all_documents.extend(loader.load())
        elif source["type"] == "xml":
            print(f"📄 Loading XML: {source['path']}")
            loader = UnstructuredXMLLoader(source["path"])
            all_documents.extend(loader.load())
        elif source["type"] == "txt":
            print(f"📄 Loading TXT: {source['path']}")
            loader = TextLoader(source["path"])
            all_documents.extend(loader.load())

        elif source["type"] == "path":
            if source.get("subtype") == "xml":
                print(f"📂 Loading XML files from folder: {source['path']}")
                xml_files = glob.glob(os.path.join(source["path"], "*.xml"))
                for xml_file in xml_files:
                    loader = UnstructuredXMLLoader(xml_file)
                    all_documents.extend(loader.load())
            elif source.get("subtype") == "md":
                print(f"📂 Loading markdown files from folder: {source['path']}")
                md_files = glob.glob(os.path.join(source["path"], "*.md"))
                for md_file in md_files:
                    loader = UnstructuredMarkdownLoader(md_file)
                    all_documents.extend(loader.load())
        else:
            print(f"⚠️ Unknown source type: {source['type']}")
        
    cleaned_documents: list[Document] = clean_documents(all_documents)
        
    return cleaned_documents

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )
    print(f"👉 Adding {len(chunks)} chunks to Chroma")
    db.add_documents(chunks)


if __name__ == "__main__":
    main()
