# agent.py
from langchain_ollama import ChatOllama
from langchain.memory.buffer import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from rag import get_retriever
from langchain_ollama import ChatOllama
import os

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")


def get_agent():
    llm = ChatOllama(
        model="llama3",
        base_url=OLLAMA_URL,
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

    retriever = get_retriever() # This is the RAG bootstrap phase

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        verbose=True,
    )

    return chain
