/** Navigation metadata only; game content and progress belong to the backend. */
interface GameDefinition {
  id: string
  href: `/games/${string}`
  titleKey: string
  descriptionKey: string
}

// Register only implemented games with working routes and localized copy.
export const availableGames: readonly GameDefinition[] = [
  {
    id: 'error-detective',
    href: '/games/error-detective',
    titleKey: 'detectiveTitle',
    descriptionKey: 'detectiveDescription',
  },
  {
    id: 'sentence-order',
    href: '/games/sentence-order',
    titleKey: 'sentenceOrderTitle',
    descriptionKey: 'sentenceOrderDescription',
  },
]
