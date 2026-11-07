import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import VocabularyPage from '@/app/(app)/vocabulary/page'
import GrammarPage from '@/app/(app)/grammar/page'
import PhrasebookPage from '@/app/(app)/phrasebook/page'
import { getLanguageByCode } from '@/lib/target-languages'
import { useAuthStore, type User } from '@/store/auth'
import { useLanguageStore } from '@/store/language'

const { api } = vi.hoisted(() => ({ api: vi.fn() }))
vi.mock('@/lib/api', () => ({ apiFetch: api }))
vi.mock('next-intl', () => ({
  useTranslations: (namespace: string) => (key: string) =>
    `${namespace}.${key}`,
}))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: () => <p role="status">Loading resources</p>,
}))
vi.mock('@/components/ui/AudioPlayer', () => ({ AudioPlayer: () => null }))

const originalFetchLanguages = useLanguageStore.getState().fetchLanguages

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (error: Error) => void
  const promise = new Promise<T>((yes, no) => {
    resolve = yes
    reject = no
  })
  return { promise, resolve, reject }
}

const catalogs = [
  {
    name: 'vocabulary',
    Page: VocabularyPage,
    body: (title?: string) => ({
      sets: title
        ? [
            {
              id: 'greetings',
              topic: title,
              level: 'A1',
              unit_ref: '1',
              words: [],
            },
          ]
        : [],
    }),
  },
  {
    name: 'grammar',
    Page: GrammarPage,
    body: (title?: string) => ({
      topics: title
        ? [
            {
              slug: 'greetings',
              title,
              summary: '',
              level: 'A1',
              category: 'Basics',
            },
          ]
        : [],
    }),
  },
  {
    name: 'phrasebook',
    Page: PhrasebookPage,
    body: (title?: string) => ({
      categories: title
        ? [
            {
              id: 'greetings',
              situation: title,
              level: 'A1',
              icon: '',
              phrases: [
                { text: `${title} phrase`, context: '', register: 'neutral' },
              ],
            },
          ]
        : [],
    }),
  },
]

beforeEach(() => {
  api.mockReset()
  useAuthStore.setState({ sessionVersion: 0, user: null })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB')!,
    needsRefresh: false,
    isSwitching: false,
    invalidationVersion: 0,
    fetchLanguages: originalFetchLanguages,
  })
})

afterEach(() => {
  cleanup()
  useLanguageStore.setState({ fetchLanguages: originalFetchLanguages })
})

