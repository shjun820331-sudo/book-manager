# 프로젝트 히스토리 / 진행 상황

이 파일은 **다른 컴퓨터에서도 작업을 이어갈 수 있도록** 만든 기록 파일이다.
작업 세션이 끝날 때마다 맨 아래 "진행 로그"에 날짜와 내용을 추가한다.

## 프로젝트 개요

- 과제명: AI 웹서비스 제작 및 배포 미션 (바닐라 HTML/CSS/JS + Vercel
  Serverless Functions(Python) + AI API)
- 요구사항 상세 분석: [`docs/01_과제분석및레포트.md`](docs/01_과제분석및레포트.md)
- 학습 정리(내 과제로 설명하기, 발표·질의응답 대비):
  [`docs/04_학습정리_설명가이드.md`](docs/04_학습정리_설명가이드.md)
- 초보자용 핵심 개념 가이드: [`docs/02_초보자가이드.md`](docs/02_초보자가이드.md)

## 현재 범위 방침 (중요)

> **이번 작업은 "배포 전 단계까지만" 진행한다.** 즉 기획 → 폴더 구조 →
> 프론트엔드 → 반응형 → AI 기능(로컬 기준) 구현까지 완료하고, **Vercel에
> 실제로 배포하는 단계는 별도로 진행**한다. 새 컴퓨터에서 이어받는 사람은
> 아래 체크리스트에서 "배포" 항목 이전까지가 현재 목표임을 인지할 것.

## 진행 체크리스트

- [x] 과제 요구사항 분석 완료 (2026-09-18)
- [x] 초보자 가이드 문서 작성 (2026-09-18)
- [x] 서비스 아이디어 확정 (2026-09-18) — "북토크 나침반": 책 제목 →
      저자소개+줄거리, 연령대/목적 → 토론주제 추천
