# Practice 17: 7대 실수 체험

## Goal

Claude Code 사용 시 흔히 저지르는 안티패턴을 의도적으로 체험하고, 올바른 사용법을 학습합니다. 실수를 직접 경험함으로써 "왜 안 되는지"를 체감합니다.

## Prerequisites

- Practice 01 (Golden Workflow) 완료

## Time

45-60 minutes

## Difficulty

★★☆ (Intermediate)

## What You'll Learn

- Blind Trust: Claude 코드를 무비판적으로 수용하는 위험성
- Kitchen Sink Session: 한 세션에서 너무 많은 작업을 하는 문제
- Over-specified CLAUDE.md: 너무 긴 설정 파일의 문제
- No Verification: 테스트 없이 개발하는 위험성
- Scope Creep: 구조 없이 기능을 추가하는 문제

## Key Concepts

### 7대 실수 목록

| # | 안티패턴 | 증상 | 해결책 |
|---|---------|------|--------|
| 1 | Blind Trust | 보안 취약점 간과 | 항상 코드 리뷰 |
| 2 | Kitchen Sink | 세션 품질 저하 | 작업당 1세션 |
| 3 | Over-specified | 규칙 무시 | CLAUDE.md 30줄 이내 |
| 4 | No Verification | 숨겨진 버그 | TDD 워크플로우 |
| 5 | Scope Creep | 스파게티 코드 | 사전 구조 설계 |
| 6 | Copy-Paste Prompt | 맥락 손실 | 대화형 반복 |
| 7 | Ignoring Warnings | 기술 부채 | 경고 즉시 해결 |

### 이 실습의 철학

> "실수를 두려워하지 말고, 안전한 환경에서 직접 체험하라"

각 안티패턴을 의도적으로 실행하고, 그 결과를 관찰한 뒤, 올바른 방법과 비교합니다.

## Setup

```bash
uv sync
```

## Getting Started

1. `CHALLENGE.md`를 열어 단계별 실습을 진행하세요
2. `src/` 디렉토리에 의도적으로 문제가 있는 코드가 준비되어 있습니다
3. 각 단계에서 "잘못된 방법"을 먼저 체험하고, "올바른 방법"을 적용합니다
