function runtimeEnv(name: string): string | undefined {
  // Dynamic lookup keeps published server images configurable at container startup.
  return process.env[name]
}

export function getUmamiConfig(): {
  scriptUrl: string
  websiteId: string
} | null {
  const scriptUrl = runtimeEnv('NEXT_PUBLIC_UMAMI_SCRIPT_URL')?.trim()
  const websiteId = runtimeEnv('NEXT_PUBLIC_UMAMI_WEBSITE_ID')
    ?.trim()
    .toLowerCase()
  if (
    !scriptUrl ||
    !websiteId ||
    !/^[\da-f]{8}-(?:[\da-f]{4}-){3}[\da-f]{12}$/.test(websiteId)
  )
    return null
  try {
    const url = new URL(scriptUrl)
    if (
      !['http:', 'https:'].includes(url.protocol) ||
      url.username ||
      url.password ||
      url.search ||
      url.hash
    )
      return null
    return { scriptUrl: url.toString(), websiteId }
  } catch {
    return null
  }
}
