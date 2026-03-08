# Harness Engineering 연구 자료

---

## 1. Harness Engineering 정의

### 핵심 개념

Harness Engineering은 AI 에이전트를 둘러싼 인프라, 제약, 피드백 메커니즘을 설계하는 분야다. 직접 코드를 작성하는 것이 아니라, AI 시스템이 정의된 가드레일 안에서 운영되도록 환경을 만드는 것이다.

**비유**: AI 모델은 "말"(강력하지만 예측 불가), 하네스는 "인프라"(제약과 피드백 루프), 엔지니어는 "기수"(방향 제공).

> "2025년은 에이전트의 해였다. 2026년은 에이전트 하네스의 해다. 에이전트가 어려운 부분이 아니라, 하네스가 어려운 부분이다."
> — Aakash Gupta, Medium

### Martin Fowler / Birgitta Böckeler의 정의

Harness Engineering은 AI 에이전트가 대규모로 코드를 생성할 때 이를 **제약하고 신뢰성 있게 유지하기 위한 도구와 관행**이다. 이 용어는 OpenAI 팀이 에이전트만으로 100만 줄 이상의 코드베이스를 구축한 실험에서 유래했다.

핵심 철학: **에이전트 실패를 신호로 취급한다** — 에이전트가 어려움을 겪으면 누락된 요소(도구, 가드레일, 문서)를 식별하고 개선사항을 코드베이스에 반영한다.

### 컴퓨터 아키텍처 비유 (Philipp Schmid)

| 개념 | 비유 |
|------|------|
| Model | CPU — 원시 연산 능력 |
| Context Window | RAM — 제한적이고 휘발성인 작업 메모리 |
| Agent Harness | 운영체제 — 컨텍스트 큐레이션, 부트 시퀀스, 도구 핸들링 |
| Agent | 애플리케이션 — OS 위에서 동작하는 사용자별 로직 |

### 에이전트 하네스의 4가지 핵심 기능

1. AI 에이전트가 **할 수 있는 것을 제약** (Constrain)
2. 에이전트에게 **해야 할 것을 알려줌** (Inform)
3. 에이전트가 **올바르게 했는지 검증** (Verify)
4. 잘못했을 때 **교정** (Correct)

---

## 2. 하네스의 3대 핵심 구성 요소

### 2.1 Context Engineering (컨텍스트 엔지니어링)

에이전트가 적절한 시점에 적절한 정보에 접근하도록 보장한다.

**정적 요소:**
- 저장소 문서 (Repository documentation)
- `AGENTS.md` / `CLAUDE.md` 파일
- 검증된 설계 스펙

**동적 요소:**
- 실시간 로그, 메트릭, 트레이스
- 디렉토리 구조 매핑
- CI/CD 상태

**핵심 원칙**: 에이전트가 필요한 모든 것은 저장소에서 접근 가능해야 한다. Slack이나 Google Docs에만 있는 지식은 시스템에서 보이지 않는다.

### 2.2 Architectural Constraints (아키텍처 제약)

제안이 아닌 **기계적으로** 구조적 표준을 강제한다.

- 의존성 레이어링 규칙
- 커스텀 린터로 위반 감지
- LLM 기반 코드 감사자
- 구조적 테스트 프레임워크
- Pre-commit 자동화

> **역설**: 솔루션 공간을 제약하면 에이전트가 더 생산적이 된다 — 막다른 길 탐색을 제거하기 때문.

### 2.3 Entropy Management (엔트로피 관리)

주기적 정리 에이전트가 코드베이스 건강을 유지한다:

- 문서 일관성 검증
- 제약 위반 스캔
- 패턴 적용
- 의존성 감사

---

## 3. Deterministic vs Probabilistic Control (결정론적 vs 확률적 제어)

### 근본적 차이

| 구분 | 확률적 제어 (Probabilistic) | 결정론적 제어 (Deterministic) |
|------|---------------------------|-------------------------------|
| 메커니즘 | CLAUDE.md, 프롬프트, 자연어 지시 | Hooks, 린터, 테스트, 샌드박스 |
| 강제력 | 권고 사항 (Advisory) | 강제 게이트 (Enforced Gates) |
| 신뢰성 | 모델이 무시할 수 있음 | 물리적으로 우회 불가 |
| 적용 시점 | 모델 추론 중 | 모델 실행 전/후 |

### Praetorian의 "Thin Agent / Fat Platform" 패턴

