import { apiFetch } from '@/lib/api'
import type {
  PaginatedReviewsResponse,
  ReviewAdmin,
  ReviewMeResponse,
  ReviewPublic,
} from '@/types/api'

export interface CreateReviewInput {
  rating: number
  comment?: string
}

export interface AdminReviewFilters {
  isApproved?: boolean
  rating?: number
  targetLanguage?: string
  order?: 'asc' | 'desc'
  skip?: number
  limit?: number
}

async function parseOrThrow<T>(res: Response): Promise<T> {
  if (!res.ok) {
    throw new Error(`reviews_api_error_${res.status}`)
  }
  return res.json() as Promise<T>
}

export async function fetchMyReview(): Promise<ReviewMeResponse> {
  const res = await apiFetch('/api/reviews/me')
  return parseOrThrow<ReviewMeResponse>(res)
}

export async function createReview(
  data: CreateReviewInput
): Promise<ReviewAdmin> {
  const res = await apiFetch('/api/reviews', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return parseOrThrow<ReviewAdmin>(res)
}

export async function updateMyReview(
  data: CreateReviewInput
): Promise<ReviewAdmin> {
  const res = await apiFetch('/api/reviews/me', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return parseOrThrow<ReviewAdmin>(res)
}

export async function deleteMyReview(): Promise<void> {
  const res = await apiFetch('/api/reviews/me', {
    method: 'DELETE',
  })
  if (!res.ok) {
    throw new Error(`reviews_api_error_${res.status}`)
  }
}

export async function fetchPublicReviews(limit = 50): Promise<ReviewPublic[]> {
  const params = new URLSearchParams({ limit: String(limit) })
  const res = await apiFetch(`/api/reviews/public?${params.toString()}`)
  return parseOrThrow<ReviewPublic[]>(res)
}

export async function fetchAdminReviews(
  filters: AdminReviewFilters = {},
  signal?: AbortSignal
): Promise<PaginatedReviewsResponse> {
  const params = new URLSearchParams({
    order: filters.order ?? 'desc',
    skip: String(filters.skip ?? 0),
    limit: String(filters.limit ?? 10),
  })
  if (filters.isApproved !== undefined) {
    params.set('is_approved', String(filters.isApproved))
  }
  if (filters.rating !== undefined) {
    params.set('rating', String(filters.rating))
  }
  if (filters.targetLanguage) {
    params.set('target_language', filters.targetLanguage)
  }
  const res = await apiFetch(`/api/admin/reviews?${params.toString()}`, {
    signal,
  })
  return parseOrThrow<PaginatedReviewsResponse>(res)
}

export async function updateReviewApproval(
  reviewId: number,
  isApproved: boolean
): Promise<ReviewAdmin> {
  const res = await apiFetch(`/api/admin/reviews/${reviewId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ is_approved: isApproved }),
  })
  return parseOrThrow<ReviewAdmin>(res)
}

export async function deleteReview(reviewId: number): Promise<void> {
  const res = await apiFetch(`/api/admin/reviews/${reviewId}`, {
    method: 'DELETE',
  })
  if (!res.ok) {
    throw new Error(`reviews_api_error_${res.status}`)
  }
}
