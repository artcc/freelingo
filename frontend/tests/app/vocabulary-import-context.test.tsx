import { Suspense } from 'react'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { NextIntlClientProvider } from 'next-intl'
import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import messages from '../../../messages/en.json'
import VocabularySetPage from '@/app/(app)/vocabulary/[setId]/page'
import { useLanguageStore } from '@/store/language'
import { useAuthStore, type User } from '@/store/auth'
import { getLanguageByCode } from '@/lib/target-languages'

const { api } = vi.hoisted(() => ({ api: vi.fn() }))
vi.mock('@/lib/api', () => ({ apiFetch: api }))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: () => <p>Loading</p>,
}))
const originalFetch = useLanguageStore.getState().fetchLanguages
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status })
let serverLanguage: string

function vocabulary(language: string) {
  return {
    set: {
      id: 'greetings_a1',
      level: 'A1',
      topic: 'Greetings',
      unit_ref: '1',
      words: [
        {
          word: language === 'en-GB' ? 'hello' : 'ciao',
          pos: 'noun',
          definition: 'greeting',
          example: 'A greeting.',
        },
      ],
    },
  }
}

async function show() {
  const params = Promise.resolve({ setId: 'greetings_a1' })
  await act(async () => {
    render(
      <NextIntlClientProvider locale="en" messages={messages} timeZone="UTC">
        <Suspense fallback={<p>Loading params</p>}>
          <VocabularySetPage params={params} />
        </Suspense>
      </NextIntlClientProvider>
    )
  })
}

beforeEach(() => {
  serverLanguage = 'en-GB'
  api.mockReset()
  useAuthStore.setState({ sessionVersion: 0, user: null })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB')!,
    isSwitching: false,
    needsRefresh: false,
    invalidationVersion: 0,
    fetchLanguages: vi.fn(async () => {
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode(serverLanguage)!,
        needsRefresh: false,
      })
      return true
    }),
  })
  api.mockImplementation(async (url: string, options?: RequestInit) => {
    if (url.startsWith('/api/vocabulary/'))
      return json(
        vocabulary(
          new URL(url, 'https://test.invalid').searchParams.get('language')!
        )
      )
    if (url === '/api/study-plan/current')
      return json({
        id: serverLanguage === 'en-GB' ? 42 : 43,
        target_language: serverLanguage,
      })
    if (url === '/api/flashcards/bulk') {
      const body = JSON.parse(String(options?.body))
      return body.target_language === serverLanguage
        ? json({ created: 1 })
        : json({ detail: 'flashcard_context_changed' }, 409)
    }
    throw new Error(`Unexpected request ${url}`)
  })
})

afterEach(() => useLanguageStore.setState({ fetchLanguages: originalFetch }))

it('offers recovery instead of loading indefinitely when no active language is returned', async () => {
  useLanguageStore.setState({
    activeLanguage: null,
    fetchLanguages: vi.fn(async () => true),
  })
  await show()
  expect(await screen.findByRole('alert')).toHaveTextContent(
    messages.common.errorMessage
  )
  expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument()
  expect(api).not.toHaveBeenCalled()
})

