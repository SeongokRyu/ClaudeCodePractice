# Challenge: 멀티세션 워크플로우

## Step 1: Writer/Reviewer 패턴

하나의 세션이 코드를 작성하고, 다른 세션이 리뷰합니다.

### 준비

터미널 2개를 엽니다.

### Terminal 1 — Writer Session

```bash
claude
```

Writer에게 요청:

```
src/rate_limiter_interface.py의 RateLimiter 인터페이스를 구현하는
SlidingWindowRateLimiter 클래스를 작성해주세요.

요구사항:
- 슬라이딩 윈도우 알고리즘 사용
- src/sliding_window_limiter.py에 구현
- 모든 테스트가 통과해야 합니다
```

### Terminal 2 — Reviewer Session

Writer가 코드를 작성한 후, Reviewer에게 요청:

```bash
claude
```

```
src/sliding_window_limiter.py를 리뷰해주세요.

다음 관점에서 평가해주세요:
1. 정확성: 슬라이딩 윈도우 알고리즘이 올바르게 구현되었는가?
2. 엣지 케이스: 동시 요청, 윈도우 경계, 0 limit 등
3. 성능: 메모리 누수 가능성, O(n) 복잡도 확인
4. 타입 안전성: Python type hints가 적절한가?

구체적인 개선 제안을 코드와 함께 제시해주세요.
```

### 확인 사항
- [ ] Writer의 코드가 모든 테스트를 통과하는가
- [ ] Reviewer가 Writer가 놓친 문제를 발견했는가
- [ ] Reviewer의 피드백을 반영하여 코드가 개선되었는가

---

## Step 2: Competing Prototypes 패턴

같은 문제를 두 가지 다른 방식으로 해결하고 비교합니다.

### 문제 정의

`src/problem.md`를 읽어보세요. Rate Limiter를 두 가지 방식으로 구현합니다:
- **방식 1**: Sliding Window
- **방식 2**: Token Bucket

### Terminal 1 — Sliding Window

```bash
claude
```

```
src/problem.md의 요구사항을 읽고, Sliding Window 방식으로
RateLimiter를 구현해주세요.

- 파일: src/sliding_window_limiter.py
- src/rate_limiter_interface.py의 인터페이스를 구현
- src/test_rate_limiter.py의 테스트를 통과해야 함
- 구현 선택의 이유를 주석으로 설명
```

### Terminal 2 — Token Bucket

```bash
claude
```

```
src/problem.md의 요구사항을 읽고, Token Bucket 방식으로
RateLimiter를 구현해주세요.

- 파일: src/token_bucket_limiter.py
- src/rate_limiter_interface.py의 인터페이스를 구현
- src/test_rate_limiter.py의 테스트를 통과해야 함
- 구현 선택의 이유를 주석으로 설명
```

### 비교 분석

두 구현이 완성되면, 새 세션에서 비교합니다:

```
src/sliding_window_limiter.py와 src/token_bucket_limiter.py를
다음 기준으로 비교 분석해주세요:

1. 정확성: 두 구현 모두 테스트를 통과하는가?
2. 메모리 효율: 어느 것이 메모리를 더 적게 사용하는가?
3. 시간 복잡도: 각 연산의 Big-O는?
4. Burst 트래픽: 순간적인 대량 요청에 어떻게 반응하는가?
5. 적합한 사용 사례: 각 방식이 더 적합한 상황은?

표로 정리해주세요.
```

### 확인 사항
- [ ] 두 구현 모두 같은 테스트를 통과하는가
- [ ] 각 구현의 장단점이 명확하게 드러나는가
- [ ] 어떤 상황에서 어떤 구현이 더 적합한지 이해했는가

---

## Step 3: TDD Ping-Pong 패턴

세션 A가 실패하는 테스트를 작성하면, 세션 B가 구현합니다.

### Round 1

**Terminal 1 (Test Writer)**:

```
src/rate_limiter_interface.py의 RateLimiter 인터페이스에 대한
실패하는 테스트를 3개 작성해주세요.

- 파일: src/test_tdd_limiter.py
- 기본 기능: isAllowed가 limit 이내에서 true를 반환
- 엣지 케이스: limit이 0이면 항상 false
- 시간 경과: windowMs 이후에는 다시 허용

테스트만 작성하고 구현은 하지 마세요.
```

