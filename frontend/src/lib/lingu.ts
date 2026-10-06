/** Playback defaults from blender/lingu.animations.json. */
export const LINGU_ANIMATIONS = {
  reposo: 'repeat',
  saludo: 'once',
  pensando: 'repeat',
  hablando: 'repeat',
  celebracion: 'once',
  escuchando: 'repeat',
  acierto: 'once',
  animando: 'once',
  explicando_l: 'once',
  explicando_r: 'once',
  tu_turno: 'once',
  despedida: 'once',
  six_seven: 'once',
} as const

export type LinguAnimation = keyof typeof LINGU_ANIMATIONS
