# Multi-Agent Systems (멀티 에이전트 시스템)

---

## 핵심 개념

Claude Code는 3단계의 멀티 에이전트 메커니즘을 제공한다:

```
복잡도 ↑
  │  Agent Teams    (독립 세션, 직접 소통, 공유 태스크 리스트)
  │  Subagents      (하위 에이전트, 결과만 부모에게 반환)
  │  Skills/Commands (재사용 프롬프트, 인라인 실행)
복잡도 ↓                                          토큰 비용 →
```

---

## 1. Claude Agent SDK

Python/TypeScript 오픈소스 프레임워크. Claude Code와 동일한 인프라를 프로그래밍 가능한 라이브러리로 제공.

### 기본 사용법

**Python:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="auth.py의 버그를 찾아 수정해줘",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)

asyncio.run(main())
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "auth.py의 버그를 찾아 수정해줘",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);
}
```

### 에이전트 루프
`컨텍스트 수집 → 행동 → 검증 → 반복`

---

## 2. Subagents vs Agent Teams

| 차원 | Subagents | Agent Teams |
|------|-----------|-------------|
| 컨텍스트 | 자체 윈도우, 결과만 부모에게 반환 | 자체 윈도우, 완전 독립 |
| 소통 | 부모에게만 보고 | 팀원끼리 직접 메시지 |
| 조율 | 메인 에이전트가 관리 | 공유 태스크 리스트로 자율 조율 |
| 적합한 경우 | 결과만 필요한 집중 작업 | 토론/논쟁이 필요한 복잡 작업 |
| 토큰 비용 | 낮음 (결과 요약) | 높음 (각 팀원 = 별도 인스턴스) |

---

## 3. 서브에이전트 정의

### 파일 기반 (`.claude/agents/`)
```markdown
---
name: code-reviewer
description: 코드 변경 후 품질/보안 검토
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: plan
---
시니어 코드 리뷰어로서 변경사항을 검토하세요:
1. 보안 취약점
2. 성능 문제
3. 유지보수성
```

### 주요 설정 필드
| 필드 | 설명 |
|------|------|
| `model` | sonnet, opus, haiku, inherit |
| `tools` | 허용 도구 목록 |
| `isolation` | `worktree`로 Git worktree 격리 |
| `permissionMode` | default, acceptEdits, plan 등 |
| `maxTurns` | 최대 턴 수 |
| `skills` | 사전 로드할 스킬 |
| `memory` | 지속적 메모리 (user/project/local) |
| `background` | 백그라운드 실행 여부 |

### 빌트인 서브에이전트
- **Explore**: Haiku 모델, 읽기 전용, 코드베이스 검색 최적화
- **Plan**: 상속 모델, 읽기 전용, 계획 수립용 컨텍스트 수집
- **General-purpose**: 상속 모델, 전체 도구, 복잡한 멀티스텝 작업

---

## 4. Agent Teams (실험적 기능)

활성화: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

```
┌─────────────────────────────────┐
│          TEAM LEAD              │
│   (메인 세션, 작업 분배/조율)    │
└──────┬────┬────┬────┬──────────┘
       │    │    │    │
       v    v    v    v
     팀원1 팀원2 팀원3 팀원4
       │    │    │    │
       └────┴────┴────┘
            │         │
     공유 태스크 리스트  메일박스
     (의존성 추적)    (직접 메시징)
```

### 시작 방법
```text
Create an agent team:
- 팀원 1: UX 관점에서 분석
- 팀원 2: 기술 아키텍처 분석
- 팀원 3: 악마의 변호인 역할
```

### 팀 전용 Hooks
- `TeammateIdle`: 팀원이 유휴 상태일 때 (exit 2로 계속 작업시키기)
- `TaskCompleted`: 태스크 완료 시 (exit 2로 완료 거부)

---

## 5. 6가지 핵심 멀티에이전트 패턴

### 패턴 1: Writer/Reviewer
```
Writer → 코드 작성 → Reviewer → 리뷰/피드백 → Writer → 수정 → ...
```
구현 에이전트 + 읽기 전용 리뷰 에이전트. 인간 리뷰 대기 시간 제거.

### 패턴 2: Specialist Team (전문가 팀)
```
Team Lead → 보안 리뷰어 + 성능 리뷰어 + 테스트 커버리지 리뷰어 (병렬)
```
각 리뷰어가 다른 관점으로 동시 검토. Lead가 결과 종합.

### 패턴 3: Competing Hypotheses (경쟁 가설)
```
Team Lead → 가설1 + 가설2 + 가설3 + 가설4 + 가설5 (병렬)
           → 서로 반박하며 토론 → 합의 도출
