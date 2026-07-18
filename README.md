# Jusigi Plugin

[English](README.en.md)

Jusigi는 Codex가 **사용자 소유 GitHub 저장소**에 한국 주식 리서치·Telegram 알림·모의투자·리스크 게이트·GitHub Actions 워크플로를 생성하거나 점검하도록 안내하는 무료 오픈소스 Skill 플러그인입니다.

중앙 서버가 계좌를 보관하거나 대신 주문하는 서비스가 아닙니다. 비밀값은 대화나 코드로 받지 않으며, 생성된 자동화는 사용자의 저장소·GitHub Actions·증권사 계정 안에서만 운영됩니다.

## 설치

현재 공개 GitHub 마켓플레이스를 Codex CLI에 추가하고 플러그인을 설치합니다.

```bash
codex plugin marketplace add jinsu0000/jusigi-plugin
codex plugin add jusigi@jusigi-plugins
```

Codex CLI 또는 IDE에서 `$jusigi`를 명시적으로 호출하세요.

```text
$jusigi로 내 GitHub 저장소에 한국 주식 리서치와 모의투자 자동화를 구성해 줘.
```

공식 호출 문법은 `/jusigi`가 아니라 `$jusigi`입니다. `/skills` 또는 `$` 입력으로 설치된 Skill을 찾을 수도 있습니다.

## 생성하는 것

- 사용자 정책을 담은 `config/investment-policy.yaml`
- 미래 Codex 작업에 안전 규칙을 적용하는 `AGENTS.md`
- 데이터·모델 제안·리스크 게이트·브로커를 분리한 Python 구조
- Telegram 알림 연결 지점
- 평일 09:05/12:05/16:05 KST 보고 스케줄 예시
- 장중 매시간 모의 판단 스케줄 예시
- 최소 권한 CI와 네트워크 없는 리스크 테스트
- 운영 중지·롤백·대사 절차 문서

## 안전 기본값

- paper/dry-run만 활성화
- 실거래와 공매도 비활성화
- 사용자 승인 종목 allowlist가 비어 있으면 주문 거부
- 모델 출력은 주문이 아니라 제안이며 결정론적 `RiskGate`를 우회할 수 없음
- KIS·LS·신한 등은 최신 공식 문서를 확인한 모의환경 어댑터만 생성하며 실주문 엔드포인트는 공개 Skill 범위에서 제외
- 앱키, 시크릿키, 계좌번호, Telegram 토큰은 GitHub Secrets에 사용자가 직접 설정

## 현재 v0.1 범위

이 버전은 안전한 저장소 계약, 생성 스크립트, 모의 브로커, 리스크 게이트, 테스트와 예약 워크플로의 기반을 제공합니다. 사용자가 `$jusigi`를 실행하면 Codex가 선택한 증권사·데이터원·투자 정책에 맞춰 대상 저장소를 확장합니다.

플러그인 자체에는 실주문 API를 넣거나 생성하지 않습니다. 공식 공개판은 리서치와 모의투자 자동화에 한정합니다.

## 로컬 개발

```bash
python plugins/jusigi/skills/jusigi/scripts/scaffold.py \
  --target /tmp/jusigi-demo \
  --broker dry-run \
  --core-ratio 50

python plugins/jusigi/skills/jusigi/scripts/validate_target.py /tmp/jusigi-demo
PYTHONPATH=/tmp/jusigi-demo/src \
  python -m unittest discover -s /tmp/jusigi-demo/tests -v
```

## 공개 배포 로드맵

GitHub 공개 마켓플레이스 설치는 지금 지원합니다. 다음 단계는 실제 사용자 피드백과 안전성 검증 후 OpenAI의 공개 Plugins Directory에 **skills-only plugin**으로 제출하는 것입니다. 제출 준비 자료는 [배포 가이드](docs/DISTRIBUTION.md)와 [심사 테스트](submission/test-cases.md)에 정리했습니다.

## 기여와 지원

- 버그와 기능 제안: [GitHub Issues](https://github.com/jinsu0000/jusigi-plugin/issues)
- 보안 문제: [SECURITY.md](SECURITY.md)
- 기여 방법: [CONTRIBUTING.md](CONTRIBUTING.md)
- 지원 범위: [SUPPORT.md](SUPPORT.md)

## 면책

Jusigi는 자동화 소프트웨어이며 투자 자문, 투자 권유, 적합성 판단 또는 수익 보장이 아닙니다. 생성된 코드와 정책, 데이터 라이선스, 증권사 약관, 세금, 계좌 자격과 주문 결과는 사용자가 독립적으로 검토해야 합니다.

MIT License
