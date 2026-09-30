# 2026-09-30 Claude Code 프로젝트 공식 피드 점검

- 작성 도구: Claude Code (claude.ai/code 클라우드 세션). 피드와 약관 확인에는 조사 에이전트 하나를 함께 썼고, 수집원에 추가한 두 곳(Hedera, Stellar)은 Claude Code가 피드와 약관 문구를 다시 확인했다.
- 작성 시각: 2026-09-30 18:45 KST 전후
- 조사 범위: 관심 표본 프로젝트(Chainlink, Hedera, Stellar, Quant, Ondo)와 같은 서사의 대조군(Ripple)이 직접 운영하는 블로그와 보도자료 페이지에 수집 프로그램이 쓸 수 있는 RSS·Atom 피드가 있는지, 그 사이트의 robots.txt와 이용약관이 수집 프로그램의 사용 방식을 허용하는지
- 조사하지 못한 범위: 아래 "확인하지 못한 것" 절에 적었다.
- 접속 환경: 미국 소재 클라우드 환경에서 확인했다. 한국에서 접속할 때 차단 여부가 다를 수 있다.

판정 기준은 [2026-09-30 데이터 출처 점검](../2026-09-30-claude-data-source-check/README.md)과 같다. 수집 프로그램은 개인·비상업적 용도로, 10~30분마다 조건부 요청(ETag, If-Modified-Since)으로 피드를 확인하고, 제목, 링크, 날짜를 로컬 데이터베이스에 저장한다. 공개 저장소에는 원문을 옮기지 않고 링크와 자체 분석만 올린다.

## 결과

