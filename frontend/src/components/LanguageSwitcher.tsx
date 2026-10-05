'use client'

import { useEffect, useState, useRef, useMemo } from 'react'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { useLanguageStore } from '@/store/language'
import { getLanguageByCode } from '@/lib/target-languages'

export default function LanguageSwitcher() {
  const tLang = useTranslations('languages')
  const tTarget = useTranslations('targetLanguages')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const activeLanguage = useLanguageStore((s) => s.activeLanguage)
  const userLanguages = useLanguageStore((s) => s.userLanguages)
  const isSwitching = useLanguageStore((s) => s.isSwitching)
  const needsRefresh = useLanguageStore((s) => s.needsRefresh)
  const fetchLanguages = useLanguageStore((s) => s.fetchLanguages)
  const switchLanguage = useLanguageStore((s) => s.switchLanguage)

  const [open, setOpen] = useState(false)
  const [toast, setToast] = useState(false)
  const [toastMsg, setToastMsg] = useState('')
  const [switchFailed, setSwitchFailed] = useState(false)
  const [recovering, setRecovering] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetchLanguages()
  }, [fetchLanguages])

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    if (open) {
      document.addEventListener('mousedown', handleClick)
      return () => document.removeEventListener('mousedown', handleClick)
    }
  }, [open])

  async function handleSwitch(code: string) {
    setOpen(false)
    if (code === activeLanguage?.code) return
    setToast(false)
    setSwitchFailed(false)
    // Capture target language info before switching (store will update after)
    const targetInfo = userLanguages.find((l) => l.target_language === code)
    const ok = await switchLanguage(code)
    setSwitchFailed(!ok)
    if (ok) {
      const langName = tTarget(code)
      const level = targetInfo?.plan?.cefr_level
      setToastMsg(
        level ? tLang('switched', { language: langName, level }) : langName
      )
      setToast(true)
      setTimeout(() => setToast(false), 2500)
      router.refresh()
    }
  }

  const skeleton = useMemo(
    () => (
      <div className="flex animate-pulse items-center gap-2 px-5 py-2.5">
        <div className="bg-fl-border h-3.5 w-5 rounded-sm" />
        <div className="bg-fl-border h-3 w-20 rounded" />
      </div>
    ),
    []
  )

  if (switchFailed && needsRefresh) {
    return (
      <div className="space-y-2 px-5 py-2.5">
        <p role="alert" className="text-fl-error-fg text-xs">
          {tCommon('errorMessage')}
        </p>
        <button
          disabled={recovering}
          onClick={async () => {
            setRecovering(true)
            await fetchLanguages()
            setRecovering(false)
          }}
          className="text-fl-muted-2 hover:text-fl-fg text-xs disabled:opacity-50"
        >
          {tCommon('retry')}
        </button>
      </div>
    )
  }

  if (!activeLanguage) {
    return skeleton
  }

  const multiple = userLanguages.length > 1

  return (
    <div ref={ref} className="relative w-full">
      {toast && (
        <div className="pointer-events-none fixed inset-x-0 top-16 z-50 flex justify-center">
          <div className="animate-in fade-in slide-in-from-top-2 border-fl-border bg-fl-surface text-fl-muted-1 pointer-events-auto border px-4 py-2 font-mono text-xs tracking-widest uppercase shadow-lg">
            {toastMsg}
          </div>
        </div>
      )}

      <button
        onClick={() => multiple && setOpen(!open)}
        disabled={!multiple}
        className="text-fl-muted-2 hover:text-fl-fg hover:bg-fl-surface flex w-full items-center gap-2 px-5 py-2.5 font-mono text-xs tracking-widest uppercase transition-colors"
      >
        <Image
          src={activeLanguage.flagPath}
          alt={activeLanguage.code}
          width={20}
          height={14}
          className="shrink-0 object-cover"
        />
        <span className="truncate">
          {isSwitching ? '...' : tTarget(activeLanguage.code)}
        </span>
        {multiple && (
          <span className="text-fl-label text-fl-muted-4 ml-auto">
            {open ? '▴' : '▾'}
          </span>
        )}
      </button>

      {open && multiple && (
        <div className="border-fl-border bg-fl-bg absolute top-full right-0 left-0 z-50 border py-1 shadow-lg">
          {[...userLanguages]
            .sort((a, b) =>
              tTarget(a.target_language).localeCompare(
                tTarget(b.target_language)
              )
            )
            .map((ulang) => {
              const lang = getLanguageByCode(ulang.target_language)
              if (!lang) return null
              return (
                <button
                  key={ulang.target_language}
                  onClick={() => handleSwitch(ulang.target_language)}
                  className={`flex w-full items-center gap-2 px-5 py-2.5 text-left font-mono text-xs tracking-widest uppercase transition-colors ${
                    ulang.is_active
                      ? 'text-fl-fg bg-fl-surface'
                      : 'text-fl-muted-2 hover:text-fl-fg hover:bg-fl-surface'
                  }`}
                >
                  <Image
                    src={lang.flagPath}
                    alt={lang.code}
                    width={20}
                    height={14}
                    className="shrink-0 object-cover"
                  />
                  <span className="truncate">{tTarget(lang.code)}</span>
                  {ulang.plan?.cefr_level && (
                    <span className="text-fl-label text-fl-accent ml-1 font-mono">
                      {ulang.plan.cefr_level}
                    </span>
                  )}
                  {ulang.is_active && (
                    <span className="text-fl-label text-fl-accent ml-auto">
                      ✓
                    </span>
                  )}
                </button>
              )
            })}
        </div>
      )}
    </div>
  )
}
