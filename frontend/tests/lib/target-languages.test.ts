import { describe, it, expect } from 'vitest'
import {
  SUPPORTED_TARGET_LANGUAGES,
  TARGET_LANGUAGE_CATALOG,
  getLanguageByCode,
  DEFAULT_TARGET_LANGUAGE,
  TARGET_LANGUAGE_CAPABILITIES,
  getTargetLanguageCapability,
  getTargetLanguageTextClass,
} from '@/lib/target-languages'

describe('SUPPORTED_TARGET_LANGUAGES', () => {
  it('contains exactly 16 languages', () => {
    expect(SUPPORTED_TARGET_LANGUAGES).toHaveLength(16)
  })

  const expectedCodes = [
    'en-US',
    'en-GB',
    'es-ES',
    'it-IT',
    'pl-PL',
    'nl-NL',
    'ru-RU',
    'sv-SE',
    'da-DK',
    'pt-BR',
    'pt-PT',
    'fr-FR',
    'de-DE',
    'ja-JP',
    'ko-KR',
    'zh-CN',
  ]

  it.each(expectedCodes)('%s has all required fields', (code) => {
    const lang = SUPPORTED_TARGET_LANGUAGES.find((l) => l.code === code)
    const catalogLang = TARGET_LANGUAGE_CATALOG.find((l) => l.code === code)
    expect(lang).toBeDefined()
    expect(catalogLang).toBeDefined()
    expect(lang!.code).toBeTypeOf('string')
    expect(lang!.name).toBeTypeOf('string')
    expect(lang!.nameEn).toBeTypeOf('string')
    expect(lang!.flagPath).toMatch(/^\/flags\/[a-zA-Z_]+\./)
    expect(lang!.iso639).toMatch(/^[a-z]{2}$/)
    expect(lang!.script).toBe(catalogLang!.script)
    expect(lang!.fontClass).toBe(catalogLang!.fontClass)
    expect(lang!.usesWordSpacing).toBe(catalogLang!.usesWordSpacing)
  })

  it('every code is unique', () => {
    const codes = SUPPORTED_TARGET_LANGUAGES.map((l) => l.code)
    expect(new Set(codes).size).toBe(codes.length)
  })

  it('flag paths match expected values', () => {
    const paths = SUPPORTED_TARGET_LANGUAGES.map((l) => l.flagPath)
    expect(paths).toContain('/flags/usa.jpg')
    expect(paths).toContain('/flags/uk.jpg')
    expect(paths).toContain('/flags/spain.jpg')
    expect(paths).toContain('/flags/italy.jpg')
    expect(paths).toContain('/flags/poland.jpg')
    expect(paths).toContain('/flags/netherlands.jpg')
    expect(paths).toContain('/flags/russia.jpg')
    expect(paths).toContain('/flags/sweden.jpg')
    expect(paths).toContain('/flags/denmark.jpg')
    expect(paths).toContain('/flags/brazil.jpg')
    expect(paths).toContain('/flags/portugal.jpg')
    expect(paths).toContain('/flags/france.jpg')
    expect(paths).toContain('/flags/germany.jpg')
    expect(paths).toContain('/flags/japan.jpg')
    expect(paths).toContain('/flags/south_korea.jpg')
    expect(paths).toContain('/flags/china.jpg')
  })

  it('iso639 codes map to correct languages', () => {
    const enLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'en')
    const esLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'es')
    const itLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'it')
    const plLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'pl')
    const ptLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'pt')
    const frLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'fr')
    const deLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'de')
    const jaLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'ja')
    const koLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'ko')
    const zhLangs = SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'zh')
    expect(enLangs).toHaveLength(2)
    expect(esLangs).toHaveLength(1)
    expect(itLangs).toHaveLength(1)
    expect(plLangs).toHaveLength(1)
    expect(
      SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'da')
    ).toHaveLength(1)
    expect(SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'nl')).toHaveLength(1)
    expect(
      SUPPORTED_TARGET_LANGUAGES.filter((l) => l.iso639 === 'ru')
    ).toHaveLength(1)
    expect(ptLangs).toHaveLength(2)
    expect(frLangs).toHaveLength(1)
    expect(deLangs).toHaveLength(1)
    expect(jaLangs).toHaveLength(1)
    expect(koLangs).toHaveLength(1)
    expect(zhLangs).toHaveLength(1)
  })
})