> "현재의 '에이전틱' 접근법은 대규모에서 실패한다. 결정론적 엔지니어링 작업에 확률적 안내(프롬프트)를 의존하기 때문이다."

**솔루션 — 전통적 아키텍처를 뒤집는다:**

- **에이전트**: 상태 없는 임시 워커 (< 150줄)
- **스킬**: 도메인 지식, JIT 로드
- **후크**: LLM 컨텍스트 밖에서 제약 강제
- **오케스트레이션**: 특화된 역할 라이프사이클 관리

### 도구 제한을 통한 제약 기반 결정론

프롬프트 제안에 의존하는 대신 **도구 제한**으로 행동을 강제:

- **오케스트레이터**: `Task` 도구만 받음 (Edit 없음) → 물리적으로 코드 작성 불가, 위임 필수
- **실행자**: `Edit`/`Write` 도구만 받음 (Task 없음) → 물리적으로 위임 불가, 작업 필수
- **서브 에이전트 스폰 불가**: 무한 재귀 방지

### CLAUDE.md vs Hooks의 관계

- CLAUDE.md 규칙은 Hooks 없이는 **권고 사항**에 불과
- Hooks가 있으면 **강제 게이트**가 됨
- `PreToolUse` Hooks: 검토가 필요한 액션 차단
- `PostToolUse` Hooks: 품질 검사 실행
- `Stop` Hooks: 최종 출력 검증

---

## 4. Claude Code Hooks 시스템 — 하네스 메커니즘

### 4.1 Hook 이벤트 전체 라이프사이클

| 이벤트 | 발동 시점 |
|--------|-----------|
| `SessionStart` | 세션 시작 또는 재개 |
| `UserPromptSubmit` | 프롬프트 제출, Claude 처리 전 |
| `PreToolUse` | 도구 호출 실행 전 — **차단 가능** |
| `PermissionRequest` | 권한 대화상자 표시 시 |
| `PostToolUse` | 도구 호출 성공 후 |
| `PostToolUseFailure` | 도구 호출 실패 후 |
| `Notification` | Claude Code가 알림 전송 시 |
| `SubagentStart` | 서브에이전트 스폰 시 |
| `SubagentStop` | 서브에이전트 완료 시 |
| `Stop` | Claude 응답 완료 시 |
| `TeammateIdle` | 팀원 에이전트 유휴 전환 시 |
| `TaskCompleted` | 작업 완료 표시 시 |
| `InstructionsLoaded` | CLAUDE.md 로드 시 |
| `ConfigChange` | 설정 파일 변경 시 |
| `WorktreeCreate` | 워크트리 생성 시 |
| `WorktreeRemove` | 워크트리 제거 시 |
| `PreCompact` | 컨텍스트 압축 전 |
| `SessionEnd` | 세션 종료 시 |

### 4.2 Hook 유형 (4가지)

| 유형 | 설명 |
|------|------|
| `command` | 셸 명령 실행 |
| `http` | HTTP 엔드포인트에 POST |
| `prompt` | 단일 턴 LLM 평가 (판단이 필요한 결정) |
| `agent` | 멀티 턴 검증 (도구 접근 가능) |

### 4.3 PreToolUse — 가장 중요한 하네스 메커니즘

**PreToolUse만이 액션을 차단할 수 있다.** PostToolUse는 이미 실행된 액션을 되돌릴 수 없다.

**결정 옵션:**
- `"allow"`: 권한 프롬프트 없이 진행
- `"deny"`: 도구 호출 취소, 이유를 Claude에 피드백
- `"ask"`: 사용자에게 권한 프롬프트 표시

**v2.0.10부터 입력 수정 가능:**
- 차단 대신 도구 입력을 인터셉트하여 수정 후 실행
- 투명한 샌드박싱, 자동 보안 강제, 팀 규약 준수 가능

### 4.4 핵심 실용 패턴

#### 보호 파일 차단

```bash
#!/bin/bash
# protect-files.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done
exit 0
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

#### 위험한 Bash 명령 차단

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2
  exit 2
fi
exit 0
```

#### 코드 자동 포맷팅 (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

#### 압축 후 컨텍스트 재주입

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

#### Agent 기반 Stop Hook (테스트 통과 검증)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

#### Prompt 기반 Stop Hook (작업 완료 검증)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

### 4.5 Hook 저장 위치와 범위

