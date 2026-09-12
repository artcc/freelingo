import { beforeEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import {
  ReviewPrompt,
  getReviewPromptDismissal,
} from '@/components/reviews/ReviewPrompt'

const { mockCreateReview, mockFetchMyReview } = vi.hoisted(() => ({
  mockCreateReview: vi.fn(),
  mockFetchMyReview: vi.fn(),
}))

vi.mock('@/lib/reviews', () => ({
  createReview: mockCreateReview,
  fetchMyReview: mockFetchMyReview,
}))

const translations: Record<string, string> = {
  cancel: 'Cancel',
  commentLabel: 'Comment optional',
  ratingLabel: 'Rating required',
  ratingRequiredError: 'Please choose a rating before submitting.',
  star: 'star',
  stars: 'stars',
  submit: 'Submit',
}

const translate = (key: string) => translations[key] ?? key

vi.mock('next-intl', () => ({
  useTranslations: () => translate,
}))

describe('ReviewPrompt', () => {
  beforeEach(() => {
    mockCreateReview.mockReset()
    mockFetchMyReview
      .mockReset()
      .mockResolvedValue({ has_review: false, review: null })
    window.localStorage.clear()
  })

  it('does not submit without rating', async () => {
    render(<ReviewPrompt open onClose={() => {}} />)
    await screen.findByText('Rating required')
    fireEvent.click(screen.getByText('Submit'))
    expect(mockCreateReview).not.toHaveBeenCalled()
    expect(
      screen.getByText('Please choose a rating before submitting.')
    ).toBeDefined()
  })

  it('submits rating-only reviews', async () => {
    const onClose = vi.fn()
    mockCreateReview.mockResolvedValue({ id: 1, rating: 5 })
    render(<ReviewPrompt open onClose={onClose} />)
    await screen.findByText('Rating required')
    fireEvent.click(screen.getByLabelText('5 stars'))
    await waitFor(() =>
      expect(screen.getByLabelText('5 stars')).toHaveAttribute(
        'aria-checked',
        'true'
      )
    )
    fireEvent.click(screen.getByText('Submit'))
    await waitFor(() =>
      expect(mockCreateReview).toHaveBeenCalledWith({
        rating: 5,
        comment: undefined,
      })
    )
    expect(onClose).toHaveBeenCalled()
  })

  it('submits rating plus comment', async () => {
    mockCreateReview.mockResolvedValue({ id: 1, rating: 4 })
    render(<ReviewPrompt open onClose={() => {}} />)
    await screen.findByText('Rating required')
    fireEvent.click(screen.getByLabelText('4 stars'))
    await waitFor(() =>
      expect(screen.getByLabelText('4 stars')).toHaveAttribute(
        'aria-checked',
        'true'
      )
    )
    fireEvent.change(screen.getByLabelText('Comment optional'), {
      target: { value: 'Helpful app' },
    })
    await waitFor(() =>
      expect(screen.getByLabelText('Comment optional')).toHaveValue('Helpful app')
    )
    fireEvent.click(screen.getByText('Submit'))
    await waitFor(() =>
      expect(mockCreateReview).toHaveBeenCalledWith({
        rating: 4,
        comment: 'Helpful app',
      })
    )
  })

  it('cancel stores dismissal and does not call backend create', async () => {
    const onClose = vi.fn()
    render(<ReviewPrompt open onClose={onClose} />)
    await screen.findByText('Rating required')
    fireEvent.click(screen.getByText('Cancel'))
    expect(mockCreateReview).not.toHaveBeenCalled()
    expect(onClose).toHaveBeenCalled()
    expect(getReviewPromptDismissal().count).toBe(1)
  })

  it('does not render prompt when user already has review', async () => {
    mockFetchMyReview.mockResolvedValue({ has_review: true, review: { id: 1 } })
    render(<ReviewPrompt open onClose={() => {}} />)
    await waitFor(() =>
      expect(screen.queryByText('Rating required')).toBeNull()
    )
  })

  it('does not submit when review status check fails', async () => {
    mockFetchMyReview.mockRejectedValue(new Error('network error'))
    render(<ReviewPrompt open onClose={() => {}} />)
    await screen.findByText('statusError')
    expect(screen.queryByText('Submit')).toBeNull()
    expect(mockCreateReview).not.toHaveBeenCalled()
  })
})
