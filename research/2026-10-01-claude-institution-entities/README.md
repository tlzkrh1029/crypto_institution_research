# 2026-10-01 Claude Code 기관 엔터티 확대

- 작성 도구: Claude Code (claude.ai/code 클라우드 세션). 분야별 조사 에이전트 5개가 규칙과 실제 헤드라인 시험 사례를 만들었고, Claude Code가 합치고 검증했다.
- 작성 시각: 2026-10-01 13:10 KST 전후
- 조사 범위: 사용자가 요청한 기관(Grayscale, Robinhood, BlackRock, Coinbase, MoneyGram, Santander 등)과 같은 분야의 주요 기관을 뉴스 대조용 기관 엔터티로 등록하고, 기존 기관의 규칙을 다시 검토했다.
- 조사하지 못한 범위: 규칙을 만든 에이전트와 다른 에이전트가 따로 모은 헤드라인으로 다시 검증하는 단계(D-017)는 이번에 거치지 않았다. 아래 "한계" 절에 적었다.
- 관련 결정: [D-019](../../docs/decisions.md)

## 결과

기관은 25곳에서 85곳으로 늘었다. 새로 60곳을 등록했고, 기존 25곳 가운데 20곳의 규칙을 다시 만들었다. BVNK, Bybit, LF Decentralized Trust, IBM, Bank of England의 규칙은 그대로 두었다. 모든 기관에 분야(`category`)를 붙였다.

| 분야 | 수 | 기관 |
|---|---|---|
| 은행 (bank) | 21 | U.S. Bank, JPMorgan, Citi, BNY, State Street, Goldman Sachs, HSBC, Banco Santander, Morgan Stanley, Bank of America, Wells Fargo, Deutsche Bank, UBS, BNP Paribas, Société Générale, Standard Chartered, Barclays, MUFG, SBI Holdings, Nomura, Shinhan Financial |
| 운용사 (asset_manager) | 16 | Franklin Templeton, BlackRock, Fidelity, Grayscale, Bitwise, 21Shares, VanEck, Invesco, WisdomTree, ARK Invest, CoinShares, Canary Capital, Hashdex, Apollo, KKR, Hamilton Lane |
| 거래소·증권사 (exchange_broker) | 17 | Bybit, Nasdaq, ICE/NYSE, CME Group, Coinbase, Robinhood, Kraken, Gemini, Binance, OKX, Bullish, Cboe, Charles Schwab, Interactive Brokers, eToro, 업비트, 빗썸 |
| 결제·스테이블코인 (payments_stablecoin) | 12 | BVNK, Visa, Mastercard, PayPal, Stripe, MoneyGram, Western Union, Circle, Paxos, Block, Revolut, Tether |
| 시장 인프라 (market_infrastructure) | 10 | The Clearing House, DTCC, Swift, Euroclear, Broadridge, Cantor Fitzgerald, Clearstream, SIX·SIX Digital Exchange, LSEG, Deutsche Börse |
| 수탁·인프라 (custody_infra) | 6 | Anchorage Digital, BitGo, Fireblocks, Galaxy Digital, Securitize, Copper |
| 중앙은행 (central_bank) | 1 | Bank of England |
| 기타 (other) | 2 | LF Decentralized Trust, IBM |

## 방법

- 분야를 다섯으로 나눠 에이전트마다 한 분야를 맡겼다. 각 에이전트는 기관마다 규칙을 만들고, 크립토 관련 실제 헤드라인(긍정 사례)과 이름이 다른 뜻으로 쓰였거나 크립토와 무관한 실제 헤드라인(부정 사례)을 출처 URL과 함께 모았다. 그리고 수집기의 실제 대조 코드로 시험했다.
- 기존 기관 규칙은 문맥 조건으로 "토큰화, 블록체인, 크립토, 결제(settlement)" 같은 단어를 요구했다. 이 조건은 코인 이름만 나오는 헤드라인(예: "BlackRock files for spot Ethereum ETF")을 놓쳤고, 소송 합의(settlement) 기사를 잘못 잡았다. 은행 분야 에이전트가 같은 자료로 비교한 결과, 기존 조건은 긍정 사례 175건 가운데 26건을 놓치고 부정 사례 130건 가운데 11건을 잘못 잡았다.
- 그래서 분야마다 크립토 문맥 단어 목록을 새로 만들었다(`crypto_asset`, `crypto_exchange`, `crypto_payments`, `crypto_bank`, `crypto_infra`). 목록마다 그 분야의 실제 헤드라인으로 검증했으므로 하나로 합치지 않았다.
- 실제 헤드라인 시험 사례 1,480건은 [tests/test_entities_institutions.py](../../tests/test_entities_institutions.py)에 출처 URL과 함께 있다. 전체 시험 3,181개가 통과했다.

## 제외하거나 따로 둔 것

- 국내 은행 초안 가운데 KB국민은행과 하나은행은 확인된 실제 사례가 너무 적어 등록하지 않았다. Zelle(Early Warning Services)도 같은 이유로 뺐다. 이후 추천 조사([2026-10-01 기관 추가 후보 조사](../2026-10-01-claude-institution-recommendations/README.md))에서 세 곳 모두 필수 후보로 다시 올랐으므로, 다음 확대 때 실제 사례를 더 모아 등록한다.
- 크립토 단어가 없는 헤드라인 1건("Citi, Goldman back TRM Labs ...")은 문맥 조건으로 잡을 수 없어 시험에서 "알고 놓치는 사례"로 따로 두었다.

## 확인한 동작

- 사용자가 지목한 회사의 대표 문장이 의도대로 대조된다. 예를 들어 "Grayscale files to convert Cardano trust into spot ETF"는 Grayscale과 Cardano가 함께 대조되어 high 알림이 된다. 반대로 회색조 사진, 로빈 후드 재단, 스페인 도시 산탄데르, 비자 수수료, 형용사 bullish 같은 문장은 대조되지 않는다.
- 2026-10-01에 연준, DTCC, Hedera, Stellar 피드로 병합 전 규칙과 비교했다. 달라진 것은 DTCC 피드의 일반 기사 21건에서 DTCC가 더는 대조되지 않는다는 점이다. DTCC 규칙이 크립토 문맥을 요구하게 되었기 때문이다. 이 피드는 `publisher_entity: dtcc`로 모든 글에 DTCC를 붙이므로, 사건 기록에는 영향이 없다.

## 한계

- 규칙을 만든 에이전트가 직접 모은 사례로만 시험했다. 지난 종목 작업([2026-10-01 뉴스 대조 범위 시험 확대](../2026-10-01-claude-entity-ranks-11-20/README.md))에서는 다른 에이전트가 모은 헤드라인으로 검증하자 종목마다 놓치는 사례가 나왔다. 기관 규칙도 같은 검증을 거치면 놓치는 사례가 나올 수 있다.
- 거래소와 결제 회사가 기관으로 등록되면서, "Robinhood가 DOGE를 상장했다" 같은 상장 소식도 high 알림이 된다. 알림이 지나치게 많아지면 분야(`category`)별로 알림을 조정한다.
- 영문 헤드라인만 시험했다. 업비트와 빗썸 규칙에는 한국어 이름도 들어 있지만, 지금 수집원에는 한국어 피드가 없다.
