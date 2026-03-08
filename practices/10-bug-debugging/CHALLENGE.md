# Challenge: 버그 디버깅

## Step 1: Bug 1 — 논리 버그 (Logic Bug)

`src/event-scheduler.ts`의 이벤트 스케줄러에는 날짜 범위 체크에서 **off-by-one 에러**가 있습니다.

```bash
npx jest event-scheduler
```

테스트를 실행하면 대부분 통과하지만, 경계값(boundary) 테스트 하나가 실패합니다.

### Claude에게 시도해볼 프롬프트

```
src/event-scheduler.test.ts를 실행하면 일부 테스트가 실패해.
실패하는 테스트를 확인하고, 코드의 실행 흐름을 한 줄씩 추적해서
근본 원인을 찾아줘.
```

---

## Step 2: Bug 2 — 비동기 버그 (Async Bug)

`src/data-fetcher.ts`의 데이터 페처에는 **경쟁 조건(Race Condition)**이 있습니다. 공유 가변 상태를 적절히 관리하지 않아 동시 호출 시 문제가 발생합니다.

```bash
npx jest data-fetcher
```

### Claude에게 시도해볼 프롬프트

```
src/data-fetcher.ts에 경쟁 조건(race condition) 버그가 있어.
동시에 여러 요청이 들어올 때 어떤 순서로 실행되는지
타임라인을 그려서 설명해줘.
```

---

## Step 3: Bug 3 — 타입 버그 (Type Bug)

`src/config-parser.ts`의 설정 파서는 **문자열 "false"를 true로 잘못 변환**합니다. JavaScript의 truthy/falsy 평가 때문에 발생하는 미묘한 버그입니다.

```bash
npx jest config-parser
```

### Claude에게 시도해볼 프롬프트

```
src/config-parser.ts에서 boolean 값 파싱이 잘못되고 있어.
JavaScript의 타입 강제 변환(type coercion)과 관련된 문제야.
"false" 문자열이 어떻게 처리되는지 단계별로 추적해줘.
```

---

## Step 4: 실행 추적 요청

각 버그에 대해 Claude에게 실행 추적(execution trace)을 요청하세요.

### Claude에게 시도해볼 프롬프트

```
다음 함수 호출의 실행 흐름을 단계별로 추적해줘:

scheduler.getEventsInRange(new Date('2024-03-01'), new Date('2024-03-31'))

각 단계에서 변수의 값이 어떻게 변하는지 보여줘.
```

---

## Step 5: 근본 원인 분석

Claude에게 **증상 수정이 아닌 근본 원인 수정**을 요청하세요.

### Claude에게 시도해볼 프롬프트

```
이 3가지 버그 각각에 대해:
1. 증상(symptom)이 무엇인지
2. 근본 원인(root cause)이 무엇인지
3. 증상만 고치는 방법과 근본 원인을 고치는 방법의 차이

를 설명해줘. 근본 원인을 해결하는 수정을 적용하고,
모든 테스트가 통과하는지 확인해줘.
```

---

## 완료 기준

- [ ] Bug 1 (off-by-one): 근본 원인을 이해하고 수정했다
- [ ] Bug 2 (race condition): 경쟁 조건의 타임라인을 이해했다
- [ ] Bug 3 (type coercion): 타입 강제 변환 문제를 이해했다
- [ ] 모든 테스트가 통과한다 (`npm test`)
- [ ] 각 버그의 "증상"과 "근본 원인"의 차이를 설명할 수 있다

## 회고 질문

1. Claude에게 "왜 실패해?"라고 물었을 때와 "실행 흐름을 추적해줘"라고 물었을 때 답변의 질이 어떻게 달랐나요?
2. 세 가지 버그 유형 중 어떤 것이 가장 찾기 어려웠나요?
3. 실제 프로젝트에서 비슷한 버그를 만났을 때 Claude를 어떻게 활용하겠습니까?
