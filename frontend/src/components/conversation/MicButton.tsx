import { useTranslations } from 'next-intl'
import type { ConvStatus } from './StatusIndicator'

interface Props {
  status: ConvStatus
  sessionActive?: boolean
  onStart: () => void
  onStop: () => void
}

export default function MicButton({ status, onStart, onStop }: Props) {
  const t = useTranslations('conversation')

  if (status === 'loading') {
    return (
      <button
        disabled
        className="border-fl-border bg-fl-surface flex h-16 w-16 items-center justify-center rounded-full border-2 opacity-40"
        aria-label={t('statusLoading')}
      >
        <span className="text-fl-muted-4 animate-pulse font-mono text-xl">
          ◌
        </span>
      </button>
    )
  }

  if (status === 'warming') {
    return (
      <button
        disabled
        className="border-fl-border bg-fl-surface flex h-16 w-16 items-center justify-center rounded-full border-2 opacity-60"
        aria-label={t('statusWarming')}
      >
        <span className="text-fl-muted-2 animate-pulse font-mono text-xl">
          ○
        </span>
      </button>
    )
  }

  if (status === 'connecting') {
    return (
      <button
        disabled
        className="border-fl-border bg-fl-surface flex h-16 w-16 items-center justify-center rounded-full border-2 opacity-60"
        aria-label={t('statusConnecting')}
      >
        <span className="text-fl-muted-2 animate-pulse font-mono text-xl">
          ○
        </span>
      </button>
    )
  }

  if (status === 'ready') {
    return (
      <button
        onClick={onStart}
        className="bg-fl-accent text-fl-accent-fg hover:bg-fl-accent/90 px-8 py-3 font-mono text-sm font-bold tracking-widest uppercase transition-colors"
      >
        {t('start')}
      </button>
    )
  }

  if (status === 'live') {
    return (
      <button
        onClick={onStop}
        className="border-fl-error/60 bg-fl-surface hover:bg-fl-error/10 group flex h-16 w-16 items-center justify-center rounded-full border-2 transition-colors"
        aria-label={t('stop')}
        title={t('stop')}
      >
        <span className="text-fl-error font-mono text-lg transition-transform group-hover:scale-110">
          ■
        </span>
      </button>
    )
  }

  // ended or error → offer restart
  return (
    <button
      onClick={onStart}
      className="border-fl-border text-fl-muted-2 hover:text-fl-fg hover:border-fl-border-2 border px-8 py-3 font-mono text-sm tracking-widest uppercase transition-colors"
    >
      {t('startNew')}
    </button>
  )
}
