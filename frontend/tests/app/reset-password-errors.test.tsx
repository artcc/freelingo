import { fireEvent, render, screen } from '@testing-library/react'
import React from 'react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import ResetPasswordPage from '@/app/(auth)/reset-password/page'

const apiFetch = vi.hoisted(() => vi.fn())

vi.mock('@/lib/api', () => ({ apiFetch }))
vi.mock('next-intl', () => ({
  useTranslations: (namespace: string) => (key: string) => `${namespace}.${key}`,
}))
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn() }),
  useSearchParams: () => new URLSearchParams('token=valid'),
}))
vi.mock('next/link', () => ({
  default: ({ href, children }: React.PropsWithChildren<{ href: string }>) => (
    <a href={href}>{children}</a>
  ),
}))

describe('reset password errors', () => {
  beforeEach(() => apiFetch.mockReset())

  it.each([
    [400, 'Invalid or expired reset token', 'auth.resetPassword.error'],
    [422, 'Password validation failed', 'auth.register.invalidPassword'],
    [503, 'Service unavailable', 'common.errorMessage'],
  ])('localizes HTTP %i without exposing the backend detail', async (status, detail, message) => {
    apiFetch.mockResolvedValue(
      new Response(JSON.stringify({ detail }), {
        status,
        headers: { 'Content-Type': 'application/json' },
      })
    )
    render(<ResetPasswordPage />)

    fireEvent.change(screen.getByPlaceholderText('auth.resetPassword.newPassword'), {
      target: { value: 'ValidPwd12!' },
    })
    fireEvent.change(screen.getByPlaceholderText('auth.resetPassword.confirmPassword'), {
      target: { value: 'ValidPwd12!' },
    })
    fireEvent.click(screen.getByRole('button', { name: 'auth.resetPassword.submit' }))

    expect(await screen.findByText(new RegExp(message))).toBeInTheDocument()
    expect(screen.queryByText(detail)).toBeNull()
  })
})
