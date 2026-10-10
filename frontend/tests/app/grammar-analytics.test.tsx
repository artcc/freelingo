import { Component, StrictMode, Suspense, type ReactNode } from 'react'
import { act, cleanup, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import GrammarDetailPage from '@/app/(app)/grammar/[slug]/page'
import { getGrammarTopics } from '@/data/grammar'
import { getLanguageByCode } from '@/lib/target-languages'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLanguageStore } from '@/store/language'

vi.mock('next-intl', () => ({ useTranslations: () => (key: string) => key }))
vi.mock('next/navigation', () => ({
  notFound: () => {
    throw new Error('missing-topic')
  },
}))

const topics = ['first', 'second'].map((slug) => ({
  slug,
  title: `Topic ${slug}`,
  level: 'B1',
  category: 'tenses',
  summary: 'Summary',
  explanation: 'Explanation',
  rules: [],
  examples: [],
  common_mistakes: [],
  related: [slug === 'first' ? 'second' : 'first'],
}))

class MissingTopic extends Component<
  { children: ReactNode },
  { missing: boolean }
> {
  state = { missing: false }
  static getDerivedStateFromError() {
    return { missing: true }
  }
  render() {
    return this.state.missing ? <p>Missing topic</p> : this.props.children
  }
}

function page(params: Promise<{ slug: string }>) {
  return (
    <StrictMode>
      <MissingTopic>
        <Suspense fallback={<p>Waiting</p>}>
          <GrammarDetailPage params={params} />
        </Suspense>
      </MissingTopic>
    </StrictMode>
  )
}

function events() {
  return vi
    .mocked(fetch)
    .mock.calls.filter(([url]) => url === '/api/analytics/ui')
    .map(([, options]) => JSON.parse(String(options?.body)))
}

async function renderPage(params: Promise<{ slug: string }>) {
  let view!: ReturnType<typeof render>
  await act(async () => {
    view = render(page(params))
  })
  return view
}

beforeEach(() => {
  useAuthStore.getState().startSession('token')
  useAuthStore.setState({ user: null })
  useConfigStore.setState({ analyticsEnabled: true, loaded: true })
  useLanguageStore.setState({
    activeLanguage: getLanguageByCode('en-GB') ?? null,
    needsRefresh: false,
    isSwitching: false,
  })
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url) => {
      if (String(url).startsWith('/api/grammar?'))
        return Response.json({ topics })
      return new Response(null, { status: 204 })
    })
  )
  vi.stubGlobal('IntersectionObserver', undefined)
})

afterEach(() => {
  cleanup()
  useConfigStore.setState({ analyticsEnabled: false })
  vi.unstubAllGlobals()
})

describe('real grammar detail consumption', () => {
  it('counts valid topic views once, including related-topic navigation, without exporting the slug', async () => {
    const first = Promise.resolve({ slug: 'first' })
    const view = await renderPage(first)
    await screen.findByRole('heading', { name: 'Topic first' })
    await waitFor(() => expect(events()).toHaveLength(1))
    await act(async () => view.rerender(page(first)))
    expect(events()).toHaveLength(1)
    await act(async () =>
      view.rerender(page(Promise.resolve({ slug: 'second' })))
    )
    await screen.findByRole('heading', { name: 'Topic second' })
    await waitFor(() => expect(events()).toHaveLength(2))
    expect(events().map((event) => event.event)).toEqual([
      'grammar_viewed',
      'grammar_viewed',
    ])
    expect(
      events().every(
        (event) => Object.keys(event).sort().join(',') === 'event,operation_id'
      )
    ).toBe(true)
    expect(events()[0].operation_id).not.toBe(events()[1].operation_id)
    expect(
      vi
        .mocked(fetch)
        .mock.calls.filter(([url]) => String(url).startsWith('/api/grammar/'))
    ).toHaveLength(0)
  })

  it('does not count list loading or lesson-style preloading', async () => {
    await getGrammarTopics('en-GB')
    expect(events()).toHaveLength(0)
  })

  it('does not count missing topics', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    await renderPage(Promise.resolve({ slug: 'unknown' }))
    await screen.findByText('Missing topic')
    expect(events()).toHaveLength(0)
  })

  it('keeps grammar usable with analytics disabled', async () => {
    useConfigStore.setState({ analyticsEnabled: false })
    await renderPage(Promise.resolve({ slug: 'first' }))
    await screen.findByRole('heading', { name: 'Topic first' })
    expect(events()).toHaveLength(0)
  })

  it('waits for the selected language data before counting another view', async () => {
    let finish!: (response: Response) => void
    const french = new Promise<Response>((resolve) => {
      finish = resolve
    })
    vi.mocked(fetch).mockImplementation(async (url) => {
      if (String(url).includes('/api/grammar?language=fr-FR')) return french
      if (String(url).startsWith('/api/grammar?'))
        return Response.json({ topics })
      return new Response(null, { status: 204 })
    })
    await renderPage(Promise.resolve({ slug: 'first' }))
    await screen.findByRole('heading', { name: 'Topic first' })
    await waitFor(() => expect(events()).toHaveLength(1))
    await act(async () =>
      useLanguageStore.setState({
        activeLanguage: getLanguageByCode('fr-FR') ?? null,
      })
    )
    expect(events()).toHaveLength(1)
    await act(async () =>
      finish(
        Response.json({
          topics: topics.map((topic) => ({
            ...topic,
            title: `French ${topic.slug}`,
          })),
        })
      )
    )
    await screen.findByRole('heading', { name: 'French first' })
    await waitFor(() => expect(events()).toHaveLength(2))
  })
})
