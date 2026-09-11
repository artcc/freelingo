'use client'

import { useState, useEffect, useRef } from 'react'
import { useTranslations, useLocale } from 'next-intl'
import { apiFetch } from '@/lib/api'
import { clearAvatarCache } from '@/lib/avatar-cache'
import { mapUser } from '@/lib/mappers'
import { useAuthStore } from '@/store/auth'
import { SUPPORTED_LOCALES } from '@/lib/locales'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'

const LANGUAGES = [
  'en',
  'es',
  'fr',
  'pt',
  'de',
  'it',
  'pl',
  'nl',
  'ro',
  'ru',
] as const

function resizeImage(file: File, maxPx: number): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    const url = URL.createObjectURL(file)
    img.onload = () => {
      URL.revokeObjectURL(url)
      let { width, height } = img
      if (width > maxPx || height > maxPx) {
        if (width > height) {
          height = Math.round((height * maxPx) / width)
          width = maxPx
        } else {
          width = Math.round((width * maxPx) / height)
          height = maxPx
        }
      }
      const canvas = document.createElement('canvas')
      canvas.width = width
      canvas.height = height
      canvas.getContext('2d')!.drawImage(img, 0, 0, width, height)
      canvas.toBlob(
        (b) => (b ? resolve(b) : reject(new Error())),
        file.type,
        0.9
      )
    }
    img.onerror = reject
    img.src = url
  })
}

