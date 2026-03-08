# Anthropic 공식 문서 및 자료

---

## 1. 공식 문서 (code.claude.com/docs)

### Best Practices - 핵심 요약

**중심 제약**: 컨텍스트 윈도우가 차면 성능이 저하된다. 이것이 모든 Best Practice의 근간.

**7가지 핵심 원칙**

1. **검증 수단 제공** (Single highest-leverage action)
   - 테스트, 스크린샷, expected output 없이 구현 요청하지 말 것
   - 검증 없으면 그럴듯하지만 깨진 코드 생산

2. **Explore → Plan → Code**
   - Plan Mode (Shift+Tab)로 탐색과 실행 분리
   - Ctrl+G로 에디터에서 계획 편집
   - 사소한 작업에는 불필요

3. **구체적 컨텍스트 제공**
   - 범위 지정, 소스 지시, 기존 패턴 참조, 증상 설명
   - @ 참조, 이미지 붙여넣기, URL, 파이프 입력 활용

4. **환경 구성**
   - CLAUDE.md: `/init`으로 생성, 200줄 이하 유지
   - 권한: `/permissions` 또는 `/sandbox`
   - CLI 도구: gh, aws, gcloud 등 설치
   - MCP: `claude mcp add`
   - Hooks: 결정론적 스크립트
   - Skills: `.claude/skills/` SKILL.md
   - Subagents: `.claude/agents/`
   - Plugins: `/plugin`

5. **효과적 소통**
   - 시니어 엔지니어에게 물어볼 질문을 Claude에게
   - 큰 기능은 Claude가 인터뷰하게 하기
   - 최소한의 프롬프트로 시작 → Claude가 어려운 부분 파고들기

6. **세션 관리**
   - Esc로 중단, Esc+Esc 또는 /rewind로 체크포인트 복원
   - /clear로 무관한 작업 사이 초기화
   - /compact로 제어된 압축
   - 조사 작업은 서브에이전트에 위임

7. **자동화와 확장**
   - `claude -p "prompt"`로 CI/pre-commit 연동
   - 병렬 세션 (데스크톱 앱, 웹, Agent Teams)
   - Writer/Reviewer 패턴

### 흔한 실패 패턴
- Kitchen sink session: 무관한 작업 혼합 → /clear
- 반복 수정: 실패 접근 오염 → /clear 후 재시작
- 과도한 CLAUDE.md: 너무 길면 무시 → 가차없이 정리
- 검증 없는 신뢰: 깨진 코드 배포 → 항상 테스트 제공
- 무한 탐색: 범위 없는 조사 → 범위 좁히기, 서브에이전트 활용

---

## 2. CLAUDE.md 및 메모리 시스템

### CLAUDE.md 로딩 위치 (우선순위 순)
| 위치 | 범위 | 공유 |
|------|------|------|
| /Library/.../ClaudeCode/CLAUDE.md (macOS) | 관리 정책 | 조직 |
| /etc/claude-code/CLAUDE.md (Linux) | 관리 정책 | 조직 |
| ./CLAUDE.md 또는 ./.claude/CLAUDE.md | 프로젝트 | Git |
| ~/.claude/CLAUDE.md | 사용자 전체 | X |
| ./CLAUDE.local.md | 프로젝트 개인 | X |

### 기타
- `@path/to/file` import 문법
- `.claude/rules/` 디렉토리로 규칙 정리
- `paths:` YAML frontmatter로 경로별 규칙 적용
- Auto Memory: `~/.claude/projects/<project>/memory/`

---

## 3. Common Workflows

- 코드베이스 탐색, 버그 수정, 리팩토링
- 서브에이전트, Plan Mode, 테스트
- PR 생성/리뷰, 문서화
- 이미지 분석 (드래그/드롭, 붙여넣기)
- Extended Thinking (`ultrathink` 키워드)
- 세션 관리 (/rename, /resume, --continue, --from-pr)
- Git Worktree 병렬 세션
- Unix 파이프: `cat file | claude -p "prompt" > output.txt`

---

## 4. 공식 GitHub 레포지토리

| 레포 | Stars | 설명 |
|------|-------|------|
| anthropics/claude-code | 75.1k | Claude Code 본체 |
| anthropics/claude-code-action | 6.1k | GitHub Actions PR/이슈 자동화 |
| anthropics/claude-plugins-official | - | 공식 플러그인 디렉토리 |
| anthropics/skills | - | 공개 Agent Skills |

### claude-code-action 주요 기능
- @claude 멘션으로 PR/이슈에서 자동 응답
- 코드 리뷰, 구현, Q&A
- 9개 솔루션 패턴 (자동 PR 리뷰, 보안 리뷰, 이슈 트리아지 등)
- 설치: `/install-github-app`

---

## 5. 샌드박싱 및 보안

- **Sandboxed Bash**: Linux bubblewrap, macOS seatbelt
- 파일시스템 격리 + 네트워크 격리
- 권한 프롬프트 84% 감소
- `/sandbox` 명령으로 활성화
- 웹 버전은 격리된 클라우드 샌드박스에서 실행

---

## 6. Anthropic 팀의 활용 사례

- 인프라팀: 온보딩 가속 (코드베이스 읽기, 의존성 설명)
- 제품 엔지니어링: 파일 탐색의 "첫 번째 관문"
- 보안 엔지니어링: TDD 전환, 제어 흐름 추적 3배 빠름
- 제품 디자인: Figma → 코드 자율 루프
- 추론팀: 테스트 로직 언어 변환 (예: Rust)
- 데이터 인프라: K8s 문제 20분 내 진단
- 핵심: **코드 생성기가 아닌 사고 파트너로 활용**

---

## 7. Agent SDK

- 자율 에이전트 구축 프레임워크
- 핵심: "에이전트에게 컴퓨터를 주어 인간처럼 일하게 하라"
- 피드백 루프: 컨텍스트 수집 → 행동 → 검증 → 반복
- `systemPrompt: { preset: "claude_code" }` 사용
- CLAUDE.md 로딩: `settingSources: ['project']` 명시 필요
