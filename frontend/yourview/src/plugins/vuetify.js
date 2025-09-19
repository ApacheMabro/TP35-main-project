// src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#3B82F6',   // brand primary (blue-500 vibe)
          secondary: '#10B981', // brand secondary (emerald-500)
          surface: '#FFFFFF',
          background: '#FAFAFA',
        },
      },
    },
  },
  icons: { defaultSet: 'mdi', aliases, sets: { mdi } },
})
