# Practice 02: 프롬프팅 기법 (Prompting Techniques)

## Goal

효과적인 프롬프팅 기법을 학습합니다 -- 검증 기준 제공, 인터뷰 기법, 구조화된 프롬프트 작성법을 익힙니다.

## Why This Matters

> "Providing verification means is the single highest-leverage action you can take to improve Claude's output quality."
> -- Anthropic 공식 문서

Claude에게 단순히 "이거 고쳐줘"라고 말하는 것과, 명확한 기준과 검증 방법을 제공하는 것은 결과물의 품질에 큰 차이를 만듭니다.

## Prerequisites

- Practice 01 (Golden Workflow) 완료

## Time

20-30분

## What You'll Learn

1. **나쁜 프롬프트 vs 좋은 프롬프트** -- 모호한 요청과 구체적인 요청의 차이
2. **검증 기준 제공** -- Claude에게 기능 구현과 함께 테스트 검증을 요청하는 방법
3. **인터뷰 기법** -- Claude가 먼저 질문하도록 유도하는 방법
4. **구조화된 프롬프트** -- 역할 + 컨텍스트 + 제약조건 + 예상 출력 + 검증

## Getting Started

```bash
cd practices/02-prompting-techniques
npm install
npm test
```

테스트가 통과하는지 확인한 후, `CHALLENGE.md`의 단계별 지시를 따라가세요.

## Key Concepts

### 검증 기준 (Verification Criteria)

Claude에게 작업을 요청할 때 "어떻게 검증할 것인가"를 함께 알려주세요:

```
구현 후 npm test를 실행하여 모든 테스트가 통과하는지 확인해주세요.
```

### 인터뷰 기법 (Interview Technique)

Claude에게 먼저 질문하도록 요청하세요:

```
이 기능을 구현하기 전에, 요구사항에 대해 궁금한 점이 있으면 먼저 질문해주세요.
```

### 구조화된 프롬프트 (Structured Prompt)

```
역할: TypeScript 시니어 개발자
컨텍스트: 계산기 모듈의 에러 처리 개선
제약조건: 기존 테스트를 깨뜨리지 않을 것
예상 출력: 수정된 코드 + 새로운 테스트
검증: npm test로 모든 테스트 통과
```
