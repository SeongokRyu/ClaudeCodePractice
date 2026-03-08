# Practice 18: 보안 체크리스트

## Goal

보안 리뷰 워크플로우를 학습합니다. OWASP Top 10 기준으로 취약한 코드를 분석하고, 취약점을 수정하며, slopsquatting(가짜 패키지 공격)을 탐지하는 방법을 익힙니다.

## Prerequisites

- Practice 01 (Golden Workflow) 완료

## Time

45-60 minutes

## Difficulty

★★☆ (Intermediate)

## What You'll Learn

- OWASP Top 10 취약점 식별 방법
- Claude를 활용한 보안 코드 리뷰
- 취약점 심각도 평가 (Critical/High/Medium/Low)
- 취약점 수정 및 검증
- Slopsquatting 탐지 (가짜/유사 패키지명 공격)

## Key Concepts

### OWASP Top 10 (2021)

| # | 취약점 | 이 실습에서의 예시 |
|---|--------|-------------------|
| A01 | Broken Access Control | 인증 없는 관리자 엔드포인트 |
| A02 | Cryptographic Failures | 하드코딩된 비밀 키 |
| A03 | Injection | SQL 인젝션 (문자열 템플릿) |
| A04 | Insecure Design | IDOR (직접 객체 참조) |
| A05 | Security Misconfiguration | CORS 전체 허용 |
| A06 | Vulnerable Components | 가짜 패키지 (slopsquatting) |
| A07 | Auth Failures | 평문 비밀번호 저장 |
| A08 | Data Integrity Failures | 입력 검증 없음 |
| A09 | Logging Failures | 민감 정보 로깅 |
| A10 | SSRF | 검증 없는 URL 요청 |

### Slopsquatting이란?

AI가 존재하지 않는 패키지명을 추천(hallucinate)하는 것을 악용하여, 해당 이름으로 악성 패키지를 등록하는 공격입니다.

```
Claude: "express-rate-limiter-v2를 설치하세요"  ← 존재하지 않는 패키지!
공격자: npm에 express-rate-limiter-v2 이름으로 악성 패키지 등록
개발자: npm install express-rate-limiter-v2  ← 악성 코드 실행!
```

## Getting Started

1. `CHALLENGE.md`를 열어 단계별 실습을 진행하세요
2. `src/vulnerable-app.ts`에 의도적으로 취약한 코드가 있습니다
3. 취약점을 찾고, 수정하고, 테스트로 검증합니다
