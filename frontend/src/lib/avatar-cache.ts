import { useAuthStore } from '@/store/auth'
import { requestAccessToken } from '@/lib/api'

type Subscriber = (src: string | null) => void

let cacheKey: string | null = null
let objectUrl: string | null = null
let pending: Promise<string | null> | null = null
const subscribers = new Set<Subscriber>()

function notify() {
  for (const subscriber of subscribers) {
    subscriber(objectUrl)
  }
}

function resetObjectUrl() {
  if (objectUrl?.startsWith('blob:')) URL.revokeObjectURL(objectUrl)
  objectUrl = null
}

export function subscribeAvatar(subscriber: Subscriber) {
  subscribers.add(subscriber)
  subscriber(objectUrl)
  return () => {
    subscribers.delete(subscriber)
  }
}

export function clearAvatarCache() {
  cacheKey = null
  pending = null
  resetObjectUrl()
  notify()
}

export function loadAvatar(avatar: string, accessToken: string | null) {
  const { sessionVersion } = useAuthStore.getState()
  const sameSession = () =>
    useAuthStore.getState().sessionVersion === sessionVersion
  const key = `${sessionVersion}:${avatar}:${accessToken ?? ''}`
  if (cacheKey === key && objectUrl) return Promise.resolve(objectUrl)
  if (cacheKey === key && pending) return pending

  cacheKey = key
  resetObjectUrl()
  notify()

  if (avatar.startsWith('data:image/')) {
    objectUrl = avatar
    notify()
    return Promise.resolve(objectUrl)
  }

  const fetchAvatar = (token: string | null) =>
    fetch('/api/auth/me/avatar-file', {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      credentials: 'include',
    })

  const request = fetchAvatar(accessToken)
    .then(async (res) => {
      if (!sameSession()) return null
      if (res.status === 401 && accessToken) {
        const currentToken = useAuthStore.getState().accessToken
        const token =
          currentToken !== accessToken
            ? currentToken
            : await requestAccessToken()
        if (!sameSession()) return null
        const state = useAuthStore.getState()
        // Another consumer may have published this shared rotation already.
        const nextToken =
          state.accessToken !== accessToken ? state.accessToken : token
        if (!nextToken) return null
        if (state.accessToken === accessToken) state.setTokens(nextToken)
        res = await fetchAvatar(nextToken)
      }
      if (!res.ok) return null
      const blob = await res.blob()
      if (!sameSession() || cacheKey !== key) return null
      objectUrl = URL.createObjectURL(blob)
      notify()
      return objectUrl
    })
    .catch(() => null)
    .finally(() => {
      if (pending === request) pending = null
    })

  pending = request
  return request
}