| 위치 | 범위 | 공유 가능 |
|------|------|-----------|
| `~/.claude/settings.json` | 모든 프로젝트 | 아니오 (로컬) |
| `.claude/settings.json` | 단일 프로젝트 | 예 (커밋 가능) |
| `.claude/settings.local.json` | 단일 프로젝트 | 아니오 (gitignored) |
| Managed policy settings | 조직 전체 | 예 (관리자 제어) |

---

## 5. 샌드박싱 및 보안 경계

### 5.1 Claude Code 네이티브 샌드박싱

Claude Code는 OS 수준 프리미티브를 사용하여 파일시스템과 네트워크 격리를 제공한다.

**파일시스템 격리:**
- 기본: 현재 작업 디렉토리에만 읽기/쓰기
- 전체 컴퓨터에 읽기 접근 (특정 거부 디렉토리 제외)
- `sandbox.filesystem.allowWrite`로 추가 경로 허용
- macOS: Seatbelt, Linux: bubblewrap 사용

**네트워크 격리:**
- 승인된 도메인만 접근 가능
- 새 도메인 요청 시 권한 프롬프트
- 모든 스크립트/프로그램/하위 프로세스에 적용

**샌드박스 모드:**
- **Auto-allow 모드**: 샌드박스 내 Bash 명령 자동 승인
- **Regular permissions 모드**: 모든 Bash 명령 표준 권한 흐름 통과

### 5.2 프로덕션 AI 에이전트 샌드박싱 원칙

**Zero-Trust 원칙**: 모든 AI 생성 코드를 잠재적으로 악의적인 것으로 취급

**방어 심층 (Defense-in-Depth):**
1. 격리 경계 (Isolation Boundaries)
2. 리소스 제한 (Resource Limits)
3. 네트워크 제어 (Network Controls)
4. 권한 범위 지정 (Permission Scoping)
5. 모니터링 (Monitoring)

**프로덕션 배포 전 체크리스트:**
- `CAP_SYS_ADMIN` 삭제
- 기본 네트워크 접근 제로, 이그레스 거부 목록 구현
- 로깅 프록시를 통한 필요 트래픽 라우팅
- 모든 에이전트 세션에 고유한 시간 제한 서비스 계정 할당

### 5.3 격리 기술 계층

| 기술 | 격리 강도 | 사용 사례 |
|------|-----------|-----------|
| Firecracker microVMs | 최강 | 프로덕션 비신뢰 코드 |
| Kata Containers | 강함 | 하드웨어 강제 경계 |
| gVisor | 중간 | 커널 호출 인터셉트 |
| 표준 컨테이너 | 부족 | 비신뢰 코드에 불충분 |

---

## 6. "Stop Prompting, Start Governing" 패러다임

### 패러다임 전환

2026년은 AI 에이전트 실험에서 엔터프라이즈 거버넌스와 운영 통제로의 전환을 의미한다.

**핵심 변화:**
- "채택 촉진"에서 "거버넌스 강제"로
- 빌드 타임에서 런타임으로 초점 이동
- 에이전트 생성보다 에이전트 관리가 더 복잡

> "AI 에이전트 사용을 막는 것이 아니라, 정의된 'Trust Sandbox' 내에서 운영되도록 보장하는 것이 목표다."

### 엔터프라이즈 거버넌스 프레임워크

**규제 컨텍스트 (2026):**
- ISO 42001 준수가 기본선
- NIST AI Risk Management Framework
- EU AI Act 및 DORA 전면 시행
- AI 모델의 기술 부채가 재무 오류와 동일한 심각도로 취급

**핵심 거버넌스 패턴:**
- 에이전트를 구축하는 시스템과 거버넌스하는 시스템 분리
- 런타임 제어 평면: 프롬프트 방화벽, 에이전트 Zero Trust, 행동 모니터링
- Fine-grained 역할 기반 접근, 데이터 거버넌스 정책, 민감 작업 승인 워크플로우

### 확률적 가드레일의 실패

> "현재의 소프트 가드레일이 치명적으로 실패하고 있다. 이 제어는 종종 확률적이거나 패턴 기반이거나 LLM 자기 평가에 의존하며, 에이전트의 핵심 역량인 자율성과 구성 가능성에 의해 쉽게 우회된다."

---

## 7. Context Engineering vs Prompt Engineering

### 핵심 차이

