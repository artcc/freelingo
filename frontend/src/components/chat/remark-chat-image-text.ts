import type { PhrasingContent } from 'mdast'
import type { Extension } from 'mdast-util-from-markdown'
import type {} from 'remark-parse'
import type { Processor } from 'unified'

function descriptionText(node: PhrasingContent): string {
  if (node.type === 'break') return '\n'
  if (node.type === 'html') return ''
  if ('value' in node) return node.value
  if ('alt' in node) return node.alt ?? ''
  if ('children' in node) return node.children.map(descriptionText).join('')
  return ''
}

const imageTextExtension: Extension = {
  afterExit(token) {
    if (token.type !== 'labelText') return
    const image = this.stack.at(-2)
    const fragment = this.stack.at(-1)
    if (image?.type !== 'image' || fragment?.type !== 'fragment') return

    // Preserve breaks and omit HTML before the parser flattens this label into alt.
    // Keep its normal reference resolution and entity/escape decoding intact.
    fragment.children = [
      { type: 'text', value: fragment.children.map(descriptionText).join('') },
    ]
  },
}

export function remarkChatImageText(this: Processor) {
  const data = this.data()
  data.fromMarkdownExtensions = [
    ...(data.fromMarkdownExtensions ?? []),
    imageTextExtension,
  ]
}
