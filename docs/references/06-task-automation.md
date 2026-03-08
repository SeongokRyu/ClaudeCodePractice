# 업무 자동화 (Task Automation with Claude Code)

---

## 핵심 개념

Claude Code의 자동화는 **`claude -p` (headless mode)**를 기반으로 한다.
모든 자동화 패턴(CI/CD, 스크립트, cron, git hooks)은 이 모드 위에 구축된다.

---

## 1. Headless Mode (`claude -p`)

비대화형 모드. 프롬프트를 받아 실행하고 stdout으로 결과 출력.

```bash
# 기본 사용
claude -p "이 프로젝트의 아키텍처를 설명해줘"

# 파이프 입력 (PR diff 리뷰)
gh pr diff 42 | claude -p "보안 취약점을 리뷰해줘"

# JSON 출력 (프로그래밍적 파싱)
claude -p "TODO 주석 목록" --output-format json | jq '.result'

# 도구 제한 (CI 안전성)
claude -p "src/ 리뷰" --allowedTools Read,Grep --max-turns 5

# 시스템 프롬프트 추가
git diff --cached | claude -p "커밋 메시지 작성" \
  --append-system-prompt "시니어 엔지니어처럼 간결하게"
```

**출력 형식**: `text` (기본), `json` (구조화), `stream-json` (스트리밍)

**CI 안전 수칙**: `--allowedTools`로 Bash 제외, API 키는 시크릿 매니저에, `--max-turns`로 무한 루프 방지

---

## 2. GitHub Actions (`claude-code-action`)

공식 GitHub Action. PR/이슈 자동화의 핵심.

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned, labeled]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          claude_args: "--max-turns 10"
```

| 트리거 | 용도 |
|--------|------|
| `@claude` 멘션 | 대화형 코드 리뷰, 질문 응답 |
| `issues: [opened]` | 자동 이슈 트리아지 |
| `pull_request_review` | PR마다 자동 리뷰 |
| `push: tags` | 릴리즈 노트 자동 생성 |
| `schedule: cron` | 정기 유지보수 (의존성 체크 등) |

**설치**: Claude Code 터미널에서 `/install-github-app` 실행

---

## 3. Hooks - 결정론적 워크플로우 제어

스킬과 달리 Hooks는 **항상 실행**되며 LLM이 건너뛸 수 없다.

### 라이프사이클 이벤트

| 이벤트 | 시점 | 용도 |
|--------|------|------|
| PreToolUse | 도구 실행 전 | 위험 작업 차단, 입력 수정 |
| PostToolUse | 도구 실행 후 | 코드 포맷, 로깅 |
| SessionStart | 세션 시작 | 환경 로드, 리마인더 |
| SessionEnd | 세션 종료 | 정리, 요약 생성 |
| Notification | 알림 발생 | 커스텀 알림 라우팅 |

### Exit Code
- `0` = 허용 (계속 진행)
- `2` = 차단 (도구 실행 중단, stderr 메시지가 Claude에게 전달)
- 기타 = 비차단 에러 (경고 표시 후 계속)

### 실전 예시

**편집 후 자동 포맷 (PostToolUse):**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "type": "command",
      "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
    }]
  }
}
```

**민감 파일 편집 차단 (PreToolUse):**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "type": "command",
      "command": "python3 -c \"import json,sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2) if any(s in path for s in ['.env','package-lock.json']) else sys.exit(0)\""
    }]
  }
}
```

**v2.0.10+**: PreToolUse 훅이 도구 입력을 실행 전에 수정 가능 (차단 + 재시도 불필요)

---

## 4. 배치 처리 및 Fan-Out 패턴

### `/batch` 명령 (내장)
Git Worktree 격리로 안전한 병렬 실행. 완료 후 각각 PR 생성.
```
/batch "모든 React 클래스 컴포넌트를 함수형으로 마이그레이션"
```

### 수동 Fan-Out (bash 스크립팅)
```bash
#!/bin/bash
# 여러 디렉토리 병렬 리뷰
for dir in src/auth src/api src/frontend; do
  claude -p "$dir의 보안 이슈를 리뷰. JSON 출력." \
    --output-format json > "review_${dir//\//_}.json" &
done
wait
jq -s '.' review_*.json > full_review.json
```

### 자동 커밋 메시지 생성
```bash
ai_commit() {
  msg=$(git diff --cached | claude -p \
    "이 diff의 커밋 메시지를 한 줄로 작성. 메시지만 출력.")
  git commit -m "$msg"
}
```

---

## 5. 스케줄링 / Cron 자동화

| 방식 | 설명 |
|------|------|
| `/loop` | 세션 내 반복 실행 (`/loop 5m /check-status`) |
| Desktop 예약 작업 | 재시작해도 유지, GUI 설정 |
| GitHub Actions `schedule` | 인프라 수준 자동화 |
| cron + `claude -p` | 시스템 cron에서 headless 호출 |

```yaml
# 매일 새벽 2시 코드 건강 검사
on:
  schedule:
    - cron: '0 2 * * *'
```

---

## 6. Git Hooks와 Claude Code 연동

### pre-commit에서 Claude로 보안 검사
```bash
#!/bin/bash
# .git/hooks/pre-commit
DIFF=$(git diff --cached)
RESULT=$(echo "$DIFF" | claude -p \
  "시크릿이나 보안 이슈가 있으면 BLOCK, 없으면 PASS 출력" \
  --max-turns 1)
if echo "$RESULT" | grep -q "^BLOCK"; then
  echo "Pre-commit 실패: $RESULT"
  exit 1
fi
```

---

## 7. 실제 사례

| 조직 | 용도 | 결과 |
|------|------|------|
| Anthropic 마케팅 | CSV 광고 데이터 분석, 변형 생성 | 시간→분 단위, 배치당 0.5초 |
| Anthropic 보안 | 스택 트레이스 분석, 제어 흐름 추적 | 인시던트 해결 3배 빠름 |
| Anthropic 법률 | "폰 트리" 시스템 구축 | 개발자 없이 프로토타입 |
| 일반 파일럿 | 자동 코드 리뷰 | PR 처리 30% 빠름, 테스트 커버리지 72% |
