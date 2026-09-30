# 맥북 설치와 운영 안내

이 문서는 수집 프로그램을 맥북에 설치하고 상시 실행하는 방법을 설명한다. 설계 배경은 [collector-spec.md](collector-spec.md) 8절에 있다. 맥북 모델과 macOS 버전은 아직 정해지지 않았으므로([open-questions.md](open-questions.md) Q2), 명령은 Apple Silicon과 Intel 맥북에 공통으로 쓸 수 있는 것만 적었다.

## 1. 준비

- Python 3.11 이상이 필요하다. `python3 --version`으로 확인하고, 버전이 낮으면 [python.org](https://www.python.org/downloads/macos/)의 설치 파일이나 Homebrew로 설치한다.
- git이 필요하다. 처음 `git`을 실행하면 macOS가 개발자 도구 설치를 안내한다.

## 2. 설치

```sh
git clone https://github.com/tlzkrh1029/crypto_institution_research.git
cd crypto_institution_research
python3 -m venv .venv
.venv/bin/pip install -e .
cp .env.example .env
```

`.env`를 열어 값을 채운다. `.env`는 공개 저장소에 올라가지 않도록 `.gitignore`로 제외되어 있다.

- `SEC_USER_AGENT`: SEC 공정 접근 정책이 요구하는 이름과 연락처다. 비워 두면 SEC 수집원은 건너뛴다.
- `HEARTBEAT_URL`: 외부 감시 서비스의 신호 주소다 (6절). 이 주소도 인증 정보이므로 `.env`에만 둔다.

## 3. 설정 확인과 시험 실행

```sh
.venv/bin/python -m collector check-config   # 수집원과 엔터티 설정 확인
.venv/bin/python -m collector once           # 모든 수집원을 한 번씩 확인
.venv/bin/python -m collector status         # 수집원별 마지막 정상 확인 시각과 오류
.venv/bin/python -m collector events --days 7
.venv/bin/python -m collector market         # 업비트 시세를 한 번 확인
.venv/bin/python -m collector reactions      # 최근 사건의 가격 반응 계산
```

`run`으로 상시 실행하면 뉴스 수집원은 각자의 주기로, 업비트 시세는 5분마다, 가격 반응은 30분마다 갱신된다. 주기와 감시 종목은 `config/sources.yaml`과 `config/market.yaml`에서 바꾼다.

사건을 검토한 결과는 다음과 같이 기록한다. 연결 등급과 사업 단계의 뜻은 [research-principles.md](research-principles.md) 2절과 4절에 있다.

```sh
.venv/bin/python -m collector review 12 --directness QNT=direct --stage-after "선정·협약" \
    --evidence-url https://example.com/release --next-check "참여기관 명단" --note "기관 직접 발표"
```

처음 확인한 수집원의 기존 자료는 기준선으로만 저장하고 알림을 보내지 않는다. 알림은 그다음 확인부터 새로 나온 자료에 대해서만 보낸다. 데이터베이스와 로그는 `data/`에 저장되며, `data/`는 커밋되지 않는다.

## 4. 자동 실행

```sh
sh deploy/macos/install.sh            # 설치하거나 다시 설치
sh deploy/macos/install.sh uninstall  # 제거
```

설치 스크립트는 `~/Library/LaunchAgents/`에 LaunchAgent를 등록한다. 수집기는 로그인하면 시작되고, 멈추면 60초 뒤에 다시 시작된다. 수집기는 `caffeinate -s`로 실행되므로, 전원이 연결되어 있는 동안에는 시스템이 잠자기에 들어가지 않는다. 화면은 꺼져도 된다.

상태 확인과 재시작은 다음 명령으로 한다.

```sh
launchctl print gui/$(id -u)/com.crypto-institution-research.collector | grep -E "state|pid"
launchctl kickstart -k gui/$(id -u)/com.crypto-institution-research.collector
tail -f data/collector.log
```

## 5. 운영할 때 주의할 점

- 외부 모니터 없이 덮개를 닫으면 잠자기에 들어간다. 덮개를 열어 둔다.
- LaunchAgent는 로그인한 뒤에만 실행된다. FileVault가 켜져 있으면 자동 로그인을 쓸 수 없으므로, 재부팅 뒤에는 직접 로그인해야 수집이 다시 시작된다. 자세한 내용과 보안상 고려 사항은 [collector-spec.md](collector-spec.md) 8절에 있다.
- 항상 전원에 연결해 두므로 충전 한도나 최적화된 배터리 충전을 켠다 ([collector-spec.md](collector-spec.md) 8절).

## 6. 수집 중단 감시

수집기가 멈추면 알림도 함께 멈추므로, 외부 감시 서비스로 중단을 알아차려야 한다.

1. healthchecks.io 같은 서비스에서 감시 항목을 만들고, 주기를 5분, 유예 시간을 15분 정도로 정한다.
2. 발급된 신호 주소를 `.env`의 `HEARTBEAT_URL`에 넣는다.
3. 수집기는 실행 중 5분마다 이 주소로 신호를 보낸다. 신호가 끊기면 감시 서비스가 휴대전화나 이메일로 알린다.

## 7. 업데이트

```sh
git pull
.venv/bin/pip install -e .
launchctl kickstart -k gui/$(id -u)/com.crypto-institution-research.collector
```

## 8. 알림 채널

알림 채널은 아직 정해지지 않았다 ([open-questions.md](open-questions.md) Q3). 그때까지 알림은 `data/collector.log`에 기록되고, 데이터베이스의 `alerts` 테이블에도 남는다.
