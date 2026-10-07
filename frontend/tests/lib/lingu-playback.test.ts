import { describe, expect, it, vi } from 'vitest'
import {
  AnimationClip,
  AnimationMixer,
  NumberKeyframeTrack,
  Object3D,
} from 'three'
import { createLinguPlayback } from '@/lib/lingu-playback'

function setup() {
  const model = new Object3D()
  const mixer = new AnimationMixer(model)
  const actions = new Map(
    ['hablando', 'reposo', 'saludo'].map((name, index) => [
      name,
      mixer.clipAction(
        new AnimationClip(name, 2, [
          new NumberKeyframeTrack(
            '.position[x]',
            [0, 1, 2],
            [index * 10, index * 10 + 4, index * 10]
          ),
        ])
      ),
    ])
  )
  const playback = createLinguPlayback(actions)
  const advance = (delta: number) => {
    playback.update(delta)
    mixer.update(delta)
  }
  return { model, mixer, actions, playback, advance }
}

describe('Lingu playback transitions', () => {
  it('preserves the pose and clip times when reversing an unfinished fade', () => {
    const { model, actions, playback, advance } = setup()
    playback.play('hablando')
    advance(0.25)
    playback.play('reposo')
    advance(0.05)

    const position = model.position.x
    const times = [...actions.values()].map((action) => action.time)
    const weights = [...actions.values()].map((action) =>
      action.getEffectiveWeight()
    )
    playback.play('hablando')
    advance(0)

    expect(model.position.x).toBeCloseTo(position, 10)
    expect([...actions.values()].map((action) => action.time)).toEqual(times)
    expect(
      [...actions.values()].map((action) => action.getEffectiveWeight())
    ).toEqual(weights)

    advance(0.25)
    expect(actions.get('hablando')!.getEffectiveWeight()).toBe(1)
    expect(actions.get('reposo')!.isScheduled()).toBe(false)
    const time = actions.get('hablando')!.time
    expect(model.position.x).toBeCloseTo(time * 4)
  })

  it('preserves all contributing poses when a third animation interrupts the fade', () => {
    const { model, actions, playback, advance } = setup()
    playback.play('hablando')
    advance(0.25)
    playback.play('reposo')
    advance(0.05)
    const position = model.position.x

    playback.play('saludo')
    advance(0)
    expect(model.position.x).toBeCloseTo(position, 10)
    advance(0.05)
    const blendedPosition = model.position.x
    playback.play('reposo')
    advance(0)
    expect(model.position.x).toBeCloseTo(blendedPosition, 10)

    advance(0.25)
    expect(actions.get('hablando')!.isScheduled()).toBe(false)
    expect(actions.get('saludo')!.isScheduled()).toBe(false)
    expect(actions.get('reposo')!.getEffectiveWeight()).toBe(1)
  })

  it('keeps looping overrides and one-shot completion after transitions', () => {
    const { mixer, playback, advance } = setup()
    const finished = vi.fn()
    mixer.addEventListener('finished', (event) => {
      if (playback.isActive(event.action)) finished()
    })
    playback.play('saludo', true)
    advance(0.25)
    advance(4)
    expect(finished).not.toHaveBeenCalled()

    playback.play('reposo')
    advance(0.25)
    playback.play('saludo')
    advance(0.25)
    advance(2)
    expect(finished).toHaveBeenCalledTimes(1)
    advance(2)
    expect(finished).toHaveBeenCalledTimes(1)
  })

  it('notifies completion when reactivating a one-shot that finished while fading out', () => {
    const { model, mixer, actions, playback, advance } = setup()
    const finished = vi.fn()
    mixer.addEventListener('finished', (event) => {
      if (playback.isActive(event.action)) finished()
    })

    playback.play('saludo')
    advance(1.98)
    playback.play('hablando')
    advance(0.04)

    expect(actions.get('saludo')!.paused).toBe(true)
    expect(finished).not.toHaveBeenCalled()
    const position = model.position.x
    const times = [...actions.values()].map((action) => action.time)
    const weights = [...actions.values()].map((action) =>
      action.getEffectiveWeight()
    )

    playback.play('saludo')
    advance(0)
    expect(model.position.x).toBeCloseTo(position, 10)
    expect([...actions.values()].map((action) => action.time)).toEqual(times)
    expect(
      [...actions.values()].map((action) => action.getEffectiveWeight())
    ).toEqual(weights)
    expect(finished).not.toHaveBeenCalled()

    advance(0.01)
    expect(finished).toHaveBeenCalledTimes(1)
    playback.play('saludo')
    advance(0.25)
    advance(0.25)
    expect(finished).toHaveBeenCalledTimes(1)
    expect(actions.get('saludo')!.getEffectiveWeight()).toBe(1)
    expect(actions.get('hablando')!.isScheduled()).toBe(false)
  })

  it('preserves the current pose when changing the loop mode of an active clip', () => {
    const { model, actions, playback, advance } = setup()
    playback.play('saludo')
    advance(0.4)
    const position = model.position.x
    const time = actions.get('saludo')!.time

    playback.play('saludo', true)
    advance(0)
    expect(model.position.x).toBeCloseTo(position, 10)
    expect(actions.get('saludo')!.time).toBe(time)
    advance(3)
    expect(actions.get('saludo')!.isRunning()).toBe(true)
  })
})