describe('TARGET_LANGUAGE_CATALOG', () => {
  it('contains the current supported languages plus CJK catalog entries', () => {
    expect(TARGET_LANGUAGE_CATALOG).toHaveLength(16)
    expect(TARGET_LANGUAGE_CATALOG.map((l) => l.code)).toEqual([
      'en-US',
      'en-GB',
      'es-ES',
      'it-IT',
      'pt-BR',
      'pt-PT',
      'fr-FR',
      'de-DE',
      'pl-PL',
      'nl-NL',
      'ru-RU',
      'sv-SE',
      'da-DK',
      'ja-JP',
      'ko-KR',
      'zh-CN',
    ])
  })

  it('keeps canonical Brazilian metadata distinct from Portugal', () => {
    expect(getLanguageByCode('PT-br')).toMatchObject({
      code: 'pt-BR',
      name: 'Português (Brasil)',
      nameEn: 'Portuguese (Brazil)',
      flagPath: '/flags/brazil.jpg',
      iso639: 'pt',
      fontClass: 'font-target-latin',
      script: 'latin',
      usesWordSpacing: true,
    })
    expect(getTargetLanguageTextClass('pt-BR')).toBe(
      getTargetLanguageTextClass('pt-PT')
    )
  })

  it('resolves canonical Dutch metadata and Latin typography', () => {
    expect(getLanguageByCode('NL-nl')).toMatchObject({
      code: 'nl-NL',
      name: 'Nederlands',
      nameEn: 'Dutch (Netherlands)',
      flagPath: '/flags/netherlands.jpg',
      iso639: 'nl',
      fontClass: 'font-target-latin',
      script: 'latin',
      usesWordSpacing: true,
    })
    expect(getTargetLanguageTextClass('nl-NL')).toContain('font-target-latin')
    expect(getTargetLanguageTextClass('nl-NL')).toContain('leading-relaxed')
  })

  it('resolves canonical Russian metadata without mandatory romanization', () => {
    expect(getLanguageByCode('RU-ru')).toMatchObject({
      code: 'ru-RU',
      name: 'Русский',
      nameEn: 'Russian',
      flagPath: '/flags/russia.jpg',
      iso639: 'ru',
      fontClass: 'font-target-cyrillic',
      script: 'cyrillic',
      usesWordSpacing: true,
    })
    expect(getLanguageByCode('ru-RU')?.romanization).toBeUndefined()
  })

  it.each(['sv-SE', 'SV-se', 'sv-se'])('resolves Swedish metadata for %s', (code) => {
    expect(getLanguageByCode(code)).toEqual({
      code: 'sv-SE',
      name: 'Svenska',
      nameEn: 'Swedish',
      flagPath: '/flags/sweden.jpg',
      iso639: 'sv',
      script: 'latin',
      fontClass: 'font-target-latin',
      usesWordSpacing: true,
    })
    expect(getTargetLanguageTextClass(code)).toContain('font-target-latin')
    expect(getTargetLanguageTextClass(code)).toContain('leading-relaxed')
    expect(getLanguageByCode('sv')).toBeUndefined()
  })

  it.each(['da-DK', 'DA-dk', 'da-dk'])(
    'resolves Danish metadata and Latin typography for %s',
    (code) => {
      expect(getLanguageByCode(code)).toEqual({
        code: 'da-DK',
        name: 'Dansk',
        nameEn: 'Danish',
        flagPath: '/flags/denmark.jpg',
        iso639: 'da',
        script: 'latin',
        fontClass: 'font-target-latin',
        usesWordSpacing: true,
      })
      expect(TARGET_LANGUAGE_CAPABILITIES['da-DK']).toEqual({
        script: 'latin',
        fontClass: 'font-target-latin',
        usesWordSpacing: true,
      })
      expect(getTargetLanguageTextClass(code)).toContain('font-target-latin')
      expect(getTargetLanguageTextClass(code)).toContain('leading-relaxed')
      expect(getLanguageByCode('da')).toBeUndefined()
    }
  )

  it('contains complete Polish display metadata', () => {
    expect(getLanguageByCode('pl-PL')).toMatchObject({
      name: 'Polski',
      nameEn: 'Polish',
      flagPath: '/flags/poland.jpg',
      iso639: 'pl',
      fontClass: 'font-target-latin',
      script: 'latin',
      usesWordSpacing: true,
    })
  })

  it('contains complete CJK display metadata', () => {
    expect(getLanguageByCode('ja-JP')).toMatchObject({
      name: '日本語',
      nameEn: 'Japanese',
      flagPath: '/flags/japan.jpg',
      iso639: 'ja',
      fontClass: 'font-target-ja',
    })
    expect(getLanguageByCode('ko-KR')).toMatchObject({
      name: '한국어',
      nameEn: 'Korean',
      flagPath: '/flags/south_korea.jpg',
      iso639: 'ko',
      fontClass: 'font-target-ko',
    })
    expect(getLanguageByCode('zh-CN')).toMatchObject({
      name: '中文（中国）',
      nameEn: 'Chinese (Mainland China)',
      flagPath: '/flags/china.jpg',
      iso639: 'zh',
      fontClass: 'font-target-zh',
    })
  })
})

