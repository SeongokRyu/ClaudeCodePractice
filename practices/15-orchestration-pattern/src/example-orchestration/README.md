# Example Orchestration: Code Analyzer

이 디렉토리는 Command→Agent→Skill 3계층 오케스트레이션 패턴의 완성된 예제입니다.

## Architecture

```
사용자 입력
    │
    ▼
┌──────────────────────────────────────────────┐
│  /analyze src/                                │
│  .claude/commands/analyze.md                  │
│                                               │
│  역할:                                        │
│  - $ARGUMENTS로 대상 경로를 받음               │
│  - analyzer-agent에게 작업 위임               │
│  - 결과를 포맷팅하여 사용자에게 출력            │
└──────────────┬───────────────────────────────┘
               │ 위임
               ▼
┌──────────────────────────────────────────────┐
│  analyzer-agent                               │
│  .claude/agents/analyzer-agent.md             │
│                                               │
│  역할:                                        │
│  - code-analyzer Skill을 로드                 │
│  - 대상 파일 탐색 및 수집                      │
│  - Skill 기준에 따라 파일별 분석               │
│  - 분석 보고서 생성                            │
└──────────────┬───────────────────────────────┘
               │ 참조
               ▼
┌──────────────────────────────────────────────┐
│  code-analyzer Skill                          │
│  .claude/skills/code-analyzer/SKILL.md        │
│                                               │
│  역할:                                        │
│  - 복잡도 분석 기준 (30점)                     │
│  - 유지보수성 분석 기준 (30점)                  │
│  - 모범 사례 분석 기준 (40점)                   │
│  - 등급 산정 기준 (A~F)                        │
│  - 출력 형식 템플릿                            │
└──────────────────────────────────────────────┘
```

## File Structure

```
.claude/
├── commands/
│   └── analyze.md          ← Layer 1: 사용자 진입점
├── agents/
│   └── analyzer-agent.md   ← Layer 2: 실행 로직
└── skills/
    └── code-analyzer/
        └── SKILL.md        ← Layer 3: 도메인 지식
```

## How It Works

### 1. Command Layer (진입점)

`analyze.md`는 사용자가 `/analyze src/`를 입력하면 실행됩니다.
- `$ARGUMENTS`를 통해 대상 경로를 받습니다
- 실제 분석 작업은 Agent에게 위임합니다
- Agent의 결과를 사용자에게 보기 좋게 출력합니다

### 2. Agent Layer (실행자)

`analyzer-agent.md`는 실제 분석 작업을 수행합니다.
- Skill을 preload하여 분석 기준을 참조합니다
- 파일 탐색 → 개별 분석 → 보고서 생성의 3단계로 진행합니다
- 구조화된 보고서를 생성합니다

### 3. Skill Layer (지식 제공)

`SKILL.md`는 코드 품질 분석에 필요한 도메인 지식을 정의합니다.
- 복잡도, 유지보수성, 모범 사례의 3가지 카테고리
- 각 카테고리의 구체적인 점수 산정 기준
- 등급 기준과 출력 형식 템플릿

## Extending This Pattern

이 패턴을 활용하여 새로운 파이프라인을 만들 수 있습니다:

| Command | Agent | Skill | 용도 |
|---------|-------|-------|------|
| /analyze | analyzer-agent | code-analyzer | 코드 품질 분석 |
| /review | review-agent | code-reviewer | 코드 리뷰 |
| /docs | docs-agent | docs-generator | 문서 자동 생성 |
| /security | security-agent | security-checker | 보안 점검 |

핵심: Skill은 여러 Agent가 공유할 수 있고, Agent는 여러 Command에서 재사용 가능합니다.
