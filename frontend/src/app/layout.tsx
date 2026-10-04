import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import './globals.css'
import './theme-modes.css'
import { ThemeProvider } from '@/components/ThemeProvider'
import { ThemeToggle } from '@/components/ThemeToggle'
import { NextIntlClientProvider } from 'next-intl'
import { getLocale, getMessages } from 'next-intl/server'
import { CookieBanner } from '@/components/CookieBanner'

export const metadata: Metadata = {
  metadataBase: new URL('https://jubalisan.com'),
  title: { default: 'JUBA LISAN', template: '%s | JUBA LISAN' },
  description: 'JUBA LISAN is a modern AI-powered language learning platform for speaking, listening, reading, vocabulary, grammar, and measurable progress.',
  keywords: ['JUBA LISAN', 'AI language learning', 'AI language tutor', 'learn languages', 'voice conversation', 'speaking practice', 'CEFR', 'language learning platform', 'vocabulary', 'grammar'],
  applicationName: 'JUBA LISAN',
  category: 'education',
  icons: { icon: [{ url: '/favicon.ico', sizes: 'any' }, { url: '/favicon.png', type: 'image/png' }], apple: '/apple-touch-icon.png' },
  openGraph: { type: 'website', locale: 'en_US', url: 'https://jubalisan.com', siteName: 'JUBA LISAN', title: 'JUBA LISAN — Learn languages naturally with AI', description: 'Practice real conversations, build vocabulary, master grammar, and follow a personalized path to fluency with JUBA LISAN.', images: [{ url: '/og-image-v2.png', width: 1200, height: 630, alt: 'JUBA LISAN — AI-powered language learning' }] },
  twitter: { card: 'summary_large_image', title: 'JUBA LISAN — AI-powered language learning', description: 'Practice speaking, listening, reading, vocabulary, and grammar with your personal AI tutor.', images: ['/og-image-v2.png'] },
}

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const locale = await getLocale()
  const messages = await getMessages()
  return <html suppressHydrationWarning lang={locale} dir={locale === 'ar' ? 'rtl' : 'ltr'} data-scroll-behavior="smooth" className={`${GeistSans.variable} ${GeistMono.variable} h-full antialiased`}>
    <head><meta name="theme-color" content="#fdfdfd" /><meta name="color-scheme" content="light dark" /></head>
    <body className="min-h-full bg-[var(--juba-bg)] text-[var(--juba-text)]"><NextIntlClientProvider locale={locale} messages={messages}><ThemeProvider><ThemeToggle/>{children}</ThemeProvider><CookieBanner/></NextIntlClientProvider></body>
  </html>
}
