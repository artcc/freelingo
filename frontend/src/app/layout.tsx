import type { Metadata } from 'next'
import {
  Geist,
  Geist_Mono,
  Noto_Sans_JP,
  Noto_Sans_KR,
  Noto_Sans_SC,
} from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/ThemeProvider'
import { NextIntlClientProvider } from 'next-intl'
import { getLocale, getMessages } from 'next-intl/server'
import { CookieBanner } from '@/components/CookieBanner'
import { getUmamiConfig } from '@/lib/umami-config'
import { SITE_URL } from '@/lib/seo'

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin', 'cyrillic'],
})

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
})

const notoSansJP = Noto_Sans_JP({
  variable: '--font-noto-ja',
  subsets: ['latin'],
  preload: false,
})

const notoSansKR = Noto_Sans_KR({
  variable: '--font-noto-ko',
  subsets: ['latin'],
  preload: false,
})

const notoSansSC = Noto_Sans_SC({
  variable: '--font-noto-zh',
  subsets: ['latin'],
  preload: false,
})

const themeScript = `(function(){try{var t='system';var s=localStorage.getItem('fl-theme');if(s){var p=JSON.parse(s);t=p&&p.state&&p.state.theme?p.state.theme:t}var l=t==='light'||(t==='system'&&window.matchMedia('(prefers-color-scheme: light)').matches);if(l){document.documentElement.setAttribute('data-theme','light')}else{document.documentElement.removeAttribute('data-theme')}}catch(e){}})();`

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'FreeLingo',
    template: '%s | FreeLingo',
  },
  // Public content opts in at its own route; private and account pages stay out.
  robots: { index: false, follow: true },
  authors: [
    {
      name: 'Arturo Carretero Calvo',
      url: 'https://www.arturocarreterocalvo.com',
    },
  ],
  creator: 'Arturo Carretero Calvo',
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/favicon.png', type: 'image/png' },
    ],
    apple: '/apple-touch-icon.png',
  },
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const locale = await getLocale()
  const messages = await getMessages()
  const umami = getUmamiConfig()

  return (
    <html
      suppressHydrationWarning
      lang={locale}
      className={`${geistSans.variable} ${geistMono.variable} ${notoSansJP.variable} ${notoSansKR.variable} ${notoSansSC.variable} h-full antialiased`}
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){if(document.cookie.indexOf('LOCALE_DETECTED=')!==-1)return;var m=document.cookie.match(/(^| )NEXT_LOCALE=([^;]+)/);var cl=m?m[2]:null;var bl=(navigator.language||'').split('-')[0].toLowerCase();var s=['es','fr','pt','de','it','pl','nl','ro','ru','tr','sv','da','fi','hr'];document.cookie='LOCALE_DETECTED=1;path=/;max-age=31536000;SameSite=Lax';if(cl==='en'||s.indexOf(cl)!==-1)return;if(bl!=='en'&&s.indexOf(bl)!==-1&&cl!==bl){document.cookie='NEXT_LOCALE='+bl+';path=/;max-age=31536000;SameSite=Lax';location.reload()}})();`,
          }}
        />
        {umami && (
          <script
            defer
            src="/umami/script.js"
            data-host-url="/umami"
            data-website-id={umami.websiteId}
            data-exclude-search="true"
            data-exclude-hash="true"
          />
        )}
      </head>
      <body className="bg-background text-foreground min-h-full">
        <NextIntlClientProvider locale={locale} messages={messages}>
          <ThemeProvider>{children}</ThemeProvider>
          <CookieBanner />
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
