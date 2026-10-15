"""
Evaluation module for comparing retrieval strategies in a RAG system.

Metrics implemented:
1) Precision@k
2) Recall@k
3) Mean Reciprocal Rank (MRR)
4) Retrieval latency
"""

from __future__ import annotations

import time
from typing import Dict, List

from retrieval.retrieval_engine import RetrievalEngine


class EvaluationEngine:
    """Evaluate retrieval quality and speed for different search methods."""

    def __init__(self, retrieval_engine: RetrievalEngine, documents: List[str]) -> None:
        """
        Initialize evaluator.

        Args:
            retrieval_engine: RetrievalEngine instance.
            documents: Corpus document chunks (kept for extensibility/reporting).
        """
        self.retrieval_engine = retrieval_engine
        self.documents = documents

    def precision_at_k(
        self, query: str, relevant_docs: List[str], method: str = "bm25", k: int = 3
    ) -> float:
        """
        Precision@k = relevant_retrieved / total_retrieved.
        """
        retrieved = self.retrieval_engine.search(query, method=method, top_k=k)
        if not retrieved:
            return 0.0

        relevant_set = set(relevant_docs)
        relevant_retrieved = sum(1 for doc in retrieved if doc in relevant_set)
        return relevant_retrieved / len(retrieved)

    def recall_at_k(
        self, query: str, relevant_docs: List[str], method: str = "bm25", k: int = 3
    ) -> float:
        """
        Recall@k = relevant_retrieved / total_relevant.
        """
        if not relevant_docs:
            return 0.0

        retrieved = self.retrieval_engine.search(query, method=method, top_k=k)
        relevant_set = set(relevant_docs)
        relevant_retrieved = sum(1 for doc in retrieved if doc in relevant_set)
        return relevant_retrieved / len(relevant_set)

    def mean_reciprocal_rank(
        self, query: str, relevant_docs: List[str], method: str = "bm25", k: int = 3
    ) -> float:
        """
        MRR for a single query:
            - Find rank of first relevant doc in top-k results
            - Return 1/rank
            - Return 0.0 if none found
        """
        retrieved = self.retrieval_engine.search(query, method=method, top_k=k)
        relevant_set = set(relevant_docs)

        for rank, doc in enumerate(retrieved, start=1):
            if doc in relevant_set:
                return 1.0 / rank
        return 0.0

    def measure_latency(self, query: str, method: str = "bm25", k: int = 3) -> float:
        """
        Measure retrieval latency (seconds) for one query.
        """
        start = time.time()
        _ = self.retrieval_engine.search(query, method=method, top_k=k)
        end = time.time()
        return end - start

    def evaluate_query(
        self, query: str, relevant_docs: List[str], method: str = "bm25", k: int = 3
    ) -> Dict[str, float]:
        """
        Compute all metrics for one query and one retrieval method.
        """
        return {
            "precision": self.precision_at_k(query, relevant_docs, method=method, k=k),
            "recall": self.recall_at_k(query, relevant_docs, method=method, k=k),
            "mrr": self.mean_reciprocal_rank(query, relevant_docs, method=method, k=k),
            "latency": self.measure_latency(query, method=method, k=k),
        }

    def compare_methods(
        self,
        query: str,
        relevant_docs: List[str],
        methods: List[str] | None = None,
        k: int = 3,
    ) -> Dict[str, Dict[str, float]]:
        """
        Evaluate multiple methods and return per-method metric dictionaries.
        """
        if methods is None:
            methods = ["tfidf", "bm25", "semantic", "hybrid"]

        results: Dict[str, Dict[str, float]] = {}
        for method in methods:
            results[method] = self.evaluate_query(
                query=query,
                relevant_docs=relevant_docs,
                method=method,
                k=k,
            )
        return results


if __name__ == "__main__":
    documents = [
        "Employees joining before 2025 receive 10% salary hike",
        "Employees joining after 2025 receive 5% salary hike",
        "Salary revision is done annually",
    ]

    from retrieval.retrieval_engine import RetrievalEngine

    retriever = RetrievalEngine(documents)

    evaluator = EvaluationEngine(retriever, documents)

    query = "salary hike policy"

    relevant_docs = [
        "Employees joining before 2025 receive 10% salary hike",
    ]

    results = evaluator.compare_methods(query, relevant_docs)

    print(results)

