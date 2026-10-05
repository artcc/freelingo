import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useLanguageStore } from '@/store/language'
import { SUPPORTED_TARGET_LANGUAGES } from '@/lib/target-languages'

vi.mock('@/lib/api', () => ({
  apiFetch: vi.fn(),
}))

import { apiFetch } from '@/lib/api'

const mockApiFetch = vi.mocked(apiFetch)

function mockResponse(body: unknown, ok = true, status = 200): Response {
  return {
    ok,
    status,
    json: async () => body,
    headers: new Headers(),
  } as Response
}

describe('useLanguageStore — initial state', () => {
  beforeEach(() => {
    useLanguageStore.setState({
      activeLanguage: null,
      userLanguages: [],
      supportedLanguages: SUPPORTED_TARGET_LANGUAGES,
      availableLanguageCodes: [],
      isSwitching: false,
    })
    vi.clearAllMocks()
  })

  it('starts with null activeLanguage', () => {
    expect(useLanguageStore.getState().activeLanguage).toBeNull()
  })

  it('starts with empty userLanguages', () => {
    expect(useLanguageStore.getState().userLanguages).toEqual([])
  })

  it('starts with supportedLanguages preloaded', () => {
    expect(useLanguageStore.getState().supportedLanguages).toEqual(
      SUPPORTED_TARGET_LANGUAGES
    )
    expect(useLanguageStore.getState().supportedLanguages.length).toBe(10)
  })

  it('starts with empty availableLanguageCodes', () => {
    expect(useLanguageStore.getState().availableLanguageCodes).toEqual([])
  })

  it('starts with isSwitching false', () => {
    expect(useLanguageStore.getState().isSwitching).toBe(false)
  })
})

