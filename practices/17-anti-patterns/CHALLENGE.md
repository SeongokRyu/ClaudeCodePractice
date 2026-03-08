# Challenge: 7대 실수 체험

## Step 1: Blind Trust — 맹목적 신뢰

### 잘못된 방법

Claude에게 다음을 요청하세요:

```
src/anti-pattern-1-blind-trust.ts의 deepMerge 함수를 확인해주세요.
잘 동작하나요?
```

Claude는 아마 "잘 동작합니다" 또는 일부 개선점만 언급할 것입니다.

### 숨겨진 문제 발견

이제 다음을 요청하세요:

```
src/anti-pattern-1-blind-trust.ts의 deepMerge 함수에
보안 취약점이 있는지 집중적으로 분석해주세요.
특히 Prototype Pollution 공격이 가능한지 확인해주세요.
```

### 직접 확인

`src/anti-pattern-tests.test.ts`의 "Blind Trust" 테스트를 실행하세요:

```bash
npm test -- --testNamePattern="Blind Trust"
```

### 교훈

- Claude가 "문제 없다"고 해도 보안 관점에서 별도 검증 필수
- **구체적인 관점을 제시하면** Claude의 분석 품질이 올라감
- "확인해줘" vs "Prototype Pollution이 가능한지 확인해줘"는 결과가 다름

---

## Step 2: Kitchen Sink Session — 주방 싱크대 세션

### 잘못된 방법

하나의 Claude 세션에서 다음 5가지를 연속으로 요청하세요:

```
1. "간단한 TODO 앱의 데이터 모델을 설계해줘"
2. "React와 Vue의 상태 관리 차이를 설명해줘"
3. "Docker compose 파일을 작성해줘"
4. "이전에 만든 TODO 앱에 사용자 인증을 추가해줘"
5. "Python으로 웹 스크레이퍼를 만들어줘"
```

### 관찰

4번 요청에서 Claude가 1번에서 만든 TODO 앱의 세부사항을 정확히 기억하는지 확인하세요. 아마 맥락이 흐려져 있을 것입니다.

### 올바른 방법

```bash
# 각 작업별로 독립된 세션 사용
claude  # Session 1: TODO 앱 전용
claude  # Session 2: Docker 설정 전용

# 또는 같은 세션에서 작업을 전환할 때
> /clear
> 이제 새로운 작업을 시작합니다. Docker compose 파일을 작성해주세요.
```

### 교훈

- 하나의 세션 = 하나의 관련된 작업
- 작업 전환 시 `/clear`로 컨텍스트 초기화
- 연관 없는 5개 작업 → 5개 세션

---

## Step 3: Over-specified CLAUDE.md

### 잘못된 방법 — 200줄 CLAUDE.md

다음과 같은 긴 CLAUDE.md를 사용해보세요:

```markdown
# Rules (이런 파일을 만들지는 마세요 — 생각만 하세요)

1. Always use camelCase
2. Always add JSDoc to every function
3. Never use var
4. Always use const over let
5. Maximum line length is 80 characters
6. Use 2 spaces for indentation
7. Always use semicolons
8. No trailing commas
9. Use single quotes
10. Always use strict equality
... (190줄 더)
```

Claude에게 코드를 작성하게 하면, 많은 규칙이 무시됩니다.
200개의 규칙을 컨텍스트에 넣으면 Claude의 주의가 분산됩니다.

### 올바른 방법 — 30줄 CLAUDE.md

```markdown
# Project Rules

## Code Style
- TypeScript strict mode
- Prefer const, avoid any
- Functions under 20 lines

## Testing
- Jest for testing
- Test file: *.test.ts

## Git
- Conventional commits
- PR required for main
```

### 실험

두 가지 CLAUDE.md로 같은 작업을 요청하고, 규칙 준수율을 비교해보세요.

### 교훈

- CLAUDE.md는 30줄 이내가 최적
- 핵심 규칙만 포함 (나머지는 ESLint/Prettier에 위임)
- "규칙이 많다 ≠ 더 좋은 코드"

---

## Step 4: No Verification — 검증 없는 개발

### 잘못된 방법

```
통화 금액을 포맷팅하는 함수를 만들어줘.
- 1234567.89 → "$1,234,567.89"
- 소수점 2자리까지 표시
- 음수는 괄호로 표시: -1234 → "($1,234.00)"
```

