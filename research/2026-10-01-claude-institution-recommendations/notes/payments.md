# 결제사·핀테크·스테이블코인 발행사 엔터티 추가 후보 (payments)

작성 도구는 Claude Code(Opus 5.5)이고, 작성 시각은 2026-10-01 12시 무렵(KST)이다. 조사 범위는 이미 추적 중인 기관(BVNK, Visa, Mastercard, PayPal, Stripe(Bridge, Tempo 포함), MoneyGram, Western Union, Circle, Paxos, Block, Revolut, Tether)을 제외한 결제 처리사, 결제 네트워크, 송금사, 플랫폼 기업, 핀테크, 스테이블코인 발행사와 인프라 기업이다. 은행, 자산운용사, 거래소, 규제기관은 다른 조사자가 맡으므로, 겹치는 기관(SoFi, Capital One, Anchorage Digital, OSL 등)은 겹친다는 사실만 적었다. 세션 전체의 웹 검색 한도(200회)에 도달해서 Rakuten, LINE·Kaia, Apple, Amazon·Walmart의 2026년 동향, Walmart OnePay, SBI VC Trade, Chime, Coupang Pay, Ramp Network, Ebanx, Thunes, Flutterwave, Yellow Card, Corpay, Deel은 검색하지 못했다. 이 항목들은 각 질문의 "공백"에 적었다.

