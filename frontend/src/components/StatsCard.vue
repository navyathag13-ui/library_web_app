<script setup lang="ts">
defineProps<{
  label:    string
  value:    number | string
  icon:     string
  color:    string
  loading?: boolean
}>()
</script>

<template>
  <v-card rounded="lg" elevation="1" height="120">
    <v-card-text class="pa-5 fill-height">
      <div class="d-flex align-center justify-space-between fill-height">
        <div>
          <div class="text-body-2 text-medium-emphasis mb-2">{{ label }}</div>
          <v-skeleton-loader v-if="loading" type="text" width="64" />
          <div
            v-else
            class="text-h4 font-weight-bold"
            :style="{ color: `rgb(var(--v-theme-${color}))` }"
            :aria-label="`${label}: ${value}`"
          >{{ value }}</div>
        </div>
        <v-avatar :color="color" variant="tonal" size="52">
          <v-icon :icon="icon" size="26" aria-hidden="true" />
        </v-avatar>
      </div>
    </v-card-text>
  </v-card>
</template>
