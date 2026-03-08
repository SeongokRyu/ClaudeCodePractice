# AI Native Camp - 1기

- **URL**: https://github.com/ai-native-camp/camp-1
- **Stars**: 196 | **기간**: 2026-02-14 ~ 2026-02-21 (7일)
- **특징**: 비개발자 대상 Claude Code 집중 캠프. Skill로 커리큘럼 구성 (Skill을 만드는 법을 Skill로 배운다)
- **장소**: Naver D2SF

---

## 커리큘럼

| Day | Skill | 주제 |
|-----|-------|------|
| 1 | day1-onboarding | Claude Code 설치 + 7개 핵심 기능 |
| 2 | day2-supplement-mcp | MCP 딥다이브 |
| 2 | day2-create-context-sync-skill | 나만의 Context Sync 스킬 만들기 |
| 3 | coming soon | 요구사항 명확화 |
| 4 | day4-wrap-and-analyze | session-wrap + history-insight + session-analyzer |
| 5 | day5-fetch-and-digest | fetch-tweet, fetch-youtube, content-digest |
| 6 | day6-prd-submit | PRD 작성 및 GitHub PR 제출 |
| 7 | coming soon | 졸업 |

---

## Day 1: 온보딩 - 7개 핵심 기능

### Block 0: 환경 설정
- Claude Code 설치, 터미널/Git/GitHub 기초

### Block 1: 체험 데모
- Claude Code의 능력을 직접 체험

### Block 2: Why CLI?
- GUI가 아닌 CLI 선택의 이유

### Block 3: 7개 핵심 기능
1. **CLAUDE.md**: 프로젝트의 "헌법"
2. **Skill**: 재사용 가능한 워크플로우 정의
3. **MCP**: 외부 도구/서비스 연결 프로토콜
4. **Subagent**: 하위 에이전트 위임
5. **Agent Teams**: 멀티 에이전트 팀 협업
6. **Hook**: 결정론적 자동화
7. **Plugin**: 확장 기능

### Block 4: CLI/Git/GitHub 기초
- 기본 명령어, 버전 관리 기초

---

## Day 2: MCP + Context Sync 스킬

### MCP 딥다이브
- MCP 개념 이해
- 서버 설치 방법
- /mcp 명령어 사용법
- 인기 서버 소개
- Plugin MCP

### Context Sync 스킬 만들기 (핵심 실습)
단계별 과정:
1. **도구 선택** (block0): 어떤 MCP/API를 사용할지 결정
2. **프로젝트 탐색** (block1): 기존 코드베이스 이해
3. **도구 연결** (block2): MCP/API 실제 연동
4. **병렬 수집** (block3): 여러 소스에서 동시에 데이터 수집
5. **출력 포맷** (block4): 결과를 마크다운으로 정리
6. **완성** (block5): 스킬 최종 검증 및 마무리

---

## Day 4: Wrap & Analyze

### 핵심 개념
- 멀티 에이전트 개념 이해
- 세션 기록을 자동으로 정리하는 스킬 만들기

### 실습 내용
1. **session-wrap 스킬**: 세션 종료 시 자동으로 작업 내용 요약
2. **history-insight**: 과거 세션 히스토리에서 인사이트 추출
3. **session-analyzer**: 세션 패턴 분석 (어떤 작업에 시간을 많이 쓰는지)

---

## Day 5: Fetch & Digest

### 콘텐츠 파이프라인 구축
1. **fetch-tweet**: 트윗 콘텐츠 가져오기
2. **fetch-youtube**: 유튜브 콘텐츠 가져오기
3. **content-digest**: 콘텐츠 번역 + Quiz-First 학습
4. **통합**: 전체 파이프라인 연결

---

## 핵심 인사이트

### "Skills as Curriculum" 접근법
- 강의 슬라이드가 아닌, Claude가 직접 가르치는 대화형 학습
- `/day1-onboarding` 실행하면 Claude가 안내
- Skill을 만드는 것 자체가 학습 과정

### 설치 방법
```bash
npx skills add ai-native-camp/camp-1 --agent claude-code --yes
```

### Practice 설계에 참고할 점
- 비개발자도 접근 가능한 난이도 설계
- "만들면서 배우기" 패턴이 효과적
- 각 Day가 이전 Day 위에 쌓이는 점진적 구조
- 실제 산출물(스킬)이 남는 실습
