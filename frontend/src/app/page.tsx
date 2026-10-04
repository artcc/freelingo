import Link from 'next/link'
import {cookies} from 'next/headers'
import {getLocale,getTranslations} from 'next-intl/server'
import type {Metadata} from 'next'
import PricingSection from '@/components/billing/PricingSection'
import {LandingFAQ} from '@/components/ui/landing-faq'
import {ContactButton} from '@/components/ui/contact-button'
import {LandingReviewsCarousel} from '@/components/reviews/LandingReviewsCarousel'
import type {ReviewPublic} from '@/types/api'
import {normalizeLocale} from '@/lib/locales'
import './landing-refresh.css'

export const metadata:Metadata={
  title:'JUBA LISAN | Learn languages naturally with AI',
  description:'Learn languages naturally with AI through speaking, listening, reading, vocabulary, grammar, and personalized practice.',
  robots:{index:true,follow:true},
  openGraph:{title:'JUBA LISAN | AI-powered language learning',description:'Speaking, listening, reading and personalized language practice.',url:'https://jubalisan.com',type:'website',images:[{url:'/og-image-v2.png',width:1200,height:630,alt:'JUBA LISAN | AI-powered language learning'}]},
  twitter:{card:'summary_large_image',title:'JUBA LISAN | AI-powered language learning',description:'Learn with an AI tutor, voice conversations, flashcards, and structured grammar lessons.',images:['/og-image-v2.png']},
}

/** Original Juba owl artwork. No Duolingo logos, characters or product claims. */
function LinguArtwork({id}:{id:string}){
  return <svg className="jl-mascot" viewBox="0 0 420 380" fill="none" aria-hidden="true">
    <defs><linearGradient id={id} x1="80" y1="80" x2="340" y2="330" gradientUnits="userSpaceOnUse"><stop stopColor="var(--jl-mint)"/><stop offset=".5" stopColor="var(--jl-blue)"/><stop offset="1" stopColor="var(--jl-purple)"/></linearGradient></defs>
    <g transform="rotate(-13 210 190)">
      <path d="M105 110 116 61 161 87Q210 65 259 87L304 61 315 110Q354 133 341 238Q322 318 210 329Q99 318 79 238Q66 133 105 110Z" fill={`url(#${id})`} stroke="var(--jl-paper)" strokeWidth="9"/>
      <path d="M116 130Q130 106 170 113Q210 131 250 113Q290 106 305 130L300 197Q256 225 210 196Q165 225 121 197Z" fill="var(--jl-face)"/>
      <ellipse cx="158" cy="157" rx="20" ry="29" fill="var(--jl-eye)"/><ellipse cx="265" cy="157" rx="20" ry="29" fill="var(--jl-eye)"/>
      <ellipse cx="165" cy="148" rx="6" ry="9" fill="var(--jl-paper)"/><ellipse cx="272" cy="148" rx="6" ry="9" fill="var(--jl-paper)"/>
      <path d="m194 186 16 22 16-22Z" fill="var(--jl-gold)"/>
      <path d="M170 246q40 38 80 0M180 277q30 25 60 0" stroke="var(--jl-mint)" strokeWidth="12" strokeLinecap="round"/>
      <path d="M90 156C78 37 342 37 330 156" stroke="var(--jl-purple)" strokeWidth="17"/>
      <rect x="74" y="136" width="26" height="70" rx="13" fill="var(--jl-pink)"/><rect x="320" y="136" width="26" height="70" rx="13" fill="var(--jl-pink)"/>
      <path d="M88 193q-6 35 47 39" stroke="var(--jl-purple)" strokeWidth="10" strokeLinecap="round"/><ellipse cx="142" cy="234" rx="14" ry="10" fill="var(--jl-pink)"/>
    </g>
    <path d="m53 100 4 11 11 4-11 4-4 11-4-11-11-4 11-4Zm301 192 5 13 13 5-13 5-5 13-5-13-13-5 13-5Z" fill="var(--jl-paper)"/>
  </svg>
}

