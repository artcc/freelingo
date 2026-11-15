import { createTranslator } from 'next-intl'
import { describe, expect, it } from 'vitest'

import { SUPPORTED_LOCALES } from '@/lib/locales'
import en from '../../../messages/en.json'

const errorKeys = [
  'accountDeletion.cancellationRequired',
  'accountDeletion.checkoutPending',
  'accountDeletion.verificationUnavailable',
  'accountDeletion.failed',
  'accountDeletion.manageSubscription',
  'common.errorMessage',
  'auth.login.error',
  'auth.login.loginFailed',
  'auth.register.error',
  'auth.register.invalidInvite',
  'auth.verifyEmail.error',
  'auth.forgotPassword.error',
  'auth.resetPassword.missingToken',
  'auth.resetPassword.error',
  'onboarding.saveFailed',
  'onboarding.trialError',
  'billing.checkoutError',
  'billing.portalError',
  'billing.successPendingDesc',
  'billing.successErrorDesc',
  'chat.errorMessage',
  'lesson.regenerateError',
  'lesson.questionTranslationError',
  'lessonPractice.unavailable',
  'listening.audioError',
  'listening.errorLoading',
  'listening.errorSubmit',
  'reading.errorLoading',
  'reading.errorSubmit',
  'exerciseGeneration.contextChanged',
  'exerciseGeneration.failed',
  'exerciseGeneration.timeout',
  'exerciseGeneration.unavailable',
  'detective.failedDescription',
  'detective.contextChanged',
  'conversation.errorServicesDisabled',
  'conversation.errorConnection',
  'conversation.errorTranscription',
  'conversation.errorResponse',
  'conversation.errorSpeech',
  'conversation.errorUnauthorized',
  'conversation.errorMic',
  'conversation.errorVadInit',
  'conversation.quotaExceededTokens',
  'contact.errorGeneric',
  'error.body',
  'error.digest',
] as const

const billingKeys = [
  'legal.terms.s5Body',
  'legal.terms.s6Body',
  'dashboard.premiumBannerTitle',
  'dashboard.premiumBannerDescTrialUsed',
  'dashboard.freemiumTrialDesc',
  'conversation.trialCtaDesc',
  'onboarding.trialDesc',
  'onboarding.trialDescTrialUsed',
  'onboarding.trialNoCharge',
  'onboarding.trialNoChargeTrialUsed',
  'onboarding.freemiumTrialDesc',
  'billing.paywallDesc',
  'billing.paywallDescTrialUsed',
  'billing.paywallChatTitle',
  'billing.planFeature.feature1',
  'billing.successLabel',
  'billing.successDesc',
  'billing.canceledLabel',
  'billing.canceledTitle',
  'billing.canceledDesc',
  'billing.canceledNoCharge',
  'freemium.trialUnlimited',
] as const

const durationKeys = [
  'onboarding.trialNoCharge',
  'billing.paywallDesc',
  'billing.trialDays',
  'freemium.trialDaysLeft',
] as const

const english = createTranslator({ locale: 'en', messages: en })

function messageKeys(value: Record<string, unknown>, prefix = ''): string[] {
  return Object.entries(value).flatMap(([key, child]) => {
    const path = prefix ? `${prefix}.${key}` : key
    return typeof child === 'string'
      ? [path]
      : messageKeys(child as Record<string, unknown>, path)
  })
}

function placeholders(message: string) {
  const names = [...message.matchAll(/\{(\w+)(?:,|\})/g)].map(
    (match) => match[1]
  )
  return [...new Set(names)].sort()
}

describe.each(SUPPORTED_LOCALES)(
  'billing and access messages in %s',
  (locale) => {
    it('localizes every Premium invitation and keeps its billing placeholders', async () => {
      const messages = (await import(`../../../messages/${locale}.json`))
        .default
      expect(messageKeys(messages.premiumOffer).sort()).toEqual(
        messageKeys(en.premiumOffer).sort()
      )
      const t = createTranslator({
        locale,
        messages,
        onError: (error) => {
          throw error
        },
      })
      const keys = messageKeys(en.premiumOffer, 'premiumOffer') as Array<
        Extract<Parameters<typeof english>[0], `premiumOffer.${string}`>
      >
      for (const key of keys) {
        expect(placeholders(t.raw(key)), key).toEqual(
          placeholders(english.raw(key))
        )
        const text = t(key, { days: 7, date: '15/11/2026' })
        expect(text.trim(), key).not.toBe('')
        expect(text, key).not.toMatch(/[{}]/)
        if (locale !== 'en' && english.raw(key).split(/\s+/).length >= 4) {
          expect(text, key).not.toBe(
            english(key, { days: 7, date: '15/11/2026' })
          )
        }
      }
    })

    it('has localized messages with matching placeholders and valid ICU', async () => {
      const messages = (await import(`../../../messages/${locale}.json`))
        .default
      const t = createTranslator({
        locale,
        messages,
        onError: (error) => {
          throw error
        },
      })

      for (const key of [...errorKeys, ...billingKeys, ...durationKeys]) {
        expect(t.has(key), key).toBe(true)
        expect(typeof t.raw(key), key).toBe('string')
        expect(placeholders(t.raw(key)), key).toEqual(
          placeholders(english.raw(key))
        )

        const values = { days: 5 }
        const text = t(key, values)
        const source = english(key, values)
        expect(text.trim(), key).not.toBe('')
        expect(text, key).not.toBe(key)
        expect(text, key).not.toMatch(/[{}]/)

        // Short labels may legitimately match English; full sentences should not.
        if (locale !== 'en' && source.trim().split(/\s+/).length >= 4) {
          expect(text, key).not.toBe(source)
        }
      }

      for (const key of errorKeys) {
        expect(t(key), key).not.toMatch(
          /\b(?:WebAssembly|WebSocket|Traceback|HTTP|API|backend|tokens?)\b|(?:stt|tts|llm)_failed|quota_exceeded_[a-z_]+/i
        )
      }
    })

    it('renders configured trial lengths and plural branches', async () => {
      const messages = (await import(`../../../messages/${locale}.json`))
        .default
      const t = createTranslator({
        locale,
        messages,
        onError: (error) => {
          throw error
        },
      })

      for (const days of [0, 1, 2, 5, 11, 21, 22, 25]) {
        for (const key of durationKeys) {
          const text = t(key, { days })
          expect(text, key).toContain(String(days))
          expect(text, key).not.toMatch(/[{}]/)
        }
      }
    })
  }
)
