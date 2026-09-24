import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'

const { mockApiFetch, translate } = vi.hoisted(() => ({
  mockApiFetch: vi.fn(),
  translate: (key: string) => key,
}))

vi.mock('next-intl', () => ({
  useTranslations: () => translate,
}))

vi.mock('@/lib/api', () => ({
  apiFetch: mockApiFetch,
}))

import FeedbackPage from '@/app/(app)/feedback/page'
import { useAuthStore } from '@/store/auth'

function jsonResponse(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

describe('FeedbackPage unread labels', () => {
  beforeEach(() => {
    mockApiFetch.mockReset()
    useAuthStore.setState({
      accessToken: 'test-token',
      user: {
        id: 1,
        username: 'student',
        displayName: 'Student',
        email: 'student@example.com',
        native_language: 'en',
        ui_locale: 'en',
        role: 'user',
        avatar: null,
        is_verified: true,
        bio: null,
        learning_goals: [],
        conversation_max_duration: 30,
        conversation_inactivity_timeout: 3,
        subscription_status: 'active',
        subscription_ends_at: null,
      },
    })
  })

  it('renders the unread label beside a feedback status badge', async () => {
    mockApiFetch.mockResolvedValue(
      jsonResponse({
        items: [
          {
            id: 10,
            type: 'feature',
            title: 'Add focused practice',
            description: 'A suggestion with unread activity.',
            status: 'pending',
            author: {
              id: 2,
              username: 'other',
              display_name: 'Other User',
            },
            vote_count: 3,
            voted_by_me: false,
            unread_by_me: true,
            comment_count: 1,
            created_at: '2026-07-04T10:00:00',
          },
        ],
        total: 1,
        skip: 0,
        limit: 20,
      })
    )

    render(<FeedbackPage />)

    await waitFor(() => expect(screen.getByText('unread')).toBeDefined())
    expect(screen.getAllByText('statusPending').length).toBeGreaterThan(0)
    expect(screen.getByText('Add focused practice')).toBeDefined()
  })

  it('updates the translated vote button label when a vote is toggled', async () => {
    const list = {
      items: [
        {
          id: 10,
          type: 'feature',
          title: 'Add focused practice',
          description: 'A suggestion.',
          status: 'pending',
          author: {
            id: 2,
            username: 'other',
            display_name: 'Other User',
          },
          vote_count: 0,
          voted_by_me: false,
          unread_by_me: false,
          comment_count: 0,
          created_at: '2026-07-04T10:00:00',
        },
      ],
      total: 1,
      skip: 0,
      limit: 20,
    }
    mockApiFetch
      .mockResolvedValueOnce(jsonResponse(list))
      .mockResolvedValueOnce(jsonResponse(list))
      .mockResolvedValueOnce(jsonResponse({ voted: true, vote_count: 1 }))

    render(<FeedbackPage />)
    const voteButton = await screen.findByRole('button', { name: 'voteAction' })
    expect(voteButton).toHaveAttribute('title', 'voteAction')
    fireEvent.click(voteButton)
    expect(
      await screen.findByRole('button', { name: 'removeVoteAction' })
    ).toHaveAttribute('title', 'removeVoteAction')
  })
})
