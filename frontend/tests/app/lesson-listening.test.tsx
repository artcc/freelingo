import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import LessonPage from '@/app/(app)/lesson/[id]/page'
import { useAuthStore, type User } from '@/store/auth'
import { useLanguageStore } from '@/store/language'
import { useConfigStore } from '@/store/config'
import { getLanguageByCode } from '@/lib/target-languages'

const mocks = vi.hoisted(() => ({ apiFetch: vi.fn(), lessonId: '1' }))
vi.mock('@/lib/api', () => ({ apiFetch: mocks.apiFetch }))
vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
  useLocale: () => 'en',
}))
vi.mock('next/navigation', () => ({
  useParams: () => ({ id: mocks.lessonId }),
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
  usePathname: () => `/lesson/${mocks.lessonId}`,
  useSearchParams: () => new URLSearchParams(),
}))
vi.mock('@/data/grammar', () => ({ getGrammarTopics: async () => [] }))
vi.mock('@/components/lesson/LessonVoicePracticeButton', () => ({
  LessonVoicePracticeButton: () => null,
}))

const user = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  conversation_max_duration: 300,
  conversation_inactivity_timeout: 30,
} satisfies User

function exercise(overrides: Record<string, unknown> = {}) {
  return {
    id: 10,
    exercise_type: 'listening',
    question: 'Quand le train arrive-t-il ?',
    options: ['À midi', 'À minuit'],
    correct_answer: 'À midi',
    listening_text: 'Le train arrive à midi.',
    listening_ready: true,
    score: null,
    user_answer: null,
    feedback: null,
    explanation: null,
    corrections: null,
    native_explanation: null,
    native_hint: null,
    ...overrides,
  }
}

function detail(items = [exercise()], completed = false) {
  return {
    lesson: {
      id: Number(mocks.lessonId),
      study_plan_id: 42,
      title: 'Le voyage',
      lesson_type: 'listening',
      cefr_level: 'B1',
      content: {},
      is_completed: completed,
    },
    exercises: items,
    target_language: 'fr-FR',
  }
}

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status })

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>((done) => {
    resolve = done
  })
  return { promise, resolve }
}

class FakeAudio extends EventTarget {
  currentTime = 0
  duration = 60
  play = vi.fn(async () => {})
  pause = vi.fn()
  load = vi.fn()
  removeAttribute = vi.fn()
}

let saved: ReturnType<typeof detail>
let audios: FakeAudio[]

function request(url: string) {
  if (url === `/api/lessons/${mocks.lessonId}`)
    return Promise.resolve(json(saved))
  if (url === '/api/study-plan/today')
    return Promise.resolve(json({ progress_day: 0 }))
  if (url === '/api/tts')
    return Promise.resolve(new Response(new Blob(['audio'])))
  if (url.endsWith('/answer'))
    return Promise.resolve(json({ score: 1, feedback: 'Bravo !' }))
  return Promise.resolve(json({}))
}

async function openLesson() {
  let view!: ReturnType<typeof render>
  await act(async () => {
    view = render(<LessonPage />)
  })
  return view
}

async function click(name: string) {
  await act(async () => {
    fireEvent.click(screen.getByRole('button', { name }))
  })
}

beforeEach(() => {
  mocks.lessonId = '1'
  saved = detail()
  audios = []
  mocks.apiFetch.mockReset().mockImplementation(request)
  useAuthStore.setState({ user, sessionVersion: 1, accessToken: 'token' })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB') ?? null,
  })
  useConfigStore.setState({ stripeEnabled: false })
  localStorage.removeItem('tts_voice')
  vi.stubGlobal(
    'Audio',
    vi.fn(function () {
      const audio = new FakeAudio()
      audios.push(audio)
      return audio
    })
  )
  vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:lesson')
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
})

afterEach(() => {
  cleanup()
  useAuthStore.setState(useAuthStore.getInitialState(), true)
  useLanguageStore.setState(useLanguageStore.getInitialState(), true)
  useConfigStore.setState(useConfigStore.getInitialState(), true)
  vi.unstubAllGlobals()
})

