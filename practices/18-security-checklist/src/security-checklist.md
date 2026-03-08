# 8 Security Quality Gates

코드가 프로덕션에 배포되기 전에 통과해야 하는 8가지 보안 품질 게이트입니다.

## Gate 1: Secrets Management

- [ ] 하드코딩된 비밀 키, API 키, 비밀번호가 없는가?
- [ ] 비밀은 환경 변수 또는 secrets manager로 관리되는가?
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는가?
- [ ] 커밋 히스토리에 비밀이 노출된 적이 없는가?

**검증 방법**: `grep -r "password\|secret\|api_key\|token" --include="*.ts" src/`

## Gate 2: Input Validation

- [ ] 모든 사용자 입력이 검증되는가? (타입, 길이, 형식)
- [ ] SQL/NoSQL 쿼리에 파라미터화된 쿼리를 사용하는가?
- [ ] HTML 출력에서 사용자 데이터가 이스케이프되는가?
- [ ] 파일 업로드 시 타입과 크기가 검증되는가?

**검증 방법**: 모든 요청 핸들러에서 `req.body`, `req.params`, `req.query` 사용 부분 검토

## Gate 3: Authentication & Authorization

- [ ] 모든 보호 대상 엔드포인트에 인증이 적용되는가?
- [ ] 인증 토큰의 만료 시간이 설정되어 있는가?
- [ ] 권한 확인이 적절히 수행되는가? (RBAC/ABAC)
- [ ] 비밀번호가 안전하게 해싱되는가? (bcrypt, argon2)

**검증 방법**: 각 라우트에 인증 미들웨어가 적용되어 있는지 확인

## Gate 4: Data Protection

- [ ] 민감한 데이터가 API 응답에 포함되지 않는가?
- [ ] 비밀번호, 토큰 등이 로그에 기록되지 않는가?
- [ ] HTTPS가 강제되는가?
- [ ] 민감한 데이터가 암호화되어 저장되는가?

**검증 방법**: API 응답 스키마에서 `password`, `token`, `secret` 필드 검토

## Gate 5: Error Handling

- [ ] 에러 응답에 내부 정보가 노출되지 않는가? (스택 트레이스, DB 쿼리)
- [ ] 일관된 에러 형식을 사용하는가?
- [ ] 예상치 못한 에러가 안전하게 처리되는가?
- [ ] 에러 로그에 충분한 정보가 기록되는가? (단, 민감 정보 제외)

**검증 방법**: 에러 핸들러에서 `error.message`, `error.stack` 반환 여부 확인

## Gate 6: CORS & Headers

- [ ] CORS가 필요한 도메인만 허용하는가? (`*` 금지)
- [ ] 보안 헤더가 설정되어 있는가?
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Strict-Transport-Security`
  - `Content-Security-Policy`
- [ ] 불필요한 서버 정보가 노출되지 않는가? (`X-Powered-By` 제거)

**검증 방법**: 응답 헤더 검토

## Gate 7: Dependencies

- [ ] 알려진 취약점이 있는 패키지가 없는가? (`npm audit`)
- [ ] 의심스러운 패키지명이 없는가? (slopsquatting/typosquatting)
- [ ] 패키지 버전이 고정되어 있는가? (lock 파일 사용)
- [ ] 불필요한 의존성이 제거되었는가?

**검증 방법**: `npm audit`, 각 패키지의 npm 페이지 확인

## Gate 8: Access Control

- [ ] IDOR 취약점이 없는가? (직접 객체 참조 시 소유권 확인)
- [ ] 최소 권한 원칙이 적용되는가?
- [ ] 관리자 기능에 추가 보안이 적용되는가?
- [ ] Rate limiting이 적용되는가?

**검증 방법**: 리소스 접근 시 소유권/권한 확인 로직 검토

---

## 사용 방법

### Claude에게 게이트 적용 요청

```
src/security-checklist.md의 8가지 보안 게이트를 현재 프로젝트에 적용해주세요.
각 게이트에 대해 PASS 또는 FAIL을 판정하고, FAIL인 항목은 수정 방법을 제시해주세요.
```

### 결과 형식

| Gate | 항목 | 상태 | 비고 |
|------|------|------|------|
| 1 | Secrets Management | FAIL | JWT_SECRET 하드코딩 |
| 2 | Input Validation | FAIL | SQL 인젝션 가능 |
| ... | ... | ... | ... |

### 통과 기준

- **배포 가능**: 모든 게이트 PASS
- **조건부 배포**: Gate 1-4 PASS, Gate 5-8 중 일부 FAIL (개선 계획 필요)
- **배포 불가**: Gate 1-4 중 하나라도 FAIL
