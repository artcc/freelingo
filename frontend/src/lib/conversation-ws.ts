/**
 * Builds the WebSocket URL for the /ws/conversation endpoint.
 *
 * The backend WebSocket route is NOT covered by Next.js rewrites (which only
 * handle HTTP). The browser connects directly to the backend using
 * NEXT_PUBLIC_API_URL.
 *
 * Rules:
 *  - If NEXT_PUBLIC_API_URL is set (e.g. "https://api.example.com"), replace
 *    the http(s) scheme with ws(s) and append the path.
 *  - If NEXT_PUBLIC_API_URL is empty (same-origin / Traefik fronting both),
 *    derive the WS base from window.location.
 */
export function buildConversationWsUrl(): string {
  const base = (process.env.NEXT_PUBLIC_API_URL ?? '')
    .trim()
    .replace(/\/+$/, '')

  let wsBase: string
  if (base) {
    // e.g. "https://api.example.com" → "wss://api.example.com"
    wsBase = base.replace(/^http/, 'ws')
  } else {
    // Same origin — derive from window.location
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    wsBase = `${proto}//${window.location.host}`
  }

  return `${wsBase}/ws/conversation`
}

// ─── Incoming WS message types ───────────────────────────────────────────────

export interface TranscriptMessage {
  type: 'transcript'
  role: 'user' | 'assistant'
  text: string
  final: boolean
  turn_id?: number
}

export interface BargeInMessage {
  type: 'barge_in'
  turn_id?: number
}

export interface SessionWarningMessage {
  type: 'session_warning'
  reason: 'max_duration' | 'inactivity'
  remaining_seconds: number
  turn_id?: number
}

export interface SessionEndMessage {
  type: 'session_end'
  reason: 'max_duration' | 'inactivity'
  turn_id?: number
}

export interface StatusMessage {
  type: 'status'
  value: 'transcribing' | 'thinking' | 'speaking' | 'listening'
  turn_id?: number
}

export interface ErrorMessage {
  type: 'error'
  code: string
  message?: string
  reason?: 'freemium_exhausted' | 'freemium_unavailable'
  feature?: 'voice'
  remaining?: number
  limit?: number
  turn_id?: number
}

export interface MemoryUpdatedMessage {
  type: 'memory_updated'
  turn_id?: number
}

export interface TurnCompleteMessage {
  type: 'turn_complete'
  turn_id?: number
}

export type WsMessage =
  | TranscriptMessage
  | BargeInMessage
  | SessionWarningMessage
  | SessionEndMessage
  | StatusMessage
  | ErrorMessage
  | MemoryUpdatedMessage
  | TurnCompleteMessage

// ─── Chat context passed from tutor chat to voice session ────────────────────

export interface ChatContextItem {
  role: 'user' | 'assistant'
  content: string
}