describe.each(catalogs)('$name catalog lifecycle', ({ name, Page, body }) => {
  it('shows an empty result only after a successful response', async () => {
    const pending = deferred<Response>()
    api.mockReturnValue(pending.promise)
    render(<Page />)
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(screen.queryByText(`${name}.noResults`)).not.toBeInTheDocument()
    expect(screen.queryByText('vocabulary.sets')).not.toBeInTheDocument()
    await act(async () => pending.resolve(Response.json(body())))
    expect(screen.getByText(`${name}.noResults`)).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  })

  it('reports HTTP errors and clears the error when a manual retry succeeds', async () => {
    const retry = deferred<Response>()
    api.mockResolvedValueOnce(new Response(null, { status: 503 }))
    api.mockReturnValueOnce(retry.promise)
    render(<Page />)
    await screen.findByRole('alert')
    expect(screen.queryByText(`${name}.noResults`)).not.toBeInTheDocument()
    expect(api).toHaveBeenCalledTimes(1)
    fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(screen.getByRole('status')).toBeInTheDocument()
    await act(async () =>
      retry.resolve(Response.json(body('Recovered catalog')))
    )
    expect(screen.getByText('Recovered catalog')).toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(api).toHaveBeenCalledTimes(2)
  })

  it('exits loading on timeout and allows retry without mistaking the deadline for obsolete context', async () => {
    const deadline = new AbortController()
    const timeout = vi
      .spyOn(AbortSignal, 'timeout')
      .mockReturnValue(deadline.signal)
    api.mockImplementationOnce(
      (_url: string, options: RequestInit) =>
        new Promise((_resolve, reject) => {
          options.signal!.addEventListener('abort', () =>
            reject(options.signal!.reason)
          )
        })
    )
    render(<Page />)
    expect(screen.getByRole('status')).toBeInTheDocument()
    await act(async () => {
      deadline.abort(new DOMException('Timed out', 'TimeoutError'))
    })
    expect(screen.getByRole('alert')).toBeInTheDocument()
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(screen.queryByText(`${name}.noResults`)).not.toBeInTheDocument()
    timeout.mockReturnValue(new AbortController().signal)
    api.mockResolvedValueOnce(Response.json(body('Recovered catalog')))
    fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
    await screen.findByText('Recovered catalog')
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it.each(['success', 'failure'])(
    'ignores an obsolete %s without releasing the current load',
    async (outcome) => {
      const old = deferred<Response>()
      const current = deferred<Response>()
      api.mockReturnValueOnce(old.promise).mockReturnValueOnce(current.promise)
      render(<Page />)
      const signal = api.mock.calls[0][1].signal as AbortSignal
      act(() =>
        useLanguageStore.setState({
          activeLanguage: getLanguageByCode('fr-FR')!,
        })
      )
      expect(signal.aborted).toBe(true)
      await act(async () => {
        if (outcome === 'success')
          old.resolve(Response.json(body('Obsolete catalog')))
        else old.reject(new Error('Old request failed'))
      })
      expect(screen.getByRole('status')).toBeInTheDocument()
      expect(screen.queryByRole('alert')).not.toBeInTheDocument()
      expect(screen.queryByText('Obsolete catalog')).not.toBeInTheDocument()
      await act(async () =>
        current.resolve(Response.json(body('French catalog')))
      )
      expect(screen.getByText('French catalog')).toBeInTheDocument()
      expect(api.mock.calls[1][0]).toContain('language=fr-FR')
    }
  )

  it('cannot replace a newer catalog with a delayed response body', async () => {
    const oldBody = deferred<unknown>()
    api.mockResolvedValueOnce({ ok: true, json: () => oldBody.promise })
    api.mockResolvedValueOnce(Response.json(body('French catalog')))
    render(<Page />)
    await act(async () => {})
    act(() =>
      useLanguageStore.setState({ activeLanguage: getLanguageByCode('fr-FR')! })
    )
    await screen.findByText('French catalog')
    await act(async () => oldBody.resolve(body('Obsolete catalog')))
    expect(screen.getByText('French catalog')).toBeInTheDocument()
    expect(screen.queryByText('Obsolete catalog')).not.toBeInTheDocument()
  })

  it('cancels on unmount and ignores late failure', async () => {
    const pending = deferred<Response>()
    api.mockReturnValue(pending.promise)
    const view = render(<Page />)
    const signal = api.mock.calls[0][1].signal as AbortSignal
    view.unmount()
    expect(signal.aborted).toBe(true)
    await act(async () => pending.reject(new Error('Late failure')))
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    expect(api).toHaveBeenCalledTimes(1)
  })

  it('reconciles invalidated language before fetching and retries only the recovery after failure', async () => {
    const recover = vi
      .fn()
      .mockResolvedValueOnce(false)
      .mockImplementationOnce(async () => {
        useLanguageStore.setState({
          activeLanguage: getLanguageByCode('fr-FR')!,
          needsRefresh: false,
        })
        return true
      })
    useLanguageStore.setState({ needsRefresh: true, fetchLanguages: recover })
    api.mockResolvedValue(Response.json(body('French catalog')))
    render(<Page />)
    await screen.findByRole('alert')
    expect(api).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
    await screen.findByText('French catalog')
    expect(recover).toHaveBeenCalledTimes(2)
    expect(api).toHaveBeenCalledTimes(1)
    expect(api.mock.calls[0][0]).toContain('language=fr-FR')
  })

  it('does not substitute a default language when recovery returns no active language', async () => {
    useLanguageStore.setState({
      activeLanguage: null,
      fetchLanguages: vi.fn().mockResolvedValue(true),
    })
    render(<Page />)
    await screen.findByRole('alert')
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(api).not.toHaveBeenCalled()
  })

  it('cancels its language recovery wait when unmounted', async () => {
    const recovery = deferred<boolean>()
    const recover = vi.fn().mockReturnValue(recovery.promise)
    useLanguageStore.setState({ activeLanguage: null, fetchLanguages: recover })
    const view = render(<Page />)
    const signal = recover.mock.calls[0][0] as AbortSignal
    view.unmount()
    expect(signal.aborted).toBe(true)
    await act(async () => recovery.resolve(false))
    expect(api).not.toHaveBeenCalled()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('pauses catalog requests during switching and clears an old error on the next language', async () => {
    api.mockResolvedValueOnce(new Response(null, { status: 500 }))
    api.mockResolvedValueOnce(Response.json(body('French catalog')))
    render(<Page />)
    await screen.findByRole('alert')
    act(() => useLanguageStore.setState({ isSwitching: true }))
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(api).toHaveBeenCalledTimes(1)
    act(() =>
      useLanguageStore.setState({
        isSwitching: false,
        activeLanguage: getLanguageByCode('fr-FR')!,
      })
    )
    await screen.findByText('French catalog')
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })
})

it.each(['target language', 'native language', 'session', 'invalidation'])(
  'isolates phrasebook help after %s replacement with the same category ID',
  async (context) => {
    const old = deferred<Response>()
    const current = deferred<Response>()
    const pendingHelp = vi
      .fn()
      .mockReturnValueOnce(old.promise)
      .mockReturnValueOnce(current.promise)
    const body = catalogs[2].body
    useAuthStore.setState({ user: { id: 1, native_language: 'es' } as User })
    api.mockImplementation((url: string, options: RequestInit) => {
      if (url.includes('/native-help')) return pendingHelp(url, options)
      return Promise.resolve(Response.json(body('Greetings')))
    })
    render(<PhrasebookPage />)
    fireEvent.click(
      await screen.findByRole('button', { name: 'common.nativeHelpShow' })
    )
    const signal = pendingHelp.mock.calls[0][1].signal as AbortSignal
    act(() => {
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
      if (context === 'session') useAuthStore.setState({ sessionVersion: 1 })
      if (context === 'invalidation')
        useLanguageStore.setState({ invalidationVersion: 1 })
    })
    fireEvent.click(
      await screen.findByRole('button', { name: 'common.nativeHelpShow' })
    )
    expect(signal.aborted).toBe(true)
    await act(async () => old.reject(new Error('Old help failed')))
    expect(screen.getByText('common.nativeHelpLoading')).toBeInTheDocument()
    await act(async () =>
      current.resolve(
        Response.json({
          native_help: {
            summary: 'French help',
            usage_tips: [],
            register_notes: [],
            phrase_notes: [],
            common_traps: [],
            mini_glossary: [],
          },
        })
      )
    )
    expect(screen.getByText('French help')).toBeInTheDocument()
    expect(
      screen.queryByRole('button', { name: 'common.retry' })
    ).not.toBeInTheDocument()
    expect(pendingHelp).toHaveBeenCalledTimes(2)
  }
)

describe('phrasebook provisional language switching', () => {
  function helpResponse() {
    return Response.json({
      native_help: {
        summary: 'Preserved phrasebook help',
        usage_tips: [],
        register_notes: [],
        phrase_notes: [],
        common_traps: [],
        mini_glossary: [],
      },
    })
  }

  it('waits for an initial provisional switch before fetching its catalog', async () => {
    useLanguageStore.setState({ isSwitching: true })
    api.mockResolvedValueOnce(Response.json(catalogs[2].body('Greetings')))
    render(<PhrasebookPage />)
    expect(api).not.toHaveBeenCalled()
    act(() => useLanguageStore.setState({ isSwitching: false }))
    await screen.findByText('Greetings')
    expect(api).toHaveBeenCalledTimes(1)
  })

  it('retains a catalog response received during a rejected switch without fetching again', async () => {
    const pending = deferred<Response>()
    api.mockReturnValueOnce(pending.promise)
    render(<PhrasebookPage />)
    const signal = api.mock.calls[0][1].signal as AbortSignal
    act(() => useLanguageStore.setState({ isSwitching: true }))
    expect(signal.aborted).toBe(false)
    await act(async () =>
      pending.resolve(Response.json(catalogs[2].body('Greetings')))
    )
    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(screen.getByText('Greetings')).not.toBeVisible()
    act(() => useLanguageStore.setState({ isSwitching: false }))
    expect(screen.getByText('Greetings')).toBeVisible()
    expect(api).toHaveBeenCalledTimes(1)
  })

  it.each(['success', 'failure'])(
    'preserves help %s and only retries on explicit action after a rejected switch',
    async (outcome) => {
      const help = vi
        .fn()
        .mockResolvedValueOnce(
          outcome === 'success'
            ? helpResponse()
            : new Response(null, { status: 503 })
        )
      useAuthStore.setState({ user: { id: 1, native_language: 'es' } as User })
      api.mockImplementation((url: string, options: RequestInit) => {
        if (url.includes('/native-help')) return help(url, options)
        return Promise.resolve(Response.json(catalogs[2].body('Greetings')))
      })
      render(<PhrasebookPage />)
      fireEvent.click(
        await screen.findByRole('button', { name: 'common.nativeHelpShow' })
      )
      if (outcome === 'success')
        await screen.findByText('Preserved phrasebook help')
      else await screen.findByRole('button', { name: 'common.retry' })
      act(() => useLanguageStore.setState({ isSwitching: true }))
      expect(screen.getByRole('status')).toBeInTheDocument()
      expect(screen.getByText('Greetings')).not.toBeVisible()
      expect(screen.getByText('Greetings').closest('[inert]')).not.toBeNull()
      act(() => useLanguageStore.setState({ isSwitching: false }))
      await act(async () => {})
      expect(screen.getByText('Greetings')).toBeVisible()
      expect(api).toHaveBeenCalledTimes(2)
      expect(help).toHaveBeenCalledTimes(1)
      if (outcome === 'success') {
        expect(screen.getByText('Preserved phrasebook help')).toBeVisible()
      } else {
        help.mockResolvedValueOnce(helpResponse())
        fireEvent.click(screen.getByRole('button', { name: 'common.retry' }))
        await screen.findByText('Preserved phrasebook help')
        expect(help).toHaveBeenCalledTimes(2)
      }
    }
  )

  it.each(['success', 'failure'])(
    'retains help %s received while a provisional switch is pending',
    async (outcome) => {
      const pending = deferred<Response>()
      const help = vi.fn().mockReturnValue(pending.promise)
      useAuthStore.setState({ user: { id: 1, native_language: 'es' } as User })
      api.mockImplementation((url: string, options: RequestInit) => {
        if (url.includes('/native-help')) return help(url, options)
        return Promise.resolve(Response.json(catalogs[2].body('Greetings')))
      })
      render(<PhrasebookPage />)
      fireEvent.click(
        await screen.findByRole('button', { name: 'common.nativeHelpShow' })
      )
      const signal = help.mock.calls[0][1].signal as AbortSignal
      act(() => useLanguageStore.setState({ isSwitching: true }))
      expect(signal.aborted).toBe(false)
      await act(async () => {
        if (outcome === 'success') pending.resolve(helpResponse())
        else pending.reject(new Error('Help failed'))
      })
      act(() => useLanguageStore.setState({ isSwitching: false }))
      expect(
        screen.queryByText('common.nativeHelpLoading')
      ).not.toBeInTheDocument()
      if (outcome === 'success')
        expect(screen.getByText('Preserved phrasebook help')).toBeVisible()
      else
        expect(
          screen.getByRole('button', { name: 'common.retry' })
        ).toBeVisible()
      expect(api).toHaveBeenCalledTimes(2)
      expect(help).toHaveBeenCalledTimes(1)
    }
  )
})