describe('Lesson listening exercises', () => {
  it('plays plan-owned audio, submits a choice and reveals the transcript in the persisted language', async () => {
    await openLesson()
    expect(screen.getAllByText('lessonTypes.listening')).toHaveLength(2)
    expect(useLanguageStore.getState().activeLanguage?.code).toBe('en-GB')
    expect(screen.getByText('Quand le train arrive-t-il ?')).toHaveAttribute(
      'lang',
      'fr-FR'
    )
    expect(screen.getByText('À midi')).toHaveAttribute('lang', 'fr-FR')
    expect(screen.getByText('À minuit')).toHaveAttribute('lang', 'fr-FR')
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
    expect(
      screen.queryByText('Le train arrive à midi.')
    ).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'submitAnswer' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'À midi' })).toHaveAttribute(
      'aria-pressed',
      'false'
    )
    await click('listen')
    expect(mocks.apiFetch).toHaveBeenCalledWith(
      '/api/tts',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          text: 'Le train arrive à midi.',
          study_plan_id: 42,
        }),
      })
    )
    await click('À midi')
    expect(screen.getByRole('button', { name: 'À midi' })).toHaveAttribute(
      'aria-pressed',
      'true'
    )
    expect(screen.getByRole('button', { name: 'À minuit' })).toHaveAttribute(
      'aria-pressed',
      'false'
    )
    await click('submitAnswer')
    expect(mocks.apiFetch).toHaveBeenCalledWith(
      '/api/lessons/exercises/10/answer',
      expect.objectContaining({
        body: JSON.stringify({ answer: 'À midi' }),
      })
    )
    expect(screen.getByText('Le train arrive à midi.')).toHaveAttribute(
      'lang',
      'fr-FR'
    )
    expect(screen.getByText('100%')).toBeVisible()
    expect(screen.getByRole('button', { name: /À midi/ })).toBeDisabled()
  })

  it.each([409, 422, 503])(
    'does not invent a score or reveal the transcript after HTTP %s',
    async (status) => {
      mocks.apiFetch.mockImplementation((url: string) =>
        url.endsWith('/answer')
          ? Promise.resolve(json({ detail: 'Rejected answer' }, status))
          : request(url)
      )
      await openLesson()
      await click('À midi')
      await click('submitAnswer')
      expect(screen.getByText('title')).toBeVisible()
      expect(screen.queryByText(/\d+%/)).not.toBeInTheDocument()
      expect(
        screen.queryByText('Le train arrive à midi.')
      ).not.toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'submitAnswer' })).toBeEnabled()
      expect(
        screen.getByRole('button', { name: 'regenerateExercise' })
      ).toBeEnabled()
      expect(screen.getByRole('button', { name: 'À minuit' })).toBeEnabled()
    }
  )

  it('accepts a valid 5000-character source containing a supplementary Unicode character', async () => {
    const text = `${'字'.repeat(4999)}𠀀`
    saved = detail([exercise({ listening_text: text })])
    await openLesson()
    expect(screen.queryByText('listeningIncomplete')).not.toBeInTheDocument()
    await click('listen')
    expect(mocks.apiFetch).toHaveBeenCalledWith(
      '/api/tts',
      expect.objectContaining({
        body: JSON.stringify({ text, study_plan_id: 42 }),
      })
    )
    await click('À midi')
    await click('submitAnswer')
    expect(screen.getByText('100%')).toBeVisible()
  })

  it('locks choices, submit and regeneration while an answer is pending', async () => {
    const pending = deferred<Response>()
    mocks.apiFetch.mockImplementation((url: string) =>
      url.endsWith('/answer') ? pending.promise : request(url)
    )
    await openLesson()
    await click('À midi')
    await click('submitAnswer')
    expect(screen.getByRole('button', { name: 'checking' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'À minuit' })).toBeDisabled()
    expect(
      screen.getByRole('button', { name: 'regenerateExercise' })
    ).toBeDisabled()
    await act(async () =>
      pending.resolve(json({ score: 1, feedback: 'Bravo !' }))
    )
    expect(screen.getByText('100%')).toBeVisible()
  })

  it.each([
    ['not ready', { listening_ready: false }],
    ['missing text', { listening_text: null }],
    ['blank text', { listening_text: ' ' }],
    ['oversized text', { listening_text: 'x'.repeat(5001) }],
    ['missing options', { options: null }],
    ['one option', { options: ['À midi'] }],
    ['invalid answer', { correct_answer: 'Unknown' }],
  ] as const)(
    'blocks %s without falling back to text input',
    async (_reason, overrides) => {
      saved = detail([exercise(overrides)])
      await openLesson()
      expect(screen.getByText('listeningIncomplete')).toBeVisible()
      expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'listen' })
      ).not.toBeInTheDocument()
      expect(
        screen.getByRole('button', { name: 'submitAnswer' })
      ).toBeDisabled()
      expect(
        screen.getByRole('button', { name: 'regenerateExercise' })
      ).toBeEnabled()
      expect(
        screen.queryByRole('button', { name: 'À midi' })
      ).not.toBeInTheDocument()
      expect(
        mocks.apiFetch.mock.calls.some(([url]) => url.endsWith('/answer'))
      ).toBe(false)
    }
  )

  it('regenerates legacy data in place and reloads the saved audio and choices', async () => {
    saved = detail([
      exercise({ listening_ready: false, listening_text: null, options: null }),
    ])
    const pending = deferred<Response>()
    mocks.apiFetch.mockImplementation((url: string) =>
      url.endsWith('/regenerate') ? pending.promise : request(url)
    )
    const view = await openLesson()
    await click('regenerateExercise')
    expect(
      screen.getByRole('button', { name: 'regeneratingExercise' })
    ).toBeDisabled()
    expect(screen.getByRole('button', { name: 'submitAnswer' })).toBeDisabled()
    saved = detail()
    await act(async () => pending.resolve(json(saved.exercises[0])))
    expect(screen.queryByText('listeningIncomplete')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'À midi' })).toBeEnabled()
    await click('listen')
    view.unmount()
    expect(audios[0].pause).toHaveBeenCalled()
    await openLesson()
    expect(screen.getByRole('button', { name: 'listen' })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'À midi' })).toBeEnabled()
    expect(
      mocks.apiFetch.mock.calls.filter(([url]) => url.endsWith('/regenerate'))
    ).toHaveLength(1)
  })

  it('recovers legacy listening with malformed options without rendering invalid React children', async () => {
    saved = detail([
      exercise({
        listening_ready: false,
        options: [{ text: 'Invalid option' }, null, 'À midi'],
      }),
    ])
    mocks.apiFetch.mockImplementation((url: string) =>
      url.endsWith('/regenerate')
        ? Promise.resolve(json(exercise()))
        : request(url)
    )
    await openLesson()
    expect(screen.getByText('listeningIncomplete')).toBeVisible()
    expect(
      screen.queryByRole('button', { name: 'À midi' })
    ).not.toBeInTheDocument()
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'submitAnswer' })).toBeDisabled()
    await click('regenerateExercise')
    expect(screen.queryByText('listeningIncomplete')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'À midi' })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'listen' })).toBeEnabled()
    await click('À midi')
    await click('submitAnswer')
    expect(screen.getByText('100%')).toBeVisible()
  })

  it('stops playback during regeneration and uses replacement text even with the same exercise id', async () => {
    const pending = deferred<Response>()
    mocks.apiFetch.mockImplementation((url: string) =>
      url.endsWith('/regenerate') ? pending.promise : request(url)
    )
    await openLesson()
    await click('listen')
    await click('regenerateExercise')
    expect(audios[0].pause).toHaveBeenCalled()
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:lesson')
    expect(
      screen.queryByRole('button', { name: 'listen' })
    ).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'À midi' })).toBeDisabled()
    await act(async () =>
      pending.resolve(
        json(exercise({ listening_text: 'Le train arrive demain.' }))
      )
    )
    await click('listen')
    expect(mocks.apiFetch).toHaveBeenLastCalledWith(
      '/api/tts',
      expect.objectContaining({
        body: JSON.stringify({
          text: 'Le train arrive demain.',
          study_plan_id: 42,
        }),
      })
    )
  })

  it('keeps incomplete data blocked after regeneration fails and permits a manual retry', async () => {
    saved = detail([exercise({ listening_ready: false, listening_text: null })])
    let attempts = 0
    mocks.apiFetch.mockImplementation((url: string) => {
      if (!url.endsWith('/regenerate')) return request(url)
      attempts += 1
      return Promise.resolve(attempts === 1 ? json({}, 503) : json(exercise()))
    })
    await openLesson()
    await click('regenerateExercise')
    expect(screen.getByText('regenerateError')).toBeVisible()
    expect(screen.getByRole('button', { name: 'submitAnswer' })).toBeDisabled()
    expect(
      screen.queryByRole('button', { name: 'À midi' })
    ).not.toBeInTheDocument()
    await click('regenerateExercise')
    expect(screen.queryByText('regenerateError')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'listen' })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'À midi' })).toBeEnabled()
  })

  it('keeps a completed legacy exercise read-only and preserves its answer and score', async () => {
    saved = detail(
      [
        exercise({
          listening_text: null,
          listening_ready: false,
          options: [{ text: 'Invalid option' }, null],
          score: 0.5,
          user_answer: 'Old answer',
        }),
      ],
      true
    )
    await openLesson()
    expect(screen.getByText('listeningUnavailable')).toBeVisible()
    expect(screen.getByText('Old answer')).toBeVisible()
    expect(screen.getByText('50%')).toBeVisible()
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
    expect(
      screen.queryByRole('button', { name: 'regenerateExercise' })
    ).not.toBeInTheDocument()
    expect(
      screen.queryByRole('button', { name: 'submitAnswer' })
    ).not.toBeInTheDocument()
  })

  it('reveals saved transcripts in review and cancels audio when advancing', async () => {
    saved = detail(
      [
        exercise({ score: 1, user_answer: 'À midi' }),
        exercise({
          id: 11,
          question: 'Deuxième question',
          listening_text: 'Un autre voyage.',
        }),
      ],
      true
    )
    await openLesson()
    expect(screen.getByText('Le train arrive à midi.')).toBeVisible()
    await click('listen')
    await click('next →')
    expect(audios[0].pause).toHaveBeenCalled()
    expect(screen.getByText('Un autre voyage.')).toHaveAttribute(
      'lang',
      'fr-FR'
    )
    expect(
      screen.queryByText('Le train arrive à midi.')
    ).not.toBeInTheDocument()
  })

  describe.each(['answer', 'regenerate'] as const)(
    'pending %s',
    (operation) => {
      it.each(['resource', 'session'] as const)(
        'ignores obsolete results after %s replacement',
        async (change) => {
          const pending = deferred<Response>()
          const url = `/api/lessons/exercises/10/${operation}`
          mocks.apiFetch.mockImplementation((requested: string) =>
            requested === url ? pending.promise : request(requested)
          )
          const view = await openLesson()
          if (operation === 'answer') await click('À midi')
          await click(
            operation === 'answer' ? 'submitAnswer' : 'regenerateExercise'
          )
          const signal = mocks.apiFetch.mock.calls.find(
            ([requested]) => requested === url
          )![1].signal as AbortSignal
          saved = detail([
            exercise({
              id: 20,
              question: 'Nouvelle question',
              listening_text: 'Un nouveau texte.',
            }),
          ])
          await act(async () => {
            if (change === 'resource') {
              mocks.lessonId = '2'
              view.rerender(<LessonPage />)
            } else useAuthStore.getState().startSession('replacement')
          })
          expect(signal.aborted).toBe(true)
          await act(async () =>
            pending.resolve(
              json(
                operation === 'answer'
                  ? { score: 1, feedback: 'Stale feedback' }
                  : exercise({ question: 'Stale question' })
              )
            )
          )
          expect(screen.getByText('Nouvelle question')).toBeVisible()
          expect(screen.queryByText('Stale feedback')).not.toBeInTheDocument()
          expect(screen.queryByText('Stale question')).not.toBeInTheDocument()
          expect(
            screen.queryByText('Un nouveau texte.')
          ).not.toBeInTheDocument()
          expect(
            screen.getByRole('button', { name: 'regenerateExercise' })
          ).toBeEnabled()
          expect(screen.getByRole('button', { name: 'À midi' })).toBeEnabled()
        }
      )
    }
  )

  it('discards an obsolete lesson load after navigation', async () => {
    const pending = deferred<Response>()
    const oldDetail = saved
    mocks.apiFetch.mockImplementation((url: string) =>
      url === '/api/lessons/1' ? pending.promise : request(url)
    )
    const view = await openLesson()
    const signal = mocks.apiFetch.mock.calls.find(
      ([url]) => url === '/api/lessons/1'
    )![1].signal as AbortSignal
    mocks.lessonId = '2'
    saved = detail([exercise({ id: 20, question: 'Nouvelle question' })])
    await act(async () => view.rerender(<LessonPage />))
    expect(signal.aborted).toBe(true)
    await act(async () => pending.resolve(json(oldDetail)))
    expect(screen.getByText('Nouvelle question')).toBeVisible()
    expect(
      screen.queryByText('Quand le train arrive-t-il ?')
    ).not.toBeInTheDocument()
  })
})

