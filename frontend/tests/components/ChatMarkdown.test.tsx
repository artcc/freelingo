import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { ChatMarkdown } from '@/components/chat/ChatMarkdown'
import { TargetLanguageText } from '@/components/TargetLanguageText'

describe('ChatMarkdown', () => {
  it('renders emphasis, paragraphs and both list types', () => {
    const { container } = render(
      <ChatMarkdown>
        {
          'Use **went**, not *goed*.\n\nExamples:\n\n- I went home.\n- She went shopping.\n\n3. ***Your turn***\n4. Try again'
        }
      </ChatMarkdown>
    )

    expect(screen.getByText('went').tagName).toBe('STRONG')
    expect(screen.getByText('goed').tagName).toBe('EM')
    expect(container.querySelectorAll('ul > li')).toHaveLength(2)
    expect(container.querySelectorAll('ol > li')).toHaveLength(2)
    expect(container.querySelector('ol')).toHaveAttribute('start', '3')
    expect(container.querySelector('ol strong')).toHaveTextContent('Your turn')
    expect(container.querySelector('ol em')).toHaveTextContent('Your turn')
    expect(screen.getByText('Examples:').tagName).toBe('P')
  })

  it('preserves plain text, escaped punctuation and line breaks', () => {
    const text = '2026, 3.14, -5 and 2 * 3; well-known, user_name.'
    const { container } = render(
      <ChatMarkdown>{`${text}\n\nLiteral \\*word\\*.  \nNext line.`}</ChatMarkdown>
    )

    expect(screen.getByText(text)).toBeInTheDocument()
    expect(container).toHaveTextContent('Literal *word*.')
    expect(container.querySelector('br')).not.toBeNull()
    expect(container.querySelector('em')).toBeNull()
  })

  describe.each(['  \n', '\\\n'])('hard break %j', (hardBreak) => {
    it.each([
      ['paragraph', '', '', 'p'],
      ['compact unordered list', '- ', '  ', 'li'],
      ['compact ordered list', '1. ', '   ', 'li'],
    ])(
      'renders one break in a %s and retains soft breaks',
      (_, prefix, indent, selector) => {
        const { container } = render(
          <ChatMarkdown>
            {`${prefix}First${hardBreak}${indent}Second\n${indent}Third`}
          </ChatMarkdown>
        )
        const content = container.querySelector(selector)!
        const br = content.querySelector('br')!

        expect(content.childNodes).toHaveLength(3)
        expect(content.querySelectorAll('br')).toHaveLength(1)
        expect(br.previousSibling?.textContent).toBe('First')
        expect(br.nextSibling?.textContent).toBe('Second\nThird')
        if (selector === 'li') expect(content.querySelector('p')).toBeNull()
      }
    )

    it('handles hard breaks inside emphasis without adding whitespace', () => {
      const { container } = render(
        <ChatMarkdown>{`**First${hardBreak}Second**`}</ChatMarkdown>
      )
      const emphasis = container.querySelector('strong')!

      expect(emphasis.childNodes).toHaveLength(3)
      expect(emphasis.querySelectorAll('br')).toHaveLength(1)
      expect(emphasis.querySelector('br')?.nextSibling?.textContent).toBe(
        'Second'
      )
    })
  })

  it('keeps soft line breaks as text without inserting br elements', () => {
    const { container } = render(<ChatMarkdown>{'First\nSecond'}</ChatMarkdown>)

    expect(container.querySelector('p')?.textContent).toBe('First\nSecond')
    expect(container.querySelector('br')).toBeNull()
  })

  it('keeps unsupported content readable without HTML, links or image requests', () => {
    const { container } = render(
      <ChatMarkdown>
        {
          '# Heading\n\n> A [link](javascript:alert%281%29).\n\n![description](https://example.com/image.png)\n\n`went`\n\n```text\nI went home.\n```\n\n<script>alert("hidden")</script>'
        }
      </ChatMarkdown>
    )

    for (const text of [
      'Heading',
      'link',
      'description',
      'went',
      'I went home.',
    ]) {
      expect(container).toHaveTextContent(text)
    }
    expect(
      container.querySelector('a, img, script, h1, blockquote, code, pre')
    ).toBeNull()
    expect(container).not.toHaveTextContent('hidden')
  })

  it('accepts unfinished emphasis and replaces it when the stream completes', () => {
    const { container, rerender } = render(
      <ChatMarkdown>{'Use **we'}</ChatMarkdown>
    )
    expect(container).toHaveTextContent('Use **we')

    rerender(<ChatMarkdown>{'Use **went**.'}</ChatMarkdown>)
    expect(screen.getByText('went').tagName).toBe('STRONG')
    expect(container).not.toHaveTextContent('**')
  })

  describe.each(['inline', 'reference'])('%s image descriptions', (kind) => {
    it.each(['- ', '1. '])(
      'preserves multiline descriptions in compact lists starting with %j',
      (prefix) => {
        const indent = ' '.repeat(prefix.length)
        const label = `first\\\n${indent}second`
        const markdown =
          kind === 'inline'
            ? `${prefix}![${label}](https://example.com/image.png)`
            : `${prefix}![${label}][ref]\n\n[ref]: https://example.com/image.png`
        const { container } = render(<ChatMarkdown>{markdown}</ChatMarkdown>)
        const item = container.querySelector('li')!
        const description = item.querySelector('span')!

        expect(item.querySelector('p')).toBeNull()
        expect(description.textContent).toBe('first\nsecond')
        expect(description).toHaveClass('whitespace-pre-line')
        expect(item.querySelector('img, br')).toBeNull()
      }
    )

    it.each([
      ['caf&#233;', 'café'],
      ['&#50; cats', '2 cats'],
      ['caf&#xE9; &amp; tea', 'café & tea'],
      ['\\*cats\\* and \\_dogs\\_', '*cats* and _dogs_'],
      ['**caf&#233;**', 'café'],
      ['first\\\nsecond', 'first\nsecond'],
      ['first  \nsecond', 'first\nsecond'],
      ['first\nsecond', 'first\nsecond'],
      ['a <b>word</b>', 'a word'],
      ['`<b>word</b>`', '<b>word</b>'],
      ['a \\<b>word\\</b>', 'a <b>word</b>'],
      [
        'outer ![first\\\nsecond](https://example.com/nested.png)',
        'outer first\nsecond',
      ],
    ])('preserves image description %s as text', (label, expected) => {
      const markdown =
        kind === 'inline'
          ? `![${label}](https://example.com/image.png)`
          : `![${label}][ref]\n\n[ref]: https://example.com/image.png`
      const { container } = render(<ChatMarkdown>{markdown}</ChatMarkdown>)

      expect(container.textContent).toBe(expected)
      expect(container.querySelector('img, b')).toBeNull()
    })
  })

  it.each([
    'https://example.com',
    'javascript:alert%281%29',
    'file:///private/example',
    'data:text/plain,hello',
  ])('discards destinations for %s while preserving labels', (destination) => {
    const { container } = render(
      <ChatMarkdown>
        {`Read [**this**](${destination}).\n\nRead [**this**][ref].\n\nRead ![**this**](${destination}).\n\n[ref]: ${destination}`}
      </ChatMarkdown>
    )

    expect(container.textContent).toBe('Read this.\nRead this.\nRead this.')
    expect(container.querySelector('a, img')).toBeNull()
  })

  it.each([
    'https://example.com/%32%30%32%36',
    'https://xn--caf-dma.example/%C3%A9',
    'file:///example/%32%30%32%36',
    'hello@xn--caf-dma.example',
  ])('preserves autolink label %s verbatim', (label) => {
    const { container } = render(
      <ChatMarkdown>{`Read <${label}>.`}</ChatMarkdown>
    )

    expect(container.textContent).toBe(`Read ${label}.`)
    expect(container.querySelector('a')).toBeNull()
  })

  it.each([
    ['ja-JP', 'font-target-ja'],
    ['ko-KR', 'font-target-ko'],
    ['zh-CN', 'font-target-zh'],
  ])('inherits the learned-language presentation for %s', (language, font) => {
    const { container } = render(
      <TargetLanguageText as="div" languageCode={language}>
        <ChatMarkdown>{'**例**\n\n- 例'}</ChatMarkdown>
      </TargetLanguageText>
    )

    expect(container.firstElementChild).toHaveAttribute('lang', language)
    expect(container.firstElementChild).toHaveClass(font)
    expect(container.querySelector('strong')).toHaveTextContent('例')
    expect(container.querySelector('li')).toHaveTextContent('例')
  })
})
