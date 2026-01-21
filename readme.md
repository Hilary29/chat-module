# 🏉 RAG Rugby Chatbot (Dockerized)

This project is a **Retrieval-Augmented Generation (RAG) chatbot** built with:

- **LangChain**
- **ChromaDB**
- **Ollama**
- **DeepSeek-R1**
- **Gradio**

It allows you to ask questions about the book **“Comprendre le Rugby”** using a local LLM.

The project is fully **Dockerized**, so it can run on **any computer** without installing Python or dependencies manually.

---

## 📁 Project Structure


---

## ⚙️ Requirements

You only need:

- **Docker**
- **Docker Compose**

### Check installation

```bash
docker --version
docker compose --version

🚀 How to Launch the Project
1️⃣ Clone the repository

git clone <your-repository-url>
cd rag-rugby

2️⃣ Build and start all services
docker compose up --build
This will start:

Ollama (LLM server)

The RAG + Gradio application

ChromaDB (persistent vector store)
3️⃣ Download required models (first run only)

Open a new terminal and run:

docker exec -it ollama ollama pull deepseek-r1
docker exec -it ollama ollama pull nomic-embed-text
The models are stored in a Docker volume and will not be downloaded again.

4️⃣ Open the application
Once everything is running, open your browser:
http://localhost:7860

You can now ask questions about the rugby book.

💾 Data Persistence

The following data is persisted automatically using Docker volumes:

Ollama models

Chroma vector database

Stopping or restarting containers will not delete embeddings or models.

🛑 Stop the Project

To stop all services:

docker-compose down


To stop and remove volumes (⚠️ deletes models and embeddings):

docker-compose down -v

🧠 Technologies Used

Python 3.11

LangChain

ChromaDB

Ollama

DeepSeek-R1

Gradio

Docker & Docker Compose

📌 Notes

The PDF file must remain inside the app/ folder.

First startup may be slow due to model downloads.

Works on Windows, macOS, and Linux.

👥 Authors

Christian

Omar

📄 License

This project is for educational and academic use.