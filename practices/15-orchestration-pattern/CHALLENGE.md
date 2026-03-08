# Challenge: Command→Agent→Skill 오케스트레이션

## Step 1: 3계층 패턴 이해

### 왜 3계층인가?

단일 프롬프트로 복잡한 작업을 처리하면 다음 문제가 생깁니다:
- 프롬프트가 너무 길어져서 Claude가 일부를 무시
- 재사용이 불가능 (매번 처음부터 설명)
- 테스트와 디버깅이 어려움

3계층으로 분리하면:
- **Skill**: 재사용 가능한 지식 모듈 (여러 Agent가 공유)
- **Agent**: 재사용 가능한 실행 모듈 (여러 Command가 공유)
- **Command**: 사용자 친화적 진입점

### 데이터 흐름

```
사용자 → /analyze src/
         ↓
  Command (analyze.md)
    - 인자 파싱: target = "src/"
    - Agent 호출
         ↓
  Agent (analyzer-agent.md)
    - Skill 로드: code-analyzer
    - 파일 탐색: src/**/*.ts
    - 각 파일 분석
    - 보고서 생성
         ↓
  Skill (SKILL.md)
    - 분석 기준 제공
    - 점수 산정 규칙
    - 패턴 매칭 규칙
         ↓
  결과 → 사용자에게 보고서 출력
```

### Exercise

`src/example-orchestration/` 디렉토리의 예제를 살펴보세요:

```bash
ls -la src/example-orchestration/.claude/
```

각 파일의 역할을 파악하고, 데이터가 어떻게 흘러가는지 추적해보세요.

---

## Step 2: Skill 생성 — 코드 분석 지식

Skill은 Claude가 특정 작업을 수행할 때 참고하는 지식 베이스입니다.

### 프로젝트 루트에 Skill 생성

```bash
mkdir -p .claude/skills/code-analyzer
```

`.claude/skills/code-analyzer/SKILL.md` 파일을 생성하세요:

```markdown
# Code Analyzer Skill

## Purpose
TypeScript/JavaScript 코드의 품질을 분석하고 점수를 산정합니다.

## Analysis Criteria

### 1. Complexity (복잡도) — 30점
- 함수당 줄 수: 20줄 이하 = 10점, 50줄 이하 = 5점, 50줄 초과 = 0점
- 중첩 깊이: 3단계 이하 = 10점, 5단계 이하 = 5점
- 매개변수 수: 3개 이하 = 10점, 5개 이하 = 5점

### 2. Maintainability (유지보수성) — 30점
- 타입 안전성: any 사용 없음 = 10점
- 에러 처리: try-catch 적절히 사용 = 10점
- 네이밍: 의미있는 변수/함수명 = 10점

### 3. Best Practices (모범 사례) — 40점
- 단일 책임 원칙 준수 = 10점
- DRY 원칙 (중복 코드 없음) = 10점
- 테스트 존재 여부 = 10점
- 문서화 (JSDoc 등) = 10점

## Output Format

각 파일에 대해 다음 형식으로 보고:

| 파일 | 복잡도 | 유지보수성 | 모범사례 | 총점 | 등급 |
|------|--------|-----------|---------|------|------|
| file.ts | X/30 | X/30 | X/40 | X/100 | A~F |

등급 기준: A(90+), B(80+), C(70+), D(60+), F(60 미만)
```

### 확인 사항
- [ ] SKILL.md가 구체적인 분석 기준을 정의하고 있는가
- [ ] 점수 산정 규칙이 명확한가
- [ ] 출력 형식이 정의되어 있는가

---

## Step 3: Agent 생성 — 분석 실행자

Agent는 Skill의 지식을 활용하여 실제 작업을 수행합니다.

### Agent 파일 생성

```bash
mkdir -p .claude/agents
```

`.claude/agents/analyzer-agent.md` 파일을 생성하세요:

