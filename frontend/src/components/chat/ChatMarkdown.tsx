import type { Element } from 'hast'
import type { ReactNode } from 'react'
import Markdown, { type Components, type Options } from 'react-markdown'
import { remarkChatImageText } from './remark-chat-image-text'

const remarkRehypeOptions: Options['remarkRehypeOptions'] = {
  handlers: {
    break(state, node) {
      // The default handler also adds a newline, which pre-line renders a second time.
      const element: Element = {
        type: 'element',
        tagName: 'br',
        properties: {},
        children: [],
      }
      state.patch(node, element)
      return state.applyData(node, element)
    },
  },
}

function Paragraph({ children }: { children?: ReactNode }) {
  return (
    <p className="my-2 whitespace-pre-line first:mt-0 last:mb-0">{children}</p>
  )
}

const components: Components = {
  p: Paragraph,
  ul: ({ children }) => (
    <ul className="my-2 list-disc space-y-1 pl-5 first:mt-0 last:mb-0">
      {children}
    </ul>
  ),
  ol: ({ children, start }) => (
    <ol
      start={start}
      className="my-2 list-decimal space-y-1 pl-5 first:mt-0 last:mb-0"
    >
      {children}
    </ol>
  ),
  // Unsupported presentation retains readable content, never interactive elements.
  h1: Paragraph,
  h2: Paragraph,
  h3: Paragraph,
  h4: Paragraph,
  h5: Paragraph,
  h6: Paragraph,
  pre: Paragraph,
  code: ({ children }) => <>{children}</>,
  img: ({ alt }) => <span className="whitespace-pre-line">{alt}</span>,
}

const allowedElements = ['strong', 'em', 'li', 'br', ...Object.keys(components)]

export function ChatMarkdown({ children }: { children: string }) {
  return (
    <Markdown
      remarkPlugins={[remarkChatImageText]}
      remarkRehypeOptions={remarkRehypeOptions}
      components={components}
      allowedElements={allowedElements}
      unwrapDisallowed
      skipHtml
    >
      {children}
    </Markdown>
  )
}
