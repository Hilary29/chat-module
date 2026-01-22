import pandas as pd
from langchain_core.documents import Document
from typing import List


def load_excel_as_documents(path: str) -> List[Document]:
    """Charge un fichier Excel et convertit chaque ligne en Document."""
    df = pd.read_excel(path)
    documents = []

    for _, row in df.iterrows():
        content = f"""
Categorie: {row['category']}
Intention: {row['intent']}
Question: {row['question']}
Reponse: {row['answer']}
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
