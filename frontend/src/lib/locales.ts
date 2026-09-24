// Single source of truth for supported locales.
// This file must remain a pure ES module (no Node.js APIs) so it can be
// imported from both the Edge-runtime middleware and server-side code.

export const SUPPORTED_LOCALES = [
  'en',
  'es',
  'fr',
  'pt',
  'de',
  'it',
  'pl',
  'nl',
  'ro',
  'ru',
  'tr',
  'sv',
  'da',
] as const

export type Locale = (typeof SUPPORTED_LOCALES)[number]