export function ProfileSection({ title }: { title?: string } = {}) {
  const t = useTranslations('settings')
  const tLang = useTranslations('languages')
  const currentLocale = useLocale()
  const user = useAuthStore((s) => s.user)
  const setUser = useAuthStore((s) => s.setUser)

  const [displayName, setDisplayName] = useState('')
  const [email, setEmail] = useState('')
  const [nativeLanguage, setNativeLanguage] = useState('es')
  const [uiLocale, setUiLocale] = useState(currentLocale)
  const [bio, setBio] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [message, setMessage] = useState<{
    type: 'ok' | 'err'
    text: string
  } | null>(null)
  const [saving, setSaving] = useState(false)

  const fileInputRef = useRef<HTMLInputElement>(null)
  const [avatarUploading, setAvatarUploading] = useState(false)
  const [avatarError, setAvatarError] = useState<string | null>(null)

  useEffect(() => {
    if (user) {
      setDisplayName(user.displayName || '')
      setEmail(user.email || '')
      setNativeLanguage(user.native_language || 'es')
      setUiLocale(user.ui_locale || currentLocale)
      setBio(user.bio || '')
    }
  }, [user, currentLocale])

  async function handleAvatarUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    e.target.value = ''
    if (!file) return
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      setAvatarError(t('avatarTypeError'))
      return
    }
    setAvatarUploading(true)
    setAvatarError(null)
    try {
      const blob = await resizeImage(file, 1024)
      if (blob.size > 2 * 1024 * 1024) {
        setAvatarError(t('avatarSizeError'))
        return
      }
      const form = new FormData()
      form.append('file', blob, file.name)
      const res = await apiFetch('/api/auth/me/avatar', {
        method: 'POST',
        body: form,
      })
      if (!res.ok) throw new Error()
      const updated = await res.json()
      clearAvatarCache()
      setUser({ ...user!, avatar: updated.avatar })
    } catch {
      setAvatarError(t('avatarTypeError'))
    } finally {
      setAvatarUploading(false)
    }
  }

  async function handleAvatarRemove() {
    setAvatarUploading(true)
    setAvatarError(null)
    try {
      const res = await apiFetch('/api/auth/me/avatar', { method: 'DELETE' })
      if (!res.ok) throw new Error()
      clearAvatarCache()
      setUser({ ...user!, avatar: null })
    } catch {
      setAvatarError(t('avatarTypeError'))
    } finally {
      setAvatarUploading(false)
    }
  }

  async function handleSave() {
    setSaving(true)
    setMessage(null)
    if (password && password !== confirmPassword) {
      setMessage({ type: 'err', text: t('passwordMismatch') })
      setSaving(false)
      return
    }
    try {
      const res = await apiFetch('/api/auth/me', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          display_name: displayName,
          email: email || null,
          native_language: nativeLanguage,
          ui_locale: uiLocale,
          bio: bio || null,
          ...(password ? { password } : {}),
        }),
      })
      if (!res.ok) throw new Error(t('saveFailed'))
      const updated = await res.json()
      setUser(mapUser(updated, user))
      setMessage({ type: 'ok', text: t('saved') })
      setPassword('')
      setConfirmPassword('')

      if (uiLocale !== user?.ui_locale) {
        const opts = `path=/; max-age=${60 * 60 * 24 * 365}; SameSite=Lax${window.location.protocol === 'https:' ? '; Secure' : ''}`
        document.cookie = `NEXT_LOCALE=${uiLocale}; ${opts}`
        document.cookie = `LOCALE_DETECTED=1; ${opts}`
        window.location.reload()
      }
    } catch (err: unknown) {
      setMessage({
        type: 'err',
        text: err instanceof Error ? err.message : t('saveFailed'),
      })
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="border-fl-border bg-fl-surface space-y-5 border p-6">
      <div className="border-fl-border flex items-center gap-2 border-b pb-4">
        <span className="text-fl-label text-fl-muted-2">●</span>
        <span className="text-fl-label text-fl-muted-2 font-mono tracking-widest uppercase">
          {title ?? t('sectionProfile')}
        </span>
      </div>

      {/* Avatar */}
      <div className="flex items-center gap-4">
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={avatarUploading}
          className="border-fl-border hover:border-fl-border-2 relative h-16 w-16 flex-shrink-0 overflow-hidden rounded-full border transition-colors focus:outline-none disabled:opacity-60"
        >
          {user?.avatar ? (
            <AuthAvatarImage
              avatar={user.avatar}
              alt=""
              width={64}
              height={64}
              className="h-full w-full object-cover"
              fallback={
                <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
                  <span className="text-fl-muted-1 font-mono text-xl select-none">
                    {(user?.displayName ||
                      user?.username ||
                      '?')[0].toUpperCase()}
                  </span>
                </div>
              }
            />
          ) : (
            <div className="bg-fl-surface-2 flex h-full w-full items-center justify-center">
              <span className="text-fl-muted-1 font-mono text-xl select-none">
                {(user?.displayName || user?.username || '?')[0].toUpperCase()}
              </span>
            </div>
          )}
          {avatarUploading && (
            <div className="bg-fl-bg/70 absolute inset-0 flex items-center justify-center">
              <span className="text-fl-hint text-fl-muted-2 animate-pulse font-mono">
                ...
              </span>
            </div>
          )}
        </button>
        <div className="space-y-1">
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={avatarUploading}
            className="text-fl-muted-2 hover:text-fl-fg block font-mono text-xs tracking-widest uppercase transition-colors disabled:opacity-40"
          >
            {avatarUploading ? t('avatarUploading') : t('avatarChange')}
          </button>
          {user?.avatar && !avatarUploading && (
            <button
              type="button"
              onClick={handleAvatarRemove}
              className="text-fl-muted-4 hover:text-fl-error block font-mono text-xs tracking-widest uppercase transition-colors"
            >
              {t('avatarRemove')}
            </button>
          )}
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png"
          className="hidden"
          onChange={handleAvatarUpload}
        />
      </div>
      {avatarError && (
        <div className="border-fl-error/40 text-fl-error border px-4 py-3 font-mono text-xs">
          ✕ {avatarError}
        </div>
      )}

      {[
        {
          label: t('displayName'),
          value: displayName,
          onChange: setDisplayName,
          type: 'text',
        },
        { label: t('email'), value: email, onChange: setEmail, type: 'email' },
      ].map((field) => (
        <div key={field.label}>
          <label className="text-fl-muted-2 mb-2 block font-mono text-xs tracking-widest uppercase">
            {field.label}
          </label>
          <input
            type={field.type}
            value={field.value}
            onChange={(e) => field.onChange(e.target.value)}
            autoCorrect={field.type === 'email' ? 'off' : undefined}
            autoCapitalize={field.type === 'email' ? 'none' : undefined}
            spellCheck={field.type === 'email' ? false : undefined}
            className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-sm transition-colors focus:outline-none"
          />
        </div>
      ))}

      <div>
        <label className="text-fl-muted-2 mb-2 block font-mono text-xs tracking-widest uppercase">
          {t('bio')}
        </label>
        <textarea
          value={bio}
          onChange={(e) => setBio(e.target.value)}
          rows={3}
          maxLength={500}
          placeholder={t('bioPlaceholder')}
          className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 min-h-[74px] w-full resize-y border px-4 py-3 font-mono text-sm transition-colors focus:outline-none"
        />
        <p className="text-fl-hint text-fl-muted-4 mt-1 font-mono">
          {t('bioHint')}
        </p>
      </div>

      <div>
        <label className="text-fl-muted-2 mb-2 block font-mono text-xs tracking-widest uppercase">
          {t('nativeLanguage')}
        </label>
        <select
          value={nativeLanguage}
          onChange={(e) => setNativeLanguage(e.target.value)}
          className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full appearance-none border px-4 py-3 font-mono text-sm transition-colors focus:outline-none"
        >
          {[...LANGUAGES]
            .sort((a, b) => tLang(a).localeCompare(tLang(b)))
            .map((code) => (
              <option key={code} value={code}>
                {tLang(code)}
              </option>
            ))}
        </select>
      </div>

      <div>
        <label className="text-fl-muted-2 mb-2 block font-mono text-xs tracking-widest uppercase">
          {t('uiLocale')}
        </label>
        <select
          value={uiLocale}
          onChange={(e) => setUiLocale(e.target.value)}
          className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full appearance-none border px-4 py-3 font-mono text-sm transition-colors focus:outline-none"
        >
          {[...SUPPORTED_LOCALES]
            .sort((a, b) => tLang(a).localeCompare(tLang(b)))
            .map((code) => (
              <option key={code} value={code}>
                {tLang(code)}
              </option>
            ))}
        </select>
        <p className="text-fl-hint text-fl-muted-4 mt-1 font-mono">
          {t('uiLocaleHint')}
        </p>
      </div>

      <div>
        <label className="text-fl-muted-2 mb-2 block font-mono text-xs tracking-widest uppercase">
          {t('newPassword')}
        </label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder={t('newPasswordPlaceholder')}
          autoCorrect="off"
          autoCapitalize="none"
          spellCheck={false}
          className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-sm transition-colors focus:outline-none"
        />
      </div>

      <div>
        <label className="text-fl-muted-2 mb-2 block font-mono text-xs tracking-widest uppercase">
          {t('confirmPassword')}
        </label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder={t('confirmPasswordPlaceholder')}
          disabled={!password}
          autoCorrect="off"
          autoCapitalize="none"
          spellCheck={false}
          className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-sm transition-colors focus:outline-none disabled:opacity-30"
        />
      </div>

      {message && (
        <div
          className={`border px-4 py-3 font-mono text-xs ${message.type === 'ok' ? 'border-fl-border text-fl-muted-1' : 'border-fl-error/40 text-fl-error'}`}
        >
          {message.type === 'ok' ? '✓ ' : '✕ '}
          {message.text}
        </div>
      )}

      <button
        onClick={handleSave}
        disabled={saving}
        className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 w-full py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
      >
        {saving ? t('saving') : t('saveChanges')}
      </button>
    </div>
  )
}
