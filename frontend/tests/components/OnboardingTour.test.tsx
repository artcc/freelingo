import React from 'react'
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { NextIntlClientProvider } from 'next-intl'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import OnboardingTour from '@/components/tour/OnboardingTour'
import WhatsNew from '@/components/whats-new/WhatsNew'
import { useAuthStore } from '@/store/auth'
import es from '../../../messages/es.json'

const originalDialogMethods = Object.getOwnPropertyDescriptors(
  HTMLDialogElement.prototype
)

vi.mock('@/components/lingu/LinguAvatar', () => ({
  default: ({ animation }: { animation: string }) => (
    <div data-testid="lingu" data-animation={animation} />
  ),
}))

class MockAudio {
  static instances: MockAudio[] = []
  onended: (() => void) | null = null
  onerror: (() => void) | null = null
  play = vi.fn().mockResolvedValue(undefined)
  pause = vi.fn()
  constructor() {
    MockAudio.instances.push(this)
  }
}

function audioResponse() {
  return new Response(new Blob(['ID3audio'], { type: 'audio/mpeg' }))
}

function showTour(withNews = false) {
  return render(
    <NextIntlClientProvider locale="es" messages={es}>
      <OnboardingTour />
      {withNews && <WhatsNew />}
    </NextIntlClientProvider>
  )
}

beforeEach(() => {
  localStorage.clear()
  MockAudio.instances = []
  useAuthStore.setState({ accessToken: 'test-token', user: null })
  vi.stubGlobal('Audio', MockAudio)
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(audioResponse()))
  vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:tour-audio')
  vi.spyOn(URL, 'revokeObjectURL').mockImplementation(() => {})
  Object.defineProperties(HTMLDialogElement.prototype, {
    showModal: {
      configurable: true,
      value: function (this: HTMLDialogElement) {
        this.setAttribute('open', '')
      },
    },
    close: {
      configurable: true,
      value: function (this: HTMLDialogElement) {
        this.removeAttribute('open')
      },
    },
  })
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
  for (const name of ['showModal', 'close']) {
    const original = originalDialogMethods[name]
    if (original)
      Object.defineProperty(HTMLDialogElement.prototype, name, original)
    else Reflect.deleteProperty(HTMLDialogElement.prototype, name)
  }
})