```markdown
# Code Analyzer Agent

## Role
코드 품질 분석을 수행하는 에이전트입니다.

## Preloaded Skills
- code-analyzer: .claude/skills/code-analyzer/SKILL.md

## Instructions

1. 대상 디렉토리의 모든 .ts, .tsx, .js, .jsx 파일을 찾으세요
2. 각 파일에 대해 code-analyzer Skill의 기준에 따라 분석하세요
3. 파일별 점수를 산정하세요
4. 전체 요약 보고서를 생성하세요

## Execution Steps

### Step 1: 파일 탐색
대상 경로에서 분석할 파일 목록을 수집합니다.
테스트 파일 (*.test.ts, *.spec.ts)은 분석 대상에서 제외합니다.

### Step 2: 개별 분석
각 파일을 읽고 Skill의 기준에 따라 점수를 산정합니다.

### Step 3: 보고서 생성
- 파일별 상세 점수표
- 전체 평균 점수
- 가장 개선이 필요한 파일 Top 3
- 구체적인 개선 제안

## Output
분석 결과를 마크다운 테이블 형식으로 출력합니다.
```

### 확인 사항
- [ ] Agent가 Skill을 참조하고 있는가
- [ ] 실행 단계가 명확하게 정의되어 있는가
- [ ] 입력(대상 경로)과 출력(보고서) 형식이 정의되어 있는가

---

## Step 4: Command 생성 — 사용자 진입점

Command는 사용자가 `/analyze` 슬래시 명령으로 실행하는 진입점입니다.

### Command 파일 생성

```bash
mkdir -p .claude/commands
```

`.claude/commands/analyze.md` 파일을 생성하세요:

```markdown
# /analyze Command

Analyze code quality for the specified path.

## Usage
/analyze <target-path>

## Arguments
- $ARGUMENTS: 분석할 디렉토리 또는 파일 경로 (기본값: src/)

## Execution

1. 대상 경로를 확인합니다: $ARGUMENTS (미지정 시 src/)
2. analyzer-agent를 호출하여 코드 분석을 수행합니다
3. 분석 결과를 보기 좋게 포맷팅하여 출력합니다

## Agent Delegation
이 분석 작업은 analyzer-agent에게 위임합니다.
analyzer-agent는 code-analyzer Skill의 기준에 따라 분석합니다.

## Expected Output
- 파일별 품질 점수 테이블
- 전체 프로젝트 평균 점수
- 개선 우선순위 Top 3
- 구체적 개선 제안
```

### 확인 사항
- [ ] $ARGUMENTS를 사용하여 인자를 받고 있는가
- [ ] Agent에게 작업을 위임하고 있는가
- [ ] 사용자에게 보여줄 출력 형식이 정의되어 있는가

---

## Step 5: 전체 파이프라인 테스트

### 5-1. Command 실행

```bash
claude
> /analyze src/
```

### 5-2. 결과 확인

Claude가 다음 과정을 거치는지 확인하세요:

1. Command가 `$ARGUMENTS`로 `src/`를 받음
2. Agent가 `src/` 디렉토리의 파일을 탐색
3. Skill의 기준에 따라 각 파일을 분석
4. 점수와 보고서를 사용자에게 출력

### 5-3. 다른 경로로 테스트

```bash
> /analyze lib/
> /analyze src/utils/
```

### 5-4. 자신만의 파이프라인 만들기

배운 패턴을 활용하여 새로운 오케스트레이션을 만들어보세요:

**예시 아이디어:**
- `/review` — 코드 리뷰 자동화 (review-skill + review-agent + review command)
- `/docs` — 문서 자동 생성 (docs-skill + docs-agent + docs command)
- `/refactor` — 리팩토링 제안 (refactor-skill + refactor-agent + refactor command)

---

## 성공 기준

- [ ] Skill이 구체적인 분석 기준을 정의한다
- [ ] Agent가 Skill을 참조하여 작업을 수행한다
- [ ] Command가 사용자 입력을 받아 Agent에게 위임한다
- [ ] `/analyze src/` 실행 시 분석 보고서가 출력된다
- [ ] 3계층이 각각 독립적으로 재사용 가능하다

## 핵심 교훈

1. **관심사 분리**: 각 계층이 하나의 책임만 가짐
2. **재사용성**: Skill은 여러 Agent가, Agent는 여러 Command가 공유 가능
3. **테스트 용이성**: 각 계층을 독립적으로 테스트 가능
4. **확장성**: 새 Command를 추가할 때 기존 Agent와 Skill을 재사용
5. **유지보수성**: 분석 기준 변경 시 Skill만 수정하면 됨
