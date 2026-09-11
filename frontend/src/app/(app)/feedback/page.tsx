'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import { Pagination } from '@/components/ui/pagination'
import { AdminAuthorBadge } from '@/components/feedback/AdminAuthorBadge'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface FeedbackAuthor {
  id: number
  username: string
  display_name: string
  role: 'admin' | 'user'
}

interface FeedbackEntry {
  id: number
  type: 'feature' | 'bug'
  title: string
  description: string
  status: string
  author: FeedbackAuthor
  vote_count: number
  voted_by_me: boolean
  unread_by_me: boolean
  comment_count: number
  created_at: string
}

interface FeedbackComment {
  id: number
  entry_id: number
  author: FeedbackAuthor
  body: string
  created_at: string
}

type Tab = 'feature' | 'bug'
type SortOption = 'votes' | 'date'

const PAGE_SIZE = 10

const STATUS_STYLES: Record<string, string> = {
  pending: 'border-fl-border text-fl-muted-2',
  planned: 'border-blue-500/40 text-blue-400',
  in_progress: 'border-yellow-500/40 text-yellow-400',
  done: 'border-green-500/40 text-green-400',
  declined: 'border-fl-error/30 text-fl-error-fg',
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function StatusBadge({ status, label }: { status: string; label: string }) {
  const cls = STATUS_STYLES[status] ?? STATUS_STYLES.pending
  return (
    <span
      className={`text-fl-hint border px-2 py-0.5 font-mono tracking-widest uppercase ${cls}`}
    >
      {label}
    </span>
  )
}

// ---------------------------------------------------------------------------
// Create modal
// ---------------------------------------------------------------------------

interface CreateModalProps {
  type: Tab
  onClose: () => void
  onCreated: () => void
}

function CreateModal({ type, onClose, onCreated }: CreateModalProps) {
  const t = useTranslations('feedback')
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const inputCls =
    'w-full bg-fl-bg border border-fl-border px-4 py-3 font-mono text-xs text-fl-fg placeholder:text-fl-muted-4 focus:outline-none focus:border-fl-border-2 transition-colors resize-none'
  const textareaCls =
    'w-full bg-fl-bg border border-fl-border px-4 py-3 font-mono text-xs text-fl-fg placeholder:text-fl-muted-4 focus:outline-none focus:border-fl-border-2 transition-colors resize-y min-h-[106px]'

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      const res = await apiFetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type,
          title: title.trim(),
          description: description.trim(),
        }),
      })
      if (!res.ok) throw new Error()
      onCreated()
    } catch {
      setError(t('errorSubmit'))
    } finally {
      setSubmitting(false)
    }
  }

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  return (
    <div
      className="fixed inset-0 z-[200] flex items-center justify-center p-4"
      style={{
        backgroundColor: 'rgba(0,0,0,0.7)',
        backdropFilter: 'blur(2px)',
      }}
      onClick={onClose}
    >
      <div
        className="border-fl-border bg-fl-surface w-full max-w-md border shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="border-fl-border flex items-center justify-between border-b px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="text-fl-label text-fl-muted-2">●</span>
            <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
              {type === 'feature'
                ? t('modalCreateTitleFeature')
                : t('modalCreateTitleBug')}
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-fl-label text-fl-muted-2 hover:text-fl-fg font-mono transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-3 p-6">
          {error && (
            <div className="border-fl-error/40 text-fl-error border px-4 py-3 font-mono text-xs">
              ✕ {error}
            </div>
          )}
          <div>
            <label className="text-fl-muted-2 mb-1 block font-mono text-xs tracking-widest uppercase">
              {t('labelTitle')}
            </label>
            <input
              type="text"
              required
              maxLength={200}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder={
                type === 'feature'
                  ? t('placeholderTitleFeature')
                  : t('placeholderTitleBug')
              }
              className={inputCls}
              autoFocus
            />
          </div>
          <div>
            <label className="text-fl-muted-2 mb-1 block font-mono text-xs tracking-widest uppercase">
              {t('labelDescription')}
            </label>
            <textarea
              required
              maxLength={5000}
              rows={5}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={
                type === 'feature'
                  ? t('placeholderDescriptionFeature')
                  : t('placeholderDescriptionBug')
              }
              className={textareaCls}
            />
          </div>
          <div className="flex gap-2 pt-1">
            <button
              type="button"
              onClick={onClose}
              className="border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 flex-1 border px-4 py-3 font-mono text-xs tracking-widest uppercase transition-colors"
            >
              {t('cancel')}
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 flex-1 py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
            >
              {submitting ? t('submitting') : t('submit')}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Detail view
// ---------------------------------------------------------------------------

interface DetailViewProps {
  entry: FeedbackEntry
  currentUserId: number | undefined
  isAdmin: boolean
  getStatusLabel: (status: string) => string
  onBack: () => void
  onVoteToggled: (entryId: number, voted: boolean, voteCount: number) => void
  onEntryRead: (entryId: number) => void
  onEntryDeleted: (entryId: number) => void
}

function DetailView({
  entry: initialEntry,
  currentUserId,
  isAdmin,
  getStatusLabel,
  onBack,
  onVoteToggled,
  onEntryRead,
  onEntryDeleted,
}: DetailViewProps) {
  const t = useTranslations('feedback')
  const [entry, setEntry] = useState(initialEntry)
  const [comments, setComments] = useState<FeedbackComment[]>([])
  const [commentBody, setCommentBody] = useState('')
  const [postingComment, setPostingComment] = useState(false)
  const [deletePendingComment, setDeletePendingComment] =
    useState<FeedbackComment | null>(null)
  const [deleteEntryPending, setDeleteEntryPending] = useState(false)
  const [voting, setVoting] = useState(false)
  const [error, setError] = useState('')

  // Load comments on mount
  useEffect(() => {
    apiFetch(`/api/feedback/${entry.id}/read`, { method: 'POST' })
      .then((r) => {
        if (r.ok) {
          onEntryRead(entry.id)
          window.dispatchEvent(new Event('freelingo:feedback-read'))
        }
      })
      .catch(() => {})

    apiFetch(`/api/feedback/${entry.id}/comments`)
      .then((r) => r.json())
      .then((d) => setComments(d.items ?? []))
      .catch(() => {})
  }, [entry.id, onEntryRead])

  async function handleVote() {
    if (voting) return
    setVoting(true)
    try {
      const res = await apiFetch(`/api/feedback/${entry.id}/vote`, {
        method: 'POST',
      })
      if (res.ok) {
        const data = await res.json()
        setEntry((e) => ({
          ...e,
          voted_by_me: data.voted,
          vote_count: data.vote_count,
        }))
        onVoteToggled(entry.id, data.voted, data.vote_count)
      }
    } finally {
      setVoting(false)
    }
  }

  async function handlePostComment(e: React.FormEvent) {
    e.preventDefault()
    if (!commentBody.trim()) return
    setPostingComment(true)
    setError('')
    try {
      const res = await apiFetch(`/api/feedback/${entry.id}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ body: commentBody.trim() }),
      })
      if (!res.ok) throw new Error()
      const comment: FeedbackComment = await res.json()
      setComments((prev) => [...prev, comment])
      setEntry((e) => ({ ...e, comment_count: e.comment_count + 1 }))
      setCommentBody('')
    } catch {
      setError(t('errorSubmit'))
    } finally {
      setPostingComment(false)
    }
  }

  async function handleDeleteComment(comment: FeedbackComment) {
    await apiFetch(`/api/feedback/${entry.id}/comments/${comment.id}`, {
      method: 'DELETE',
    })
    setComments((prev) => prev.filter((c) => c.id !== comment.id))
    setEntry((e) => ({ ...e, comment_count: Math.max(0, e.comment_count - 1) }))
    setDeletePendingComment(null)
  }

  async function handleDeleteEntry() {
    await apiFetch(`/api/feedback/${entry.id}`, { method: 'DELETE' })
    setDeleteEntryPending(false)
    onEntryDeleted(entry.id)
    onBack()
  }

  const statusLabel = getStatusLabel(entry.status)

  return (
    <div className="space-y-4">
      {/* Back */}
      <button
        onClick={onBack}
        className="text-fl-label text-fl-muted-1 hover:text-fl-fg font-mono tracking-widest uppercase transition-colors"
      >
        {t('backToList')}
      </button>

      {/* Entry card */}
      <div className="border-fl-border bg-fl-surface border">
        <div className="border-fl-border space-y-3 border-b px-6 py-5">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <h2 className="text-fl-fg min-w-0 flex-1 font-mono text-base leading-snug font-bold">
              {entry.title}
            </h2>
            <StatusBadge status={entry.status} label={statusLabel} />
          </div>
          <p className="text-fl-muted-1 font-mono text-xs leading-relaxed whitespace-pre-wrap">
            {entry.description}
          </p>
          <div className="flex flex-wrap items-center gap-3 pt-1">
            <span className="text-fl-hint text-fl-muted-4 inline-flex flex-wrap items-center gap-x-1 font-mono">
              <span>
                {t('by')} {entry.author.display_name}
              </span>
              <AdminAuthorBadge role={entry.author.role} />
              <span>· {formatDate(entry.created_at)}</span>
            </span>
            {/* Vote button — only for features */}
            {entry.type === 'feature' && (
              <button
                onClick={handleVote}
                disabled={voting}
                className={`text-fl-hint border px-3 py-1 font-mono tracking-widest uppercase transition-colors disabled:opacity-50 ${
                  entry.voted_by_me
                    ? 'border-fl-accent/60 text-fl-accent bg-fl-accent/10'
                    : 'border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg'
                }`}
              >
                ▲ {entry.vote_count}
              </button>
            )}
            {/* Delete — author or admin */}
            {(currentUserId === entry.author.id || isAdmin) && (
              <button
                onClick={() => setDeleteEntryPending(true)}
                className="text-fl-hint border-fl-error/30 text-fl-error-fg hover:border-fl-error ml-auto border px-3 py-1 font-mono tracking-widest uppercase transition-colors"
              >
                {t('deleteEntry')}
              </button>
            )}
          </div>
        </div>

        {/* Comments */}
        <div className="divide-fl-border divide-y">
          {comments.length === 0 ? (
            <p className="text-fl-muted-4 px-6 py-6 text-center font-mono text-xs">
              {t('addComment')}
            </p>
          ) : (
            comments.map((c) => (
              <div key={c.id} className="space-y-1 px-6 py-4">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-fl-hint text-fl-muted-2 inline-flex flex-wrap items-center gap-x-1 font-mono">
                    <span>{c.author.display_name}</span>
                    <AdminAuthorBadge role={c.author.role} />
                    <span>· {formatDate(c.created_at)}</span>
                  </span>
                  {currentUserId === c.author.id && (
                    <button
                      onClick={() => setDeletePendingComment(c)}
                      className="text-fl-hint text-fl-muted-4 hover:text-fl-error-fg font-mono tracking-widest uppercase transition-colors"
                    >
                      {t('deleteComment')}
                    </button>
                  )}
                </div>
                <p className="text-fl-muted-1 font-mono text-xs leading-relaxed whitespace-pre-wrap">
                  {c.body}
                </p>
              </div>
            ))
          )}
        </div>

        {/* Add comment form */}
        <form
          onSubmit={handlePostComment}
          className="border-fl-border space-y-2 border-t px-6 py-4"
        >
          {error && (
            <div className="border-fl-error/40 text-fl-error border px-4 py-2 font-mono text-xs">
              ✕ {error}
            </div>
          )}
          <textarea
            rows={2}
            value={commentBody}
            onChange={(e) => setCommentBody(e.target.value)}
            placeholder={t('commentPlaceholder')}
            maxLength={2000}
            className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 min-h-[50px] w-full resize-y border px-4 py-2 font-mono text-xs transition-colors focus:outline-none"
          />
          <button
            type="submit"
            disabled={postingComment || !commentBody.trim()}
            className="border-fl-border text-fl-muted-1 hover:text-fl-fg hover:border-fl-border-2 border px-4 py-2 font-mono text-sm tracking-widest uppercase transition-colors disabled:cursor-not-allowed disabled:opacity-30"
          >
            {postingComment ? t('postingComment') : t('postComment')}
          </button>
        </form>
      </div>

      {/* Confirm delete entry */}
      <ConfirmDialog
        open={deleteEntryPending}
        title={t('deleteEntryConfirmTitle')}
        message={t('deleteEntryConfirmMessage')}
        confirmLabel={t('deleteEntryConfirm')}
        danger
        onConfirm={handleDeleteEntry}
        onCancel={() => setDeleteEntryPending(false)}
      />

      {/* Confirm delete comment */}
      <ConfirmDialog
        open={deletePendingComment !== null}
        title={t('deleteCommentConfirmTitle')}
        message={t('deleteCommentConfirmMessage')}
        confirmLabel={t('deleteCommentConfirm')}
        danger
        onConfirm={() =>
          deletePendingComment && handleDeleteComment(deletePendingComment)
        }
        onCancel={() => setDeletePendingComment(null)}
      />
    </div>
  )
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export default function FeedbackPage() {
  const t = useTranslations('feedback')
  const currentUserId = useAuthStore((s) => s.user?.id)
  const isAdmin = useAuthStore((s) => s.user?.role === 'admin')

  const [tab, setTab] = useState<Tab>('feature')
  const [sort, setSort] = useState<SortOption>('votes')
  const [statusFilter, setStatusFilter] = useState<string>('')
  const [entries, setEntries] = useState<FeedbackEntry[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showCreate, setShowCreate] = useState(false)

  // Detail view
  const [selectedEntry, setSelectedEntry] = useState<FeedbackEntry | null>(null)

  // Delete confirm (from list)
  const [deletePending, setDeletePending] = useState<FeedbackEntry | null>(null)

  const loadEntries = useCallback(
    async (
      pageIndex: number,
      currentTab: Tab,
      currentSort: SortOption,
      currentStatus: string
    ) => {
      setLoading(true)
      setError('')
      try {
        const params = new URLSearchParams({
          type: currentTab,
          sort: currentSort,
          order: 'desc',
          skip: String(pageIndex * PAGE_SIZE),
          limit: String(PAGE_SIZE),
        })
        if (currentStatus) params.set('status', currentStatus)
        const res = await apiFetch(`/api/feedback?${params.toString()}`)
        if (!res.ok) throw new Error()
        const data = await res.json()
        setEntries(data.items)
        setTotal(data.total)
      } catch {
        setError(t('errorLoad'))
      } finally {
        setLoading(false)
      }
    },
    [t]
  )

  // Reload when page changes
  useEffect(() => {
    loadEntries(page, tab, sort, statusFilter)
  }, [loadEntries, page]) // eslint-disable-line react-hooks/exhaustive-deps

  // Reset to page 0 when tab/sort/filter changes
  useEffect(() => {
    if (page !== 0) {
      setPage(0)
    } else {
      loadEntries(0, tab, sort, statusFilter)
    }
  }, [tab, sort, statusFilter]) // eslint-disable-line react-hooks/exhaustive-deps

  function handleVoteToggled(
    entryId: number,
    voted: boolean,
    voteCount: number
  ) {
    setEntries((prev) =>
      prev.map((e) =>
        e.id === entryId
          ? { ...e, voted_by_me: voted, vote_count: voteCount }
          : e
      )
    )
  }

  const handleEntryRead = useCallback((entryId: number) => {
    setEntries((prev) =>
      prev.map((e) => (e.id === entryId ? { ...e, unread_by_me: false } : e))
    )
    setSelectedEntry((entry) =>
      entry?.id === entryId ? { ...entry, unread_by_me: false } : entry
    )
  }, [])

  function handleEntryDeleted(entryId: number) {
    const newTotal = total - 1
    setTotal(newTotal)
    setEntries((prev) => prev.filter((e) => e.id !== entryId))
    const maxPage = Math.max(0, Math.ceil(newTotal / PAGE_SIZE) - 1)
    const targetPage = Math.min(page, maxPage)
    if (targetPage !== page) {
      setPage(targetPage)
    } else {
      loadEntries(targetPage, tab, sort, statusFilter)
    }
  }

  async function handleDeleteFromList(entry: FeedbackEntry) {
    await apiFetch(`/api/feedback/${entry.id}`, { method: 'DELETE' })
    setDeletePending(null)
    handleEntryDeleted(entry.id)
  }

  const statusOptions = useMemo(
    () => [
      { value: '', label: t('filterAll') },
      ...[
        { value: 'pending', label: t('statusPending') },
        { value: 'planned', label: t('statusPlanned') },
        { value: 'in_progress', label: t('statusInProgress') },
        { value: 'done', label: t('statusDone') },
        { value: 'declined', label: t('statusDeclined') },
      ].sort((a, b) => a.label.localeCompare(b.label)),
    ],
    [t]
  )

  function getStatusLabel(status: string) {
    return statusOptions.find((o) => o.value === status)?.label ?? status
  }

  // If a detail view is open, render it instead
  if (selectedEntry) {
    return (
      <div className="mx-auto max-w-4xl p-6">
        <DetailView
          entry={selectedEntry}
          currentUserId={currentUserId}
          isAdmin={isAdmin}
          getStatusLabel={getStatusLabel}
          onBack={() => setSelectedEntry(null)}
          onVoteToggled={handleVoteToggled}
          onEntryRead={handleEntryRead}
          onEntryDeleted={handleEntryDeleted}
        />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-4xl space-y-4 p-6">
      {/* Page header */}
      <div className="border-fl-border border-b pb-4">
        <p className="text-fl-label text-fl-muted-2 mb-1 font-mono tracking-widest uppercase">
          {t('title')}
        </p>
        <h1 className="text-fl-fg font-mono text-2xl font-bold tracking-tight">
          {t('subtitle')}
        </h1>
      </div>

      {/* Tabs */}
      <div className="border-fl-border flex border-b">
        {(['feature', 'bug'] as Tab[]).map((tabOption) => (
          <button
            key={tabOption}
            onClick={() => setTab(tabOption)}
            className={`-mb-px border-b-2 px-5 py-2 font-mono text-xs tracking-widest uppercase transition-colors ${
              tab === tabOption
                ? 'border-fl-fg text-fl-fg'
                : 'text-fl-muted-2 hover:text-fl-fg border-transparent'
            }`}
          >
            {tabOption === 'feature' ? t('tabFeatures') : t('tabBugs')}
          </button>
        ))}
        <div className="flex-1" />
        <button
          onClick={() => setShowCreate(true)}
          className="text-fl-muted-1 hover:text-fl-fg px-4 py-2 font-mono text-sm tracking-widest uppercase transition-colors"
        >
          {tab === 'feature' ? t('newFeature') : t('newBug')}
        </button>
      </div>

      {/* Filters + sort row */}
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-fl-hint text-fl-muted-4 font-mono tracking-widest uppercase">
          {t('sortBy')}
        </span>
        {(['votes', 'date'] as SortOption[]).map((s) => (
          <button
            key={s}
            onClick={() => setSort(s)}
            className={`text-fl-hint border px-3 py-1 font-mono tracking-widest uppercase transition-colors ${
              sort === s
                ? 'border-fl-fg/40 text-fl-fg'
                : 'border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg'
            }`}
          >
            {s === 'votes' ? t('sortVotes') : t('sortDate')}
          </button>
        ))}

        <span className="text-fl-hint text-fl-muted-4 ml-2 font-mono tracking-widest uppercase">
          {t('filterStatus')}
        </span>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="bg-fl-bg border-fl-border text-fl-hint text-fl-muted-1 focus:border-fl-border-2 appearance-none border px-3 py-1 font-mono transition-colors focus:outline-none"
        >
          {statusOptions.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </div>

      {/* Error */}
      {error && (
        <div className="border-fl-error/40 text-fl-error border px-4 py-3 font-mono text-xs">
          ✕ {error}
        </div>
      )}

      {/* List */}
      <div className="border-fl-border bg-fl-surface border">
        {loading ? (
          <PageLoading
            fullScreen={false}
            className="block px-6 py-10 text-center"
          />
        ) : entries.length === 0 ? (
          <p className="text-fl-muted-2 px-6 py-10 text-center font-mono text-xs">
            {t('noEntries')}
          </p>
        ) : (
          <div>
            {entries.map((entry, i) => {
              const canDelete = currentUserId === entry.author.id || isAdmin
              return (
                <div
                  key={entry.id}
                  className={`hover:bg-fl-surface-2 flex cursor-pointer gap-4 px-5 py-4 transition-colors ${
                    i < entries.length - 1 ? 'border-fl-border border-b' : ''
                  }`}
                  onClick={() => setSelectedEntry(entry)}
                >
                  {/* Vote column — only for features */}
                  {entry.type === 'feature' && (
                    <div
                      className="flex shrink-0 flex-col items-center gap-0.5 pt-0.5"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <button
                        onClick={async (e) => {
                          e.stopPropagation()
                          const res = await apiFetch(
                            `/api/feedback/${entry.id}/vote`,
                            {
                              method: 'POST',
                            }
                          )
                          if (res.ok) {
                            const data = await res.json()
                            handleVoteToggled(
                              entry.id,
                              data.voted,
                              data.vote_count
                            )
                          }
                        }}
                        className={`border px-2 py-1 font-mono text-sm leading-none transition-colors ${
                          entry.voted_by_me
                            ? 'border-fl-accent/60 text-fl-accent bg-fl-accent/10'
                            : 'border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg'
                        }`}
                        title={entry.voted_by_me ? 'Remove vote' : 'Vote'}
                      >
                        ▲
                      </button>
                      <span className="text-fl-hint text-fl-muted-2 font-mono tabular-nums">
                        {entry.vote_count}
                      </span>
                    </div>
                  )}
                  {/* Bug entries — show placeholder column for alignment */}
                  {entry.type === 'bug' && <div className="w-8 shrink-0" />}

                  {/* Content */}
                  <div className="min-w-0 flex-1 space-y-1.5">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-fl-fg truncate font-mono text-sm font-semibold">
                        {entry.title}
                      </span>
                      <StatusBadge
                        status={entry.status}
                        label={getStatusLabel(entry.status)}
                      />
                      {entry.unread_by_me && (
                        <span className="text-fl-label border border-red-500/40 px-2 py-0.5 font-mono leading-none font-bold tracking-widest text-red-400 uppercase">
                          {t('unread')}
                        </span>
                      )}
                    </div>
                    <p className="text-fl-muted-2 line-clamp-2 font-mono text-xs leading-relaxed">
                      {entry.description}
                    </p>
                    <div className="flex flex-wrap items-center gap-3">
                      <span className="text-fl-hint text-fl-muted-4 inline-flex flex-wrap items-center gap-x-1 font-mono">
                        <span>
                          {t('by')} {entry.author.display_name}
                        </span>
                        <AdminAuthorBadge role={entry.author.role} />
                        <span>· {formatDate(entry.created_at)}</span>
                      </span>
                      {entry.comment_count > 0 && (
                        <span className="text-fl-hint text-fl-muted-4 font-mono">
                          ◌{' '}
                          {entry.comment_count === 1
                            ? t('comment')
                            : t('comments', { count: entry.comment_count })}
                        </span>
                      )}
                      {canDelete && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            setDeletePending(entry)
                          }}
                          className="text-fl-hint text-fl-muted-4 hover:text-fl-error-fg ml-auto font-mono tracking-widest uppercase transition-colors"
                        >
                          {t('deleteEntry')}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Pagination */}
      <Pagination
        page={page}
        totalPages={Math.ceil(total / PAGE_SIZE)}
        onPageChange={setPage}
        prevLabel={t('prevPage')}
        nextLabel={t('nextPage')}
      />

      {/* Create modal */}
      {showCreate && (
        <CreateModal
          type={tab}
          onClose={() => setShowCreate(false)}
          onCreated={() => {
            setShowCreate(false)
            setPage(0)
            loadEntries(0, tab, sort, statusFilter)
          }}
        />
      )}

      {/* Confirm delete from list */}
      <ConfirmDialog
        open={deletePending !== null}
        title={t('deleteEntryConfirmTitle')}
        message={t('deleteEntryConfirmMessage')}
        confirmLabel={t('deleteEntryConfirm')}
        danger
        onConfirm={() => deletePending && handleDeleteFromList(deletePending)}
        onCancel={() => setDeletePending(null)}
      />
    </div>
  )
}
