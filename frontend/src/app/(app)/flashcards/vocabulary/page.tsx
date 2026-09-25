'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslations } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { AudioPlayer } from '@/components/ui/AudioPlayer'
import { PageLoading } from '@/components/ui/page-loading'
import { Pagination } from '@/components/ui/pagination'

interface VocabItem {
  id: number
  word: string
  definition: string
  example_sentence: string
  translation: string
}

const LIMIT = 10

export default function VocabularyPage() {
  const t = useTranslations('flashcards')
  const tCommon = useTranslations('common')

  const [items, setItems] = useState<VocabItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [search, setSearch] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [deletingId, setDeletingId] = useState<number | null>(null)

  // Debounce search input: reset to page 1 on new query
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search)
      setPage(1)
    }, 300)
    return () => clearTimeout(timer)
  }, [search])

  const loadPage = useCallback(async (p: number, q: string) => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: String(p),
        limit: String(LIMIT),
        search: q,
      })
      const res = await apiFetch(`/api/flashcards/vocabulary?${params}`)
      if (res.ok) {
        const data = await res.json()
        setItems(data.items)
        setTotal(data.total)
        setPage(data.page)
        setPages(data.pages)
      }
    } catch {
      /* ignore */
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadPage(page, debouncedSearch)
  }, [page, debouncedSearch, loadPage])

  async function deleteItem(id: number) {
    setDeletingId(id)
    try {
      await apiFetch(`/api/flashcards/${id}`, { method: 'DELETE' })
      // Reload current page (total may change)
      await loadPage(page, debouncedSearch)
    } catch {
      /* ignore */
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <div className="mx-auto max-w-4xl space-y-4 p-6">
      {/* Header */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <span className="text-fl-label text-fl-muted-3">●</span>
          <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
            {t('myVocabulary')}
          </span>
          {!loading && (
            <span className="text-fl-hint text-fl-muted-3 font-mono tracking-widest">
              {total}
            </span>
          )}
        </div>
        <Link
          href="/flashcards"
          className="text-fl-label text-fl-muted-3 hover:text-fl-fg border-fl-border hover:border-fl-border-2 border px-4 py-2 font-mono tracking-widest uppercase transition-colors"
        >
          ← {t('backToFlashcards')}
        </Link>
      </div>

      {/* Search */}
      <input
        type="search"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder={t('vocabularySearch')}
        className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-border-2 focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-sm transition-colors focus:outline-none"
      />

      {/* List */}
      <div className="border-fl-border bg-fl-surface border">
        {loading ? (
          <PageLoading fullScreen={false} className="block p-5" />
        ) : items.length === 0 ? (
          <p className="text-fl-muted-3 p-5 font-mono text-xs tracking-widest uppercase">
            {debouncedSearch
              ? t('myVocabularyNoResults')
              : t('myVocabularyEmpty')}
          </p>
        ) : (
          <div className="divide-fl-border divide-y">
            {items.map((item) => (
              <div
                key={item.id}
                className="flex items-start justify-between gap-4 px-5 py-3"
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <p className="text-fl-fg font-mono text-xs font-bold">
                      {item.word}
                    </p>
                    <AudioPlayer text={item.word} size="sm" />
                  </div>
                  <p className="text-fl-muted-2 mt-0.5 font-mono text-xs leading-relaxed">
                    {item.definition}
                  </p>
                  <p className="text-fl-muted-3 text-fl-label mt-1 font-mono tracking-widest uppercase">
                    {item.translation}
                  </p>
                </div>
                <button
                  onClick={() => deleteItem(item.id)}
                  disabled={deletingId === item.id}
                  className="text-fl-muted-3 shrink-0 font-mono text-xs transition-colors hover:text-red-400 disabled:opacity-40"
                  aria-label={tCommon('delete')}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Pagination */}
      <Pagination
        page={page - 1}
        totalPages={pages}
        loading={loading}
        onPageChange={(p) => setPage(p + 1)}
        prevLabel={`← ${t('vocabularyPrev')}`}
        nextLabel={`${t('vocabularyNext')} →`}
        pageInfo={t('vocabularyPageInfo', { page, pages })}
        className="gap-2 border-0 bg-transparent"
      />
    </div>
  )
}
