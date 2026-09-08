
export interface ApiResponse<T> {
  code: number
  status_code: number
  data: T | null
  is_success: boolean
  detail: string
  timestamp: Date
}
