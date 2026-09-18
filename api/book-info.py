from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI

SYSTEM_PROMPT = """너는 독서모임 준비를 돕는 도서 정보 도우미다.
사용자가 알려준 책 제목을 보고, 다음 JSON 형식으로만 답해라. 다른 설명은 절대 덧붙이지 마라.

{
  "author_intro": "작가의 작품 경향, 주요 수상 내역, 작가 히스토리, 대표작을 포함한 소개 (3~5문장, 한국어)",
  "summary": "스포일러를 최소화한 줄거리 요약 (3~5문장, 한국어)"
}

만약 책 제목을 실제로 알 수 없거나 존재를 확신할 수 없으면, author_intro와 summary에
"해당 도서 정보를 찾을 수 없습니다"라고 답해라."""


def _send_json(handler, status, data):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(content_length) if content_length else b"{}"
            body = json.loads(raw or b"{}")
        except (ValueError, json.JSONDecodeError):
            _send_json(self, 400, {"error": "요청 형식이 올바르지 않습니다."})
            return

        title = (body.get("title") or "").strip()
        if not title:
            _send_json(self, 400, {"error": "책 제목을 입력해주세요."})
            return

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            _send_json(self, 500, {"error": "서버에 API 키가 설정되지 않았습니다."})
            return

        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

        try:
            client = OpenAI(api_key=api_key, timeout=15.0)
            completion = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"책 제목: {title}"},
                ],
            )
            result = json.loads(completion.choices[0].message.content)
        except Exception:
            _send_json(self, 502, {"error": "정보를 가져오지 못했어요. 잠시 후 다시 시도해주세요."})
            return

        _send_json(
            self,
            200,
            {
                "title": title,
                "author_intro": result.get("author_intro", ""),
                "summary": result.get("summary", ""),
            },
        )
