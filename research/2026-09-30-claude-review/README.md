# 2026-09-30 Claude 검토와 재측정

- 작성 도구: Claude Code (claude.ai/code 클라우드 세션)
- 작성 시각: 2026-09-30. 시장 데이터는 12:39~12:45 KST에 조회했다.
- 조사 범위: Codex 원본 문서와 답변 세 개의 검토, TCH와 Chainlink·Swift 원문 확인, Sibos 2026 일정 확인, X API 요금 확인, CoinGecko와 업비트 공개 API를 이용한 재측정
- 조사하지 못한 범위: 선물 지표(바이낸스 API 지역 제한), 코인베이스 거래 비중, 운용사 원자료 기준 ETF 흐름, 과거 Sibos 기간 가격 반응

## 파일

| 파일 | 내용 |
|---|---|
| [review.md](review.md) | 검토 본문 |
| [market-remeasure.md](market-remeasure.md) | 재측정 방법과 수치 |
| [snapshot-2026-09-30-1239kst.csv](snapshot-2026-09-30-1239kst.csv) | 관심 종목의 CoinGecko 원자료 (12:39 KST) |
| [remeasure.py](remeasure.py) | 재측정 스크립트. 다시 실행하면 그 시점의 새 스냅숏을 만든다. |

## 요약

- Codex 문서가 관찰한 기관 연계 종목의 상대강세는 7일 기준에서만 뚜렷했다. 30일 기준으로는 중형 알트 전반이 크게 올랐다.
- Sibos 2026(2026-09-28~10-01, 마이애미) 기간과 관찰 기간이 겹친다. 행사 일정 효과를 먼저 배제해야 한다.
- 하루 사이에 HBAR는 급등분 대부분을 반납했고, 직접 선정 발표가 있었던 QNT는 다시 올랐다.
- 새 가설 H1~H4를 [docs/hypotheses.md](../../docs/hypotheses.md)에 등록했다.
- 수집 프로그램 설계의 보완점을 [docs/collector-spec.md](../../docs/collector-spec.md)에 반영했다.