**Terminal 2 (Implementer)**:

```
src/test_tdd_limiter.py의 실패하는 테스트 3개를 통과하도록
TddRateLimiter를 구현해주세요.

- 파일: src/tdd_limiter.py
- 최소한의 코드로 테스트를 통과시키세요
- 구현 후 uv run pytest로 확인해주세요
```

### Round 2

**Terminal 1 (Test Writer)**:

```
src/test_tdd_limiter.py에 추가 테스트를 3개 더 작성해주세요.

- 동시 다발 요청: 100개 요청을 동시에 보냈을 때
- 다중 키: 서로 다른 키에 대해 독립적으로 제한
- 리셋: reset() 호출 후 카운트가 초기화
```

**Terminal 2 (Implementer)**:

```
src/test_tdd_limiter.py의 새로 추가된 테스트를 통과하도록
src/tdd_limiter.py를 업데이트해주세요.
```

### 확인 사항
- [ ] 각 라운드에서 테스트가 먼저 실패하고, 구현 후 통과하는가
- [ ] 구현이 테스트에 필요한 최소한의 코드만 포함하는가
- [ ] 라운드를 거듭할수록 구현이 더 견고해지는가

---

## Step 4: Specialist Team 패턴

전문 분야별로 세션을 나누어 병렬 작업합니다.

### 시나리오

Rate Limiter 서비스를 완성합니다. 3개의 전문 세션이 병렬로 작업합니다.

### Terminal 1 — Backend Specialist

```
Rate Limiter 백엔드를 구현해주세요.

1. src/rate_limiter_service.py — HTTP 서버
   - POST /check — { key, limit, windowMs } → { allowed, remaining, retryAfter }
   - GET /stats — 전체 통계
   - DELETE /reset/:key — 특정 키 리셋

2. 슬라이딩 윈도우 알고리즘 사용
3. in-memory 저장소
```

### Terminal 2 — Frontend Specialist

```
Rate Limiter 대시보드 UI를 구현해주세요.

1. src/dashboard.html — 단일 HTML 파일
   - Rate limit 상태 실시간 표시
   - 요청 보내기 버튼
   - 남은 요청 수, 리셋 시간 표시
   - 간단한 차트 (CSS 바 그래프)

2. Vanilla JS/HTML/CSS만 사용 (프레임워크 없음)
3. fetch API로 백엔드와 통신
```

### Terminal 3 — Test Specialist

```
Rate Limiter 서비스의 통합 테스트를 작성해주세요.

1. src/test_rate_limiter_service.py
   - API 엔드포인트별 테스트
   - Rate limit이 정확히 동작하는지
   - 윈도우 경과 후 리셋되는지
   - 동시 요청 처리
   - 에러 처리 (잘못된 입력)

2. 각 테스트가 독립적으로 실행 가능해야 함
```

### 통합

모든 세션의 작업이 완료된 후:

```
세 개의 전문 세션이 만든 결과물을 통합 검증해주세요:
1. 백엔드 서비스를 시작하고
2. 통합 테스트를 실행하고
3. 대시보드가 백엔드와 올바르게 통신하는지 확인
```

### 확인 사항
- [ ] 각 Specialist가 자신의 영역에만 집중했는가
- [ ] 인터페이스(API 스펙)를 통해 소통했는가
- [ ] 통합 시 큰 문제 없이 합쳐졌는가

---

## 성공 기준

- [ ] Writer/Reviewer 패턴으로 코드 품질을 높일 수 있었다
- [ ] Competing Prototypes로 최적의 구현을 선택할 수 있었다
- [ ] TDD Ping-Pong으로 견고한 코드를 작성할 수 있었다
- [ ] Specialist Team으로 병렬 개발을 수행할 수 있었다

## 핵심 교훈

1. **역할 분리**: 작성과 리뷰를 분리하면 품질이 올라간다
2. **다양한 관점**: 같은 문제를 다르게 풀어보면 최선의 해법을 찾을 수 있다
3. **점진적 개발**: TDD Ping-Pong은 항상 동작하는 코드를 보장한다
4. **전문화**: 각 세션이 전문 영역에 집중하면 효율이 높아진다
5. **인터페이스 중심**: 멀티세션의 핵심은 명확한 인터페이스(계약)
