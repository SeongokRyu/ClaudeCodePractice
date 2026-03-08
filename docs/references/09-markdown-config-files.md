# Claude Code Markdown 설정 파일 완전 가이드

---

## 전체 .claude/ 디렉토리 구조

```
project-root/
├── CLAUDE.md                        # 팀 프로젝트 규칙 (git 공유)
├── CLAUDE.local.md                  # 개인 프로젝트 설정 (gitignore)
├── .mcp.json                        # MCP 서버 설정
├── .claude/
│   ├── CLAUDE.md                    # 대체 팀 규칙 위치
│   ├── settings.json                # 팀 공유 설정
│   ├── settings.local.json          # 개인 설정 (gitignore)
│   ├── agents/                      # 서브에이전트 정의
│   │   └── *.md
│   ├── skills/                      # 스킬 정의
│   │   └── <skill-name>/
│   │       └── SKILL.md
│   ├── commands/                    # 슬래시 명령어 (레거시, skills로 통합됨)
│   │   └── *.md
│   ├── rules/                       # 경로별 규칙 파일
│   │   └── *.md
│   ├── agent-memory/                # 서브에이전트 프로젝트 메모리
│   │   └── <agent-name>/MEMORY.md
│   └── agent-memory-local/          # 서브에이전트 로컬 메모리 (gitignore)

~/.claude/
├── CLAUDE.md                        # 사용자 전역 규칙
├── settings.json                    # 사용자 전역 설정
├── agents/*.md                      # 사용자 서브에이전트
├── skills/<name>/SKILL.md           # 사용자 스킬
├── commands/*.md                    # 사용자 명령어
├── rules/*.md                       # 사용자 규칙
├── agent-memory/<agent>/MEMORY.md   # 사용자 에이전트 메모리
└── projects/<project>/memory/       # 프로젝트별 Auto Memory
    ├── MEMORY.md
    └── <topic>.md
```

---

## 1. CLAUDE.md — 프로젝트 헌법

### 모든 변형과 위치 (우선순위 순)

| 우선순위 | 위치 | 공유 | 용도 |
|---------|------|------|------|
| 1 (최고) | 관리 정책: `/etc/claude-code/CLAUDE.md` (Linux) | 조직 | 조직 전체 규칙 (무시 불가) |
| 2 | CLI 인자 | 세션 | 세션별 오버라이드 |
| 3 | `./CLAUDE.local.md` | X | 개인 프로젝트 설정 |
| 4 | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | Git | 팀 프로젝트 규칙 |
| 5 (최저) | `~/.claude/CLAUDE.md` | X | 사용자 전역 규칙 |

### 핵심 동작
- 상위 디렉토리의 CLAUDE.md는 시작 시 전부 로드 (상향 로딩)
- 하위 디렉토리의 CLAUDE.md는 해당 파일 접근 시 로드 (하향/lazy)
- `@path/to/import` 문법으로 외부 파일 포함 (최대 5단계)
- **200줄 이하** 유지 권장
- `claudeMdExcludes`로 모노레포에서 불필요한 CLAUDE.md 건너뛰기

---

## 2. .claude/agents/*.md — 서브에이전트 정의

### Frontmatter 필드

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | O | 고유 식별자 (소문자+하이픈) |
| `description` | O | 언제 이 에이전트를 사용할지 |
| `tools` | X | 허용 도구 목록 (생략 시 전체 상속) |
| `disallowedTools` | X | 거부할 도구 |
| `model` | X | sonnet, opus, haiku, inherit |
| `permissionMode` | X | default, acceptEdits, plan 등 |
| `maxTurns` | X | 최대 턴 수 |
| `skills` | X | 사전 로드할 스킬 |
| `memory` | X | 지속 메모리: user, project, local |
| `background` | X | 백그라운드 실행 여부 |
| `isolation` | X | worktree 격리 |
| `hooks` | X | 이 에이전트 전용 훅 |
| `mcpServers` | X | 사용 가능한 MCP 서버 |

### 예시
```markdown
---
name: code-reviewer
description: 코드 변경 후 품질/보안 검토. 변경 시 자동 실행.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: user
---
시니어 코드 리뷰어로서 변경사항을 검토하세요.
```

---

## 3. .claude/skills/*/SKILL.md — 스킬 정의

### 디렉토리 구조
```
my-skill/
├── SKILL.md           # 메인 지침 (필수)
├── template.md        # Claude가 채울 템플릿
├── reference.md       # 상세 참조 문서
├── examples/          # 예시
└── scripts/           # 스크립트
```

