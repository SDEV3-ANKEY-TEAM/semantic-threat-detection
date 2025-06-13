# 🧐 LLM + RAG 기반 보안 시나리오 추론 시스템

이 프로젝트는 보안 이벤트 로그(OTEL 기반)을 전처리하고, RAG(Retrieval-Augmented Generation)을 통해 유사 시나리오를 검색한 뒤 LLM이 공격 여부를 추론하는 시스템입니다.

---

## 프로젝트 구조

```
.
├── data/                        # 로그 데이터 및 벡터 인데스
│   ├── otel_traces_sample.json
│   ├── preprocessed_traces.json
│   ├── vector.index
│   └── llm_rag_results.json
├── llm/                         # LLM 관련 코드
│   ├── predictor.py             # GPT 호출
│   └── prompt_template.py       # 프론프트 구성
├── rag/                         # RAG 관련 코드
│   ├── retriever.py             # 유사 로그 검색기
│   └── vector_store.py          # FAISS 인데스팅
├── preprocess/trace_preprocessor.py  # OTEL 로그 전처리
└── main.py                      # 전체 추론 실행 진입점
```

---

## 실행 방법

```bash
# 1. 환경 변수 설정
echo "OPENAI_API_KEY=your_key_here" > .env

# 2. 전처리
python preprocess/trace_preprocessor.py

# 3. 벡터 인데스 생성
python rag/vector_store.py

# 4. 추론 실행
python main.py
```

---

## 출력 결과

- `data/llm_rag_results.json`: 각 로그에 대한 LLM 추론 결과가 저장됩니다.
- `llm_output`: '공격' 또는 '정상'으로 시작하는 LLM의 판단
- `label`: 실제 정보값 ('정상' 또는 '이상')

---

## 성능 평가

추론 결과를 기준으로 `llm_output`의 첫 줄에서 판단값을 추출하여, 정보(`label`)과 비교해 F1, Accuracy를 평가합니다.

---

## 사용 기술

- Python
- OpenAI GPT-4o
- FAISS
- SentenceTransformer
- LangChain (tracing only)
- dotenv

---

