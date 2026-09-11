'use client'

import { type ReactNode } from 'react'
import Link from 'next/link'
import { type LucideIcon } from 'lucide-react'

interface SettingsPageHeaderProps {
  title: string
  eyebrow: string
  description?: string
}

export function SettingsPageHeader({
  title,
  eyebrow,
  description,
}: SettingsPageHeaderProps) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div className="min-w-0">
        <div className="mb-2 flex items-center gap-2">
          <span className="text-fl-label text-fl-muted-2">●</span>
          <span className="text-fl-muted-1 font-mono text-xs tracking-widest uppercase">
            {eyebrow}
          </span>
        </div>
        <h1 className="text-fl-fg font-mono text-2xl font-semibold tracking-tight">
          {title}
        </h1>
        {description && (
          <p className="text-fl-muted-3 mt-2 max-w-2xl font-mono text-sm leading-relaxed">
            {description}
          </p>
        )}
      </div>
    </div>
  )
}

export function SettingsNav({
  items,
}: {
  items: { href: string; label: string; icon: LucideIcon }[]
}) {
  return (
    <div className="border-fl-border bg-fl-surface flex flex-wrap items-center gap-1 border p-1">
      {items.map((item) => {
        const Icon = item.icon
        return (
          <a
            key={item.href}
            href={item.href}
            className="text-fl-muted-2 hover:bg-fl-bg hover:text-fl-fg focus:bg-fl-bg focus:text-fl-fg flex min-h-9 items-center gap-2 border-l-2 border-transparent px-3 py-2 font-mono text-xs tracking-widest uppercase transition-colors focus:outline-none"
          >
            <Icon className="size-3.5" aria-hidden="true" />
            {item.label}
          </a>
        )
      })}
    </div>
  )
}

export function SettingsPanel({
  id,
  title,
  children,
}: {
  id?: string
  title?: string
  children: ReactNode
}) {
  return (
    <section id={id} className="scroll-mt-24 space-y-3">
      {title && (
        <div className="flex items-center gap-2 px-1">
          <span className="text-fl-label text-fl-muted-2">●</span>
          <h2 className="text-fl-muted-1 font-mono text-xs tracking-widest uppercase">
            {title}
          </h2>
        </div>
      )}
      {children}
    </section>
  )
}

export function SettingsActionCard({
  href,
  label,
  description,
  icon: Icon,
}: {
  href: string
  label: string
  description: string
  icon: LucideIcon
}) {
  return (
    <Link
      href={href}
      className="border-fl-border bg-fl-surface hover:border-fl-border-2 group block border p-5 transition-colors"
    >
      <div className="mb-5 flex items-center justify-between gap-3">
        <Icon
          className="text-fl-muted-2 group-hover:text-fl-fg size-5 transition-colors"
          aria-hidden="true"
        />
        <span className="text-fl-muted-4 group-hover:text-fl-muted-2 font-mono text-lg transition-colors">
          ›
        </span>
      </div>
      <p className="text-fl-fg font-mono text-sm tracking-widest uppercase">
        {label}
      </p>
      <p className="text-fl-muted-2 mt-2 font-mono text-sm leading-relaxed">
        {description}
      </p>
    </Link>
  )
}
