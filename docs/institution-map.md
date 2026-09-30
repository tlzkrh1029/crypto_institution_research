# 기관·업무·프로젝트·토큰 연결표

이 문서는 기관과 프로젝트, 토큰 사이의 연결을 기록한다. 작성 규칙은 다음과 같다.

- 원문 링크가 있는 연결만 넣는다. 원문을 직접 열어 보지 못한 항목은 "확인" 칸에 "미확인"으로 표시하고, 연결이 인정된 것으로 보지 않는다. 미확인 항목을 알림 기준이나 가설 검증에 쓰기 전에 원문을 확인한다.
- 연결 등급은 [research-principles.md](research-principles.md) 2절의 등급(직접, 프로젝트 측 발표, 간접) 가운데 하나를 쓴다. 판단할 수 없으면 "확인 필요"로 적는다. 연상 등급은 연결로 인정하지 않으므로 아래 "연결로 인정하지 않은 항목"에 적는다.
- 사업 단계는 research-principles.md 4절의 단계 가운데 하나를 쓴다. 해당하는 단계가 없거나 판단할 수 없으면 "확인 필요"로 적고, 괄호 안에 설명과 그 출처를 붙인다.
- 발표일에는 원문의 발표 시각을 KST로 바꿔 적고, 괄호 안에 원문의 날짜·시각과 시간대를 함께 적는다. 예: 2026-09-29 05:53 KST (원문 2026-09-28 16:53 ET). 원문에 시각이 없으면 원문에 적힌 날짜만 적는다. 원문의 시간대 표기가 날짜와 맞지 않으면(예: 서머타임 기간의 "EST") 원문 표기를 그대로 옮기고 KST 변환은 생략한다.
- 기관과 사업 관계가 있다고 해서 토큰 보유자에게 경제적 이익이 돌아간다는 뜻은 아니므로, "토큰 언급" 항목을 따로 둔다.
- "확인" 칸에는 확인한 날짜와 도구를 적는다.
- "기능 분류"는 [hypotheses.md](hypotheses.md) H5 검증을 위해 Claude Code가 붙인 분류다 (담보, 결제·이동, 유통·상환, 신원·규정·프라이버시).

## 요약

| 기관 | 프로젝트·네트워크 | 토큰 | 연결 등급 | 사업 단계 | 발표일 |
|---|---|---|---|---|---|
| The Clearing House | Quant | QNT | 직접 | 선정·협약 | 2026-09-24 |
| Swift (원장) | Chainlink | LINK | 프로젝트 측 발표 | 선정·협약 전 | 2026-09-29 05:53 KST |
| DTCC | Chainlink | LINK | 직접 | 선정·협약 (09-28 Sibos 소개는 재확산) | 2026-05-12 |
| DTCC Fund/SERV | Ondo Finance | ONDO | 직접 | 선정·협약 (회원 가입) | 2026-09-16 |
| BVNK | Stellar | XLM | 직접 (BVNK 고객에게는 간접) | 가동 | 2026-09-22 |
| U.S. Bank | Stellar | XLM | 직접 | 시험 | 2026-09-09 |
| Bybit, Franklin Templeton | Benji 플랫폼, Mantle | 없음 | 직접 (Bybit와 Benji 사이) | 가동 (담보 프로그램) | 2026-09-28 21:00 KST |
| LF Decentralized Trust | Hedera (CLPR) | HBAR | 확인 필요 (LFDT의 코드 기여 수용, 네트워크 선정·사용 아님) | 선정·협약 전 | 2026-09-24 |
| IBM | Hedera (THG IDTrust) | HBAR | 간접 | 가동 (카탈로그 등재) | 2026-09-23 23:02 KST |
| Bank of England Synchronisation Lab | Stellar (Nuvanté 시제품) | XLM | 프로젝트 측 발표 | 시험 | 2026-09-03 |

## 연결별 상세

### The Clearing House와 Quant

