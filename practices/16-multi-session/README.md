# Practice 16: 멀티세션 워크플로우

## Goal

8가지 멀티세션 패턴을 학습합니다. 두 개 이상의 Claude 세션을 동시에 활용하여 Writer/Reviewer, Competing Prototypes, TDD Ping-Pong, Specialist Team 등의 병렬 작업 패턴을 익힙니다.

## Prerequisites

- Practice 13 (Subagents) 완료

## Time

45-60 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

- Writer/Reviewer 패턴: 작성과 리뷰를 분리
- Competing Prototypes 패턴: 같은 문제를 다른 방식으로 해결
- TDD Ping-Pong 패턴: 테스트 작성과 구현을 분리
- Specialist Team 패턴: 전문 분야별 세션 운영

## Key Concepts

### 멀티세션이 필요한 이유

단일 세션의 한계:
- 컨텍스트 윈도우 소진
- 한 가지 관점에 고착
- 역할 혼합으로 인한 품질 저하

멀티세션의 장점:
- 역할 분리로 높은 품질
- 다양한 관점에서의 검증
- 병렬 작업으로 시간 절약

### 4가지 핵심 패턴

```
1. Writer/Reviewer     2. Competing Prototypes
   Session A: 작성        Session A: 방식 1
   Session B: 리뷰        Session B: 방식 2
                          → 비교 후 최선 선택

3. TDD Ping-Pong       4. Specialist Team
   Session A: 테스트       Session A: Frontend
   Session B: 구현         Session B: Backend
   → 반복                  Session C: Tests
                           → 병렬 작업
```

## Getting Started

1. `CHALLENGE.md`를 열어 단계별 실습을 진행하세요
2. `src/problem.md`에 정의된 문제를 여러 세션에서 해결합니다
3. `src/rate-limiter-interface.ts`의 인터페이스를 구현합니다
