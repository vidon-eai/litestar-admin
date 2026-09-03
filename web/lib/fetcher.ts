/**
 * lib/fetcher.ts
 * ──────────────
 * Single, typed fetch wrapper. All network calls in the app go through here.
 * - Injects auth header (from stored token / cookie-based auth)
 * - Normalises error shapes into ApiError
 * - Returns typed ApiResponse<T> envelope
 *
 * Replace the `getAuthToken` implementation below once your auth provider is chosen.
 */

// ──────────────────────────────────────────────
// Types
// ──────────────────────────────────────────────

export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
    public readonly data?: unknown
  ) {
    super(message)
    this.name = "ApiError"
  }
}

type RequestOptions = Omit<RequestInit, "body"> & {
  body?: unknown
  params?: Record<string, string | number | boolean | undefined>
}

// ──────────────────────────────────────────────
// Auth token provider (swap based on your auth strategy)
// ──────────────────────────────────────────────

function getAuthToken(): string | null {
  if (typeof window === "undefined") return null
  // TODO: return token from Clerk, Auth.js session, or localStorage JWT
  return null
}

// ──────────────────────────────────────────────
// Core fetcher
// ──────────────────────────────────────────────

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002/api/v1"

export async function fetcher<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { body, params, headers: extraHeaders, ...rest } = options

  const url = new URL(
    `${BASE_URL}${endpoint}`,
    typeof window !== "undefined"
      ? window.location.origin
      : "http://localhost:8082"
  )
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) url.searchParams.set(key, String(value))
    })
  }

  const token = getAuthToken()
  const authHeader: Record<string, string> = token
    ? { Authorization: `Bearer ${token}` }
    : {}

  // 判斷 body 是否為 URLSearchParams
  const isFormUrlEncoded = body instanceof URLSearchParams

  // 處理 Content-Type 預設值（如果是 URLSearchParams 則不強制使用 application/json）
  const defaultContentType = isFormUrlEncoded
    ? "application/x-www-form-urlencoded"
    : "application/json"

  // 處理 body 轉譯（若是 URLSearchParams 則傳送原內容或字串）
  const formattedBody =
    body !== undefined
      ? isFormUrlEncoded
        ? body.toString()
        : JSON.stringify(body)
      : undefined

  const response = await fetch(url.toString(), {
    ...rest,
    headers: {
      "Content-Type": defaultContentType,
      ...authHeader,
      ...(extraHeaders as Record<string, string>),
    },
    body: formattedBody,
  })

  if (!response.ok) {
    let errData: unknown
    try {
      errData = await response.json()
    } catch {
      errData = null
    }
    const message =
      (errData as { message?: string } | null)?.message ??
      `Request failed with status ${response.status}`
    throw new ApiError(response.status, message, errData)
  }

  return response.json() as Promise<T>
}

/** Convenience helpers for common HTTP verbs */
export const api = {
  get: <T>(endpoint: string, params?: RequestOptions["params"]) =>
    fetcher<T>(endpoint, { method: "GET", params }),

  // 🌟 修改處：讓 post 可以接受第三個參數 options (用來傳入自訂 headers 等)
  post: <T>(
    endpoint: string,
    body: unknown,
    options?: Omit<RequestOptions, "body">
  ) => fetcher<T>(endpoint, { method: "POST", body, ...options }),

  put: <T>(
    endpoint: string,
    body: unknown,
    options?: Omit<RequestOptions, "body">
  ) => fetcher<T>(endpoint, { method: "PUT", body, ...options }),

  patch: <T>(
    endpoint: string,
    body: unknown,
    options?: Omit<RequestOptions, "body">
  ) => fetcher<T>(endpoint, { method: "PATCH", body, ...options }),

  delete: <T>(endpoint: string) => fetcher<T>(endpoint, { method: "DELETE" }),
}