```
앵커링 편향 극복. 적대적 토론으로 근본 원인 빠르게 수렴.

### 패턴 4: Cross-Layer (교차 레이어)
```
프론트엔드 에이전트 | 백엔드 에이전트 | 테스트 에이전트
각자 파일 영역 소유, API 계약으로 소통
```

### 패턴 5: Verification Subagent (검증 전담)
```
메인 에이전트 → 산출물 → 검증 에이전트 → pass/fail + 피드백 → 메인
```
가장 보편적으로 유용한 패턴. "전화 게임" 문제 회피.

### 패턴 6: Scatter-Gather (분산 수집)
```
Lead → 연구원1~5 (병렬 WebSearch) → 결과 수집 → 종합 보고서
```
Opus Lead + Sonnet 서브에이전트 조합이 단일 Opus 대비 90.2% 향상.

---

## 6. Command → Agent → Skill 패턴

3계층 관심사 분리:

```
Layer 1: Commands (.claude/commands/)
  사용자 진입점, 파라미터 수집, 에이전트에 위임, 비즈니스 로직 ZERO

Layer 2: Agents (.claude/agents/)
  자율 실행 컨텍스트, 데이터 처리, 스킬 사전 로드, 상태 유지

Layer 3: Skills (.claude/skills/)
  재사용 가능한 지식 단위, 도메인 전문성, 점진적 노출
```

**설계 원칙**:
- Commands는 조율만, 데이터 처리 X
- Agents는 다른 Agent를 생성하지 않음 (Commands만 조율)
- Skills는 원자적 — 하나의 일만 잘함

---

## 7. Worktree 병렬 실행

```
main repo (branch: main)
  ├── worktree-1/ (branch: agent-1-auth)     ← 에이전트 1
  ├── worktree-2/ (branch: agent-2-api)      ← 에이전트 2
  └── worktree-3/ (branch: agent-3-frontend)  ← 에이전트 3
```

같은 파일도 서로 다른 접근법으로 동시 편집 가능. 충돌 없음.

```markdown
---
name: refactor-agent
isolation: worktree
tools: Read, Write, Edit, Bash, Glob, Grep
---
```

---

## 8. 프로덕션 멀티에이전트 시스템 구축

### 프로젝트 구조
```
.claude/
  agents/
    researcher.md     # 탐색/조사
    implementer.md    # 구현
    reviewer.md       # 리뷰
    tester.md         # 테스트
  skills/
    coding-conventions/SKILL.md
    error-handling/SKILL.md
  commands/
    build-feature.md  # 오케스트레이션 진입점
  agent-memory/
    reviewer/MEMORY.md  # 패턴 축적
CLAUDE.md
```

### SDK로 CI/CD 파이프라인 구축
```python
async def build_feature(description: str):
    async for msg in query(
        prompt=f"Build feature: {description}",
        options=ClaudeAgentOptions(
            setting_sources=["project"],  # .claude/ 설정 로드
            agents={
                "researcher": AgentDefinition(
                    tools=["Read", "Glob", "Grep"],
                    model="haiku",
                ),
                "implementer": AgentDefinition(
                    tools=["Read", "Write", "Edit", "Bash"],
                    model="sonnet",
                ),
                "reviewer": AgentDefinition(
                    tools=["Read", "Glob", "Grep"],
                    model="inherit",
                ),
            },
        ),
    ):
        if hasattr(msg, "result"):
            print(msg.result)
```

---

## 9. 의사결정 프레임워크

```
단순/단일 도메인 작업? → 단일 에이전트
  ↓ NO
에이전트 간 소통 필요? → NO → Subagents
  ↓ YES
토론/논쟁 필요? → NO → Subagents (순차 체이닝)
  ↓ YES
Agent Teams (공유 태스크, 메일박스)
```

### 핵심 원칙
1. **단일 에이전트에서 시작**, 필요할 때만 복잡도 추가
2. **검증 서브에이전트**가 가장 보편적으로 유용
3. **파일 소유권**으로 충돌 방지 (또는 worktree 격리)
4. **컨텍스트 경계로 분해**, 문제 유형이 아닌 독립 정보 경로로
5. **80% 계획, 20% 실행** — 좋은 스펙이 좋은 에이전트 출력을 만듦