describe('dashboard tour', () => {
  it('reopens all seven steps after legacy completion and defers the news modal', async () => {
    localStorage.setItem('fl_tour_done', '1')
    showTour(true)
    expect(await screen.findByRole('dialog')).toBeVisible()
    expect(screen.getByTestId('lingu')).toHaveAttribute(
      'data-animation',
      'saludo'
    )
    expect(screen.queryByText(es.whatsNew.title)).not.toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: es.tour.step1.title })
    ).toHaveFocus()
    for (let i = 0; i < 5; i++)
      fireEvent.click(screen.getByRole('button', { name: es.tour.next }))
    expect(screen.getByText(es.tour.step6.desc)).toBeVisible()
    expect(screen.getByText(es.games.detectiveTitle)).toBeVisible()
    expect(screen.getByText(es.games.sentenceOrderTitle)).toBeVisible()
    expect(screen.getByText(es.games.vocabularyPairsTitle)).toBeVisible()
    expect(screen.getByTestId('lingu')).toHaveAttribute(
      'data-animation',
      'animando'
    )
    fireEvent.click(screen.getByRole('button', { name: es.tour.prev }))
    fireEvent.click(screen.getByRole('button', { name: es.tour.next }))
    expect(screen.getByTestId('lingu')).toHaveAttribute(
      'data-animation',
      'reposo'
    )
    fireEvent.click(screen.getByRole('button', { name: es.tour.next }))
    expect(screen.getByTestId('lingu')).toHaveAttribute(
      'data-animation',
      'celebracion'
    )
    expect(fetch).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: es.tour.done }))
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(localStorage.getItem('fl_tour_done_v1.10.0')).toBe('1')
    expect(screen.queryByText(es.whatsNew.title)).not.toBeInTheDocument()
    expect(document.body.style.overflow).toBe('')
  })

  it('uses the UI language and selected voice only after a manual click', async () => {
    localStorage.setItem('tts_voice', 'coral')
    showTour()
    fireEvent.click(await screen.findByRole('button', { name: es.tour.listen }))
    await waitFor(() => expect(MockAudio.instances).toHaveLength(1))
    expect(fetch).toHaveBeenCalledWith(
      '/api/tts/tour/es/step1',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ text: es.tour.step1.desc, voice: 'coral' }),
      })
    )
    await waitFor(() =>
      expect(screen.getByTestId('lingu')).toHaveAttribute(
        'data-animation',
        'hablando'
      )
    )
    act(() => MockAudio.instances[0].onended?.())
    expect(screen.getByTestId('lingu')).toHaveAttribute(
      'data-animation',
      'reposo'
    )
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:tour-audio')
  })

  it('stops playback when changing steps and does not autoplay the next one', async () => {
    showTour()
    fireEvent.click(await screen.findByRole('button', { name: es.tour.listen }))
    await waitFor(() =>
      expect(screen.getByTestId('lingu')).toHaveAttribute(
        'data-animation',
        'hablando'
      )
    )
    const audio = MockAudio.instances[0]
    fireEvent.click(screen.getByRole('button', { name: es.tour.next }))
    expect(audio.pause).toHaveBeenCalled()
    expect(audio.onended).toBeNull()
    expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:tour-audio')
    expect(screen.getByTestId('lingu')).toHaveAttribute(
      'data-animation',
      'reposo'
    )
    expect(fetch).toHaveBeenCalledTimes(1)
  })

  it('discards a late audio response after navigation', async () => {
    let resolve!: (response: Response) => void
    vi.mocked(fetch).mockReturnValue(
      new Promise((done) => {
        resolve = done
      })
    )
    showTour()
    fireEvent.click(await screen.findByRole('button', { name: es.tour.listen }))
    const signal = vi.mocked(fetch).mock.calls[0][1]?.signal
    fireEvent.click(screen.getByRole('button', { name: es.tour.next }))
    expect(signal?.aborted).toBe(true)
    await act(async () => resolve(audioResponse()))
    expect(MockAudio.instances).toHaveLength(0)
    expect(screen.getByTestId('lingu')).toHaveAttribute(
      'data-animation',
      'reposo'
    )
  })

  it('stops playback on close and restores focus', async () => {
    const opener = document.createElement('button')
    document.body.appendChild(opener)
    opener.focus()
    showTour()
    fireEvent.click(await screen.findByRole('button', { name: es.tour.listen }))
    await waitFor(() => expect(MockAudio.instances).toHaveLength(1))
    fireEvent(
      screen.getByRole('dialog'),
      new Event('cancel', { cancelable: true })
    )
    expect(MockAudio.instances[0].pause).toHaveBeenCalled()
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(opener).toHaveFocus()
    opener.remove()
  })

  it('keeps navigation available after audio failure and permits retry', async () => {
    vi.mocked(fetch).mockResolvedValueOnce(new Response('', { status: 503 }))
    showTour()
    fireEvent.click(await screen.findByRole('button', { name: es.tour.listen }))
    expect(await screen.findByText(es.tour.audioError)).toBeVisible()
    expect(screen.getByRole('button', { name: es.tour.next })).toBeEnabled()
    fireEvent.click(screen.getByRole('button', { name: es.tour.listen }))
    await waitFor(() =>
      expect(screen.getByTestId('lingu')).toHaveAttribute(
        'data-animation',
        'hablando'
      )
    )
  })

  it('respects the current completion flag and allows the news modal instead', () => {
    localStorage.setItem('fl_tour_done_v1.10.0', '1')
    showTour(true)
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(screen.getByText(es.whatsNew.title)).toBeVisible()
    expect(fetch).not.toHaveBeenCalled()
  })
})