| 구분 | Prompt Engineering | Context Engineering |
|------|-------------------|---------------------|
| 초점 | 무엇을 묻는가 | 모델이 물을 때 이미 알고 있는 것 |
| 범위 | 일회성 텍스트 지시 | 전체 정보 환경 아키텍처 |
| 대상 | 단일 LLM 호출 | 다단계 에이전트 상호작용 |
| 관리 | 지시 작성 | 메모리, 문서, 도구 정의, 대화 이력 |

### Anthropic 공식 가이드 핵심 원칙

**Attention Budget 문제:**
- LLM은 "컨텍스트 부패(context rot)" 현상 발생: 토큰 볼륨 증가 시 정보 회상 정확도 저하
- 트랜스포머의 n² 관계로 컨텍스트 크기와 집중력 사이 긴장
- **컨텍스트를 귀중하고 유한한 자원으로 취급**

**시스템 프롬프트 구조화:**
- "적절한 고도"를 찾아야 함 — 충분히 구체적이되 경직된 하드코딩은 피함
- XML 태그 또는 Markdown 헤더로 구분된 섹션:
  - `<background_information>`
  - `<instructions>`
  - `## Tool guidance`
  - `## Output description`

**도구 설계 원칙:**
- 자기 완결적이고 모호하지 않아야 함
- 기능 중복 없어야 함
- 인간 엔지니어가 어떤 도구를 사용할지 확실히 말할 수 없으면, AI 에이전트도 불가능

**런타임 컨텍스트 검색 — 하이브리드 접근:**
- 모든 데이터를 사전 로딩하지 않고, 가벼운 식별자(파일 경로, 링크) 유지
- 도구를 통해 동적으로 정보 로드
- Claude Code 예시: CLAUDE.md는 사전 로드, grep/glob으로 런타임 탐색

**장기 태스크 기법:**
1. **압축 (Compaction)**: 대화 이력 요약, 아키텍처 결정/미해결 버그/구현 세부사항 보존
2. **구조적 메모 (Agentic Memory)**: 외부 파일/DB에 진행 상황 추적
3. **서브 에이전트 아키텍처**: 전문 에이전트가 집중 작업 수행, 압축된 요약 반환

**핵심 규칙**: 원하는 결과를 최대화하는 가장 작은 고신호 토큰 집합을 찾아라.

---

## 8. 에이전트 오케스트레이션 패턴

### 9가지 프로덕션 준비 패턴

#### 1. 결정론적 상태 머신 오케스트레이션
자유형 에이전트 의사결정을 명시적 워크플로우 상태로 대체. 오케스트레이터가 유효한 상태를 관리, 에이전트는 해당 제약 내에서 제한된 선택.

#### 2. Supervisor + Specialists 아키텍처
모든 것을 처리하는 하나의 에이전트 대신 도메인별 전문 에이전트에 라우팅. 각 전문가는 축소된 도구 접근, 명확한 정책, 독립적 소유권.

#### 3. 엄격한 도구 계약 (Strict Tool Contracts)
모든 도구에 요구:
- 타입된 입력/출력 스키마
- 멱등성 제어
- 권한 강제
- 속도 제한 및 타임아웃

#### 4. 2단계 액션 (Plan → Validate → Execute)
제안과 실행 분리. 에이전트가 계획 생성 → 결정론적 정책 검사 → 승인된 계획만 실행.

#### 5. 이벤트 기반 큐 백업 워크플로우
장기 실행 작업에 비동기 태스크 큐 사용. 워크플로우 상태를 지속적으로 저장.

#### 6. 모델 라우팅 + 폴백
작업 복잡성과 위험 등급별 요청 라우팅. 폴백 체인 구현. 요청별 예산 제어 (토큰, 도구 호출, 벽시계 시간).

#### 7. 계층적 컨텍스트 관리
세션 컨텍스트 (대화 윈도우) / 태스크 상태 (지속적 체크포인트) / 시스템 상태 (정책) 분리. 대부분의 "메모리" 실패는 실제로 데이터 거버넌스 실패.

#### 8. 구조화된 에스컬레이션 표면
HITL(Human-in-the-loop)을 안전 밸브가 아닌 제품 기능으로 설계. 리뷰어에게 증거, 제안 계획, 정책 검사를 보여줌.

#### 9. 지속적 평가 + 리플레이
골든 데이터셋, 회귀 테스트, 섀도 모드, 카나리 릴리스. 모든 것을 버전 관리 (프롬프트, 도구, 정책, 모델).

### Praetorian 16단계 오케스트레이션 상태 머신

