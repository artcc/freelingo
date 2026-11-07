import { StrictMode, Suspense } from 'react'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import GrammarDetailPage from '@/app/(app)/grammar/[slug]/page'
import { getLanguageByCode } from '@/lib/target-languages'
import { useAuthStore, type User } from '@/store/auth'
import { useLanguageStore } from '@/store/language'

const { api, help, missing } = vi.hoisted(() => ({
  api: vi.fn(),
  help: vi.fn(),
  missing: vi.fn(() => {
    throw new Error('Missing topic')
  }),
}))
vi.mock('@/lib/api', () => ({ apiFetch: api }))
vi.mock('next-intl', () => ({
  useTranslations: (namespace: string) => (key: string) =>
    `${namespace}.${key}`,
}))
vi.mock('next/navigation', () => ({ notFound: missing }))
vi.mock('@/hooks/useAnalyticsView', () => ({
  useAnalyticsView: () => undefined,
}))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: () => <p role="status">Loading resources</p>,
}))

const topics = ['A1', 'A2', 'B1'].map((level) => ({
  slug: level.toLowerCase(),
  title: `Topic ${level}`,
  level,
  category: 'Basics',
  summary: 'Summary',
  explanation: 'Explanation',
  rules: [],
  examples: [],
  common_mistakes: [],
  related: [],
}))

function helpResponse(summary: string) {
  return Response.json({
    native_help: {
      summary,
      explanation: 'Native explanation',
      key_points: [],
      examples: [],
      common_traps: [],
      mini_glossary: [],
    },
  })
}

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (error: Error) => void
  const promise = new Promise<T>((yes, no) => {
    resolve = yes
    reject = no
  })
  return { promise, resolve, reject }
}

function page(slug: string) {
  return (
    <Suspense fallback={<p>Loading params</p>}>
      <GrammarDetailPage params={Promise.resolve({ slug })} />
    </Suspense>
  )
}

async function show(slug = 'a1') {
  let view!: ReturnType<typeof render>
  await act(async () => {
    view = render(page(slug))
  })
  return view
}

beforeEach(() => {
  api.mockReset()
  help.mockReset()
  missing.mockClear()
  useAuthStore.setState({
    sessionVersion: 0,
    user: { id: 1, native_language: 'es' } as User,
  })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB')!,
    needsRefresh: false,
    isSwitching: false,
    invalidationVersion: 0,
  })
  api.mockImplementation((url: string, options: RequestInit) => {
    if (url.includes('/native-help')) return help(url, options)
    return Promise.resolve(Response.json({ topics }))
  })
  help.mockResolvedValue(helpResponse('Native help'))
})

afterEach(cleanup)

