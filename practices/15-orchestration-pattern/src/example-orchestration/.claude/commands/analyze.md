# /analyze Command

Analyze code quality for the specified path using the Code Analyzer pipeline.

## Usage

```
/analyze <target-path>
```

## Arguments

- `$ARGUMENTS`: 분석할 디렉토리 또는 파일 경로
  - 기본값: `src/`
  - 예시: `/analyze src/utils/`, `/analyze lib/`

## Execution Flow

```
/analyze src/
    ↓
[1] 인자 파싱: target = $ARGUMENTS (기본값: src/)
    ↓
[2] analyzer-agent 호출
    → Agent가 code-analyzer Skill을 로드
    → 대상 파일 탐색
    → 파일별 분석 수행
    ↓
[3] 결과 포맷팅 및 출력
    → 파일별 점수 테이블
    → 전체 프로젝트 요약
    → 개선 제안
```

## Agent Delegation

이 Command는 분석 작업을 **analyzer-agent**에게 위임합니다.

- Agent 위치: `.claude/agents/analyzer-agent.md`
- Agent가 사용하는 Skill: `.claude/skills/code-analyzer/SKILL.md`

대상 경로를 Agent에게 전달하고, Agent의 분석 결과를 사용자에게 보기 좋게 출력합니다.

## Expected Output

1. **파일별 품질 점수 테이블** — 각 파일의 복잡도, 유지보수성, 모범사례 점수
2. **전체 프로젝트 평균 점수** — 프로젝트 전체의 코드 품질 등급
3. **개선 우선순위 Top 3** — 가장 개선이 필요한 파일
4. **구체적 개선 제안** — 각 파일에 대한 실행 가능한 제안

## Example Output

```
## Code Quality Analysis Report

### Summary
- 분석 대상: src/
- 분석 파일 수: 5개
- 프로젝트 평균: 78/100 (C)

### File Details
| 파일 | 복잡도 | 유지보수성 | 모범사례 | 총점 | 등급 |
|------|--------|-----------|---------|------|------|
| app.ts | 25/30 | 20/30 | 30/40 | 75/100 | C |
| utils.ts | 30/30 | 28/30 | 35/40 | 93/100 | A |
| ...  | ...    | ...       | ...     | ...  | ... |

### Top 3 Improvement Targets
1. router.ts (62/100) — 함수 길이 초과, 중첩 깊이 5단계
2. db.ts (68/100) — any 타입 4회 사용, 에러 처리 미흡
3. app.ts (75/100) — 테스트 없음, JSDoc 누락

### Recommendations
- router.ts: handleRequest 함수를 3개의 작은 함수로 분리
- db.ts: any 타입을 구체적인 인터페이스로 교체
- app.ts: 단위 테스트 추가, 주요 함수에 JSDoc 작성
```
