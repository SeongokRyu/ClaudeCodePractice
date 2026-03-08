# Practice 15: Command→Agent→Skill 패턴

## Goal

Claude Code의 3계층 오케스트레이션 패턴을 설계하고 구현합니다. Command가 진입점을 제공하고, Agent가 실행을 담당하며, Skill이 전문 지식을 제공하는 구조를 학습합니다.

## Prerequisites

- Practice 08 (Skills) 완료
- Practice 13 (Subagents) 완료

## Time

45-60 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

- Command, Agent, Skill의 역할과 책임
- 3계층 오케스트레이션 패턴의 설계 원칙
- Skill을 Agent에 연결하고, Agent를 Command에서 호출하는 방법
- 재사용 가능한 자동화 파이프라인 구축

## Key Concepts

### 3계층 아키텍처

```
┌─────────────────────────────────────────────┐
│  Layer 1: Commands (진입점)                   │
│  .claude/commands/analyze.md                 │
│  → 사용자가 /analyze src/ 로 실행             │
│  → Agent를 호출하고 결과를 정리                │
├─────────────────────────────────────────────┤
│  Layer 2: Agents (실행자)                     │
│  .claude/agents/analyzer-agent.md            │
│  → 실제 분석 작업을 수행                       │
│  → Skill에서 분석 기준을 로드                  │
│  → 파일을 읽고, 분석하고, 보고서 생성           │
├─────────────────────────────────────────────┤
│  Layer 3: Skills (지식 제공)                   │
│  .claude/skills/code-analyzer/SKILL.md       │
│  → 코드 품질 분석 기준 정의                    │
│  → 어떤 패턴을 찾아야 하는지 가이드             │
│  → 점수 산정 기준 제공                         │
└─────────────────────────────────────────────┘
```

### 각 계층의 책임

| 계층 | 역할 | 비유 |
|------|------|------|
| Command | 진입점, 인자 파싱, 결과 포맷팅 | 리셉셔니스트 |
| Agent | 작업 실행, 로직 수행, 도구 사용 | 엔지니어 |
| Skill | 도메인 지식, 규칙, 기준 제공 | 매뉴얼/교과서 |

## Getting Started

1. `CHALLENGE.md`를 열어 단계별 실습을 진행하세요
2. `src/example-orchestration/`에 완성된 예제가 있습니다
3. 예제를 참고하여 자신만의 오케스트레이션 파이프라인을 만들어보세요
