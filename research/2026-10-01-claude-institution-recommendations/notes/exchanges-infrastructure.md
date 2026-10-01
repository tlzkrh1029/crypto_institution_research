# 크립토 기관 엔터티 추가 후보: 거래소, 시장 인프라, 수탁·프라임, 토큰화 플랫폼

- 작성 도구: Claude Code (하위 조사 에이전트)
- 작성 시각: 2026-10-01 12:02 KST
- 조사 범위: (a) 크립토 거래소와 브로커, (b) 전통 거래소·CSD·청산소, (c) 기관 수탁·프라임 브로커·마켓메이커, (d) 토큰화·RWA 플랫폼. 2025~2026년 근거를 우선했고, 그 이전 사실은 "(과거 사실)"로 표시했다.
- 제외 범위: 이미 추적 중이거나 작업 중인 기관(The Clearing House, DTCC, Swift, Euroclear, Broadridge, Bybit, Nasdaq, ICE/NYSE, CME Group, Coinbase, Robinhood, Kraken, Gemini, Binance, OKX, Bullish, Cboe, Charles Schwab, Interactive Brokers, eToro, Upbit, Bithumb, Anchorage Digital, BitGo, Fireblocks, Galaxy Digital, Securitize, Cantor Fitzgerald, Clearstream, SIX Digital Exchange, LSEG, Deutsche Börse)은 새 후보로 제안하지 않았다. 다만 이들의 자회사나 인수 대상이 뉴스에 다른 이름으로 나오는 경우에는 "별칭 추가"로 제안했다. 은행, 자산운용사, 결제, 규제기관, 토큰 매입 상장사는 다른 조사자가 맡으므로 다루지 않았다.
- 확인 방식: 모든 링크는 2026-10-01(KST)에 확인했다. 출처 뒤에 [원문 열람]이 붙은 항목은 해당 페이지를 직접 열어 내용을 확인했다. 표시가 없는 항목은 웹 검색 결과에 함께 제시된 요약으로 확인했으며, 원문 전문은 열지 못했다. 이 세션은 도중에 웹 검색 한도(세션당 200회)에 도달했기 때문에, 이후에는 개별 페이지 열람만으로 확인했다.
- 시장 수치: 이 노트에 들어 있는 거래량·운용자산·평가액 수치는 출처가 밝힌 시점의 값이며, 현재 시장 상황을 뜻하지 않는다.
- 이 노트는 조사 기록이며 투자 권유가 아니다.

등급 기준: Must는 2025~2026년 기관-크립토 발표에 자주 등장하거나 상위 125개 토큰 다수에 영향을 주는 기관이다. Recommended는 특정 지역(한국·일본·홍콩·유럽)이나 특정 사업(ETF, 토큰화)에서 의미 있는 사건이 반복된 기관이다. Optional은 사건이 드물거나, 근거를 충분히 확보하지 못했거나, 기관 성격이 약한 곳이다. "별칭 추가"는 새 엔터티를 만들지 않고 기존 엔터티(config/entities.yaml)의 match 규칙에 이름을 더하자는 제안이다.

## (a) 추적 대상 밖의 크립토 거래소와 브로커 중 상장과 기관 자금 흐름에 중요한 곳은 어디이며, 2025~2026년에 규제된 기관 관련성을 가진 곳은 어디인가

### Takeaway
Crypto.com은 2026년에 Citadel Securities 투자, 토큰화 주식, 예측시장, ETF 수탁 제휴(이후 종료)를 연달아 발표했기 때문에 Must 등급이 타당하다. 한국 범위에서는 코빗(미래에셋 인수), 코인원(OKX·한국투자증권 지분 투자, FIU 제재), 고팍스(Binance 인수 승인)가 2025~2026년에 기관 소유 구조가 바뀌었으므로 추가할 가치가 크다. Bitstamp와 Deribit, xStocks처럼 이미 추적 중인 기관이 인수한 곳은 새 엔터티보다 별칭으로 추가하는 편이 맞다.

### Cited Findings

