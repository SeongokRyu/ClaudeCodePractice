/**
 * Rate Limiter Interface
 *
 * API 요청 속도를 제한하는 Rate Limiter의 공통 인터페이스.
 * Sliding Window와 Token Bucket 두 가지 구현 모두 이 인터페이스를 따릅니다.
 */

export interface RateLimiterConfig {
  /** 시간 윈도우 내 최대 허용 요청 수 */
  maxRequests: number;

  /** 시간 윈도우 크기 (밀리초) */
  windowMs: number;
}

export interface RateLimitResult {
  /** 요청이 허용되었는지 여부 */
  allowed: boolean;

  /** 현재 윈도우에서 남은 허용 요청 수 */
  remaining: number;

  /** 다음 요청이 허용될 때까지의 시간 (밀리초). 허용된 경우 0 */
  retryAfterMs: number;
}

export interface RateLimiter {
  /**
   * 주어진 키에 대한 요청이 허용되는지 확인하고,
   * 허용되면 요청을 기록합니다.
   *
   * @param key - 제한을 적용할 키 (예: IP 주소, API 키)
   * @returns 요청 허용 여부와 관련 정보
   */
  isAllowed(key: string): RateLimitResult;

  /**
   * 주어진 키의 현재 윈도우에서 남은 허용 요청 수를 반환합니다.
   * isAllowed와 달리 요청을 기록하지 않습니다 (조회만).
   *
   * @param key - 조회할 키
   * @returns 남은 요청 수
   */
  getRemainingRequests(key: string): number;

  /**
   * 주어진 키의 요청 기록을 초기화합니다.
   *
   * @param key - 초기화할 키
   */
  reset(key: string): void;

  /**
   * 모든 키의 요청 기록을 초기화합니다.
   */
  resetAll(): void;
}
