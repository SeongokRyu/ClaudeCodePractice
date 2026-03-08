# Practice 14: Worktree 병렬 개발

## Goal

Git worktree를 활용한 병렬 개발 워크플로우를 익힙니다. `claude --worktree` 옵션으로 독립된 브랜치에서 동시에 여러 기능을 개발하는 방법을 학습합니다.

## Prerequisites

- Practice 13 (Subagents) 완료

## Time

45-60 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

- Git worktree의 개념과 동작 원리
- `claude --worktree` 옵션으로 독립 브랜치에서 병렬 작업
- 여러 터미널에서 동시에 서로 다른 기능 개발
- Worktree 기반 브랜치를 PR로 머지하는 워크플로우

## Key Concepts

### Git Worktree란?

하나의 Git 저장소에서 여러 개의 작업 디렉토리(working tree)를 동시에 체크아웃할 수 있는 기능입니다.

```
my-project/              (main branch)
├── .git/
├── src/
└── ...

my-project-feature-auth/  (feature-auth branch - worktree)
├── src/
└── ...

my-project-feature-log/   (feature-logging branch - worktree)
├── src/
└── ...
```

### claude --worktree 워크플로우

```
Terminal 1: claude --worktree feature-auth
  → 새 worktree + 새 브랜치 자동 생성
  → 인증 기능 개발에 집중

Terminal 2: claude --worktree feature-logging
  → 또 다른 worktree + 브랜치 생성
  → 로깅 기능 개발에 집중

결과: 두 기능이 독립적으로 동시에 개발됨
```

## Setup

```bash
uv sync
```

## Getting Started

1. `CHALLENGE.md`를 열어 단계별 실습을 진행하세요
2. `src/app.py`를 기반으로 두 가지 기능을 병렬로 추가합니다
3. 각 worktree에서 작업한 내용을 PR로 머지합니다
