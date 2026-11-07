import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import FeedbackPage from '@/app/(app)/feedback/page'
import AdminFeedbackPage from '@/app/(app)/admin/feedback/page'
import AdminReviewsPage from '@/app/(app)/admin/reviews/page'
import { useAuthStore } from '@/store/auth'

const mocks = vi.hoisted(() => ({
  apiFetch: vi.fn(),
  translate: (key: string) => key,
}))
vi.mock('@/lib/api', () => ({ apiFetch: mocks.apiFetch }))
vi.mock('next-intl', () => ({
  useLocale: () => 'en',
  useTranslations: () => mocks.translate,
}))
vi.mock('@/components/admin/AdminNav', () => ({ AdminNav: () => null }))
vi.mock('@/components/ui/page-loading', () => ({
  PageLoading: ({ fullScreen = true }: { fullScreen?: boolean }) => (
    <div role="status" data-full-screen={fullScreen}>
      loading
    </div>
  ),
}))

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (reason: unknown) => void
  const promise = new Promise<T>((yes, no) => {
    resolve = yes
    reject = no
  })
  return { promise, resolve, reject }
}

const feedback = {
  id: 1,
  type: 'feature',
  title: 'Current row',
  description: 'Description',
  status: 'pending',
  author: { id: 2, display_name: 'Author', role: 'user' },
  vote_count: 0,
  comment_count: 0,
  created_at: '2026-07-01',
}
const review = {
  id: 1,
  user_id: 2,
  user_display_name: 'Current row',
  target_language: 'en-GB',
  rating: 5,
  comment: 'Comment',
  is_approved: false,
  created_at: '2026-07-01',
}
const json = (data: unknown) =>
  new Response(JSON.stringify(data), { status: 200 })
const surfaces = [
  {
    name: 'feedback',
    Page: FeedbackPage,
    row: feedback,
    filter: () => screen.getByRole('combobox'),
    value: 'done',
    query: 'status=done',
    next: 'nextPage',
  },
  {
    name: 'admin feedback',
    Page: AdminFeedbackPage,
    row: feedback,
    filter: () => screen.getByLabelText('filterStatus'),
    value: 'done',
    query: 'status=done',
    next: 'nextPage',
  },
  {
    name: 'admin reviews',
    Page: AdminReviewsPage,
    row: review,
    filter: () => screen.getByLabelText('approvalFilter'),
    value: 'approved',
    query: 'is_approved=true',
    next: 'next',
  },
]

beforeEach(() => {
  mocks.apiFetch.mockReset()
  useAuthStore.getState().setUser({
    id: 2,
    username: 'admin',
    displayName: 'Admin',
    role: 'admin',
    subscription_status: 'active',
    conversation_max_duration: 300,
    conversation_inactivity_timeout: 30,
  })
})

