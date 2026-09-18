import json
import os

from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)

BOOK_INFO_SYSTEM_PROMPT = """너는 독서모임 준비를 돕는 도서 정보 도우미다.
사용자가 알려준 책 제목을 보고, 다음 JSON 형식으로만 답해라. 다른 설명은 절대 덧붙이지 마라.

{
  "author_intro": "작가의 작품 경향, 주요 수상 내역, 작가 히스토리, 대표작을 포함한 소개 (3~5문장, 한국어)",
  "summary": "스포일러를 최소화한 줄거리 요약 (3~5문장, 한국어)"
}

만약 책 제목을 실제로 알 수 없거나 존재를 확신할 수 없으면, author_intro와 summary에
"해당 도서 정보를 찾을 수 없습니다"라고 답해라."""

DISCUSSION_SYSTEM_PROMPT = """너는 독서모임 진행을 돕는 토론 주제 추천 도우미다.
주어진 책 제목, 참여자 연령대, 토론 목적을 참고해서 다음 JSON 형식으로만 답해라. 다른 설명은 덧붙이지 마라.

{
  "talking_points": ["이야깃거리 1", "이야깃거리 2", "..."],
  "discussion_topics": ["토론 주제 1", "토론 주제 2", "..."]
}

talking_points와 discussion_topics는 각각 5~7개, 한국어로 작성하고, 연령대와 목적에 맞는
눈높이와 난이도로 작성해라."""


def _client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, timeout=15.0)


def _model():
    return os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


@app.route("/api/book-info", methods=["POST"])
def book_info():
    body = request.get_json(silent=True) or {}
    title = (body.get("title") or "").strip()
    if not title:
        return jsonify({"error": "책 제목을 입력해주세요."}), 400

    client = _client()
    if client is None:
        return jsonify({"error": "서버에 API 키가 설정되지 않았습니다."}), 500

    try:
        completion = client.chat.completions.create(
            model=_model(),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": BOOK_INFO_SYSTEM_PROMPT},
                {"role": "user", "content": f"책 제목: {title}"},
            ],
        )
        result = json.loads(completion.choices[0].message.content)
    except Exception:
        return jsonify({"error": "정보를 가져오지 못했어요. 잠시 후 다시 시도해주세요."}), 502

    return jsonify(
        {
            "title": title,
            "author_intro": result.get("author_intro", ""),
            "summary": result.get("summary", ""),
        }
    )


@app.route("/api/discussion-topics", methods=["POST"])
def discussion_topics():
    body = request.get_json(silent=True) or {}
    title = (body.get("title") or "").strip()
    age_group = (body.get("age_group") or "").strip()
    purpose = (body.get("purpose") or "").strip()

    if not title or not age_group or not purpose:
        return (
            jsonify({"error": "필수 항목(책 제목, 연령대, 목적)을 모두 입력/선택해주세요."}),
            400,
        )

    client = _client()
    if client is None:
        return jsonify({"error": "서버에 API 키가 설정되지 않았습니다."}), 500

    user_message = f"책 제목: {title}\n연령대: {age_group}\n토론 목적: {purpose}"

    try:
        completion = client.chat.completions.create(
            model=_model(),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": DISCUSSION_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        result = json.loads(completion.choices[0].message.content)
    except Exception:
        return jsonify({"error": "추천을 가져오지 못했어요. 다시 시도해주세요."}), 502

    return jsonify(
        {
            "title": title,
            "talking_points": result.get("talking_points", []),
            "discussion_topics": result.get("discussion_topics", []),
        }
    )
