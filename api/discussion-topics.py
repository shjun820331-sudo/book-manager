from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI

SYSTEM_PROMPT = """너는 독서모임 진행을 돕는 토론 주제 추천 도우미다.
주어진 책 제목, 참여자 연령대, 토론 목적을 참고해서 다음 JSON 형식으로만 답해라. 다른 설명은 덧붙이지 마라.

{
  "talking_points": ["이야깃거리 1", "이야깃거리 2", "..."],
  "discussion_topics": ["토론 주제 1", "토론 주제 2", "..."]
}

talking_points와 discussion_topics는 각각 5~7개, 한국어로 작성하고, 연령대와 목적에 맞는
눈높이와 난이도로 작성해라."""


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
        age_group = (body.get("age_group") or "").strip()
        purpose = (body.get("purpose") or "").strip()

        if not title or not age_group or not purpose:
            _send_json(self, 400, {"error": "필수 항목(책 제목, 연령대, 목적)을 모두 입력/선택해주세요."})
            return

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            _send_json(self, 500, {"error": "서버에 API 키가 설정되지 않았습니다."})
            return

        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        user_message = f"책 제목: {title}\n연령대: {age_group}\n토론 목적: {purpose}"

        try:
            client = OpenAI(api_key=api_key, timeout=15.0)
            completion = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            result = json.loads(completion.choices[0].message.content)
        except Exception:
            _send_json(self, 502, {"error": "추천을 가져오지 못했어요. 다시 시도해주세요."})
            return

        _send_json(
            self,
            200,
            {
                "title": title,
                "talking_points": result.get("talking_points", []),
                "discussion_topics": result.get("discussion_topics", []),
            },
        )
