import { describe, expect, it } from 'vitest'
import { GAME_REGISTRY, getGameDefinition, isArenaGame } from './registry'

describe('game registry', () => {
  it('contains unique launchable games', () => {
    const ids = GAME_REGISTRY.map(game => game.id)
    expect(ids.length).toBe(10)
    expect(new Set(ids).size).toBe(ids.length)
    expect(GAME_REGISTRY.every(game => game.ar && game.en && game.arDesc && game.enDesc)).toBe(true)
  })

  it('keeps arena routing explicit', () => {
    expect(isArenaGame('memory')).toBe(true)
    expect(isArenaGame('matching')).toBe(true)
    expect(isArenaGame('sentence_builder')).toBe(false)
    expect(getGameDefinition('review_mix')?.category).toBe('review')
  })
})