describe('Lesson pronunciation operation exclusion', () => {
  it.each(['recording', 'transcribing'] as const)(
    'preserves the spoken answer when regeneration is requested while %s',
    async (stage) => {
      saved = detail([
        exercise({
          exercise_type: 'pronunciation',
          question: 'Dites bonjour.',
          correct_answer: 'Bonjour',
          options: [],
        }),
      ])
      const stt = deferred<Response>()
      const regeneration = deferred<Response>()
      const stop = vi.fn()
      const processor = {
        connect: vi.fn(),
        disconnect: vi.fn(),
        onaudioprocess: null as
          | ((event: {
              inputBuffer: { getChannelData: () => Float32Array }
            }) => void)
          | null,
      }
      vi.stubGlobal('navigator', {
        mediaDevices: {
          getUserMedia: vi.fn(async () => ({
            getTracks: () => [{ stop }],
          })),
        },
      })
      vi.stubGlobal(
        'AudioContext',
        vi.fn(function () {
          return {
            sampleRate: 16000,
            destination: {},
            createMediaStreamSource: () => ({ connect: vi.fn() }),
            createScriptProcessor: () => processor,
            close: vi.fn(async () => {}),
          }
        })
      )
      mocks.apiFetch.mockImplementation((url: string) => {
        if (url === '/api/stt') return stt.promise
        if (url.endsWith('/regenerate')) return regeneration.promise
        return request(url)
      })

      await openLesson()
      await click('ariaRecord')
      processor.onaudioprocess!({
        inputBuffer: { getChannelData: () => new Float32Array([0.5, 0.2]) },
      })
      if (stage === 'transcribing') await click('ariaStop')
      await click('regenerateExercise')
      if (stage === 'recording') await click('ariaStop')
      await act(async () => stt.resolve(json({ text: 'Bonjour' })))
      await act(async () => regeneration.resolve(json({}, 400)))

      expect(mocks.apiFetch).toHaveBeenCalledWith(
        '/api/lessons/exercises/10/answer',
        expect.objectContaining({
          body: JSON.stringify({ answer: 'Bonjour' }),
        })
      )
      expect(stop).toHaveBeenCalledOnce()
      expect(
        mocks.apiFetch.mock.calls.some(([url]) => url.endsWith('/regenerate'))
      ).toBe(false)
      expect(screen.getByText('100%')).toBeVisible()
    }
  )
})
