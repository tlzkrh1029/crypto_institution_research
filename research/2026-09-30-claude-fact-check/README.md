# 2026-09-30 Claude Code 사실 확인과 정정 내역

- 작성 도구: Claude Code (claude.ai/code 클라우드 세션). 검토 에이전트 7개와, 관점마다 지적 사항을 반박해 보는 검증 에이전트 7개를 함께 실행했다.
- 작성 시각: 2026-09-30 14:30 KST 전후 (검토 실행은 13:20~14:20 KST)
- 조사 범위: 첫 커밋(dc05f77)에 담긴 모든 문서의 사실 주장, 문서 사이의 일관성, 한국어 문체, 다른 AI 도구 관점의 사용성, 공개 저장소 관점의 안전성. 기관 연결 10건의 원문을 직접 열어 확인했다. 수집원은 곳마다 작동 여부나 이용 조건을 직접 확인했고, 수집원별로 확인한 범위는 아래 "수집원과 이용 조건" 표에 적었다 (PR Newswire, Business Wire, GlobeNewswire, 업비트, 코인베이스는 이용 조건을 확인하지 않았다).
- 조사하지 못한 범위: 아래 "확인하지 못한 것" 절에 적었다.
- 반영 방식: 검증 에이전트가 반박한 지적 사항은 반영하지 않았다. 부분적으로 맞다고 판단된 지적은 검증 에이전트가 고친 수정안으로 반영했다. 첫 커밋 이후 같은 날의 초안 정정이므로 원 파일을 직접 고쳤다 (D-008). 고치기 전 내용은 git 이력에 있다.

## 확인 결과

### 기관 연결

기관 연결 10건의 상세 내용은 [docs/institution-map.md](../../docs/institution-map.md)에 반영했다. 첫 초안과 달라진 핵심 사실은 다음과 같다.