describe('getLanguageByCode', () => {
  it('returns the correct language for a valid code', () => {
    const lang = getLanguageByCode('es-ES')
    expect(lang).toBeDefined()
    expect(lang!.code).toBe('es-ES')
    expect(lang!.name).toBe('Español')
    expect(lang!.nameEn).toBe('Spanish')
    expect(lang!.iso639).toBe('es')
  })

  it('returns English (UK) for en-GB', () => {
    const lang = getLanguageByCode('en-GB')
    expect(lang).toBeDefined()
    expect(lang!.name).toBe('English (UK)')
  })

  it('returns English (US) for en-US', () => {
    const lang = getLanguageByCode('en-US')
    expect(lang).toBeDefined()
    expect(lang!.name).toBe('English (US)')
  })

  it('returns Italian for it-IT', () => {
    const lang = getLanguageByCode('it-IT')
    expect(lang).toBeDefined()
    expect(lang!.name).toBe('Italiano')
  })

  it('returns Polish for pl-PL', () => {
    const lang = getLanguageByCode('pl-PL')
    expect(lang).toBeDefined()
    expect(lang!.code).toBe('pl-PL')
    expect(lang!.name).toBe('Polski')
    expect(lang!.nameEn).toBe('Polish')
    expect(lang!.iso639).toBe('pl')
  })

  it('returns Portuguese for pt-PT', () => {
    const lang = getLanguageByCode('pt-PT')
    expect(lang).toBeDefined()
    expect(lang!.name).toBe('Português (Portugal)')
  })

  it('returns French for fr-FR', () => {
    const lang = getLanguageByCode('fr-FR')
    expect(lang).toBeDefined()
    expect(lang!.code).toBe('fr-FR')
    expect(lang!.name).toBe('Français')
    expect(lang!.nameEn).toBe('French')
    expect(lang!.iso639).toBe('fr')
  })

  it('returns German for de-DE', () => {
    const lang = getLanguageByCode('de-DE')
    expect(lang).toBeDefined()
    expect(lang!.code).toBe('de-DE')
    expect(lang!.name).toBe('Deutsch')
    expect(lang!.nameEn).toBe('German')
    expect(lang!.iso639).toBe('de')
  })

  it('returns undefined for an unknown code', () => {
    expect(getLanguageByCode('')).toBeUndefined()
  })

  it('matches codes case-insensitively', () => {
    expect(getLanguageByCode('ES-ES')?.code).toBe('es-ES')
    expect(getLanguageByCode('es-es')?.code).toBe('es-ES')
    expect(getLanguageByCode('EN-US')?.code).toBe('en-US')
  })
})

