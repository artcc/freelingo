import type { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'FreeLingo',
    short_name: 'FreeLingo',
    description: 'AI-powered language learning platform',
    start_url: '/',
    display: 'standalone',
    background_color: '#0c1316',
    theme_color: '#0c1316',
    icons: [
      { src: '/favicon.png', sizes: '32x32', type: 'image/png' },
      { src: '/logo.png', sizes: '72x72', type: 'image/png' },
    ],
  }
}
