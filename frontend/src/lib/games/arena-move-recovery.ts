/** A lost response must not become a new action. Only server state proves success. */
export interface VersionedMove { action_id: string; version: number }
export interface VersionedState { session_id: string; version: number }
export interface ArenaFailure extends Error { permanent?: boolean; terminal?: boolean }

export async function submitArenaMove<S extends VersionedState, M extends VersionedMove>(
  sessionId: string,
  move: M,
  send: (id: string, payload: M) => Promise<S>,
  read: (id: string) => Promise<S>,
): Promise<S> {
  try {
    return await send(sessionId, move)
  } catch (error) {
    const failure = error as ArenaFailure
    if (failure?.name === 'AbortError' || failure?.permanent || failure?.terminal) throw error
    // A structured HTTP error remains retryable using the original action ID.
    if (failure?.name === 'ArenaRequestError') throw error
    try {
      const recovered = await read(sessionId)
      // Same version does not establish that this move was committed.
      if (recovered.session_id === sessionId && recovered.version > move.version) return recovered
    } catch (readError) {
      const readFailure = readError as ArenaFailure
      if (readFailure?.terminal || readFailure?.name === 'AbortError') throw readError
    }
    throw error
  }
}
