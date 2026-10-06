/** Navigation metadata only; game content and progress belong to the backend. */
interface GameDefinition {
  id: string
  href: `/games/${string}`
  titleKey: string
  descriptionKey: string
}

// Register only implemented games with working routes and localized copy.
export const availableGames: readonly GameDefinition[] = []
