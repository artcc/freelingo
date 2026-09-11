'use client'

import { useState, useEffect } from 'react'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'

interface ContactFormModalProps {
  open: boolean
  onClose: () => void
}

type Status = 'idle' | 'loading' | 'success' | 'error'

export function ContactFormModal({ open, onClose }: ContactFormModalProps) {
  const t = useTranslations('contact')
  const tCommon = useTranslations('common')

  const [email, setEmail] = useState('')
  const [subject, setSubject] = useState('')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState<Status>('idle')
  const [errorMsg, setErrorMsg] = useState('')

  // Reset form when modal opens
  useEffect(() => {
    if (open) {
      setEmail('')
      setSubject('')
      setDescription('')
      setStatus('idle')
      setErrorMsg('')
    }
  }, [open])

  // Close on Escape
  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open, onClose])

  // Auto-close after success with short delay
  useEffect(() => {
    if (status !== 'success') return
    const timer = setTimeout(() => onClose(), 2000)
    return () => clearTimeout(timer)
  }, [status, onClose])

  if (!open) return null

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setStatus('loading')
    setErrorMsg('')
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, subject, description }),
      })
      if (res.status === 204) {
        setStatus('success')
      } else {
        const data = await res.json().catch(() => ({}))
        setErrorMsg(data?.detail ?? t('errorGeneric'))
        setStatus('error')
      }
    } catch {
      setErrorMsg(t('errorGeneric'))
      setStatus('error')
    }
  }

  const isLoading = status === 'loading'

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
        <div className="border-fl-border flex items-center gap-2 border-b px-6 py-4">
          <span className="text-fl-label text-fl-muted-2">●</span>
          <span className="text-fl-label text-fl-muted-2 flex-1 font-mono tracking-widest uppercase">
            {t('title')}
          </span>
          <button
            onClick={onClose}
            className="text-fl-label text-fl-muted-3 hover:text-fl-fg font-mono transition-colors"
            aria-label={tCommon('close')}
          >
            ✕
          </button>
        </div>

        {status === 'success' ? (
          /* Success state */
          <div className="flex flex-col items-center gap-3 px-6 py-10">
            <span className="text-fl-success font-mono text-sm tracking-widest uppercase">
              ✓ {t('sent')}
            </span>
          </div>
        ) : (
          /* Form */
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col gap-4 px-6 py-6">
              {/* Email */}
              <div className="flex flex-col gap-1">
                <label className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
                  {t('labelEmail')}
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isLoading}
                  className="border-fl-border bg-fl-bg text-fl-fg placeholder:text-fl-muted-3 focus:border-fl-border-2 border px-3 py-2 font-mono text-xs transition-colors focus:outline-none disabled:opacity-50"
                  placeholder={t('placeholderEmail')}
                />
              </div>

              {/* Subject */}
              <div className="flex flex-col gap-1">
                <label className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
                  {t('labelSubject')}
                </label>
                <input
                  type="text"
                  required
                  maxLength={200}
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  disabled={isLoading}
                  className="border-fl-border bg-fl-bg text-fl-fg placeholder:text-fl-muted-3 focus:border-fl-border-2 border px-3 py-2 font-mono text-xs transition-colors focus:outline-none disabled:opacity-50"
                  placeholder={t('placeholderSubject')}
                />
              </div>

              {/* Description */}
              <div className="flex flex-col gap-1">
                <label className="text-fl-muted-3 font-mono text-xs tracking-widest uppercase">
                  {t('labelDescription')}
                </label>
                <textarea
                  required
                  maxLength={5000}
                  rows={5}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  disabled={isLoading}
                  className="border-fl-border bg-fl-bg text-fl-fg placeholder:text-fl-muted-3 focus:border-fl-border-2 min-h-[98px] resize-y border px-3 py-2 font-mono text-xs transition-colors focus:outline-none disabled:opacity-50"
                  placeholder={t('placeholderDescription')}
                />
              </div>

              {/* Error */}
              {status === 'error' && (
                <p className="text-fl-error-fg font-mono text-xs leading-relaxed">
                  {errorMsg}
                </p>
              )}
            </div>

            {/* Actions */}
            <div className="flex gap-2 px-6 pb-6">
              <button
                type="button"
                onClick={onClose}
                disabled={isLoading}
                className="border-fl-border text-fl-muted-2 hover:border-fl-border-2 hover:text-fl-fg flex-1 border py-3 font-mono text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
              >
                {tCommon('cancel')}
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="bg-fl-fg text-fl-bg hover:bg-fl-fg-bright flex-1 py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-50"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 inline h-4 w-4 animate-spin" />
                    {t('sending')}
                  </>
                ) : (
                  t('send')
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
