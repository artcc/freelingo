const { createHash } = require('node:crypto')
const fs = require('node:fs')
const path = require('node:path')

// Temporary lifecycle fix for the exact versions in package-lock.json.
// Review/remove this patch when upgrading VAD; unknown package contents fail closed.
const patches = [
  {
    name: '@ricky0123/vad-web',
    version: '0.0.30',
    file: 'dist/real-time-vad.js',
    sha256: 'dd0cfc58e977e4616eeccf9cc5c24c896b8f0601ea4537c5105771102c9362ce',
    changes: [
      [
        '        this.start = async () => {',
        '        const start = async () => {',
      ],
      [
        '                    if (this.options.audioContext) {',
        `                    if (this._freelingoDestroyRequested) return;
                    if (this.options.audioContext) {`,
      ],
      [
        '                    this._mediaStreamAudioSourceNode = new MediaStreamAudioSourceNode(this._audioContext, {',
        `                    if (this._freelingoDestroyRequested) return;
                    this._mediaStreamAudioSourceNode = new MediaStreamAudioSourceNode(this._audioContext, {`,
      ],
      [
        '                    this._stream = await this.options.resumeStream(stream);',
        `                    this._stream = await this.options.resumeStream(stream);
                    if (this._freelingoDestroyRequested) return;`,
      ],
      [
        '        this.pause = async () => {',
        `        this.start = () => {
            if (this._freelingoDestroyRequested) return Promise.resolve();
            if (!this._freelingoStartPromise) {
                this._freelingoStartPromise = start().finally(() => {
                    this._freelingoStartPromise = null;
                });
            }
            return this._freelingoStartPromise;
        };
        this.pause = async () => {`,
      ],
      [
        `        this.destroy = async () => {
            logging_1.log.debug("destroy called");
            this.initializationState = "destroyed";
            const { vadNode } = this.getAudioInstances();
            if (vadNode instanceof AudioWorkletNode) {
                vadNode.port.postMessage(messages_1.Message.SpeechStop);
            }
            if (this.listening) {
                await this.pause();
            }
            await this.model.release();
            if (this.ownsAudioContext) {
                await this._audioContext?.close();
            }
        };`,
        `        this.destroy = () => {
            if (!this._freelingoDestroyPromise) {
                this._freelingoDestroyRequested = true;
                this._freelingoDestroyPromise = (async () => {
                    // A pending start/resume must finish acquiring resources before disposal.
                    await this._freelingoStartPromise?.catch(() => {});
                    logging_1.log.debug("destroy called");
                    this.initializationState = "destroyed";
                    try {
                        const vadNode = this._vadNode;
                        if (typeof AudioWorkletNode !== "undefined" && vadNode instanceof AudioWorkletNode) {
                            vadNode.port.postMessage(messages_1.Message.SpeechStop);
                        }
                        if (this.listening) {
                            await this.pause();
                        }
                        else if (this._stream) {
                            await this.options.pauseStream(this._stream);
                        }
                    }
                    finally {
                        try {
                            this._vadNode?.disconnect();
                        }
                        finally {
                            try {
                                await this.model.release();
                            }
                            finally {
                                if (this.ownsAudioContext) {
                                    await this._audioContext?.close();
                                }
                            }
                        }
                    }
                })();
            }
            return this._freelingoDestroyPromise;
        };`,
      ],
    ],
  },
  {
    name: '@ricky0123/vad-react',
    version: '0.0.36',
    file: 'dist/index.js',
    sha256: '3b0ce7cac5430f97c0dec4a341c7f9ef7d32f505e70a224db2ebed0562e3d133',
    changes: [
      [
        `                    await myvad.start();
                    setListening(true);`,
        `                    await myvad.start();
                    if (canceled) return;
                    setListening(true);`,
      ],
      [
        `            catch (e) {
                setLoading(false);`,
        `            catch (e) {
                if (canceled) return;
                setLoading(false);`,
      ],
      [
        '                void myvad.destroy();',
        `                void myvad.destroy().catch((error) => {
                    console.error("Failed to destroy MicVAD", error);
                });`,
      ],
    ],
  },
]

function patchInstalledVad(root = path.resolve(__dirname, '..')) {
  // Validate both packages before writing either one. Reversing known changes
  // allows repeated installs while still rejecting unrelated edits or upgrades.
  const prepared = patches.map((patch) => {
    const directory = path.join(root, 'node_modules', patch.name)
    const { version } = JSON.parse(fs.readFileSync(path.join(directory, 'package.json'), 'utf8'))
    if (version !== patch.version) {
      throw new Error(`[patch-vad] Review required: ${patch.name}@${version}, expected ${patch.version}`)
    }
    const file = path.join(directory, patch.file)
    const current = fs.readFileSync(file, 'utf8')
    let original = current
    for (const [before, after] of [...patch.changes].reverse()) {
      original = original.replace(after, before)
    }
    if (createHash('sha256').update(original).digest('hex') !== patch.sha256) {
      throw new Error(`[patch-vad] Review required: unexpected contents in ${patch.name}/${patch.file}`)
    }
    let updated = original
    for (const [before, after] of patch.changes) {
      if (updated.split(before).length !== 2) {
        throw new Error(`[patch-vad] Patch target is not unique in ${patch.name}/${patch.file}`)
      }
      updated = updated.replace(before, after)
    }
    return { file, current, updated }
  })

  for (const { file, current, updated } of prepared) {
    if (current !== updated) fs.writeFileSync(file, updated)
  }
}

module.exports = { patchInstalledVad, patches }

if (require.main === module) {
  patchInstalledVad()
  console.log('[patch-vad] VAD lifecycle patch ready')
}
