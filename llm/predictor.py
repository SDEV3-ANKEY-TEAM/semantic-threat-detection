# llm/predictor.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from llm.prompt_template import build_prompt

# 환경변수 로딩 및 OpenAI 클라이언트 설정
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def query_gpt(prompt: str, model: str = "gpt-4o") -> str:
    """
    OpenAI GPT 모델에 프롬프트를 보내고 응답 받기 (v1.x SDK 호환)
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a cybersecurity analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {str(e)}"


# 예시 실행
def example():
    trace_id = "trace-001"
    sequence = "powershell.exe 실행 → 인코딩된 PowerShell 명령어 실행 → evil.ps1 파일 생성 또는 수정 → 외부 접속 시도: 185.42.99.12:443"
    sigma = "Encoded PowerShell, Suspicious File Creation"
    prompt = build_prompt(trace_id, sequence, sigma)
    result = query_gpt(prompt)
    print("🔍 GPT 응답:")
    print(result)


if __name__ == "__main__":
    example()