describe.each(surfaces)(
  '$name loading ownership',
  ({ Page, row, filter, value, query, next }) => {
    const response = (label = 'Current row', total = 21) =>
      json({
        items: [{ ...row, title: label, user_display_name: label }],
        total,
      })
    const listCalls = () =>
      mocks.apiFetch.mock.calls.filter(
        ([path]) =>
          new URL(path, 'http://localhost').searchParams.get('limit') === '10'
      )
    const totalsOr = (pending: Promise<Response>) => (path: string) =>
      new URL(path, 'http://localhost').searchParams.get('limit') === '1'
        ? Promise.resolve(json({ total: 21 }))
        : pending

    it('issues one initial list read and one page-zero read after filtering a later page', async () => {
      mocks.apiFetch.mockImplementation(() => Promise.resolve(response()))
      render(<Page />)
      await screen.findAllByText('Current row')
      expect(listCalls()).toHaveLength(1)
      fireEvent.click(screen.getByRole('button', { name: next }))
      await waitFor(() => expect(listCalls()).toHaveLength(2))
      expect(listCalls()[1][0]).toContain('skip=10')
      await waitFor(() =>
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      )
      fireEvent.change(filter(), { target: { value } })
      await waitFor(() => expect(listCalls()).toHaveLength(3))
      expect(listCalls()[2][0]).toContain('skip=0')
      expect(listCalls()[2][0]).toContain(query)
    })

    it('hides already-loaded rows while a different filter is pending', async () => {
      mocks.apiFetch.mockImplementation(() => Promise.resolve(response()))
      render(<Page />)
      await screen.findAllByText('Current row')
      const pending = deferred<Response>()
      mocks.apiFetch.mockImplementation(totalsOr(pending.promise))
      fireEvent.change(filter(), { target: { value } })
      expect(screen.queryByText('Current row')).not.toBeInTheDocument()
      expect(screen.getByRole('status')).toBeInTheDocument()
      expect(screen.queryByText('noEntries')).not.toBeInTheDocument()
      expect(screen.queryByText('empty')).not.toBeInTheDocument()
      expect(listCalls().at(-1)![0]).toContain(query)
      await act(async () => {
        pending.resolve(response('Filtered row'))
      })
      await screen.findAllByText('Filtered row')
      expect(screen.queryByText('Current row')).not.toBeInTheDocument()
    })

    it.each(['success', 'failure'])(
      'ignores obsolete %s and finally while the new filter is pending',
      async (outcome) => {
        const old = deferred<Response>()
        const current = deferred<Response>()
        mocks.apiFetch.mockImplementation(totalsOr(old.promise))
        render(<Page />)
        expect(screen.getByRole('status')).toHaveAttribute(
          'data-full-screen',
          'false'
        )
        const signal = listCalls()[0][1].signal as AbortSignal
        mocks.apiFetch.mockImplementation(totalsOr(current.promise))
        fireEvent.change(filter(), { target: { value } })
        expect(signal.aborted).toBe(true)
        await act(async () => {
          if (outcome === 'success') old.resolve(response('Obsolete row'))
          else old.reject(new Error('Old failure'))
        })
        expect(screen.queryByText('Obsolete row')).not.toBeInTheDocument()
        expect(
          screen.queryByText(/errorLoad|loadError/)
        ).not.toBeInTheDocument()
        expect(screen.getByRole('status')).toBeInTheDocument()
        await act(async () => {
          current.resolve(response('Newest row'))
        })
        expect(
          (await screen.findAllByText('Newest row')).length
        ).toBeGreaterThan(0)
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      }
    )

    it('offers retry after failure and aborts the retry on unmount', async () => {
      mocks.apiFetch.mockRejectedValue(new Error('Network'))
      const view = render(<Page />)
      const retry = await screen.findByRole('button', { name: 'retry' })
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      const pending = deferred<Response>()
      mocks.apiFetch.mockImplementation(totalsOr(pending.promise))
      fireEvent.click(retry)
      expect(screen.getByRole('status')).toBeInTheDocument()
      const signal = listCalls().at(-1)![1].signal as AbortSignal
      view.unmount()
      expect(signal.aborted).toBe(true)
      await act(async () => {
        pending.resolve(response('Late row'))
      })
    })

    it('recovers a failed initial read through retry without an empty-state flash', async () => {
      mocks.apiFetch.mockRejectedValue(new Error('Network'))
      render(<Page />)
      const retry = await screen.findByRole('button', { name: 'retry' })
      expect(screen.queryByText('noEntries')).not.toBeInTheDocument()
      expect(screen.queryByText('empty')).not.toBeInTheDocument()
      mocks.apiFetch.mockImplementation(() =>
        Promise.resolve(response('Recovered row'))
      )
      fireEvent.click(retry)
      await screen.findAllByText('Recovered row')
      expect(
        screen.queryByRole('button', { name: 'retry' })
      ).not.toBeInTheDocument()
    })

    it('a read deadline shows an error and releases loading for the current owner', async () => {
      const deadline = new AbortController()
      vi.spyOn(AbortSignal, 'timeout').mockReturnValue(deadline.signal)
      mocks.apiFetch.mockImplementation(
        (_path: string, options: RequestInit) =>
          new Promise((_resolve, reject) => {
            options.signal?.addEventListener(
              'abort',
              () => reject(options.signal?.reason),
              { once: true }
            )
          })
      )
      render(<Page />)
      expect(AbortSignal.timeout).toHaveBeenCalledWith(20_000)
      await act(async () => {
        deadline.abort(new DOMException('Timed out', 'TimeoutError'))
      })
      expect(screen.queryByRole('status')).not.toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'retry' })).toBeEnabled()
    })

    it('a delayed deletion refreshes the current filter instead of its captured query', async () => {
      const deletion = deferred<Response>()
      mocks.apiFetch.mockImplementation(
        (_path: string, options?: RequestInit) =>
          options?.method === 'DELETE'
            ? deletion.promise
            : Promise.resolve(response())
      )
      render(<Page />)
      await screen.findAllByText('Current row')
      fireEvent.click(
        screen.getAllByRole('button', { name: /^(delete|deleteEntry)$/ })[0]
      )
      fireEvent.click(
        within(screen.getByRole('alertdialog')).getByRole('button', {
          name: /^(delete|deleteEntryConfirm)$/,
        })
      )
      fireEvent.change(filter(), { target: { value } })
      await waitFor(() =>
        expect(screen.queryByRole('status')).not.toBeInTheDocument()
      )
      const before = listCalls().length
      await act(async () => {
        deletion.resolve(new Response(null, { status: 204 }))
      })
      await waitFor(() => expect(listCalls().length).toBeGreaterThan(before))
      expect(
        listCalls()
          .slice(before)
          .every(([path]) => path.includes(query))
      ).toBe(true)
    })

    it('removes the previous session rows before a new session read settles', async () => {
      mocks.apiFetch.mockImplementation(() => Promise.resolve(response()))
      render(<Page />)
      await screen.findAllByText('Current row')
      const pending = deferred<Response>()
      mocks.apiFetch.mockImplementation(totalsOr(pending.promise))
      act(() =>
        useAuthStore.setState((state) => ({
          sessionVersion: state.sessionVersion + 1,
        }))
      )
      expect(screen.queryByText('Current row')).not.toBeInTheDocument()
      expect(screen.getByRole('status')).toBeInTheDocument()
      await act(async () => {
        pending.resolve(response('New account row'))
      })
      await screen.findAllByText('New account row')
    })
  }
)

