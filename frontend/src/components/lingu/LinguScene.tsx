'use client'

import { useEffect, useRef, useState } from 'react'
import Image from 'next/image'
import {
  AnimationMixer,
  Box3,
  DirectionalLight,
  HemisphereLight,
  Mesh,
  NeutralToneMapping,
  OrthographicCamera,
  Scene,
  Vector3,
  WebGLRenderer,
  type Object3D,
} from 'three'
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js'
import { createLinguPlayback } from '@/lib/lingu-playback'
import type { LinguAnimation, LinguSceneProps } from './LinguAvatar'

function disposeModel(model: Object3D) {
  model.traverse((object) => {
    if (object instanceof Mesh) {
      object.geometry.dispose()
      const materials = Array.isArray(object.material)
        ? object.material
        : [object.material]
      materials.forEach((material) => material.dispose())
    }
  })
}

export default function LinguScene({
  animation,
  loop,
  onFinished,
  onReady,
  onError,
}: LinguSceneProps) {
  const hostRef = useRef<HTMLDivElement>(null)
  const controlRef = useRef<
    ((name: LinguAnimation, loop?: boolean) => void) | null
  >(null)
  const callbacks = useRef({ animation, loop, onFinished, onReady, onError })
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    callbacks.current = { animation, loop, onFinished, onReady, onError }
    controlRef.current?.(animation, loop)
  }, [animation, loop, onFinished, onReady, onError])

  useEffect(() => {
    const host = hostRef.current
    if (!host) return
    const controller = new AbortController()
    let renderer: WebGLRenderer | undefined
    let model: Object3D | undefined
    let mixer: AnimationMixer | undefined
    let observer: ResizeObserver | undefined
    let frame = 0
    let disposed = false

    const contextLost = (event: Event) => {
      event.preventDefault()
      cancelAnimationFrame(frame)
      callbacks.current.onError()
    }

    async function load() {
      try {
        renderer = new WebGLRenderer({
          alpha: true,
          antialias: true,
          powerPreference: 'low-power',
        })
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5))
        renderer.setClearColor(0, 0)
        renderer.toneMapping = NeutralToneMapping
        renderer.toneMappingExposure = 1.0
        renderer.domElement.addEventListener('webglcontextlost', contextLost)
        host!.appendChild(renderer.domElement)

        const response = await fetch('/models/lingu.glb', {
          signal: controller.signal,
        })
        if (!response.ok) throw new Error('Lingu model unavailable')
        const data = await response.arrayBuffer()
        if (disposed) return
        const gltf = await new GLTFLoader().parseAsync(data, '')
        if (disposed) {
          disposeModel(gltf.scene)
          return
        }
        model = gltf.scene
        const scene = new Scene()
        scene.add(model)
        // Keep studio-style contrast without washing out Lingu's green enamel.
        scene.add(new HemisphereLight(0xffffff, 0x527080, 0.45))
        const key = new DirectionalLight(0xffffff, 1.8)
        key.position.set(5, 12, 10)
        scene.add(key)
        const fill = new DirectionalLight(0xc5e4ff, 0.45)
        fill.position.set(-6, 7, 4)
        scene.add(fill)
        mixer = new AnimationMixer(model)
        const actions = new Map(
          gltf.animations.map((clip) => [clip.name, mixer!.clipAction(clip)])
        )

        // Frame the union of sampled poses, so waving and jumping stay in view.
        const bounds = new Box3().setFromObject(model)
        for (const clip of gltf.animations) {
          const action = actions.get(clip.name)!
          action.play()
          for (let sample = 0; sample <= 8; sample++) {
            mixer.setTime((clip.duration * sample) / 8)
            model.updateMatrixWorld(true)
            bounds.union(new Box3().setFromObject(model))
          }
          mixer.stopAllAction()
        }
        mixer.setTime(0)
        const center = bounds.getCenter(new Vector3())
        const size = bounds.getSize(new Vector3())
        const camera = new OrthographicCamera(-1, 1, 1, -1, 0.1, 100)
        camera.position.set(center.x, center.y, bounds.max.z + 25)
        camera.lookAt(center)

        const resize = () => {
          if (!renderer || disposed) return
          const width = host!.clientWidth || 180
          const height = host!.clientHeight || 180
          const aspect = width / height
          const halfHeight = Math.max(size.y, size.x / aspect) * 0.55
          camera.left = -halfHeight * aspect
          camera.right = halfHeight * aspect
          camera.top = halfHeight
          camera.bottom = -halfHeight
          camera.updateProjectionMatrix()
          renderer.setSize(width, height)
        }
        observer = new ResizeObserver(resize)
        observer.observe(host!)
        resize()

        const playback = createLinguPlayback(actions)
        controlRef.current = playback.play
        mixer.addEventListener('finished', (event) => {
          if (playback.isActive(event.action)) callbacks.current.onFinished?.()
        })
        controlRef.current(callbacks.current.animation, callbacks.current.loop)

        let lastTime = performance.now()
        let ready = false
        const render = (now: number) => {
          if (disposed) return
          const delta = Math.min((now - lastTime) / 1000, 0.05)
          lastTime = now
          if (!document.hidden) {
            playback.update(delta)
            mixer!.update(delta)
            renderer!.render(scene, camera)
            if (!ready) {
              ready = true
              setLoaded(true)
              callbacks.current.onReady?.()
            }
          }
          frame = requestAnimationFrame(render)
        }
        frame = requestAnimationFrame(render)
      } catch {
        if (!disposed) callbacks.current.onError()
      }
    }
    void load()
    return () => {
      disposed = true
      controller.abort()
      controlRef.current = null
      cancelAnimationFrame(frame)
      observer?.disconnect()
      mixer?.stopAllAction()
      if (model) {
        mixer?.uncacheRoot(model)
        disposeModel(model)
      }
      if (renderer) {
        renderer.domElement.removeEventListener('webglcontextlost', contextLost)
        renderer.dispose()
        renderer.forceContextLoss()
        renderer.domElement.remove()
      }
    }
  }, [])

  return (
    <>
      {!loaded && (
        <Image
          src="/logo.png"
          alt=""
          fill
          sizes="280px"
          className="object-contain p-2"
        />
      )}
      <div
        ref={hostRef}
        className={`absolute inset-0 ${loaded ? '' : 'invisible'}`}
      />
    </>
  )
}
