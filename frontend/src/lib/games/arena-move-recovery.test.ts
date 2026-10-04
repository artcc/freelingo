import { describe, expect, it, vi } from 'vitest'
import { submitArenaMove } from './arena-move-recovery'

const move = { action_id: 'same-action', version: 2 }
const state = { session_id: 'round-1', version: 3 }

describe('arena move recovery', () => {
  it('accepts a server response without an extra read', async () => {
    const read = vi.fn()
    expect(await submitArenaMove('round-1', move, async () => state, read)).toEqual(state)
    expect(read).not.toHaveBeenCalled()
  })
  it('recovers an advanced server state after a lost response', async () => {
    expect(await submitArenaMove('round-1', move, async () => { throw Error('network') }, async () => state)).toEqual(state)
  })
  it('does not treat an unchanged version as committed', async () => {
    await expect(submitArenaMove('round-1', move, async () => { throw Error('network') }, async () => ({ ...state, version: 2 }))).rejects.toThrow('network')
  })
  it('does not accept a different session', async () => {
    await expect(submitArenaMove('round-1', move, async () => { throw Error('network') }, async () => ({ ...state, session_id: 'other' }))).rejects.toThrow('network')
  })
  it('does not recover rejected or aborted actions', async () => {
    for (const error of [Object.assign(Error('rejected'), { permanent: true }), Object.assign(Error('aborted'), { name: 'AbortError' })]) {
      const read = vi.fn()
      await expect(submitArenaMove('round-1', move, async () => { throw error }, read)).rejects.toBe(error)
      expect(read).not.toHaveBeenCalled()
    }
  })
  it('preserves the exact payload for an explicit transient retry', async () => {
    const error = Object.assign(Error('temporary'), { name: 'ArenaRequestError' })
    const send = vi.fn().mockRejectedValueOnce(error).mockResolvedValueOnce(state)
    const read = vi.fn()
    await expect(submitArenaMove('round-1', move, send, read)).rejects.toBe(error)
    expect(await submitArenaMove('round-1', move, send, read)).toEqual(state)
    expect(send.mock.calls[0][1]).toBe(send.mock.calls[1][1])
    expect(read).not.toHaveBeenCalled()
  })
  it('propagates expiry during recovery', async () => {
    const expired = Object.assign(Error('expired'), { terminal: true })
    await expect(submitArenaMove('round-1', move, async () => { throw Error('network') }, async () => { throw expired })).rejects.toBe(expired)
  })
})
