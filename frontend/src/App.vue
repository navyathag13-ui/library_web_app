<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute }   from 'vue-router'
import { useUiStore } from './stores/ui'
import AppSnackbar    from './components/AppSnackbar.vue'

const ui    = useUiStore()
const route = useRoute()

const drawer    = ref(true)
const pageTitle = ref('Dashboard')
watch(() => route.meta.title, v => { pageTitle.value = String(v ?? 'Dashboard') }, { immediate: true })

const navItems = [
  { title: 'Dashboard',    icon: 'mdi-view-dashboard-outline', to: '/dashboard' },
  { title: 'Resources',    icon: 'mdi-bookshelf',               to: '/resources'  },
  { title: 'Loan History', icon: 'mdi-history',                 to: '/history'    },
]
</script>

<template>
  <v-app>

    <!-- Navigation drawer -->
    <v-navigation-drawer v-model="drawer" permanent>
      <v-list-item
        prepend-icon="mdi-library-outline"
        title="LibraryHub"
        subtitle="Circulation Tracker"
        nav class="py-4"
      />
      <v-divider />
      <v-list density="compact" nav class="mt-2">
        <v-list-item
          v-for="item in navItems"
          :key="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          :to="item.to"
          rounded="lg"
          active-color="primary"
        />
      </v-list>
    </v-navigation-drawer>

    <!-- Top bar -->
    <v-app-bar elevation="0" border="b">
      <v-app-bar-nav-icon @click="drawer = !drawer" aria-label="Toggle navigation" />
      <v-app-bar-title class="font-weight-semibold">{{ pageTitle }}</v-app-bar-title>
    </v-app-bar>

    <!-- Page content -->
    <v-main>
      <v-container fluid class="pa-6" style="background: rgb(var(--v-theme-background)); min-height: 100%">
        <RouterView />
      </v-container>
    </v-main>

    <!-- Global toast — reads from ui store -->
    <AppSnackbar />

  </v-app>
</template>