describe('grammar native help lifecycle', () => {
  it.each(['a1', 'a2'])(
    'starts only one %s help POST under StrictMode and cancels on real unmount',
    async (slug) => {
      const pending = deferred<Response>()
      help.mockReturnValueOnce(pending.promise)
      let view!: ReturnType<typeof render>
      await act(async () => {
        view = render(<StrictMode>{page(slug)}</StrictMode>)
      })
      await screen.findByText('common.nativeHelpLoading')
      expect(help).toHaveBeenCalledTimes(1)
      expect(help.mock.calls[0][1].method).toBe('POST')
      const signal = help.mock.calls[0][1].signal as AbortSignal
      expect(signal.aborted).toBe(false)
      view.unmount()
      expect(signal.aborted).toBe(true)
      await act(async () => pending.reject(new Error('Unmounted request')))
      await act(async () => {
        render(<StrictMode>{page(slug)}</StrictMode>)
      })
      await screen.findByText('Native help')
      expect(help).toHaveBeenCalledTimes(2)
    }
  )

  it.each(['a1', 'a2'])(
    'preserves loaded %s help and its catalog after a rejected provisional switch',
    async (slug) => {
      await show(slug)
      await screen.findByText('Native help')
      const requests = api.mock.calls.length
      act(() => useLanguageStore.setState({ isSwitching: true }))
      expect(screen.getByRole('status')).toBeInTheDocument()
      expect(screen.getByText('Native help')).not.toBeVisible()
      expect(screen.getByText('Native help').closest('[inert]')).not.toBeNull()
      act(() => useLanguageStore.setState({ isSwitching: false }))
      expect(screen.getByText('Native help')).toBeVisible()
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      expect(api).toHaveBeenCalledTimes(requests)
      expect(help).toHaveBeenCalledTimes(1)
    }
  )

  it.each(['a1', 'a2'])(
    'preserves failed %s help across a rejected switch until explicit retry',
    async (slug) => {
      help.mockResolvedValueOnce(new Response(null, { status: 503 }))
      await show(slug)
      await screen.findByRole('button', { name: 'common.retry' })
      const requests = api.mock.calls.length
      act(() => useLanguageStore.setState({ isSwitching: true }))
      expect(
        screen.queryByRole('button', { name: 'common.retry' })
      ).not.toBeInTheDocument()
      act(() => useLanguageStore.setState({ isSwitching: false }))
      await act(async () => {})
      expect(screen.getByRole('button', { name: 'common.retry' })).toBeVisible()
      expect(api).toHaveBeenCalledTimes(requests)
      expect(help).toHaveBeenCalledTimes(1)
      fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
      await screen.findByText('Native help')
      expect(help).toHaveBeenCalledTimes(2)
    }
  )

  it.each(['success', 'failure'])(
    'retains a help %s received during a rejected switch',
    async (outcome) => {
      const pending = deferred<Response>()
      help.mockReturnValueOnce(pending.promise)
      await show()
      await screen.findByText('common.nativeHelpLoading')
      const signal = help.mock.calls[0][1].signal as AbortSignal
      act(() => useLanguageStore.setState({ isSwitching: true }))
      expect(signal.aborted).toBe(false)
      await act(async () => {
        if (outcome === 'success')
          pending.resolve(helpResponse('Preserved help'))
        else pending.reject(new Error('Help failed'))
      })
      act(() => useLanguageStore.setState({ isSwitching: false }))
      expect(
        screen.queryByText('common.nativeHelpLoading')
      ).not.toBeInTheDocument()
      if (outcome === 'success')
        expect(screen.getByText('Preserved help')).toBeVisible()
      else
        expect(
          screen.getByRole('button', { name: 'common.retry' })
        ).toBeVisible()
      expect(help).toHaveBeenCalledTimes(1)
      expect(api).toHaveBeenCalledTimes(2)
    }
  )

  it('waits for a provisional switch on initial mount before loading the catalog and help', async () => {
    useLanguageStore.setState({ isSwitching: true })
    await show()
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(api).not.toHaveBeenCalled()
    act(() => useLanguageStore.setState({ isSwitching: false }))
    await screen.findByText('Native help')
    expect(api).toHaveBeenCalledTimes(2)
    expect(help).toHaveBeenCalledTimes(1)
  })

  it('preserves an in-flight catalog through a rejected switch without refetching', async () => {
    const pending = deferred<Response>()
    api.mockReturnValueOnce(pending.promise)
    await show()
    const signal = api.mock.calls[0][1].signal as AbortSignal
    act(() => useLanguageStore.setState({ isSwitching: true }))
    expect(signal.aborted).toBe(false)
    await act(async () => pending.resolve(Response.json({ topics })))
    expect(help).not.toHaveBeenCalled()
    expect(
      screen.queryByRole('heading', { name: 'Topic A1' })
    ).not.toBeInTheDocument()
    act(() => useLanguageStore.setState({ isSwitching: false }))
    await screen.findByText('Native help')
    expect(api).toHaveBeenCalledTimes(2)
  })

  it.each(['a1', 'a2'])(
    'automatically loads %s once, stops after error, and permits a successful manual retry',
    async (slug) => {
      const retry = deferred<Response>()
      help.mockReset()
      help.mockResolvedValueOnce(new Response(null, { status: 503 }))
      help.mockReturnValue(retry.promise)
      await show(slug)
      await screen.findByRole('button', { name: 'common.retry' })
      await act(async () => {})
      expect(help).toHaveBeenCalledTimes(1)
      expect(
        screen.queryByText('common.nativeHelpLoading')
      ).not.toBeInTheDocument()
      fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
      expect(screen.getByText('common.nativeHelpLoading')).toBeInTheDocument()
      await act(async () => retry.resolve(helpResponse('Recovered help')))
      expect(screen.getByText('Recovered help')).toBeInTheDocument()
      expect(
        screen.queryByRole('button', { name: 'common.retry' })
      ).not.toBeInTheDocument()
      expect(help).toHaveBeenCalledTimes(2)
    }
  )

  it('loads B1 help on opening and does not retry a failure when merely reopened', async () => {
    help.mockResolvedValue(new Response(null, { status: 503 }))
    await show('b1')
    await screen.findByRole('heading', { name: 'Topic B1' })
    expect(help).not.toHaveBeenCalled()
    const toggle = screen.getByRole('button', {
      name: /common.nativeHelpTitle/,
    })
    fireEvent.click(toggle)
    await screen.findByRole('button', { name: 'common.retry' })
    fireEvent.click(toggle)
    fireEvent.click(toggle)
    await act(async () => {})
    expect(help).toHaveBeenCalledTimes(1)
    help.mockResolvedValueOnce(helpResponse('Explicit retry'))
    fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
    await screen.findByText('Explicit retry')
  })

  describe.each([
    'topic',
    'target language',
    'native language',
    'session',
    'invalidation',
  ])('%s replacement', (context) => {
    it.each(['success', 'failure'])(
      'discards old help %s and cannot release the new help loading state',
      async (outcome) => {
        const old = deferred<Response>()
        const current = deferred<Response>()
        help.mockReset()
        help
          .mockReturnValueOnce(old.promise)
          .mockReturnValueOnce(current.promise)
        const view = await show()
        await screen.findByText('common.nativeHelpLoading')
        const signal = help.mock.calls[0][1].signal as AbortSignal
        await act(async () => {
          if (context === 'topic') view.rerender(page('a2'))
          if (context === 'target language') {
            useLanguageStore.setState({
              activeLanguage: getLanguageByCode('fr-FR')!,
            })
          }
          if (context === 'native language') {
            useAuthStore.setState({
              user: { id: 1, native_language: 'fr' } as User,
            })
          }
          if (context === 'session')
            useAuthStore.setState({ sessionVersion: 1 })
          if (context === 'invalidation')
            useLanguageStore.setState({ invalidationVersion: 1 })
        })
        await screen.findByText('common.nativeHelpLoading')
        expect(help).toHaveBeenCalledTimes(2)
        expect(signal.aborted).toBe(true)
        await act(async () => {
          if (outcome === 'success') old.resolve(helpResponse('Obsolete help'))
          else old.reject(new Error('Obsolete failure'))
        })
        expect(screen.getByText('common.nativeHelpLoading')).toBeInTheDocument()
        expect(screen.queryByText('Obsolete help')).not.toBeInTheDocument()
        expect(
          screen.queryByRole('button', { name: 'common.retry' })
        ).not.toBeInTheDocument()
        await act(async () => current.resolve(helpResponse('Current help')))
        expect(screen.getByText('Current help')).toBeInTheDocument()
      }
    )
  })

  it('clears a previous failure and automatically loads help for a new native language', async () => {
    help.mockResolvedValueOnce(new Response(null, { status: 503 }))
    await show()
    await screen.findByRole('button', { name: 'common.retry' })
    help.mockResolvedValueOnce(helpResponse('French help'))
    act(() =>
      useAuthStore.setState({ user: { id: 1, native_language: 'fr' } as User })
    )
    await screen.findByText('French help')
    expect(
      screen.queryByRole('button', { name: 'common.retry' })
    ).not.toBeInTheDocument()
    expect(help).toHaveBeenCalledTimes(2)
  })

  it('cancels help on unmount and does not retry its late failure', async () => {
    const pending = deferred<Response>()
    help.mockReturnValue(pending.promise)
    const view = await show()
    await screen.findByText('common.nativeHelpLoading')
    const signal = help.mock.calls[0][1].signal as AbortSignal
    view.unmount()
    expect(signal.aborted).toBe(true)
    await act(async () => pending.reject(new Error('Late failure')))
    expect(help).toHaveBeenCalledTimes(1)
  })

  it('offers catalog retry for HTTP failure rather than treating the topic as missing', async () => {
    api.mockResolvedValueOnce(new Response(null, { status: 500 }))
    await show('b1')
    await screen.findByRole('alert')
    expect(missing).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
    await screen.findByRole('heading', { name: 'Topic B1' })
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('ignores an old empty catalog while the new language is still loading', async () => {
    const old = deferred<Response>()
    const current = deferred<Response>()
    api.mockReturnValueOnce(old.promise).mockReturnValueOnce(current.promise)
    await show('b1')
    const signal = api.mock.calls[0][1].signal as AbortSignal
    act(() =>
      useLanguageStore.setState({ activeLanguage: getLanguageByCode('fr-FR')! })
    )
    expect(signal.aborted).toBe(true)
    await act(async () => old.resolve(Response.json({ topics: [] })))
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(missing).not.toHaveBeenCalled()
    await act(async () => current.resolve(Response.json({ topics })))
    await screen.findByRole('heading', { name: 'Topic B1' })
    expect(help).not.toHaveBeenCalled()
  })
})
