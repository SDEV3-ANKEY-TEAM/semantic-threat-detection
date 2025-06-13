import json
import os
from tqdm import tqdm
from dotenv import load_dotenv
from rag.retriever import SimilarTraceRetriever
from llm.predictor import query_gpt
from llm.prompt_template import build_prompt
from preprocess.trace_preprocessor import load_preprocessed_traces
from sklearn.metrics import classification_report, confusion_matrix


def run_llm_inference_with_rag(traces, top_k=3):
    retriever = SimilarTraceRetriever()

    results = []

    for trace in tqdm(traces):
        query = trace["prompt_input"]
        similar_traces = retriever.retrieve(query, top_k=top_k)

        retrieved_block = "\n".join([f"- {t}" for t in similar_traces])

        full_prompt = f"""
        [유사 정상 시나리오 예시]\n{retrieved_block}

        [쿼리 로그]\n{query}

        이 쿼리 로그는 공격입니까?
        공격이라면 어떤 TTP에 해당하며, 그 이유는 무엇입니까?
        반드시 '공격' 또는 '정상'으로 판단해 주세요.
        """

        response = query_gpt(full_prompt.strip())

        results.append(
            {
                "trace_id": trace["trace_id"],
                "llm_output": response,
                "label": trace["label"],
            }
        )

    return results


def evaluate(results):
    def classify(output):
        first_line = output.strip().splitlines()[0].strip()
        if first_line.startswith("공격"):
            return "이상"
        elif first_line.startswith("정상"):
            return "정상"
        else:
            return "판단불가"

    true_labels = [r["label"] for r in results]
    pred_labels = [classify(r["llm_output"]) for r in results]

    # 판단불가 제외
    filtered = [(t, p) for t, p in zip(true_labels, pred_labels) if p != "판단불가"]
    y_true, y_pred = zip(*filtered)

    print("\n[성능 평가 결과]")
    print(classification_report(y_true, y_pred, digits=4))
    print("\n[혼동 행렬]")
    print(confusion_matrix(y_true, y_pred, labels=["정상", "이상"]))


if __name__ == "__main__":
    load_dotenv()
    traces = load_preprocessed_traces("data/preprocessed_traces.json")
    results = run_llm_inference_with_rag(traces)

    with open("data/llm_rag_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    evaluate(results)
