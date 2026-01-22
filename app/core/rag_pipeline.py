from app.core.vectorstore import VectorStoreManager
from app.core.llm import get_llm
from app.config import get_settings
from typing import Dict, Any, Optional


class RAGPipeline:
    def __init__(self):
        settings = get_settings()
        self.retriever = VectorStoreManager.get_retriever(k=settings.retriever_k)
        self.llm = get_llm()

    def ask(self, question: str) -> Dict[str, Any]:
        """Execute le pipeline RAG et retourne la reponse avec contexte."""
        docs = self.retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = f"""
You are a helpful assistant pour le service client.
Repondez a la question en utilisant uniquement le contexte ci-dessous.
Si plusieurs reponses correspondent, choisissez la plus precise.
Si la reponse ne se trouve pas dans le contexte, dites que vous ne savez pas.

Context:
{context}

Question:
{question}
"""

        response = self.llm.invoke(prompt)

        # Extraire le texte de la reponse
        if isinstance(response.content, list) and len(response.content) > 0:
            answer = response.content[0].get('text', '')
        elif isinstance(response.content, str):
            answer = response.content
        else:
            answer = str(response.content)

        return {
            "answer": answer,
            "sources": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in docs
            ]
        }

    def ask_simple(self, question: str) -> str:
        """Version simplifiee retournant uniquement la reponse textuelle."""
        result = self.ask(question)
        return result["answer"]


_pipeline_instance: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = RAGPipeline()
    return _pipeline_instance
