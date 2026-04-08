<script setup lang="ts">
// Global snackbar driven by the UI Pinia store.
// Placed once in App.vue — accessible from any component via useUiStore().
import { useUiStore } from '../stores/ui'
const ui = useUiStore()
</script>

<template>
  <v-snackbar
    v-model="ui.show"
    :color="ui.color"
    :timeout="3500"
    location="bottom right"
    rounded="lg"
    elevation="4"
  >
    {{ ui.message }}
    <template #actions>
      <v-btn variant="text" @click="ui.hide" aria-label="Dismiss notification">Close</v-btn>
    </template>
  </v-snackbar>
</template>
