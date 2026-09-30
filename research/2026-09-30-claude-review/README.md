# 2026-09-30 Claude Code 검토와 재측정

- 작성 도구: Claude Code (claude.ai/code 클라우드 세션)
- 작성 시각: 2026-09-30 13:19 KST (첫 커밋 dc05f77 기준). 시장 데이터는 12:39~12:45 KST에 조회했다.
- 조사 범위: Codex 원본 문서와 답변 세 개의 검토, TCH와 Chainlink·Swift 원문 확인, Sibos 2026 일정 확인, X API 요금 확인, CoinGecko와 업비트 공개 API를 이용한 재측정
- 조사하지 못한 범위: 선물 지표(바이낸스·바이빗 API 지역 제한), 코인베이스 거래 비중과 가격 프리미엄, 급등 시점의 거래소별 비중 변화, 운용사 원자료 기준 ETF 흐름, 과거 Sibos 기간의 가격 반응
- 정정: 첫 커밋 이후 같은 날, 사용자가 검토하기 전에 사실 확인 결과를 반영해 이 폴더의 파일을 고쳤다. 바뀐 내용은 ETF 자료의 기간과 출처, 재측정 스크립트의 제외 목록과 구간 표, 텔레그램과 Google News RSS에 대한 서술, 일부 문장이다. 정정 내역과 근거는 [research/2026-09-30-claude-fact-check/](../2026-09-30-claude-fact-check/)에 있고, 고치기 전 내용은 git 이력에 있다.

## 파일

| 파일 | 내용 |
|---|---|
| [review.md](review.md) | 검토 본문 |
| [market-remeasure.md](market-remeasure.md) | 재측정 방법과 수치 |
| [snapshot-2026-09-30-1239kst.csv](snapshot-2026-09-30-1239kst.csv) | 관심 종목 12개의 CoinGecko 원자료 (12:39 KST, Powered by [CoinGecko API](https://www.coingecko.com/en/api/)). upbit_로 시작하는 열은 비어 있고, 업비트 수치는 market-remeasure.md에 있다. |
| [remeasure.py](remeasure.py) | 재측정 스크립트. 다시 실행하면 그 시점의 새 스냅숏을 만든다. |

## 요약

- Codex 문서가 관찰한 기관 연계 종목의 상대강세는 24시간과 7일 같은 짧은 기간에서 나타났고, 하루 뒤 재측정에서는 7일 기준에서만 남았다. 30일 기준으로는 중형 알트 전반이 크게 올랐다.
- Sibos 2026(2026-09-28~10-01, 마이애미) 기간과 관찰 기간이 겹친다. 행사 일정 효과를 먼저 배제해야 한다.
- 하루 사이에 HBAR는 급등분 대부분을 반납했고, 직접 선정 발표가 있었던 QNT는 다시 올랐다.
- 새 가설 H1~H4를 [docs/hypotheses.md](../../docs/hypotheses.md)에 등록했다.
- 수집 프로그램 설계의 보완점을 [docs/collector-spec.md](../../docs/collector-spec.md)에 반영했다.
