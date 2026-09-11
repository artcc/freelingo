'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import {
  getLanguageByCode,
  TARGET_LANGUAGE_CATALOG,
} from '@/lib/target-languages'
import TargetLanguageSelector from '@/components/TargetLanguageSelector'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { PageLoading } from '@/components/ui/page-loading'
import type { UserLanguageInfo } from '@/store/language'

export default function MyLanguagesPage() {
  const t = useTranslations('languages')
  const tTarget = useTranslations('targetLanguages')
  const tSettings = useTranslations('settings')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const userLanguages = useLanguageStore((s) => s.userLanguages)
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)
  const switchLanguage = useLanguageStore((s) => s.switchLanguage)
  const addLanguage = useLanguageStore((s) => s.addLanguage)
  const removeLanguage = useLanguageStore((s) => s.removeLanguage)

  const [addModalOpen, setAddModalOpen] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState<UserLanguageInfo | null>(
    null
  )
  const [addingCode, setAddingCode] = useState('')
  const [switchingCode, setSwitchingCode] = useState<string | null>(null)
  const [toast, setToast] = useState('')
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setLoading(true)
    await fetchLanguages()
    setLoading(false)
  }, [fetchLanguages])

  useEffect(() => {
    load()
  }, [load])

  function getLangInfo(code: string) {
    return getLanguageByCode(code)
  }

  async function handleSwitch(info: UserLanguageInfo) {
    if (info.is_active) return
    setSwitchingCode(info.target_language)
    const ok = await switchLanguage(info.target_language)
    setSwitchingCode(null)
    if (ok) {
      const level = info.plan?.cefr_level ?? ''
      setToast(
        t('switched', { language: tTarget(info.target_language), level })
      )
      setTimeout(() => setToast(''), 2500)
      router.refresh()
    }
  }

  async function handleDelete() {
    if (!deleteTarget) return
    const ok = await removeLanguage(deleteTarget.target_language)
    if (!ok) {
      setToast(
        t('deleteError', {
          language: tTarget(deleteTarget.target_language),
        })
      )
      setDeleteTarget(null)
      return
    }
    setDeleteTarget(null)
  }

  async function handleAdd() {
    if (!addingCode) return
    const ok = await addLanguage(addingCode)
    if (!ok) return
    setAddModalOpen(false)
    setAddingCode('')
    router.push(`/assessment`)
  }

  const availableLanguageCodes = useLanguageStore(
    (s) => s.availableLanguageCodes
  )
  const addedCodes = userLanguages.map((ul) => ul.target_language)
  // Only show operator-enabled languages that the user hasn't added yet
  const unusedCodes = TARGET_LANGUAGE_CATALOG.filter(
    (l) =>
      availableLanguageCodes.includes(l.code) && !addedCodes.includes(l.code)
  ).map((l) => l.code)
  const hasMultiple = userLanguages.length > 1

  return (
    <div className="mx-auto max-w-4xl p-6">
      {/* Toast */}
      {toast && (
        <div className="pointer-events-none fixed inset-x-0 top-16 z-50 flex justify-center">
          <div className="animate-in fade-in slide-in-from-top-2 border-fl-border bg-fl-surface text-fl-muted-1 pointer-events-auto border px-4 py-2 font-mono text-xs tracking-widest uppercase shadow-lg">
            {toast}
          </div>
        </div>
      )}

      {/* Breadcrumb */}
      <nav className="text-fl-label text-fl-muted-3 mb-8 flex items-center gap-2 font-mono">
        <Link
          href="/settings"
          className="hover:text-fl-fg tracking-widest uppercase transition-colors"
        >
          {tSettings('title')}
        </Link>
        <span>›</span>
        <span className="text-fl-fg tracking-widest uppercase">
          {t('myLanguages')}
        </span>
      </nav>

      {/* Header + Add button */}
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-fl-fg font-mono text-xl font-bold tracking-widest uppercase">
          {t('myLanguages')}
        </h1>
        {unusedCodes.length > 0 && (
          <button
            onClick={() => setAddModalOpen(true)}
            className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 px-4 py-2 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
          >
            + {t('addLanguage')}
          </button>
        )}
      </div>

      {/* Language cards */}
      {loading ? (
        <PageLoading />
      ) : userLanguages.length === 0 ? (
        <div className="border-fl-border bg-fl-surface border px-6 py-10 text-center">
          <p className="text-fl-muted-2 font-mono text-sm">
            {t('noLanguages')}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {[...userLanguages]
            .sort((a, b) =>
              tTarget(a.target_language).localeCompare(
                tTarget(b.target_language)
              )
            )
            .map((ulang) => {
              const lang = getLangInfo(ulang.target_language)
              const isActive = ulang.is_active
              const plan = ulang.plan
              const progress = ulang.progress

              return (
                <div
                  key={ulang.target_language}
                  className={`bg-fl-surface border p-5 ${
                    isActive ? 'border-fl-accent/50' : 'border-fl-border'
                  }`}
                >
                  {/* Top row: flag + name + status */}
                  <div className="mb-3 flex items-center gap-3">
                    {lang && (
                      <Image
                        src={lang.flagPath}
                        alt={lang.code}
                        width={28}
                        height={20}
                        className="shrink-0 object-cover"
                      />
                    )}
                    <span className="text-fl-fg flex-1 font-mono text-sm font-bold">
                      {tTarget(ulang.target_language)}
                    </span>
                    {isActive ? (
                      <span className="text-fl-label bg-fl-accent/20 text-fl-accent px-2 py-0.5 font-mono text-xs tracking-widest uppercase">
                        {t('activeLanguage')}
                      </span>
                    ) : plan?.cefr_level ? (
                      <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
                        {plan.cefr_level}
                      </span>
                    ) : null}
                  </div>

                  {/* Stats */}
                  {plan && (
                    <div className="text-fl-muted-1 mb-3 flex flex-wrap gap-x-6 gap-y-1 font-mono text-xs">
                      <span>
                        {t('levelLabel')}: {plan.cefr_level ?? '—'}
                      </span>
                      <span>
                        {t('progressLabel')}: {plan.completion_pct}%
                      </span>
                      {progress && (
                        <>
                          <span>
                            {t('xpLabel')}: {progress.total_xp.toLocaleString()}
                          </span>
                          <span>
                            {t('streakLabel')}: {progress.current_streak}d
                          </span>
                          <span>
                            {t('lessonsLabel')}: {progress.lessons_completed}
                          </span>
                        </>
                      )}
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    {isActive ? (
                      <button
                        onClick={() => router.push(`/plan`)}
                        className="text-fl-label text-fl-muted-2 hover:text-fl-fg font-mono text-xs tracking-widest uppercase transition-colors"
                      >
                        {t('viewDetails')} →
                      </button>
                    ) : (
                      <>
                        <button
                          onClick={() => handleSwitch(ulang)}
                          disabled={switchingCode === ulang.target_language}
                          className="text-fl-bg bg-fl-fg hover:bg-fl-accent/90 px-3 py-1 font-mono text-xs tracking-widest uppercase transition-colors disabled:opacity-40"
                        >
                          {switchingCode === ulang.target_language
                            ? '...'
                            : t('switchTo')}
                        </button>
                        {hasMultiple && (
                          <button
                            onClick={() => setDeleteTarget(ulang)}
                            className="text-fl-label text-fl-muted-3 hover:text-fl-error font-mono text-xs tracking-widest uppercase transition-colors"
                          >
                            {t('removeLanguage')}
                          </button>
                        )}
                      </>
                    )}
                  </div>
                </div>
              )
            })}
        </div>
      )}

      {/* Add language modal */}
      {addModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-fl-bg border-fl-border w-full max-w-lg border p-6 shadow-xl">
            <h2 className="text-fl-fg mb-4 font-mono text-sm font-bold tracking-widest uppercase">
              {t('selectLanguage')}
            </h2>
            <TargetLanguageSelector
              value={addingCode}
              onChange={setAddingCode}
              availableCodes={unusedCodes}
            />
            <div className="mt-5 flex justify-end gap-2">
              <button
                onClick={() => setAddModalOpen(false)}
                className="text-fl-label text-fl-muted-3 hover:text-fl-fg px-4 py-2 font-mono text-xs tracking-widest uppercase transition-colors"
              >
                {tCommon('cancel')}
              </button>
              <button
                onClick={handleAdd}
                disabled={!addingCode}
                className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 px-4 py-2 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
              >
                {t('addLanguage')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete confirmation */}
      <ConfirmDialog
        open={deleteTarget !== null}
        title={t('removeConfirmTitle', {
          language: deleteTarget ? tTarget(deleteTarget.target_language) : '',
        })}
        message={t('removeConfirmMessage')}
        confirmLabel={t('removeConfirmButton')}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