it('keeps review rows mounted during same-filter moderation refresh and failure', async () => {
  const pending = deferred<Response>()
  mocks.apiFetch.mockImplementation(() =>
    Promise.resolve(json({ items: [review], total: 1 }))
  )
  render(<AdminReviewsPage />)
  await screen.findByText('Current row')
  fireEvent.change(screen.getByLabelText('approvalFilter'), {
    target: { value: 'pending' },
  })
  await waitFor(() =>
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  )
  mocks.apiFetch.mockImplementation((path: string, options?: RequestInit) =>
    options?.method === 'PATCH'
      ? Promise.resolve(json({ ...review, is_approved: true }))
      : pending.promise
  )
  fireEvent.click(screen.getByRole('button', { name: 'approve' }))
  await screen.findByRole('status')
  expect(screen.getByText('Current row')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'approve' })).toBeDisabled()
  await act(async () => {
    pending.reject(new Error('Refresh failed'))
  })
  expect(screen.getByText('Current row')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'retry' })).toBeInTheDocument()
})

it('a delayed approval refreshes the new review filter rather than its original pending query', async () => {
  const approval = deferred<Response>()
  mocks.apiFetch.mockImplementation((_path: string, options?: RequestInit) =>
    options?.method === 'PATCH'
      ? approval.promise
      : Promise.resolve(json({ items: [review], total: 1 }))
  )
  render(<AdminReviewsPage />)
  await screen.findByText('Current row')
  fireEvent.change(screen.getByLabelText('approvalFilter'), {
    target: { value: 'pending' },
  })
  await waitFor(() =>
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  )
  fireEvent.click(screen.getByRole('button', { name: 'approve' }))
  fireEvent.change(screen.getByLabelText('approvalFilter'), {
    target: { value: 'approved' },
  })
  await waitFor(() =>
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  )
  const before = mocks.apiFetch.mock.calls.length
  await act(async () => {
    approval.resolve(json({ ...review, is_approved: true }))
  })
  await waitFor(() =>
    expect(mocks.apiFetch.mock.calls.length).toBeGreaterThan(before)
  )
  expect(
    mocks.apiFetch.mock.calls
      .slice(before)
      .every(([path]) => path.includes('is_approved=true'))
  ).toBe(true)
})

