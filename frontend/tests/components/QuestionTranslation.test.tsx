import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { QuestionTranslation } from '@/components/lesson/QuestionTranslation'
import { useAuthStore, type User } from '@/store/auth'

const mockApiFetch = vi.hoisted(() => vi.fn())

vi.mock('@/lib/api', () => ({ apiFetch: mockApiFetch }))
vi.mock('next-intl', () => ({
  useTranslations: () => (key: string, values?: { language: string }) =>
    values ? `${key} ${values.language}` : key,
}))

const user = {
  id: 1,
  username: 'learner',
  displayName: 'Learner',
  role: 'user',
  native_language: 'es',
  conversation_max_duration: 300,
  conversation_inactivity_timeout: 30,
} satisfies User

const props = {
  exerciseId: 10,
  question: 'Describe your favourite place.',
  nativeLanguage: 'es',
  nativeLanguageName: 'Español',
}
const translatedQuestion = 'Describe tu lugar favorito.'

function translationResponse(overrides: Record<string, unknown> = {}) {
  return new Response(
    JSON.stringify({
      question: props.question,
      question_translation: translatedQuestion,
      question_translation_language: props.nativeLanguage,
      ...overrides,
    }),
    { status: 200 }
  )
}

function pendingResponse() {
  let resolve!: (response: Response) => void
  const promise = new Promise<Response>((resolvePromise) => {
    resolve = resolvePromise
  })
  return { promise, resolve }
}

function openTranslation() {
  fireEvent.click(
    screen.getByRole('button', { name: /^showQuestionTranslation / })
  )
}

function closeTranslation() {
  fireEvent.click(
    screen.getByRole('button', { name: 'hideQuestionTranslation' })
  )
}