describe('useLanguageStore — fetchLanguages', () => {
  beforeEach(() => {
    useLanguageStore.setState({
      activeLanguage: null,
      userLanguages: [],
      supportedLanguages: SUPPORTED_TARGET_LANGUAGES,
      availableLanguageCodes: [],
      isSwitching: false,
      needsRefresh: false,
    })
    vi.clearAllMocks()
  })

  const fullResponse = {
    languages: [
      {
        target_language: 'en-GB',
        is_active: true,
        plan: {
          id: 1,
          cefr_level: 'B1',
          progress_day: 42,
          total_days: 48,
          completion_pct: 87.5,
        },
        progress: {
          total_xp: 12500,
          current_streak: 23,
          lessons_completed: 38,
        },
      },
      {
        target_language: 'it-IT',
        is_active: false,
        plan: null,
        progress: null,
      },
    ],
    all_supported_languages: ['en-US', 'en-GB', 'es-ES'],
  }

  it('populates userLanguages from API', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(fullResponse))

    await useLanguageStore.getState().fetchLanguages()

    const state = useLanguageStore.getState()
    expect(state.userLanguages).toHaveLength(2)
    expect(state.userLanguages[0].target_language).toBe('en-GB')
    expect(state.userLanguages[1].target_language).toBe('it-IT')
  })

  it('sets activeLanguage to the active language from API', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(fullResponse))

    await useLanguageStore.getState().fetchLanguages()

    const state = useLanguageStore.getState()
    expect(state.activeLanguage).not.toBeNull()
    expect(state.activeLanguage!.code).toBe('en-GB')
    expect(state.activeLanguage!.name).toBe('English (UK)')
  })

  it('sets availableLanguageCodes from API', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(fullResponse))

    await useLanguageStore.getState().fetchLanguages()

    expect(useLanguageStore.getState().availableLanguageCodes).toEqual([
      'en-US',
      'en-GB',
      'es-ES',
    ])
  })

  it('maps plan fields correctly including cefr_level', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(fullResponse))

    await useLanguageStore.getState().fetchLanguages()

    const plan = useLanguageStore.getState().userLanguages[0].plan
    expect(plan).not.toBeNull()
    expect(plan!.cefr_level).toBe('B1')
    expect(plan!.progress_day).toBe(42)
    expect(plan!.total_days).toBe(48)
    expect(plan!.completion_pct).toBe(87.5)
  })

  it('maps progress fields correctly', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(fullResponse))

    await useLanguageStore.getState().fetchLanguages()

    const progress = useLanguageStore.getState().userLanguages[0].progress
    expect(progress).not.toBeNull()
    expect(progress!.total_xp).toBe(12500)
    expect(progress!.current_streak).toBe(23)
    expect(progress!.lessons_completed).toBe(38)
  })

  it('handles null plan and progress for inactive language', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(fullResponse))

    await useLanguageStore.getState().fetchLanguages()

    const lang = useLanguageStore.getState().userLanguages[1]
    expect(lang.plan).toBeNull()
    expect(lang.progress).toBeNull()
  })

  it('keeps activeLanguage null when no language is active', async () => {
    const noActive = {
      languages: [
        {
          target_language: 'es-ES',
          is_active: false,
          plan: null,
          progress: null,
        },
      ],
      all_supported_languages: ['es-ES'],
    }
    mockApiFetch.mockResolvedValueOnce(mockResponse(noActive))

    await useLanguageStore.getState().fetchLanguages()

    expect(useLanguageStore.getState().activeLanguage).toBeNull()
  })

  it('handles empty languages array', async () => {
    const empty = { languages: [], all_supported_languages: ['en-US'] }
    mockApiFetch.mockResolvedValueOnce(mockResponse(empty))

    await useLanguageStore.getState().fetchLanguages()

    expect(useLanguageStore.getState().userLanguages).toEqual([])
    expect(useLanguageStore.getState().activeLanguage).toBeNull()
  })

  it('handles missing all_supported_languages gracefully', async () => {
    const noAllSupported = { languages: [] }
    mockApiFetch.mockResolvedValueOnce(mockResponse(noAllSupported))

    await useLanguageStore.getState().fetchLanguages()

    expect(useLanguageStore.getState().availableLanguageCodes).toEqual([])
  })

  it('keeps state unchanged on API error (non-ok response)', async () => {
    useLanguageStore.setState({
      userLanguages: [
        {
          target_language: 'en-GB',
          is_active: true,
          plan: null,
          progress: null,
        },
      ],
      availableLanguageCodes: ['en-GB'],
    })
    mockApiFetch.mockResolvedValueOnce(mockResponse(null, false, 500))

    await useLanguageStore.getState().fetchLanguages()

    const state = useLanguageStore.getState()
    expect(state.userLanguages).toHaveLength(1)
    expect(state.availableLanguageCodes).toEqual(['en-GB'])
  })

  it('keeps state unchanged on network error', async () => {
    useLanguageStore.setState({
      userLanguages: [
        {
          target_language: 'en-GB',
          is_active: true,
          plan: null,
          progress: null,
        },
      ],
      availableLanguageCodes: ['en-GB'],
    })
    mockApiFetch.mockRejectedValueOnce(new Error('network error'))

    await useLanguageStore.getState().fetchLanguages()

    const state = useLanguageStore.getState()
    expect(state.userLanguages).toHaveLength(1)
  })

  it('keeps an invalidated snapshot invalid until a successful refresh', async () => {
    useLanguageStore.setState({ needsRefresh: true })
    mockApiFetch.mockResolvedValueOnce(mockResponse({}, false, 502))
    expect(await useLanguageStore.getState().fetchLanguages()).toBe(false)
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
    mockApiFetch.mockResolvedValueOnce(mockResponse(fullResponse))
    expect(await useLanguageStore.getState().fetchLanguages()).toBe(true)
    expect(useLanguageStore.getState().needsRefresh).toBe(false)
  })

  it('discards a response started before invalidation even if the new refresh fails', async () => {
    let finishOld: (response: Response) => void = () => {}
    mockApiFetch.mockImplementationOnce(
      () =>
        new Promise((resolve) => {
          finishOld = resolve
        })
    )
    const oldRequest = useLanguageStore.getState().fetchLanguages()
    useLanguageStore.getState().invalidateLanguages()
    mockApiFetch.mockResolvedValueOnce(mockResponse({}, false, 502))
    expect(await useLanguageStore.getState().fetchLanguages()).toBe(false)
    finishOld(mockResponse(fullResponse))
    expect(await oldRequest).toBe(false)
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
    expect(useLanguageStore.getState().activeLanguage).toBeNull()
  })

  it('does not overwrite a newer summary with an older response', async () => {
    let finishOld: (response: Response) => void = () => {}
    mockApiFetch.mockImplementationOnce(
      () =>
        new Promise((resolve) => {
          finishOld = resolve
        })
    )
    const oldRequest = useLanguageStore.getState().fetchLanguages()
    useLanguageStore.getState().invalidateLanguages()
    const updated = {
      ...fullResponse,
      languages: [
        {
          ...fullResponse.languages[0],
          plan: { ...fullResponse.languages[0].plan, id: 8 },
        },
      ],
    }
    mockApiFetch.mockResolvedValueOnce(mockResponse(updated))
    expect(await useLanguageStore.getState().fetchLanguages()).toBe(true)
    finishOld(mockResponse(fullResponse))
    expect(await oldRequest).toBe(false)
    expect(useLanguageStore.getState().userLanguages[0].plan?.id).toBe(8)
    expect(useLanguageStore.getState().needsRefresh).toBe(false)
  })

  it('does not publish a cancelled language response', async () => {
    const controller = new AbortController()
    useLanguageStore.setState({ needsRefresh: true })
    mockApiFetch.mockImplementationOnce(async () => {
      controller.abort()
      return mockResponse(fullResponse)
    })
    expect(
      await useLanguageStore.getState().fetchLanguages(controller.signal)
    ).toBe(false)
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
    expect(useLanguageStore.getState().activeLanguage).toBeNull()
  })
})

