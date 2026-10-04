import {create} from 'zustand'
import {persist} from 'zustand/middleware'

export type Theme='system'|'dark'|'light'
interface ThemeStore{theme:Theme;setTheme:(theme:Theme)=>void}

export const useThemeStore=create<ThemeStore>()(persist((set)=>({
 theme:'light',
 setTheme:(theme)=>set({theme}),
}),{name:'fl-theme',skipHydration:true}))