모든 복잡한 워크플로우가 따르는 엄격한 상태 머신:

| 단계 | 목적 |
|------|------|
| 1-4 | 셋업, 트리아지, 디스커버리, 스킬 매핑 |
| 5-7 | 복잡도 분석, 설계 정제, 아키텍처 계획 |
| 8-11 | 구현, 검증, 컴플라이언스, 코드 품질 |
| 12-16 | 테스트 계획, 테스팅, 커버리지 검증, 완료 |

**지능적 단계 스킵**: 버그 수정은 ~5단계 실행; 새 서브시스템은 16단계 모두 사용.

### 5역할 개발 패턴 (Praetorian)

| 역할 | 책임 | 산출물 |
|------|------|--------|
| Lead | 아키텍처 & 전략 분해 | Architecture Plan |
| Developer | 서브 태스크 구현 | Source Code |
| Reviewer | 컴플라이언스 검증 | Review Report |
| Test Lead | 테스트 전략 분석 | Test Plan |
| Tester | 테스트 작성 & 실행 | Test Cases |

---

## 9. Quality Gates 및 Validation Gates

### 품질 게이트 구현 패턴

**라우팅 게이트 vs Git 훅:**
- Git 훅은 사용자가 건너뛸 수 있음
- 라우팅 게이트는 에이전트 지시에 내장되고 트랜스크립트 증거를 통해 강제됨

**CI/CD 파이프라인 품질 게이트:**
- 코딩, 보안, 아키텍처 정책을 인간 리뷰 전에 강제
- 리뷰 병목 해소 및 피드백 표준화

**태스크 분해와 검증:**
- 체크포인팅, 세분화된 검증, 병렬 실행 가능
- Durable execution이 인프라 실패 처리
- Validation gates가 AI 환각 포착

### Compaction Gates (Praetorian)

토큰 위생을 프로그래밍적으로 강제하는 하드 블록:

| 컨텍스트 사용률 | 조치 |
|----------------|------|
| < 75% | 진행 |
| 75-85% | 경고 |
| > 85% | **하드 블록** — 컨텍스트 압축 실행까지 |

### 3단계 루프 시스템

**Level 1 (Intra-Task)**: 단일 에이전트가 셸 명령에 대한 무한 반복 방지 (최대 10회)

**Level 2 (Inter-Phase)**: 다중 도메인 피드백 루프가 구현 → 리뷰 → 테스트 사이클 강제

```yaml
modified_domains: ["backend", "frontend"]
domain_phases:
  backend: {review: PASS, testing: PASS}
  frontend: {review: PASS, testing: FAIL}
# 모든 도메인이 모든 단계를 통과할 때까지 종료 차단
```

**Level 3 (Orchestrator)**: 매크로 목표 미달 시 전체 단계 재호출

---

## 10. 프로덕션 준비: 신뢰성, 에러 처리, 모니터링

### 4대 지주 (Four Pillars)

#### 1. 구조화된 로깅
- 상관 ID(Correlation ID)로 모든 결정 포인트 로깅
- 도구 호출, 모델 결정, 실행 결과, 모든 에러

#### 2. 다층 에러 처리

| 계층 | 에러 유형 | 조치 |
|------|-----------|------|
| 1 | 일시적 (타임아웃, 속도 제한) | 지수 백오프로 자동 재시도 |
| 2 | LLM 복구 가능 (잘못된 파라미터) | 에러 컨텍스트를 모델에 반환 |
| 3 | 사용자 수정 가능 (인증, 권한) | 인간 개입 요청 |
| 4 | 예기치 않음 | 경보 및 에스컬레이션 |

#### 3. 출력 검증
모델 출력을 절대 신뢰하지 않는다:
- 스키마 검증 (Pydantic)
- 의미론적 검사 (신뢰도 임계값, 추론 품질)
- 도구별 형식 검증기

#### 4. 실시간 모니터링
실행 이벤트 스트리밍 및 추적:
- 태스크 유형별 성공/에러율
- 단계별 지연 시간
- 토큰 사용량 및 비용
- 복구율

### 측정 가능한 개선 (실증 데이터)

| 메트릭 | Before | After |
|--------|--------|-------|
| 실패율 | 22% | 2.1% |
| 평균 진단 시간 | 3+ 일 | < 30분 |
| 자동 복구율 | 0% | 87% |

### 프로덕션 준비 체크리스트