it('sends the plan and language captured with the displayed set', async () => {
  await show()
  fireEvent.click(
    await screen.findByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  await screen.findByText(/1 cards added/)
  const call = api.mock.calls.find(([url]) => url === '/api/flashcards/bulk')!
  expect(JSON.parse(call[1].body)).toMatchObject({
    study_plan_id: 42,
    target_language: 'en-GB',
    flashcards: [{ word: 'hello' }],
  })
})

it('retries an initial language mismatch and imports the refreshed set', async () => {
  serverLanguage = 'it-IT'
  await show()
  expect(await screen.findByRole('alert')).toHaveTextContent(
    messages.flashcards.contextChanged
  )
  expect(screen.queryByText('hello')).not.toBeInTheDocument()
  expect(api.mock.calls.some(([url]) => url === '/api/flashcards/bulk')).toBe(
    false
  )

  fireEvent.click(screen.getByRole('button', { name: 'Retry' }))
  await screen.findByText('ciao')
  expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  await screen.findByText(/1 cards added/)
  const call = api.mock.calls.find(([url]) => url === '/api/flashcards/bulk')!
  expect(JSON.parse(call[1].body)).toMatchObject({
    study_plan_id: 43,
    target_language: 'it-IT',
    flashcards: [{ word: 'ciao' }],
  })
})

it('handles a different server-side language by reloading without automatically adding the new set', async () => {
  await show()
  await screen.findByText('hello')
  serverLanguage = 'it-IT' // Another tab switched the server context; this store is still English.
  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  expect(await screen.findByText('ciao')).toBeInTheDocument()
  expect(
    screen.getByText(messages.flashcards.contextChanged)
  ).toBeInTheDocument()
  const calls = api.mock.calls.filter(([url]) => url === '/api/flashcards/bulk')
  expect(calls).toHaveLength(1)
  expect(JSON.parse(calls[0][1].body)).toMatchObject({
    study_plan_id: 42,
    target_language: 'en-GB',
  })
  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  await screen.findByText(/1 cards added/)
  expect(
    JSON.parse(
      api.mock.calls.filter(([url]) => url === '/api/flashcards/bulk')[1][1]
        .body
    )
  ).toMatchObject({
    study_plan_id: 43,
    target_language: 'it-IT',
    flashcards: [{ word: 'ciao' }],
  })
})

it('preserves a new import when the language refresh finishes after publishing the new context', async () => {
  let finishRefresh!: (ok: boolean) => void
  const refresh = new Promise<boolean>((resolve) => {
    finishRefresh = resolve
  })
  useLanguageStore.setState({
    fetchLanguages: vi.fn(() => {
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode(serverLanguage)!,
        needsRefresh: false,
      })
      return refresh
    }),
  })
  await show()
  await screen.findByText('hello')
  serverLanguage = 'it-IT'
  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  await screen.findByText('ciao')
  expect(
    api.mock.calls.filter(([url]) => url === '/api/flashcards/bulk')
  ).toHaveLength(1)

  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  await screen.findByText(/1 cards added/)
  await act(async () => finishRefresh(true))
  expect(screen.getByText(/1 cards added/)).toBeInTheDocument()
  const imports = api.mock.calls.filter(
    ([url]) => url === '/api/flashcards/bulk'
  )
  expect(imports).toHaveLength(2)
  expect(JSON.parse(imports[1][1].body)).toMatchObject({
    study_plan_id: 43,
    target_language: 'it-IT',
    flashcards: [{ word: 'ciao' }],
  })
})

it('reloads a replaced plan even when the language snapshot stays unchanged', async () => {
  await show()
  await screen.findByText('hello')
  const original = api.getMockImplementation()!
  api.mockImplementation(async (url: string, options?: RequestInit) => {
    if (url === '/api/study-plan/current')
      return json({ id: 44, target_language: 'en-GB' })
    if (url === '/api/flashcards/bulk') {
      const body = JSON.parse(String(options?.body))
      return body.study_plan_id === 44
        ? json({ created: 1 })
        : json({ detail: 'flashcard_context_changed' }, 409)
    }
    return original(url, options)
  })
  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  await screen.findByText(messages.flashcards.contextChanged)
  expect(
    api.mock.calls.filter(([url]) => url === '/api/flashcards/bulk')
  ).toHaveLength(1)
  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  await screen.findByText(/1 cards added/)
  const imports = api.mock.calls.filter(
    ([url]) => url === '/api/flashcards/bulk'
  )
  expect(imports).toHaveLength(2)
  expect(JSON.parse(imports[1][1].body)).toMatchObject({
    study_plan_id: 44,
    target_language: 'en-GB',
    flashcards: [{ word: 'hello' }],
  })
})

it('ignores late set content from the previous language', async () => {
  let resolveOld!: (body: unknown) => void
  const old = new Promise((resolve) => {
    resolveOld = resolve
  })
  const first = api.getMockImplementation()!
  api.mockImplementation(async (url: string, options?: RequestInit) =>
    url.includes('language=en-GB')
      ? { ok: true, json: () => old }
      : first(url, options)
  )
  await show()
  await waitFor(() =>
    expect(api).toHaveBeenCalledWith(
      expect.stringContaining('language=en-GB'),
      expect.anything()
    )
  )
  serverLanguage = 'it-IT'
  act(() =>
    useLanguageStore.setState({ activeLanguage: getLanguageByCode('it-IT')! })
  )
  await screen.findByText('ciao')
  await act(async () => resolveOld(vocabulary('en-GB')))
  expect(screen.queryByText('hello')).not.toBeInTheDocument()
  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  await screen.findByText(/1 cards added/)
  const body = JSON.parse(
    api.mock.calls.find(([url]) => url === '/api/flashcards/bulk')![1].body
  )
  expect(body.flashcards[0].word).toBe('ciao')
  expect(body.study_plan_id).toBe(43)
})

