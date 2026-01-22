import gradio as gr
import os
import pandas as pd

## pour utiliser pdf
#from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

##Loader excel personnalisé en passant par pandas, langchain ne gere pas auto xlsx
def load_excel_as_documents(path: str):
    df = pd.read_excel(path)

    documents = []

    for _, row in df.iterrows():
        content = f"""
Catégorie: {row['category']}
Intention: {row['intent']}
Question: {row['question']}
Réponse: {row['answer']}
Contexte: {row['context']}
""".strip()

        doc = Document(
            page_content=content,
            metadata={
                "category": row["category"],
                "intent": row["intent"]
            }
        )
        documents.append(doc)

    return documents


'''
# Load PDF
print("Loading document...")
loader = PyMuPDFLoader("./Comprendre-le-rugby.pdf")
documents = loader.load()
print(f"Loaded {len(documents)} documents.")
'''

# Load Excel doc
print("Loading Excel document...")
documents = load_excel_as_documents("./Modele_RAG_ServiceClient.xlsx")
print(f"Loaded {len(documents)} rows.")

'''
# Split (interessant avec pdf)
print("Splitting document into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks.")
'''

# Le split est moins interessant avec excel car deja decoupé
chunks = documents


# Embeddings & LLM
print("Setting up embeddings and LLM...")
embedding_function = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

# Vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_function,
    collection_name="clientService_RAG",
    persist_directory="./chroma_db"
)
print("Vector store created.")

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# RAG pipeline
def ask_question(question):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a helpful assistant pour le service client.
Répondez à la question en utilisant uniquement le contexte ci-dessous.
Si plusieurs réponses correspondent, choisissez la plus précise.
Si la réponse ne se trouve pas dans le contexte, dites que vous ne savez pas.

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
    title="client service Chatbot",
    description="Ask questions."
)
print("Launching interface...")
interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
