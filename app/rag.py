import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaLLM

def initialize_vector_store():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "hr_manual.txt")
    persistent_directory = os.path.join(current_dir, "..", "db", "improved_db2")

    if not os.path.exists(persistent_directory):
        print("Initializing vector store...")
        loader = TextLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", "\. ", " ", ""]
        )
        splits = text_splitter.split_documents(documents)

        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        db = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=persistent_directory
        )
    else:
        db = Chroma(persist_directory=persistent_directory,
                    embedding_function=OllamaEmbeddings(model="nomic-embed-text"))

    return db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "score_threshold": 0.4
        }
    )

template = """You are an HR assistant for our company. Follow these rules:
1. Answer ONLY using the context provided
2. For HR policy questions, be precise
3. For non-HR questions, respond politely that you specialize in HR policies
4. If unsure, say "I need to verify that information. Please check with HR directly."

Context: {context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
llm = OllamaLLM(model="llama3.2")
retriever = initialize_vector_store()

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

def get_rag_response(query: str) -> str:
    return rag_chain.invoke(query)