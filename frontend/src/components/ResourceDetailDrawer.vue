<script setup lang="ts">
/**
 * ResourceDetailDrawer — right-side navigation drawer showing full resource info + loan history.
 * New in final version (was not in ResourceHub).
 */
import { computed } from 'vue'
import type { Resource } from '../types'
import StatusBadge     from './StatusBadge.vue'
import LoanStatusBadge from './LoanStatusBadge.vue'

const props = defineProps<{
  modelValue: boolean
  resource:   Resource | null
}>()

const emit = defineEmits<{
  'update:modelValue': [v: boolean]
  'checkout': [id: number]
  'return':   [id: number]
  'edit':     [resource: Resource]
}>()

function fmt(iso: string | null) {
  if (!iso) return '—'
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(iso))
}

const loanHeaders = [
  { title: 'Borrower',      key: 'borrowerName',  sortable: false },
  { title: 'Checked Out',   key: 'checkoutDate',  sortable: false },
  { title: 'Due',           key: 'dueDate',        sortable: false },
  { title: 'Returned',      key: 'returnDate',     sortable: false },
  { title: 'Status',        key: 'status',         sortable: false },
]

const sortedLoans = computed(() =>
  [...(props.resource?.loans ?? [])].sort(
    (a, b) => new Date(b.checkoutDate).getTime() - new Date(a.checkoutDate).getTime()
  )
)
</script>

<template>
  <v-navigation-drawer
    :model-value="modelValue"
    location="right"
    width="480"
    temporary
    @update:model-value="emit('update:modelValue', $event)"
  >
    <template v-if="resource">
      <!-- Header -->
      <div class="pa-5 pb-3">
        <div class="d-flex align-start justify-space-between mb-3">
          <v-avatar color="primary" variant="tonal" size="48">
            <v-icon icon="mdi-book-open-outline" size="24" />
          </v-avatar>
          <v-btn icon="mdi-close" variant="text" size="small" @click="emit('update:modelValue', false)" aria-label="Close detail panel" />
        </div>
        <h2 class="text-h6 font-weight-bold mb-1">{{ resource.title }}</h2>
        <div class="text-body-2 text-medium-emphasis mb-3">{{ resource.author }}</div>
        <StatusBadge :status="resource.status" />
      </div>

      <v-divider />

      <!-- Details -->
      <v-list density="compact" class="pa-3">
        <v-list-item prepend-icon="mdi-tag-outline" :title="resource.category" subtitle="Category" />
        <v-list-item v-if="resource.isbn" prepend-icon="mdi-barcode" :title="resource.isbn" subtitle="ISBN" />
        <v-list-item prepend-icon="mdi-content-copy"
          :title="`${resource.availableCopies} of ${resource.totalCopies} available`"
          subtitle="Copies" />
        <v-list-item v-if="resource.description" prepend-icon="mdi-text-long" :title="resource.description" subtitle="Description" class="text-wrap" />
        <v-list-item prepend-icon="mdi-calendar-plus-outline" :title="fmt(resource.dateAdded)" subtitle="Date Added" />
      </v-list>

      <!-- Action buttons -->
      <div class="pa-4 d-flex gap-2">
        <v-btn
          v-if="resource.status === 'available'"
          color="primary" variant="tonal" prepend-icon="mdi-arrow-right-circle-outline"
          @click="emit('checkout', resource.id)" :aria-label="`Check out ${resource.title}`"
        >Check Out</v-btn>
        <v-btn
          v-else
          color="success" variant="tonal" prepend-icon="mdi-arrow-left-circle-outline"
          @click="emit('return', resource.id)" :aria-label="`Return ${resource.title}`"
        >Check In</v-btn>
        <v-btn
          variant="outlined" prepend-icon="mdi-pencil-outline"
          @click="emit('edit', resource)" :aria-label="`Edit ${resource.title}`"
        >Edit</v-btn>
      </div>

      <v-divider />

      <!-- Loan history -->
      <div class="pa-4">
        <h3 class="text-subtitle-1 font-weight-semibold mb-3">
          <v-icon icon="mdi-history" class="mr-1" size="18" />Loan History
        </h3>

        <div v-if="sortedLoans.length === 0" class="text-center py-6 text-medium-emphasis text-body-2">
          No loans recorded for this resource.
        </div>

        <v-data-table
          v-else
          :headers="loanHeaders"
          :items="sortedLoans"
          :items-per-page="5"
          density="compact"
          rounded="lg"
          class="elevation-0 border"
          aria-label="Loan history table"
        >
          <template #item.checkoutDate="{ item }">
            <span class="text-caption">{{ fmt(item.checkoutDate) }}</span>
          </template>
          <template #item.dueDate="{ item }">
            <span class="text-caption" :class="item.isOverdue && item.status !== 'returned' ? 'text-error font-weight-bold' : ''">
              {{ fmt(item.dueDate) }}
            </span>
          </template>
          <template #item.returnDate="{ item }">
            <span class="text-caption">{{ fmt(item.returnDate) }}</span>
          </template>
          <template #item.status="{ item }">
            <LoanStatusBadge :status="item.status" :is-overdue="item.isOverdue" />
          </template>
        </v-data-table>
      </div>
    </template>

    <!-- Loading state if resource not yet fetched -->
    <div v-else class="pa-6">
      <v-skeleton-loader type="article" />
    </div>
  </v-navigation-drawer>
</template>