배포 전 필수:
- [ ] 정의된 전환이 있는 명시적 오케스트레이터 상태
- [ ] 모든 도구 스키마 검증 및 허용 목록화
- [ ] 부작용 있는 작업의 멱등성
- [ ] 상관 ID가 있는 엔드투엔드 트레이스
- [ ] 적대적 입력 포함 골든 테스트 셋
- [ ] 요청별 토큰/시간 예산 강제
- [ ] 롤백이 가능한 섀도/카나리 릴리스 전략

### 회피해야 할 안티패턴

- 무제한 도구 접근
- 대화에만 존재하는 워크플로우 상태
- 모든 관심사를 처리하는 메가 프롬프트
- 프롬프트 언어로 강제하는 권한
- 관찰 가능성 계층 없음
- 데모로만 평가하는 품질
- 계약 없는 수십 개의 도구 통합
- 통제되지 않는 토큰 지출

---

## 11. CNCF의 4대 플랫폼 제어 원칙 (에이전트 적용)

### 1. Golden Paths
사전 승인된 구성과 표준화된 하네스 설정. 팀이 독립적으로 생성하지 않고 상속.

### 2. Guardrails
"재정의할 수 없는 하드 정책 강제. 비용 상한, 기간 제한, 차단된 출력 패턴, 도구 허용 목록."

### 3. Safety Nets
자동 복구 메커니즘: 재시도 로직, 폴백 응답, 서킷 브레이커.

### 4. Manual Review
신뢰도가 낮거나 민감한 시스템 관련 시 인간 개입 게이트.

**시너지**: Golden Paths가 Guardrail 표면적을 줄이고, Safety Nets가 Guardrail이 놓치는 것을 잡고, Manual Review가 자동화 엣지 케이스를 처리.

---

## 12. 실무 전략 및 구현 수준

### 구현 수준별 로드맵

| 수준 | 대상 | 내용 | 소요 시간 |
|------|------|------|-----------|
| Level 1 | 개인 | `.cursorrules`, pre-commit hooks, 테스트 스위트 | 1-2시간 |
| Level 2 | 소규모 팀 | `CLAUDE.md`, CI 강제 제약, 공유 템플릿 | 1-2일 |
| Level 3 | 조직 | 커스텀 미들웨어, 관찰 가능성 통합, 성능 대시보드 | 1-2주 |

### 핵심 통찰

**LangChain 사례 연구**: 하네스만 수정하고 모델은 동일하게 유지 → Terminal Bench 2.0에서 52.8%에서 66.5%로 성능 향상 → Top 30에서 Top 5로 도약.

**OpenAI 성과**: 일반 개발 시간의 약 1/10로 100만+ 줄 프로덕션 애플리케이션 구축. 수동 작성 코드 제로. 3명의 엔지니어로 ~1,500 PR 병합 (엔지니어당 하루 3.5 PR).

### "빌드 투 딜리트" 원칙

> "모든 새 모델 릴리스에는 에이전트를 구조화하는 다른 최적의 방법이 있다."

모듈형 아키텍처를 설계하여 모델이 발전하면 어제의 로직을 빠르게 제거할 수 있어야 한다.

**경쟁 우위**: 하네스 엔지니어링에 지금 투자하는 기업이 지속되는 이점을 구축한다.

---

## 13. 비밀 관리 및 보안 패턴

### JIT (Just-In-Time) 주입 패턴 (Praetorian)

```
에이전트 요청: run_with_secrets("aws s3 ls")
→ 래퍼가 자식 프로세스 스폰
→ 1Password가 ENV 변수로 주입
→ 격리된 엔클레이브에서 명령 실행
→ 비밀이 로깅되거나 컨텍스트화되지 않음
```

비밀이 절대 LLM 컨텍스트에 진입하지 않도록 보장.

### 프롬프트 인젝션 방어 (Claude Code)

샌드박스가 프롬프트 인젝션 공격을 성공적으로 방어:
- **파일시스템**: `~/.bashrc`, `/bin/` 등 핵심 파일 수정 불가
- **네트워크**: 공격자 서버로 데이터 유출 불가, 비승인 도메인에서 스크립트 다운로드 불가
- **모니터링**: 모든 경계 테스트 시도가 OS 수준에서 차단되고 즉시 알림

---

## 14. 에이전트 관찰 가능성 (Observability)

### 핵심 메트릭