| 프로젝트 | 피드 | robots.txt | 이용약관 | 판정 | 처리 |
|---|---|---|---|---|---|
| Hedera | `https://hedera.com/feed/` (블로그 페이지의 `<link rel="alternate">`로 공개된 WordPress 피드, 10건, 모두 날짜 있음, ETag와 Last-Modified 지원) | 모든 경로 허용, `Crawl-delay: 10` | [이용약관](https://hedera.com/terms/) (2025-11-24 수정): 사이트 접근과 이용을 허락한다. 상업적 목적으로 복제·배포하는 것만 금지하며, 자동 접근이나 AI 이용에 대한 조항은 없다 | 가능 | 수집원에 추가 (`hedera-blog`) |
| Stellar | `https://stellar.org/blog/rss.xml` (블로그 페이지의 `<link rel="alternate">`로 공개, 10건, 모두 날짜 있음, 조건부 요청 미지원) | 피드 경로 허용 | [이용약관](https://stellar.org/terms-of-service) (2026-03-23 시행): "personal, non-commercial use only". 명시적 허락 없이 상업적 또는 공개 목적으로 복제, 게시, 배포하는 것을 금지한다. 자동 접근 금지 조항은 없고, 다른 사람에 대한 정보 수집만 금지한다 | 조건부 가능 | 수집원에 추가 (`stellar-blog`). 공개 기록에는 링크만 남긴다 |
| Chainlink | 블로그 피드는 없다. 보도자료 피드 `https://chain.link/press-releases/rss.xml`가 있지만 chain.link에서 안내하지 않는다 (100건, 날짜만 있고 시각은 없음, Last-Modified 지원). 뉴스 피드 `/chainlink-news/rss.xml`은 robots.txt가 막는다 | 보도자료 경로 허용, `/chainlink-news/*` 금지 | [Chainlink Foundation 이용약관](https://chain.link/terms) (v6.0, 2026-08-18 시행): "robot, spider, crawler, scraper, or other automated means or interface not provided by us"로 접근하는 것을 금지한다 | 불명확 | 추가하지 않음 (Q10) |
| Quant | `https://quant.network/feed/` (WordPress 기본 피드, 10건) | 모든 경로 허용 | [이용약관](https://quant.network/terms-of-use/) (날짜 표시 없음): 개인적 이용만 허락하고, 사이트나 자료를 "store ... in any way" 하는 것을 금지한다 | 제한 | 추가하지 않음 (Q10) |
| Ondo | 없음. 사이트맵만 있다 | 모든 경로 허용 | [이용약관](https://docs.ondo.finance/legal/terms-of-service) (2026-02-02 갱신) 5.5항: Ondo가 제공하지 않은 자동화 수단으로 접근하거나 데이터를 추출하는 것을 금지한다 | 제한 | 추가하지 않음 (Q10) |
| Ripple (대조군) | 없음. 보도자료 사이트맵(`/sitemap/press-release.xml`)만 있다 | 대부분 허용 | [이용약관](https://ripple.com/legal/terms-of-use/) (2019-05-10 개정): 이용 허락 범위에서 "data mining, robots or similar data gathering or extraction methods"를 제외한다 | 제한 | 추가하지 않음 (Q10) |

여섯 곳 모두 Medium, Substack 같은 외부 플랫폼이 아니라 자기 도메인에서 사이트를 운영한다. 여섯 곳의 약관 가운데 사이트 콘텐츠를 AI에 이용하는 것을 다룬 조항은 없었다.

## 수집원에 추가한 뒤 확인한 결과

2026-09-30 18:33 KST에 수집 프로그램으로 두 피드를 한 번씩 확인했다. 두 피드 모두 10건을 읽었고, 각각 1건이 사건이 되었다. 사건이 된 글은 Hedera 피드에서 LFDT(기관)가 함께 대조된 글, Stellar 피드에서 U.S. Bank(기관)가 함께 대조된 글이다. 나머지 18건은 발행 프로젝트만 대조되었으므로 사건을 만들지 않고 items에만 남았다. 이 규칙은 [collector-spec.md](../../docs/collector-spec.md) 5절에 적었다. 요약문(excerpt)은 저장하지 않았다.

## 비교할 때 주의할 점

프로젝트 쪽 발표를 자동으로 받는 종목은 HBAR와 XLM뿐이다. LINK, QNT, ONDO와 대조군 XRP는 프로젝트 쪽 피드를 받지 못한다. 따라서 수집원 구성 때문에 HBAR와 XLM의 사건이 더 많이 기록될 수 있다. 종목별 사건 수나 반응을 비교할 때는 모든 종목에 똑같이 적용되는 수집원(규제기관과 기관의 피드)에서 나온 사건만 쓰거나, 사건의 출처를 함께 표시해 비교한다. 이 비대칭은 Q10을 정할 때 함께 고려한다.

## 바이낸스 접속

- 사용자가 설치 장소에서 `https://api.binance.com/api/v3/ping`을 호출해 HTTP 200을 받았다고 알렸다 (2026-09-30). 설치 장소에서 바이낸스 API에 접속할 수 있다는 뜻이다.
- 설치 장소가 [바이낸스 이용약관](https://www.binance.com/en/terms)의 이용 자격(Eligibility) 조항에 맞는지는 확인하지 못했다. 약관 페이지가 이 환경에서 자동화 차단 확인 화면(HTTP 202, `x-amzn-waf-action: challenge`)을 돌려주었고, 본문이 브라우저에서만 그려지기 때문이다. 바이낸스 데이터를 쓰기 전에 사용자가 브라우저로 이 조항과 금지 국가 목록을 확인해야 한다.

## 확인하지 못한 것

- Quant 블로그 페이지가 `/feed/`를 안내하는지. HTML 페이지가 Cloudflare 확인 화면(HTTP 403)을 돌려주어 열지 못했다. 한국에서 접속할 때도 같은지 확인하지 못했다.
- Chainlink가 보도자료 RSS를 공개 인터페이스로 의도했는지. chain.link에는 이 피드로 가는 링크가 없다.
- Chainlink 블로그 피드와, Stellar Development Foundation의 보도자료 전용 피드. 찾지 못했다.
- Quant 이용약관의 갱신 날짜. 페이지에 표시되어 있지 않다.
- chainlinklabs.com의 이용약관
- 바이낸스 이용 자격 조항과 금지 국가 목록