#### Crypto.com (별칭: Crypto.com Exchange, Crypto.com Custody, Cronos, CRO, OG.com)
- 2026-07-16에 Citadel Securities가 Crypto.com에 4억 달러를 투자했고, 평가액은 약 200억 달러였다. CoinDesk는 이것이 Crypto.com의 첫 기관 투자 유치이며, 자금을 토큰화 증권, 파생상품, 24시간 거래 인프라, 예측시장, 토큰화 RWA에 쓰겠다고 밝혔다고 보도했다. ([CoinDesk, 2026-07-16](https://www.coindesk.com/business/2026/07/16/citadel-securities-invests-usd400-million-in-crypto-com-valuing-exchange-at-usd20-billion) [원문 열람])
- Crypto.com 회사 뉴스 페이지에는 2026-08-07 "Crypto.com, Trump Media and Technology Group, and Yorkville Provide Update on CRO Digital Asset Treasury and ETF Partnership", 2026-08-08 "Crypto.com and Trump Media and Technology Group to Realign Integration Partnership to Marketing Agreement", 2026-08-12 "Crypto.com Launches the Future of Trading with Tokenized Stocks"가 게시되어 있다. ([Crypto.com company news](https://crypto.com/en/company-news) [원문 열람])
- SEC에 제출된 증빙 문서(Exhibit 99.1)에 따르면, Crypto.com, Trump Media, Yorkville은 2026년 8월에 Crypto.com이 Yorkville America의 ETF 상품에 서비스를 제공하기로 했던 제휴를 합의 해지했다. ([SEC EDGAR exhibit](https://www.sec.gov/Archives/edgar/data/2064658/000110465926093049/tm2622603d1_ex99-1.htm))
- 같은 뉴스 페이지에는 예측시장 관련 발표가 이어진다: 2026-06-09 FanDuel Predicts 제휴, 2026-08-18 Trading Technologies의 OG.com·Crypto.com 지원, 2026-08-31 OG.com AI 예측 계약, 2026-09-08 "Robinhood Selects OG.com as Infrastructure Partner for Prediction Markets Platform, Holding Equity Stake in Exchange Engine". ([Crypto.com company news](https://crypto.com/en/company-news) [원문 열람])
- 수탁 사업으로는 2026-07-27 XYO 토큰 기관 수탁, Sui Foundation과 SUI 토큰 기관 수탁(날짜 미확인), 2026-09-16 ZagTrader와 기관 접근 확대 발표가 있다. ([Crypto.com company news](https://crypto.com/en/company-news) [원문 열람]; [Crypto.com: SUI custody](https://crypto.com/en/company-news/cryptocom-launches-secure-institutional-custody-solutions-for-sui-tokens-in-partnership-with-sui-foundation); [Crypto.com: XYO custody](https://crypto.com/us/company-news/xyo-selects-cryptocom-for-secure-institutional-custody-solutions))

#### Bitstamp (Robinhood 자회사, 별칭 추가 후보)
- Robinhood는 2025-06-02에 Bitstamp 인수를 완료했다. Bitstamp는 전 세계에서 50개가 넘는 인가와 등록을 보유하고 있고, Robinhood는 이 인수를 기관 크립토 서비스 진출로 설명했다. ([Robinhood newsroom, 2025-06-02](https://robinhood.com/newsroom/robinhood-completes-acquisition-of-bitstamp/) [원문 열람])

#### 코빗 (Korbit)
- 미래에셋컨설팅은 2026-02-13에 코빗 지분 92.06%를 1,335억 원(약 9,227만 달러)에 인수하기로 했다. 매도자는 NXC와 SK플래닛이었다. The Block은 디지털자산기본법에서 논의되는 대주주 지분 상한이 이 거래에 변수가 될 수 있다고 보도했다. ([The Block, 2026-02-13](https://www.theblock.co/post/389835/mirae-asset-acquires-korbit) [원문 열람])
- 공정거래위원회 승인은 2026년 7월에 나왔다. ([UPI, 2026-07-09](https://www.upi.com/Top_News/World-News/2026/07/09/mirae-asset-group-acquires-korbit/3871783605440/)) 이후 미래에셋의 지분이 97.15%로 늘었다는 보도가 있지만, 이 내용은 거래소 뉴스 플래시(2차 출처)로만 확인했다. ([KuCoin news flash](https://www.kucoin.com/news/flash/mirae-asset-completes-korbit-acquisition-increases-stake-to-97-15))
- 코빗은 원화 거래가 가능한 국내 5개 거래소 중 4위로 소개된다. ([crypto.news](https://crypto.news/south-koreas-mirae-asset-completes-acquisition-of-crypto-exchange-korbit/)) 최초 인수 검토 보도는 2025-12-29에 나왔다. ([CoinDesk, 2025-12-29](https://www.coindesk.com/business/2025/12/29/south-korean-financial-group-mirae-asset-eyes-crypto-exchange-korbit-acquisition-report))

#### 코인원 (Coinone)
- OKX와 한국투자증권이 각각 약 20%의 코인원 지분을 신주 발행 방식으로 인수하는 방안이 2026-05-15에 보도되었다. 같은 기사는 디지털자산기본법에서 법인 34%, 개인 20%의 대주주 지분 상한이 논의되고 있다고 전했다. ([The Block, 2026-05-15](https://www.theblock.co/post/401431/okx-coinone-acquisition) [원문 열람]; [CoinDesk, 2026-05-15](https://www.coindesk.com/business/2026/05/15/okx-korea-investment-and-securities-said-to-be-in-talks-for-40-of-coinone))
- OKX Ventures와 한국투자증권은 각각 800억 원(약 5,300만 달러)을 투자해 19.6%씩 취득했다. 검색 요약에 따르면 FIU가 7월에 대주주 변경을 수리했고, 차명훈 대표가 약 30.36%와 경영권을 유지했다. ([CoinDesk, 2026-05-29](https://www.coindesk.com/markets/2026/05/29/okx-ventures-buys-usd53-million-stake-in-korea-s-coinone-exchange); [Ledger Insights](https://www.ledgerinsights.com/okx-korea-investment-securities-acquire-20-stakes-in-coinone-crypto-exchange/))
- FIU는 자금세탁방지 위반을 이유로 코인원에 과태료 52억 원과 3개월 일부 영업정지(2026-04-29~07-28)를 부과했다. ([AML Intelligence, 2026-04](https://www.amlintelligence.com/2026/04/news-south-korea-fines-crypto-exchange-coinone-3-5m-over-aml-violations/))

#### 고팍스 (Gopax, Binance 자회사)
- FIU는 2025-10-15에 Binance의 고팍스 대주주 변경을 최종 승인했다. Binance는 2023년 2월에 고팍스 지분 67%를 인수했지만(과거 사실) 승인이 2년 넘게 지연되었다. ([KED Global, 2025-10-16](https://www.kedglobal.com/cryptocurrencies/newsView/ked202510160007); [The Block](https://www.theblock.co/post/374486/binance-south-korea-gopax-review))

#### HashKey (별칭: HashKey Group, HashKey Holdings, HashKey Exchange, HashKey Chain, HSK, 3887.HK)
- HashKey Holdings는 2025-12-17에 홍콩거래소 메인보드에 상장했다. ([HashKey newsroom](https://group.hashkey.com/en/newsroom/hashkey-holdings-officially-lists-on-the-main-board-of-hkex)) 공모 규모는 The Block이 2억 600만 달러로, 다른 검색 요약이 2억 1,500만 달러로 적어 서로 다르다. ([The Block](https://www.theblock.co/post/382902/hashkey-hong-kong-debut))
- OSL과 HashKey는 2023년 8월에 홍콩 증권선물위원회(SFC)로부터 처음으로 개인 투자자 대상 거래소 운영 승인을 받았다(과거 사실). ([Wikipedia: OSL Group](https://en.wikipedia.org/wiki/OSL_Group) [원문 열람])

#### OSL (별칭: OSL Group, 863.HK, 옛 BC Technology Group)
- OSL Group은 홍콩거래소에 종목코드 863으로 상장되어 있다. ([Wikipedia: OSL Group](https://en.wikipedia.org/wiki/OSL_Group) [원문 열람]) 2024~2026년 사건(Banxa 인수, USDGO 스테이블코인 등)은 이번 조사에서 원문으로 확인하지 못했다.

#### Bitpanda (별칭: Bitpanda Technology Solutions)
- Bloomberg는 2026-01-13에 Bitpanda가 2026년 상반기 프랑크푸르트 상장을 준비하며 평가액 40억~50억 유로를 목표로 하고, Goldman Sachs, Citigroup, Deutsche Bank를 주관사로 선정했다고 보도했다. ([The Block, 2026-01-13](https://www.theblock.co/post/385494/bitpanda-ipo-2026) [원문 열람]; [Bloomberg](https://www.bloomberg.com/news/articles/2026-01-13/bitpanda-said-to-gear-up-for-frankfurt-ipo-in-first-half-of-2026))
- Deutsche Bank는 Bitpanda의 기술 부문과 Taurus를 활용해 2026년에 디지털자산 수탁 서비스를 출시할 계획이다. ([Cointelegraph](https://cointelegraph.com/news/deutsche-bank-crypto-custody-accounts-2026))

#### Bitget (BGB)
- Bitget EU는 2026-06-17에 오스트리아 금융시장감독청(FMA)에 MiCA 인가를 신청했다. ([Wikipedia: Bitget](https://en.wikipedia.org/wiki/Bitget) [원문 열람]; [Datawallet](https://www.datawallet.com/crypto/best-mica-licensed-crypto-exchanges))
- Wikipedia는 2026년 9월에 Bitget이 해킹으로 3억 8,750만 달러 상당의 자산을 잃었다고 적고 있다. 이 내용은 1차 출처로 확인하지 못했으므로 "미확인"으로 다뤄야 한다. ([Wikipedia: Bitget](https://en.wikipedia.org/wiki/Bitget) [원문 열람])
- 2024년 12월에 Bitget Wallet Token(BWB)이 BGB로 통합되었다(과거 사실). ([Wikipedia: Bitget](https://en.wikipedia.org/wiki/Bitget) [원문 열람])

#### KuCoin (KCS)
- KuCoin EU Exchange GmbH는 2025-11-27에 오스트리아 FMA로부터 MiCA CASP 인가를 받았다. ([CoinDesk, 2025-11-28](https://www.coindesk.com/policy/2025/11/28/crypto-exchange-kucoin-s-european-arm-wins-mica-license-in-austria)) 2차 출처는 FMA가 2026년 초에 준법 핵심 직위 공석을 이유로 신규 고객 유치를 막았다고 적었다. ([CASP Tracker](https://casptracker.eu/exchange/kucoin/))

#### Gate (별칭: Gate.io, GT)
- 몰타 금융감독청(MFSA)은 2025-09-29에 Gate Technology Ltd에 거래소와 수탁을 포함한 6개 CASP 업무를 인가했다고 검색 요약에 나온다. 1차 출처(ESMA 등록부)는 열지 못했다. ([Blockspot](https://blockspot.io/best-mica-licensed-crypto-exchanges-europe/))

#### Polymarket
- ICE는 2025-10-07에 Polymarket에 최대 20억 달러를 투자한다고 발표했다(투자 전 평가액 약 80억 달러). ICE는 Polymarket의 이벤트 데이터를 기관 고객에게 배포하고, 두 회사는 향후 토큰화 사업에서 협력하기로 했다. ([ICE IR, 2025-10-07](https://ir.theice.com/press/news-details/2025/ICE-Announces-Strategic-Investment-in-Polymarket/default.aspx) [원문 열람])
- Polymarket은 2025년 7월에 CFTC 인가 거래소 QCEX를 1억 1,200만 달러에 인수했고, 2025년 11월에 CFTC로부터 수정된 지정 명령을 받아 미국 시장에 다시 진입했다. ([Wikipedia: Polymarket](https://en.wikipedia.org/wiki/Polymarket) [원문 열람])

#### Kalshi
- Kalshi는 2025년에 Robinhood 예측시장 허브의 이벤트 계약 인프라가 되었고, 2026년 5월에 220억 달러 평가액으로 투자를 받았으며, 2026년에 크립토 연동 영구선물(perpetual futures)을 출시했다. ([Wikipedia: Kalshi](https://en.wikipedia.org/wiki/Kalshi) [원문 열람])

#### 일본: Coincheck, bitFlyer
- Coincheck는 2018년 4월에 Monex Group에 인수되었다(과거 사실). ([Wikipedia: Coincheck](https://en.wikipedia.org/wiki/Coincheck) [원문 열람]) 2차 출처는 Coincheck를 일본에서 등록 사용자가 가장 많은 거래소(2026년 기준 약 200만 명)로, bitFlyer를 비트코인 거래량 1위 거래소로 소개한다. ([iBuidl, 2026-03-10](https://ibuidl.org/blog/japan-crypto-exchange-comparison-2026-20260310))
- bitFlyer는 2014년에 설립되었고, 2023년 5월에 뉴욕 금융감독청으로부터 사이버보안 위반으로 120만 달러 제재를 받았다(과거 사실). ([Wikipedia: bitFlyer](https://en.wikipedia.org/wiki/BitFlyer) [원문 열람])

### Inferences
- Crypto.com은 2026년 한 해에만 Citadel Securities(기관), Trump Media·Yorkville(상장사·ETF), Robinhood(추적 중), Sui·XYO(프로젝트)와 연결된 발표를 냈기 때문에, 기관과 프로젝트를 동시에 잡아내는 데 효율이 높은 엔터티로 판단한다. CRO 토큰은 상위 125위 안팎에 있을 가능성이 높지만, 순위는 이번에 확인하지 않았다.
- 코빗, 코인원, 고팍스는 상장 공지가 업비트·빗썸만큼 가격을 움직이는지 근거를 찾지 못했다. 다만 2025~2026년에 미래에셋, 한국투자증권, OKX, Binance라는 금융기관·글로벌 거래소가 지분을 확보했으므로 "기관-거래소 연결" 사건으로서 추적 가치가 크다고 본다.
- Bitget, KuCoin, Gate, MEXC, HTX는 상장 공지가 중소형 토큰 가격을 움직일 수 있지만, 규제된 기관 관련성은 약하다. 따라서 Bitget만 Recommended로 두고 나머지는 Optional로 두는 편이 수집기의 잡음을 줄인다고 판단한다.
- Polymarket은 ICE(추적 중)가 대규모로 투자한 크립토 기반 시장이며 USDC로 정산되므로, ICE 엔터티만으로는 Polymarket 단독 기사(예: 토큰 발행설)를 놓칠 수 있다.

우선순위 표 (a):

| 후보 | 뉴스 속 별칭 | 국가 | 연결 프로젝트·토큰 | 등급 | 이름 충돌 위험 |
|---|---|---|---|---|---|
| Crypto.com | Crypto.com, Crypto.com Exchange, Crypto.com Custody, OG.com, Cronos | 싱가포르 본사로 알려짐(미확인) | CRO, SUI, XYO, Trump Media | Must | "Crypto.com Arena"(LA 경기장) 기사가 많다. "Cronos"는 대마초 기업 Cronos Group(NASDAQ: CRON)과 겹친다. "OG"는 일반 단어다. |
| 코빗 | Korbit, 코빗 | 한국 | 미래에셋 | Must (한국 범위) | 낮음 |
| 코인원 | Coinone, 코인원 | 한국 | OKX, 한국투자증권 | Must (한국 범위) | "coin one"처럼 띄어 쓴 일반 문구와 겹칠 수 있다. |
| 고팍스 | Gopax, GOPAX, 고팍스 | 한국 | Binance (BNB) | Recommended (Binance 엔터티에 별칭으로 넣어도 된다) | 낮음 |
| Bitstamp | Bitstamp | 룩셈부르크·영국 등 | Robinhood | 별칭 추가 (Robinhood) | 낮음 |
| Deribit | Deribit | 파나마·두바이로 알려짐(미확인) | Coinbase | 별칭 추가 (Coinbase), 인수 사실은 Gaps 참조 | 낮음 |
| HashKey | HashKey Group, HashKey Exchange, HashKey Chain, HSK | 홍콩 | HSK | Recommended | "HSK"는 중국어 시험 HSK와 겹친다. |
| OSL | OSL Group, 863.HK | 홍콩 | 미확인 | Recommended | 매우 높음: "OSL"은 오슬로 공항 코드이고 다른 약어로도 쓰인다. "OSL Group" 또는 맥락어를 요구해야 한다. |
| Bitpanda | Bitpanda, Bitpanda Technology Solutions | 오스트리아 | Deutsche Bank, Taurus | Recommended | "Bitpanda Technology Solutions"의 약칭 "BTS"는 K-pop 그룹과 겹치므로 약칭을 패턴에 넣지 않는다. |
| Bitget | Bitget, Bitget Wallet | 세이셸 | BGB | Recommended | 낮음 |
| Polymarket | Polymarket, QCEX | 미국 | ICE, USDC, Polygon(POL) | Recommended | 낮음 |
| Coincheck | Coincheck, Coincheck Group, CNCK | 일본 | Monex Group | Recommended (일본 범위) | 낮음 |
| bitFlyer | bitFlyer | 일본 | 미확인 | Optional | 낮음 |
| KuCoin | KuCoin, KuCoin EU | 세이셸 | KCS | Optional | 낮음 |
| Gate | Gate.io, Gate | 미확인 | GT | Optional | 매우 높음: "gate"는 일반 단어이고 "Bill Gates"와도 겹친다. "Gate.io" 또는 "Gate exchange"만 쓴다. |
| MEXC, HTX | MEXC, HTX(옛 Huobi) | 미확인 | HT/HTX | Optional | "HTX"는 휴스턴의 약칭으로도 쓰인다. |
| Kalshi | Kalshi | 미국 | 크립토 영구선물 | Optional | 낮음 |

### Gaps
- Coinbase의 Deribit 인수 완료일과 가격은 원문으로 확인하지 못했다. Coinbase 블로그는 403을 반환했고 Wikipedia 문서는 404였다. 학습 지식으로는 2025년 5월 발표, 2025년 8월 완료로 기억하지만 "미확인"으로 둔다.
- Bitpanda가 실제로 상장했는지, 상장했다면 언제인지는 확인하지 못했다.
- Coincheck Group의 Nasdaq 상장(티커 CNCK)과 2025~2026년 인수 활동은 원문으로 확인하지 못했다.
- bitFlyer와 그 밖의 일본 거래소(bitbank, GMO Coin, Binance Japan)의 2025~2026년 기관 사건은 찾지 못했다.
- Bitso, Backpack, Bitvavo, Bitkub, MEXC, HTX의 2025~2026년 사건은 검색 한도 때문에 조사하지 못했다.
- 크립토를 취급하는 증권 브로커(Webull, Futu/moomoo, Public, Trade Republic)와 브로커용 크립토 인프라(Zero Hash 등)는 조사하지 못했다.
- 한국 거래소별 상장 공지가 가격에 미치는 영향의 크기(업비트 대비 코인원·코빗·고팍스)는 근거 자료를 찾지 못했다.
- Bitget 해킹(2026년 9월)은 Wikipedia에만 근거하므로 1차 출처 확인이 필요하다.

## (b) 전통 거래소와 시장 인프라(일본거래소그룹, HKEX, SGX, 한국거래소, ASX, Euronext, B3, Eurex, LCH, OCC 등)의 크립토·토큰화 움직임은 무엇인가

### Takeaway
2025~2026년에 크립토 상품이나 토큰화 사업을 실제로 출시하거나 공식 계획을 낸 전통 인프라는 SGX(비트코인·이더 영구선물, 2026년 CFTC 승인), Boerse Stuttgart Group(Seturion, Nasdaq·Societe Generale 제휴), B3(이더·솔라나 선물, 토큰화 플랫폼과 헤알화 스테이블코인 계획), 한국거래소(현물 비트코인 ETF 준비)다. Eurex와 LCH는 각각 작업 중인 Deutsche Börse와 LSEG의 별칭으로 처리하면 충분하다. OCC는 이름 충돌이 심해서 정확한 전체 이름으로만 매칭해야 한다.

### Cited Findings

#### SGX (Singapore Exchange, SGX Derivatives)
- SGX Derivatives는 2025-11-24에 비트코인과 이더 영구선물을 출시했다. 계약 단위는 0.2 BTC와 5 ETH이고, 기초지수는 iEdge CoinDesk Crypto Indices이며, 기관·적격·전문 투자자만 거래할 수 있다. ([CoinDesk, 2025-11-17](https://www.coindesk.com/markets/2025/11/17/emb-9-20-am-utc-sgx-derivatives-debuts-bitcoin-ether-perpetual-futures-tied-to-iedge-coindesk-cryptocurrency-indices); [The Asset](https://www.theasset.com/article/55370/sgx-derivatives-to-launch-crypto-perpetual-futures))
- CFTC는 2026-09-10에 Regulation 48.10에 따라 미국 기관 투자자가 SGX의 비트코인·이더 영구선물을 거래할 수 있도록 승인했다. 검색 요약에 따르면 이 상품의 누적 거래량은 2026년 8월까지 58억 달러였다. ([Blockhead, 2026-09-14](https://www.blockhead.co/2026/09/14/sgx-wins-cftc-approval-to-open-bitcoin-ether-perps-to-us-institutions/))

#### 일본거래소그룹 (JPX, Japan Exchange Group, 도쿄증권거래소, 오사카거래소)
- JPX는 크립토를 대량 보유하는 상장사(디지털자산 트레저리 기업)에 대해 우회상장 규정 적용 강화와 재감사 요구 등을 검토했다. 여러 보도는 이 방안이 내부 검토 단계이며 공식 정책은 발표되지 않았다고 전했다. ([crypto.news](https://crypto.news/japan-exchange-group-weighs-tighter-oversight-of-crypto-treasury-firms/); [FinanceFeeds](https://financefeeds.com/japan-jpx-tightens-rules-crypto-treasury-firms/)) 보도 날짜는 검색 요약에 나오지 않아 확인하지 못했다.
- 일본은 크립토를 금융상품거래법 체계로 옮기는 법 개정을 추진했다. CoinDesk는 2026-04-10에 법안 추진을, 2026-07-15에 재분류 결정을 보도했다. ([CoinDesk, 2026-04-10](https://www.coindesk.com/policy/2026/04/10/japan-moves-to-classify-cryptocurrencies-as-financial-products); [CoinDesk, 2026-07-15](https://www.coindesk.com/policy/2026/07/15/japan-reclassifies-crypto-as-a-financial-asset-paves-way-for-tax-cuts))

#### 한국거래소 (KRX, Korea Exchange)
- 한국 정부는 2026년 경제성장전략에 현물 비트코인 ETF 허용을 넣었고, 금융위원회는 2026년 하반기에 자본시장법을 개정할 계획이다. ([Bloomingbit](https://en.bloomingbit.io/feed/news/116210); [Coinpaprika](https://coinpaprika.com/news/south-korea-spot-bitcoin-etf-2026-government-approves-plan/))
- 정은보 한국거래소 이사장은 거래소가 크립토 ETF를 상장하고 거래할 준비가 되어 있다고 밝혔다. ([CCN](https://www.ccn.com/news/crypto/south-korea-prepares-open-door-spot-bitcoin-crypto-etfs/))
- The Block은 2026년 2월 기사에서 한국 국회가 토큰증권(STO) 시장 관련 입법을 최근 통과시켰다고 언급했다. ([The Block, 2026-02-13](https://www.theblock.co/post/389835/mirae-asset-acquires-korbit) [원문 열람])

#### HKEX (Hong Kong Exchanges and Clearing, 홍콩거래소)
- HKEX에는 2025-12-17에 HashKey Holdings가 상장했다. ([HashKey newsroom](https://group.hashkey.com/en/newsroom/hashkey-holdings-officially-lists-on-the-main-board-of-hkex))
- 홍콩 당국은 2026년 말까지 외환기금채권(Exchange Fund Bills) 토큰화 시범, EnsembleTX를 통한 24시간 도매 CBDC 결제, CMU OmniClear 디지털자산 발행·결제 플랫폼을 추진한다. 이 계획의 주체는 HKMA(중앙은행)이며 HKEX가 아니다. ([Crypto Briefing](https://cryptobriefing.com/hong-kong-tokenized-exchange-fund-bills-2026/); [Ledger Insights](https://www.ledgerinsights.com/hong-kong-launches-tokenized-deposit-pilots-a-wholesale-cbdc-soon-not-yet/))
- SHEIN이 2026-09-01에 HKEX에 상장한 다음 날, xStocks가 Solana에서 $SHEINx를 발행했다. 이것은 HKEX가 아니라 xStocks(Kraken)의 사업이다. ([Solana Compass](https://solanacompass.com/news/shein-lists-on-hong-kong-stock-exchange-and-gets-tokenized-on-solana-as-sheinx-the-same-day))
- 검색 요약에는 "HKEX 블록체인 기반 다중자산 토큰화 플랫폼"이 언급되었지만, 근거가 거래소 뉴스 플래시(2차 출처)뿐이라 미확인으로 둔다. ([KuCoin news flash](https://www.kucoin.com/news/flash/hong-kong-plans-crypto-licensing-bill-advances-tokenized-finance))

#### B3 (B3 S.A. Brasil Bolsa Balcão)
- B3는 2026년에 토큰화 플랫폼과 브라질 헤알화 연동 스테이블코인을 출시할 계획이며, 주식시장 상품부터 토큰화하겠다고 밝혔다. ([CoinDesk, 2025-12-17](https://www.coindesk.com/business/2025/12/17/brazilian-stock-exchange-b3-to-launch-its-own-tokenization-platform-and-stablecoin))
- B3는 2025년 6월부터 이더와 솔라나 선물을 상장한다고 2025년 5월에 발표했다. ([FXStreet, 2025-05-09](https://www.fxstreet.com/amp/cryptocurrencies/news/brazilian-stock-exchange-set-to-list-ethereum-and-solana-futures-from-june-2025-202505092134)) 2026년 4월에는 비트코인 연동 이벤트 계약을 준비한다는 보도가 나왔다. ([CoinReporter, 2026-04](https://www.coinreporter.io/2026/04/brazils-b3-exchange/))

#### Euronext
- 21Shares는 2026-09-22에 유럽 최초의 Zcash(ZEC) ETP와 ether.fi(ETHFI) ETP를 Euronext 암스테르담·파리에 상장했다. ([The Crypto Times, 2026-09-22](https://www.cryptotimes.io/2026/09/22/21shares-brings-ethfi-and-zcash-etps-to-european-euronext-markets/))
- Euronext는 Tokeny에 투자한 적이 있다(과거 사실, 2019~2020년경). ([Ledger Insights](https://www.ledgerinsights.com/euronext-invests-tokeny-digital-assets-public-blockchain/); [The Block](https://www.theblock.co/linked/30222/euronext-invests-e5m-in-blockchain-fintech-tokeny-solutions)) Euronext CEO는 토큰화 관련 여러 사업을 검토하고 있다고 말했다. ([Markets Media](https://www.marketsmedia.com/euronext-exploring-tokenization-initiatives/)) 같은 기사에 나온 "2026년 9월부터 새 모델 제공"이 토큰화를 뜻하는지 결제 표준화를 뜻하는지는 검색 요약만으로 판단하지 못했다.

#### Boerse Stuttgart Group (별칭: Börse Stuttgart, Boerse Stuttgart Digital, BSDEX, Seturion, SeturionX, 옛 BX Digital)
- Nasdaq은 2026년 3월에 Seturion과 제휴해 Nasdaq의 유럽 거래소를 Seturion의 블록체인 결제 플랫폼에 연결하기로 했다. ([The Block](https://www.theblock.co/post/392931/nasdaq-boerse-stuttgarts-tokenized-settlement-europe); [Nasdaq 보도자료](https://view.news.eu.nasdaq.com/view?id=be351d0b3268dc7f2e400cc259f8ce77e&lang=en))
- 2026년 5월에 Seturion, flatexDEGIRO, Societe Generale과 그 디지털자산 자회사(SG-FORGE)가 협력해, Societe Generale이 토큰화 구조화상품을 Seturion을 통해 발행하기로 했다는 검색 요약이 있다. ([Bitcoin.com News](https://news.bitcoin.com/boerse-stuttgart-targets-europes-fragmented-markets-with-tokenized-trades/))
- Boerse Stuttgart Digital은 2026년 7월에 SG-FORGE의 MiCAR 준수 유로 스테이블코인 EUR CoinVertible(EURCV)을 거래·수탁 서비스에 통합했다. ([Crowdfund Insider, 2026-07](https://www.crowdfundinsider.com/2026/07/293440-boerse-stuttgart-digital-integrates-societe-generale-forge-euro-stablecoin/))
- 스위스 DLT 거래시설 BX Digital AG는 2026년 9월에 Seturion AG로 이름을 바꾸고 SeturionX 브랜드로 운영한다. ([Mondo Visione, 2026-09-15](https://mondovisione.com/media-and-resources/news/bx-digital-becomes-seturionx-2026915))

#### OCC (Options Clearing Corporation)
- OCC는 2026년 2월에 담보 유형 변경과 wrong-way risk 완화 규칙 변경을 제출했고, SEC가 승인했다. 이 규칙은 청산회원이나 그 계열사가 수탁기관을 맡은 현물 크립토 ETP 포지션에 추가 증거금을 부과한다. ([Federal Register, 2026-04-10](https://www.federalregister.gov/documents/2026/04/10/2026-06930/self-regulatory-organizations-the-options-clearing-corporation-order-approving-proposed-rule-change))

#### 참고: 이미 추적 중인 기관의 관련 사건
- Cboe와 S&P Dow Jones Indices는 2026-09-29에 연장한 라이선스 계약에서 토큰화 옵션을 검토할 수 있게 했다. ([CoinDesk, 2026-09-29](https://www.coindesk.com/business/2026/09/29/cboe-s-and-p-dow-jones-may-explore-tokenized-options-contracts-under-extended-licensing-deal))
- CFTC는 2025년 12월과 2026년 3월에 토큰화 자산 담보 사용과 FCM의 크립토 증거금 수령에 관한 지침·FAQ를 냈다. ([CFTC 보도자료 9303-26](https://www.cftc.gov/PressRoom/PressReleases/9303-26); [Morgan Lewis, 2026-03](https://www.morganlewis.com/pubs/2026/03/crypto-clarity-cftc-faqs-clarify-use-of-crypto-assets-by-registrants-and-registered-entities-part-2))

### Inferences
- Boerse Stuttgart Group은 2026년 3월, 5월, 7월, 9월에 Nasdaq(추적 중), Societe Generale(은행 조사자 범위), 유로 스테이블코인과 연결된 발표를 냈으므로 유럽 토큰화 결제 분야에서 Must로 판단한다.
- 한국거래소는 현물 ETF가 실제로 허용되면 상장 심사, 상장일, 수탁기관 선정 등 사건이 연달아 나올 것으로 보이므로 한국 범위에서 Must로 둔다. 다만 이것은 예측이며, 2026-10-01 현재 법 개정은 확인하지 못했다.
- SGX, JPX, HKEX, B3, Euronext는 비트코인·이더 중심이거나 정책 검토 단계라서 상위 125개 토큰 대부분에 직접 영향을 주지는 않는다. Recommended로 둔다. 그중 Euronext는 알트코인 ETP 상장지(ZEC, ETHFI 등)라서 개별 토큰과의 연결이 상대적으로 잦을 수 있다.
- Eurex(Deutsche Börse 자회사), LCH(LSEG 자회사)는 별도 엔터티보다 작업 중인 엔터티의 별칭으로 넣는 편이 중복을 줄인다.

우선순위 표 (b):

| 후보 | 뉴스 속 별칭 | 국가 | 연결 프로젝트·토큰 | 등급 | 이름 충돌 위험 |
|---|---|---|---|---|---|
| Boerse Stuttgart Group | Börse Stuttgart, Boerse Stuttgart Digital, BSDEX, Seturion, SeturionX, BX Digital | 독일·스위스 | Nasdaq, SG-FORGE EURCV | Must | "Stuttgart"만 쓰면 도시·축구팀(VfB Stuttgart) 기사와 겹친다. "Seturion"은 고유하다. |
| 한국거래소 | Korea Exchange, KRX, 한국거래소 | 한국 | BTC(현물 ETF 예정) | Must (한국 범위) | "Korea Exchange Bank"(외환은행, 하나은행에 합병)와 겹친다. 한국어 "거래소"는 가상자산 거래소를 뜻하는 경우가 많아 "한국거래소" 전체를 요구해야 한다. |
| SGX | Singapore Exchange, SGX, SGX Derivatives | 싱가포르 | BTC, ETH, CoinDesk Indices | Recommended | 낮음 |
| 일본거래소그룹 | Japan Exchange Group, JPX, Tokyo Stock Exchange, TSE, Osaka Exchange | 일본 | 크립토 트레저리 상장사(Metaplanet 등, 미확인) | Recommended (일본 범위) | "TSE"는 토론토증권거래소의 옛 약칭과 겹친다. |
| HKEX | HKEX, Hong Kong Exchanges and Clearing, 홍콩거래소 | 홍콩 | HashKey(상장사), 크립토 ETF | Recommended | 낮음 |
| B3 | B3, Brasil Bolsa Balcão | 브라질 | ETH, SOL 선물, 헤알화 스테이블코인(계획) | Recommended | 매우 높음: "B3"는 비타민 B3 등 일반 약어다. "B3"와 함께 Brazil·exchange·bolsa를 요구해야 한다. |
| Euronext | Euronext, Euronext Amsterdam/Paris | 유럽(네덜란드 등) | 21Shares ETP(ZEC, ETHFI), Tokeny | Recommended | 낮음 |
| Eurex | Eurex | 독일 | Deutsche Börse | 별칭 추가 (Deutsche Börse) | 낮음 |
| LCH | LCH, LCH SA, LCH DigitalAssetClear | 영국·프랑스 | LSEG | 별칭 추가 (LSEG) | 낮음 |
| OCC | Options Clearing Corporation | 미국 | 현물 크립토 ETP 담보 | Optional | 매우 높음: "OCC"는 크립토 뉴스에 자주 나오는 미국 통화감독청(Office of the Comptroller of the Currency)의 약칭과 같다. 전체 이름만 매칭해야 한다. |

### Gaps
- ASX, TMX(캐나다), 대만·태국·UAE 거래소, Moscow Exchange, Bolsa Mexicana의 2025~2026년 크립토 사건은 검색 한도 때문에 조사하지 못했다.
- Eurex와 LCH의 2025~2026년 크립토 상품(크립토 선물, DigitalAssetClear) 현황은 이번에 원문으로 확인하지 못했다.
- 한국예탁결제원(KSD), 일본 증권보관대체기구(JASDEC), 오사카디지털거래소(ODX)의 토큰증권 사업은 조사하지 못했다.
- JPX의 크립토 트레저리 규정 검토가 처음 보도된 날짜와 그 이후 확정 여부는 확인하지 못했다.
- 한국 현물 비트코인 ETF 관련 자본시장법 개정이 2026-10-01 현재 국회를 통과했는지는 확인하지 못했다.
- HKEX 자체의 토큰화 플랫폼 발표는 1차 출처를 찾지 못했다.

## (c) 수탁기관, 프라임 브로커, 마켓메이커 중 기관 추적기에 중요한 곳은 어디인가

### Takeaway
2025~2026년에 기관 발표에 가장 자주 등장한 곳은 FalconX(21Shares 인수, IPO 준비), Citadel Securities(Crypto.com·Ripple·Kraken 투자), Ripple Prime(옛 Hidden Road)이다. 수탁기관은 Copper(매각 추진), Taurus(유럽 은행 수탁 기술), Zodia Custody(Standard Chartered 흡수)가 사건을 냈지만, 각각 이름 충돌이나 모회사 편입 문제가 있어 패턴 설계에 주의해야 한다. 크립토 전문 마켓메이커(Wintermute, GSR, B2C2, Flowdesk, DWF Labs)는 이번 조사에서 대부분 2차 출처로만 확인되었다.

### Cited Findings

#### FalconX
- FalconX는 2025-11-20에 21Shares 인수를 완료했다. 거래는 2025-10-22에 발표되었고, 21Shares는 2025년 9월 말 기준 55개 상장 상품에서 110억 달러 이상을 운용하고 있었다. FalconX는 2025년에 Arbelos Markets와 Monarq Asset Management 과반 지분도 인수했다. ([FalconX newsroom](https://www.falconx.io/newsroom/falconx-completes-acquisition-of-21shares); [PR Newswire](https://www.prnewswire.com/news-releases/falconx-completes-acquisition-of-21shares-302620920.html))
- FalconX는 2026년 5월에 SEC에 비공개로 IPO 서류를 냈고, Cantor Fitzgerald를 자문사로 선정했다. 기사에 따르면 기관 고객은 600곳이 넘고 누적 거래량은 2조 달러다. ([Blockhead, 2026-05-29](https://www.blockhead.co/2026/05/29/falconx-files-confidentially-with-sec-for-ipo-hires-cantor-as-advisor/) [원문 열람])

#### Ripple Prime (옛 Hidden Road, Ripple 별칭 추가 후보)
- Ripple은 2025년 4월에 Hidden Road 인수를 발표했고, 2025년 10월에 12억 5,000만 달러 규모의 인수를 완료했다. Ripple은 이로써 글로벌 멀티에셋 프라임 브로커를 소유한 첫 크립토 기업이 되었다고 밝혔다. ([Ripple insights](https://ripple.com/insights/ripple-closes-hidden-road-acquisition/))
- 인수 후 Hidden Road는 Ripple Prime으로 이름이 바뀌었다. 2026년 5월 기사에 따르면 사업 규모가 세 배로 커졌고, Ripple은 2025년 11월에 Fortress Investment Group과 Citadel Securities가 주도한 5억 달러 투자를 400억 달러 평가액으로 유치했다. ([24/7 Wall St., 2026-05-02](https://247wallst.com/investing/2026/05/02/ripples-1-25-billion-hidden-road-acquisition-one-year-on-whats-changed/))
- 2026-03-02에 Hidden Road Partners CIV US LLC가 NSCC 시장참가자 식별자(MPID) 목록에 포함되었다. ([BeInCrypto](https://beincrypto.com/ripple-prime-nscc-xrp-ledger-integration-2026/))

#### Citadel Securities
- Citadel Securities는 2026-07-16에 Crypto.com에 4억 달러를 투자했다. ([CoinDesk, 2026-07-16](https://www.coindesk.com/business/2026/07/16/citadel-securities-invests-usd400-million-in-crypto-com-valuing-exchange-at-usd20-billion) [원문 열람]; [Bloomberg, 2026-07-23](https://www.bloomberg.com/news/articles/2026-07-23/citadel-securities-400-million-deal-marks-digital-asset-era))
- 검색 요약에 따르면 Citadel Securities는 2025년 11월에 Jane Street와 함께 Kraken에 투자했다(금액 2억 달러). ([Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/crypto-com-hits-20b-valuation-101233699.html))
- Citadel Securities는 2025년 11월 Ripple의 5억 달러 투자를 공동 주도했다. ([24/7 Wall St., 2026-05-02](https://247wallst.com/investing/2026/05/02/ripples-1-25-billion-hidden-road-acquisition-one-year-on-whats-changed/))

#### Jane Street
- CoinDesk는 2026-02-26에 "미국 장 개장 직후 비트코인 하락"을 Jane Street 탓으로 돌리는 주장이 X에서 퍼졌다고 보도하면서, 이 주장이 사실이 아닐 수 있는 이유를 다뤘다. ([CoinDesk, 2026-02-26](https://www.coindesk.com/markets/2026/02/26/why-crypto-x-thinks-jane-street-crashed-bitcoin-and-what-s-actually-behind-the-10-am-slam))
- Jane Street가 Citadel Securities와 함께 2025년 11월 Kraken 투자에 참여했다는 내용은 위의 검색 요약에 근거한다. ([Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/crypto-com-hits-20b-valuation-101233699.html))

#### Copper (별칭: Copper Technologies, Copper.co, ClearLoop)
- Copper는 2026년 5월에 약 5억 달러 가격으로 회사 매각을 추진했고, Cantor Fitzgerald가 매각 자문을 맡았다. ([CoinDesk, 2026-05-20](https://www.coindesk.com/business/2026/05/20/crypto-custody-firm-copper-is-looking-to-sale-the-company-for-usd500-million))
- 2차 출처에 따르면 ClearLoop는 거래소에 자산을 옮기지 않고 수탁 상태에서 DvP 결제를 하는 구조이며, 1,000곳이 넘는 상대방과 월 500억 달러 이상의 거래량을 처리한다. Copper Markets (US)는 SEC 등록 브로커딜러이자 FINRA 회원이 되었다(날짜 미확인). ([Coin Insider](https://www.coininsider.com/news/copper-seeks-500-million-buyer-for-clearloop-custody-and-settlement-platform); [Bitbase](https://www.bitbase.com/news/copper-expands-into-us-with-regulated-crypto-custody-and-trading-services))

#### Zodia Custody (Standard Chartered 별칭 추가 후보)
- Standard Chartered는 2026-05-18에 과반 지분을 가진 Zodia Custody의 수탁 사업을 인수한다고 발표했다. 두바이, 룩셈부르크, 홍콩의 StanChart 수탁 사업이 Zodia Custody와 합쳐진 뒤 StanChart 브랜드로 통합되며, 인프라 부문은 SC Ventures 아래 Zodia Solutions로 분리된다. ([CoinDesk, 2026-05-18](https://www.coindesk.com/business/2026/05/18/standard-chartered-to-acquire-remainder-of-subsidiary-zodia-custody); [Blockhead, 2026-05-19](https://www.blockhead.co/2026/05/19/standard-chartered-absorbs-zodia-custody-in-digital-asset-consolidation/))
- Julian Sawyer CEO는 2026-09-11에 물러나 자문역으로 옮겼다. ([CoinDesk, 2026-09-11](https://www.coindesk.com/business/2026/09/11/zodia-custody-ceo-julian-sawyer-steps-down-becomes-adviser))

#### Taurus (Taurus SA, Taurus-PROTECT)
- Deutsche Bank는 2023년부터 Taurus와 협력했고(과거 사실), 2026년에 Bitpanda 기술 부문과 Taurus를 활용해 수탁 서비스를 출시할 계획이다. ([Cointelegraph](https://cointelegraph.com/news/deutsche-bank-crypto-custody-accounts-2026))
- 영국 ClearBank는 2026년 1월에 스테이블코인 관련 서비스를 위해 Taurus-PROTECT를 선택했다. ([FinTech Futures](https://www.fintechfutures.com/blockchain-crypto-digital-assets/clearbank-partners-taurus-for-digital-asset-custody))
- 벨기에 KBC는 2026년 3월에 리테일 증권 플랫폼에서 크립토 거래를 시작하면서 Taurus를 수탁 파트너로 선택했다. ([EU Reporter, 2026-03-11](https://www.eureporter.co/videos/cryptocurrency/2026/03/11/kbc-becomes-first-belgian-bank-to-offer-regulated-crypto-trading-through-its-etail-brokerage-platform-selecting-taurus-as-custody-partner/); [FinTech Futures](https://www.fintechfutures.com/blockchain-crypto-digital-assets/kbc-selects-taurus-protect-to-power-its-crypto-custody-infrastructure))

#### Hex Trust
- Hex Trust는 2026년 2월 Consensus Hong Kong의 주요 후원사였다. ([Hex Trust](https://www.hextrust.com/resources-collection/hex-trust-concludes-consensus-hong-kong-2026)) 홍콩 기관 수탁 모델에 관한 기사도 있다. ([The Asian Banker](https://www.theasianbanker.com/updates-and-articles/hex-trust-s-custody-model-drives-hong-kong-s-institutional-digital-asset-push))

#### Komainu
- Komainu는 Nomura, Ledger, CoinShares의 합작 수탁기관이다. ([Dealroom](https://dealroom.co/companies/komainu/)) 2025~2026년 사건은 찾지 못했다.

#### 크립토 전문 마켓메이커 (Wintermute, GSR, B2C2, Flowdesk, DWF Labs, Cumberland)
- 업계 목록 기사들은 DWF Labs, Wintermute, GSR, Cumberland, B2C2를 주요 크립토 마켓메이커로 꼽는다. 이 출처들은 DWF Labs 자사 블로그 등 이해관계가 있는 2차 출처라는 점에 주의해야 한다. ([DWF Labs](https://www.dwf-labs.com/news/20-top-crypto-market-makers); [Coingape](https://coingape.com/blog/the-biggest-crypto-market-making-companies/))
- B2C2는 런던에 본사가 있고 일본 SBI Holdings가 소유한다. ([Eco](https://eco.com/support/en/articles/15426770-top-stablecoin-otc-desks-2026-b2c2-wintermute-cumberland-gsr))
- Wintermute는 2017년 런던에서 설립되었고, 하루 약 150억 달러를 65개 거래소에서 거래한다고 2차 출처가 소개한다. 검색 요약에는 Wintermute가 토큰화 금 OTC를 시작했다는 내용도 있다. ([Tracxn](https://tracxn.com/d/companies/wintermute/__73C04clWj_Ke9L7t29A2iEy1MWRE4ue1B74V8HL1qCY); [Coingape](https://coingape.com/blog/the-biggest-crypto-market-making-companies/))

### Inferences
- FalconX는 21Shares(이미 ETF 발행사 엔터티로 추적 중)를 소유하게 되었으므로, FalconX 엔터티를 추가하면 프라임 브로커 기사와 ETF 기사가 같은 그룹으로 연결된다. Must로 판단한다.
- Citadel Securities는 2025~2026년에 Kraken, Ripple, Crypto.com이라는 세 크립토 기업에 투자했으므로 Must로 판단한다. 다만 Citadel(헤지펀드, Citadel LLC)과 Citadel Securities(마켓메이커)는 다른 회사이므로 "Citadel Securities"를 정확히 매칭해야 한다.
- Ripple Prime과 Hidden Road는 Ripple(프로젝트 엔터티로 추적 중)의 기관 사업이므로 Ripple 엔터티에 별칭을 넣거나, 기관 성격을 살려 별도 institution 엔터티로 두고 XRP·RLUSD를 연결하는 두 방법이 있다. 어느 방식을 택할지는 사용자가 정할 사항이다.
- Copper, Taurus, Hex Trust는 은행 수탁 기술이나 토큰 재단 수탁처럼 기관-프로젝트 연결 사건을 만들지만, "copper"와 "taurus"는 일반 단어라서 맥락어 없이는 오탐이 매우 많을 것이다.
- 크립토 전문 마켓메이커는 토큰 런칭·상장·청산 기사에 자주 등장하지만 금융기관으로서의 성격은 약하다. 추적한다면 Wintermute 정도만 Recommended로 두고 나머지는 Optional이 적절하다고 본다.

우선순위 표 (c):

| 후보 | 뉴스 속 별칭 | 국가 | 연결 프로젝트·토큰 | 등급 | 이름 충돌 위험 |
|---|---|---|---|---|---|
| FalconX | FalconX | 미국 | 21Shares ETP·ETF, Cantor | Must | "Falcon Finance"(FF, USDf)와 겹치므로 "FalconX"를 단어 경계로 매칭해야 한다. |
| Citadel Securities | Citadel Securities | 미국 | Crypto.com(CRO), Ripple(XRP), Kraken | Must | "Citadel"만 쓰면 헤지펀드 Citadel LLC, 사우스캐롤라이나의 The Citadel 대학과 겹친다. |
| Ripple Prime | Ripple Prime, Hidden Road | 미국 | XRP, RLUSD | 별칭 추가 (Ripple), 등급은 Must 수준 | "hidden road"는 일반 문구로도 쓰일 수 있다. |
| Copper | Copper, Copper.co, ClearLoop, Copper Markets | 영국 | 미확인 | Recommended | 매우 높음: 금속 구리 시세 기사와 겹친다. ClearLoop·custody·crypto 맥락어를 요구해야 한다. |
| Taurus | Taurus, Taurus-PROTECT, Taurus SA | 스위스 | Deutsche Bank, KBC, ClearBank | Recommended | 매우 높음: 별자리, Taurus 총기, Ford Taurus와 겹친다. |
| Hex Trust | Hex Trust | 홍콩 | 미확인 | Recommended | "HEX" 토큰과 겹치므로 "Hex Trust" 전체를 요구해야 한다. |
| Zodia Custody | Zodia, Zodia Custody, Zodia Solutions | 영국 | Standard Chartered | Recommended (Standard Chartered 별칭 추가) | "Zodia"는 "Zodiac"의 앞부분과 같으므로 단어 경계(\bZodia\b)가 필요하다. |
| Jane Street | Jane Street | 미국 | Kraken, 비트코인 ETF | Recommended | 뉴욕의 거리 이름 "Jane Street"와 겹칠 수 있다. |
| Wintermute | Wintermute | 영국 | 다수 토큰(미확인) | Recommended | 낮음 |
| Komainu | Komainu | 영국·저지 등(미확인) | Nomura, CoinShares | Optional (Nomura 별칭 가능) | 일본의 사자 석상 "komainu"와 겹친다. |
| B2C2 | B2C2 | 영국 | SBI Holdings | Optional (SBI 별칭 가능) | "B2C"(기업-소비자 거래)와 비슷하므로 단어 경계가 필요하다. |
| GSR, Flowdesk, DWF Labs, Cumberland, Jump Crypto | GSR Markets, Flowdesk, DWF Labs, Cumberland DRW, Jump Crypto | 영국·프랑스·스위스 등(미확인) | 다수 토큰(미확인) | Optional | "GSR"(유전체 약어 등), "Cumberland"(지명), "Jump"(일반 단어)는 충돌이 크다. |

### Gaps
- Hex Trust의 2025~2026년 구체 사건(wXRP 등 래핑 토큰 발행, ETF 수탁, 라이선스)은 Hex Trust 뉴스 페이지가 404를 반환해 확인하지 못했다.
- Zodia Custody 인수가 2026년 8월 말 예정대로 완료되었는지는 확인하지 못했다.
- Copper 매각 결과(매수자, 완료 여부)는 확인하지 못했다.
- Ceffu(Binance 수탁), Amber Group, Cumberland, Jump Crypto, GSR, Flowdesk, Keyrock, Marex, StoneX, Clear Street, Talos, EDX Markets의 2025~2026년 기관 사건은 검색 한도 때문에 조사하지 못했다.
- Jane Street의 비트코인 ETF 보유 규모는 X 게시물에만 근거가 있어 신뢰할 수 있는 출처를 찾지 못했다.
- 마켓메이커별 토큰 계약(어떤 토큰의 유동성 공급자인지)은 1차 출처를 찾지 못했다.

## (d) 토큰화·RWA 플랫폼 중 추가해야 할 곳은 어디인가 (Figure, Superstate, Centrifuge, Digital Asset(Canton), Tokeny, Libre, Backed/xStocks, Dinari 등)

### Takeaway
rwa.xyz의 토큰화 국채 상위 상품(2026-10-01 확인)과 2025~2026년 발표를 함께 보면, Figure, Digital Asset(Canton Network), Centrifuge, Superstate가 기관-토큰 연결 사건을 가장 자주 만들며 Must로 판단한다. Backed Finance(xStocks)는 Kraken이 인수했으므로 Kraken 별칭으로 넣는다. Dinari, Apex Group(Tokeny), Libeara, Progmat(일본)은 Recommended다. 다만 "Figure", "Digital Asset", "Canton", "Backed"처럼 일반 단어인 이름이 많아서 이름 충돌 대책이 필수다.

### Cited Findings

#### rwa.xyz 토큰화 국채 현황 (2026-10-01 확인, 이 시점의 수치)
- 토큰화 국채의 분산 가치(Distributed Value)는 146억 5,000만 달러였고, 상품 수는 108개였다. 상위 10개 상품과 플랫폼은 다음과 같았다: Circle USYC(Circle) 24억 달러, Ondo USDY(Ondo) 22억 8,000만 달러, BlackRock BUIDL(Securitize) 22억 5,000만 달러, Franklin Templeton iBENJI 17억 2,000만 달러, WisdomTree WTGXX 12억 3,000만 달러, Franklin BENJI 6억 6,400만 달러, JPMorgan JLTXX(Kinexys Digital Assets) 5억 9,500만 달러, Invesco USTB(Superstate) 5억 8,900만 달러, ChinaAMC CUMIU(Libeara) 5억 5,300만 달러, Janus Henderson JTRSY(Centrifuge) 3억 4,400만 달러. ([rwa.xyz Treasuries](https://app.rwa.xyz/treasuries) [원문 열람])

#### Figure (별칭: Figure Technology Solutions, FIGR, Figure Markets, Figure Certificate Company, Provenance Blockchain, YLDS, HASH)
- YLDS는 Figure Certificate Company가 발행하는 SEC 등록 이자부 달러 상품이다. 2025년 2월에 Provenance Blockchain에서, 2025년 11월에 Solana에서 출시되었고, 2026-05-05에 Stellar에서도 출시되었다. Figure는 Nasdaq에 FIGR로 상장되어 있다. ([Eco: YLDS on Stellar](https://eco.com/support/en/articles/14982160-ylds-on-stellar-figure-s-yield-bearing-stablecoin-explained); [Eco: Figure onchain stack](https://eco.com/support/en/articles/14982167-figure-technology-s-onchain-stack-certificates-capital-markets-ylds))
- Figure는 토큰화 주식과 관련한 S-1 초안을 비공개로 제출했다고 발표했다(날짜 미확인). ([Stock Titan](https://www.stocktitan.net/news/FIGR/figure-technology-solutions-inc-announces-confidential-submission-of-v0hfjdc5zi6k.html))

#### Digital Asset (별칭: Digital Asset Holdings, Canton Network, Canton Coin, Daml)
- DTCC와 Digital Asset은 DTC가 보관하는 미국 국채를 Canton Network에서 토큰화하기로 했다. 2026년 상반기에 통제된 운영 환경에서 MVP를 만들고 이후 범위를 넓힐 계획이며, 이 협력은 DTCC가 SEC로부터 토큰화 서비스에 관한 no-action letter를 받은 뒤에 나왔다. ([Canton Network 보도자료](https://www.canton.network/canton-network-press-releases/dtcc-and-digital-asset-partner-to-tokenize-dtc-custodied-u.s.-treasury-securities-on-the-canton-network); [Ledger Insights](https://www.ledgerinsights.com/dtcc-to-tokenize-us-treasuries-on-canton-network/))
- 검색 요약에 따르면 DTCC는 DTC Tokenization Service를 2026년 10월에 출시할 계획이다. ([crypto.news](https://crypto.news/citi-says-77-of-institutions-eye-tokenized-collateral/))

#### Centrifuge (CFG)
- New York Life Investment Management는 2026-06-30에 Centrifuge와 함께 미국 하이일드 회사채 전략을 토큰화했고, 투자자는 USDC로 청약·환매할 수 있다. ([Business Wire, 2026-06-30](https://www.businesswire.com/news/home/20260630051099/en/Centrifuge-and-New-York-Life-Investment-Management-Partner-to-Tokenize-U.S.-High-Yield-Corporate-Bond-Strategy); [CoinDesk, 2026-06-29](https://www.coindesk.com/business/2026/06/29/new-york-life-makes-tokenization-debut-with-onchain-high-yield-bond-fund-with-centrifuge))
- 2차 출처는 Centrifuge가 2026년 2분기에 Coinbase, Ethena, Kraken Institutional, OKX와 제휴했고, Ethena가 2026년 6월에 JAAA에 2억 5,000만 달러를 배분했다고 적었다. ([Tokenized Living](https://tokenizedliving.com/centrifuge-integrating-real-world-assets-into-defi/)) 2026-09-26에는 Symbiotic Liquid Lane 통합 보도가 있었다. ([Gokhshtein](https://gokhshtein.com/news/2026-09-26-centrifuge-integrates-symbiotic-liquid-lane-for-16b))

#### Superstate
- Superstate는 2026-01-22에 Bain Capital Crypto와 Distributed Global이 주도한 8,250만 달러 시리즈 B를 마쳤다. ([CoinDesk, 2026-01-22](https://www.coindesk.com/business/2026/01/22/tokenization-firm-superstate-raises-usd82-5-million-to-bring-wall-street-onchain); [The Block](https://www.theblock.co/news/deals/2026-01-22-superstate-raises-82-5-million-usd-series-b-funding-round-386690))
- Opening Bell 플랫폼에는 GLXY(Galaxy), FWDI(Forward Industries), SBET(SharpLink Gaming), EXOD(Exodus) 등의 토큰화 주식이 Ethereum이나 Solana에 있다. 2025년 말에는 SEC 등록 상장사가 토큰화 주식을 직접 발행하는 Direct Issuance Programs를 발표했다. ([Superstate docs](https://docs.superstate.com/tokenized-equities); [The Block](https://www.theblock.co/post/382027/superstates-new-direct-issuance-programs-let-public-companies-raise-capital-using-tokenized-stock))
- Opening Bell 토큰화 주식은 Solana 대출 프로토콜 Kamino에서 담보로 쓸 수 있다. ([The Defiant](https://thedefiant.io/news/defi/superstate-tokenized-shares-collateral-solana-defi-kamino))

#### Backed Finance / xStocks (Kraken 별칭 추가 후보)
- Kraken은 2025-12-02에 xStocks 운영사인 스위스 Backed Finance AG 인수를 발표했다. 발표 시점에 xStocks는 Solana와 Ethereum에서 60개가 넘는 상품을 운영했고 누적 거래량이 100억 달러를 넘었다. ([Kraken blog](https://blog.kraken.com/news/backed-acquisition); [The Block](https://www.theblock.co/post/381095/kraken-to-buy-backed-finance-in-tokenization-push-ahead-of-ipo); [Business Wire, 2025-12-02](https://www.businesswire.com/news/home/20251202666578/en))
- xStocks는 2026-09-02에 HKEX 상장 첫날 다음 날 SHEIN 토큰($SHEINx)을 발행했다. ([Solana Compass](https://solanacompass.com/news/shein-lists-on-hong-kong-stock-exchange-and-gets-tokenized-on-solana-as-sheinx-the-same-day))

#### Dinari (dShares)
- Dinari는 2026-08-04에 S&P 500 전체를 포함한 미국 주식 724종목의 토큰을 미국 투자자와 금융기관에 열었고, Circle과 제휴해 자기수탁 지갑의 USDC로 매수하게 했다. Dinari는 SEC 등록 브로커딜러이자 이전대리인(transfer agent)이다. ([CoinDesk, 2026-08-04](https://www.coindesk.com/business/2026/08/04/dinari-brings-tokenized-u-s-stocks-to-american-investors-as-equity-race-heats-up); [Fortune, 2026-08-04](https://fortune.com/2026/08/04/dinari-stripe-apple-alums-partnership-circle-tokenized-stocks-us-investors/))
- dShares는 Ethereum, Arbitrum, Base, Avalanche에서 발행되며, Sei 지원 계획이 2026-09-26에 보도되었다. ([The Crypto Times, 2026-09-26](https://www.cryptotimes.io/2026/09/26/dinari-plans-to-bring-tokenized-sp-500-shares-to-sei/))
- Dinari는 카카오페이증권과 한국 주식 토큰화를 검토하고 있다는 보도가 있다(날짜 미확인). ([UseTheBitcoin](https://usethebitcoin.com/news/kakao-pay-dinari-tokenized-korean-stocks/))

#### Apex Group / Tokeny
- Apex Group은 Tokeny 과반 지분을 인수했고, 최초 투자(2023년 12월) 후 3년 안에 100% 지배권을 갖는 구조다. Tokeny는 ERC-3643 표준을 만들었고 320억 달러가 넘는 자산 토큰화에 쓰였다고 밝힌다. ([Apex Group](https://www.apexgroup.com/insights/apex-group-acquires-majority-stake-in-tokeny-to-catalyse-widespread-industry-tokenisation-adoption/); [Asset Servicing Times](https://www.assetservicingtimes.com/assetservicesnews/industryarticle.php?article_id=16755))
- 2026년 3월에 T-REX Network가 Polygon 기술로 만든 T-REX Ledger를 공개했고, Tokeny가 이를 지원한다. ([The Block](https://www.theblock.co/post/394284/apex-group-taps-polygon-trex-ledger))
- 2026년 3월에 Coinbase Asset Management가 Apex Group과 함께 Bitcoin Yield Fund를 Base에서 토큰화했다는 보도가 있다. ([RWA Times](https://rwatimes.substack.com/p/coinbase-and-apex-group-tokenize))

#### Libeara
- rwa.xyz에서 ChinaAMC USD Digital Money Market Fund(CUMIU)의 플랫폼으로 Libeara가 표시되어 있다(2026-10-01 확인). ([rwa.xyz Treasuries](https://app.rwa.xyz/treasuries) [원문 열람]) Libeara의 소유 구조와 2025~2026년 발표는 원문으로 확인하지 못했다.

#### Progmat (일본)
- Progmat은 블록체인 기반 디지털자산 플랫폼이며, 363개 회사가 참여하는 Digital Asset Co-Creation Consortium(DCC)을 운영한다. ([Progmat](https://progmat.co.jp/en/) [원문 열람]) 주주 구성(MUFG 등)과 2025~2026년 사건은 페이지에서 확인하지 못했다.

### Inferences
- Figure는 YLDS가 Provenance, Solana, Stellar(추적 중인 프로젝트)로 확장되었고 Nasdaq 상장사이므로 Must로 판단한다. 다만 "Figure"는 일반 명사이자 로봇 기업 Figure AI의 이름이라서 "Figure Technology", "Figure Markets", "FIGR", "YLDS"처럼 구체적 패턴만 써야 한다.
- Digital Asset과 Canton Network는 DTCC(추적 중)의 국채 토큰화 사업자이므로 Must로 판단한다. "digital asset"은 크립토 기사에서 가장 흔한 일반 명사이고 "Canton"은 지명(미국 오하이오주 Canton, 광저우의 옛 영어 이름, Canton Fair)이므로, "Digital Asset Holdings", "Canton Network", "Canton Coin"만 매칭해야 한다.
- Centrifuge는 CFG 토큰을 가진 프로젝트이면서 New York Life, Janus Henderson 같은 운용사의 토큰화 대행사이므로, project 엔터티로 추가하고 기관과 함께 나오면 "high" 알림이 나가도록 하는 편이 맞다고 본다.
- Superstate는 Galaxy(작업 중)와 여러 크립토 트레저리 상장사의 주식을 토큰화했고 rwa.xyz 상위 10위 상품의 플랫폼이므로 Must로 판단한다. rwa.xyz가 USTB를 Invesco 상품으로 표시한 점은 Invesco(추적 중)와의 관계 변화를 시사하지만, 이번 조사에서 원문을 확인하지 못했다.
- Backed Finance는 "backed by"와 같은 일반 표현과 겹치므로 "Backed Finance"와 "xStocks"만 Kraken 별칭으로 추가하는 것이 안전하다.

우선순위 표 (d):

| 후보 | 뉴스 속 별칭 | 국가 | 연결 프로젝트·토큰 | 등급 | 이름 충돌 위험 |
|---|---|---|---|---|---|
| Figure | Figure Technology Solutions, FIGR, Figure Markets, Figure Certificate Company, YLDS, Provenance Blockchain | 미국 | HASH, YLDS, SOL, XLM | Must | 매우 높음: 일반 명사 "figure", 로봇 기업 Figure AI와 겹친다. "Provenance"도 일반 단어다. |
| Digital Asset | Digital Asset Holdings, Canton Network, Canton Coin, Daml | 미국 | CC(Canton Coin), DTCC | Must | 매우 높음: "digital asset"은 일반 명사다. "Canton"은 지명이다. |
| Centrifuge | Centrifuge | 미국·독일(미확인) | CFG, JTRSY, JAAA, USDC | Must (project 엔터티) | 실험실 원심분리기 기사와 겹친다. |
| Superstate | Superstate, Opening Bell, USTB, USCC | 미국 | Galaxy(GLXY), SBET, FWDI, EXOD, Kamino | Must | "super state"라는 정치 용어와 겹칠 수 있다. "Opening Bell"은 장 시작 일반 표현이다. |
| xStocks / Backed Finance | xStocks, Backed Finance, Backed | 스위스 | Kraken, SOL, ETH | 별칭 추가 (Kraken) | "Backed"는 일반 단어다. "Backed Finance"만 쓴다. |
| Dinari | Dinari, dShares | 미국 | USDC, Arbitrum, Base, Avalanche, Sei | Recommended | 낮음 |
| Apex Group / Tokeny | Apex Group, Tokeny, T-REX, ERC-3643 | 룩셈부르크·버뮤다(미확인) | Polygon, Coinbase Asset Management | Recommended | "Apex"는 Apex Legends(게임)와 증권 청산사 Apex Fintech/Apex Clearing과 겹친다. "Apex Group"만 쓴다. |
| Libeara | Libeara | 싱가포르(미확인) | ChinaAMC CUMIU | Recommended | 낮음 |
| Progmat | Progmat, Progmat Coin | 일본 | MUFG(미확인) | Recommended (일본 범위) | 낮음 |
| Libre, Plume, OpenEden, Spiko, Midas | Libre, Plume, OpenEden, Spiko, Midas | 미확인 | PLUME 등 | Optional (미조사) | "Libre"(스페인어 일반 단어, LibreOffice), "Midas"(신화·자동차 정비 체인)는 충돌이 크다. |

### Gaps
- Libre(Laser Digital·WebN 계열로 알려짐), Plume, OpenEden, Spiko, Midas, Archax, 21X, ADDX, R3, Fnality, Partior의 2025~2026년 사건은 검색 한도 때문에 조사하지 못했다.
- Figure의 토큰화 주식 S-1 초안 제출 날짜와 내용, Figure Markets의 2026년 사업 확장은 원문으로 확인하지 못했다.
- Digital Asset·DTCC MVP가 2026년 상반기에 실제로 가동되었는지, DTC Tokenization Service가 2026년 10월에 출시되었는지는 확인하지 못했다.
- rwa.xyz가 USTB를 Invesco 상품으로 표시한 배경(인수, 관리 위탁 등)은 확인하지 못했다.
- Kraken의 Backed Finance 인수 완료일은 발표일(2025-12-02)과 별개로 확인하지 못했다.
- rwa.xyz의 토큰화 주식(stocks) 페이지와 비공개 신용(private credit) 페이지는 열지 않았으므로, 그 분야의 상위 플랫폼 순위는 이 노트에 없다.
- Progmat의 주주 구성과 2025~2026년 발표, 한국 토큰증권 플랫폼(증권사 컨소시엄 등)은 조사하지 못했다.