it('reconciles a delayed vote with the current query and retains its rows during refresh', async () => {
  const vote = deferred<Response>()
  const refresh = deferred<Response>()
  const listCalls = () =>
    mocks.apiFetch.mock.calls.filter(([path]) =>
      path.startsWith('/api/feedback?')
    )
  mocks.apiFetch.mockImplementation((_path: string, options?: RequestInit) =>
    options?.method === 'POST'
      ? vote.promise
      : Promise.resolve(json({ items: [feedback], total: 1 }))
  )
  render(<FeedbackPage />)
  await screen.findByText('Current row')
  fireEvent.click(screen.getByRole('button', { name: 'voteAction' }))
  fireEvent.click(screen.getByRole('button', { name: 'sortDate' }))
  await waitFor(() =>
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
  )
  expect(listCalls()).toHaveLength(2)
  expect(listCalls()[1][0]).toContain('sort=date')
  expect(screen.getByRole('button', { name: 'voteAction' })).toBeDisabled()
  mocks.apiFetch.mockReturnValue(refresh.promise)
  await act(async () => {
    vote.resolve(json({ voted: true, vote_count: 1 }))
  })
  await waitFor(() => expect(listCalls()).toHaveLength(3))
  expect(listCalls()[2][0]).toContain('sort=date')
  expect(screen.getByText('Current row')).toBeInTheDocument()
  expect(screen.getByRole('status')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'voteAction' })).toBeDisabled()
  await act(async () => {
    refresh.resolve(
      json({
        items: [{ ...feedback, voted_by_me: true, vote_count: 1 }],
        total: 1,
      })
    )
  })
  const removeVote = await screen.findByRole('button', {
    name: 'removeVoteAction',
  })
  expect(removeVote).toBeEnabled()
  expect(within(removeVote.parentElement!).getByText('1')).toBeInTheDocument()
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
})

it('does not reconcile an old session vote into a replacement session', async () => {
  const vote = deferred<Response>()
  mocks.apiFetch.mockImplementation((_path: string, options?: RequestInit) =>
    options?.method === 'POST'
      ? vote.promise
      : Promise.resolve(json({ items: [feedback], total: 1 }))
  )
  render(<FeedbackPage />)
  await screen.findByText('Current row')
  fireEvent.click(screen.getByRole('button', { name: 'voteAction' }))
  mocks.apiFetch.mockImplementation(() =>
    Promise.resolve(
      json({
        items: [{ ...feedback, title: 'New account row' }],
        total: 1,
      })
    )
  )
  act(() =>
    useAuthStore.setState((state) => ({
      sessionVersion: state.sessionVersion + 1,
    }))
  )
  await screen.findByText('New account row')
  const before = mocks.apiFetch.mock.calls.length
  await act(async () => {
    vote.resolve(json({ voted: true, vote_count: 1 }))
  })
  expect(mocks.apiFetch).toHaveBeenCalledTimes(before)
  expect(screen.getByText('New account row')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'voteAction' })).toBeEnabled()
  expect(
    screen.queryByRole('button', { name: 'removeVoteAction' })
  ).not.toBeInTheDocument()
  expect(screen.queryByRole('status')).not.toBeInTheDocument()
})

it('keeps public feedback visible while creation refreshes the same list', async () => {
  const refresh = deferred<Response>()
  mocks.apiFetch.mockImplementation(() =>
    Promise.resolve(json({ items: [feedback], total: 1 }))
  )
  render(<FeedbackPage />)
  await screen.findByText('Current row')
  fireEvent.click(screen.getByRole('button', { name: 'newFeature' }))
  fireEvent.change(screen.getByPlaceholderText('placeholderTitleFeature'), {
    target: { value: 'New suggestion' },
  })
  fireEvent.change(
    screen.getByPlaceholderText('placeholderDescriptionFeature'),
    { target: { value: 'Details' } }
  )
  mocks.apiFetch.mockImplementation((_path: string, options?: RequestInit) =>
    options?.method === 'POST'
      ? Promise.resolve(json({ id: 2 }))
      : refresh.promise
  )
  fireEvent.click(screen.getByRole('button', { name: 'submit' }))
  await screen.findByRole('status')
  expect(screen.getByText('Current row')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'voteAction' })).toBeDisabled()
  await act(async () => {
    refresh.resolve(json({ items: [feedback], total: 1 }))
  })
  expect(screen.getByRole('button', { name: 'voteAction' })).not.toBeDisabled()
})
