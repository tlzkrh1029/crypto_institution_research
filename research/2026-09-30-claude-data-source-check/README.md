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

## 뉴스와 공식 발표 출처

수집 프로그램이 하는 일을 기준으로 판정했다. 수집 프로그램은 맥북에서 개인적·비상업적으로 5분 안팎마다 RSS를 확인하고, 제목, 링크, 발표 시각, 300자 이하의 발췌를 로컬 데이터베이스에 저장한다. 조사 결과로는 링크와 짧은 인용, 사용자의 분석만 공개 저장소에 올린다. 일부 자료는 분류를 위해 AI에 보낼 수 있다. 확인 시각은 2026-09-30 14:55~15:15 KST다.

| 출처 | 판정 | 근거 | 이 저장소의 처리 |
|---|---|---|---|
| SEC (sec.gov) | 조건부 가능 | sec.gov의 정보는 공개 정보이며 허락 없이 복사·배포할 수 있다. 출처 표기를 권한다. 공정 접근 정책은 연락처를 넣은 User-Agent 선언과 전체 초당 10건 이하를 요구하고, 분류되지 않은 봇의 크롤링을 허용하지 않는다. robots.txt는 `/cgi-bin`을 막는다. | 보도자료와 발언 RSS만 켰다. `SEC_USER_AGENT`가 없으면 건너뛴다. EDGAR 최신 공시 피드(`/cgi-bin` 아래)는 넣지 않았다. |
| 연준 (federalreserve.gov) | 조건부 가능 | 따로 표시하지 않은 정보는 퍼블릭 도메인이며 허락 없이 복사·배포할 수 있다. 연준을 출처로 밝혀 달라고 요청한다. 제3자 저작물과 로고는 제외된다. | 전체 보도자료 RSS를 켰다. |
| DTCC RSS | 조건부 가능 | RSS 구독은 권장된다. 사이트 이용 허락은 개인적 범위이고, 내용을 데이터베이스로 모으거나 재배포하려면 서면 허락이 필요하다. CUSIP 정보는 CGS와 ABA의 지식재산이다. | Insights 피드만 켜고, 제목·링크·날짜만 저장한다(`store_excerpt: false`). CUSIP 목록이 담기는 공지 피드는 넣지 않았다. |
| DTCC 사이트맵 | 불명확 | 사이트맵은 robots.txt에 공개되어 있지만, 약관은 자동화 도구로 사이트의 데이터를 체계적으로 추출하는 것을 금지한다. | 설정에는 두되 꺼 두었다. 사용자가 정한다 (Q10). |
| PR Newswire | 제한 | 약관은 로봇이나 자동 장치로 콘텐츠에 접근하거나 수집하는 것, 서면 허락 없는 데이터베이스 저장과 재배포, AI 시스템 학습을 포함한 소프트웨어 개발에 콘텐츠를 쓰는 것을 금지한다. 이용은 개인적·비상업적 범위로 한정된다. 다만 RSS 안내 페이지는 필터를 거는 개인용 RSS 리더를 소개한다. | 넣지 않았다. 사용자가 정한다 (Q10). |
| Business Wire | 불명확 | 약관 페이지가 이 환경에서 모두 차단되어 원문을 확인하지 못했다. 검색 결과에 인용된 문구로는 RSS 확인은 허용하지만 정보를 저장·집계·재배포하는 것은 금지한다. | 넣지 않았다. 사용자가 브라우저로 약관을 확인한 뒤 정한다 (Q10). |
| GlobeNewswire | 불명확 | 독자에게 적용되는 약관을 찾지 못했다. 찾은 약관은 유료 고객용 계약이며, 봇으로 데이터를 수집하는 것을 금지한다. robots.txt는 RSS 경로를 막지 않는다. | 넣지 않았다. 사용자가 정한다 (Q10). |

출처 페이지: [SEC 개인정보·보안 정책](https://www.sec.gov/about/privacy-information), [EDGAR 공정 접근 정책](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data), [연준 면책 고지](https://www.federalreserve.gov/disclaimer.htm), [DTCC 이용약관](https://www.dtcc.com/terms), [DTCC RSS](https://www.dtcc.com/rss-feeds), [PR Newswire 이용약관](https://www.prnewswire.com/terms-of-use/), [GlobeNewswire 고객 약관](https://portal.notified.com/terms-conditions/en). 인용문은 SEC만 WebFetch 요약을 거쳤고, 나머지는 원문을 직접 내려받아 확인했다.

확인하지 못한 것:

- Business Wire의 약관, robots.txt, 피드 안내 페이지는 모두 접속이 거부되었다.
- GlobeNewswire의 운영사(Notified)의 법적 고지 페이지는 열리지 않았다.
- 프로젝트 공식 블로그(Chainlink, Hedera, Stellar, Quant, Ondo)와 기관 보도자료 페이지(TCH, U.S. Bank, BVNK)의 약관은 아직 확인하지 않았다.

## 이 결과가 뜻하는 것

약관상 문제없이 자동으로 수집할 수 있는 뉴스 출처는 규제기관과 일부 기관의 공식 피드로 좁혀진다. 기관과 크립토 프로젝트의 연결 발표가 가장 많이 나오는 보도자료 배포처는 모두 제한되거나 불명확하다. 따라서 첫 버전은 공식 피드만으로 시작하고, 보도자료 배포처를 쓸지는 사용자가 이용 조건을 보고 정한다. 개인 열람 수준(제목과 링크만 로컬에 저장하고 AI에 보내지 않음)으로 쓰는 방안도 선택지로 둔다.
