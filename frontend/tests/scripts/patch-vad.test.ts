import { createRequire } from 'node:module'
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import path from 'node:path'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'

const loadCjs = createRequire(import.meta.url)
const { patchInstalledVad, patches } = loadCjs(
  '../../scripts/patch-vad.js'
) as typeof import('../../scripts/patch-vad')
const frontend = path.dirname(loadCjs.resolve('../../package.json'))
let fixture: string

function packageFile(index: number, file = patches[index].file) {
  return path.join(fixture, 'node_modules', patches[index].name, file)
}

function contents() {
  return patches.map((_, index) => readFileSync(packageFile(index), 'utf8'))
}

beforeEach(() => {
  fixture = mkdtempSync(path.join(frontend, 'tests/scripts/.vad-patch-'))
  for (const [index, patch] of patches.entries()) {
    let original = readFileSync(
      path.join(frontend, 'node_modules', patch.name, patch.file),
      'utf8'
    )
    for (const [before, after] of [...patch.changes].reverse()) {
      original = original.replace(after, before)
    }
    mkdirSync(path.dirname(packageFile(index)), { recursive: true })
    writeFileSync(packageFile(index), original)
    writeFileSync(
      packageFile(index, 'package.json'),
      JSON.stringify({ name: patch.name, version: patch.version })
    )
  }
})

afterEach(() => {
  rmSync(fixture, { recursive: true, force: true })
})

describe('versioned VAD lifecycle patch installer', () => {
  it('patches a fresh installation and safely handles repeated installation', () => {
    const original = contents()
    patchInstalledVad(fixture)
    const patched = contents()
    for (const index of patches.keys()) {
      expect(patched[index]).not.toBe(original[index])
      for (const [, after] of patches[index].changes) {
        expect(patched[index]).toContain(after)
      }
    }

    patchInstalledVad(fixture)
    expect(contents()).toEqual(patched)
  })

  it('rejects an unexpected dependency version before modifying either package', () => {
    writeFileSync(packageFile(1, 'package.json'), JSON.stringify({ version: '0.0.37' }))
    const original = contents()

    expect(() => patchInstalledVad(fixture)).toThrow('expected 0.0.36')
    expect(contents()).toEqual(original)
  })

  it.each(['fresh', 'patched'] as const)(
    'rejects unexpected %s package contents without overwriting them',
    (state) => {
      if (state === 'patched') patchInstalledVad(fixture)
      writeFileSync(packageFile(1), `${readFileSync(packageFile(1), 'utf8')}\n// unexpected edit\n`)
      const original = contents()

      expect(() => patchInstalledVad(fixture)).toThrow('unexpected contents')
      expect(contents()).toEqual(original)
    }
  )

  it('completes an interrupted patch without duplicating changes', () => {
    patchInstalledVad(fixture)
    const patched = contents()
    const [before, after] = patches[0].changes[0]
    writeFileSync(packageFile(0), patched[0].replace(after, before))

    patchInstalledVad(fixture)
    expect(contents()).toEqual(patched)
  })
})
