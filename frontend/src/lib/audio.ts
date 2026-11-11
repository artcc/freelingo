import { getLogger, silentLogger } from '@/lib/logger'

/**
 * Encodes a Float32Array of mono PCM samples into a standard WAV ArrayBuffer.
 * VAD delivers samples at 16 000 Hz; STT service accepts audio/wav.
 */
export function float32ToWav(
  samples: Float32Array,
  sampleRate: number
): ArrayBuffer {
  const numChannels = 1
  const bitsPerSample = 16
  const blockAlign = numChannels * (bitsPerSample / 8)
  const byteRate = sampleRate * blockAlign
  const dataSize = samples.length * blockAlign
  const buffer = new ArrayBuffer(44 + dataSize)
  const view = new DataView(buffer)

  function writeStr(offset: number, s: string) {
    for (let i = 0; i < s.length; i++)
      view.setUint8(offset + i, s.charCodeAt(i))
  }

  writeStr(0, 'RIFF')
  view.setUint32(4, 36 + dataSize, true)
  writeStr(8, 'WAVE')
  writeStr(12, 'fmt ')
  view.setUint32(16, 16, true) // PCM chunk size
  view.setUint16(20, 1, true) // PCM format
  view.setUint16(22, numChannels, true)
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, byteRate, true)
  view.setUint16(32, blockAlign, true)
  view.setUint16(34, bitsPerSample, true)
  writeStr(36, 'data')
  view.setUint32(40, dataSize, true)

  let offset = 44
  for (let i = 0; i < samples.length; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true)
    offset += 2
  }

  return buffer
}

export interface AudioQueue {
  enqueue: (arrayBuffer: ArrayBuffer) => Promise<void>
  cancel: () => void
}

const ENABLE_CONVERSATION_AUDIO_DEBUG_LOGS = false
const audioQueueLogger = ENABLE_CONVERSATION_AUDIO_DEBUG_LOGS
  ? getLogger('audio-queue')
  : silentLogger

/**
 * Creates a gapless audio playback queue backed by the Web Audio API.
 * Each ArrayBuffer is decoded (MP3/WAV/OGG accepted) and scheduled to play
 * immediately after the previous chunk, avoiding gaps between TTS segments.
 *
 * The AudioContext must be created during a user gesture to satisfy browser
 * autoplay policies.
 */
