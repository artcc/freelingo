import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { QuestionExplanation } from '@/components/comprehension/QuestionExplanation'
import { getLanguageByCode } from '@/lib/target-languages'
import { useAuthStore, type User } from '@/store/auth'
import { useLanguageStore } from '@/store/language'

const mockApiFetch = vi.hoisted(() => vi.fn())
vi.mock('@/lib/api', () => ({ apiFetch: mockApiFetch }))
vi.mock('next-intl', () => ({
  useLocale: () => 'en',
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
  feature: 'reading' as const,
  attemptId: 81,
  questionIndex: 2,
  sourceText: 'The museum opens at nine. It closes at five.',
  context: { study_plan_id: 8, target_language: 'en-GB', level: 'A1' },
  sessionVersion: 1,
}
const explanation = 'El museo abre a las nueve, por eso la opción A es correcta.'
const evidence = 'The museum opens at nine.'

function response(overrides: Record<string, unknown> = {}) {
  return new Response(
    JSON.stringify({
      explanation,
      evidence,
      native_language: 'es',
      target_language: 'en-GB',
      ...overrides,
    })
  )
}

function pendingResponse() {
  let resolve!: (value: Response) => void
  const promise = new Promise<Response>((done) => {
    resolve = done
  })
  return { promise, resolve }
}

function open() {
  fireEvent.click(screen.getByRole('button', { name: 'show' }))
}

beforeEach(() => {
  mockApiFetch.mockReset()
  useAuthStore.setState({ user, sessionVersion: 1 })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB') ?? null,
    isSwitching: false,
    needsRefresh: false,
    userLanguages: [
      {
        target_language: 'en-GB',
        is_active: true,
        progress: null,
        plan: {
          id: 8,
          cefr_level: 'A1',
          progress_day: 0,
          total_days: 48,
          completion_pct: 0,
        },
      },
    ],
  })
})

afterEach(() => {
  cleanup()
  useAuthStore.setState(useAuthStore.getInitialState(), true)
  useLanguageStore.setState(useLanguageStore.getInitialState(), true)
})

