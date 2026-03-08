# Challenge: Worktree 병렬 개발

## Step 1: Git Worktree 개념 이해

Git worktree는 하나의 저장소에서 여러 작업 디렉토리를 동시에 유지할 수 있게 해줍니다.

### 일반 브랜치 전환 vs Worktree

```
일반 브랜치 전환:
  git checkout feature-auth   → 작업 → git stash
  git checkout feature-log    → 작업 → git stash
  git checkout feature-auth   → git stash pop → 작업 계속
  ❌ 컨텍스트 스위칭 비용이 큼

Worktree:
  Terminal 1: ~/project/           (main)
  Terminal 2: ~/project-auth/      (feature-auth)
  Terminal 3: ~/project-log/       (feature-logging)
  ✅ 각 터미널에서 독립적으로 작업
```

### 기본 명령어

```bash
# worktree 생성
git worktree add ../my-project-feature-auth -b feature-auth

# worktree 목록 확인
git worktree list

# worktree 제거
git worktree remove ../my-project-feature-auth
```

### Exercise

다음 명령어를 실행하여 worktree의 동작을 확인하세요:

```bash
git worktree list
```

---

## Step 2: Worktree 세션 시작 — 인증 기능

첫 번째 터미널에서 worktree 기반 Claude 세션을 시작합니다.

```bash
claude --worktree feature-auth
```

이 명령은 다음을 자동으로 수행합니다:
1. `feature-auth` 브랜치 생성
2. 새로운 worktree 디렉토리 생성
3. 해당 디렉토리에서 Claude 세션 시작

### 인증 기능 구현 요청

Claude에게 다음을 요청하세요:

```
src/app.py에 인증 기능을 추가해주세요:
1. POST /auth/login 엔드포인트 — username, password를 받아 JWT 토큰 반환
2. POST /auth/register 엔드포인트 — 새 사용자 등록
3. auth_middleware — 토큰 검증 미들웨어
4. 기존 GET /users 엔드포인트에 인증 미들웨어 적용
5. 테스트도 함께 추가해주세요
```

### 확인 사항
- [ ] feature-auth 브랜치에서 작업 중인지 확인
- [ ] 인증 관련 코드가 추가되었는지 확인
- [ ] 테스트가 통과하는지 확인

---

## Step 3: 두 번째 Worktree 세션 — 로깅 기능

**다른 터미널**을 열고 두 번째 worktree 세션을 시작합니다.

```bash
claude --worktree feature-logging
```

### 로깅 기능 구현 요청

Claude에게 다음을 요청하세요:

```
src/app.py에 요청 로깅 기능을 추가해주세요:
1. requestLogger 미들웨어 — 모든 요청의 method, path, 응답시간을 로그
2. GET /logs 엔드포인트 — 최근 로그 조회
3. 로그 레벨 지원 (info, warn, error)
4. 에러 발생 시 자동으로 error 로그 기록
5. 테스트도 함께 추가해주세요
```

### 확인 사항
- [ ] feature-logging 브랜치에서 작업 중인지 확인 (feature-auth와 독립!)
- [ ] 로깅 관련 코드가 추가되었는지 확인
- [ ] 테스트가 통과하는지 확인
- [ ] feature-auth의 변경사항이 이 브랜치에 없는지 확인

---

## Step 4: 병렬 작업 수행

두 터미널에서 동시에 작업이 진행되는 것을 체험합니다.

### Terminal 1 (feature-auth)에서

```
인증 기능에 비밀번호 해싱을 추가해주세요.
bcrypt를 사용하여 비밀번호를 안전하게 저장하도록 수정해주세요.
```

### Terminal 2 (feature-logging)에서

```
로깅에 구조화된 JSON 포맷을 추가해주세요.
각 로그 엔트리가 timestamp, level, message, metadata를 포함하도록 해주세요.
```

### 병렬 작업의 장점 확인

```bash
# Terminal 1에서
git log --oneline feature-auth

# Terminal 2에서
git log --oneline feature-logging

# 두 브랜치의 커밋 히스토리가 완전히 독립적!
```

---

## Step 5: PR을 통한 머지

각 worktree에서 작업한 내용을 PR로 머지합니다.

### 5-1. 각 브랜치에서 PR 생성

```bash
# Terminal 1 (feature-auth)
git push -u origin feature-auth
gh pr create --title "feat: Add authentication system" --body "JWT 기반 인증 시스템 추가"

# Terminal 2 (feature-logging)
git push -u origin feature-logging
gh pr create --title "feat: Add request logging" --body "구조화된 요청 로깅 시스템 추가"
```

### 5-2. PR 리뷰 및 머지

```bash
# 각 PR을 리뷰하고 머지
gh pr merge --squash
```

### 5-3. Worktree 정리

```bash
# 작업 완료 후 worktree 제거
git worktree list
git worktree remove ../project-feature-auth
git worktree remove ../project-feature-logging
git worktree prune
```

---

## 성공 기준

- [ ] 두 개의 worktree에서 독립적으로 기능을 개발했다
- [ ] 각 worktree의 변경사항이 서로 격리되어 있었다
- [ ] 두 기능 모두 테스트가 통과했다
- [ ] PR을 통해 main 브랜치에 머지할 수 있었다
- [ ] 사용 완료 후 worktree를 정리했다

## 핵심 교훈

1. **worktree = 물리적 격리**: 각 기능이 완전히 독립된 디렉토리에서 개발됨
2. **컨텍스트 스위칭 제로**: stash/checkout 없이 터미널만 전환하면 됨
3. **Claude 세션 격리**: 각 worktree의 Claude가 해당 기능에만 집중
4. **PR 기반 통합**: 각 기능을 독립적으로 리뷰하고 머지 가능
