<script setup lang="ts">
withDefaults(defineProps<{
  title?:   string
  message?: string
  icon?:    string
}>(), {
  title:   'Nothing here yet',
  message: 'Add a resource to get started.',
  icon:    'mdi-tray-remove',
})
</script>

<template>
  <div class="d-flex flex-column align-center justify-center py-16 text-center" role="status" :aria-label="title">
    <v-avatar color="grey-lighten-3" size="80" class="mb-4">
      <v-icon :icon="icon" size="40" color="grey" />
    </v-avatar>
    <div class="text-h6 font-weight-medium text-medium-emphasis mb-1">{{ title }}</div>
    <div class="text-body-2 text-disabled">{{ message }}</div>
  </div>
</template>
