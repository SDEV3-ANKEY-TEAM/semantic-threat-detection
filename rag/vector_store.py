# rag/vector_store.py
from typing import List
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json


class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.embeddings = []
        self.texts = []

    def build(self, texts: List[str]):
        self.texts = texts
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)

        print(f"🔎 임베딩 개수: {len(self.embeddings)}")
        print(f"🔎 텍스트 개수: {len(self.texts)}")

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(self.embeddings)

    def save(self, path: str):
        faiss.write_index(self.index, path)

    def load(self, path: str):
        self.index = faiss.read_index(path)

    def search(self, query: str, top_k=5):
        q_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(q_embedding, top_k)

        results = []
        for idx, i in enumerate(I[0]):
            if i == -1 or i >= len(self.texts):
                continue
            results.append((self.texts[i], float(D[0][idx])))

        return results


if __name__ == "__main__":
    with open("data/preprocessed_traces.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [d["prompt_input"] for d in data if d["label"] in ["benign", "정상"]]
    print(f"✅ benign 샘플 수: {len(texts)}")

    if not texts:
        raise ValueError(
            "❌ '정상' 샘플이 없습니다. preprocessed_traces.json을 확인하세요."
        )

    store = VectorStore()
    store.build(texts)
    store.save("data/vector.index")
    print("✅ 벡터 인덱스 저장 완료")
