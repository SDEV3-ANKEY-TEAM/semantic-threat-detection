# preprocess/trace_preprocessor.py
import json
from typing import List, Dict


def extract_behavior_sequence(events: List[Dict]) -> List[str]:
    sequence = []
    for e in events:
        etype = e.get("event_type", "").lower()

        if etype == "process_creation":
            cmd = e.get("command_line", "")
            if "-enc" in cmd or "base64" in cmd:
                sequence.append("인코딩된 PowerShell 명령어 실행")
            else:
                sequence.append(f"프로세스 실행: {cmd}")
        elif etype == "network_connection":
            ip = e.get("destination_ip", "")
            port = e.get("destination_port", "")
            sequence.append(f"외부 접속 시도: {ip}:{port}")
        elif etype == "registry_modification":
            path = e.get("registry_path", "")
            key = e.get("registry_key", "")
            value = e.get("registry_value", "")
            sequence.append(f"레지스트리 변경: {path}\\{key} → {value}")
        elif etype == "file_write":
            path = e.get("file_path", "")
            sequence.append(f"파일 생성 또는 수정: {path}")
        else:
            sequence.append(f"기타 이벤트: {etype}")
    return sequence


def preprocess_trace(trace: Dict) -> Dict:
    """
    단일 trace 항목을 의미 기반 시퀀스와 함께 요약
    """
    events = trace.get("events", [])
    sequence = extract_behavior_sequence(events)
    sigma = ", ".join(trace.get("sigma_match", [])) or "없음"

    return {
        "trace_id": trace.get("trace_id"),
        "host": trace.get("host"),
        "label": trace.get("label"),
        "sequence": sequence,
        "sigma_match": sigma,
        "prompt_input": " → ".join(sequence),
    }


def preprocess_otel_file(input_path: str, output_path: str):
    """
    전체 OTEL 파일을 읽어 전처리한 후 결과를 저장
    """
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    processed = [preprocess_trace(t) for t in raw_data]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)

    print(f"✅ 전처리 완료: {output_path}")


def load_preprocessed_traces(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    preprocess_otel_file(
        input_path="data/otel_traces_sample.json",
        output_path="data/preprocessed_traces.json",
    )
