import gradio as gr
import os

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Load PDF
print("Loading document...")
loader = PyMuPDFLoader("./Comprendre-le-rugby.pdf")
documents = loader.load()
print(f"Loaded {len(documents)} documents.")

# Split
print("Splitting document into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks.")

# Embeddings & LLM
print("Setting up embeddings and LLM...")
embedding_function = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

# Vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_function,
    collection_name="rugby_RAG",
    persist_directory="./chroma_db"
)
print("Vector store created.")

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# RAG pipeline
def ask_question(question):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content

# Gradio UI
interface = gr.Interface(
    fn=ask_question,
    inputs="text",
    outputs="text",
    title="RAG Chatbot: Comprehensive Guide to Rugby",
    description="Ask questions about the Comprehensive Guide to Rugby book."
)
print("Launching interface...")
interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