it('still allows browsing a set without an active plan and does not send an unbound import', async () => {
  const first = api.getMockImplementation()!
  api.mockImplementation(async (url: string, options?: RequestInit) =>
    url === '/api/study-plan/current' ? json(null) : first(url, options)
  )
  await show()
  await screen.findByText('hello')
  fireEvent.click(
    screen.getByRole('button', { name: 'Add All 1 to Flashcards' })
  )
  expect(screen.getByText(messages.common.noActivePlan)).toBeInTheDocument()
  expect(api.mock.calls.some(([url]) => url === '/api/flashcards/bulk')).toBe(
    false
  )
})

it.each(['language', 'account', 'native-language', 'plan'] as const)(
  'discards obsolete native help on %s changes without disturbing the new request',
  async (change) => {
    const user: User = {
      id: 1,
      username: 'learner',
      displayName: 'Learner',
      role: 'user',
      native_language: 'es',
      conversation_max_duration: 300,
      conversation_inactivity_timeout: 30,
    }
    useAuthStore.setState({ user })
    let oldHelp!: (response: Response) => void
    let newHelp!: (response: Response) => void
    const firstHelp = new Promise<Response>((resolve) => {
      oldHelp = resolve
    })
    const secondHelp = new Promise<Response>((resolve) => {
      newHelp = resolve
    })
    const original = api.getMockImplementation()!
    let helps = 0
    api.mockImplementation(async (url: string, options?: RequestInit) => {
      if (url.includes('/native-help?'))
        return ++helps === 1 ? firstHelp : secondHelp
      return original(url, options)
    })
    await show()
    await screen.findByText('hello')
    fireEvent.click(screen.getByRole('button', { name: 'Help in Spanish+' }))
    fireEvent.click(
      screen.getByRole('button', { name: 'Show help in Spanish' })
    )
    const oldSignal = api.mock.calls.find(([url]) =>
      url.includes('/native-help?')
    )![1].signal as AbortSignal
    act(() => {
      if (change === 'language') {
        serverLanguage = 'it-IT'
        useLanguageStore.setState({
          activeLanguage: getLanguageByCode('it-IT')!,
        })
      } else if (change === 'account') {
        useAuthStore.setState({ sessionVersion: 1, user: { ...user, id: 2 } })
      } else if (change === 'native-language') {
        useAuthStore.setState({ user: { ...user, native_language: 'fr' } })
      } else {
        useLanguageStore.setState({ invalidationVersion: 1 })
      }
    })
    const language = change === 'native-language' ? 'French' : 'Spanish'
    fireEvent.click(
      await screen.findByRole('button', { name: `Help in ${language}+` })
    )
    fireEvent.click(
      screen.getByRole('button', { name: `Show help in ${language}` })
    )
    expect(helps).toBe(2)
    expect(oldSignal.aborted).toBe(true)
    const response = (summary: string) =>
      json({
        native_help: {
          summary,
          study_tips: [],
          word_notes: [],
          common_traps: [],
          mini_glossary: [],
          practice_prompts: [],
        },
      })
    await act(async () => oldHelp(response('Obsolete English help')))
    expect(screen.queryByText('Obsolete English help')).not.toBeInTheDocument()
    expect(
      screen.getByText(`Preparing help in ${language}...`)
    ).toBeInTheDocument()
    await act(async () => newHelp(response('Current help')))
    expect(screen.getByText('Current help')).toBeInTheDocument()
  }
)

it('ignores an obsolete help failure and lets the current help retry its own failure', async () => {
  useAuthStore.setState({
    user: {
      id: 1,
      username: 'learner',
      displayName: 'Learner',
      role: 'user',
      native_language: 'es',
      conversation_max_duration: 300,
      conversation_inactivity_timeout: 30,
    },
  })
  let failOld!: (response: Response) => void
  const pending = new Promise<Response>((resolve) => {
    failOld = resolve
  })
  const original = api.getMockImplementation()!
  let helps = 0
  api.mockImplementation(async (url: string, options?: RequestInit) => {
    if (url.includes('/native-help?'))
      return ++helps === 1 ? pending : json({}, 503)
    return original(url, options)
  })
  await show()
  await screen.findByText('hello')
  fireEvent.click(screen.getByRole('button', { name: 'Help in Spanish+' }))
  fireEvent.click(screen.getByRole('button', { name: 'Show help in Spanish' }))
  serverLanguage = 'it-IT'
  act(() =>
    useLanguageStore.setState({ activeLanguage: getLanguageByCode('it-IT')! })
  )
  await screen.findByText('ciao')
  await act(async () => failOld(json({}, 503)))
  fireEvent.click(screen.getByRole('button', { name: 'Help in Spanish+' }))
  fireEvent.click(screen.getByRole('button', { name: 'Show help in Spanish' }))
  fireEvent.click(await screen.findByRole('button', { name: 'Retry' }))
  await screen.findByRole('button', { name: 'Retry' })
  expect(helps).toBe(3)
})
