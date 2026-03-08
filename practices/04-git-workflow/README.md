# Practice 04: Git 워크플로우 (Git Workflow)

## Goal

Claude Code와 함께 안전한 Git 워크플로우를 학습합니다 -- 커밋, 브랜치, PR, 안전한 습관을 익힙니다.

## Why This Matters

AI 에이전트와 작업할 때 안전한 Git 습관은 데이터 손실을 방지합니다. Claude는 Git 작업을 자동화할 수 있지만, 올바른 워크플로우를 이해하고 있어야 합니다.

## Prerequisites

- Practice 01 (Golden Workflow) 완료

## Time

20-30분

## What You'll Learn

1. **백업 브랜치 생성** -- 변경 전 안전망 구축
2. **설명적인 커밋 메시지** -- Claude에게 커밋을 요청하는 방법
3. **피처 브랜치** -- 새 기능을 위한 브랜치 생성과 구현
4. **PR 설명 작성** -- 변경 사항을 요약하는 방법
5. **/rewind 사용** -- 변경 사항 되돌리기

## Getting Started

```bash
cd practices/04-git-workflow
npm install
npm test
```

**중요**: 이 연습을 위해 Git 저장소가 초기화되어 있어야 합니다.
아직 Git 저장소가 아니라면:

```bash
cd /path/to/ClaudeCodePractice
git init
git add .
git commit -m "Initial commit"
```

테스트가 통과하는지 확인한 후, `CHALLENGE.md`의 단계별 지시를 따라가세요.

## Key Concepts

### 백업 브랜치

변경하기 전에 항상 백업 브랜치를 만드세요:

```
변경하기 전에 backup/before-refactor 이름으로 백업 브랜치를 만들어주세요.
```

### 설명적인 커밋

Claude에게 커밋을 요청할 때:

```
지금까지의 변경 사항을 설명적인 커밋 메시지와 함께 커밋해주세요.
```

### /rewind

Claude의 변경 사항을 되돌리고 싶을 때:

```
/rewind
```

이전 체크포인트 목록이 표시되고, 원하는 시점으로 되돌릴 수 있습니다.
