# 맥북 설치와 운영 안내

이 문서는 수집 프로그램을 맥북에 설치하고 상시 실행하는 방법을 설명한다. 설계 배경은 [collector-spec.md](collector-spec.md) 8절에 있다. 명령은 Apple Silicon과 Intel 맥북에 공통으로 쓸 수 있는 것만 적었다. 명령은 모두 "터미널" 앱(응용 프로그램 > 유틸리티 > 터미널)에서 실행한다.

## 1. 맥북 정보 확인

설치 방식을 정하려면 다음 정보가 필요하다 ([open-questions.md](open-questions.md) Q2).

화면에서 확인하는 방법은 다음과 같다.

- 칩, macOS 버전, 메모리: 화면 왼쪽 위 Apple 메뉴 > "이 Mac에 관하여"를 연다. "칩" 항목이 Apple M으로 시작하면 Apple Silicon이고, "프로세서" 항목에 Intel이 보이면 Intel 맥북이다.
- FileVault: 시스템 설정 > 개인정보 보호 및 보안 > FileVault 항목에서 켬·끔을 확인한다.

터미널에서 한 번에 확인할 수도 있다. 이 명령들은 일련번호 같은 개인 식별 정보를 출력하지 않는다.

```sh
sw_vers -productVersion               # macOS 버전 (예: 15.6)
uname -m                              # arm64이면 Apple Silicon, x86_64이면 Intel
sysctl -n machdep.cpu.brand_string    # 칩 이름
fdesetup status                       # FileVault is On. 또는 Off.
python3 --version                     # 설치된 Python 버전 (없으면 설치 안내 창이 뜬다)
```

알려 줄 정보는 다음과 같다. 공개 저장소에 기록되므로, 판단에 필요한 수준만 적는다.

- 칩 종류 (Apple Silicon 또는 Intel)와 macOS 버전
- FileVault 켜짐 여부
- 메모리 크기 (나중에 로컬 AI 모델을 쓸지 판단할 때만 필요하다)
- 덮개를 열어 둔 채 전원을 계속 연결해 둘 수 있는지

일련번호, IP 주소, 공유기 설정, 설치 장소의 주소는 알려 주지 않아도 되고, 저장소에 적지 않는다.

## 2. 준비