- 업무: 토큰화 예금의 청산·결제 네트워크(On-Chain Money Initiative). Quant가 상호운용성, 오케스트레이션, 거래 관리 계층을 맡고, RTP와 CHIPS에 연결한다.
- 발표 주체: 기관 (TCH)
- 연결 등급: 직접
- 사업 단계: 선정·협약. 참여기관 제공 목표는 2027년 상반기다.
- 토큰 언급: 없음 (QNT와 Overledger 모두 원문에 없음)
- 발표일: 2026-09-24
- 기능 분류: 결제·이동
- 원문: [TCH](https://www.theclearinghouse.org/payment-systems/Articles/2026/09/The-Clearing-House-Partners-with-Quant-to-Advance-the--On-Chain-Money-Initiative)
- 확인: 2026-09-30 Claude Code

### Swift 원장과 Chainlink

- 업무: 금융기관이 Chainlink Runtime Environment(CRE)를 통해 자기 시스템과 서명 키를 Swift의 블록체인 공유 원장에 연결해 24/7 토큰화 예금 결제에 참여하는 기능. 독점 연결이 아니다. 같은 날 Oracle도 Swift 원장 연동을 발표했다 ([Oracle](https://www.oracle.com/europe/news/announcement/oracle-integration-with-swifts-ledger-helps-banks-connect-tokenized-deposit-infrastructures-across-institutions-2026-09-28/)).
- 발표 주체: 프로젝트 (Chainlink). 보도자료에 Swift 발언이 없고, Swift 측 발표는 확인하지 못했다 (swift.com 접속 거부).
- 연결 등급: 프로젝트 측 발표
- 사업 단계: 선정·협약 전. Chainlink가 연결 기능을 준비 중이라고 발표했고, 이용 기관은 밝히지 않았다. Swift 원장 자체는 17개 금융기관이 시험 중이다.
- 토큰 언급: 회사 소개문에만 있다. 기업 수입을 LINK로 전환해 Chainlink Reserve에 보관한다는 일반 설명이며, 이 연결에 LINK를 쓴다는 내용은 없다.
- 발표일: 2026-09-29 05:53 KST (원문 2026-09-28 16:53 ET, 마이애미)
- 기능 분류: 결제·이동
- 원문: [PR Newswire](https://www.prnewswire.com/news-releases/chainlink-is-enabling-financial-institutions-to-connect-to-swifts-blockchain-ledger-302891972.html)
- 확인: 2026-09-30 Claude Code

### DTCC와 Chainlink

- 업무: 24/7 담보 관리. DTCC의 Collateral AppChain에 Chainlink CRE와 데이터 표준을 통합한다.
- 발표 주체: 기관 (DTCC)
- 연결 등급: 직접
- 사업 단계: 선정·협약. Collateral AppChain의 가동 목표는 2026년 4분기다. 2026-09-28 Sibos 무대에서 DTCC와 Chainlink가 이 협업을 다시 소개했는데, 새 발표가 아니므로 재확산으로 기록한다 ([Chainlink Sibos 정리](https://chain.link/blog/sibos-2026-recap), 2026-09-29).
- 토큰 언급: 회사 소개문에만 있다. 기업 수입을 LINK로 전환한다는 Chainlink의 일반 설명이며, 이 거래에 LINK를 쓴다는 내용은 없다.
- 발표일: 2026-05-12
- 기능 분류: 담보
- 원문: [DTCC](https://www.dtcc.com/press-releases/2026/dtcc-collaborates-with-chainlink-to-advance-24-7-collateral-management)
- 확인: 2026-09-30 Claude Code

### DTCC Fund/SERV와 Ondo Finance

- 업무: 토큰화 펀드 유통. Ondo의 자회사이자 SEC 등록 브로커딜러인 Oasis Pro Markets가 Fund/SERV의 첫 토큰화 회원으로 가입했다.
- 발표 주체: 기관과 프로젝트 공동 (DTCC 사이트에 게시)
- 연결 등급: 직접
- 사업 단계: 선정·협약 (회원 가입 완료). Fund/SERV를 거친 실제 상품 배포와 거래는 원문에 없다.
- 토큰 언급: 없음
- 발표일: 2026-09-16
- 기능 분류: 유통·상환
- 원문: [DTCC](https://www.dtcc.com/press-releases/2026/DTCC-FundSERV-Adds-Ondo-Finance-as-First-Tokenization-Member)
- 확인: 2026-09-30 Claude Code

### BVNK와 Stellar

- 업무: 기업 고객의 스테이블코인 지급·송금 경로에 Stellar를 추가했다. BVNK는 2026-08-03부터 Mastercard의 자회사다.
- 발표 주체: 중개사 (BVNK). Stellar Development Foundation CEO의 발언을 인용했다.
- 연결 등급: 직접 (BVNK가 스스로 발표). BVNK의 고객 기관과 Stellar의 관계는 간접이다.
- 사업 단계: 가동. 130여 개국의 BVNK 기업 고객 전체에 적용되었다. Stellar 경로의 거래액은 공개되지 않았다.
- 토큰 언급: 없음
- 발표일: 2026-09-22 (원문 표기 "8am EST". 서머타임 기간의 EST 표기이므로 KST 변환은 생략)
- 기능 분류: 결제·이동
- 원문: [BVNK](https://www.bvnk.com/press/bvnk-expands-multi-chain-stablecoin-infrastructure-with-stellar-integration)
- 확인: 2026-09-30 Claude Code

### U.S. Bank와 Stellar

- 업무: 자체 달러 스테이블코인 USBDC의 발행과 국가 간 지급 시험. 북미와 유럽의 U.S. Bank 법인 사이에서 실거래 1건을 처리했고, 발행, 상환, 동결, 회수 기능을 시험했다.
- 발표 주체: 기관 (U.S. Bank)
- 연결 등급: 직접
- 사업 단계: 시험. 2026-09-09에 실거래 파일럿 1건을 완료했다. 시험 사실은 2025-11-25 Stellar 블로그가 먼저 알렸다 (U.S. Bank의 Money20/20 팟캐스트 인용, [Stellar](https://stellar.org/blog/ecosystem/u-s-bank-is-testing-custom-stablecoin-issuance-on-the-stellar-network)).
- 토큰 언급: 없음
- 발표일: 2026-09-09
- 기능 분류: 결제·이동
- 원문: [U.S. Bank](https://www.usbank.com/about-us-bank/news-and-stories/article-library/us-bank-launches-usbdc-stablecoin.html)
- 확인: 2026-09-30 Claude Code

### Bybit, Franklin Templeton과 Benji 플랫폼

- 업무: 토큰화 MMF 지분을 거래소 밖(ByCustody)에 보관한 채 담보로 맡기고 USDT·USDC 거래 신용한도를 받는 프로그램. Bybit 거래소와 Mantle 체인의 자산관리 상품도 예고했다.
- 발표 주체: 거래소 (Bybit). Franklin Templeton의 발언을 인용했다.
- 연결 등급: 직접 (Bybit와 Franklin Templeton의 Benji 플랫폼 사이)
- 사업 단계: 가동 (담보 프로그램). 자산관리 상품은 세부 내용이 발표되지 않았다.
- 토큰 언급: 없음. QNT, LINK, XLM, HBAR, ONDO와 연결이 없고, Mantle의 토큰도 원문에 없다. 담보로 쓰는 펀드 지분이 어느 체인에 있는지도 적혀 있지 않다.
- 발표일: 2026-09-28 21:00 KST (원문 2026-09-28 08:00 ET, 두바이)
- 기능 분류: 담보
- 원문: [PR Newswire](https://www.prnewswire.com/news-releases/bybit-and-franklin-templeton-form-strategic-collaboration-to-expand-access-to-tokenized-investing-302891429.html)
- 확인: 2026-09-30 Claude Code

### LF Decentralized Trust와 Hedera (CLPR)

- 업무: 브리지 없는 교차 원장 프로토콜 CLPR의 코드를 LFDT Labs 과제로 받아 공개 개발한다. LFDT는 코드를 맡아 공개 개발하는 오픈소스 재단이며, Hedera 네트워크를 사용하는 기관이 아니다. Hedera는 LFDT의 창립 Premier 회원이다. CLPR 개발사는 Hashgraph이며, Hashgraph가 테스트넷 조기 도입 프로그램(국가 간 결제와 외환, 교차 원장 결제, 담보 이동) 참가자를 모집하고 있다.
- 발표 주체: 프로젝트 (Hedera)와 기관 (LFDT)이 같은 날 각각 발표했다.
- 연결 등급: 확인 필요. LFDT가 CLPR lab 추가를 스스로 발표했지만, 관계의 내용은 코드 기여이며 Hedera의 선정이나 네트워크 사용이 아니므로 research-principles.md 2절의 "직접" 기준에 맞지 않는다.
- 사업 단계: 선정·협약 전. LFDT Labs 단계의 초기 코드 공개이며, 기관의 시험은 아직 시작되지 않았다.
- 토큰 언급: 없음
- 발표일: 2026-09-24
- 기능 분류: 결제·이동
- 원문: [Hedera](https://hedera.com/blog/hedera-contributes-hashgraph-developed-clpr-to-lfdt/), [LFDT](https://www.lfdecentralizedtrust.org/announcements/lf-decentralized-trust-adds-swift-wells-fargo-and-13-additional-new-members)
- 확인: 2026-09-30 Claude Code

### IBM과 Hedera (IDTrust)

- 업무: AI 에이전트 신원 관리 SaaS인 The Hashgraph Group(THG)의 IDTrust를 IBM Cloud Catalog에 등재했다. THG는 IBM과 Embedded Solution Agreement를 맺고 IBM Silver Partner가 되었다. IDTrust는 Hedera 위에 구축되었다. THG는 스위스 회사이며, CLPR 개발사 Hashgraph와 다른 회사다.
- 발표 주체: 파트너사 (THG). IBM 파트너 생태계 부사장(DACH)의 발언을 인용했다. IBM 측 발표는 찾지 못했다.
- 연결 등급: 간접 (IBM → THG → Hedera)
- 사업 단계: 가동 (카탈로그 등재). 실제 고객과 거래액은 원문에 없다.
- 토큰 언급: 없음
- 발표일: 2026-09-23 23:02 KST (원문 2026-09-23 10:02 ET)
- 기능 분류: 신원·규정·프라이버시
- 원문: [PR Newswire](https://www.prnewswire.com/news-releases/thg-and-ibm-sign-global-partnership-to-bring-idtrust-as-agentic-ai-identity-solution-on-ibm-cloud-catalog-as-know-your-agent-kya-becomes-an-enterprise-priority-302887805.html)
- 확인: 2026-09-30 Claude Code

### Bank of England Synchronisation Lab과 Stellar

- 업무: Nuvanté Technologies가 Stellar로 만든 스테이블코인 청산 시제품을 Bank of England RTGS 동기화 실험 환경(Synchronisation Lab)에서 시험했다. Codex 문서가 XLM 근거로 든 "영국 중앙은행 실험"이 이 항목이다.
- 발표 주체: 프로젝트 (Nuvanté, Stellar 사이트에 게시). Bank of England 측 발표는 확인하지 못했다.
- 연결 등급: 프로젝트 측 발표
- 사업 단계: 시험 (실험 환경의 시제품)
- 토큰 언급: 없음
- 발표일: 2026-09-03 (Stellar 사이트 게시일)
- 기능 분류: 결제·이동
- 원문: [Stellar](https://stellar.org/press/nuvante-technologies-announces-stablecoin-clearing-prototype-built-on-stellar-network-integrated-to-bank-of-england-rtgs)
- 확인: 2026-09-30 Claude Code

## 연결로 인정하지 않은 항목

| 항목 | 이유 | 확인 |
|---|---|---|
| NVIDIA와 Hedera | NVIDIA의 2026-09-28 Open Agent Safety Platform 발표문은 Hedera, Hashgraph, HBAR, 블록체인을 언급하지 않는다. 발표문에 참여 기업으로 나오는 Accenture, Dell Technologies, IBM, ServiceNow는 Hedera Council 구성사이고, Hitachi Energy는 구성사인 Hitachi의 계열사다. NVIDIA는 Hedera Council 구성사 목록에 없다. 같은 날 Hedera가 X에 "Great to see Hedera Council representation on the NVIDIA Open Agent Safety Platform"이라고 올렸다. 연결 등급은 연상이다. | 2026-09-30 Claude Code ([NVIDIA](https://nvidianews.nvidia.com/news/open-agent-safety-platform), [Hedera Council](https://hederacouncil.org/). Hedera의 X 게시물은 [crypto.news](https://crypto.news/hedera-price-jumps-30-percent-ai-post-draws-attention/) 인용으로만 확인) |
| U.S. Bank와 BVNK | Codex 문서의 "U.S. Bank/BVNK → Stellar"는 U.S. Bank의 USBDC 파일럿(2026-09-09)과 BVNK의 Stellar 통합(2026-09-22)이라는 별개의 두 발표를 한 줄로 적은 것이다. 두 회사의 사업 관계를 밝힌 원문은 찾지 못했다. | 2026-09-30 Claude Code (검색) |
| Bybit·Franklin Templeton과 Stellar | 2026-09-28 Bybit 보도자료에는 Stellar와 XLM이 나오지 않고, 담보로 쓰는 펀드 지분이 어느 체인에 있는지도 적혀 있지 않다. 연결 등급은 연상이다. | 2026-09-30 Claude Code |
| Swift, Wells Fargo와 Hedera | 2026-09-24 LFDT 발표는 CLPR lab 추가와 함께 Swift, Wells Fargo 등 신규 회원 15곳을 알렸다. 같은 재단의 회원이라는 사실만으로는 Hedera와 사업 관계가 있다고 볼 수 없다. 연결 등급은 연상이다. | 2026-09-30 Claude Code |

## 다음 확인 조건

| 토큰 | 다음으로 확인할 변화 |
|---|---|
| QNT | TCH 참여기관 명단, 실서비스 개시, 처음 확인되는 거래, 계약에서 QNT가 맡는 역할 |
| LINK | Swift 원장 연결을 실제로 쓰는 기관, DTCC Collateral AppChain의 2026년 4분기 가동 여부, 유료 사용과 관련 수입의 LINK 전환 증거 |
| XLM | BVNK를 거친 실제 Stellar 거래액, U.S. Bank USBDC가 자사 법인 간 파일럿에서 고객 거래로 넓어지는지, Bank of England 실험 이후의 후속 발표 |
| HBAR | CLPR이 LFDT Labs 단계를 넘어 기관 시험이나 유료 운영으로 넘어가는지, 조기 도입 프로그램 참가 기관, IDTrust의 실제 고객, 퍼블릭 네트워크의 HBAR 사용 여부 |
| ONDO | Fund/SERV를 통한 실제 상품 배포와 판매, 토큰 귀속 구조의 변화 |
