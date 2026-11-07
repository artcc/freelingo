'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useLocale, useTranslations } from 'next-intl'
import {
  CheckCircle2,
  FilterX,
  Loader2,
  Star,
  Trash2,
  XCircle,
} from 'lucide-react'
import { AdminNav } from '@/components/admin/AdminNav'
import {
  AdminBadge,
  AdminMetric,
  AdminPageHeader,
  AdminPanel,
} from '@/components/admin/AdminShell'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { Pagination } from '@/components/ui/pagination'
import {
  deleteReview,
  fetchAdminReviews,
  updateReviewApproval,
} from '@/lib/reviews'
import { getLanguageByCode } from '@/lib/target-languages'
import type { ReviewAdmin } from '@/types/api'
import { useAuthStore } from '@/store/auth'

const PAGE_SIZE = 10

type ApprovalFilter = 'all' | 'pending' | 'approved'

function formatDate(iso: string, locale: string): string {
  return new Date(iso).toLocaleDateString(locale, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function stars(rating: number): string {
  return '★'.repeat(rating) + '☆'.repeat(Math.max(0, 5 - rating))
}

export default function AdminReviewsPage() {
  const sessionVersion = useAuthStore((s) => s.sessionVersion)
  return <AdminReviewsContent key={sessionVersion} />
}

function AdminReviewsContent() {
  const t = useTranslations('adminReviews')
  const tCommon = useTranslations('common')
  const tAdmin = useTranslations('admin')
  const tTarget = useTranslations('targetLanguages')
  const tStars = useTranslations('landingReviews')
  const locale = useLocale()

  function languageLabel(code: string): string {
    const language = getLanguageByCode(code)
    return language ? tTarget(language.code) : code
  }
  const [reviews, setReviews] = useState<ReviewAdmin[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(0)
  const [approvalFilter, setApprovalFilter] = useState<ApprovalFilter>('all')
  const [ratingFilter, setRatingFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [savingId, setSavingId] = useState<number | null>(null)
  const [deletePending, setDeletePending] = useState<ReviewAdmin | null>(null)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const loadController = useRef<AbortController | null>(null)
  const listContext = useRef('')
  const [reload, setReload] = useState(0)

  const loadReviews = useCallback(
    async (pageIndex: number, approval: ApprovalFilter, rating: string) => {
      loadController.current?.abort()
      const controller = new AbortController()
      loadController.current = controller
      const signal = AbortSignal.any([
        controller.signal,
        AbortSignal.timeout(20_000),
      ])
      const context = JSON.stringify([pageIndex, approval, rating])
      if (listContext.current !== context) {
        setReviews([])
        setTotal(0)
        listContext.current = context
      }
      setLoading(true)
      setError('')
      try {
        const data = await fetchAdminReviews(
          {
            isApproved:
              approval === 'all' ? undefined : approval === 'approved',
            rating: rating ? Number(rating) : undefined,
            skip: pageIndex * PAGE_SIZE,
            limit: PAGE_SIZE,
          },
          signal
        )
        signal.throwIfAborted()
        if (loadController.current !== controller) return
        setReviews(data.items)
        setTotal(data.total)
      } catch {
        if (loadController.current === controller) setError(t('loadError'))
      } finally {
        if (loadController.current === controller) setLoading(false)
      }
    },
    [t]
  )

  useEffect(() => {
    loadReviews(page, approvalFilter, ratingFilter)
    return () => {
      loadController.current?.abort()
      loadController.current = null
    }
  }, [loadReviews, page, approvalFilter, ratingFilter, reload])

  async function handleApproval(review: ReviewAdmin, isApproved: boolean) {
    if (loading || savingId !== null || deletingId !== null) return
    const owner = loadController.current
    setSavingId(review.id)
    setError('')
    try {
      const updated = await updateReviewApproval(review.id, isApproved)
      if (loadController.current !== owner) {
        if (loadController.current) setReload((value) => value + 1)
        return
      }
      if (
        (approvalFilter === 'approved' && !isApproved) ||
        (approvalFilter === 'pending' && isApproved)
      ) {
        await loadReviews(page, approvalFilter, ratingFilter)
      } else {
        setReviews((prev) =>
          prev.map((item) => (item.id === review.id ? updated : item))
        )
      }
    } catch {
      if (loadController.current === owner) setError(t('updateError'))
    } finally {
      if (loadController.current) setSavingId(null)
    }
  }

  async function handleDelete(review: ReviewAdmin) {
    if (loading || savingId !== null || deletingId !== null) return
    const owner = loadController.current
    setDeletingId(review.id)
    setError('')
    try {
      await deleteReview(review.id)
      if (!loadController.current) return
      setDeletePending(null)
      if (loadController.current !== owner) {
        setReload((value) => value + 1)
        return
      }
      const nextTotal = total - 1
      const maxPage = Math.max(0, Math.ceil(nextTotal / PAGE_SIZE) - 1)
      const nextPage = Math.min(page, maxPage)
      setTotal(nextTotal)
      setReviews((prev) => prev.filter((item) => item.id !== review.id))
      if (page !== nextPage) setPage(nextPage)
      else await loadReviews(nextPage, approvalFilter, ratingFilter)
    } catch {
      if (loadController.current === owner) setError(t('deleteError'))
    } finally {
      if (loadController.current) setDeletingId(null)
    }
  }

  function clearFilters() {
    setApprovalFilter('all')
    setRatingFilter('')
    if (page !== 0) setPage(0)
  }

  const approvedCount = reviews.filter((review) => review.is_approved).length
  const pendingCount = reviews.filter((review) => !review.is_approved).length
  const approvalFilterOptions: { value: ApprovalFilter; label: string }[] =
    useMemo(
      () => [
        { value: 'all', label: t('allReviews') },
        ...[
          { value: 'pending' as const, label: t('pending') },
          { value: 'approved' as const, label: t('approved') },
        ].sort((a, b) => a.label.localeCompare(b.label)),
      ],
      [t]
    )

  return (
    <div className="mx-auto max-w-6xl space-y-4 p-6">
      <AdminPageHeader
        title={t('title')}
        eyebrow={`${tAdmin('title')} / ${tAdmin('reviews')}`}
      />

      <AdminNav />

      <div className="grid gap-3 md:grid-cols-3">
        <AdminMetric label={t('totalFiltered')} value={total} icon={Star} />
        <AdminMetric
          label={t('approvedOnPage')}
          value={approvedCount}
          icon={CheckCircle2}
        />
        <AdminMetric
          label={t('pendingOnPage')}
          value={pendingCount}
          icon={XCircle}
        />
      </div>

      <AdminPanel title={t('filters')}>
        <div className="grid gap-3 p-4 md:grid-cols-[1fr_1fr_auto]">
          <select
            value={approvalFilter}
            onChange={(event) => {
              setPage(0)
              setApprovalFilter(event.target.value as ApprovalFilter)
            }}
            className="border-fl-border bg-fl-bg text-fl-fg border px-3 py-2 font-mono text-sm"
            aria-label={t('approvalFilter')}
          >
            {approvalFilterOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <select
            value={ratingFilter}
            onChange={(event) => {
              setPage(0)
              setRatingFilter(event.target.value)
            }}
            className="border-fl-border bg-fl-bg text-fl-fg border px-3 py-2 font-mono text-sm"
            aria-label={t('ratingFilter')}
          >
            <option value="">{t('allRatings')}</option>
            {[5, 4, 3, 2, 1].map((rating) => (
              <option key={rating} value={rating}>
                {t('starsOption', { rating })}
              </option>
            ))}
          </select>
          <button
            type="button"
            onClick={clearFilters}
            className="border-fl-border text-fl-label text-fl-muted-2 hover:text-fl-fg flex items-center justify-center gap-2 border px-4 py-2 font-mono tracking-widest uppercase"
          >
            <FilterX className="size-3.5" /> {t('clear')}
          </button>
        </div>
      </AdminPanel>

      {error && (
        <div className="border-fl-error text-fl-error-fg border px-4 py-3 font-mono text-sm">
          {error}
          <button
            onClick={() => loadReviews(page, approvalFilter, ratingFilter)}
            disabled={loading}
            className="ml-3 underline disabled:opacity-50"
          >
            {tCommon('retry')}
          </button>
        </div>
      )}

      <AdminPanel
        title={t('queue')}
        meta={<AdminBadge>{t('total', { total })}</AdminBadge>}
      >
        {loading && (
          <PageLoading
            fullScreen={false}
            label={t('loading')}
            className="p-4"
          />
        )}
        {reviews.length === 0 ? (
          !loading &&
          !error && (
            <div className="text-fl-muted-2 p-8 text-center font-mono text-sm">
              {t('empty')}
            </div>
          )
        ) : (
          <div className="divide-fl-border divide-y">
            {reviews.map((review) => (
              <article
                key={review.id}
                className="grid gap-4 p-5 lg:grid-cols-[1fr_auto]"
              >
                <div className="min-w-0 space-y-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="text-fl-fg font-sans text-sm font-semibold tracking-tight">
                      {review.user_display_name}
                    </h2>
                    <AdminBadge
                      tone={review.is_approved ? 'success' : 'warning'}
                    >
                      {review.is_approved ? t('approved') : t('pending')}
                    </AdminBadge>
                    <span
                      className="text-fl-muted-2 font-mono text-xs"
                      aria-label={tStars('starsLabel', {
                        rating: review.rating,
                      })}
                    >
                      {stars(review.rating)}
                    </span>
                  </div>
                  <p className="text-fl-hint text-fl-muted-3 font-mono tracking-widest uppercase">
                    {t('learningLanguage', {
                      language: languageLabel(review.target_language),
                    })}{' '}
                    · {formatDate(review.created_at, locale)}
                  </p>
                  <p className="text-fl-muted-1 font-mono text-sm leading-relaxed">
                    {review.comment || t('ratingOnly')}
                  </p>
                </div>
                <div className="flex flex-wrap items-start gap-2 lg:justify-end">
                  <button
                    type="button"
                    onClick={() => handleApproval(review, !review.is_approved)}
                    disabled={
                      loading || savingId !== null || deletingId !== null
                    }
                    className="border-fl-border text-fl-label text-fl-muted-1 hover:text-fl-fg flex items-center gap-2 border px-3 py-2 font-mono tracking-widest uppercase disabled:opacity-60"
                  >
                    {savingId === review.id ? (
                      <Loader2 className="size-3.5 animate-spin" />
                    ) : null}
                    {review.is_approved ? t('unapprove') : t('approve')}
                  </button>
                  <button
                    type="button"
                    onClick={() => setDeletePending(review)}
                    disabled={
                      loading || savingId !== null || deletingId !== null
                    }
                    className="border-fl-error/30 text-fl-error-fg text-fl-label hover:bg-fl-error/10 flex items-center gap-2 border px-3 py-2 font-mono tracking-widest uppercase disabled:opacity-60"
                  >
                    <Trash2 className="size-3.5" /> {t('delete')}
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </AdminPanel>

      <Pagination
        page={page}
        totalPages={Math.ceil(total / PAGE_SIZE)}
        onPageChange={setPage}
        prevLabel={t('prev')}
        nextLabel={t('next')}
      />

      <ConfirmDialog
        open={!!deletePending}
        title={t('deleteTitle')}
        message={t('deleteMessage')}
        confirmLabel={t('delete')}
        danger
        confirming={deletingId !== null}
        onCancel={() => setDeletePending(null)}
        onConfirm={() => deletePending && handleDelete(deletePending)}
      />
    </div>
  )
}
