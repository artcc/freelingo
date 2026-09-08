import { useTranslations } from 'next-intl'

export type ConvStatus =
  | 'loading'
  | 'ready'
  | 'warming'
  | 'connecting'
  | 'live'
  | 'ended'
  | 'error'

interface Props {
  status: ConvStatus
  userSpeaking: boolean
  assistantSpeaking: boolean
}

export default function StatusIndicator({
  status,
  userSpeaking,
  assistantSpeaking,
}: Props) {
  const t = useTranslations('conversation')

  let label: string
  let dotClass = 'text-fl-muted-4'
  let pulse = false

  if (status === 'loading') {
    label = t('statusLoading')
  } else if (status === 'warming') {
    label = t('statusWarming')
    pulse = true
  } else if (status === 'connecting') {
    label = t('statusConnecting')
    pulse = true
  } else if (status === 'live') {
    if (userSpeaking) {
      label = t('statusDetecting')
      dotClass = 'text-fl-accent'
      pulse = true
    } else if (assistantSpeaking) {
      label = t('statusSpeaking')
      dotClass = 'text-fl-accent'
      pulse = true
    } else {
      label = t('statusListening')
      dotClass = 'text-fl-muted-2'
    }
  } else if (status === 'ended') {
    label = t('sessionEnded')
  } else if (status === 'error') {
    label = t('statusError')
    dotClass = 'text-fl-error'
  } else {
    // ready
    label = t('statusReady')
  }

  return (
    <div className="flex items-center gap-2">
      <span
        className={`text-fl-label ${dotClass} ${pulse ? 'animate-pulse' : ''}`}
      >
        ●
      </span>
      <span className="text-fl-fg font-mono text-xs font-semibold tracking-wide uppercase">
        {label}
      </span>
    </div>
  )
}
