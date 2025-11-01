from langchain.chains import ConversationalRetrievalChain
from langchain_ollama import ChatOllama 
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_chroma import Chroma 
from rag.get_embedding_function import get_embedding_function 
from rag import config 
from typing import Dict
from langchain.memory import ConversationBufferWindowMemory  
 
CHROMA_PATH = config.CHROMA_PATH 

QA_PROMPT = """
You are an assistant for question-answering tasks. Use the following retrieved context to answer the question. Be concise. Answer the question in the same language in which the question was asked.
Context: {context}
Question: {question}
Answer:
"""

embedding_function = get_embedding_function() 
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function) 

# Dictionary to store memory objects for each user
memories: Dict[str, ConversationBufferWindowMemory] = {}
 
def query_rag(query_text: str, user_id: str): 

    retriever = db.as_retriever( 
        search_type="similarity", 
        search_kwargs={"k": config.DB_RETRIEVER_K} 
    ) 
 
    model = ChatOllama( 
        model=config.LANGUAGE_MODEL, 
        temperature=0, 
        base_url=config.OLLAMA_BASE_URL 
    ) 
 
    # Get or create memory for this user
    if user_id not in memories:
        memories[user_id] = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer",
            k=config.CONVERSATION_BUFFER_WINDOW_MEMORY_K
        )
    
    memory = memories[user_id]
    
    # Create prompt templates
    qa_prompt = ChatPromptTemplate.from_template(QA_PROMPT)
    
    # Create the ConversationalRetrievalChain
    chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        return_source_documents=True,
        verbose=True
    )
    
    # Run the chain
    result = chain.invoke({
        "question": query_text
    })
    
    response_text = result["answer"]
    
    return response_text