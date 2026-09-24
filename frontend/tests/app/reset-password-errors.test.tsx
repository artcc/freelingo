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

    expect(await screen.findByRole('alert')).toHaveTextContent(message)
    expect(screen.queryByText(detail)).toBeNull()
  })

  it.each([
    ['Valid12!', 'auth.resetPassword.tooShort'],
    ['Valid123!', 'auth.resetPassword.tooShort'],
    [`A1!${'😀'.repeat(6)}`, 'auth.resetPassword.tooShort'],
    [`A1!${'a'.repeat(23)}`, 'auth.register.invalidPassword'],
  ])('rejects an invalid password length before submitting: %s', async (password, message) => {
    render(<ResetPasswordPage />)
    fireEvent.change(screen.getByPlaceholderText('auth.resetPassword.newPassword'), {
      target: { value: password },
    })
    fireEvent.change(screen.getByPlaceholderText('auth.resetPassword.confirmPassword'), {
      target: { value: password },
    })
    fireEvent.click(screen.getByRole('button', { name: 'auth.resetPassword.submit' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(message)
    expect(apiFetch).not.toHaveBeenCalled()
  })

  it.each(['Abcdefg1!?', `A1!${'a'.repeat(22)}`, `A1!${'😀'.repeat(22)}`])(
    'submits a password within the backend length limits: %s',
    async (password) => {
      apiFetch.mockResolvedValue(new Response(null, { status: 503 }))
      render(<ResetPasswordPage />)
      fireEvent.change(screen.getByPlaceholderText('auth.resetPassword.newPassword'), {
        target: { value: password },
      })
      fireEvent.change(screen.getByPlaceholderText('auth.resetPassword.confirmPassword'), {
        target: { value: password },
      })
      fireEvent.click(screen.getByRole('button', { name: 'auth.resetPassword.submit' }))

      expect(await screen.findByRole('alert')).toHaveTextContent('common.errorMessage')
      expect(apiFetch).toHaveBeenCalledWith(
        '/api/auth/reset-password',
        expect.objectContaining({
          body: JSON.stringify({ token: 'valid', new_password: password }),
        })
      )
    }
  )

  it('shows the translated password requirements before submission', () => {
    render(<ResetPasswordPage />)

    expect(screen.getByPlaceholderText('auth.resetPassword.newPassword')).toHaveAccessibleDescription(
      'auth.register.invalidPassword'
    )
  })
})