- Python 3.11 이상이 필요하다. `python3 --version`의 결과가 3.11보다 낮거나 명령이 없으면, [python.org](https://www.python.org/downloads/macos/)에서 최신 macOS 설치 파일을 내려받아 설치한다. 설치한 뒤에도 `python3 --version`이 예전 버전을 보여 주면, 아래 명령의 `python3`를 `python3.13`처럼 설치한 버전 이름으로 바꿔 쓴다.
- git이 필요하다. 처음 `git`을 실행하면 macOS가 개발자 도구 설치를 안내한다.

## 3. 설치

```sh
cd ~
git clone https://github.com/tlzkrh1029/crypto_institution_research.git
cd crypto_institution_research
python3 -m venv .venv
.venv/bin/pip install -e .
cp .env.example .env
```

## 4. `.env` 편집

`.env`는 비밀 값을 두는 파일이다. `.gitignore`로 제외되어 있어 공개 저장소에 올라가지 않는다. 터미널 편집기 nano로 연다. 텍스트 편집기 앱은 따옴표를 모양이 다른 따옴표로 바꿀 수 있으므로 쓰지 않는다.

```sh
nano .env
```

화살표 키로 줄을 옮겨 값을 고친다. 저장은 Control+O를 누른 뒤 Enter, 종료는 Control+X다.

### 4-1. SEC 수집원 켜기 (`SEC_USER_AGENT`)

SEC는 자동으로 접속하는 프로그램에 "누가 요청하는지"를 요청 헤더에 밝히라고 요구한다. 형식은 이름과 연락 가능한 이메일이다 (SEC 예시: `Sample Company Name AdminContact@<sample company domain>.com`). 개인이라면 다음처럼 적는다.

```
SEC_USER_AGENT="Hong Gildong personal-research gildong@example.com"
```

- 이름과 이메일은 본인 것으로 바꾼다. 이메일은 실제로 확인하는 주소를 쓴다. 요청이 문제가 되면 SEC가 이 주소로 연락할 수 있다.
- 이 값은 sec.gov에 보내는 요청의 헤더에만 들어간다. `.env`에 있으므로 저장소에는 올라가지 않는다. 코드나 문서, AI 대화에는 붙여 넣지 않는다.
- 저장한 뒤 다음 명령으로 확인한다. `check-config` 결과에서 sec-press와 sec-speeches 옆의 `[skipped: SEC_USER_AGENT not set]`이 사라지고, `once` 결과에 `sec-press: ok`가 나오면 된다.

```sh
.venv/bin/python -m collector check-config
.venv/bin/python -m collector once --source sec-press --source sec-speeches
```

### 4-2. 텔레그램 알림 설정

알림은 텔레그램 봇으로 받는다 ([decisions.md](decisions.md) D-010). 봇은 한 번만 만들면 된다.

1. 텔레그램 앱에서 `@BotFather`를 검색해 연다. 이름 옆에 파란 인증 표시가 있는 공식 계정인지 확인한다.
2. `/newbot`을 보낸다. 봇 이름(예: `내 크립토 수집기`)과 사용자명을 차례로 입력한다. 사용자명은 영문이어야 하고 `bot`으로 끝나야 한다 (예: `gildong_collector_bot`).
3. BotFather가 `123456789:AAH...` 모양의 토큰을 알려 준다. 이 토큰을 `.env`의 `TELEGRAM_BOT_TOKEN`에 넣는다. 토큰을 가진 사람은 누구나 이 봇으로 메시지를 보낼 수 있으므로, 채팅이나 AI 대화에 붙여 넣지 않는다.
4. BotFather가 알려 준 봇 링크(`t.me/...`)를 열고 "시작"을 누르거나 아무 메시지나 보낸다. 봇은 사용자가 먼저 말을 걸기 전에는 메시지를 보낼 수 없다.
5. 맥북 터미널에서 다음 명령을 실행한다. `TELEGRAM_CHAT_ID=...` 형태의 줄이 나오면 그 줄을 `.env`에 옮겨 적는다.

   ```sh
   .venv/bin/python -m collector telegram-chat-id
   ```

6. `.env`에서 `NOTIFIER="telegram"`으로 바꾼다. `.venv/bin/python -m collector check-config`를 실행해 `notifier: telegram (telegram token set, chat id set)` 줄이 나오면 값이 제대로 들어간 것이다. 이 명령은 토큰 값 자체는 출력하지 않는다.
7. 시험 알림을 보낸다. 텔레그램에 `[TEST] collector notification test` 메시지가 오면 설정이 끝난다.

   ```sh
   .venv/bin/python -m collector notify-test
   ```

8. 자동 실행 중이라면 7절의 재시작 명령으로 수집기를 다시 시작해 새 설정을 적용한다.

알림은 다음과 같이 온다.

- `[HIGH]`: 한 자료에 기관과 프로젝트가 함께 나왔다.
- `[MEDIUM]`: 기관이나 규제기관의 피드에 프로젝트가 나왔거나, 60분 동안 한 종목이 같은 거래소의 BTC보다 3%p 이상 더 움직였다 ([decisions.md](decisions.md) D-011).

모든 알림은 `data/collector.log`에도 남는다. 전송에 실패한 알림은 5분마다 다시 보내며, 최대 12번(약 1시간) 시도한다. 토큰이 유출되었다고 생각되면 BotFather에서 `/revoke`로 새 토큰을 받고 `.env`를 고친다.

### 4-3. 외부 감시 신호 (`HEARTBEAT_URL`)

수집기가 멈추면 알림도 함께 멈추므로, 외부 감시 서비스로 중단을 알아차려야 한다.

1. healthchecks.io 같은 서비스에서 감시 항목을 만들고, 주기를 5분, 유예 시간을 15분 정도로 정한다.
2. 발급된 신호 주소를 `.env`의 `HEARTBEAT_URL`에 넣는다. 이 주소도 인증 정보이므로 `.env`에만 둔다.
3. 수집기는 실행 중 5분마다 이 주소로 신호를 보낸다. 신호가 끊기면 감시 서비스가 휴대전화나 이메일로 알린다.

## 5. 설정 확인과 시험 실행

```sh
.venv/bin/python -m collector check-config   # 수집원, 엔터티, 시장 데이터 설정 확인
.venv/bin/python -m collector once           # 모든 뉴스 수집원을 한 번씩 확인
.venv/bin/python -m collector status         # 수집원별 마지막 정상 확인 시각과 오류
.venv/bin/python -m collector events --days 7
.venv/bin/python -m collector market         # 업비트와 Kraken 시세를 한 번 확인
.venv/bin/python -m collector reactions      # 최근 사건의 가격 반응 계산
```

`run`으로 상시 실행하면 뉴스 수집원은 각자의 주기로, 시세는 5분마다, 가격 반응은 30분마다 갱신된다. 주기와 감시 종목은 `config/sources.yaml`과 `config/market.yaml`에서 바꾼다.

사건을 검토한 결과는 다음과 같이 기록한다. 연결 등급과 사업 단계의 뜻은 [research-principles.md](research-principles.md) 2절과 4절에 있다.

```sh
.venv/bin/python -m collector review 12 --directness QNT=direct --stage-after "선정·협약" \
    --evidence-url https://example.com/release --next-check "참여기관 명단" --note "기관 직접 발표"
```

처음 확인한 수집원의 기존 자료는 기준선으로만 저장하고 알림을 보내지 않는다. 알림은 그다음 확인부터 새로 나온 자료에 대해서만 보낸다. 데이터베이스와 로그는 `data/`에 저장되며, `data/`는 커밋되지 않는다.

## 6. 자동 실행

```sh
sh deploy/macos/install.sh            # 설치하거나 다시 설치
sh deploy/macos/install.sh uninstall  # 제거
```

설치 스크립트는 `~/Library/LaunchAgents/`에 LaunchAgent를 등록한다. 수집기는 로그인하면 시작되고, 멈추면 60초 뒤에 다시 시작된다. 수집기는 `caffeinate -s`로 실행되므로, 전원이 연결되어 있는 동안에는 시스템이 잠자기에 들어가지 않는다. 화면은 꺼져도 된다.

## 7. 상태 확인과 재시작

```sh
launchctl print gui/$(id -u)/com.crypto-institution-research.collector | grep -E "state|pid"
launchctl kickstart -k gui/$(id -u)/com.crypto-institution-research.collector
tail -f data/collector.log
```

## 8. 운영할 때 주의할 점

- 외부 모니터 없이 덮개를 닫으면 잠자기에 들어간다. 덮개를 열어 둔다.
- LaunchAgent는 로그인한 뒤에만 실행된다. FileVault가 켜져 있으면 자동 로그인을 쓸 수 없으므로, 재부팅 뒤에는 직접 로그인해야 수집이 다시 시작된다. 자세한 내용과 보안상 고려 사항은 [collector-spec.md](collector-spec.md) 8절에 있다.
- 항상 전원에 연결해 두므로 충전 한도나 최적화된 배터리 충전을 켠다 ([collector-spec.md](collector-spec.md) 8절).

## 9. 업데이트

```sh
git pull
.venv/bin/pip install -e .
launchctl kickstart -k gui/$(id -u)/com.crypto-institution-research.collector
```
