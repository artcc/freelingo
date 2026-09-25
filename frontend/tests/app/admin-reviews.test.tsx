import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import React from 'react'
import AdminReviewsPage from '@/app/(app)/admin/reviews/page'

vi.mock('next-intl', () => ({
  useLocale: () => 'en',
  useTranslations:
    (namespace: string) => (key: string, values?: Record<string, string | number>) => {
      if (namespace === 'targetLanguages' && key === 'de-DE') return 'German'
      if (key === 'learningLanguage') return `Learning ${values?.language}`
      if (key === 'starsLabel')
        return namespace === 'landingReviews'
          ? `${values?.rating} out of 5 stars`
          : `${values?.rating} stars`
      if (key === 'total') return `${values?.total} total`
      const labels: Record<string, string> = {
        approve: 'Approve',
        approved: 'Approved',
        cancel: 'Cancel',
        delete: 'Delete',
        pending: 'Pending',
        ratingOnly: 'Rating-only review.',
      }
      return labels[key] ?? key
    },
}))
vi.mock('next/link', () => ({
  default: ({
    href,
    children,
    ...props
  }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', { href: String(href), ...props }, children),
}))
vi.mock('next/navigation', () => ({ usePathname: () => '/admin/reviews' }))

const { mockDeleteReview, mockFetchAdminReviews, mockUpdateReviewApproval } =
  vi.hoisted(() => ({
    mockDeleteReview: vi.fn(),
    mockFetchAdminReviews: vi.fn(),
    mockUpdateReviewApproval: vi.fn(),
  }))

vi.mock('@/lib/reviews', () => ({
  deleteReview: mockDeleteReview,
  fetchAdminReviews: mockFetchAdminReviews,
  updateReviewApproval: mockUpdateReviewApproval,
}))

const review = {
  id: 7,
  user_id: 3,
  user_display_name: 'Reviewer',
  target_language: 'de-DE',
  rating: 5,
  comment: 'Strong experience',
  is_approved: false,
  created_at: '2026-06-19T10:00:00',
  updated_at: '2026-06-19T10:00:00',
}

describe('AdminReviewsPage', () => {
  beforeEach(() => {
    mockDeleteReview.mockReset().mockResolvedValue(undefined)
    mockUpdateReviewApproval
      .mockReset()
      .mockResolvedValue({ ...review, is_approved: true })
    mockFetchAdminReviews
      .mockReset()
      .mockResolvedValue({ items: [review], total: 1, skip: 0, limit: 20 })
  })

  it('renders review list', async () => {
    render(<AdminReviewsPage />)
    expect(await screen.findByText('Reviewer')).toBeDefined()
    expect(screen.getByText('Strong experience')).toBeDefined()
    expect(screen.getByText(/Learning German/)).toBeDefined()
    expect(screen.getByLabelText('5 out of 5 stars')).toBeInTheDocument()
  })

  it('calls approve action', async () => {
    render(<AdminReviewsPage />)
    fireEvent.click(await screen.findByText('Approve'))
    await waitFor(() =>
      expect(mockUpdateReviewApproval).toHaveBeenCalledWith(7, true)
    )
  })

  it('calls delete after confirmation', async () => {
    render(<AdminReviewsPage />)
    fireEvent.click(await screen.findByText('Delete'))
    const callsBeforeDelete = mockFetchAdminReviews.mock.calls.length
    const deleteButtons = screen.getAllByText('Delete')
    fireEvent.click(deleteButtons[deleteButtons.length - 1])
    await waitFor(() => expect(mockDeleteReview).toHaveBeenCalledWith(7))
    await waitFor(() =>
      expect(mockFetchAdminReviews.mock.calls.length).toBeGreaterThan(
        callsBeforeDelete
      )
    )
  })
})