/** Schematic product artwork, not fabricated learner statistics or a live session. */
function PracticeArtwork({variant,label}:{variant:number;label:string}){
  return <div className={`jl-phone jl-phone-${variant}`} aria-hidden="true"><div className="jl-phone-head"><span>Lingu</span><span className="jl-online"/></div><div className="jl-phone-progress"><span/></div><div className="jl-phone-orbit"><span>{variant===0?'✦':variant===1?'✓':'◇'}</span></div><div className="jl-phone-lines"><i/><i/><i/></div><div className="jl-wave">{[18,30,45,28,52,35,20].map((height,index)=><i key={index} style={{height}}/>)}</div><div className="jl-phone-button">{label}</div><span className="jl-phone-spark">✧</span></div>
}

const LEARNING_LANGUAGES=[
  {code:'en-GB',name:'English',flag:'🇬🇧'},{code:'en-US',name:'English (US)',flag:'🇺🇸'},
  {code:'es',name:'Español',flag:'🇪🇸'},{code:'fr',name:'Français',flag:'🇫🇷'},
  {code:'de',name:'Deutsch',flag:'🇩🇪'},{code:'it',name:'Italiano',flag:'🇮🇹'},
  {code:'pt',name:'Português',flag:'🇵🇹'},{code:'ja',name:'日本語',flag:'🇯🇵'},
  {code:'ko',name:'한국어',flag:'🇰🇷'},{code:'zh',name:'中文',flag:'🇨🇳'},
  {code:'ar',name:'العربية',flag:'🇸🇦'},
]
const INTERFACE_LOCALES=[['en','English'],['ar','العربية'],['es','Español'],['fr','Français'],['pt','Português'],['de','Deutsch'],['it','Italiano'],['pl','Polski'],['nl','Nederlands'],['ro','Română'],['ru','Русский']]

