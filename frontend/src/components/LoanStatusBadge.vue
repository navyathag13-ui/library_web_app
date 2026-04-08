<script setup lang="ts">
import { computed } from 'vue'
import type { LoanStatus } from '../types'

const props = defineProps<{ status: LoanStatus; isOverdue?: boolean }>()

const cfg = {
  active:   { color: 'info',    icon: 'mdi-arrow-right-circle-outline', label: 'Active'   },
  returned: { color: 'success', icon: 'mdi-check-circle-outline',       label: 'Returned' },
  overdue:  { color: 'error',   icon: 'mdi-alert-circle-outline',        label: 'Overdue'  },
} as const

const badge = computed(() => {
  // Active loans that have passed due date show as overdue even if backend hasn't synced yet
  if (props.status === 'active' && props.isOverdue) return cfg['overdue']
  return cfg[props.status] ?? cfg['active']
})
</script>

<template>
  <v-chip
    :color="badge.color"
    :prepend-icon="badge.icon"
    size="small"
    variant="tonal"
    class="font-weight-medium"
    :aria-label="`Loan status: ${badge.label}`"
    role="status"
  >
    {{ badge.label }}
  </v-chip>
</template>
