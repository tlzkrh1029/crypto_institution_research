# AGENTS.md: 공통 작업 지침

이 파일은 이 저장소에서 작업하는 모든 AI 도구(Codex, Claude Code, Cursor, GitHub Copilot, Gemini 등)가 가장 먼저 읽어야 하는 공통 지침이다. Claude Code는 `CLAUDE.md`를 통해, Gemini CLI는 `GEMINI.md`를 통해 이 파일을 불러온다. 이 파일은 짧게 유지하고, 세부 내용은 아래에 연결한 문서에 둔다.

## 프로젝트 목적

이 저장소는 기관 금융 인프라(은행 간 결제, 토큰화 예금과 토큰화 자산, 청산·결제, 스테이블코인 지급 등)와 연결된 크립토 자산을 조사하기 위해 만들었다. 목표로 하는 산출물은 두 가지다.

1. 조사 체계: 기관 발표에서 출발해 실제로 연결된 프로젝트와 토큰을 찾고, 사업 단계가 어떻게 바뀌었는지 기록한다.
2. 수집 프로그램: 기관 발표, 뉴스, 가격 반응을 주기적으로 수집하고 사건 단위로 기록한다.

## 현재 상태 (2026-09-30 기준)

- 저장소: https://github.com/tlzkrh1029/crypto_institution_research (공개). main 브랜치가 생기기 전까지 GitHub 기본 브랜치는 `claude/blissful-cerf-rr8n08`이다 ([docs/open-questions.md](docs/open-questions.md) Q5).
- 설계 단계이며, 수집 프로그램 코드는 아직 없다.
- 결정되지 않은 사항은 [docs/open-questions.md](docs/open-questions.md)에 있다. 미결 사항을 임의로 확정하지 않는다. 임시 기본값이 있는 항목은 그 값으로 작업을 진행하고, 임시 기본값을 적용했다는 사실을 결과물(PR 설명이나 research 폴더의 README.md)에 적는다. 임시 기본값이 "없음"인 항목은 사용자에게 확인한다. 사용자에게 물을 수 없는 실행 환경에서는 그 부분을 진행하지 않고, 진행하지 않은 이유를 결과물에 적는다.
- 작업 단계가 바뀌면 이 절도 함께 갱신한다.

## 문서 지도

| 경로 | 내용 | 변경 방식 |
|---|---|---|
| [AGENTS.md](AGENTS.md), [CLAUDE.md](CLAUDE.md), [GEMINI.md](GEMINI.md) | 공통 작업 지침과 도구별 진입점 | PR로 제안하고 사용자 승인 후 변경 |
| [docs/research-principles.md](docs/research-principles.md) | 조사 원칙 | PR로 제안하고 사용자 승인 후 변경 |
| [docs/hypotheses.md](docs/hypotheses.md) | 검증 중인 가설, 검증 방법, 기각 조건, 상태 | 근거가 생길 때마다 상태 갱신 |
| [docs/institution-map.md](docs/institution-map.md) | 기관·업무·프로젝트·토큰 연결표 | 원문 링크가 있는 연결만 추가. 직접 확인하지 못한 항목은 "미확인"으로 표시 |
| [docs/collector-spec.md](docs/collector-spec.md) | 수집 프로그램 설계 | 결정 사항에 맞춰 갱신 |
| [docs/decisions.md](docs/decisions.md) | 결정 기록 | 항목을 추가만 하고, 기존 항목은 고치지 않음 |
| [docs/open-questions.md](docs/open-questions.md) | 미결 사항 | 결정되면 decisions.md에 기록하고 여기서는 "결정됨"으로 표시 |
| [docs/writing-style-ko.md](docs/writing-style-ko.md) | 한국어 문서 작성 지침 (사용자 원문) | 수정·요약 금지 |
| [research/](research/) | 날짜별 조사 기록과 원자료 | 새 폴더를 추가만 하고, 기존 기록은 고치지 않음 |

처음 작업하는 AI는 이 파일, research-principles.md, open-questions.md, [README.md](README.md)의 "조사 기록" 표에서 날짜가 가장 늦은 폴더의 README.md(같은 날짜의 폴더가 여러 개면 그 폴더들의 README.md 모두) 순서로 읽는다. 조사 작업을 하면 hypotheses.md와 institution-map.md를 추가로 읽고, 한국어 문서를 쓰면 writing-style-ko.md를 전문으로 읽는다.

## 작업 규칙

### 사실, 수치, 가설

- 사실을 주장할 때는 확인 날짜와 원문 링크를 함께 적는다. 시장 수치처럼 시각에 따라 달라지는 자료는 확인 시각(KST)까지 적는다. 원문을 직접 확인하지 못했다면 "미확인"으로 표시한다.
- 가격, 수익률, 순위, 거래량 같은 시장 수치는 research/ 아래 날짜별 기록에만 둔다. docs/ 문서에는 시장 수치를 넣지 않고, 필요하면 research/ 기록을 링크한다.
- research/의 수치를 인용할 때는 측정 시각을 함께 적는다. 과거에 측정한 수치를 현재 시장 상황처럼 서술하지 않는다.
- 가설을 규칙처럼 쓰지 않는다. 가설은 docs/hypotheses.md에서 검증 방법, 기각 조건, 상태와 함께 관리한다.

