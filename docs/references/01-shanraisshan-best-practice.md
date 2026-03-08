# shanraisshan/claude-code-best-practice

- **URL**: https://github.com/shanraisshan/claude-code-best-practice
- **Stars**: 12.4k | **License**: MIT
- **특징**: 실전 예제 중심의 Best Practice 모음. 날씨 시스템으로 Command/Agent/Skill 패턴 시연.

---

## 핵심 콘텐츠 구조

### Best Practice 문서
| 파일 | 내용 |
|------|------|
| claude-commands.md | 커맨드 frontmatter, 문자열 치환, 호출 방법, 빌트인 슬래시 명령어 전체 |
| claude-subagents.md | 서브에이전트 frontmatter, 6개 빌트인 에이전트 타입 |
| claude-skills.md | 스킬 frontmatter, 2가지 패턴(skill vs agent skill), 호출/스코프 |
| claude-memory.md | CLAUDE.md 로딩 메커니즘 (상향/하향/lazy), 모노레포 시나리오 |
| claude-settings.md | 55+ 설정 항목, 140+ 환경 변수 |
| claude-mcp.md | 추천 MCP 서버 (Context7, Playwright, Chrome, DeepWiki, Excalidraw) |
| claude-cli-startup-flags.md | CLI 시작 플래그 전체 레퍼런스 |

### Orchestration Workflow
**Command -> Agent -> Skill 패턴**
- Command: 사용자 진입점 (슬래시 명령)
- Agent: 작업 조율자 (모델/도구 선택)
- Skill: 실행 단위 (구체적 작업 수행)

### Development Workflows
- **Cross-Model Workflow**: Claude Code + Codex (Plan → QA Review → Implement → Verify)
- **RPI Workflow**: Research → Plan → Implement (검증 게이트 포함)

### Reports (심화 분석)
- Agent SDK vs CLI 시스템 프롬프트 비교
- 브라우저 자동화 MCP 비교 (Chrome DevTools vs Playwright)
- 모노레포에서 Skills 디스커버리 메커니즘
- Agent Memory 작동 방식
- Programmatic Tool Calling (PTC), Dynamic Filtering
- 사용량/Rate Limits 가이드
- LLM 일간 성능 변동 분석

### Tips
- Boris Cherny의 12가지 커스터마이징 팁 (2026.02)

---

## 핵심 발췌

### Orchestration 패턴 (가장 중요)
```
사용자 → /command 실행
  → Agent 호출 (모델/도구 결정)
    → Skill 실행 (구체적 작업)
      → 결과 반환
```

### CLAUDE.md 로딩 순서 (모노레포)
1. **상향 로딩**: 현재 디렉토리 → 루트까지 모든 CLAUDE.md 자동 로드
2. **하향 로딩**: 하위 디렉토리는 lazy 로드 (필요시만)

### 추천 MCP 서버 조합
- **Context7**: 공식 문서 실시간 조회 (환각 방지)
- **Playwright**: 브라우저 자동화, E2E 테스트
- **Chrome DevTools**: 실시간 브라우저 디버깅
- **DeepWiki**: GitHub 레포 분석
- **Excalidraw**: 다이어그램 생성
