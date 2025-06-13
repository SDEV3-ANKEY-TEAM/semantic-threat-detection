# llm/prompt_template.py
def build_prompt(trace_id: str, sequence: str, sigma: str) -> str:
    """
    LLM에게 입력할 프롬프트를 구성하는 템플릿 생성 함수
    """
    prompt = f"""
[Trace ID: {trace_id}]

[시나리오 요약]
{sequence}

[매칭된 Sigma 룰]
{sigma if sigma != '없음' else '매칭된 룰 없음'}

[질문]
이 시나리오는 공격입니까?
공격이라면 어떤 TTP에 해당하며, 그 이유는 무엇입니까?
반드시 '공격' 또는 '정상'으로 판단해 주세요.
"""
    return prompt


# 테스트 예시
def example():
    trace_id = "trace-001"
    sequence = "powershell.exe 실행 → 인코딩된 PowerShell 명령어 실행 → evil.ps1 파일 생성 또는 수정 → 외부 접속 시도: 185.42.99.12:443"
    sigma = "Encoded PowerShell, Suspicious File Creation"
    print(build_prompt(trace_id, sequence, sigma))


if __name__ == "__main__":
    example()
