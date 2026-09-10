import { useAuthStore } from '@/store/auth'
import { useLoadingStore } from '@/store/loading'

const BASE_URL = (process.env.NEXT_PUBLIC_API_URL ?? '').replace(/\/$/, '')

let isRefreshing = false
let refreshPromise: Promise<string | null> | null = null

async function refreshToken(): Promise<string | null> {
  if (isRefreshing && refreshPromise) {
    return refreshPromise
  }
  isRefreshing = true
  refreshPromise = (async () => {
    try {
      const res = await fetch(`${BASE_URL}/api/auth/refresh`, {
        method: 'POST',
        credentials: 'include',
      })
      if (!res.ok) throw new Error('refresh failed')
      const { access_token } = await res.json()
      useAuthStore.getState().setTokens(access_token)
      return access_token
    } catch {
      useAuthStore.getState().logout()
      if (typeof window !== 'undefined') {
        window.location.assign('/login')
      }
      return null
    } finally {
      isRefreshing = false
      refreshPromise = null
    }
  })()
  return refreshPromise
}

export async function apiFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const { inc, dec } = useLoadingStore.getState()
  inc()
  try {
    return await _apiFetch(url, options)
  } finally {
    dec()
  }
}

async function _apiFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = useAuthStore.getState().accessToken
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  let res = await fetch(`${BASE_URL}${url}`, {
    ...options,
    headers,
    credentials: 'include',
  })

  if (res.status === 401 && token) {
    const newToken = await refreshToken()
    if (newToken) {
      headers['Authorization'] = `Bearer ${newToken}`
      res = await fetch(`${BASE_URL}${url}`, {
        ...options,
        headers,
        credentials: 'include',
      })
    }
  }

  return res
}

export function apiUrl(path: string): string {
  return `${BASE_URL}${path}`
}
