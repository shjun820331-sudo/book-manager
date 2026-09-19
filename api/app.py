import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request, send_from_directory
from openai import OpenAI

# vercel dev가 .env.local을 함수 프로세스에 자동으로 주입하지 않는 경우가 있어
# 직접 로드한다. 배포 환경에서는 .env.local 파일이 없으므로 아무 영향 없음
# (실제 배포 환경변수는 Vercel 대시보드에서 os.environ으로 주입됨).
load_dotenv(".env.local")

app = Flask(__name__)

# entrypoint가 Flask 앱이라 vercel dev에서는 모든 요청이 이 앱으로 들어온다.
# 그래서 화면(HTML/CSS/JS/이미지)도 여기서 내준다. 루트 전체를 공개하면
# .env.local 같은 파일이 노출되므로 허용 목록(페이지 4개 + 정적 폴더 3개)만 연다.
ROOT_DIR = Path(__file__).resolve().parent.parent
PAGES = {"index", "book-info", "discussion", "guide"}


@app.route("/")
def home():
    return send_from_directory(ROOT_DIR, "index.html")


@app.route("/<page>.html")
def page(page):
    if page not in PAGES:
        abort(404)
    return send_from_directory(ROOT_DIR, f"{page}.html")


@app.route("/<any(css,js,images):folder>/<path:filename>")
def static_files(folder, filename):
    return send_from_directory(ROOT_DIR / folder, filename)


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


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def _client():
    # Gemini의 OpenAI 호환 엔드포인트를 쓰므로 openai SDK를 그대로 사용한다.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=GEMINI_BASE_URL, timeout=15.0)


def _model():
    # flash-lite 계열은 무료 등급 일일 한도가 넉넉하고 응답이 빠르다.
    # (gemini-3.6-flash 무료 등급은 하루 20회라 금방 소진됨)
    return os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")


def _ai_failure(exc, default_message):
    # 원인을 Vercel/터미널 로그에 남기고, 사용자에게는 알아듣기 쉬운 메시지를 준다.
    app.logger.error("AI 호출 실패: %s %s", type(exc).__name__, str(exc)[:300])
    if getattr(exc, "status_code", None) == 429:
        return (
            jsonify({"error": "요청이 많아 잠시 쉬고 있어요. 1분 뒤에 다시 시도해주세요."}),
            429,
        )
    return jsonify({"error": default_message}), 502


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
    except Exception as exc:
        return _ai_failure(exc, "정보를 가져오지 못했어요. 잠시 후 다시 시도해주세요.")

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
    except Exception as exc:
        return _ai_failure(exc, "추천을 가져오지 못했어요. 다시 시도해주세요.")

    return jsonify(
        {
            "title": title,
            "talking_points": result.get("talking_points", []),
            "discussion_topics": result.get("discussion_topics", []),
        }
    )
