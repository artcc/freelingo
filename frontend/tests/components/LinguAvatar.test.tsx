import React, { StrictMode } from 'react'
import { renderToString } from 'react-dom/server'
import { act, cleanup, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import LinguAvatar, {
  type LinguSceneProps,
} from '@/components/lingu/LinguAvatar'
import AppLoading from '@/app/(app)/loading'
import { useLoadingStore } from '@/store/loading'

const scene = vi.hoisted(() => ({ props: null as LinguSceneProps | null }))

vi.mock('next/dynamic', () => ({
  default: () =>
    function MockScene(props: LinguSceneProps) {
      scene.props = props
      return <span data-testid="scene">Animated Lingu</span>
    },
}))

vi.mock('next/image', () => ({
  default: ({
    fill,
    ...props
  }: React.ImgHTMLAttributes<HTMLImageElement> & {
    fill?: boolean
  }) => {
    void fill
    return React.createElement('img', props)
  },
}))

vi.mock('next-intl', () => ({
  useTranslations: () => (key: string) => key,
}))

beforeEach(() => {
  scene.props = null
  vi.spyOn(window, 'matchMedia').mockReturnValue({
    matches: false,
    media: '(prefers-reduced-motion: reduce)',
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(() => true),
  })
  useLoadingStore.setState({ count: 0, complete: false })
})

afterEach(() => {
  cleanup()
  useLoadingStore.setState({ count: 0, complete: false })
})

describe('Lingu loading fallback', () => {
  it('does not flash static artwork before the motion preference is known', () => {
    const onReady = vi.fn()
    const html = renderToString(
      <LinguAvatar animation="reposo" onReady={onReady} />
    )

    expect(html).not.toContain('/logo.png')
    expect(scene.props).toBeNull()
    expect(onReady).not.toHaveBeenCalled()
  })

  it('resolves to static artwork when the scene fails', () => {
    const onReady = vi.fn()
    const { container } = render(
      <LinguAvatar animation="pensando" onReady={onReady} />
    )

    act(() => scene.props!.onError())

    expect(container.querySelector('img')).toBeVisible()
    expect(screen.queryByTestId('scene')).not.toBeInTheDocument()
    expect(onReady).toHaveBeenCalledTimes(1)
  })

  it('uses only static artwork when reduced motion is enabled', () => {
    const query = window.matchMedia('(prefers-reduced-motion: reduce)')
    vi.mocked(window.matchMedia).mockReturnValue({ ...query, matches: true })
    const onReady = vi.fn()
    const { container } = render(
      <LinguAvatar animation="reposo" onReady={onReady} />
    )

    expect(container.querySelector('img')).toBeVisible()
    expect(scene.props).toBeNull()
    expect(onReady).toHaveBeenCalledTimes(1)
  })

  it('passes readiness to the scene without showing static artwork while it loads', () => {
    const onReady = vi.fn()
    const { container } = render(
      <LinguAvatar animation="saludo" onReady={onReady} />
    )

    expect(container.querySelector('img')).toBeNull()
    expect(screen.getByTestId('scene')).toBeVisible()
    expect(scene.props!.onReady).toBe(onReady)
    expect(onReady).not.toHaveBeenCalled()

    act(() => scene.props!.onReady?.())
    expect(onReady).toHaveBeenCalledTimes(1)
  })

  it('releases the route loading slot before the avatar is ready without clearing other activity', () => {
    useLoadingStore.setState({ count: 2, complete: false })
    const { unmount } = render(
      <StrictMode>
        <AppLoading />
      </StrictMode>
    )

    expect(screen.getByRole('status', { name: 'loading' })).toBeInTheDocument()
    expect(screen.getByText('loading')).toBeVisible()
    expect(screen.getByTestId('scene')).toBeInTheDocument()
    expect(useLoadingStore.getState().count).toBe(3)

    unmount()

    expect(useLoadingStore.getState().count).toBe(2)
    expect(useLoadingStore.getState().complete).toBe(false)
  })
})
