# Practice 03: 컨텍스트 관리 (Context Management)

## Goal

Claude Code의 컨텍스트 윈도우를 효과적으로 관리하는 방법을 학습합니다 -- `/clear`, `/compact`, 세션 관리, `HANDOFF.md` 작성법을 익힙니다.

## Why This Matters

> "Context window is the most important resource to manage when working with AI coding assistants."
> -- Anthropic

컨텍스트 윈도우가 가득 차면 Claude의 성능이 저하됩니다. 효율적인 컨텍스트 관리는 생산성의 핵심입니다.

## Prerequisites

- Practice 01 (Golden Workflow) 완료

## Time

20-30분

## What You'll Learn

1. **컨텍스트 채우기 관찰** -- `/cost` 명령으로 사용량 확인
2. **`/clear` 사용** -- 관련 없는 작업 간 컨텍스트 초기화
3. **`/compact` 사용** -- 힌트 파라미터를 활용한 컨텍스트 압축
4. **HANDOFF.md 작성** -- 세션 간 작업 인수인계 문서 작성
5. **`--resume`과 `--continue` 플래그** -- 이전 세션 이어가기

## Getting Started

```bash
cd practices/03-context-management
npm install
npm test
```

테스트가 통과하는지 확인한 후, `CHALLENGE.md`의 단계별 지시를 따라가세요.

## Key Concepts

### /clear

관련 없는 새로운 작업을 시작할 때 컨텍스트를 초기화합니다:

```
/clear
```

### /compact

현재 대화를 요약하여 컨텍스트를 압축합니다. 힌트를 제공하면 중요한 정보를 보존할 수 있습니다:

```
/compact user-service의 CRUD 구현에 집중하여 요약해주세요
```

### HANDOFF.md

세션 간 작업 인수인계를 위한 문서입니다:

```markdown
# Handoff

## Current State
- 어디까지 진행했는지

## What's Done
- 완료된 작업 목록

## What's Left
- 남은 작업 목록

## Key Decisions
- 중요한 결정사항들

## How to Verify
- 현재 상태를 검증하는 방법
```

### --resume & --continue

```bash
# 마지막 세션을 선택하여 이어가기
claude --resume

# 마지막 세션을 자동으로 이어가기
claude --continue
```
