import { describe, expect, it } from 'vitest'
import de from '../../../messages/de.json'
import da from '../../../messages/da.json'
import fi from '../../../messages/fi.json'
import hr from '../../../messages/hr.json'
import en from '../../../messages/en.json'
import es from '../../../messages/es.json'
import fr from '../../../messages/fr.json'
import itMessages from '../../../messages/it.json'
import nl from '../../../messages/nl.json'
import pl from '../../../messages/pl.json'
import pt from '../../../messages/pt.json'
import ro from '../../../messages/ro.json'
import ru from '../../../messages/ru.json'
import sv from '../../../messages/sv.json'
import tr from '../../../messages/tr.json'

const locales = { da, de, es, fi, fr, hr, it: itMessages, nl, pl, pt, ro, ru, sv, tr }

describe('admin i18n messages', () => {
  it('keeps admin namespace keys in sync across locales', () => {
    const expectedKeys = Object.keys(en.admin).sort()

    for (const [locale, messages] of Object.entries(locales)) {
      expect(Object.keys(messages.admin).sort(), locale).toEqual(expectedKeys)
    }
  })
})