시장 수치(스테이블코인 유통량)는 DefiLlama 스테이블코인 API([stablecoins.llama.fi/stablecoins](https://stablecoins.llama.fi/stablecoins))를 2026-10-01 11:59 KST에 조회한 값이다. 이 값은 측정 시점의 수치이며 현재 상황을 뜻하지 않는다.

우선순위 요약은 아래와 같다. 등급은 이 노트의 추론이며, 근거는 각 질문의 "추론" 표에 있다.

- Must: Fiserv(FIUSD), Zelle·Early Warning Services(ZelleUSD, ZLUSD), SoFi(SoFiUSD), Meta, Open Standard(Open USD, OUSD), World Liberty Financial(USD1), Anchorage Digital, Fireblocks, Ethena Labs(USDe, USDtb), Sky(USDS), Naver Financial(Naver Pay), Kakao Pay·KakaoBank
- Recommended: Global Payments·Worldpay, Shift4, Checkout.com, FIS, Euronet(Ria, Xe), Remitly, Payoneer, Wise, American Express, Klarna, Shopify, Google(Cloud Universal Ledger, AP2), Nubank, Mercado Libre(Mercado Pago, Meli Dólar), Ant International, Grab, StraitsX, Agora(AUSD), Zerohash, MoonPay, Rain, Toss(Viva Republica), PayPay, JPYC
- Optional: Nuvei, dLocal, Airwallex, Adyen, Brex, X Money, Amazon, Walmart, Apple, Figure(YLDS), First Digital(FDUSD), United Stables(U), M0, Brale, Transak, Banxa, Alchemy Pay, MetaMask(mUSD), Phantom(CASH)
- 기존 엔터티에 별칭만 추가할 대상: SBI Shinsei Trust & Banking의 JPYSC(기존 sbi_holdings), Global Dollar Network의 USDG(기존 paxos), Bridge가 발행하는 KlarnaUSD·mUSD·CASH·OUSD(기존 stripe), Ripple의 RLUSD(기존 ripple에 이미 있음)

## 질문 1: 어떤 결제 처리사와 결제 네트워크를 추적해야 하는가 (Fiserv, FIS, Global Payments·Worldpay, Adyen, Checkout.com, Nuvei, Shift4, American Express, Discover·Capital One, Zelle·Early Warning, Euronet·Ria, Remitly, Wise, Payoneer, Airwallex, dLocal)

### 요점 (Takeaway)
2025-2026년에 자체 스테이블코인을 발행했거나 발행을 발표한 곳은 Fiserv(FIUSD), Zelle 운영사 Early Warning Services(ZelleUSD), Payoneer(PAYO-USD 계획)이며, 이 중 Fiserv와 Zelle은 미국 은행망 전체와 연결되므로 Must로 둘 만하다. 나머지 처리사와 송금사(Worldpay, Shift4, Checkout.com, FIS, Euronet, Remitly, Nuvei, dLocal)는 대부분 BVNK, Fireblocks, Bridge, Circle 같은 인프라를 붙여 스테이블코인 정산과 지급을 제공하는 단계이므로 Recommended나 Optional로 둔다.

### 출처가 있는 발견 (Cited Findings)

#### Fiserv (미국)
- 2025-08-04 기사 기준으로 Fiserv는 자체 스테이블코인 FIUSD를 2025년 말까지 내놓을 계획이었고, FIS는 자체 코인 대신 Circle과 제휴했다고 보도됐다 ([American Banker](https://www.americanbanker.com/payments/news/fis-collaborates-with-circle-to-boost-stablecoin-scale)). 최초 발표 기사는 [Payments Dive](https://www.paymentsdive.com/news/fiserv-launches-new-stablecoin-crypto-genius-act-trump-bitcoins/751317/)에 있다.
- 2026-06-03 기사: CEO Mike Lyons가 Bernstein 콘퍼런스에서 "FIUSD goes live in July"라고 말했고, Bank of North Dakota가 화이트라벨 코인 "Roughrider"를 운영하며, Fiserv가 수탁 기능을 위해 StoneCastle Cash Management를 인수했다고 보도됐다. 기사에는 사용 체인이 나오지 않는다 ([Payments Dive](https://www.paymentsdive.com/news/fiserv-stablecoin-arrives-next-month/821877/)).
- Bank of North Dakota와 Fiserv가 North Dakota 최초의 스테이블코인 "Roughrider coin"을 Fiserv 디지털 자산 플랫폼에서 내놓겠다고 발표했다 (발표일 미확인, [Bank of North Dakota](https://bnd.nd.gov/bank-of-north-dakota-and-fiserv-partner-to-launch-roughrider-coin/)).
- FIUSD의 대상은 지역은행과 신용조합이며, 예금이 은행 체계 밖으로 빠져나가지 않게 하는 것이 목적이라고 설명됐다 ([Forbes, 2026-03-12](https://www.forbes.com/sites/christerholloman/2026/03/12/the-future-of-payments-why-fiserv-is-betting-on-stablecoins/)).

#### Zelle 운영사 Early Warning Services (미국)
- 2025-10-24: Early Warning Services가 스테이블코인을 이용해 Zelle을 해외 송금으로 확장한다고 발표했다. 이 보도자료에는 코인 이름, 발행 주체, 체인이 나오지 않는다 ([Early Warning 보도자료](https://www.earlywarning.com/press-release/zelle-goes-international-early-warning-expands-1t-payments-network-stablecoin)).
- 2026-06-11: Early Warning Services가 자체 달러 스테이블코인 ZelleUSD(ZLUSD)를 발행하고, 첫 해외 송금 대상국인 인도로 2026년 말 전에 송금 기능을 열 계획이라고 보도됐다. 체인과 협력사는 공개되지 않았다 ([PYMNTS](https://www.pymnts.com/news/cross-border-payments/2026/zelle-readies-stablecoin-for-first-cross-border-push/); [crypto.news, 2026-06-15](https://crypto.news/zelle-picks-india-for-first-cross-border-remittance-launch-unveils-zlusd-stablecoin/); [American Banker](https://www.americanbanker.com/payments/news/zelle-steps-into-crowded-remittance-market-with-a-stablecoin)).
- Early Warning Services의 소유 은행은 Bank of America, Capital One, JPMorgan Chase, PNC, Truist, U.S. Bank, Wells Fargo이다 ([crypto.news](https://crypto.news/zelle-picks-india-for-first-cross-border-remittance-launch-unveils-zlusd-stablecoin/)).

#### Global Payments와 Worldpay (미국)
- 2025-05-27: Worldpay가 BVNK와 함께 미국·유럽 고객에게 180개 이상 시장으로 스테이블코인 지급(payout)을 제공한다고 발표했고, Fireblocks가 연결을 돕는다. 시범 운영은 2025년 하반기 예정이었다 ([Worldpay 보도자료](https://corporate.worldpay.com/news-releases/news-release-details/worldpay-enable-stablecoin-payouts-global-businesses); [Bloomberg](https://www.bloomberg.com/news/articles/2025-05-27/global-payments-worldpay-offers-stablecoin-payouts-using-circle); [BVNK](https://bvnk.com/blog/worldpay-bvnk-enable-stablecoin-payouts)).
- 과거 사실(2022-2023): Worldpay는 2022년부터 일부 지역 가맹점에 USDC 정산을 제공했고, 2023년 Visa와 시범 사업을 했다 ([PYMNTS](https://www.pymnts.com/cryptocurrency/2025/worldpay-teams-with-bvnk-to-offer-stablecoin-payouts/) 등 2025-05 보도에 인용된 내용).
- Global Payments 투자자 보도자료 첫 페이지(2026-05~09 게시물)에는 스테이블코인이나 디지털 자산 발표가 없었다 ([Global Payments IR](https://investors.globalpayments.com/news-events/press-releases)).

#### Shift4 (미국)
- 2025-12-22: Shift4가 가맹점 대상 스테이블코인 정산을 시작했다. 지원 코인은 USDC, USDT, EURC, DAI이고, 지원 체인은 Ethereum, Solana, Plasma, Stellar, Polygon, TON, Base이다 ([Shift4 IR 보도자료](https://investors.shift4.com/news-events/press-releases/detail/288/shift4-launches-global-stablecoin-settlement-platform-unlocking-faster-payments-for-merchants); [Polygon 블로그](https://polygon.technology/blog/shift4-brings-24-7-stablecoin-payments-to-global-commerce-on-polygon)).

#### Checkout.com (영국)
- 2026-06-04: Checkout.com과 Fireblocks가 미국 대기업 가맹점에 스테이블코인으로 정산금을 지급하는 서비스를 발표했다. 지원 코인과 대상 가맹점 수는 공개되지 않았다 ([The Paypers](https://thepaypers.com/crypto-web3-and-cbdc/news/checkoutcom-and-fireblocks-partner-on-stablecoin-settlement-for-us-merchants)).
- 과거 사실: Checkout.com은 Fireblocks와 함께 주말 정산(암호화폐 지급)을 도입했다 ([Checkout.com 뉴스룸](https://www.checkout.com/newsroom/checkout-com-becomes-the-first-psp-to-unlock-weekend-settlement-for-merchants-powered-by-fireblocks-crypto-payouts-debut)). USDC 베타에서 3억 달러 이상을 정산했다는 보도도 있으나, 기사 날짜를 확인하지 못했다 ([Cointelegraph](https://cointelegraph.com/news/checkout-com-launches-24-7-stablecoin-settlement-in-partnership-with-fireblocks)).

#### FIS (미국)
- 2025-08-04: FIS가 Circle과 제휴해 은행이 Money Movement Hub에서 USDC로 국내외 결제를 하도록 지원한다고 보도됐다 ([American Banker](https://www.americanbanker.com/payments/news/fis-collaborates-with-circle-to-boost-stablecoin-scale)).
- 2026: FIS는 토큰화 예금을 은행이 스테이블코인에 대응하는 수단으로 제시했고, 은행용 디지털 화폐 플랫폼을 내놓았다고 보도됐다 ([PYMNTS 실적 기사](https://www.pymnts.com/earnings/2026/fis-frames-tokenized-deposits-as-banks-answer-to-stablecoins/); [PYMNTS 플랫폼 기사](https://www.pymnts.com/digital-first-banking/2026/fis-platform-bridges-the-gap-between-banking-and-digital-money/)).

#### Euronet (미국, 자회사 Ria Money Transfer, Xe, Dandelion)
- 2025-10-16: Euronet이 Fireblocks를 도입해 먼저 자금 관리(treasury)에 스테이블코인을 쓰고, 이후 Ria, Xe, Dandelion, ATM망에 온·오프램프와 소비자 상품을 붙인다는 단계별 계획을 발표했다 ([Euronet IR PDF](https://ir.euronetworldwide.com/node/22321/pdf); [Manila Times 전재 GlobeNewswire](https://www.manilatimes.net/2025/10/16/tmt-newswire/globenewswire/euronet-chooses-fireblocks-to-support-cross-border-stablecoin-payments/2202372)).

#### Remitly (미국)
- 2025-08-04: Remitly가 Circle과 함께 법정화폐와 스테이블코인을 담는 Remitly Wallet을 2025년 9월에 출시하고, Bridge와 제휴해 일부 시장 수취인이 스테이블코인으로 받게 하며, 내부 자금 관리에 USDC를 쓴다고 발표했다 ([Remitly 뉴스룸](https://news.remitly.com/innovation/remitly-harnesses-stablecoins/)).

#### Payoneer (미국)
- 2026-02-17: Payoneer가 Bridge 기반 스테이블코인 수취·보유·송금 기능을 2026년 2분기 일부 시장에서 시작한다고 발표했다. 대상 고객은 약 200만 곳이다 ([Payoneer IR](https://investor.payoneer.com/news-releases/news-release-details/payoneer-launch-stablecoin-capabilities-powered-bridge-bringing); [The Paypers](https://thepaypers.com/crypto-web3-and-cbdc/news/payoneer-to-roll-out-stablecoin-capabilities-supported-by-bridge-in-q2-2026)).
- 2026-02-24: Payoneer가 OCC에 국법 신탁은행 "PAYO Digital Bank, N.A." 인가를 신청했고, 이 은행이 자체 스테이블코인 "PAYO-USD"를 발행할 계획이라고 보도됐다 ([PYMNTS](https://www.pymnts.com/cryptocurrency/2026/payoneer-aims-launch-stablecoin-focused-digital-bank/)).
- 미확인: Nuvei가 Payoneer를 27억 5천만 달러에 인수하고 2027년 중반에 거래를 마친다는 보도가 있으나, 출처가 KuCoin 속보 한 건뿐이고 해당 페이지와 Payoneer IR 페이지를 열지 못했다 ([KuCoin 속보](https://www.kucoin.com/news/flash/nuvei-to-acquire-payoneer-for-2-75b-integrating-stablecoins-into-payment-infrastructure)).

#### Nuvei (캐나다)
- 2025-08: Nuvei가 자금 관리, 급여, 송금에 쓰는 스테이블코인 레일을 추가했다 ([Payment Expert, 2025-08-13](https://paymentexpert.com/2025/08/13/nuvei-launches-stablecoin-rails-as-business-protocol/); [Nuvei](https://www.nuvei.com/posts/nuvei-taps-stablecoin-rails-to-power-payouts-in-emerging-markets)).
- 2025: Mastercard가 OKX, Nuvei와 스테이블코인 결제 제휴를 맺었다 ([PYMNTS](https://www.pymnts.com/partnerships/2025/mastercard-partners-with-okx-and-nuvei-to-power-stablecoin-transactions/)).

#### dLocal (우루과이)
- 2025-06-24: dLocal과 BVNK가 40개 시장에서 스테이블코인으로 송금 자금을 대고 현지 통화로 지급하는 제휴를 발표했다 ([The Paypers](https://thepaypers.com/crypto-web3-and-cbdc/news/dlocal-and-bvnk-partners-to-augment-stablecoin-payouts)).
- 날짜 미확인: Stable Sea(40개 이상 신흥시장 B2B), Damisa(아시아·태평양 정산)와도 스테이블코인 제휴를 맺었다 ([dLocal 보도자료](https://www.dlocal.com/press-releases/dlocal-and-stable-sea-join-forces-to-power-low-cost-b2b-cross-border-stablecoin-payments/); [The Paypers](https://thepaypers.com/payments/news/damisa-dlocal-team-up-to-expand-cross-border-stablecoin-settlement-across-apac)).

#### Wise (영국)
- 날짜 미확인(2025년 추정): Wise가 스테이블코인 담당 디지털 자산 제품 책임자를 채용한다고 보도됐다 ([Cointelegraph](https://cointelegraph.com/news/wise-digital-asset-lead-stablecoin-hiring-crypto-expansion)).
- 2026-07: Wise가 2026-07-24에 OCC 신청이 거부됐다고 공시했고, GENIUS Act 스테이블코인 체계로 다시 신청하겠다고 했다는 보도가 있다. 2차 출처 한 건이므로 원문 공시는 미확인이다 ([CryptoDaily](https://cryptodaily.co.uk/2026/07/wise-genius-stablecoin-charter)).

#### Airwallex (호주·싱가포르)
- 2025-07-08: Airwallex가 스테이블코인 직군 22개를 채용하며 스테이블코인 조직을 만들고 있다고 보도됐다 ([Ledger Insights](https://www.ledgerinsights.com/unicorn-airwallex-builds-stablecoin-team-despite-ceos-apparent-skepticism/)).
- Airwallex는 API로 Ethereum 네트워크의 USDC 지급을 지원한다 (확인일 2026-10-01, [Airwallex 문서](https://www.airwallex.com/docs/payouts/payout-network/stablecoin-wallets/usdc)).
- 2026-08-31: Airwallex가 미국 달러 스테이블코인을 현지 통화로 바꾸는 "마지막 구간(last mile)" 서비스를 만들었고, 규제 준수형 블록체인 스타트업 Metal에 투자했으며, Visa의 투자를 받았다고 보도됐다 ([Fortune](https://fortune.com/2026/08/31/who-will-use-stablecoins-airwallex-dan-kim/)).

#### Adyen (네덜란드)
- Adyen이 x402 Foundation과 Open Standard에 참여했다는 2차 분석 글이 있으나, Adyen 원문 발표는 확인하지 못했다 ([Rivalsense](https://rivalsense.co/intel/how-adyen-capitalized-on-stripes-blockchain-bet-a-strategic-playbook-for-b2b-leaders/)).
- 2026-04-29: 2026년 3월 스테이블코인 기능을 내놓은 Sokin이 Adyen과 결제 수납 제휴를 맺었다. 이 발표는 Adyen 자체의 스테이블코인 기능이 아니다 ([Morningstar 전재 PR Newswire](https://www.morningstar.com/news/pr-newswire/20260429ny45908/sokin-and-adyen-partner-to-give-us-businesses-a-single-solution-for-ecommerce-payments-and-treasury-operations)).

#### American Express (미국)
- 2026-06-28: American Express가 Digital Labs에 "VP of Stablecoin and Blockchain Partnerships & Strategy"와 "VP of Onchain Products"를 채용한다고 보도됐다. 같은 기사는 확인된 스테이블코인 정산 시범 사업이 없다고 썼다 ([Crypto Briefing](https://cryptobriefing.com/american-express-stablecoin-blockchain-vp/)). 반면 KuCoin 속보는 Amex가 가맹점과 카드 네트워크 사이의 스테이블코인 정산을 시범 운영한다고 썼다 ([KuCoin 속보](https://www.kucoin.com/news/flash/american-express-launches-ai-payment-development-tools-and-explores-stablecoin-settlement)). 두 출처가 충돌하므로 시범 운영은 미확인으로 둔다.

#### Capital One, Discover, Brex (미국)
- 2026-01-22: Capital One이 Brex를 51억 5천만 달러에 인수하기로 했고, 2026년 중반 종결 예정이라고 보도됐다. Brex는 2025년 9월 스테이블코인 결제 도입 계획을 발표했다 ([CoinDesk](https://www.coindesk.com/markets/2026/01/22/capital-one-acquires-fintech-firm-brex); [Yahoo Finance](https://finance.yahoo.com/news/capital-one-agrees-acquire-technology-045409718.html)).
- Capital One은 Discover 네트워크를 소유하며, Brex 카드 거래를 Discover 망으로 옮길 수 있다는 분석이 있다 ([Yahoo Finance](https://finance.yahoo.com/news/capital-one-redefines-role-discover-043019147.html)). Discover 네트워크 자체의 스테이블코인 사업은 찾지 못했다.

#### 참고: 추적 중인 기관 사이의 거래
- 2026-03: Mastercard가 BVNK를 18억 달러에 인수했고, 그 뒤 Zerohash 투자 계획을 접었다고 보도됐다 ([CoinDesk, 2026-05-19](https://www.coindesk.com/business/2026/05/19/zerohash-pursues-new-funding-at-more-than-usd1-5-billion-valuation-after-mastercard-drops-investment-plans)). 두 기관 모두 이미 추적 대상이다.

### 추론 (Inferences)

| 후보 | 등급 | 뉴스 표기(별칭) | 연결 체인·토큰 | 이름 충돌 위험과 매칭 제안 |
|---|---|---|---|---|
| Fiserv | Must | Fiserv, FIUSD, Roughrider coin, Clover(가맹점 브랜드) | 체인 미확인, Circle·Paxos 연결 여부 미확인 | "Fiserv"와 "FIUSD"는 고유하다. 티커 FI/FISV와 "Clover"(Clover Health, 일반 단어)는 쓰지 않는다. |
| Zelle·Early Warning Services | Must | Zelle, ZelleUSD, ZLUSD, Early Warning Services | 체인 미확인 | "Zelle", "ZLUSD"는 고유하다. "Early Warning"은 조기경보 일반어와 겹치므로 "Early Warning Services"만 쓴다. "EWS"는 쓰지 않는다. |
| Global Payments·Worldpay | Recommended | Worldpay, Global Payments, GPN | USDC(Circle), BVNK, Fireblocks | "Worldpay"는 고유하지만 프랑스 Worldline과 철자가 비슷하다. "global payments"는 일반 구문이므로 대문자 "Global Payments Inc" 또는 "Worldpay"와 함께 나올 때만 잡는다. |
| Shift4 | Recommended | Shift4, Shift4 Payments, FOUR | Ethereum, Solana, Plasma(XPL), Stellar(XLM), Polygon(POL), TON, Base; USDC, USDT, EURC, DAI | 고유 이름이므로 위험이 낮다. Stellar 같은 추적 프로젝트와 함께 나오면 높은 등급 알림이 될 수 있다. |
| Checkout.com | Recommended | Checkout.com | USDC, Fireblocks | "checkout"은 일반어이므로 "Checkout.com"만 쓴다. |
| FIS | Recommended | FIS, Fidelity National Information Services | USDC(Circle) | "FIS"는 국제스키연맹 등과 겹친다. 정식 명칭에 "Fidelity"가 들어 있어 기존 Fidelity 엔터티의 오탐을 부를 수 있으므로, Fidelity 규칙에 "Fidelity National Information" 제외 조건이 필요하다. |
| Euronet | Recommended | Euronet, Ria Money Transfer, Xe, Dandelion | Fireblocks | "Ria", "Xe", "Dandelion"은 단독으로 쓰지 않고 "Ria Money Transfer"와 "Euronet"만 쓴다. |
| Remitly | Recommended | Remitly, Remitly Wallet | USDC(Circle), Bridge | 위험이 낮다. |
| Payoneer | Recommended | Payoneer, PAYO, PAYO-USD, PAYO Digital Bank | Bridge | 티커 "PAYO"는 단독으로 쓰지 않는다. Nuvei 인수가 확인되면 Nuvei와 같은 사건으로 묶어 본다. |
| Wise | Recommended | Wise, Wise plc, TransferWise | 미확인 | "wise"는 일반 형용사여서 위험이 매우 높다. "Wise plc", "TransferWise", 또는 문장 첫머리의 "Wise"와 스테이블코인·OCC 문맥이 함께 나올 때만 잡는다. |
| American Express | Recommended | American Express, Amex, AmEx | 미확인 | "AMEX"는 옛 American Stock Exchange(현 NYSE American)와 겹친다. 대문자 전체 "AMEX"는 제외한다. |
| Nuvei | Optional | Nuvei | Mastercard, OKX | 고유 이름이다. Payoneer 인수가 사실로 확인되면 Recommended로 올린다. |
| dLocal | Optional | dLocal, DLocal, DLO | BVNK, Stable Sea, Damisa | 고유 이름이다. BVNK가 이미 추적 대상이어서 주요 사건은 BVNK로도 잡힌다. |
| Airwallex | Optional | Airwallex | USDC on Ethereum, Metal | 고유 이름이다. |
| Adyen | Optional | Adyen | Open Standard, x402(미확인) | 고유 이름이다. 직접 발표가 나오면 등급을 올린다. |
| Brex | Optional | Brex | 미확인 | 고유 이름이다. Capital One은 은행 조사 범위이다. |

- Fiserv와 Zelle은 수천 개 미국 은행·신용조합 또는 7대 은행과 연결된 자체 스테이블코인이므로, 은행 조사자가 다루는 기관과 함께 나오는 사건이 많을 것이다.
- 처리사들의 공통 패턴은 "기존 처리사 + 인프라 기업(BVNK, Fireblocks, Bridge, Circle)" 조합이다. 따라서 Fireblocks를 엔터티로 추가하면(질문 3) 이 표의 Optional 기관이 등장하는 사건도 상당수 잡힌다.
- Shift4는 Stellar, Solana, Polygon, TON, Plasma 등 여러 상위 토큰의 체인을 명시했으므로, 기관과 프로젝트를 잇는 사건 후보로 쓸모가 크다.

### 공백 (Gaps)
- FIUSD가 2026년 7월에 실제로 출시됐는지, 어느 체인에서 발행되는지(2025년 발표 당시 Solana라는 보도가 있었다고 기억하지만 이번 세션에서 확인하지 못함)는 미확인이다. Huntington이 시범 은행이라는 검색 요약도 원문에서 확인하지 못했다.
- ZelleUSD의 발행 주체(Early Warning 자체인지 수탁 은행인지), 체인, 출시 여부는 미확인이다.
- Global Payments의 Worldpay 인수 종결 시점과 FIS로의 Issuer Solutions 매각 종결 시점은 확인하지 못했다.
- Nuvei의 Payoneer 인수 보도, Wise의 OCC 신청 거부, Adyen의 Open Standard 참여, American Express의 정산 시범 운영은 1차 출처를 확인하지 못했다.
- Discover 네트워크, Zelle 소유 은행들의 2026-09 공동 스테이블코인 법인 구상(21개 국제 금융기관이 USD 스테이블코인 법인을 세운다는 [PR Newswire 발표](https://www.prnewswire.com/news-releases/group-of-leading-international-financial-institutions-to-establish-stablecoin-enterprise-302866318.html))은 은행 조사 범위이므로 내용을 확인하지 않았다.
- Corpay, Rapyd, Thunes, Ebanx, Flutterwave, Yellow Card, Worldline, Nexi, Paysafe, Intermex, Zepz는 검색 한도 때문에 조사하지 못했다.

## 질문 2: 어떤 플랫폼 기업과 핀테크가 2025-2026년에 스테이블코인이나 크립토 사업을 했는가 (Shopify, Amazon, Apple, Google, Meta, X Money, Nubank, Mercado Libre, SoFi, Chime, Klarna, Ant, Grab, Rakuten 등)

### 요점 (Takeaway)
2025-2026년에 실제로 출시된 사례는 SoFi(SoFiUSD 발행과 Mastercard 망 정산), Meta(USDC 크리에이터 지급, Solana·Polygon), Shopify(Base 위 USDC 결제), Nubank(USDC·EURC 기반 Nu Global), Klarna(KlarnaUSD, Tempo 테스트넷)이며, Google은 자체 원장(GCUL)과 에이전트 결제 규약(AP2의 x402 확장)을 내놓았다. Amazon, Walmart, Apple은 2025년 보도 이후 확인된 실행이 없고, X Money는 2026년 출시 당시 크립토 기능이 없었으므로 Optional로 둔다.

### 출처가 있는 발견 (Cited Findings)

#### SoFi Technologies (미국, 은행 조사와 겹침)
- 2025-12: SoFi Bank, N.A.가 퍼블릭 블록체인에서 완전 준비금 스테이블코인 SoFiUSD를 발행했고, 다른 은행과 핀테크가 이를 화이트라벨로 쓸 수 있다고 발표했다 ([SoFi IR](https://investors.sofi.com/news/news-details/2025/SoFi-Launches-Fully-Reserved-Stablecoin-to-Power-Financial-Infrastructure-for-Banks-Fintechs-and-Enterprise-Partners/default.aspx); [Banking Dive](https://www.bankingdive.com/news/sofi-launches-stablecoin-infrastructure/808232/)).
- 2026-05-27: SoFi 앱에서 SoFiUSD를 사고팔고 보유할 수 있게 됐고, Ethereum과 Solana를 지원한다고 보도됐다 ([Loeb & Loeb](https://www.loeb.com/en/insights/passle/2026/06/sofi-launches-first-bankissued-stablecoin-sofiusd-on-consumer-banking-app)).
- 2026: SoFi가 Mastercard 글로벌 망에서 스테이블코인 정산을 처음 가동한 국법은행이 됐다고 발표했다 ([SoFi IR](https://investors.sofi.com/news/news-details/2026/SoFi-Becomes-First-National-Bank-to-Go-Live-with-Stablecoin-Settlement-across-Mastercards-Global-Payments-Network/default.aspx); [The Paypers](https://thepaypers.com/crypto-web3-and-cbdc/news/sofi-goes-live-with-sofiusd-settlement-on-mastercards-network)).
- DefiLlama 기준 SoFiUSD(기호 SOFID) 유통량은 약 3억 3,050만 달러이고, 체인은 Solana, Ethereum, Monad, Polygon, Tempo이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoin/430)).

#### Meta (미국)
- 2026-04-29: Meta가 콜롬비아와 필리핀의 일부 크리에이터에게 Circle USDC로 수익을 지급하기 시작했다. 체인은 Solana와 Polygon이고, Stripe가 지급과 세무 서류를 지원한다 ([CoinDesk](https://www.coindesk.com/business/2026/04/29/tech-giant-meta-starts-paying-some-creators-in-stablecoin-with-stripe-s-support); [Fortune](https://fortune.com/2026/04/29/meta-stablecoins-crypto-usdc-polygon-solana/); [Polygon 블로그](https://polygon.technology/blog/meta-announces-usdc-creator-payouts-on-polygon)).
- 검색 요약에 따르면 Meta는 2026년 2월 자체 스테이블코인을 만들 계획이 없다고 밝혔고, 지급 대상을 연말까지 160여 개국으로 넓힐 예정이라고 한다. 원문 문장은 확인하지 못했다 ([PYMNTS](https://www.pymnts.com/cryptocurrency/2026/meta-begins-offering-stablecoin-payments-to-creators/); [Crowdfund Insider](https://www.crowdfundinsider.com/2026/05/277117-metas-stablecoin-usdc-payouts-are-more-practical-approach-to-web3-after-metaverse-venture-failed/)).

#### Shopify (캐나다)
- 2025-06: Shopify가 Coinbase, Stripe와 함께 Base 네트워크의 USDC 결제를 Shopify Payments에 넣었고, 가맹점은 현지 통화나 USDC로 받을 수 있다 ([Stripe 뉴스룸](https://stripe.com/newsroom/news/shopify-stripe-stablecoin-payments); [Shopify](https://www.shopify.com/news/stablecoins-on-shopify); [PYMNTS](https://www.pymnts.com/cryptocurrency/2025/shopify-to-enable-merchants-to-accept-usdc-stablecoin-payments/)).
- Shopify는 Open USD(OUSD)를 운영하는 Open Standard의 창립 파트너이다 (질문 3 참조, [DefiLlama API](https://stablecoins.llama.fi/stablecoin/443)).

#### Google (미국)
- 2025-08-27: Google Cloud가 금융기관용 레이어1 블록체인 Google Cloud Universal Ledger(GCUL)를 공개했고, CME Group과 토큰화 정산을 시범 운영했으며 2026년 본격 출시를 목표로 했다 ([CoinDesk](https://www.coindesk.com/business/2025/08/27/google-advances-its-layer-1-blockchain-here-s-what-we-know-so-far)).
- 2025-09-16: Google이 에이전트 결제 규약 AP2를 발표했고, Coinbase, Ethereum Foundation, MetaMask와 함께 크립토 결제용 "A2A x402 extension"을 내놓았다. 크립토 쪽 참여사로 Mysten Labs(Sui), Lightspark, BVNK, Crossmint, Mesh가 나온다 ([Google Cloud 블로그](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)).

#### Klarna (스웨덴)
- 2025-11-25: Klarna가 Bridge의 Open Issuance로 발행하는 달러 스테이블코인 KlarnaUSD를 Tempo 테스트넷에 올렸고, 2026년 메인넷 출시를 예정했다 ([CoinDesk](https://www.coindesk.com/business/2025/11/25/swedish-buy-now-pay-later-giant-klarna-rolling-out-stablecoin-with-stripe-s-bridge); [The Block](https://www.theblock.co/post/380365/bnpl-firm-klarna-announces-usd-stablecoin-on-stripe-paradigms-tempo-blockchain-to-cut-payment-costs)).

#### Nubank, Nu Holdings (브라질)
- 2026-09-10: Nubank가 Lead Bank와 손잡고 미국 소비자 금융을 시작했고, 예치금을 USDC와 EURC로 바꿔 35개국 이상으로 수수료 없이 송금하는 다중통화 계좌 Nu Global을 내놓았다. 수탁·거래·환전은 스위스 Sygnum이 맡는다 ([Blockhead, 2026-09-11](https://www.blockhead.co/2026/09/11/nu-global-taps-sygnum-for-stablecoin-custody-as-brazil-tightens-cross-border-crypto-rules/); [Rio Times](https://www.riotimesonline.com/nubank-us-launch-nu-global-stablecoin-account-2026); [Startup Fortune](https://startupfortune.com/nubank-launches-us-banking-with-a-stablecoin-account-before-its-charter-clears/)).
- 브라질 중앙은행 Resolution BCB 561(2026-10-01 시행)은 전자 외환 사업자가 해외 구간을 스테이블코인으로 정산하는 것을 금지하지만, 면허 은행과 가상자산 사업자는 예외라고 보도됐다 ([Blockhead](https://www.blockhead.co/2026/09/11/nu-global-taps-sygnum-for-stablecoin-custody-as-brazil-tightens-cross-border-crypto-rules/)).

#### Mercado Libre, Mercado Pago (아르헨티나·브라질)
- 과거 사실(2024-08): Mercado Libre가 Ripio와 함께 만든 달러 스테이블코인 Meli Dólar를 브라질 Mercado Pago 앱에서 내놓았다 ([Cointelegraph](https://cointelegraph.com/news/mercado-libre-launches-meli-dollar-stablecoin-brazil)).
- 날짜 미확인(2026년 추정): Mercado Pago가 자체 코인 Mercado Coin을 종료하고(4월 17일까지 사용 또는 상환) Meli Dólar 중심으로 보상과 결제를 운영한다고 보도됐다 ([Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/mercadolibre-refocuses-mercado-coin-meli-190814204.html)).

#### Ant International, Ant Group, Alipay (중국·싱가포르)
- 2025-06-12: Ant International이 싱가포르, 홍콩, 룩셈부르크에서 스테이블코인 관련 인가를 추진하고, Ant Group 계열 Ant Digital Technologies가 홍콩 스테이블코인 면허를 신청할 계획이라고 보도됐다 ([Ledger Insights](https://www.ledgerinsights.com/both-ant-intl-and-ant-group-are-planning-stablecoins/)).
- 2025-12-22: Standard Chartered가 토큰화 예금 서비스를 내놓았고 Ant International이 첫 고객이 됐다 ([Blockhead](https://www.blockhead.co/2025/12/22/standard-chartered-launches-tokenized-deposit-solution-with-ant-international-as-first-client/)). HSBC와도 토큰화 예금 서비스를 냈다 (날짜 미확인, [Financial IT](https://financialit.net/news/cryptocurrencies/ant-international-launches-tokenised-deposit-solutions-real-time-treasury)).
- Ant International의 블록체인 자금 관리 플랫폼 이름은 Whale이다 ([Forbes, 2025-12-13](https://www.forbes.com/sites/zennonkapron/2025/12/13/inside-ant-internationals-treasury-platform-how-whale-bettr-and-ai-are-rewiring-global-liquidity/)).

#### Grab (싱가포르)
- 2025-11-18: Grab이 StraitsX와 MOU를 맺고, 동남아 8개 시장에서 XSGD·XUSD를 쓰는 Web3 지갑과 스테이블코인 정산을 검토한다고 보도됐다. 각국 규제 승인이 필요하다 ([Cointelegraph](https://cointelegraph.com/news/grab-straitsx-stablecoin-settlement-mou-web3-wallet-asia)).
- 같은 기사는 2023년 Circle과의 시범 사업을 과거 사례로 언급한다. Triple-A를 통해 BTC, ETH, USDC, USDT 충전을 받는다는 사례 글도 있으나 날짜가 없다 ([Triple-A](https://www.triple-a.io/case-studies/crypto-payments-the-growing-business-use-case-for-top-ups)).

#### Amazon, Walmart (미국)
- 2025-06: The Wall Street Journal 보도를 인용해 Amazon과 Walmart가 자체 스테이블코인 발행을 검토한다고 보도됐다 ([American Banker](https://www.americanbanker.com/payments/news/walmart-and-amazon-consider-issuing-stablecoins)). 이번 조사에서는 2026년의 후속 실행을 찾지 못했다.

#### X Money (미국)
- 2026: X Money는 4월 제한 공개 이후 2026-07-27에 미국 Premium 구독자 전체로 확대됐다. Cross River Bank 기반 계좌와 Visa 직불카드, Visa Direct 송금을 쓰며, 출시 시점에는 크립토 기능이 없었다 ([Genfinity](https://genfinity.io/2026/07/27/x-money-us-launch-6-percent-apy-everything-app/); [TechXplore](https://techxplore.com/news/2026-07-elon-musk-money-visa-debit.html); [BlockEden](https://blockeden.xyz/blog/2026/03/14/x-money-payments-super-app-elon-musk-crypto-financial-services/)).

#### Figure Technology (미국)
- YLDS는 Figure Certificate Company가 발행하고 SEC에 등록된 이자 지급형 증권형 스테이블코인이며, 체인은 Provenance, Stellar, Tempo이고 유통량은 약 5억 350만 달러이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoin/272)).

### 추론 (Inferences)

| 후보 | 등급 | 뉴스 표기(별칭) | 연결 체인·토큰 | 이름 충돌 위험과 매칭 제안 |
|---|---|---|---|---|
| SoFi | Must | SoFi, SoFi Technologies, SoFi Bank, SoFiUSD, SOFID | Ethereum, Solana, Polygon, Monad, Tempo; Mastercard | "SoFi Stadium"을 제외한다. 은행 조사자와 중복되지 않게 한쪽에서만 정의한다. |
| Meta | Must | Meta, Meta Platforms, Facebook, Instagram | USDC, Solana(SOL), Polygon(POL), Stripe | "meta"는 일반어(meta-analysis)이고 시장 기사에 "Meta 주가"가 자주 나온다. "Meta Platforms" 또는 대문자 "Meta"와 stablecoin·USDC·Solana·Polygon 문맥이 함께 나올 때만 잡는다. "MetaMask", "Metaplanet"과 구분되도록 단어 경계를 쓴다. |
| Shopify | Recommended | Shopify, Shopify Payments | USDC on Base, Coinbase, Stripe, Open Standard | 고유 이름이다. |
| Google | Recommended | Google Cloud Universal Ledger, GCUL, AP2, Agent Payments Protocol | x402, Coinbase, CME | "Google"은 "Google 검색량", "Google Trends" 기사와 겹치므로 단독으로 쓰지 않는다. "GCUL", "Universal Ledger", "AP2"와 x402 문맥으로 잡는다. |
| Klarna | Recommended | Klarna, KlarnaUSD | Tempo, Bridge(Stripe) | 고유 이름이다. Tempo 메인넷 출시 때 사건이 생길 가능성이 높다. |
| Nubank | Recommended | Nubank, Nu Holdings, Nu Global, Nu Mexico, NU | USDC, EURC, Sygnum, Lead Bank | "Nu"는 단독으로 쓰지 않는다. |
| Mercado Libre | Recommended | Mercado Libre, MercadoLibre, Mercado Pago, Meli Dólar, Meli Dollar, MELI | Ripio | "Meli Dólar"와 "Meli Dollar" 두 철자를 모두 넣는다. |
| Ant International | Recommended | Ant International, Ant Group, Ant Digital Technologies, Alipay, Alipay+ | 토큰화 예금(Standard Chartered, HSBC) | "Whale"은 크립토 대량 보유자를 뜻하는 일반어이므로 별칭으로 쓰지 않는다. "Ant"도 단독으로 쓰지 않는다. |
| Grab | Recommended | Grab, Grab Holdings, GrabPay | XSGD, XUSD(StraitsX), Solana | "grab"은 동사이므로 "Grab Holdings", "GrabPay", "Grab's", 또는 "Grab"과 StraitsX·stablecoin이 함께 나올 때만 잡는다. |
| Brex | Optional | Brex | 미확인 | 고유 이름이다. |
| Amazon, Walmart | Optional | Amazon, Walmart, OnePay | 미확인 | "Amazon"은 AWS 노드, 열대우림, 시가총액 비교 기사와 겹친다. 스테이블코인 문맥을 필수 조건으로 둔다. |
| Apple | Optional | Apple, Apple Pay | 미확인 | 시가총액 비교 기사와 겹친다. "Apple Pay"와 스테이블코인 문맥만 잡는다. |
| X Money | Optional | X Money | Visa Direct, Cross River Bank | 단독 "X"는 매칭할 수 없다. "X Money"만 쓰되, MultiversX 계열 결제 회사 xMoney와 겹친다(이 회사 정보는 기억에 의존한 것으로 이번 세션에서 확인하지 못함). |
| Figure | Optional | Figure Technology, Figure Markets, YLDS | Provenance, Stellar, Tempo | "Figure"는 일반어이므로 정식 명칭과 "YLDS"만 쓴다. |

- Meta와 Shopify는 각각 Solana·Polygon, Base·Coinbase와 직접 연결되므로, 기관과 프로젝트를 잇는 사건을 만들 가능성이 높다. 특히 Meta는 지급 국가를 넓힐 때마다 후속 보도가 나올 것으로 보인다.
- Klarna, Payoneer, MetaMask, Phantom, Open Standard는 모두 Bridge(Stripe)를 발행 인프라로 쓴다. 기존 stripe 엔터티는 "Stripe"라는 단어가 있어야 잡히므로, "Bridge"만 나오는 기사(예: "issued by Bridge")는 놓칠 수 있다.
- Ant 계열은 스테이블코인 발행보다 토큰화 예금과 내부 자금 관리 쪽 사건이 많으므로, 은행 조사(Standard Chartered, HSBC)와 함께 잡히는 사건이 주를 이룰 것으로 보인다.

### 공백 (Gaps)
- Apple, Amazon, Walmart(OnePay의 크립토 거래 서비스 포함), Chime, Rakuten, Coupang Pay의 2025-2026년 크립토 활동은 검색 한도 때문에 확인하지 못했다.
- Beijing 당국이 2025년 하반기에 Ant 계열과 JD.com의 홍콩 스테이블코인 계획을 멈추게 했다는 보도가 있었다고 기억하지만, 이번 세션에서 출처를 확인하지 못했다.
- Klarna의 Tempo 메인넷 출시 여부, SoFi의 크립토 거래 재개 시점, Nubank의 미국 국법은행 인가 신청 결과, Shopify USDC 결제의 2026년 확장 범위는 확인하지 못했다.
- Meta의 "자체 스테이블코인 계획 없음" 발언과 160개국 확대 계획은 검색 요약으로만 확인했다.

## 질문 3: Tether, Circle, Paxos 외에 어떤 스테이블코인 발행사와 인프라 기업이 중요한가 (Agora, Ethena Labs, Sky, World Liberty Financial, Ripple RLUSD, First Digital, StraitsX, Anchorage, M0, Brale, Zero Hash, MoonPay, Transak, Ramp, Banxa, Alchemy Pay)

### 요점 (Takeaway)
2026-10-01 11:59 KST의 DefiLlama 유통량 기준으로 USDT, USDC 다음 순서는 USDS(Sky), USDe(Ethena), DAI(Sky), USD1(World Liberty Financial), USDG(Paxos 컨소시엄), PYUSD(PayPal), RLUSD(Ripple)이다. 따라서 Sky, Ethena, World Liberty Financial은 Must로 다뤄야 하며, 토큰(SKY, ENA, WLFI)이 상위 125 프로젝트 목록에 들어가면 프로젝트 엔터티로 정의하는 편이 맞다. 발행 인프라 쪽에서는 Tether USAT, Western Union USDPT, OSL USDGO, Ethena USDtb를 모두 발행하는 Anchorage Digital과, 여러 결제사 발표에 반복해 등장하는 Fireblocks, 그리고 Coinbase·Mastercard·Shopify·Stripe·Visa가 창립한 Open Standard(OUSD)를 Must로 둔다.

### 출처가 있는 발견 (Cited Findings)

#### 유통량 순위 (DefiLlama, 2026-10-01 11:59 KST)
- USDT 1,837.8억 달러, USDC 741.2억, USDS(Sky Dollar) 68.2억, USDe(Ethena) 48.6억, DAI 47.9억, USD1(World Liberty Financial) 44.3억, USDG(Global Dollar) 30.9억, PYUSD 27.4억, USYC(Circle) 24.0억, RLUSD 24.0억, BUIDL 22.5억, USDY(Ondo) 22.0억, USDD 15.3억, U(United Stables) 15.0억, USDf(Falcon) 12.1억, USDGO 11.9억, USDtb 5.4억, YLDS 5.0억, OUSD 4.7억, EURC 4.7억, SoFiUSD 3.3억, FDUSD 3.2억, AUSD 2.5억, M(M0) 2.0억, USAT 1.8억, CASH 1.3억, XUSD 0.41억, mUSD(MetaMask) 0.36억, USDPT 0.22억, XSGD 0.13억 달러 ([DefiLlama API](https://stablecoins.llama.fi/stablecoins?includePrices=true)).

#### Open Standard, Open USD (OUSD) (미국)
- OUSD는 Open Standard라는 독립 회사가 운영하는 달러 스테이블코인이며, 창립 파트너는 Coinbase, Mastercard, Shopify, Stripe, Visa이다. 파트너가 준비금 수익을 나눠 받고, 발행은 Bridge가 맡는다. 체인은 Tempo, Solana, Base, Ethereum이고 유통량은 약 4억 6,830만 달러이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoin/443)).
- Open Standard 홈페이지는 "OUSD is now live"라고 쓰고 200곳 이상의 파트너를 나열하지만, 출시일은 적혀 있지 않다 (확인일 2026-10-01, [Open Standard](https://joinopenstandard.com/)).

#### World Liberty Financial, USD1 (미국)
- 2025-05: MGX가 Binance에 20억 달러를 USD1로 투자·정산한 일이 USD1의 첫 대형 기관 사례였다 ([Wikipedia](https://en.wikipedia.org/wiki/World_Liberty_Financial); [DWF Labs](https://www.dwf-labs.com/research/world-liberty-financial-why-the-wlfi-token-launch-matters)).
- 2025-12-25: USD1 시가총액이 30억 달러를 넘었다고 발표했다 ([Business Wire](https://www.businesswire.com/news/home/20251225249806/en/World-Liberty-Financials-Stablecoin-$USD1-Crosses-$3-Billion-in-Market-Capitalization)).
- 2026-08-25: USD1이 Canton Network에 네이티브로 배포되어 Canton 최대 네이티브 스테이블코인이 됐다. 현재 발행사는 BitGo이며, World Liberty Trust Company가 OCC 국법 신탁은행 인가의 조건부 예비 승인을 받아 장차 직접 발행할 수 있다고 보도됐다 ([Ledger Insights](https://www.ledgerinsights.com/world-libertys-usd1-becomes-cantons-largest-native-stablecoin/)).

#### Ethena Labs (USDe, USDtb)
- 2025-07: GENIUS Act 서명 1주일 뒤, Anchorage Digital Bank가 Ethena의 USDtb를 미국 안에서 발행·상환하기로 했다고 발표됐다 ([The Block](https://www.theblock.co/post/364119/anchorage-digital-genius-stablecoin-ethena)).
- USDe 유통량은 약 48.6억 달러, USDtb는 약 5.4억 달러이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoins?includePrices=true)).

#### Sky (USDS, DAI)
- USDS(Sky Dollar)는 약 68.2억 달러, DAI는 약 47.9억 달러로, USDT·USDC 다음 규모이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoins?includePrices=true)). Sky의 2025-2026년 기관 제휴 발표는 이번 세션에서 검색하지 못했다.

#### Anchorage Digital (미국, 수탁·은행 조사와 겹침)
- 2026-01-27: Tether의 미국용 스테이블코인 USAT가 Anchorage Digital Bank 발행으로 출시됐다. Cantor Fitzgerald가 준비금 수탁과 프라이머리 딜러를 맡고, CEO는 Bo Hines이다 ([Anchorage](https://www.anchorage.com/insights/anchorage-digital-tether-introduce-usat); [Bloomberg](https://www.bloomberg.com/news/articles/2026-01-27/tether-anchorage-digital-launch-us-focused-stablecoin-usat); [Decrypt](https://decrypt.co/356045/tether-launches-us-regulated-stablecoin-issued-anchorage-digital)).
- Western Union의 USDPT(Solana)와 OSL Group이 유통하는 USDGO(유통량 약 11.9억 달러)도 Anchorage Digital Bank가 발행한다 (2026-10-01 11:59 KST, [DefiLlama USDPT](https://stablecoins.llama.fi/stablecoin/386); [DefiLlama USDGO](https://stablecoins.llama.fi/stablecoin/347)).

#### Fireblocks (미국·이스라엘, 수탁 조사와 겹칠 수 있음)
- 2025-09: Fireblocks가 스테이블코인 결제 네트워크(Network for Payments)를 출시했다 ([Fireblocks 블로그](https://www.fireblocks.com/blog/the-fireblocks-network-for-payments-is-here)).
- 2026-08 기준 이 네트워크가 매월 1,000억 달러 이상의 스테이블코인 거래를 처리한다고 보도됐다 ([Crypto Briefing](https://cryptobriefing.com/fireblocks-network-payments-stablecoin-transactions/)). 2026-02에는 FXC Intelligence가 Fireblocks를 스테이블코인 인프라 시장 선도 기업으로 꼽았다 ([Fireblocks 블로그](https://www.fireblocks.com/blog/market-leader-fxc-stablecoin-payments-infrastructure-buyers-guide)).
- 이번 조사에서 확인된 Fireblocks 고객·제휴처는 Worldpay(2025-05), Euronet(2025-10), Checkout.com(2026-06), Kakao Pay·KakaoBank(2026-09)이다 (각 질문의 출처 참조).

#### Agora (AUSD) (미국)
- AUSD 준비금은 State Street가 관리·수탁하고 VanEck가 운용한다고 알려져 있다 ([eco.com 정리 글](https://eco.com/support/en/articles/11752971-what-is-agora-ausd); [Agora](https://www.agora.finance/)).
- 2026-06-23: 전 Robinhood Crypto COO Tanya Denisova가 Agora 운영 책임자로 합류했다 ([CoinDesk](https://www.coindesk.com/business/2026/06/23/former-robinhood-crypto-coo-tanya-denisova-joins-stablecoin-issuer-agora-as-head-of-operations)).
- 2026-04-03부터 Injective 체인의 AUSD 발행을 줄여 나갔고 2026-09-28까지 상환을 받았다는 보도가 있다 ([WEEX 뉴스](https://www.weex.com/news/detail/agora-will-stop-issuing-the-stablecoin-ausd-on-injective-with-the-redemption-window-lasting-until-september-28-621891)).
- AUSD 체인은 Monad, Ethereum, Immutable zkEVM, Mantle, Avalanche, Solana, Polygon, Sui이고 유통량은 약 2억 5,030만 달러이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoin/205)).

#### Zerohash (미국)
- 2025-10-29: Mastercard가 Zero Hash를 최대 20억 달러에 인수하는 막바지 협상을 한다고 보도됐다 ([CoinDesk](https://www.coindesk.com/business/2025/10/29/mastercard-eyes-zero-hash-acquisition-for-nearly-usd2b-bet-on-stablecoins-report)).
- 2026-01: Zerohash가 독립을 택해 인수 협상이 끝났고, 15억 달러 가치로 2억 5천만 달러 조달을 협의한다고 보도됐다 ([CoinDesk, 2026-01-16](https://www.coindesk.com/business/2026/01/16/mastercard-said-to-weigh-zerohash-investment-after-crypto-company-ends-takeover-talks); [CoinDesk, 2026-01-26](https://www.coindesk.com/business/2026/01/26/zerohash-is-in-talks-to-raise-usd250-million-at-usd1-5-billion-valuation-after-walking-away-from-mastercard-takeover)).
- 2026-05-19: Mastercard가 BVNK 인수 뒤 Zerohash 투자 계획을 접었고, Zerohash 고객으로 Morgan Stanley, Stripe, Interactive Brokers, BlackRock BUIDL, Franklin Templeton, DraftKings가 꼽혔다 ([CoinDesk](https://www.coindesk.com/business/2026/05/19/zerohash-pursues-new-funding-at-more-than-usd1-5-billion-valuation-after-mastercard-drops-investment-plans)). Zerohash는 MiCA 인가도 받았다 ([Finance Magnates](https://www.financemagnates.com/cryptocurrency/zerohash-gains-mica-license-as-mastercard-considers-acquisition/)).

#### MoonPay (미국)
- 2025-03 Iron 인수를 바탕으로 2026-08에 기업용 스테이블코인 제품 MoonPay Enterprise를 출시했다 ([The Paypers](https://thepaypers.com/crypto-web3-and-cbdc/news/moonpay-launches-moonpay-enterprise-stablecoin-platform)).
- 2026-06-22: AI 회계 에이전트 회사 Entendre를 인수했다 ([PR Newswire](https://www.prnewswire.com/news-releases/moonpay-acquires-entendre-bringing-agentic-finance-to-the-stablecoin-economy-302805927.html)).
- 2026-09-23: SEC 등록 회사 North Capital을 6천만 달러 주식 교환으로 인수한다고 발표했고, 같은 해 DFlow와 Sodot도 인수했다 ([CoinDesk](https://www.coindesk.com/business/2026/09/23/moonpay-to-acquire-sec-registered-north-capital-in-usd60-million-all-stock-deal)).
- 2026-01-27 USAT 출시 당시 유통처로 MoonPay가 이름을 올렸다 ([Decrypt](https://decrypt.co/356045/tether-launches-us-regulated-stablecoin-issued-anchorage-digital)).

#### Rain (미국)
- 2026-01-09: 스테이블코인 카드 발급 회사 Rain이 ICONIQ 주도로 2억 5천만 달러를 조달했고 기업가치는 19억 5천만 달러이다 ([SiliconANGLE](https://siliconangle.com/2026/01/09/stablecoin-payment-card-startup-rain-reels-250m/); [Ledger Insights](https://www.ledgerinsights.com/stablecoin-card-firm-rain-raises-250m-at-1-95b/)).
- Rain은 Visa 주요 회원(principal member)으로 카드를 직접 발급하며 ([Wikipedia](https://en.wikipedia.org/wiki/Rain_(platform))), 2026-05에는 Mastercard 카드 발급 계획이 보도됐다 ([Fortune](https://fortune.com/2026/05/04/mastercard-rain-stablecoin-startup-institutional-customers-partnership/)). Naver Ventures도 이 라운드에 참여했다 ([Coin Edition](https://coinedition.com/naver-expands-u-s-crypto-presence-with-first-investment-ahead-of-dunamu-merger/)).

#### StraitsX (싱가포르)
- 2025-12-16: StraitsX가 XSGD와 XUSD를 2026년 초 Solana에 출시하고 x402 표준을 지원한다고 발표했다. XSGD는 이미 Ethereum, Polygon, Avalanche, Arbitrum, Zilliqa, Hedera, XRPL에서 쓰인다 ([Crypto Times](https://www.cryptotimes.io/2025/12/16/straitsx-to-launch-xsgd-and-xusd-stablecoins-on-solana-in-2026/); [Fintech Singapore](https://fintechnews.sg/123684/digitalassets/straitsx-solana/)).
- 2025-11-18: Grab과 MOU를 맺었다 (질문 2 참조).

#### M0와 MetaMask USD (mUSD)
- 2025-09-15에 출시된 MetaMask USD(mUSD)는 Bridge가 발행하고 M0 인프라로 발행한다 ([MetaMask](https://metamask.io/news/metamask-announces-stablecoin-metamask-usd); [The Block](https://www.theblock.co/post/367713/metamask-musd-stablecoin-ethereum-linea-stripe-bridge)).
- M0의 기반 토큰 M은 유통량 약 2억 100만 달러, mUSD는 약 3,550만 달러이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoins?includePrices=true)).

#### Brale (미국)
- 2026-01-08 Algorand, 2026-03-03 Monad로 스테이블코인 발행 서비스를 넓혔다 ([PR Newswire](https://www.prnewswire.com/news-releases/brale-expands-custom-stablecoin-issuance-and-orchestration-platform-to-enterprise-grade-quantum-resistant-algorand-blockchain-302655564.html); [Stabledash](https://stabledash.com/news/2026-03-03-brale-deploys-regulated-stablecoin-infrastructure-to-monad-for-high-speed-evm-issuance)). Canton의 Brale USDA는 약 400만 달러 규모로 보도됐다 ([Ledger Insights, 2026-08-25](https://www.ledgerinsights.com/world-libertys-usd1-becomes-cantons-largest-native-stablecoin/)).

#### Transak (미국·인도)
- MetaMask의 Deposit 버튼과 mUSD 온램프를 단독으로 맡는다 ([FF News](https://ffnews.com/newsarticle/transak-and-metamask-join-forces-to-offer-11-stablecoin-onramping-and-named-ibans)). 2026-04-09에 Gobi Partners가 투자했다 ([Chainwire](https://chainwire.org/2026/04/09/gobi-partners-invests-in-transak-to-expand-compliant-stablecoin-and-digital-asset-payments-across-asia/)).

#### Banxa (호주, OSL 자회사)
- 2026-01-02: OSL Group이 Banxa 인수를 마쳐 Banxa가 OSL의 완전 자회사가 됐다 ([OSL 보도자료](https://www.osl.com/hk-en/press-release/osl-group-completes-banxa-acquisition-accelerating-global-compliant-payment-network-expansion); [The Globe and Mail](https://www.theglobeandmail.com/investing/markets/stocks/BNXAF/pressreleases/36870780/banxa-goes-private-as-osl-group-closes-c155-per-share-buyout/)).

#### Alchemy Pay (싱가포르, 토큰 ACH)
- 2026-05: 자체 레이어1 Alchemy Chain 메인넷을 출시했고 이 체인에서 달러 스테이블코인 발행을 계획한다 ([Crypto Times, 2026-05-07](https://www.cryptotimes.io/2026/05/07/alchemy-pay-launches-alchemy-chain-mainnet-to-accelerate-global-stablecoin-payments/)). 2026-05-20 Rhode Island 송금업 면허 일정이 공지됐다 ([TradingView 전재 CoinMarketCal](https://www.tradingview.com/news/coinmarketcal:b2ef2db8d094b:0-alchemy-pay-ach-rhode-island-license-date-20-may-2026/)).

#### First Digital (FDUSD) (홍콩)
- 2026년 FDUSD 관련 소식(HashKey 거래쌍, TON 배포, Canza Finance 통합)은 CoinMarketCap의 AI 요약에서만 확인했다 ([CoinMarketCap](https://coinmarketcap.com/cmc-ai/first-digital-usd/latest-updates/)). 유통량은 약 3억 2,500만 달러이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoins?includePrices=true)).

#### United Stables (U), Phantom CASH
- U는 USDT·USDC·USD1과 교환되는 스테이블코인으로 설명되며, 체인은 BSC, Ethereum, Tron, Robinhood Chain이고 유통량은 약 14.96억 달러이다 ([DefiLlama API](https://stablecoins.llama.fi/stablecoin/336); [u.tech](https://u.tech/)). 발행 법인과 주주는 확인하지 못했다.
- CASH는 Bridge Building Inc.가 발행하는 Solana 스테이블코인이다 ([DefiLlama API](https://stablecoins.llama.fi/stablecoin/316)). Phantom 지갑과의 관계는 이번 세션에서 확인하지 못했다.

### 추론 (Inferences)

| 후보 | 등급 | 뉴스 표기(별칭) | 연결 체인·토큰 | 이름 충돌 위험과 매칭 제안 |
|---|---|---|---|---|
| Open Standard | Must | Open Standard, Open USD, OUSD | Tempo, Solana, Base, Ethereum; Coinbase, Mastercard, Shopify, Stripe, Visa | "open standard"는 일반 구문이고 "OUSD"는 Origin Dollar와 겹친다. "Open USD"와 "OUSD"에 stablecoin 문맥을 붙이고, "Open Standard"는 대문자이면서 OUSD·stablecoin과 함께 나올 때만 잡는다. 기존 crypto_payments 문맥에 이미 "OUSD", "Open USD"가 있다. |
| World Liberty Financial | Must | World Liberty Financial, World Liberty, WLFI, USD1, World Liberty Trust | BNB Chain, Ethereum, Canton, Tempo; WLFI 토큰 | "USD1"은 "USD1.5 billion" 같은 금액 표기와 겹치므로 `USD1\b(?![.,]\d)`처럼 숫자가 이어지는 경우를 뺀다. WLFI 토큰이 상위 125에 들면 프로젝트로 정의한다. |
| Anchorage Digital | Must | Anchorage Digital, Anchorage Digital Bank | USAT(Tether), USDPT(Western Union), USDGO(OSL), USDtb(Ethena) | "Anchorage"는 알래스카 도시이므로 "Anchorage Digital"만 쓴다. 수탁 조사자와 정의를 맞춘다. |
| Fireblocks | Must | Fireblocks | 여러 체인 | 고유 이름이다. 현재는 crypto_payments 문맥어로만 쓰이므로 엔터티로 승격한다. 수탁 조사자와 중복을 피한다. |
| Ethena Labs | Must | Ethena, Ethena Labs, USDe, USDtb | ENA 토큰, Anchorage, BlackRock BUIDL | "USDe"는 대소문자를 구분해야 "USDE" 같은 다른 표기와 섞이지 않는다. ENA가 상위 125에 들면 프로젝트로 정의한다. |
| Sky | Must | Sky Protocol, Sky Dollar, USDS, MakerDAO, DAI, Spark | SKY 토큰 | "Sky"는 영국 방송사 Sky와 일반어가 겹치므로 "Sky Protocol", "Sky Dollar", "USDS", "MakerDAO"만 쓴다. SKY가 상위 125에 들면 프로젝트로 정의한다. |
| Zerohash | Recommended | Zerohash, Zero Hash, zerohash | Mastercard(협상 종료), Stripe, Interactive Brokers | 두 철자를 모두 넣는다. 이미 crypto_payments 문맥어에 "zero ?hash"가 있다. |
| MoonPay | Recommended | MoonPay, MoonPay Enterprise, Iron | Solana(DFlow), USAT 유통 | 고유 이름이다. "Iron"은 단독으로 쓰지 않는다. |
| Rain | Recommended | Rain, Rain Cards, rain.xyz | Visa, Mastercard, Naver Ventures | "rain"은 날씨 단어이므로 "Rain"과 stablecoin·card 문맥이 함께 나오고 문장 첫머리가 아닐 때, 또는 "stablecoin card issuer Rain" 같은 수식어가 붙을 때만 잡는다. 위험이 매우 높다. |
| StraitsX | Recommended | StraitsX, XSGD, XUSD | Solana, Hedera, XRPL, Avalanche, Polygon | 고유 이름이다. "XUSD"는 다른 소형 토큰과 겹치므로 StraitsX와 함께 나올 때만 잡는다. |
| Agora | Recommended | Agora, Agora Finance, AUSD | Monad, Solana, Sui, Avalanche 등 | "Agora"는 BIS의 Project Agorá와 정면으로 겹친다(기존 crypto_bank 문맥어에도 "Project Agora"가 있다). "Project Agora"를 제외하고 "AUSD" 또는 "Agora Finance"와 함께 나올 때만 잡는다. |
| M0 | Optional | M0, M^0, M0 Foundation, M by M0 | MetaMask mUSD, Bridge | "M0"는 경제학의 본원통화 표기와 겹친다. "M0 Foundation", "M^0 Labs"만 쓴다. |
| Brale | Optional | Brale | Algorand, Monad, Canton | 고유 이름이다. |
| Transak | Optional | Transak | MetaMask, Cross River Bank | 고유 이름이다. |
| Banxa | Optional | Banxa | OSL | 고유 이름이다. OSL은 거래소 조사 범위이다. |
| Alchemy Pay | Optional | Alchemy Pay, Alchemy Chain | ACH 토큰 | 티커 "ACH"는 미국 자동이체망(ACH)과 겹치므로 절대 쓰지 않는다. 개발 플랫폼 "Alchemy"와 구분되도록 "Alchemy Pay"만 쓴다. |
| First Digital | Optional | First Digital Labs, First Digital Trust, FDUSD | Binance, TON | "First Digital"은 일반 구문과 겹치므로 "FDUSD"와 정식 명칭만 쓴다. |
| United Stables | Optional | United Stables | BSC, Ethereum, Tron | 기호 "U"는 매칭할 수 없다. 발행 주체가 확인되기 전까지 보류에 가깝다. |
| MetaMask(mUSD), Phantom(CASH) | Optional | MetaMask USD, mUSD | Ethereum, Linea, Monad, Solana | "mUSD"는 mStable USD, Mezo USD와 겹친다. 지갑 회사는 다른 분류일 수 있다. |

- Anchorage Digital은 이미 추적 중인 Tether와 Western Union의 스테이블코인을 모두 발행하므로, 이 기관을 넣으면 두 추적 기관의 사건에 발행사 정보가 함께 붙는다.
- USDG(Global Dollar)는 유통량 기준 상위권이지만 기존 paxos 엔터티는 "Paxos"라는 단어가 있어야 잡힌다. "USDG"와 "Global Dollar Network"를 paxos 별칭으로 추가하는 편이 낫다(이미 crypto_payments 문맥어에는 USDG가 있다).
- Ripple의 RLUSD는 기존 ripple 엔터티 규칙에 이미 들어 있다.
- 사용자가 예로 든 Ramp(Ramp Network)는 이름 충돌이 가장 심한 후보이다: "on-ramp", "off-ramp"가 크립토 기사에 매우 자주 나오고, 미국 법인카드 회사 Ramp도 있다. 추가한다면 "Ramp Network"만 쓰는 것이 안전하다.

### 공백 (Gaps)
- Sky와 Ethena의 2025-2026년 기관 제휴, First Digital의 2026년 동향(1차 출처), Ramp Network의 동향은 검색 한도 때문에 조사하지 못했다.
- United Stables(U)와 USDGO의 발행·유통 구조를 원문으로 확인하지 못했다. DefiLlama 설명만 근거로 삼았다.
- Open Standard와 OUSD의 출시일, Adyen 참여 여부는 확인하지 못했다.
- Hyperliquid의 USDH(Native Markets), Falcon Finance(USDf), Ondo(USDY), Usual(USD0), Frax(frxUSD), Monerium(EURe), Quantoz, AllUnity(EURAU), Hex Trust(USDX)는 이번 범위에서 다루지 않았다. Ondo와 Hyperliquid는 이미 프로젝트 엔터티이다.
- A7A5(루블 스테이블코인, 유통량 약 5억 5,820만 달러, [DefiLlama API](https://stablecoins.llama.fi/stablecoins?includePrices=true))는 제재 관련 보도에 자주 나올 수 있으나 발행 구조를 조사하지 않았다.

## 질문 4: 한국과 일본의 스테이블코인·결제 기업은 누구이며, 영문 뉴스는 어떤 이름을 쓰는가 (Kakao Pay, Naver Pay·Naver Financial, Toss, 은행 컨소시엄, JPYC, SBI VC Trade)

### 요점 (Takeaway)
한국에서는 Naver Financial(Dunamu와 합병, 원화 스테이블코인 공동 추진)과 Kakao 그룹(Kakao, Kakao Pay, KakaoBank가 2026-07 Circle, 2026-09 Fireblocks와 MOU)이 2025-2026년 원화 스테이블코인 보도의 중심이므로 Must로 둔다. Toss(Viva Republica)는 2026-07 Optimism과 원화 스테이블코인 PoC를 시작해 Recommended로 둔다. 일본에서는 JPYC(2025-10-27 첫 엔화 스테이블코인 발행), PayPay(2025-10 Binance Japan 지분 40% 인수), SBI 계열(SBI Shinsei Trust & Banking의 JPYSC, 기존 sbi_holdings가 포함)이 핵심이다.

### 출처가 있는 발견 (Cited Findings)

#### Naver Financial, Naver Pay (한국)
- 2025-11-26: Naver Financial이 주식 교환(Dunamu 1주당 Naver Financial 2.54주)으로 Dunamu를 완전 자회사로 편입한다고 보도됐다. 기업가치는 Dunamu 약 15조 원, Naver Financial 약 5조 원이다. 주주총회는 5월 22일, 거래 종결 목표는 6월 30일(2026년)이며, 공정거래위원회와 금융당국 심사에 1년 이상 걸릴 수 있다고 했다 ([Korea Herald](https://www.koreaherald.com/article/10624296)).
- 두 회사가 원화 스테이블코인을 함께 추진하는 것이 합병의 핵심 목표로 보도됐다 ([Bitcoin.com News](https://news.bitcoin.com/koreas-naver-acquires-upbit-operator-dunamu-in-a-bold-digital-finance-expansion/)). 부산시 스테이블코인 도입을 지원한다는 보도도 있다 ([CoinCentral](https://coincentral.com/naver-dunamu-merger-to-support-stablecoin-rollout-in-busan-city/)).
- Naver Ventures가 미국 스테이블코인 카드 회사 Rain의 2억 5천만 달러 시리즈 C에 참여했다 ([Coin Edition](https://coinedition.com/naver-expands-u-s-crypto-presence-with-first-investment-ahead-of-dunamu-merger/)).

#### Kakao, Kakao Pay, KakaoBank (한국)
- 2026-05-28: Kakao가 KakaoBank 앱에 원화 스테이블코인 지갑을 내놓을 계획이라고 보도됐다 ([Seoul Economic Daily](https://en.sedaily.com/finance/2026/05/28/kakao-to-launch-won-stablecoin-wallet-on-kakaobank-app)).
- 2026-07-23: Kakao Corp., Kakao Pay, KakaoBank가 Circle과 원화 디지털 자산 결제 인프라를 개발하는 전략적 MOU를 맺었다 ([UPI](https://www.upi.com/amp/Top_News/World-News/2026/07/23/kakao-circle-stablecoin/5081784843202/)).
- 2026-09-21(또는 09-22): Kakao Pay와 KakaoBank가 Fireblocks와 수탁·토큰화·정산 인프라 MOU를 맺었다. 날짜가 출처마다 하루씩 다르다 ([CoinPaprika, 09-21](https://coinpaprika.com/news/kakao-pay-kakaobank-sign-stablecoin/); [GitHub 분석 글, 09-22](https://github.com/Ricosworks1/blockchain-payment-flow-analysis/releases/tag/deep-dive-kakao-fireblocks-won-stablecoin-race-sept-2026)).
- 2026-09-29: Kakao 그룹이 일상 결제와 송금용 원화 스테이블코인 계획을 공개했고, Kakao Pay 이용자 4,300만 명을 유통 기반으로 삼는다고 했다 ([Seoul Economic Daily](https://en.sedaily.com/finance/2026/09/29/kakao-pushes-won-based-stablecoin-for-everyday-payments)).

#### Toss, Viva Republica (한국)
- 2026-02-12: Toss가 블록체인 전담 조직을 만들었고, Bithumb의 스테이블코인 사업과 Toss의 송금·결제를 결합하는 방안을 검토한다고 보도됐다 ([Bloomingbit](https://en.bloomingbit.io/feed/news/105995)).
- 2026-07-08: Viva Republica가 Optimism, Sunnyside Labs와 OP Stack 기반 원화 스테이블코인 PoC(3개월)를 한다고 보도됐다 ([Cointelegraph](https://cointelegraph.com/news/south-korea-toss-partners-optimism-won-stablecoins)).
- 호주 진출과 원화 스테이블코인 계획 보도도 있다 (날짜 미확인, [Fintech Singapore](https://fintechnews.sg/117948/australia/toss-australia-launch-won-stablecoin/)).

#### JPYC (일본)
- 2025-10-27: JPYC Inc.가 일본 자금결제법상 첫 엔화 스테이블코인 JPYC를 발행하고 발행·상환 플랫폼 JPYC EX를 열었다. 체인은 Avalanche, Ethereum, Polygon이며, 3년 안에 10조 엔 유통을 목표로 했다 ([The Block](https://www.theblock.co/post/376199/japan-jpyc-launches-yen-stablecoin)).
- DefiLlama는 JPYC 체인에 Kaia를 포함하며, 유통량은 약 2,360만 달러이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoin/355)). 시리즈 B 1,200만 달러 조달 보도도 있다 (날짜 미확인, [Ledger Insights](https://www.ledgerinsights.com/jpyc-raises-12m-series-b-as-mainstream-investors-back-yen-stablecoin/)).

#### SBI 계열 JPYSC (일본, 기존 sbi_holdings 범위)
- JPYSC는 SBI Shinsei Trust & Banking이 Startale Group과 함께 전자결제수단 체계로 발행하는 신탁형 엔화 스테이블코인이며, 체인은 Ethereum이고 유통량은 약 1억 2,710만 달러이다 (2026-10-01 11:59 KST, [DefiLlama API](https://stablecoins.llama.fi/stablecoin/427)). 발행사 페이지([SBI Shinsei Trust](https://www.shinseitrust.com/stablecoin/jpysc.html))는 503 오류로 열지 못했다.

#### PayPay (일본)
- 2025-10-09: SoftBank와 LY Corp 계열 PayPay가 Binance Japan 지분 40%를 인수했다. PayPay Money로 크립토를 사고 PayPay 계좌로 출금하는 연동을 검토한다고 했다 ([CoinDesk](https://www.coindesk.com/business/2025/10/09/softbank-s-paypay-buys-40-stake-in-binance-japan-to-fuse-crypto-with-cashless-payments)).
- 2026-09-30부터 Binance Pay 이용자가 일본 PayPay 가맹점에서 크립토로 결제하고 가맹점은 엔화로 받는다고 보도됐다(2차 출처) ([CoinGape](https://coingape.com/binance-pay-opens-usdt-spending-at-paypay-merchants-across-japan/)).

### 추론 (Inferences)

| 후보 | 등급 | 영문 뉴스 표기 | 한국어·일본어 표기 | 연결 체인·토큰 | 이름 충돌 위험과 매칭 제안 |
|---|---|---|---|---|---|
| Naver Financial | Must | Naver Financial, Naver Pay, NaverPay, Naver | 네이버파이낸셜, 네이버페이 | Upbit·Dunamu(기존 upbit 엔터티), Rain | "Naver"는 뉴스 포털 출처 표기("Naver News")와 겹친다. "Naver Financial", "Naver Pay"를 기본으로 하고, 단독 "Naver"는 Dunamu·stablecoin 문맥이 있을 때만 잡는다. |
| Kakao 그룹 | Must | Kakao Pay, KakaoPay, KakaoBank, Kakao Bank, Kakao Corp | 카카오페이, 카카오뱅크, 카카오 | Circle, Fireblocks, (과거) Klaytn·Kaia | 고유 이름이다. KakaoBank는 은행 조사자와 겹칠 수 있다. Kaia(KAIA) 프로젝트 기사에 "Kakao"가 배경 설명으로 나올 수 있으므로, Kaia 엔터티를 두면 높은 등급 알림이 과다할 수 있다. |
| Toss | Recommended | Toss, Viva Republica, Toss Bank, Toss Securities | 토스, 비바리퍼블리카, 토스뱅크 | Optimism(OP), Bithumb(기존 엔터티) | "toss"는 동사이고 "coin toss"는 크립토 기사에도 나온다. "Viva Republica", "Toss Bank", "Toss Securities"를 쓰고, 단독 "Toss"는 Korea·won·원화 문맥이 있을 때만 잡는다. 한글 "토스"는 "토스트"와 겹치지 않게 단어 경계를 둔다. |
| PayPay | Recommended | PayPay | ペイペイ | Binance Japan(기존 binance 엔터티) | 고유 이름이다. |
| JPYC | Recommended | JPYC, JPY Coin, JPYC Inc. | JPYC株式会社 | Avalanche(AVAX), Ethereum, Polygon(POL), Kaia | 고유 이름이다. "JPY Coin"은 대소문자 구분을 둔다. |
| SBI(JPYSC) | 기존 엔터티 별칭 추가 | SBI Shinsei Trust & Banking, JPYSC | SBI新生信託銀行 | Startale, Ethereum | 기존 sbi_holdings 규칙이 "SBI Shinsei"를 이미 잡는다. "JPYSC"만 별칭으로 더한다. |

- 한국 원화 스테이블코인 보도에는 은행 컨소시엄(KB금융의 2026-05 시범 사업 보도 등)과 거래소(Upbit, Bithumb)가 함께 나오는 경우가 많다. Naver Financial과 Kakao Pay를 추가하면 기존 upbit, bithumb, shinhan 엔터티와 같은 기사에서 함께 잡히는 사건이 늘어날 것으로 보인다.
- 영문 기사는 "Naver Financial", "Kakao Pay"(또는 "KakaoPay"), "KakaoBank", "Viva Republica, operator of Toss"를 주로 쓰고, 한국어 기사는 "네이버파이낸셜", "카카오페이", "카카오뱅크", "토스", "비바리퍼블리카"를 쓴다. 기존 upbit 엔터티처럼 한글 패턴을 함께 두는 편이 맞다.
- 일본은 은행·신탁 계열(SBI, MUFG Progmat)이 이미 은행 조사 범위에 있으므로, 결제 범위에서는 JPYC와 PayPay만 추가하면 된다.

### 공백 (Gaps)
- Naver Financial과 Dunamu의 합병이 2026-06-30 목표대로 종결됐는지, 규제 심사가 끝났는지 확인하지 못했다.
- 한국 디지털자산기본법(원화 스테이블코인 근거 법)의 국회 처리 상황은 GitHub 분석 글 한 건에서 "2026년 말 목표"라는 서술만 봤고, 1차 출처를 확인하지 못했다. KB금융의 2026-05 원화 스테이블코인 시범 사업도 같은 글에서만 봤다.
- Toss가 Bithumb 스테이블코인 사업과 결합했는지는 확인하지 못했다.
- SBI VC Trade의 USDC 취급(2025년 일본 첫 USDC 유통 사업자로 알려져 있음), Rakuten(Rakuten Wallet), LINE Yahoo·LINE NEXT와 Kaia의 스테이블코인 사업, Coupang Pay, 한국 은행 컨소시엄의 공동 원화 스테이블코인 구상은 검색 한도 때문에 조사하지 못했다.