### Frontmatter 필드

| 필드 | 설명 |
|------|------|
| `name` | 표시 이름 (최대 64자) |
| `description` | 자동 호출 판단에 사용 |
| `argument-hint` | 자동완성 힌트 (`[issue-number]`) |
| `disable-model-invocation` | true = 사용자만 호출 가능 |
| `user-invocable` | false = `/` 메뉴에서 숨김 |
| `allowed-tools` | 스킬 활성 시 허용 도구 |
| `model` | 스킬 활성 시 사용 모델 |
| `context` | `fork` = 서브에이전트 컨텍스트에서 실행 |
| `agent` | `context: fork` 시 사용할 에이전트 타입 |

### 동적 컨텍스트 (셸 명령 실행)
```markdown
---
name: pr-summary
context: fork
agent: Explore
---
- PR diff: !`gh pr diff`
- 변경 파일: !`gh pr diff --name-only`
```

### 문자열 치환
- `$ARGUMENTS` — 전체 인자
- `$ARGUMENTS[N]` 또는 `$N` — N번째 인자
- `${CLAUDE_SKILL_DIR}` — SKILL.md 디렉토리 경로

---

## 4. .claude/commands/*.md — 슬래시 명령어 (레거시)

Skills로 통합됨. 기존 파일은 계속 작동하지만 새로 만들 때는 Skills 권장.
같은 이름의 Skill과 Command가 있으면 Skill이 우선.

---

## 5. .claude/rules/*.md — 경로별 규칙

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "tests/**/*.test.ts"
---
# API 개발 규칙
- 모든 엔드포인트에 입력 검증 필수
- 표준 에러 응답 형식 사용
```

- `paths` 없으면 무조건 로드
- `paths` 있으면 해당 파일 작업 시에만 로드
- 심링크로 여러 프로젝트에서 규칙 공유 가능

---

## 6. MEMORY.md — Auto Memory

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # 첫 200줄만 시작 시 로드
├── debugging.md       # 주제별 파일 (온디맨드 로드)
└── api-conventions.md
```

- Git worktree끼리 같은 디렉토리 공유
- `autoMemoryEnabled` 설정 또는 `/memory` 토글

---

## 7. .mcp.json — MCP 서버 설정

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "remote-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "headers": { "Authorization": "Bearer ${API_KEY}" }
    }
  }
}
```

환경 변수 확장 지원: `${VAR}`, `${VAR:-default}`

---

## 8. settings.json — 프로젝트 설정

```json
{
  "permissions": {
    "allow": ["Bash(npm run lint)"],
    "deny": ["Read(./.env)"]
  },
  "env": { "ENABLE_TOOL_SEARCH": "true" },
  "hooks": { ... },
  "autoMemoryEnabled": true,
  "claudeMdExcludes": ["**/irrelevant/CLAUDE.md"]
}
```

---

## 9. 커뮤니티 컨벤션 파일 (비공식)

| 파일 | 용도 |
|------|------|
| HANDOFF.md | 세션 인수인계 (시도한 것, 성공/실패, 남은 작업) |
| SPEC.md | 기능 스펙 (인터뷰 기법으로 작성) |
| MIGRATION.md | 마이그레이션 진행 상태 추적 |

---

## 갖춰두면 좋은 구성 (권장 세트)

### 최소 구성 (모든 프로젝트)
```
CLAUDE.md                    # 프로젝트 규칙
.claude/settings.json        # 권한/훅 설정
```

### 표준 구성 (팀 프로젝트)
```
CLAUDE.md
CLAUDE.local.md
.claude/settings.json
.claude/rules/               # 경로별 규칙
.mcp.json                    # MCP 서버
```

### 고급 구성 (프로덕션급)
```
CLAUDE.md
CLAUDE.local.md
.claude/settings.json
.claude/settings.local.json
.claude/rules/               # 경로별 규칙
.claude/agents/              # 커스텀 에이전트
.claude/skills/              # 재사용 워크플로우
.mcp.json                    # MCP 서버
```

### 엔터프라이즈 구성 (풀 세트)
```
위 전부 +
관리 정책 CLAUDE.md           # 조직 전체 규칙 강제
관리 정책 managed-settings.json  # 조직 설정 강제
관리 정책 managed-mcp.json    # 조직 MCP 강제
Plugin 디렉토리               # 팀별 확장
```
