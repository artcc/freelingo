import { useAuthStore } from '@/store/auth'
import { useLoadingStore } from '@/store/loading'

const BASE_URL = ''

let refreshRequest: {
  sessionVersion: number
  promise: Promise<string | null>
} | null = null
let accessTokenRequest: {
  sessionVersion: number
  promise: Promise<string>
} | null = null

function currentSession(sessionVersion: number) {
  const state = useAuthStore.getState()
  if (state.sessionVersion !== sessionVersion) {
    throw new DOMException('Authentication session changed', 'AbortError')
  }
  return state
}

// Share the HTTP rotation between session restoration and API recovery. Consumers
// own state changes so an unmounted initializer cannot log out a newer session.
export function requestAccessToken(): Promise<string> {
  const { sessionVersion } = useAuthStore.getState()
  if (accessTokenRequest?.sessionVersion === sessionVersion) {
    return accessTokenRequest.promise
  }
  const promise = (async () => {
    const res = await fetch(`${BASE_URL}/api/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
    })
    if (!res.ok) throw new Error('refresh failed')
    const { access_token } = await res.json()
    currentSession(sessionVersion)
    return access_token
  })().finally(() => {
    if (accessTokenRequest?.promise === promise) accessTokenRequest = null
  })
  accessTokenRequest = { sessionVersion, promise }
  return promise
}

async function refreshToken(sessionVersion: number): Promise<string | null> {
  const { accessToken } = currentSession(sessionVersion)
  if (refreshRequest?.sessionVersion === sessionVersion) {
    return refreshRequest.promise
  }
  const promise = (async () => {
    try {
      const access_token = await requestAccessToken()
      const state = currentSession(sessionVersion)
      if (state.accessToken !== accessToken) return state.accessToken
      state.setTokens(access_token)
      return access_token
    } catch {
      const state = currentSession(sessionVersion)
      if (state.accessToken !== accessToken) return state.accessToken
      state.logout()
      if (typeof window !== 'undefined') {
        window.location.assign('/login')
      }
      return null
    }
  })().finally(() => {
    if (refreshRequest?.promise === promise) refreshRequest = null
  })
  refreshRequest = { sessionVersion, promise }
  return promise
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
  const { accessToken: token, sessionVersion } = useAuthStore.getState()
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
    const state = currentSession(sessionVersion)
    // A sibling may already have rotated this session while this response was pending.
    const newToken =
      state.accessToken !== token
        ? state.accessToken
        : await waitForRefresh(sessionVersion, options.signal)
    options.signal?.throwIfAborted()
    if (newToken) {
      currentSession(sessionVersion)
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

function waitForRefresh(
  sessionVersion: number,
  signal?: AbortSignal | null
): Promise<string | null> {
  signal?.throwIfAborted()
  const pending = refreshToken(sessionVersion)
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
