# Getting Started

15분 안에 Claude Code 설치부터 첫 대화까지 완료합니다.

---

## 1. 환경 확인 (3분)

```bash
node --version    # v18 이상 필요
git --version     # 아무 버전이나 OK
```

Node.js가 없다면:
- macOS: `brew install node`
- Windows: [nodejs.org](https://nodejs.org)에서 LTS 다운로드
- Linux: `curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs`

에디터: **VS Code** 권장 (Claude Code 확장 지원)

---

## 2. Claude Code 설치 (5분)

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# 설치 확인
claude --version
```

---

## 3. 인증 (3분)

```bash
claude
```

처음 실행하면 로그인 안내가 나옵니다. 다음 중 하나가 필요합니다:
- **Claude Pro/Max 구독** (가장 간편)
- **Anthropic API 키** (pay-as-you-go)

---

## 4. 첫 대화 (5분)

```bash
mkdir practice-test && cd practice-test
claude
```

Claude Code가 시작되면 다음을 입력해보세요:

```
이 디렉토리에 hello.ts 파일을 만들어줘.
"Hello from Claude Code!"를 출력하는 간단한 프로그램으로.
```

Claude가 파일을 만들면 다음을 해보세요:

```
방금 만든 파일을 실행해줘
```

동작 확인 후 `/clear`를 입력해서 대화를 초기화합니다.

---

## 5. 이 Practice 레포 시작 (2분)

```bash
cd ..
git clone <repo-url> ClaudeCodePractice
cd ClaudeCodePractice
```

이제 [Practice 01: 황금 워크플로우](../practices/01-golden-workflow/)부터 시작하세요.

---

## 알아두면 좋은 것

| 단축키 | 동작 |
|--------|------|
| Shift+Tab | 모드 순환 (Normal → Auto-accept → Plan) |
| Esc | 현재 작업 중단 |
| Esc+Esc | 이전 상태로 되돌리기 |

| 명령어 | 동작 |
|--------|------|
| `/clear` | 대화 초기화 |
| `/compact` | 대화 압축 (컨텍스트 확보) |
| `/cost` | 현재 세션 비용 확인 |
| `/help` | 도움말 |
