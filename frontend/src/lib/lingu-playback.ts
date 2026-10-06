import { LoopOnce, LoopRepeat, type AnimationAction } from 'three'
import { LINGU_ANIMATIONS, type LinguAnimation } from './lingu'

const FADE_SECONDS = 0.25

export function createLinguPlayback(actions: Map<string, AnimationAction>) {
  let active: AnimationAction | undefined
  let elapsed = 0
  let transition: { action: AnimationAction; from: number; to: number }[] = []

  return {
    play(name: LinguAnimation, loopOverride?: boolean) {
      const next = actions.get(name)
      const repeat = loopOverride ?? LINGU_ANIMATIONS[name] === 'repeat'
      const mode = repeat ? LoopRepeat : LoopOnce
      if (!next || (active === next && next.loop === mode)) return

      const weight = next.isScheduled() ? next.getEffectiveWeight() : 0
      if (weight === 0) {
        next.reset()
      } else if (next.paused || next.loop !== mode) {
        // Resume completed actions and reset loop bookkeeping without changing the pose.
        const time = next.time
        next.reset()
        next.time = time
      }
      next.setLoop(mode, repeat ? Infinity : 1)
      next.clampWhenFinished = !repeat
      next.setEffectiveWeight(weight).setEffectiveTimeScale(1).play()

      // Include every contributing action, even those already fading out.
      transition = [...actions.values()]
        .filter((action) => action.isScheduled())
        .map((action) => ({
          action,
          from: action.getEffectiveWeight(),
          to: action === next ? 1 : 0,
        }))
      elapsed = 0
      active = next
    },

    update(delta: number) {
      if (!transition.length) return
      elapsed += delta
      const progress = Math.min(elapsed / FADE_SECONDS, 1)
      for (const { action, from, to } of transition) {
        action.setEffectiveWeight(from + (to - from) * progress)
        if (progress === 1 && to === 0) action.stop()
      }
      if (progress === 1) transition = []
    },

    isActive(action: AnimationAction) {
      return action === active
    },
  }
}
