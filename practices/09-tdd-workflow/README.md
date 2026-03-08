# Practice 09: TDD 워크플로우

## 목표

Test-Driven Development(TDD)를 Claude와 함께 실습합니다. Red-Green-Refactor 사이클과 Ralph Loop 패턴을 익혀, AI와 협업하는 TDD 워크플로우를 체득합니다.

## 사전 요구사항

- Practice 05 (CLAUDE.md) 완료
- TypeScript 및 Jest 기본 이해

## 소요 시간

45-60분

## 핵심 개념

### TDD 사이클: Red → Green → Refactor

1. **Red**: 실패하는 테스트를 먼저 작성합니다
2. **Green**: 테스트를 통과하는 최소한의 코드를 구현합니다
3. **Refactor**: 테스트를 유지하면서 코드 품질을 개선합니다

### Ralph Loop

Claude에게 성공 기준을 주고 반복하게 하는 패턴입니다:

```
"테스트를 실행하고, 실패하면 수정하고, 다시 실행해. 모든 테스트가 통과할 때까지 반복해."
```

이 패턴은 Claude가 스스로 피드백 루프를 돌며 문제를 해결하게 합니다.

## 시작하기

```bash
cd practices/09-tdd-workflow
npm install
```

`src/shopping-cart.test.ts`에 미리 작성된 테스트가 있습니다. 구현 파일(`src/shopping-cart.ts`)은 인터페이스만 정의되어 있어 테스트는 **모두 실패**합니다.

```bash
npm test  # 모든 테스트가 실패하는 것을 확인
```

이제 `CHALLENGE.md`의 단계를 따라 Claude와 함께 TDD를 실습하세요.

## 학습 포인트

- 테스트를 먼저 작성하면 요구사항이 명확해진다
- Claude에게 "테스트를 통과시켜"라고 말하면 TDD의 Green 단계를 수행한다
- Refactor 단계에서 Claude는 테스트라는 안전망 덕분에 자유롭게 리팩토링할 수 있다
- Ralph Loop는 Claude가 자율적으로 문제를 해결하게 하는 강력한 패턴이다