- **지연 시간 (Latency)**: 태스크 및 개별 단계별 측정
- **에러율**: 태스크 유형별 성공/실패율
- **토큰 사용량**: 비용 추적
- **추론 품질**: 사실 정확도, 의사결정 패턴
- **복구율**: 자동 복구 성공률

### 분산 트레이싱

초기 프롬프트부터 도구 호출, 최종 출력까지 에이전트 실행 경로를 추적. 병목 현상의 정확한 진단 가능.

### 도구 생태계

- **Langfuse**: 상세 트레이스 수집
- **Arize**: 실시간 메트릭 모니터링 대시보드
- **LangGraph**: 실패 시 폴백 경로가 있는 그래프 기반 접근

---

## 15. 핵심 요약: 하네스 엔지니어링의 본질

### "하네스가 제품을 결정한다"

> "동일한 모델을 사용하는 두 시스템이 하네스 품질에 따라 완전히 다른 성능을 보인다."

### 5가지 핵심 전략적 교훈

1. **모델보다 시스템**: 기저 모델은 점점 덜 중요해지고, 그것을 둘러싼 시스템이 더 중요해진다
2. **제약이 자율성을 가능하게 함**: 유연성을 포기하고 표준화된 패턴을 수용해야 에이전트 자율성이 높아진다
3. **결정론적 래핑**: LLM을 비결정론적 커널 프로세스로 취급하고 결정론적 런타임으로 감싸라
4. **피드백 루프**: 에이전트 실패에서 학습하여 하네스를 지속적으로 개선하라
5. **경쟁 우위의 원천**: 진정한 경쟁 우위는 프롬프트가 아닌 실행 중 캡처된 궤적 데이터에 있다

---

## 출처 (Sources)

- [Harness Engineering — Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [Harness Engineering: Complete Guide 2026 — NxCode](https://www.nxcode.io/resources/news/harness-engineering-complete-guide-ai-agent-codex-2026)
- [2025 Was Agents. 2026 Is Agent Harnesses — Aakash Gupta](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e)
- [The Importance of Agent Harness in 2026 — Philipp Schmid](https://www.philschmid.de/agent-harness-2026)
- [What is an Agent Harness — Parallel AI](https://parallel.ai/articles/what-is-an-agent-harness)
- [Agent Harnesses: Why 2026 Isn't About More Agents — DEV Community](https://dev.to/htekdev/agent-harnesses-why-2026-isnt-about-more-agents-its-about-controlling-them-1f24)
- [Deterministic AI Orchestration — Praetorian](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)
- [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Claude Code Hooks Guide — Anthropic](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code Sandboxing — Anthropic](https://code.claude.com/docs/en/sandboxing)
- [Context Engineering: Why It's Replacing Prompt Engineering — DEV Community](https://dev.to/serenitiesai/context-engineering-why-its-replacing-prompt-engineering-in-2026-1b4g)
- [Context Engineering vs Prompt Engineering — Firecrawl](https://www.firecrawl.dev/blog/context-engineering)
- [AI Agent Orchestration Patterns — Microsoft Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Orchestrating AI Agents in Production — Hatchworks](https://hatchworks.com/blog/ai-agents/orchestrating-ai-agents/)
- [From Guardrails to Governance — MIT Technology Review](https://www.technologyreview.com/2026/02/04/1131014/from-guardrails-to-governance-a-ceos-guide-for-securing-agentic-systems)
- [AI Agent Reliability Guide — BSWEN](https://docs.bswen.com/blog/2026-03-06-agent-reliability/)
- [Top Runtime AI Governance Platforms 2026 — AccuKnox](https://accuknox.com/blog/runtime-ai-governance-security-platforms-llm-systems-2026)
- [How to Sandbox AI Agents 2026 — Northflank](https://northflank.com/blog/how-to-sandbox-ai-agents)
- [AI Agent Sandboxing & Progressive Enforcement — ARMO](https://www.armosec.io/blog/ai-agent-sandboxing-progressive-enforcement-guide/)
- [Agentic AI Governance Frameworks 2026 — CertMage](https://certmage.com/agentic-ai-governance-frameworks/)
- [Quality Gates — DeepWiki](https://deepwiki.com/rjmurillo/ai-agents/7.1-skill-architecture-and-frontmatter)
- [AI Code Guardrails — CodeScene](https://codescene.com/use-cases/ai-code-quality)
- [Taming AI Agents 2026 — CIO](https://www.cio.com/article/4064998/taming-ai-agents-the-autonomous-workforce-of-2026.html)