- [x] 서비스 기획서 작성 (2026-09-18, `docs/03_서비스기획서.md`)
- [x] GitHub 저장소 생성 및 연결 (2026-09-18,
      https://github.com/shjun820331-sudo/book-manager)
- [x] 프로젝트 폴더 구조 초기화 (2026-09-18) — `index.html`, `css/`, `js/`,
      `api/`, `images/`, `requirements.txt`, `.gitignore`
- [x] 프론트엔드(HTML/CSS/JS) 구현 (2026-09-18) — 페이지 4개
      (`index.html`, `book-info.html`, `discussion.html`, `guide.html`)
      + 공통 네비게이션
- [x] 반응형 적용 (2026-09-18, CSS 미디어쿼리 640px/900px 기준) —
      **실제 기기/브라우저 크기별 육안 확인은 아직 안 함, 다음 단계**
- [x] AI 기능 UI 구현 (2026-09-18) — 입력 폼, 결과 표시, 실패 처리 3종
      (빈입력/API오류/지연·타임아웃) 모두 구현
- [x] `api/`에 Python 함수 작성 + AI API 연동 (2026-09-18) —
      `api/app.py` (Flask 앱, `/api/book-info` + `/api/discussion-topics`,
      OpenAI Chat Completions, JSON 응답 모드)
- [x] 로컬 개발 환경 세팅 완료 (2026-09-18) — nvm/Node/Vercel CLI 설치,
      Vercel 로그인, Python venv(`.venv/`), 의존성 설치까지 완료
- [x] 로컬 실행(`vercel dev`) 성공 확인 (2026-09-18) — 서버 기동, 페이지
      로딩, `/api/book-info` 요청이 OpenAI까지 정상적으로 도달하는 것 확인
- [x] AI 응답 실제 확인 (2026-09-19) — OpenAI 크레딧 문제로 **Gemini API로
      교체**. `/api/book-info`, `/api/discussion-topics` 모두 200 응답과
      정상 JSON 확인 (Flask test client 기준, 브라우저 확인은 아직)
- [x] `vercel dev` 로컬 서버로 전체 흐름 검증 (2026-09-19) — 페이지 4개/CSS/JS
      200, 두 API 정상, 빈입력·필수값누락 400, 없는 책 "찾을 수 없습니다" 응답,
      `.env.local`·`api/app.py` 미노출(404) 확인 (curl 기준)
- [x] 브라우저 화면 확인 (2026-09-19) — 헤드리스 Chrome(CDP)으로 375px 모바일
      에뮬레이션 E2E 13/13 통과: 4페이지 가로스크롤 없음, 네비 이동, 빈입력/
      미선택/API오류 메시지, 도서조회→결과→토론페이지 이동(제목 자동채움)→
      추천 결과 표시. (Flask 직접 실행 `flask --app api.app run` 기준)
- [x] 반응형 확인 (2026-09-19) — 375px / 1280px 스크린샷으로 레이아웃 확인
- [ ] **← 여기까지가 이번 작업 범위. 아래부터는 "배포" 단계 (다음 세션에서 진행)**
- [x] (2026-09-19) Vercel 환경 변수(`GEMINI_API_KEY`, Production, `vercel env add`로 등록) 프로덕션에 등록
- [x] Vercel 배포 (2026-09-19, `vercel --prod`) — **https://book-olive-iota.vercel.app**
      (GitHub 연동 자동배포는 아직 안 함 — `vercel git connect`)
- [x] 배포 후 전체 기능 동작 검증 (2026-09-19) — 프로덕션 URL에서 375px 모바일
      E2E 13/13 통과(네비/반응형/AI 2종/실패처리), `.env.local`·`api/app.py` 404
- [ ] README.md 작성 (소개/기술스택/배포URL/실행법/환경변수)
- [ ] 스크린샷 및 AI 코딩 도구 사용 증빙 준비
- [ ] 최종 제출 패키지 정리

## 주요 결정 사항 (Decision Log)

- 2026-09-18: 배포는 이번 작업 범위에서 제외 — 배포 직전 단계까지만 준비하고
  실제 Vercel 배포/환경변수 등록은 추후 별도 세션에서 진행하기로 함.
- 2026-09-18: 서비스 아이디어 확정 — "북토크 나침반". 책 제목 입력 시
  저자소개(작품경향/수상내역/히스토리/대표작)+줄거리 제공, 연령대·목적
  선택 시 토론 이야깃거리·주제 추천.
- 2026-09-18: AI API는 **OpenAI API** 사용하기로 결정.
- 2026-09-18: 페이지 구성은 **실제 별도 HTML 파일 4개**(멀티페이지)로
  결정 — `index.html`(메인), `book-info.html`(도서 정보 조회, AI 기능①),
  `discussion.html`(토론 주제 추천, AI 기능②), `guide.html`(이용 안내).
  도서 정보→토론 주제 페이지 간 책 제목 전달은 URL 쿼리스트링 사용.
  결정 이유: 과제의 학습 목표(HTML/CSS/JS 역할 구분, fetch 흐름 이해)에
  가장 부합하고, 디버깅이 쉽고, 스크린샷 증빙에 유리하기 때문
  (`docs/03_서비스기획서.md` 8번 참고).
- 2026-09-18: **백엔드 구조를 `api/book-info.py` + `api/discussion-topics.py`
  (파일별 자동 라우팅) → `api/app.py` 단일 Flask 앱으로 변경.** 이유:
  최신 Vercel Python 런타임(2026-08 기준 CLI 59.x)이 `vercel dev`에서
  `api/` 폴더 내 다중 `BaseHTTPRequestHandler` 파일을 제대로 인식하지
  못함(entrypoint 인식 오류). Flask 앱 하나로 두 라우트를 합치고
  `pyproject.toml`에 `[tool.vercel] entrypoint = "api.app:app"` 지정.
  `requirements.txt`에 `flask`, `python-dotenv` 추가.
- 2026-09-18: **보안 사고 기록** — 로컬 디버깅 과정에서 실수로
  `.env.local` 파일의 OpenAI API 키 전체가 대화창(터미널 출력)에 노출됨.
  사용자에게 즉시 키 폐기·재발급을 안내함. **다음 세션에서 반드시 확인:
  `.env.local`의 키가 실제로 새로 발급받은 키로 교체되었는지 확인할 것.**
  교훈: 앞으로 `.env.local` 내용을 확인할 때는 절대 `cat`으로 전체 출력하지
  말고, 길이/접두사만 확인하는 방식(awk substr 등)을 사용할 것.

- 2026-09-19: **AI API를 OpenAI → Google Gemini로 교체.** 이유: OpenAI가
  `insufficient_quota`(크레딧 0)로 429를 반환했고 무료 프로젝트라 결제하지
  않기로 함. Gemini의 OpenAI 호환 엔드포인트
  (`https://generativelanguage.googleapis.com/v1beta/openai/`)를 써서
  `openai` SDK는 그대로 두고 base_url/키 이름/모델만 변경. 환경변수는
  `GEMINI_API_KEY`(필수, 이름 대소문자 주의), `GEMINI_MODEL`(선택). 기본 모델은
  `gemini-3.6-flash` (`gemini-2.5-flash`는 신규 사용자 제공 종료로 404).
  키 발급: https://aistudio.google.com/apikey . 옛 OpenAI 키는 `.env.local`에서
  제거됨(어제 노출 사고 건도 해소, 단 OpenAI 대시보드에서 폐기했는지는 본인 확인).

- 2026-09-19: **Flask 앱에 화면 서빙 라우트 추가.** entrypoint가 Flask라
  `vercel dev`에서는 모든 요청이 Flask로 들어와 HTML/CSS/JS가 전부 404였음.
  `api/app.py`에 `/`, `/<page>.html`(허용 4개), `/css|js|images/...` 라우트를
  추가. 루트 전체 공개 시 `.env.local`이 노출되므로 허용 목록 방식 사용.
  **배포 단계에서 확인 필요**: Vercel 프로덕션에서도 HTML/CSS/JS가 함수 번들에
  포함돼 정상 서빙되는지(안 되면 `public/` 폴더 이동 또는 includeFiles 검토).

- 2026-09-19: **배포 시 발견·해결한 문제 2개.** (1) 배포 서버가 `No module named
  'dotenv'`로 전부 500 → Vercel은 `requirements.txt`가 아니라 `pyproject.toml`의
  `dependencies`로 설치함. `pyproject.toml`에 flask/openai/python-dotenv 추가
  (requirements.txt는 로컬용으로 유지, 두 파일 맞출 것). (2) Gemini 무료 등급
  `gemini-3.6-flash`는 **하루 20회** 한도 → 429. 기본 모델을
  `gemini-3.5-flash-lite`로 변경(25회 연속 성공 확인, 응답 ~3초). 그래도 무료
  등급이라 간헐적 503(과부하)/429가 날 수 있어 오류 로그(`_ai_failure`)와 친절한
  메시지 추가. 로그 확인: `vercel logs --environment production --since 15m -j`.

## 다음에 할 일 (Next Steps) — 최우선 순서

1. Flask 직접 실행(위 "알려진 이슈" 참고)으로 실제 브라우저(`http://localhost:3000`)에서 도서 정보
   조회 → 토론 주제 추천까지 전체 흐름 테스트
2. 브라우저 개발자도구로 최소 2개 화면 크기(예: 375px 모바일, 1280px
   데스크톱)에서 레이아웃 직접 확인
3. AI 응답 품질 확인 — 필요하면 `api/app.py`의 프롬프트 다듬기
4. 정리: 잘못된 옛 파일 `api/book-info.py`(untracked)와 오타 파일
   `.env.local.` 삭제
5. (이번 작업 범위 밖, 그다음 세션) Vercel 배포, `GEMINI_API_KEY` 환경 변수
   등록, 배포 후 검증
6. (배포 후) README.md 작성, 스크린샷/AI 코딩 도구 사용 증빙 준비

## 다른 컴퓨터에서 이어서 작업하는 법

**새 컴퓨터에는 Node.js/Vercel CLI/Python이 없을 수 있어서, 아래 순서대로
환경을 새로 세팅해야 한다.** (오늘 이 세팅 때문에 시간이 많이 걸렸음 —
아래 순서대로 하면 시행착오를 줄일 수 있음)

1. `git clone https://github.com/shjun820331-sudo/book-manager.git book`
2. `cd book`
3. 이 `HISTORY.md`의 "진행 체크리스트"에서 마지막으로 체크된 항목부터 확인
4. **Node.js 설치** (없다면): `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash` 로 nvm 설치 후
   터미널을 새로 열고 `nvm install --lts`
5. **Vercel CLI 설치**: `npm install -g vercel`
6. **Vercel 로그인**: `vercel login` (인터랙티브 메뉴가 안 먹히면
   `vercel login 본인이메일@example.com` 형태로 이메일 인증 방식 사용)
7. **Python 가상환경 생성 및 패키지 설치** (시스템 Python이
   "externally-managed-environment" 오류를 낼 수 있어 venv 필수):
   ```
   python3 -m venv .venv
   .venv/bin/python3 -m pip install -r requirements.txt
   source .venv/bin/activate
   ```
8. **환경 변수 설정**: `cp .env.local.example .env.local` 후, 편집기로
   `.env.local`을 열어 `GEMINI_API_KEY=`에 실제 키 입력
   (**절대 이 키를 Claude와의 대화창에 붙여넣지 말 것** — 직접 파일
   편집기나 `read -s`를 쓴 터미널 명령으로만 입력)
9. **로컬 테스트**: `vercel dev` (최초 실행 시 프로젝트 연결 질문에는
   기본값으로 진행). `http://localhost:3000` 접속해서 확인.
10. 작업이 끝나면 이 파일 맨 아래 "진행 로그"에 날짜와 작업 내용을 추가하고
    커밋/푸시

### 참고: 오늘 겪은 문제와 해결책 (다음에 같은 문제 겪으면 참고)

- `vercel`/`node` 명령을 못 찾음 → `!` 명령은 매번 새 비대화형 셸이라
  `.zshrc`가 안 읽힘. `~/.zshenv`에 nvm 초기화 라인을 넣거나, 바이너리를
  `~/.local/bin`에 심볼릭 링크로 걸어두면 해결됨.
- `vercel dev` 실행 시 "No python entrypoint found" 오류 → `api/` 폴더에
  파일이 여러 개면 최신 Vercel Python 런타임이 자동 인식을 못함. Flask
  앱 하나(`api/app.py`)로 합치고 `pyproject.toml`에 entrypoint 지정해서
  해결.
- `pip install` 시 "externally-managed-environment" 오류 → 반드시 venv
  만들고, `python3`/`pip`가 별칭(alias)으로 걸려 있을 수 있으니
  `.venv/bin/python3 -m pip install ...` 처럼 venv 안의 실행파일을 직접
  지정해서 설치.
- `.env.local`을 `vercel dev`(Flask 모드)가 자동으로 못 읽음 →
  `api/app.py`에서 `python-dotenv`로 `load_dotenv(".env.local")` 직접
  호출하도록 코드에 추가해둠 (배포 환경에는 영향 없음).

- `vercel dev`가 `ImportError: cannot import name 'UTC' from 'datetime'`로 죽음 →
  venv를 안 잡고 macOS 기본 Python 3.9를 써서 생기는 오류(Vercel 런타임은 3.11+
  필요). **반드시 `source .venv/bin/activate` 한 셸에서 `vercel dev` 실행.**

- **알려진 이슈 (원인 확인, 우회함)**: `vercel dev`(CLI 59.23.1, vercel_runtime
  0.23.0)는 브라우저가 페이지를 열 때 CSS/JS를 **동시에 요청(동시 연결 2개 이상)**
  하면 Python 함수 프로세스가 로그 없이 죽고 이후 계속 500
  (FUNCTION_INVOCATION_FAILED)을 냄. 일반 Chrome에서도 재현. Python 서버만
  직접 띄우면 정상이라 우리 코드 문제가 아니라 `vercel dev` 도구 문제로 판단.
  **로컬 확인은 Flask를 직접 실행**한다 (같은 `api/app.py`, 화면+API 모두 제공):
  `source .venv/bin/activate && flask --app api.app run --port 3000`
  → http://localhost:3000 . 배포(Vercel)에는 영향 없음(배포 시 재확인 필요).
  참고: 포트 6000은 Chrome이 막는 포트라 쓰지 말 것.

## 진행 로그

### 2026-09-18
- Claude Code로 과제 요구사항을 분석하고 문서 3종 작성
  (`docs/01_과제분석및레포트.md`, `docs/02_초보자가이드.md`, `HISTORY.md`)
- 서비스 아이디어 확정 및 서비스 기획서 작성 (`docs/03_서비스기획서.md`)
  — "북토크 나침반"
- GitHub 저장소 연결 (https://github.com/shjun820331-sudo/book-manager)
- 프로젝트 구조 생성 및 프론트엔드 4페이지 + CSS(반응형) + JS(fetch/실패
  처리) + 백엔드 API 구현
- 로컬 개발 환경(nvm/Node/Vercel CLI/Python venv) 세팅 및 Vercel 로그인
  완료. 시행착오 끝에 `vercel dev` 로컬 실행 성공.
- 백엔드를 파일별 다중 함수 → Flask 단일 앱(`api/app.py`) 구조로 변경
  (Vercel Python 런타임 최신 버전 호환 문제 때문)
- `/api/book-info` 엔드포인트가 OpenAI까지 정상적으로 요청을 보내는
  것까지 확인. 단, OpenAI가 429(결제수단 미등록 추정)를 반환해 실제 AI
  응답 확인은 다음 세션 과제로 넘어감
- 보안 사고: 디버깅 중 API 키가 대화창에 노출되어 사용자에게 키
  폐기·재발급 안내함 (위 Decision Log 참고)
- **아직 안 한 것**: 결제수단 등록 후 AI 응답 재확인, 브라우저 실제
  화면/반응형 확인, Vercel 배포, README 작성, 증빙자료 준비
- 방침: 이번 작업은 배포 전 단계까지만 진행하기로 함

### 2026-09-19
- OpenAI 크레딧 없음(429 `insufficient_quota`) 확인 → 결제 대신 Gemini API로
  교체 (Decision Log 참고). `api/app.py`, `.env.local.example` 수정.
- 환경변수 이름이 소문자(`gemini_API_KEY`)로 저장돼 못 읽던 문제와, 기본
  모델 `gemini-2.5-flash` 404 문제를 해결. 두 엔드포인트 응답 확인.
- `vercel dev` 실행 중 (1) 시스템 Python 3.9 문제, (2) 화면 파일 404 문제를
  해결. 잘못된 파일 `api/book-info.py`, `.env.local.` 삭제.
- `vercel dev` 크래시 원인 조사: 동시 연결 2개로 재현(경로 무관). 로컬 확인은
  Flask 직접 실행으로 대체.
- 화면 확인 완료(위 체크리스트). 한글 줄바꿈이 단어 중간에서 끊기는 점은
  `word-break: keep-all` 적용 검토(선택 사항).
- **아직 안 한 것**: 사용자 브라우저에서 육안 확인, 커밋, Vercel 배포,
  README, 증빙자료
- Vercel 배포 완료: https://book-olive-iota.vercel.app (프로덕션 alias).
  환경 변수 등록, 의존성(pyproject.toml) 수정, 모델 변경(gemini-3.5-flash-lite),
  오류 로깅 추가 후 재배포. 프로덕션 E2E 13/13 통과.
- **아직 안 한 것**: 커밋/푸시(현재 변경분 전부 미커밋), README.md, 스크린샷/
  AI 코딩 도구 사용 증빙, 최종 제출 패키지, (선택) GitHub 연동 자동배포
