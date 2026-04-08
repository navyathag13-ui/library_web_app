<script setup lang="ts">
import { computed } from 'vue'
import type { ResourceStatus } from '../types'

const props = defineProps<{ status: ResourceStatus }>()

const cfg = {
  'available':   { color: 'success', icon: 'mdi-check-circle-outline', label: 'Available'   },
  'checked-out': { color: 'warning', icon: 'mdi-clock-outline',         label: 'Checked Out' },
} as const

const badge = computed(() => cfg[props.status] ?? cfg['available'])
</script>

<template>
  <v-chip
    :color="badge.color"
    :prepend-icon="badge.icon"
    size="small"
    variant="tonal"
    class="font-weight-medium"
    :aria-label="`Status: ${badge.label}`"
    role="status"
  >
    {{ badge.label }}
  </v-chip>
</template>