describe('DEFAULT_TARGET_LANGUAGE', () => {
  it('is en-GB', () => {
    expect(DEFAULT_TARGET_LANGUAGE).toBe('en-GB')
  })

  it('is present in SUPPORTED_TARGET_LANGUAGES', () => {
    const lang = getLanguageByCode(DEFAULT_TARGET_LANGUAGE)
    expect(lang).toBeDefined()
  })
})

describe('TargetLanguage interface compliance', () => {
  it('all languages have non-empty nameEn', () => {
    SUPPORTED_TARGET_LANGUAGES.forEach((lang) => {
      expect(lang.nameEn.length).toBeGreaterThan(0)
    })
  })

  it('all languages have non-empty name', () => {
    SUPPORTED_TARGET_LANGUAGES.forEach((lang) => {
      expect(lang.name.length).toBeGreaterThan(0)
    })
  })
})

describe('target language capabilities', () => {
  it.each(['ru-RU', 'RU-ru', 'ru-ru'])(
    'keeps Cyrillic typography and word spacing for %s',
    (code) => {
      expect(getTargetLanguageCapability(code)).toEqual({
        script: 'cyrillic',
        fontClass: 'font-target-cyrillic',
        usesWordSpacing: true,
      })
      expect(getTargetLanguageTextClass(code)).toContain('font-target-cyrillic')
      expect(getTargetLanguageTextClass(code)).toContain('text-base')
      expect(getTargetLanguageTextClass(code)).toContain('leading-relaxed')
      expect(getTargetLanguageTextClass(code)).toContain('tracking-normal')
    }
  )

  it('keeps CJK capabilities enabled in the supported catalog', () => {
    expect(TARGET_LANGUAGE_CAPABILITIES['ja-JP']).toMatchObject({
      script: 'hiragana-katakana-kanji',
      fontClass: 'font-target-ja',
      usesWordSpacing: false,
      romanization: 'romaji',
    })
    expect(TARGET_LANGUAGE_CAPABILITIES['ko-KR']).toMatchObject({
      script: 'hangul',
      fontClass: 'font-target-ko',
      usesWordSpacing: true,
      romanization: 'revised-romanization',
    })
    expect(TARGET_LANGUAGE_CAPABILITIES['zh-CN']).toMatchObject({
      script: 'simplified-hanzi',
      fontClass: 'font-target-zh',
      usesWordSpacing: false,
      romanization: 'pinyin',
    })
    expect(TARGET_LANGUAGE_CAPABILITIES['pl-PL']).toMatchObject({
      script: 'latin',
      fontClass: 'font-target-latin',
      usesWordSpacing: true,
    })
    expect(SUPPORTED_TARGET_LANGUAGES.map((l) => l.code)).toEqual(
      TARGET_LANGUAGE_CATALOG.map((l) => l.code)
    )
  })

  it('returns safe Latin defaults for unknown codes', () => {
    expect(getTargetLanguageCapability('xx-XX')).toMatchObject({
      script: 'latin',
      fontClass: 'font-target-latin',
      usesWordSpacing: true,
    })
  })

  it('uses CJK-friendly text classes for future CJK languages', () => {
    expect(getTargetLanguageTextClass('zh-CN')).toContain('font-target-zh')
    expect(getTargetLanguageTextClass('zh-CN')).toContain('leading-loose')
    expect(getTargetLanguageTextClass('zh-CN')).not.toContain('font-mono')
    expect(getTargetLanguageTextClass('en-GB')).toContain('font-target-latin')
    expect(getTargetLanguageTextClass('pl-PL')).toContain('font-target-latin')
    expect(getTargetLanguageTextClass('pl-PL')).toContain('leading-relaxed')
  })
})
