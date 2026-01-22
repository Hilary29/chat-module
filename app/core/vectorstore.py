from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from typing import List, Optional
from app.config import get_settings
from app.core.embeddings import get_embedding_function


class VectorStoreManager:
    _instance: Optional[Chroma] = None

    @classmethod
    def get_vectorstore(cls, documents: Optional[List[Document]] = None) -> Chroma:
        """Singleton pour le vector store ChromaDB."""
        if cls._instance is None:
            settings = get_settings()
            embedding_function = get_embedding_function()

            if documents:
                cls._instance = Chroma.from_documents(
                    documents=documents,
                    embedding=embedding_function,
                    collection_name=settings.chroma_collection_name,
                    persist_directory=settings.chroma_persist_directory
                )
            else:
                cls._instance = Chroma(
                    embedding_function=embedding_function,
                    collection_name=settings.chroma_collection_name,
                    persist_directory=settings.chroma_persist_directory
                )

        return cls._instance

    @classmethod
    def get_retriever(cls, k: int = 2):
        """Retourne un retriever configure."""
        vectorstore = cls.get_vectorstore()
        return vectorstore.as_retriever(search_kwargs={"k": k})
