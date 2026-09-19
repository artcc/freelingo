import { describe, expect, it } from 'vitest'
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

const locales = {
  de,
  en,
  es,
  fr,
  it: itMessages,
  nl,
  pl,
  pt,
  ro,
  ru,
}

describe('onboarding goals subtitle', () => {
  it('templates the selected language instead of naming one in every locale', () => {
    for (const [locale, messages] of Object.entries(locales)) {
      const subtitle = messages.onboarding.goals.subtitle as string
      expect(subtitle, locale).toContain('{language}')
      expect(subtitle, locale).not.toMatch(
        /English|Englisch|inglés|anglais|inglese|Engels|angielskiego|inglês|engleza|английский/i
      )
    }
  })
})