describe('useLanguageStore — switchLanguage', () => {
  beforeEach(() => {
    useLanguageStore.setState({
      activeLanguage: null,
      userLanguages: [],
      supportedLanguages: SUPPORTED_TARGET_LANGUAGES,
      availableLanguageCodes: ['en-US', 'en-GB', 'es-ES'],
      isSwitching: false,
      needsRefresh: false,
    })
    vi.clearAllMocks()
  })

  it('sets isSwitching to true while switching and resets on success', async () => {
    mockApiFetch.mockResolvedValueOnce(
      mockResponse({ target_language: 'es-ES', is_active: true })
    )
    mockApiFetch.mockResolvedValueOnce(
      mockResponse({
        languages: [
          {
            target_language: 'es-ES',
            is_active: true,
            plan: null,
            progress: null,
          },
        ],
        all_supported_languages: ['es-ES'],
      })
    )

    const promise = useLanguageStore.getState().switchLanguage('es-ES')

    expect(useLanguageStore.getState().isSwitching).toBe(true)

    const result = await promise

    expect(result).toBe(true)
    expect(useLanguageStore.getState().isSwitching).toBe(false)
  })

  it('resets isSwitching even on API failure', async () => {
    mockApiFetch.mockRejectedValueOnce(new Error('network error'))

    const result = await useLanguageStore.getState().switchLanguage('es-ES')

    expect(result).toBe(false)
    expect(useLanguageStore.getState().isSwitching).toBe(false)
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
  })

  it('resets isSwitching on non-ok response', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(null, false, 400))

    const result = await useLanguageStore.getState().switchLanguage('es-ES')

    expect(result).toBe(false)
    expect(useLanguageStore.getState().isSwitching).toBe(false)
  })

  it('calls PUT with correct body', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse({}))
    mockApiFetch.mockResolvedValueOnce(
      mockResponse({ languages: [], all_supported_languages: [] })
    )

    await useLanguageStore.getState().switchLanguage('it-IT')

    expect(mockApiFetch).toHaveBeenCalledWith('/api/languages/active', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_language: 'it-IT' }),
      signal: expect.any(AbortSignal),
    })
  })

  it('calls fetchLanguages after successful switch', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse({}))
    mockApiFetch.mockResolvedValueOnce(
      mockResponse({ languages: [], all_supported_languages: [] })
    )

    await useLanguageStore.getState().switchLanguage('en-US')

    expect(mockApiFetch).toHaveBeenCalledTimes(2)
    expect(mockApiFetch).toHaveBeenNthCalledWith(2, '/api/languages', {
      signal: expect.any(AbortSignal),
    })
  })

  it('does not call fetchLanguages when PUT fails', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(null, false, 400))

    await useLanguageStore.getState().switchLanguage('en-US')

    expect(mockApiFetch).toHaveBeenCalledTimes(1)
    expect(useLanguageStore.getState().needsRefresh).toBe(false)
  })

  it.each([408, 500, 502])(
    'invalidates an uncertain HTTP %s switch result without repeating PUT',
    async (status) => {
      mockApiFetch.mockResolvedValueOnce(mockResponse(null, false, status))
      expect(await useLanguageStore.getState().switchLanguage('es-ES')).toBe(
        false
      )
      expect(useLanguageStore.getState().needsRefresh).toBe(true)
      expect(useLanguageStore.getState().isSwitching).toBe(false)
      expect(mockApiFetch).toHaveBeenCalledTimes(1)
    }
  )

  it('reports a failed refresh after a persisted switch and recovers without another PUT', async () => {
    mockApiFetch
      .mockResolvedValueOnce(mockResponse({}))
      .mockResolvedValueOnce(mockResponse({}, false, 502))
    expect(await useLanguageStore.getState().switchLanguage('es-ES')).toBe(
      false
    )
    expect(useLanguageStore.getState().needsRefresh).toBe(true)
    expect(useLanguageStore.getState().isSwitching).toBe(false)
    mockApiFetch.mockResolvedValueOnce(
      mockResponse({
        languages: [
          {
            target_language: 'es-ES',
            is_active: true,
            plan: null,
            progress: null,
          },
        ],
      })
    )
    expect(await useLanguageStore.getState().fetchLanguages()).toBe(true)
    expect(useLanguageStore.getState().activeLanguage?.code).toBe('es-ES')
    expect(useLanguageStore.getState().needsRefresh).toBe(false)
    expect(
      mockApiFetch.mock.calls.filter(([, options]) => options?.method === 'PUT')
    ).toHaveLength(1)
  })
})

