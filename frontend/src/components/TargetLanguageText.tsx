import type { ElementType, HTMLAttributes, ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { getTargetLanguageTextClass } from '@/lib/target-languages'

interface TargetLanguageTextProps extends HTMLAttributes<HTMLElement> {
  languageCode?: string | null
  children: ReactNode
  as?: ElementType
  reading?: string | null
  translation?: string | null
}

export function TargetLanguageText({
  languageCode,
  children,
  as: Component = 'span',
  className,
  reading,
  translation,
  ...props
}: TargetLanguageTextProps) {
  const code = languageCode ?? ''

  return (
    <Component
      className={cn(getTargetLanguageTextClass(code), className)}
      lang={code || undefined}
      {...props}
    >
      {children}
      {(reading || translation) && (
        <span className="mt-1 block font-sans text-sm leading-relaxed tracking-normal normal-case">
          {[reading, translation].filter(Boolean).join(' · ')}
        </span>
      )}
    </Component>
  )
}
