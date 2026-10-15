import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import faiss


class RetrievalEngine:

    def __init__(self, documents):

        self.documents = documents

        self.tokenized_docs = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_docs)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.embeddings = self.model.encode(
            documents,
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(self.embeddings)

        dim = self.embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def bm25_retrieval(self, query, top_k=3):

        scores = self.bm25.get_scores(query.lower().split())

        idx = np.argsort(scores)[::-1][:top_k]

        return idx.tolist()

    def semantic_retrieval(self, query, top_k=3):

        q = self.model.encode([query], convert_to_numpy=True).astype("float32")

        faiss.normalize_L2(q)

        _, idx = self.index.search(q, top_k)

        return idx[0].tolist()

    def hybrid_retrieval(self, query, top_k=3):

        bm = self.bm25_retrieval(query, top_k)
        se = self.semantic_retrieval(query, top_k)

        final = []

        for i in bm + se:
            if i not in final:
                final.append(i)

        return final[:top_k]

    def search(self, query, method="hybrid", top_k=3):

        if method == "bm25":
            return self.bm25_retrieval(query, top_k)

        elif method == "semantic":
            return self.semantic_retrieval(query, top_k)

        else:
            return self.hybrid_retrieval(query, top_k)