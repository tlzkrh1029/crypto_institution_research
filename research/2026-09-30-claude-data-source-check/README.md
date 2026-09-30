# 2026-09-30 Claude Code 데이터 출처 이용 조건 점검

- 작성 도구: Claude Code (claude.ai/code 클라우드 세션). 이용 조건 확인에는 조사 에이전트 두 개를 함께 썼다.
- 작성 시각: 2026-09-30 15:30 KST 전후
- 조사 범위: 사용자가 제안한 Yahoo Finance의 이용 가능 여부, 수집 프로그램 첫 버전에 넣을 후보 수집원의 이용 조건
- 조사하지 못한 범위: 아래 각 절의 "확인하지 못한 것"에 적었다.

## Yahoo Finance

결론: 수집 프로그램의 가격 출처로 쓰지 않는다. AGENTS.md의 규칙("이용약관이 자동 수집을 금지하는 출처에는 자동 수집 기능을 구현하지 않는다")에 해당한다.

| 확인 항목 | 확인 결과 (2026-09-30) | 출처 |
|---|---|---|
| 자동 수집 | Yahoo 이용약관 2.4(i)항은 로봇, 스파이더, 스크레이퍼, 데이터 수집 도구 같은 자동화 수단으로 서비스의 데이터를 수집하는 것을 사전의 명시적 허락 없이 금지한다 (2025-05-06 갱신본). | [Yahoo 이용약관](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html) |
| 데이터 재가공 | 같은 약관 2.8(h)항은 서비스의 데이터로 서비스를 대체하는 데이터베이스나 데이터 피드를 만드는 것을 금지한다. | 위와 같음 |
| 공식 API | Yahoo Finance에는 공개된 공식 API가 없다. 널리 쓰이는 `yfinance` 라이브러리는 Yahoo와 관계가 없는 오픈소스이며, 스스로 "Yahoo! finance API는 개인적 이용만을 위한 것"이라고 밝힌다. | [yfinance](https://github.com/ranaroussi/yfinance) |
| 크립토 데이터의 원출처 | Yahoo Finance의 크립토 시세와 시총은 CoinMarketCap이 제공한다 ("Data provided by CoinMarketCap" 표시, 2019년부터 제휴). 따라서 Yahoo를 통해 크립토 데이터를 모으면 결국 CMC 데이터를 약관 밖의 경로로 모으는 셈이 된다. | [CoinMarketCap 설명](https://coinmarketcap.com/academy/article/how-yahoo-finance-powers-its-crypto-data-with-coinmarketcap-api), [Cointelegraph](https://cointelegraph.com/news/yahoo-finance-adds-coinmarketcaps-crypto-prices-to-its-website) |

사람이 브라우저로 Yahoo Finance를 보는 것은 이 결론과 관계가 없다. 문제가 되는 것은 프로그램이 자동으로 수집하는 경우다.

## 대안 검토

Yahoo Finance를 쓰려던 목적은 세 가지로 나눌 수 있다. 목적별로 약관 문제가 없는 대안을 찾았다.

| 목적 | 대안 | 비고 |
|---|---|---|
| 시총 순위 구간 비교 (한 시점) | CoinGecko Demo API, CMC API 무료 Basic 요금제 | 두 곳 모두 공식 API다. 세부 조건은 아래 "시장 데이터" 절 참고 |
| 사건 전후 가격 반응 (1시간~7일) | 거래소 공개 API의 시간봉·일봉 | 아래 "시장 데이터" 절 참고 |
| 과거 행사 기간 검증 (2022~2025년 일봉) | 거래소 공개 API의 일봉 | CoinGecko Demo는 과거 데이터가 최근 365일로 제한되므로 쓸 수 없다 ([CoinGecko 문서](https://docs.coingecko.com/demo/reference/coins-id-market-chart-range), 검색 결과 기준) |

## 후보 수집원의 이용 조건

(확인 결과를 반영할 예정이다.)
