'use client'

import {Moon,Sun} from 'lucide-react'
import {useLocale,useTranslations} from 'next-intl'
import {useThemeStore} from '@/store/theme'

export function ThemeToggle(){
 const locale=useLocale(),t=useTranslations('settings'),theme=useThemeStore(s=>s.theme),setTheme=useThemeStore(s=>s.setTheme)
 const isLight=theme==='light'
 const next=isLight?'dark':'light'
 const label=isLight?(locale==='ar'?'تفعيل الوضع الليلي':'Switch to dark mode'):(locale==='ar'?'تفعيل الوضع النهاري':'Switch to light mode')
 return <button type="button" className="juba-theme-toggle" onClick={()=>setTheme(next)} aria-label={label} title={label} data-theme-choice={theme}>
  {isLight?<Moon size={17} aria-hidden="true"/>:<Sun size={17} aria-hidden="true"/>}
  <span>{isLight?t('themeLight'):t('themeDark')}</span>
 </button>
}