export function createAudioQueue(
  ctx: AudioContext,
  onIdle?: () => void
): AudioQueue {
  // nextTime tracks when the next chunk should start (in AudioContext time).
  // Using a closure variable (not module-level) so multiple instances are safe.
  let nextTime = 0
  let generation = 0
  const sources: AudioBufferSourceNode[] = []
  const fallbackAudios = new Map<HTMLAudioElement, () => void>()
  let resolveSourcesDrained: (() => void) | null = null
  const pendingChunks: ArrayBuffer[] = []
  let draining = false
  // Serialize decoding+scheduling so that chunks are always played in the
  // exact order they were enqueued, regardless of how long decodeAudioData
  // takes for each chunk. Without this, a short chunk 2 could decode faster
  // than chunk 1 and get scheduled first, causing out-of-order playback.
  let chain: Promise<void> = Promise.resolve()
  let lastDecodeFailTs = 0
  let lastScheduleFailTs = 0
  let chunkSeq = 0

  function notifyIdle(): void {
    if (
      !draining &&
      pendingChunks.length === 0 &&
      sources.length === 0 &&
      fallbackAudios.size === 0
    ) {
      onIdle?.()
    }
  }

  async function _decode(
    arrayBuffer: ArrayBuffer,
    generationToken: number,
    chunkId: number
  ): Promise<void> {
    if (generationToken !== generation) return
    if (ctx.state === 'closed') return

    if (ctx.state === 'suspended') {
      audioQueueLogger.warn('resuming suspended audio context', {
        chunkId,
        generationToken,
      })
      try {
        await ctx.resume()
        audioQueueLogger.warn('audio context resumed', {
          chunkId,
          state: ctx.state,
        })
      } catch {
        audioQueueLogger.error('audio context resume failed', {
          chunkId,
          state: ctx.state,
        })
        // Context may still be unusable in constrained browsers; fallback keeps us moving.
      }
    }

    let decoded: AudioBuffer
    try {
      decoded = await ctx.decodeAudioData(arrayBuffer.slice(0))
      audioQueueLogger.warn('decoded TTS chunk', {
        chunkId,
        bytes: arrayBuffer.byteLength,
        durationMs: Math.round(decoded.duration * 1000),
        sampleRate: decoded.sampleRate,
        channels: decoded.numberOfChannels,
      })
    } catch (error) {
      const now = Date.now()
      if (now - lastDecodeFailTs > 5000) {
        audioQueueLogger.warn('decode failed for TTS chunk', {
          chunkId,
          bytes: arrayBuffer.byteLength,
          error: error instanceof Error ? error.message : String(error),
        })
        lastDecodeFailTs = now
      }
      await _fallbackPlay(arrayBuffer.slice(0), generationToken, chunkId)
      return
    }

    if (generationToken !== generation) return

    let source: AudioBufferSourceNode
    try {
      source = ctx.createBufferSource()
      source.buffer = decoded
      source.connect(ctx.destination)
    } catch {
      return
    }

    const now = ctx.currentTime
    const startAt = Math.max(now + 0.005, nextTime)
    try {
      source.start(startAt)
      audioQueueLogger.warn('scheduled TTS chunk playback', {
        chunkId,
        startAt,
        now,
        nextTime,
        durationMs: Math.round(decoded.duration * 1000),
      })
    } catch (error) {
      const now = Date.now()
      if (now - lastScheduleFailTs > 5000) {
        audioQueueLogger.warn('failed to schedule TTS chunk playback', {
          chunkId,
          error: error instanceof Error ? error.message : String(error),
        })
        lastScheduleFailTs = now
      }
      return
    }

    if (generationToken !== generation) {
      try {
        source.stop(0)
      } catch {
        // ignore
      }
      return
    }
    nextTime = startAt + decoded.duration

    sources.push(source)
    source.onended = () => {
      if (generationToken !== generation) return
      const idx = sources.indexOf(source)
      if (idx !== -1) sources.splice(idx, 1)
      if (sources.length === 0) {
        resolveSourcesDrained?.()
        resolveSourcesDrained = null
      }
      audioQueueLogger.warn('TTS chunk playback ended', {
        chunkId,
        remainingSources: sources.length,
      })
      notifyIdle()
    }
  }

  async function _fallbackPlay(
    arrayBuffer: ArrayBuffer,
    generationToken: number,
    chunkId: number
  ): Promise<void> {
    if (generationToken !== generation) return

    // Decoding is serialized, but earlier Web Audio sources can still be playing.
    if (sources.length > 0) {
      await new Promise<void>((resolve) => {
        resolveSourcesDrained = resolve
      })
      if (generationToken !== generation) return
    }

    const header = new DataView(arrayBuffer)
    const isWav =
      header.byteLength >= 12 &&
      header.getUint32(0) === 0x52494646 && // RIFF
      header.getUint32(8) === 0x57415645 // WAVE
    const blob = new Blob([arrayBuffer], {
      type: isWav ? 'audio/wav' : 'audio/mpeg',
    })
    const url = URL.createObjectURL(blob)
    const audio = new Audio(url)
    audioQueueLogger.warn('using HTMLAudio fallback for TTS chunk', {
      chunkId,
      bytes: arrayBuffer.byteLength,
    })

    await new Promise<void>((resolve) => {
      let finished = false
      const done = () => {
        if (finished) return
        finished = true
        audio.removeEventListener('ended', done)
        audio.removeEventListener('error', done)
        URL.revokeObjectURL(url)
        fallbackAudios.delete(audio)
        if (generationToken === generation) notifyIdle()
        resolve()
      }

      fallbackAudios.set(audio, done)
      audio.addEventListener('ended', done)
      audio.addEventListener('error', done)
      void audio
        .play()
        .then(() => {
          audioQueueLogger.warn('HTMLAudio fallback playback started', {
            chunkId,
          })
        })
        .catch((error) => {
          audioQueueLogger.error('HTMLAudio fallback playback failed', {
            chunkId,
            error: error instanceof Error ? error.message : String(error),
          })
          done()
        })
    })
  }

  async function _drain(generationToken: number): Promise<void> {
    try {
      while (generationToken === generation && pendingChunks.length) {
        const nextChunk = pendingChunks.shift()
        if (!nextChunk) break
        const chunkId = ++chunkSeq
        audioQueueLogger.warn('draining queued TTS chunk', {
          chunkId,
          generationToken,
          pendingAfterShift: pendingChunks.length,
          bytes: nextChunk.byteLength,
          ctxState: ctx.state,
        })
        await _decode(nextChunk, generationToken, chunkId)
      }
    } finally {
      if (generationToken === generation && pendingChunks.length === 0) {
        draining = false
        notifyIdle()
      }
    }
  }

  function enqueue(arrayBuffer: ArrayBuffer): Promise<void> {
    const generationToken = generation
    pendingChunks.push(arrayBuffer)
    audioQueueLogger.warn('queued TTS chunk for playback', {
      generationToken,
      bytes: arrayBuffer.byteLength,
      queued: pendingChunks.length,
      draining,
      ctxState: ctx.state,
    })
    if (!draining) {
      draining = true
      chain = chain.then(() => _drain(generationToken)).catch(() => {})
    }
    return chain
  }

  function cancel(): void {
    generation += 1
    audioQueueLogger.warn('cancel called on audio queue', {
      generation,
      activeSources: sources.length,
      fallbackAudios: fallbackAudios.size,
      pendingChunks: pendingChunks.length,
    })
    if (pendingChunks.length) {
      audioQueueLogger.warn(
        'canceling playback and dropping queued TTS chunks',
        {
          chunks: pendingChunks.length,
        }
      )
    }
    pendingChunks.length = 0
    for (const s of sources) {
      try {
        s.stop(0)
      } catch {
        // already stopped — ignore
      }
    }
    for (const [audio, finish] of fallbackAudios) {
      try {
        audio.pause()
        audio.src = ''
      } catch {
        // ignore
      } finally {
        finish()
      }
    }
    sources.length = 0
    resolveSourcesDrained?.()
    resolveSourcesDrained = null
    nextTime = 0
    draining = false
    chain = Promise.resolve()
    notifyIdle()
  }

  return { enqueue, cancel }
}
