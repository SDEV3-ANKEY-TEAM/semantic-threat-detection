# rag/retriever.py
from rag.vector_store import VectorStore


class SimilarTraceRetriever:
    def __init__(
        self,
        index_path: str = "data/vector.index",
        data_path: str = "data/preprocessed_traces.json",
        top_k: int = 3,
    ):
        """
        FAISS 벡터 인덱스를 로딩하고 검색 가능한 retriever 구성
        """
        self.vector_store = VectorStore()
        self.vector_store.load(index_path)
        self.top_k = top_k

        # ID → 텍스트 매핑을 위해 전체 benign 샘플 로드
        import json

        with open(data_path, "r", encoding="utf-8") as f:
            self.full_data = json.load(f)
        self.id_to_text = {
            d["prompt_input"]: d for d in self.full_data if d["label"] == "benign"
        }

    def retrieve(self, query: str, top_k: int = None):
        """
        쿼리 시퀀스(query)에 대해 가장 유사한 benign 샘플 top-k 반환
        """
        k = top_k if top_k else self.top_k
        results = self.vector_store.search(query, top_k=k)

        # [(text, score)] → [(original_dict, score)]
        return [(self.id_to_text.get(text, {}), score) for text, score in results]