describe('QuestionExplanation', () => {
  it.each(['reading', 'listening'] as const)(
    'requests %s help only on demand and keeps the original and native languages',
    async (feature) => {
      const pending = pendingResponse()
      mockApiFetch.mockReturnValueOnce(pending.promise)
      render(<QuestionExplanation {...props} feature={feature} />)
      expect(mockApiFetch).not.toHaveBeenCalled()
      const toggle = screen.getByRole('button', { name: 'show' })
      expect(toggle).toHaveAttribute('aria-expanded', 'false')
      open()
      expect(screen.getByRole('status')).toHaveTextContent('loading')
      expect(toggle).toHaveAttribute('aria-expanded', 'true')
      fireEvent.click(toggle)
      open()
      expect(mockApiFetch).toHaveBeenCalledExactlyOnceWith(
        `/api/${feature}/attempts/81/questions/2/explanation`,
        { method: 'POST', signal: expect.any(AbortSignal) }
      )
      await act(async () => pending.resolve(response()))
      expect(screen.getByText(evidence)).toHaveAttribute('lang', 'en-GB')
      expect(screen.getByText(explanation)).toHaveAttribute('lang', 'es')
      expect(screen.getByText(explanation)).toHaveAttribute('dir', 'auto')
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      fireEvent.click(screen.getByRole('button', { name: 'hide' }))
      expect(screen.getByText(explanation)).not.toBeVisible()
      open()
      expect(screen.getByText(explanation)).toBeVisible()
      expect(mockApiFetch).toHaveBeenCalledTimes(1)
    }
  )

  it.each([404, 503, 'network'])(
    'offers an explicit retry after %s without fetching automatically',
    async (failure) => {
      if (failure === 'network') {
        mockApiFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))
      } else {
        mockApiFetch.mockResolvedValueOnce(
          new Response(null, { status: Number(failure) })
        )
      }
      render(<QuestionExplanation {...props} />)
      open()
      expect(await screen.findByRole('alert')).toHaveTextContent('error')
      expect(mockApiFetch).toHaveBeenCalledTimes(1)
      mockApiFetch.mockResolvedValueOnce(response())
      fireEvent.click(screen.getByRole('button', { name: 'retry' }))
      expect(await screen.findByText(explanation)).toBeVisible()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(mockApiFetch).toHaveBeenCalledTimes(2)
    }
  )

  it.each([
    { native_language: 'fr' },
    { target_language: 'en-US' },
    { explanation: '  ' },
    { evidence: 'An invented quote.' },
    { evidence: '' },
  ])('rejects a mismatching or empty response: %j', async (overrides) => {
    mockApiFetch.mockResolvedValueOnce(response(overrides))
    render(<QuestionExplanation {...props} />)
    open()
    expect(await screen.findByRole('alert')).toBeVisible()
    expect(screen.queryByText(explanation)).not.toBeInTheDocument()
  })

  it.each(['attempt', 'question', 'source', 'native language'])(
    'aborts and discards a late response after changing %s',
    async (change) => {
      const stale = pendingResponse()
      mockApiFetch.mockReturnValueOnce(stale.promise)
      const { rerender } = render(<QuestionExplanation {...props} />)
      open()
      const signal = mockApiFetch.mock.calls[0][1].signal as AbortSignal
      const next = {
        ...props,
        ...(change === 'attempt' ? { attemptId: 82 } : {}),
        ...(change === 'question' ? { questionIndex: 3 } : {}),
        ...(change === 'source'
          ? { sourceText: `${props.sourceText} Entry is free.` }
          : {}),
      }
      if (change === 'native language') {
        act(() => {
          useAuthStore.setState({ user: { ...user, native_language: 'fr' } })
        })
      }
      rerender(<QuestionExplanation {...next} />)
      expect(signal.aborted).toBe(true)
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'show' })).toBeVisible()
      mockApiFetch.mockResolvedValueOnce(
        response({
          explanation: 'Current explanation',
          native_language: change === 'native language' ? 'fr' : 'es',
        })
      )
      open()
      expect(await screen.findByText('Current explanation')).toBeVisible()
      await act(async () => stale.resolve(response()))
      expect(screen.getByText('Current explanation')).toBeVisible()
      expect(screen.queryByText(explanation)).not.toBeInTheDocument()
    }
  )

  it.each(['session', 'logout', 'target', 'plan', 'level', 'switch', 'refresh'])(
    'removes help and rejects late responses after a %s change',
    async (change) => {
      const stale = pendingResponse()
      mockApiFetch.mockReturnValueOnce(stale.promise)
      render(<QuestionExplanation {...props} />)
      open()
      const signal = mockApiFetch.mock.calls[0][1].signal as AbortSignal
      act(() => {
        if (change === 'session') useAuthStore.setState({ sessionVersion: 2 })
        if (change === 'logout') useAuthStore.setState({ user: null })
        if (change === 'target')
          useLanguageStore.setState({
            activeLanguage: getLanguageByCode('fr-FR') ?? null,
          })
        if (change === 'switch') useLanguageStore.setState({ isSwitching: true })
        if (change === 'refresh')
          useLanguageStore.setState({ needsRefresh: true })
        if (change === 'plan' || change === 'level') {
          useLanguageStore.setState({
            userLanguages: useLanguageStore
              .getState()
              .userLanguages.map((item) => ({
                ...item,
                plan: {
                  ...item.plan!,
                  ...(change === 'plan' ? { id: 9 } : { cefr_level: 'A2' }),
                },
              })),
          })
        }
      })
      expect(signal.aborted).toBe(true)
      await act(async () => stale.resolve(response()))
      expect(screen.queryByRole('button')).not.toBeInTheDocument()
      expect(screen.queryByText(explanation)).not.toBeInTheDocument()
    }
  )

  it('invalidates a request even when a rejected switch is batched into one render', async () => {
    const stale = pendingResponse()
    mockApiFetch.mockReturnValueOnce(stale.promise)
    render(<QuestionExplanation {...props} />)
    open()
    const signal = mockApiFetch.mock.calls[0][1].signal as AbortSignal
    act(() => {
      useLanguageStore.setState({ isSwitching: true })
      useLanguageStore.setState({ isSwitching: false })
    })
    expect(signal.aborted).toBe(true)
    await act(async () => stale.resolve(response()))
    expect(screen.queryByText(explanation)).not.toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    mockApiFetch.mockResolvedValueOnce(response())
    open()
    expect(await screen.findByText(explanation)).toBeVisible()
  })

  it('aborts on unmount and does not reuse its response on a later mount', async () => {
    const stale = pendingResponse()
    mockApiFetch.mockReturnValueOnce(stale.promise)
    const { unmount } = render(<QuestionExplanation {...props} />)
    open()
    const signal = mockApiFetch.mock.calls[0][1].signal as AbortSignal
    unmount()
    expect(signal.aborted).toBe(true)
    render(<QuestionExplanation {...props} />)
    await act(async () => stale.resolve(response()))
    expect(screen.queryByText(explanation)).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'show' })).toHaveAttribute(
      'aria-expanded',
      'false'
    )
    expect(mockApiFetch).toHaveBeenCalledTimes(1)
  })
})