describe('QuestionTranslation', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    useAuthStore.setState({ user, sessionVersion: 1 })
  })

  afterEach(() => {
    cleanup()
    useAuthStore.setState(useAuthStore.getInitialState(), true)
  })

  it('shows and hides a matching cached translation without requesting it', () => {
    render(
      <QuestionTranslation
        {...props}
        translation={`  ${translatedQuestion}  `}
        translationLanguage="es"
      />
    )

    const toggle = screen.getByRole('button', {
      name: 'showQuestionTranslation Español',
    })
    const content = document.getElementById(toggle.getAttribute('aria-controls')!)
    expect(toggle).toHaveAttribute('aria-expanded', 'false')
    expect(content).not.toBeVisible()

    openTranslation()

    expect(toggle).toHaveAttribute('aria-expanded', 'true')
    expect(content).toBeVisible()
    expect(screen.getByText(translatedQuestion)).toHaveAttribute('lang', 'es')
    expect(screen.getByText(translatedQuestion)).toHaveAttribute('dir', 'auto')

    closeTranslation()

    expect(toggle).toHaveAttribute('aria-expanded', 'false')
    expect(screen.getByText(translatedQuestion)).not.toBeVisible()
    expect(mockApiFetch).not.toHaveBeenCalled()
  })

  it.each([
    { name: 'absent', cache: {} },
    {
      name: 'in another language',
      cache: { translation: 'Ancienne traduction', translationLanguage: 'fr' },
    },
    {
      name: 'without a language',
      cache: { translation: 'Unverified translation' },
    },
    {
      name: 'empty',
      cache: { translation: '  ', translationLanguage: 'es' },
    },
  ])('requests only on opening when the cache is $name', async ({ cache }) => {
    mockApiFetch.mockResolvedValueOnce(translationResponse())
    render(<QuestionTranslation {...props} {...cache} />)

    expect(mockApiFetch).not.toHaveBeenCalled()
    if (cache.translation?.trim()) {
      expect(screen.queryByText(cache.translation)).not.toBeInTheDocument()
    }

    openTranslation()

    expect(await screen.findByText(translatedQuestion)).toBeVisible()
    expect(mockApiFetch).toHaveBeenCalledExactlyOnceWith(
      '/api/lessons/exercises/10/question-translation',
      expect.objectContaining({ method: 'POST', signal: expect.any(AbortSignal) })
    )

    closeTranslation()
    openTranslation()

    expect(screen.getByText(translatedQuestion)).toBeVisible()
    expect(mockApiFetch).toHaveBeenCalledTimes(1)
  })

  it('announces loading and reuses the pending request across toggles', async () => {
    const pending = pendingResponse()
    mockApiFetch.mockReturnValueOnce(pending.promise)
    render(<QuestionTranslation {...props} />)

    openTranslation()

    const status = screen.getByRole('status')
    expect(status).toHaveTextContent('translatingQuestion')
    expect(status.parentElement).toHaveAttribute('aria-busy', 'true')

    closeTranslation()
    openTranslation()

    expect(mockApiFetch).toHaveBeenCalledTimes(1)
    await act(async () => {
      pending.resolve(translationResponse())
    })

    expect(screen.getByText(translatedQuestion)).toBeVisible()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.getByText(translatedQuestion).parentElement).toHaveAttribute(
      'aria-busy',
      'false'
    )
  })

  it.each(['http', 'network'])(
    'allows retry after a %s failure',
    async (failure) => {
      if (failure === 'http') {
        mockApiFetch.mockResolvedValueOnce(new Response(null, { status: 503 }))
      } else {
        mockApiFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))
      }
      render(<QuestionTranslation {...props} />)
      openTranslation()

      expect(await screen.findByRole('alert')).toHaveTextContent(
        'questionTranslationError'
      )
      expect(screen.queryByRole('status')).not.toBeInTheDocument()

      const retry = pendingResponse()
      mockApiFetch.mockReturnValueOnce(retry.promise)
      fireEvent.click(
        screen.getByRole('button', { name: 'retryQuestionTranslation' })
      )

      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(screen.getByRole('status')).toBeVisible()
      await act(async () => {
        retry.resolve(translationResponse())
      })

      expect(screen.getByText(translatedQuestion)).toBeVisible()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(mockApiFetch).toHaveBeenCalledTimes(2)
    }
  )

  it.each([
    { name: 'another question', data: { question: 'A regenerated question' } },
    { name: 'another language', data: { question_translation_language: 'fr' } },
    { name: 'missing text', data: { question_translation: null } },
    { name: 'non-string text', data: { question_translation: 42 } },
    { name: 'blank text', data: { question_translation: ' \n ' } },
  ])('rejects a response with $name', async ({ data }) => {
    mockApiFetch.mockResolvedValueOnce(translationResponse(data))
    render(<QuestionTranslation {...props} />)
    openTranslation()

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'questionTranslationError'
    )
    expect(screen.queryByText(translatedQuestion)).not.toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'retryQuestionTranslation' })
    ).toBeVisible()
  })

  it.each(['language', 'question', 'session'])(
    'aborts on remount after a %s change and ignores the old response',
    async (context) => {
      const oldRequest = pendingResponse()
      const newRequest = pendingResponse()
      mockApiFetch
        .mockReturnValueOnce(oldRequest.promise)
        .mockReturnValueOnce(newRequest.promise)
      const { rerender } = render(<QuestionTranslation key="old" {...props} />)
      openTranslation()
      const signal = mockApiFetch.mock.calls[0][1].signal as AbortSignal
      expect(signal.aborted).toBe(false)

      const nextProps = {
        ...props,
        ...(context === 'language'
          ? { nativeLanguage: 'fr', nativeLanguageName: 'Français' }
          : context === 'question'
            ? { question: 'Describe your family.' }
            : {}),
      }
      useAuthStore.setState({
        user: { ...user, native_language: nextProps.nativeLanguage },
        sessionVersion: context === 'session' ? 2 : 1,
      })
      rerender(<QuestionTranslation key="new" {...nextProps} />)

      expect(signal.aborted).toBe(true)
      expect(mockApiFetch).toHaveBeenCalledTimes(1)
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      openTranslation()
      await act(async () => {
        newRequest.resolve(
          translationResponse({
            question: nextProps.question,
            question_translation_language: nextProps.nativeLanguage,
            question_translation: 'Current translation',
          })
        )
      })
      // The mock deliberately completes despite cancellation, like a late body read.
      await act(async () => {
        oldRequest.resolve(translationResponse())
      })

      expect(screen.getByText('Current translation')).toBeVisible()
      expect(screen.queryByText(translatedQuestion)).not.toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(mockApiFetch).toHaveBeenCalledTimes(2)
    }
  )

  it.each(['language', 'session', 'logout'])(
    'ignores a result if auth changes (%s) before the parent remounts',
    async (context) => {
      const pending = pendingResponse()
      mockApiFetch.mockReturnValueOnce(pending.promise)
      render(<QuestionTranslation {...props} />)
      openTranslation()

      useAuthStore.setState({
        user:
          context === 'logout'
            ? null
            : { ...user, native_language: context === 'language' ? 'fr' : 'es' },
        sessionVersion: context === 'session' ? 2 : 1,
      })
      await act(async () => {
        pending.resolve(translationResponse())
      })

      expect(screen.queryByText(translatedQuestion)).not.toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    }
  )
})
