import React from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import { NextIntlClientProvider } from 'next-intl'
import { TARGET_LANGUAGE_CATALOG } from '@/lib/target-languages'
import { useAuthStore } from '@/store/auth'
import { useConfigStore } from '@/store/config'
import { useLanguageStore } from '@/store/language'
import de from '../../../messages/de.json'
import en from '../../../messages/en.json'
import es from '../../../messages/es.json'
import fr from '../../../messages/fr.json'
import itMessages from '../../../messages/it.json'
import nl from '../../../messages/nl.json'
import pl from '../../../messages/pl.json'
import pt from '../../../messages/pt.json'
import ro from '../../../messages/ro.json'
import ru from '../../../messages/ru.json'
import tr from '../../../messages/tr.json'

const { searchParams, apiFetch } = vi.hoisted(() => ({
  searchParams: new URLSearchParams(),
  apiFetch: vi.fn(),
}))

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn() }),
  useSearchParams: () => searchParams,
}))

vi.mock('@/lib/api', () => ({ apiFetch }))

import OnboardingPage from '@/app/(auth)/onboarding/page'

const catalogs = { de, en, es, fr, it: itMessages, nl, pl, pt, ro, ru, tr }
type Locale = keyof typeof catalogs

const spanishSubtitles: Record<Locale, string> = {
  de: 'Sprache: Spanisch. Wofür möchtest du sie nutzen? Wähle alle zutreffenden Ziele aus.',
  en: 'Language: Spanish. What do you want to use it for? Select all that apply.',
  es: 'Idioma: español. ¿Para qué quieres utilizarlo? Selecciona todos los objetivos que correspondan.',
  fr: "Langue : espagnol. Dans quel but souhaitez-vous l'utiliser ? Sélectionnez tous les objectifs qui vous correspondent.",
  it: 'Lingua: spagnolo. Per cosa vuoi usarla? Seleziona tutti gli obiettivi che fanno al caso tuo.',
  nl: 'Taal: Spaans. Waarvoor wil je deze taal gebruiken? Selecteer alle doelen die van toepassing zijn.',
  pl: 'Język: hiszpański. Do czego chcesz go używać? Zaznacz wszystkie cele, które Ci odpowiadają.',
  pt: 'Idioma: espanhol. Para que você quer usá-lo? Selecione todos os objetivos que se aplicam.',
  ro: 'Limbă: spaniolă. Pentru ce vrei să o folosești? Selectează toate obiectivele care ți se potrivesc.',
  ru: 'Язык: испанский. Для чего ты хочешь его использовать? Выбери все подходящие цели.',
  tr: 'Dil: İspanyolca. Bu dili ne için kullanmak istiyorsunuz? Uygun olanların hepsini seçin.',
}

const onIntlError = vi.fn()
const englishSubtitle =
  'Language: English. What do you want to use it for? Select all that apply.'

function languageResponse(
  codes = TARGET_LANGUAGE_CATALOG.map((language) => language.code)
) {
  return new Response(
    JSON.stringify({ languages: [], all_supported_languages: codes })
  )
}

function renderOnboarding(locale: Locale = 'en') {
  return render(
    <NextIntlClientProvider
      locale={locale}
      messages={catalogs[locale]}
      timeZone="UTC"
      onError={onIntlError}
    >
      <OnboardingPage />
    </NextIntlClientProvider>
  )
}

beforeEach(() => {
  for (const key of Array.from(searchParams.keys())) searchParams.delete(key)
  onIntlError.mockReset()
  apiFetch.mockReset()
  apiFetch.mockImplementation(async () => languageResponse())
  useAuthStore.setState({ ...useAuthStore.getInitialState() }, true)
  useConfigStore.setState(
    { ...useConfigStore.getInitialState(), loaded: true },
    true
  )
  useLanguageStore.setState({ ...useLanguageStore.getInitialState() }, true)
})

afterEach(() => {
  cleanup()
  expect(onIntlError).not.toHaveBeenCalled()
})

describe('onboarding goals subtitle', () => {
  it.each(Object.keys(catalogs) as Locale[])(
    'names the selected language with natural wording in the %s UI',
    async (locale) => {
      const messages = catalogs[locale]
      renderOnboarding(locale)

      fireEvent.click(
        await screen.findByRole('button', {
          name: new RegExp(messages.targetLanguages['es-ES']),
        })
      )
      fireEvent.click(
        screen.getByRole('button', { name: messages.common.next })
      )

      expect(screen.getByText(spanishSubtitles[locale])).toBeInTheDocument()
    }
  )

  it.each([
    [null, 'English'],
    ['en-GB', 'English'],
    ['en-US', 'English'],
    ['de-DE', 'German'],
    ['fr-FR', 'French'],
    ['it-IT', 'Italian'],
    ['pt-PT', 'Portuguese'],
    ['ja-JP', 'Japanese'],
    ['ko-KR', 'Korean'],
    ['zh-CN', 'Chinese'],
  ])(
    'uses the language-level name for query language=%s',
    async (code, name) => {
      if (code) searchParams.set('language', code)
      renderOnboarding()
      await screen.findByRole('button', { name: /Spanish/ })
      fireEvent.click(screen.getByRole('button', { name: 'Next' }))

      expect(
        screen.getByText(
          `Language: ${name}. What do you want to use it for? Select all that apply.`
        )
      ).toBeInTheDocument()
    }
  )

  it.each(['', 'unknown-language'])(
    'safely displays the default for language=%s while languages load',
    async (code) => {
      searchParams.set('language', code)
      let resolveLanguages!: (response: Response) => void
      apiFetch.mockReturnValueOnce(
        new Promise<Response>((resolve) => {
          resolveLanguages = resolve
        })
      )
      renderOnboarding()
      fireEvent.click(screen.getByRole('button', { name: 'Next' }))

      expect(screen.getByText(englishSubtitle)).toBeInTheDocument()

      await act(async () => resolveLanguages(languageResponse(['fr-FR'])))

      expect(
        screen.getByText(
          'Language: French. What do you want to use it for? Select all that apply.'
        )
      ).toBeInTheDocument()
    }
  )

  it.each(['HTTP', 'network'])(
    'safely displays the default for an invalid query after a %s failure',
    async (failure) => {
      searchParams.set('language', 'unknown-language')
      if (failure === 'HTTP') {
        apiFetch.mockResolvedValueOnce(new Response('', { status: 503 }))
      } else {
        apiFetch.mockRejectedValueOnce(new Error('offline'))
      }
      renderOnboarding()
      await screen.findByText(en.onboarding.saveFailed)
      fireEvent.click(screen.getByRole('button', { name: 'Next' }))

      expect(screen.getByText(englishSubtitle)).toBeInTheDocument()
    }
  )
})
