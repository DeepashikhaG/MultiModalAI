from __future__ import annotations

from typing import Dict, List
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class VerificationEngine:

    def __init__(self, retrieval_engine):

        self.retrieval_engine = retrieval_engine
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def retrieve_supporting_docs(self, answer: str, top_k: int = 3) -> List[str]:

        indices = self.retrieval_engine.search(
            answer,
            method="hybrid",
            top_k=top_k
        )

        docs = []

        for i in indices:
            docs.append(self.retrieval_engine.documents[i])

        return docs

    def compute_similarity(self, answer: str, documents: List[str]) -> float:

        if not documents:
            return 0.0

        answer_embedding = self.embedding_model.encode(
            [answer],
            convert_to_numpy=True
        )

        doc_embeddings = self.embedding_model.encode(
            documents,
            convert_to_numpy=True
        )

        scores = cosine_similarity(
            answer_embedding,
            doc_embeddings
        ).flatten()

        return float(np.max(scores))

    def verify_answer(self, answer: str, threshold: float = 0.55) -> Dict:

        supporting_docs = self.retrieve_supporting_docs(answer)

        confidence = self.compute_similarity(
            answer,
            supporting_docs
        )

        status = "Verified" if confidence >= threshold else "Low Confidence"

        return {
            "status": status,
            "confidence": round(confidence, 3),
            "supporting_docs": supporting_docs
        }