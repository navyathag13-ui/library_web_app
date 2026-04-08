import { createApp }    from 'vue'
import { createPinia }  from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { createVuetify } from 'vuetify'
import * as components   from 'vuetify/components'
import * as directives   from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App          from './App.vue'
import DashboardView from './views/DashboardView.vue'
import ResourcesView from './views/ResourcesView.vue'
import HistoryView   from './views/HistoryView.vue'

const vuetify = createVuetify({
  components,
  directives,
  icons: { defaultSet: 'mdi' },
  theme: {
    defaultTheme: 'libraryHubLight',
    themes: {
      libraryHubLight: {
        dark: false,
        colors: {
          primary:    '#1A237E',   // deep indigo — professional
          secondary:  '#0277BD',
          success:    '#2E7D32',
          warning:    '#E65100',
          error:      '#B71C1C',
          info:       '#0277BD',
          background: '#F5F6FA',
          surface:    '#FFFFFF',
        },
      },
    },
  },
})

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',          redirect: '/dashboard' },
    { path: '/dashboard', component: DashboardView, meta: { title: 'Dashboard' } },
    { path: '/resources', component: ResourcesView,  meta: { title: 'Resources' } },
    { path: '/history',   component: HistoryView,    meta: { title: 'Loan History' } },
  ],
})

router.afterEach(to => {
  document.title = `LibraryHub — ${String(to.meta.title ?? 'Dashboard')}`
})

createApp(App)
  .use(createPinia())
  .use(router)
  .use(vuetify)
  .mount('#app')
