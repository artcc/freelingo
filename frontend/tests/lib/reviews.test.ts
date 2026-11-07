import { beforeEach, describe, expect, it, vi } from 'vitest'

const { mockApiFetch } = vi.hoisted(() => ({ mockApiFetch: vi.fn() }))

vi.mock('@/lib/api', () => ({ apiFetch: mockApiFetch }))

import {
  createReview,
  deleteMyReview,
  deleteReview,
  fetchAdminReviews,
  fetchMyReview,
  fetchPublicReviews,
  updateMyReview,
  updateReviewApproval,
} from '@/lib/reviews'

function jsonResponse(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

describe('reviews API client', () => {
  beforeEach(() => mockApiFetch.mockReset())

  it('fetches current user review state', async () => {
    mockApiFetch.mockResolvedValueOnce(
      jsonResponse({ has_review: false, review: null })
    )
    await expect(fetchMyReview()).resolves.toEqual({
      has_review: false,
      review: null,
    })
    expect(mockApiFetch).toHaveBeenCalledWith('/api/reviews/me')
  })

  it('creates a review', async () => {
    mockApiFetch.mockResolvedValueOnce(jsonResponse({ id: 1, rating: 5 }))
    await createReview({ rating: 5, comment: 'Nice' })
    expect(mockApiFetch).toHaveBeenCalledWith('/api/reviews', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rating: 5, comment: 'Nice' }),
    })
  })

  it('updates and deletes the current user review', async () => {
    mockApiFetch
      .mockResolvedValueOnce(jsonResponse({ id: 1, rating: 4 }))
      .mockResolvedValueOnce(new Response(null, { status: 204 }))
    await updateMyReview({ rating: 4, comment: 'Updated' })
    await deleteMyReview()
    expect(mockApiFetch).toHaveBeenNthCalledWith(1, '/api/reviews/me', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rating: 4, comment: 'Updated' }),
    })
    expect(mockApiFetch).toHaveBeenNthCalledWith(2, '/api/reviews/me', {
      method: 'DELETE',
    })
  })

  it('fetches public reviews with a limit', async () => {
    mockApiFetch.mockResolvedValueOnce(jsonResponse([]))
    await fetchPublicReviews(3)
    expect(mockApiFetch).toHaveBeenCalledWith('/api/reviews/public?limit=3')
  })

  it('fetches admin reviews with filters', async () => {
    mockApiFetch.mockResolvedValueOnce(
      jsonResponse({ items: [], total: 0, skip: 0, limit: 20 })
    )
    await fetchAdminReviews({
      isApproved: true,
      rating: 5,
      targetLanguage: 'es-ES',
    })
    expect(mockApiFetch.mock.calls[0][0]).toContain('/api/admin/reviews?')
    expect(mockApiFetch.mock.calls[0][0]).toContain('is_approved=true')
    expect(mockApiFetch.mock.calls[0][0]).toContain('rating=5')
    expect(mockApiFetch.mock.calls[0][0]).toContain('target_language=es-ES')
  })

  it('passes an optional cancellation signal to admin review reads', async () => {
    const controller = new AbortController()
    mockApiFetch.mockResolvedValueOnce(jsonResponse({ items: [], total: 0 }))
    await fetchAdminReviews({}, controller.signal)
    expect(mockApiFetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/admin/reviews?'),
      { signal: controller.signal }
    )
  })

  it('updates approval and deletes reviews', async () => {
    mockApiFetch
      .mockResolvedValueOnce(jsonResponse({ id: 2 }))
      .mockResolvedValueOnce(new Response(null, { status: 204 }))
    await updateReviewApproval(2, true)
    await deleteReview(2)
    expect(mockApiFetch).toHaveBeenNthCalledWith(1, '/api/admin/reviews/2', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_approved: true }),
    })
    expect(mockApiFetch).toHaveBeenNthCalledWith(2, '/api/admin/reviews/2', {
      method: 'DELETE',
    })
  })
})
