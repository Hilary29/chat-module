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
        docs = self.retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = f"""
Tu es assistant pour le service client d'une application bancaire.
Réponds en te basant sur le contexte ci-dessous.
Si plusieurs reponses correspondent, choisissez la plus precise.
Si la reponse ne se trouve pas dans le contexte, dis que tu n'es pas en mesure de répondre et demande si le client souhaite discuter avec un agent.

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


_pipeline_instance: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = RAGPipeline()
    return _pipeline_instance
