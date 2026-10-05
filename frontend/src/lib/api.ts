import { useAuthStore } from '@/store/auth'
import { useLoadingStore } from '@/store/loading'

const BASE_URL = ''

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
    const newToken = await waitForRefresh(options.signal)
    options.signal?.throwIfAborted()
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

function waitForRefresh(signal?: AbortSignal | null): Promise<string | null> {
  signal?.throwIfAborted()
  const pending = refreshToken()
  if (!signal) return pending
  // Cancel this consumer's wait, not the token rotation shared by other requests.
  return new Promise((resolve, reject) => {
    const abort = () => reject(signal.reason)
    signal.addEventListener('abort', abort, { once: true })
    pending.then(
      (token) => {
        signal.removeEventListener('abort', abort)
        resolve(token)
      },
      (error) => {
        signal.removeEventListener('abort', abort)
        reject(error)
      }
    )
  })
}

export function apiUrl(path: string): string {
  return `${BASE_URL}${path}`
}