| 항목 | 확인 결과 | 원문 |
|---|---|---|
| DTCC·Chainlink | 2026-05-12 발표다. 9월의 새 발표가 아니라 2026-09-28 Sibos 무대에서 다시 소개된 재확산이다. Collateral AppChain의 가동 목표는 2026년 4분기다. | [DTCC](https://www.dtcc.com/press-releases/2026/dtcc-collaborates-with-chainlink-to-advance-24-7-collateral-management), [Chainlink](https://chain.link/blog/sibos-2026-recap) |
| Chainlink·Swift | Chainlink 단독 발표다 (2026-09-28 16:53 ET). 이용 기관은 밝히지 않았고, 같은 날 Oracle도 Swift 원장 연동을 발표했다. | [PR Newswire](https://www.prnewswire.com/news-releases/chainlink-is-enabling-financial-institutions-to-connect-to-swifts-blockchain-ledger-302891972.html), [Oracle](https://www.oracle.com/europe/news/announcement/oracle-integration-with-swifts-ledger-helps-banks-connect-tokenized-deposit-infrastructures-across-institutions-2026-09-28/) |
| DTCC Fund/SERV·Ondo | 2026-09-16의 새 발표다. 회원 가입 단계이며 실제 상품 배포는 원문에 없다. | [DTCC](https://www.dtcc.com/press-releases/2026/DTCC-FundSERV-Adds-Ondo-Finance-as-First-Tokenization-Member) |
| U.S. Bank·Stellar | U.S. Bank가 2026-09-09에 USBDC 실거래 파일럿을 Stellar에서 완료했다고 직접 발표했다. 첫 초안은 이 연결을 "원문 없음"으로 제외했는데, 이는 틀렸다. | [U.S. Bank](https://www.usbank.com/about-us-bank/news-and-stories/article-library/us-bank-launches-usbdc-stablecoin.html) |
| U.S. Bank와 BVNK | 두 회사의 사업 관계를 밝힌 원문은 찾지 못했다. Codex 문서의 "U.S. Bank/BVNK → Stellar"는 별개의 두 발표를 한 줄로 적은 것이다. | 검색 |
| BVNK·Stellar | 2026-09-22 발표이며 전 기업 고객에게 가동되었다. BVNK는 2026-08-03부터 Mastercard 자회사다. | [BVNK](https://www.bvnk.com/press/bvnk-expands-multi-chain-stablecoin-infrastructure-with-stellar-integration) |
| Bybit·Franklin Templeton | 2026-09-28 발표이며 Stellar와 XLM이 나오지 않는다. | [PR Newswire](https://www.prnewswire.com/news-releases/bybit-and-franklin-templeton-form-strategic-collaboration-to-expand-access-to-tokenized-investing-302891429.html) |
| Hedera CLPR | 2026-09-24 LFDT와 Hedera가 각각 발표했다. 코드 기여 단계다. | [Hedera](https://hedera.com/blog/hedera-contributes-hashgraph-developed-clpr-to-lfdt/), [LFDT](https://www.lfdecentralizedtrust.org/announcements/lf-decentralized-trust-adds-swift-wells-fargo-and-13-additional-new-members) |
| NVIDIA·Hedera | NVIDIA 발표문에는 Hedera가 없다. Hedera Council 구성사가 참여한 데 따른 연상이다. | [NVIDIA](https://nvidianews.nvidia.com/news/open-agent-safety-platform) |
| IBM·Hedera (IDTrust) | Codex 문서의 "IBM 제품 유통"은 THG의 IDTrust가 IBM Cloud Catalog에 등재된 일(2026-09-23)이다. 간접 연결이다. | [PR Newswire](https://www.prnewswire.com/news-releases/thg-and-ibm-sign-global-partnership-to-bring-idtrust-as-agentic-ai-identity-solution-on-ibm-cloud-catalog-as-know-your-agent-kya-becomes-an-enterprise-priority-302887805.html) |
| Bank of England·Stellar | Codex 문서의 "영국 중앙은행 실험"은 Nuvanté의 시제품 시험이다 (Stellar 사이트 2026-09-03 게시). | [Stellar](https://stellar.org/press/nuvante-technologies-announces-stablecoin-clearing-prototype-built-on-stellar-network-integrated-to-bank-of-england-rtgs) |

### 시장 자료

| 항목 | 확인 결과 |
|---|---|
| ETF 유입 수치 | LINK 약 1,335만 달러, HBAR 약 85만 달러는 2026-08-24로 끝난 주의 수치다. 첫 초안은 "2026년 9월 중순 한 주"로 잘못 적었고, 수치가 없는 다른 KuCoin 게시물을 출처로 연결했다. |
| 재측정 제외 목록 | 스테이블코인과 펀드·RWA 토큰 10개가 빠져 있었고, 거버넌스 토큰 ETHFI가 잘못 제외되었다. 고친 뒤 구간 표를 다시 계산했다. 결론(상위 10위권의 상대적 약세, LINK·XLM이 11~50위 중앙값과 비슷함)은 바뀌지 않았다. |
| 구간 설명 | 첫 초안은 "제외 후 남은 상위 100개"라고 적었지만, 실제 계산은 원래 순위 1~100위에서 제외 대상을 뺀 방식이었다. |
| QNT 상장 여부 | 업비트에는 QNT 시장이 없다. 빗썸과 코인원의 원화 시장에도 없다. |
| Sibos 2026 | 2026-09-28~10-01, 마이애미. 마이애미 개최는 처음이지만, 미국 개최는 처음이 아니다 (검색 결과 기준 Atlanta 2004, Boston 2007과 2014). |

### 수집원과 이용 조건

| 수집원 | 확인 결과 (2026-09-30) |
|---|---|
| X | 이용약관이 사전 서면 동의 없는 크롤링과 스크래핑을 금지한다. API 게시물 읽기는 1건당 $0.005다. |
| 텔레그램 | API 약관 1.5항과 콘텐츠 이용 약관이 텔레그램 데이터를 AI의 학습, 개발, 배포에 쓰는 것과 통상적인 이용을 벗어난 콘텐츠 접근을 금지한다. 첫 초안의 "약관 문제 없이"는 틀렸다. |
| Google News RSS | 피드에 개인 피드 리더에서 개인적·비상업적으로 표시하는 용도 외의 사용을 금지한다고 적혀 있다. 항목 링크는 중계 주소다. |
| FinancialJuice | 이용약관이 서면 허락 없는 자동 수집과 집계를 금지한다. 공식 RSS가 있지만 같은 조항을 적용받는 것으로 본다. |
| CoinMarketCap | 이용약관이 스크래핑과 자동 수집을 금지한다. Codex 원본의 HTML 파싱 방법은 반복하지 않는다. |
| CoinGecko | Demo 키 한도는 분당 100회, 월 10,000회다. 출처 표기("Powered by CoinGecko")가 필요하고, 데이터 저장을 권장하지 않는다. 이 저장소의 재측정 문서와 CSV 설명에 출처 표기를 추가했다. |
| DTCC | 공식 RSS 목록에 보도자료 피드가 없다. 사이트맵으로 새 보도자료를 확인할 수 있다. |
| SEC | 보도자료와 발언 RSS, EDGAR 최신 공시 Atom 피드가 작동한다. 공정 접근 정책은 User-Agent 선언과 초당 10건 이하를 요구한다. 19b-4는 EDGAR에 올라오지 않는다. |
| 연준 | 공식 RSS가 작동한다. |
| PR Newswire, Business Wire, GlobeNewswire | RSS가 작동한다. 이용 조건은 확인하지 않았다. |
| 업비트, 코인베이스 | 인증 없이 공개 API가 작동한다. 이용 조건은 확인하지 않았다. |
| 바이낸스, 바이빗 | 미국 소재 클라우드 환경에서 각각 HTTP 451(약관의 지역 제한), HTTP 403(국가 차단)으로 거부되었다. |
| healthchecks.io | 무료 요금제로 작업 20개까지 감시할 수 있다. |

### AI 도구와 실행 환경

| 항목 | 확인 결과 (2026-09-30) |
|---|---|
| AGENTS.md 지원 | Codex(CLI, 클라우드), Cursor, GitHub Copilot 코딩 에이전트는 AGENTS.md를 읽는다. Gemini CLI는 기본적으로 GEMINI.md를 읽으므로 AGENTS.md를 불러오는 GEMINI.md를 추가했다 (D-007). |
| Claude Code | CLAUDE.md 안의 `@AGENTS.md` 불러오기는 공식 문서의 권장 방식과 같다. |
| 구독 CLI | `claude -p`와 `codex exec`는 구독 사용 한도에서 차감된다. Anthropic은 `claude -p` 사용량을 별도 크레딧으로 옮기는 변경을 발표했다가 보류했다. |
| macOS | LaunchAgent는 로그인한 뒤에만 실행되고, FileVault가 켜져 있으면 자동 로그인을 쓸 수 없다. Apple Silicon 맥북은 전원에 연결되면 자동으로 켜진다. macOS Tahoe 26.4 이상에는 충전 한도 기능이 있다. |
| 카카오톡 "나에게 보내기" | 휴대전화 알림이 오지 않는다 (카카오 데브톡의 카카오 담당자 답변). 리프레시 토큰은 2개월 동안 유효하다. |
| GitHub Actions | 예약 실행은 지연되거나 누락될 수 있고, 공개 저장소에서 60일 동안 활동이 없으면 꺼진다. |

## 정정한 파일

| 파일 | 정정 내용 |
|---|---|
| docs/institution-map.md | 모든 연결을 원문으로 확인해 다시 썼다. U.S. Bank, IBM, Bank of England 연결을 추가하고, 연결로 인정하지 않은 항목을 보강했다. |
| docs/hypotheses.md | ETF 자료의 기간, XRP 서술, 사후 예시 종목의 표시를 고쳤다. H3과 H5에 빠진 기각·약화 조건을 추가했다. 매매 지시로 읽힐 수 있는 H1 규칙 후보의 문구를 고쳤다. "다음 확인" 날짜를 구체적으로 적었다. |
| docs/collector-spec.md | 수집원 표를 확인 결과로 다시 썼다. 텔레그램과 Google News RSS를 보류로 옮기고, CMC 스크래핑 금지를 추가했다. CoinGecko 한도와 출처 표기, SEC 조건, 실행 환경 서술을 고쳤다. |
| docs/decisions.md | 확정과 잠정의 기준을 명확히 했다. D-006에서 텔레그램을 보류로 바꾸고, D-007과 D-008을 추가했다. |
| docs/open-questions.md | Q3(카카오 알림), Q5(브랜치 현황), Q6(추가 위치)을 고쳤다. Q10과 Q11을 추가했다. |
| docs/research-principles.md | 문장을 다듬고, "선정·협약 전" 단계를 정의했다. |
| AGENTS.md, README.md, GEMINI.md, .gitignore | 브랜치와 PR 규칙, 미결 사항 처리, 읽기 순서, 비밀 값 범위, 폴더 이름 규칙을 보완했다. GEMINI.md를 추가하고, .gitignore에 세션 파일, 로그, SQLite 보조 파일을 추가했다. |
| research/2026-09-30-claude-review/ | ETF 자료의 기간과 출처, 제외 목록과 구간 표, 텔레그램과 Google News RSS 서술, 일부 문장을 고쳤다. CoinGecko 출처 표기를 추가했다. |
| research/2026-09-29-codex-meta-ideas/README.md, codex-answers-digest.md | 조사 범위와 이용 시 주의 사항을 추가하고, 요지 문서의 문장과 검토 문구를 고쳤다. 원본 문서(research-and-ideas.md)는 고치지 않았다. |

## 2차 점검 (같은 날)

정정 커밋(059aef7)에서 새로 쓴 문장을 검토 에이전트 2개와 반박 검증 에이전트 2개로 다시 점검했고, 확인된 지적 16건을 반영했다. 주요 내용은 다음과 같다.

- LFDT와 Hedera(CLPR)의 연결 등급을 "직접"에서 "확인 필요"로 바꿨다. 관계의 내용이 코드 기여이며 네트워크 선정이나 사용이 아니어서, "직접"의 정의와 "선정·협약 전" 단계가 서로 맞지 않았다.
- hypotheses.md의 XRP 서술에서 "최근 7일"을 측정 구간(2026-09-23 12:39~2026-09-30 12:39 KST)으로 바꿨다.
- 이 문서의 조사 범위 서술이 실제로 확인한 범위보다 넓게 적혀 있어서 고쳤다.
- D-008에 지침 성격의 문서도 PR 없이 고쳤다는 사실을 추가했다.
- CoinGecko와 CMC 약관 서술에 원문 링크를 추가하고, 문장 여러 개를 다듬었다.

## 반영하지 않은 지적

검증 에이전트가 반박한 지적은 반영하지 않았다.

- README의 Claude Code 행을 버전별 설명으로 바꾸자는 지적: 현재 설명이 공식 문서의 권장 구성과 같다.
- D-001의 이유를 고치자는 지적: 이 저장소 구성에서 "Claude Code는 CLAUDE.md를 읽는다"는 서술은 맞다.
- Codex 답변 요지의 시각이 원본과 맞지 않는다는 지적: 12:30을 질문 시각으로 보면 모든 시각이 맞는다. 요지 문서에 시각의 뜻을 적었다.
- research 폴더마다 투자 권유가 아니라는 문구를 넣자는 지적: README와 AGENTS.md에 이미 있고, research 문서에 매매 권유 표현이 없다.
- 재측정 문서의 "예를 들어" 문장을 바꾸자는 지적: 원래 문장이 맞다.

## 확인하지 못한 것

- swift.com은 접속이 거부되어(HTTP 403) Swift 측 발표와 Sibos 안내 페이지를 확인하지 못했다.
- 바이낸스 이용약관 페이지는 본문을 읽을 수 없어, 한국이 제한 지역인지 확인하지 못했다.
- 2026년 9월 하순의 ETF 흐름은 운용사 원자료로 확인하지 못했다.
- 카카오톡 "나에게 보내기"의 알림 여부는 공식 문서가 아니라 개발자 포럼의 카카오 담당자 답변으로 확인했다.
- Hedera의 X 게시물은 crypto.news 인용으로만 확인했다.
- Apple Silicon 맥북에서 `pmset autorestart`가 어떻게 동작하는지는 Apple 공식 자료로 확인하지 못했다.
