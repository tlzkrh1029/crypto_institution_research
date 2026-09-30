# crypto_institution_research

기관 금융 인프라와 연결된 크립토 자산을 조사하고, 기관 발표와 시장 반응을 기록하는 저장소다. 이 저장소의 내용은 조사 기록이며 투자 권유가 아니다.

## 현재 상태

2026-09-30 기준으로 설계 단계에 있다. 조사 원칙, 가설, 기관 연결표, 수집 프로그램 설계를 문서로 정리했고, 수집 프로그램 코드는 아직 없다. 결정되지 않은 사항은 [docs/open-questions.md](docs/open-questions.md)에 모아 두었다.

## 먼저 읽을 문서

| 문서 | 내용 |
|---|---|
| [AGENTS.md](AGENTS.md) | 모든 AI 도구가 따르는 공통 작업 지침 |
| [docs/research-principles.md](docs/research-principles.md) | 조사 원칙 |
| [docs/hypotheses.md](docs/hypotheses.md) | 검증 중인 가설 |
| [docs/institution-map.md](docs/institution-map.md) | 기관·업무·프로젝트·토큰 연결표 |
| [docs/collector-spec.md](docs/collector-spec.md) | 수집 프로그램 설계 초안 |
| [docs/decisions.md](docs/decisions.md) | 결정 기록 |
| [docs/open-questions.md](docs/open-questions.md) | 미결 사항 |

## AI 도구에서 이 저장소를 쓰는 방법

코딩용 AI 도구는 작업을 시작할 때 저장소의 지침 파일을 자동으로 읽는다. 이 저장소는 `AGENTS.md`에 원본 지침을 두고, `CLAUDE.md`가 그 파일을 불러오게 했다.

| 도구 | 자동으로 읽는 파일 |
|---|---|
| Codex (CLI, 클라우드) | `AGENTS.md` |
| Claude Code | `CLAUDE.md` (안에서 `@AGENTS.md`로 불러옴) |
| Cursor, GitHub Copilot 코딩 에이전트 | `AGENTS.md` |
| Gemini CLI | 기본값은 `GEMINI.md`이며, 설정에서 `AGENTS.md`를 지정할 수 있음 |
| 웹 채팅 AI (ChatGPT, Claude, Gemini 등) | 자동으로 읽지 않음. 파일 링크를 주거나 GitHub 연결 기능을 사용 |

이 저장소는 공개 저장소이므로, 웹 검색이 가능한 채팅 AI에게 GitHub 파일 링크를 주면 내용을 읽힐 수 있다.

## 폴더 구조

```
AGENTS.md                 공통 작업 지침
CLAUDE.md                 Claude Code용 진입점 (AGENTS.md를 불러옴)
docs/                     원칙, 가설, 연결표, 설계, 결정, 미결 사항
research/                 날짜별 조사 기록과 원자료 (추가만 하고 수정하지 않음)
```

## 조사 기록

| 폴더 | 작성 | 내용 |
|---|---|---|
| [research/2026-09-29-codex-meta-ideas/](research/2026-09-29-codex-meta-ideas/) | Codex | 시장 관찰과 아이디어 문서 원본, 같은 대화의 답변 요지 |
| [research/2026-09-30-claude-review/](research/2026-09-30-claude-review/) | Claude Code | 위 기록에 대한 검토와 하루 뒤 재측정 |