export default async function Home(){
  const cookieStore=await cookies()
  const hasSession=cookieStore.has('refresh_token')
  const locale=normalizeLocale(await getLocale())
  const dir=locale==='ar'?'rtl':'ltr'
  const t=await getTranslations('landing')
  const common=await getTranslations('common')
  const billing=await getTranslations('billing')
  let allowRegistration=false,stripeEnabled=false,trialDays=7
  let priceMonthly=0,priceYearly=0,totalPriceMonthly=0,totalPriceYearly=0
  let reviews:ReviewPublic[]=[]
  const backendUrl=process.env.BACKEND_URL||'http://backend:8000'
  // Billing config and approved reviews fail independently. Never invent either.
  const [configResponse,reviewsResponse]=await Promise.allSettled([
    fetch(`${backendUrl}/api/config`,{next:{revalidate:3600}}),
    fetch(`${backendUrl}/api/reviews/public?limit=100`,{next:{revalidate:300}}),
  ])
  if(configResponse.status==='fulfilled'&&configResponse.value.ok){
    try{const cfg=await configResponse.value.json();allowRegistration=cfg.allow_registration===true;stripeEnabled=cfg.stripe_enabled===true;trialDays=cfg.stripe_trial_days??7;priceMonthly=cfg.price_monthly??0;priceYearly=cfg.price_yearly??0;totalPriceMonthly=cfg.total_price_monthly??0;totalPriceYearly=cfg.total_price_yearly??0}catch{/* Conservative defaults. */}
  }
  if(reviewsResponse.status==='fulfilled'&&reviewsResponse.value.ok){
    try{const data=await reviewsResponse.value.json();reviews=Array.isArray(data)?data:[]}catch{/* Only real public reviews. */}
  }
  const href=hasSession?'/dashboard':allowRegistration?'/register':'/login'
  const cta=hasSession?t('dashboard'):allowRegistration?t('ctaStart'):t('signIn')
  const features=[{title:t('feature1Title'),desc:t('feature1Desc'),icon:'◈'},{title:t('feature2Title'),desc:t('feature2Desc'),icon:'✦'},{title:t('feature3Title'),desc:t('feature3Desc'),icon:'◇'}]
  const jsonLd={'@context':'https://schema.org','@type':'SoftwareApplication',name:'JUBA LISAN',applicationCategory:'EducationApplication',operatingSystem:'Web',url:'https://jubalisan.com',description:'AI-powered language learning with conversation, vocabulary, grammar, listening and reading.'}
  return <div className="juba-landing-refresh" dir={dir}>
    <script type="application/ld+json" dangerouslySetInnerHTML={{__html:JSON.stringify(jsonLd)}}/>
    <a className="jl-skip" href="#main-content">{t('skipToContent')}</a>
    <header className="jl-nav"><div className="jl-wrap jl-nav-inner"><Link href={locale==='en'?'/':`/${locale}`} aria-label={t('homeLabel')} className="jl-brand"><strong>JUBA</strong><span>LISAN</span></Link><nav className="jl-nav-links" aria-label={common('menu')}><a href="#features">{t('navFeatures')}</a><a href="#pricing">{t('navPricing')}</a></nav><div className="jl-nav-actions"><details className="jl-locale"><summary aria-label={t('interfaceLanguages')}>{locale.toUpperCase()} <span aria-hidden="true">⌄</span></summary><nav aria-label={t('interfaceLanguages')}>{INTERFACE_LOCALES.map(([code,name])=><Link key={code} href={code==='en'?'/':`/${code}`} lang={code} dir="auto" hrefLang={code} aria-current={locale===code?'page':undefined}>{name}</Link>)}</nav></details><Link className="jl-nav-cta" href={hasSession?'/dashboard':'/login'}>{hasSession?t('dashboard'):t('signIn')}</Link></div></div></header>
    <main id="main-content">
      <section className="jl-hero" aria-labelledby="landing-hero-title"><div className="jl-wrap jl-hero-inner"><div className="jl-hero-copy"><span className="jl-eyebrow">JUBA LISAN</span><h1 id="landing-hero-title">{t('heroTitle')}</h1><p>{t('heroSub')}</p><Link className="jl-primary" href={href}>{cta}</Link></div><div className="jl-hero-art"><div className="jl-flight" aria-hidden="true"/><LinguArtwork id="jl-hero-lingu"/></div></div></section>
      <section id="languages" className="jl-languages" aria-labelledby="landing-languages-title"><div className="jl-wrap"><h2 id="landing-languages-title" className="jl-sr-only">{t('navLanguages')}</h2><div className="jl-language-scroll" role="region" aria-label={t('navLanguages')} tabIndex={0}><ul>{LEARNING_LANGUAGES.map(language=><li key={language.code}><span aria-hidden="true">{language.flag}</span><span lang={language.code} dir="auto">{language.name}</span></li>)}</ul></div></div></section>
      <section id="pricing" className="jl-pricing"><div className="jl-wrap"><PricingSection stripeEnabled={stripeEnabled} trialDays={trialDays} hasSession={hasSession} priceMonthly={priceMonthly} priceYearly={priceYearly} totalPriceMonthly={totalPriceMonthly} totalPriceYearly={totalPriceYearly}/></div></section>
      <section className="jl-learning-band" aria-label={t('navFeatures')}><div className="jl-wrap">{features.map((feature,index)=><div key={feature.title}><span className="jl-band-icon" aria-hidden="true">{index===0?'Lingu':index===1?'A1 → C2':'✦'}</span><span>{feature.title}</span></div>)}</div></section>
      <section id="features" className="jl-features" aria-labelledby="landing-features-title"><div className="jl-wrap"><header className="jl-section-head"><h2 id="landing-features-title">{t('navFeatures')}</h2><p>{common('tagline')}</p></header><fieldset className="jl-feature-stage"><legend className="jl-sr-only">{t('navFeatures')}</legend>{features.map((feature,index)=><input className="jl-feature-radio" type="radio" name="landing-feature" id={`jl-feature-${index}`} key={index} defaultChecked={index===0} aria-controls={`jl-panel-${index}`}/>)}<div className="jl-feature-options">{features.map((feature,index)=><label key={feature.title} htmlFor={`jl-feature-${index}`}><span aria-hidden="true">{feature.icon}</span>{feature.title}</label>)}</div><div className="jl-feature-panels">{features.map((feature,index)=><article className={`jl-feature-panel jl-feature-panel-${index}`} id={`jl-panel-${index}`} key={feature.title} aria-labelledby={`jl-panel-title-${index}`}><div className="jl-feature-visual"><PracticeArtwork variant={index} label={feature.title}/><div className="jl-small-lingu"><LinguArtwork id={`jl-feature-lingu-${index}`}/></div></div><div className="jl-feature-copy"><h3 id={`jl-panel-title-${index}`}>{feature.title}</h3><p>{feature.desc}</p></div></article>)}</div></fieldset><div className="jl-center"><Link className="jl-primary" href={href}>{cta}</Link></div></div></section>
      <section className="jl-open-source"><div className="jl-wrap jl-open-source-inner"><div><h2>{billing('openSourceTitle')}</h2><p>{billing('openSourceDesc')}</p><a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer" className="jl-primary">{billing('openSourceCta')} <span aria-hidden="true">↗</span></a></div><div className="jl-community-art" aria-hidden="true"><LinguArtwork id="jl-community-lingu"/><span>✦</span></div></div></section>
      <section className="jl-journey" aria-labelledby="jl-journey-title"><div className="jl-wrap jl-journey-inner"><div><h2 id="jl-journey-title">{t('heroTitle')}</h2><p>{t('heroSub')}</p></div><ol>{features.map((feature,index)=><li key={feature.title}><span className="jl-step" aria-hidden="true">{index+1}</span><div><h3>{feature.title}</h3><p>{feature.desc}</p></div></li>)}</ol></div></section>
      {reviews.length>0&&<section id="reviews" className="jl-reviews" aria-labelledby="landing-reviews-title"><div className="jl-wrap"><h2 id="landing-reviews-title">{t('navReviews')}</h2><LandingReviewsCarousel reviews={reviews}/></div></section>}
      <section id="faq" className="jl-faq" aria-labelledby="landing-faq-title"><div className="jl-wrap"><h2 id="landing-faq-title">{t('faqTitle')}</h2><LandingFAQ dir={dir}/></div></section>
    </main>
    <footer className="jl-footer"><div className="jl-wrap"><div className="jl-footer-top"><div><h2>{common('tagline')}</h2><p>{t('footerTagline')}</p></div><Link className="jl-primary" href={href}>{cta}</Link></div><div className="jl-footer-grid"><div className="jl-footer-brand"><strong>JUBA LISAN</strong><small>© {new Date().getFullYear()} JUBA LISAN</small></div><nav aria-label={t('footerProduct')}><h3>{t('footerProduct')}</h3><a href="#features">{t('navFeatures')}</a><a href="#languages">{t('navLanguages')}</a>{reviews.length>0&&<a href="#reviews">{t('navReviews')}</a>}<a href="#pricing">{t('navPricing')}</a></nav><nav aria-label={t('footerResources')}><h3>{t('footerResources')}</h3><a href="#faq">{t('navFAQ')}</a><a href="https://github.com/abdelhadiLRS/JUBA_LISAN" target="_blank" rel="noopener noreferrer">{t('github')}</a><ContactButton/></nav><nav aria-label={t('footerLegal')}><h3>{t('footerLegal')}</h3><Link href="/privacy?from=landing">{t('privacy')}</Link><Link href="/terms?from=landing">{t('terms')}</Link></nav></div></div></footer>
  </div>
}