### 조사

조사 방법은 docs/research-principles.md를 따른다. 특히 아래 세 가지는 반드시 지킨다.

- 기관과 프로젝트 사이의 사업 관계와, 토큰 보유자에게 돌아가는 경제적 이익을 구분한다.
- 원문으로 확인된 연결만 인정한다. 같은 협회, 행사, 위원회에 속한다는 이유만으로 연결하지 않는다.
- 비교 대상을 미리 정하고 대조군을 포함한다. 결과를 본 뒤 오른 종목만 표본에 추가하지 않는다.

### 기록

- 새 조사는 `research/YYYY-MM-DD-도구-주제/` 폴더를 새로 만들어 기록한다. 날짜는 조사를 수행한 날(KST)이고, 도구와 주제는 영문 소문자와 하이픈으로 쓴다 (예: `research/2026-10-08-codex-sibos-aftermath/`). 폴더 안 README.md 첫머리에 작성한 AI 도구, 작성 시각(KST), 조사 범위, 조사하지 못한 범위를 적는다. 조사를 마치면 루트 README.md의 "조사 기록" 표에 한 줄을 추가한다.
- 기존 기록에서 잘못을 발견하면 원래 파일을 고치지 않는다. 새 기록에서 정정 내용과 근거를 밝히고, 필요하면 hypotheses.md나 institution-map.md를 갱신한다.

### 브랜치와 PR

- AGENTS.md, CLAUDE.md, GEMINI.md, research-principles.md, decisions.md처럼 지침 성격을 가진 문서는 별도 브랜치와 PR로 변경을 제안한다. 사용자가 병합해야 반영된다.
- PR은 GitHub 기본 브랜치를 대상으로 연다. main이 생기기 전까지 기본 브랜치는 Claude Code 작업 브랜치인 `claude/blissful-cerf-rr8n08`이다.
- 각 도구는 자기 작업 브랜치에서 작업한다. 사용자의 명시적인 허락 없이 다른 도구의 작업 브랜치에 푸시하지 않고, force-push는 하지 않는다.
- PR을 열 수 없는 도구는 작업 브랜치를 푸시한 뒤 사용자에게 브랜치 이름을 알린다. 저장소에 쓸 수 없는 도구(웹 채팅 AI 등)는 파일을 고쳤다고 말하지 않고, 바꿀 파일의 경로와 내용을 사용자에게 제시한다.

### 공개 저장소 주의 사항

이 저장소는 공개 저장소이므로 누구나 내용을 읽을 수 있다.

- API 키, 봇 토큰, 비밀번호, OAuth 토큰, 세션 파일, 감시 서비스의 신호 주소(ping URL) 같은 인증 정보는 커밋하지 않는다. 비밀 값은 `.env`에, 파일 형태의 인증 정보는 `secrets/`에 두고, 둘 다 커밋하지 않는다. 폐기할 수 없는 값(예: 텔레그램 api_hash)도 있으므로 커밋 전에 `git diff --cached`로 확인한다. 실수로 커밋했다면 파일 삭제와 별개로 해당 값을 즉시 폐기하거나 교체한다.
- 보유 종목, 진입 가격, 계좌 정보 같은 개인 매매 정보와, 이름, 이메일, IP 주소, 설치 장소 같은 개인 정보는 올리지 않는다.
- 기사와 보도자료의 전문을 복사하지 않는다. 링크와 짧은 인용만 남긴다.
- 이용약관이 자동 수집을 금지하는 출처(예: X 웹사이트, CoinMarketCap 웹페이지)에는 자동 수집 기능을 구현하지 않는다. 이용 조건에 제약이 있거나 확인되지 않은 출처는 사용자가 정하기 전에 구현하지 않는다 ([docs/collector-spec.md](docs/collector-spec.md) 3절). 필요하다면 공식 API를 쓰고, 그 결정을 decisions.md에 기록한다.

## 문서 작성 규칙

- 문서는 한국어로 쓰고, [docs/writing-style-ko.md](docs/writing-style-ko.md)를 따른다. 변수명, 코드 주석, 커밋 메시지, 로그 문자열에는 이 지침을 적용하지 않고 코드 관례를 따른다.
- 날짜는 `YYYY-MM-DD`, 시각은 KST로 적는다. 다른 시간대를 쓸 때는 시간대를 명시한다.
- 파일 이름과 폴더 이름은 영문 소문자와 하이픈으로 짓는다.
- 도구 이름은 제품 이름으로 적는다 (예: Claude Code, Codex).
- 이 저장소의 내용은 조사 기록이며 투자 권유가 아니다. 문서에서 매수·매도를 권하는 표현을 쓰지 않는다.
