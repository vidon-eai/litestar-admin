const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002/api/v1';

export async function customFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.message || 'API 請求失敗');
  }

  return res.json();
}