describe('useLanguageStore — addLanguage', () => {
  beforeEach(() => {
    useLanguageStore.setState({
      activeLanguage: null,
      userLanguages: [],
      supportedLanguages: SUPPORTED_TARGET_LANGUAGES,
      availableLanguageCodes: [],
      isSwitching: false,
    })
    vi.clearAllMocks()
  })

  it('calls POST with correct body and then fetchLanguages', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse({}))
    mockApiFetch.mockResolvedValueOnce(
      mockResponse({ languages: [], all_supported_languages: [] })
    )

    await useLanguageStore.getState().addLanguage('es-ES')

    expect(mockApiFetch).toHaveBeenCalledWith('/api/languages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_language: 'es-ES' }),
    })
    expect(mockApiFetch).toHaveBeenCalledTimes(2)
  })

  it('does not call fetchLanguages when POST fails', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(null, false, 409))

    await useLanguageStore.getState().addLanguage('es-ES')

    expect(mockApiFetch).toHaveBeenCalledTimes(1)
  })

  it('handles network error silently', async () => {
    mockApiFetch.mockRejectedValueOnce(new Error('network error'))

    const result = await useLanguageStore.getState().addLanguage('pt-PT')

    expect(result).toBe(false)
  })
})

describe('useLanguageStore — removeLanguage', () => {
  beforeEach(() => {
    useLanguageStore.setState({
      activeLanguage: null,
      userLanguages: [
        {
          target_language: 'es-ES',
          is_active: true,
          plan: null,
          progress: null,
        },
        {
          target_language: 'it-IT',
          is_active: false,
          plan: null,
          progress: null,
        },
      ],
      supportedLanguages: SUPPORTED_TARGET_LANGUAGES,
      availableLanguageCodes: ['es-ES', 'it-IT'],
      isSwitching: false,
    })
    vi.clearAllMocks()
  })

  it('calls DELETE with URL-encoded code and then fetchLanguages', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(null, true, 204))
    mockApiFetch.mockResolvedValueOnce(
      mockResponse({ languages: [], all_supported_languages: [] })
    )

    await useLanguageStore.getState().removeLanguage('it-IT')

    expect(mockApiFetch).toHaveBeenCalledWith('/api/languages/it-IT', {
      method: 'DELETE',
    })
    expect(mockApiFetch).toHaveBeenCalledTimes(2)
  })

  it('encodes codes with special chars', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(null, true, 204))
    mockApiFetch.mockResolvedValueOnce(
      mockResponse({ languages: [], all_supported_languages: [] })
    )

    await useLanguageStore.getState().removeLanguage('pt-PT')

    expect(mockApiFetch).toHaveBeenCalledWith('/api/languages/pt-PT', {
      method: 'DELETE',
    })
  })

  it('does not call fetchLanguages when DELETE fails', async () => {
    mockApiFetch.mockResolvedValueOnce(mockResponse(null, false, 400))

    await useLanguageStore.getState().removeLanguage('es-ES')

    expect(mockApiFetch).toHaveBeenCalledTimes(1)
  })

  it('handles network error silently', async () => {
    mockApiFetch.mockRejectedValueOnce(new Error('network error'))

    const result = await useLanguageStore.getState().removeLanguage('es-ES')

    expect(result).toBe(false)
  })
})