Claude가 만든 코드를 그대로 사용합니다.

### 숨겨진 문제

`src/anti-pattern-2-no-verification.ts`를 확인하세요.
이 코드는 컴파일되고 대부분의 경우 잘 동작하지만...

```bash
npm test -- --testNamePattern="No Verification"
```

부동소수점 문제가 숨어 있습니다!

### 올바른 방법

```
통화 금액을 포맷팅하는 함수를 만들어줘.
테스트를 먼저 작성하고, 그 다음에 구현해줘.

엣지 케이스:
- 0.1 + 0.2 = 0.3 이 올바르게 표시되는지
- 아주 큰 수 (Number.MAX_SAFE_INTEGER)
- 아주 작은 수 (0.001)
- NaN, Infinity
```

### 교훈

- 테스트 없이 "동작하는 것처럼 보이는" 코드는 위험
- 엣지 케이스를 명시하면 Claude가 더 견고한 코드를 작성
- TDD 워크플로우가 이 문제를 사전에 방지

---

## Step 5: Scope Creep — 범위 폭주

### 잘못된 방법

하나의 세션에서 점진적으로 기능을 추가합니다:

```
1. "간단한 TODO 앱을 만들어줘" (좋은 시작)
2. "사용자 인증도 추가해줘" (아직 괜찮음)
3. "실시간 동기화도 넣어줘" (복잡해짐)
4. "팀 기능도 추가해줘" (구조가 무너짐)
5. "알림 시스템도 넣어줘" (스파게티 코드)
6. "캘린더 뷰도 추가해줘" (카오스)
```

### 관찰

6번째 요청 후 코드의 상태를 확인하세요:
- 파일 구조가 정리되어 있는가?
- 관심사가 분리되어 있는가?
- 테스트가 있는가?
- 새 기능을 추가하기 쉬운 구조인가?

### 올바른 방법

```
TODO 앱을 만들 건데, 다음 기능이 필요합니다:
1. 기본 CRUD
2. 사용자 인증
3. 실시간 동기화
4. 팀 기능

먼저 전체 아키텍처를 설계해주세요.
모듈별 책임과 인터페이스를 정의하고,
구현 순서를 제안해주세요.
```

그 다음 각 모듈을 개별 세션에서 구현합니다.

### 교훈

- 사전에 전체 구조를 설계하면 기능 추가가 깔끔
- "하나씩 추가"보다 "전체 계획 → 단계적 구현"
- 각 기능은 독립된 세션에서 구현

---

## Step 6: 올바른 접근법 정리

각 안티패턴에 대해 배운 것을 정리하세요.

Claude에게 다음을 요청합니다:

```
오늘 체험한 5가지 안티패턴을 정리해주세요.

각 패턴에 대해:
1. 잘못된 방법의 증상
2. 왜 문제인지
3. 올바른 방법
4. 기억할 한 줄 요약

마크다운 테이블로 정리해주세요.
```

### 최종 체크리스트

- [ ] Blind Trust: Claude 코드를 항상 보안 관점에서 리뷰한다
- [ ] Kitchen Sink: 하나의 세션에 하나의 작업만 수행한다
- [ ] Over-specified: CLAUDE.md는 30줄 이내로 유지한다
- [ ] No Verification: 항상 테스트를 먼저 작성한다
- [ ] Scope Creep: 전체 구조를 먼저 설계한다

---

## 성공 기준

- [ ] 각 안티패턴의 문제를 직접 체험했다
- [ ] 숨겨진 보안 취약점(Prototype Pollution)을 발견했다
- [ ] 부동소수점 버그를 발견했다
- [ ] 잘못된 방법과 올바른 방법의 차이를 체감했다
- [ ] 5가지 교훈을 정리했다

## 핵심 교훈

1. **신뢰하되 검증하라**: Claude는 도구이지 오라클이 아니다
2. **집중하라**: 하나의 세션, 하나의 작업
3. **간결하게 유지하라**: 규칙이 적을수록 잘 지켜진다
4. **테스트하라**: "동작하는 것 같은" 코드를 믿지 마라
5. **계획하라**: 구조 없이 기능을 쌓지 마라
