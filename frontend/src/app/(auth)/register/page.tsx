'use client'

import { Suspense, useCallback, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
import { apiFetch } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

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

type SelectedPlan = 'monthly' | 'yearly'

function getSelectedPlan(plan: string | null): SelectedPlan | null {
  return plan === 'monthly' || plan === 'yearly' ? plan : null
}

function RegisterForm() {
  const t = useTranslations('auth.register')
  const tLang = useTranslations('languages')
  const tCommon = useTranslations('common')
  const router = useRouter()
  const searchParams = useSearchParams()
  const invite = searchParams.get('invite')
  const selectedPlan = getSelectedPlan(searchParams.get('plan'))
  const setTokens = useAuthStore((s) => s.setTokens)

  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [displayName, setDisplayName] = useState('')
  const [nativeLanguage, setNativeLanguage] = useState('es')
  const [termsAccepted, setTermsAccepted] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault()
      setError('')
      if (password !== confirmPassword) {
        setError(t('passwordMismatch'))
        return
      }
      if (!/^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{10,25}$/.test(password)) {
        setError(t('invalidPassword'))
        return
      }
      if (!termsAccepted) {
        setError(t('termsRequired'))
        return
      }
      if (!/^[a-zA-Z0-9._\s-]+$/.test(username)) {
        setError(t('invalidUsernameChars'))
        return
      }
      setLoading(true)
      try {
        const sanitizedUsername = username.replace(/\s+/g, '_').toLowerCase()
        const body: Record<string, string | null> = {
          username: sanitizedUsername,
          email,
          password,
          display_name: displayName || username,
          native_language: nativeLanguage,
        }
        if (invite) body.invite_token = invite

        const res = await apiFetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        })
        if (!res.ok) {
          const data = await res.json().catch(() => ({}))
          let msg = t('error')
          if (typeof data.detail === 'string') {
            if (data.detail === 'Username already taken')
              msg = t('usernameTaken')
            else if (data.detail === 'Email already taken')
              msg = t('emailTaken')
            else if (data.detail === 'Registration is closed')
              msg = t('registrationClosed')
            else if (data.detail === 'Invalid or expired invite')
              msg = t('invalidInvite')
            else if (data.detail === 'Email domain not allowed')
              msg = t('invalidEmail')
          } else if (Array.isArray(data.detail) && data.detail.length > 0) {
            const first = data.detail[0] as { loc?: string[]; msg?: string }
            const loc = (first.loc ?? []).join('.')
            if (
              loc.includes('email') ||
              first.msg?.toLowerCase().includes('email')
            ) {
              msg = t('invalidEmail')
            } else if (loc.includes('password')) {
              msg = t('invalidPassword')
            }
          }
          throw new Error(msg)
        }
        const data = await res.json()
        setTokens(data.access_token)
        router.push(
          selectedPlan ? `/onboarding?plan=${selectedPlan}` : '/onboarding'
        )
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : t('error'))
      } finally {
        setLoading(false)
      }
    },
    [
      username,
      email,
      password,
      confirmPassword,
      displayName,
      nativeLanguage,
      termsAccepted,
      invite,
      selectedPlan,
      router,
      t,
      setTokens,
    ]
  )

  return (
    <div className="bg-fl-bg flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="mb-10 flex flex-col items-center">
          <Image
            src="/logo.png"
            alt="FreeLingo"
            width={100}
            height={100}
            className="mb-4"
          />
          <h1 className="text-fl-fg font-code text-xl font-bold tracking-widest uppercase">
            FreeLingo
          </h1>
          <p className="text-fl-caption text-fl-muted-2 mt-1 font-mono tracking-widest uppercase">
            {tCommon('tagline')}
          </p>
        </div>

        <div className="border-fl-border bg-fl-surface border p-8">
          <div className="border-fl-border mb-6 flex items-center gap-2 border-b pb-4">
            <span className="text-fl-label text-fl-muted-2">●</span>
            <span className="text-fl-muted-2 font-mono text-xs tracking-widest uppercase">
              {t('title')}
            </span>
            {invite && (
              <span className="text-fl-hint text-fl-muted-1 ml-auto font-mono tracking-widest uppercase">
                {t('inviteActive')}
              </span>
            )}
          </div>

          {error && (
            <div className="border-fl-error/40 text-fl-error mb-5 border px-4 py-3 font-mono text-xs tracking-wide">
              ✕ {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {[
              {
                label: t('username'),
                value: username,
                onChange: setUsername,
                type: 'text',
                required: true,
              },
              {
                label: t('displayName'),
                value: displayName,
                onChange: setDisplayName,
                type: 'text',
                required: false,
                placeholder: t('displayNamePlaceholder'),
              },
              {
                label: t('email'),
                value: email,
                onChange: setEmail,
                type: 'email',
                required: true,
              },
            ].map((field) => (
              <div key={field.label}>
                <label className="text-fl-label text-fl-muted-2 mb-2 block font-mono tracking-widest uppercase">
                  {field.label}
                </label>
                <input
                  type={field.type}
                  value={field.value}
                  onChange={(e) => field.onChange(e.target.value)}
                  required={field.required}
                  placeholder={
                    'placeholder' in field ? field.placeholder : undefined
                  }
                  autoCorrect={field.type === 'email' ? 'off' : undefined}
                  autoCapitalize={field.type === 'email' ? 'none' : undefined}
                  spellCheck={field.type === 'email' ? false : undefined}
                  className="bg-fl-bg border-fl-border text-fl-fg placeholder:text-fl-muted-4 focus:border-fl-border-2 w-full border px-4 py-3 font-mono text-sm transition-colors focus:outline-none"
                />
              </div>
            ))}

            <div>
              <label className="text-fl-label text-fl-muted-2 mb-2 block font-mono tracking-widest uppercase">
                {t('password')}
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  autoCorrect="off"
                  autoCapitalize="none"
                  spellCheck={false}
                  className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full border px-4 py-3 pr-11 font-mono text-sm transition-colors focus:outline-none"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((v) => !v)}
                  className="text-fl-muted-4 hover:text-fl-muted-0 absolute inset-y-0 right-0 flex items-center px-3 transition-colors"
                  aria-label={
                    showPassword ? t('hidePassword') : t('showPassword')
                  }
                >
                  {showPassword ? (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
                      <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </svg>
                  ) : (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            <div>
              <label className="text-fl-label text-fl-muted-2 mb-2 block font-mono tracking-widest uppercase">
                {t('confirmPassword')}
              </label>
              <div className="relative">
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  autoCorrect="off"
                  autoCapitalize="none"
                  spellCheck={false}
                  className="bg-fl-bg border-fl-border text-fl-fg focus:border-fl-border-2 w-full border px-4 py-3 pr-11 font-mono text-sm transition-colors focus:outline-none"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword((v) => !v)}
                  className="text-fl-muted-4 hover:text-fl-muted-0 absolute inset-y-0 right-0 flex items-center px-3 transition-colors"
                  aria-label={
                    showConfirmPassword ? t('hidePassword') : t('showPassword')
                  }
                >
                  {showConfirmPassword ? (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
                      <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </svg>
                  ) : (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Legal acceptance */}
            <div className="flex items-start gap-3 py-1">
              <input
                id="terms-accept"
                type="checkbox"
                checked={termsAccepted}
                onChange={(e) => setTermsAccepted(e.target.checked)}
                className="accent-fl-accent mt-0.5 h-4 w-4 flex-shrink-0 cursor-pointer"
              />
              <label
                htmlFor="terms-accept"
                className="text-fl-muted-2 cursor-pointer font-mono text-xs leading-relaxed select-none"
              >
                {t('termsAccept')}{' '}
                <a
                  href="/terms?from=register"
                  className="text-fl-muted-1 hover:text-fl-fg underline underline-offset-2 transition-colors"
                >
                  {t('termsLink')}
                </a>{' '}
                {t('andWord')}{' '}
                <a
                  href="/privacy?from=register"
                  className="text-fl-muted-1 hover:text-fl-fg underline underline-offset-2 transition-colors"
                >
                  {t('privacyLink')}
                </a>
              </label>
            </div>

            <div>
              <label className="text-fl-label text-fl-muted-2 mb-2 block font-mono tracking-widest uppercase">
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

            <button
              type="submit"
              disabled={loading}
              className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 mt-2 w-full py-3 font-mono text-xs font-bold tracking-widest uppercase transition-colors disabled:opacity-40"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 inline h-4 w-4 animate-spin" />
                  {t('creatingAccount')}
                </>
              ) : (
                t('submit')
              )}
            </button>
          </form>

          <p className="text-fl-label text-fl-muted-2 mt-6 text-center font-mono tracking-wide">
            {t('hasAccount')}{' '}
            <Link
              href="/login"
              className="text-fl-muted-1 hover:text-fl-fg transition-colors"
            >
              {t('login')}
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default function RegisterPage() {
  return (
    <Suspense>
      <RegisterForm />
    </Suspense>
  )
}
