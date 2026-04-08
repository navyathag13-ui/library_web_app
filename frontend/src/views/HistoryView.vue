<script setup lang="ts">
/**
 * HistoryView — new in final version (not in ResourceHub).
 * Shows all loan records with search + status filter + pagination.
 */
import { onMounted, watch } from 'vue'
import { useLoanStore }     from '../stores/loans'
import LoanStatusBadge      from '../components/LoanStatusBadge.vue'
import EmptyState           from '../components/EmptyState.vue'

const store = useLoanStore()

onMounted(() => store.fetchLoans())

watch(() => ({ ...store.filters }), () => store.fetchLoans(true), { deep: true })

const headers = [
  { title: 'Resource',      key: 'resourceTitle', sortable: false },
  { title: 'Borrower',      key: 'borrowerName',  sortable: false },
  { title: 'Checked Out',   key: 'checkoutDate',  sortable: false },
  { title: 'Due Date',      key: 'dueDate',        sortable: false },
  { title: 'Returned',      key: 'returnDate',     sortable: false },
  { title: 'Status',        key: 'status',         sortable: false },
]

const statusOpts = [
  { title: 'All statuses', value: '' },
  { title: 'Active',       value: 'active'   },
  { title: 'Returned',     value: 'returned' },
  { title: 'Overdue',      value: 'overdue'  },
]

function fmt(iso: string | null) {
  if (!iso) return '—'
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(iso))
}
</script>

<template>
  <div>

    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-h5 font-weight-bold mb-1">Loan History</h1>
      <p class="text-body-2 text-medium-emphasis">
        Full checkout and return record. {{ store.total ? `${store.total} loans total.` : '' }}
      </p>
    </div>

    <!-- Filters -->
    <v-card rounded="lg" elevation="1" class="pa-4 mb-4">
      <v-row dense align="center">
        <v-col cols="12" sm="5" md="4">
          <v-text-field
            :model-value="store.filters.search"
            prepend-inner-icon="mdi-magnify"
            label="Search resource or borrower"
            variant="outlined" density="compact" clearable hide-details
            @update:model-value="store.setFilter('search', $event ?? '')"
            aria-label="Search loan history"
          />
        </v-col>
        <v-col cols="6" sm="3" md="2">
          <v-select
            :model-value="store.filters.status"
            :items="statusOpts" item-title="title" item-value="value"
            label="Status" variant="outlined" density="compact" hide-details
            @update:model-value="store.setFilter('status', $event)"
            aria-label="Filter by loan status"
          />
        </v-col>
        <v-col cols="auto">
          <v-btn variant="text" size="small"
            @click="store.setFilter('search', ''); store.setFilter('status', '')">Clear</v-btn>
        </v-col>
      </v-row>
    </v-card>

    <!-- Table -->
    <v-data-table
      :headers="headers"
      :items="store.loans"
      :loading="store.loading"
      item-value="id"
      hover
      rounded="lg"
      class="elevation-1"
      :items-per-page="-1"
      hide-default-footer
      aria-label="Loan history table"
    >
      <template #loading>
        <v-skeleton-loader v-for="i in 5" :key="i" type="table-row" />
      </template>

      <template #item.checkoutDate="{ item }">
        <span class="text-body-2">{{ fmt(item.checkoutDate) }}</span>
      </template>

      <template #item.dueDate="{ item }">
        <span
          class="text-body-2"
          :class="item.isOverdue && item.status !== 'returned' ? 'text-error font-weight-bold' : ''"
        >{{ fmt(item.dueDate) }}</span>
      </template>

      <template #item.returnDate="{ item }">
        <span class="text-body-2">{{ fmt(item.returnDate) }}</span>
      </template>

      <template #item.status="{ item }">
        <LoanStatusBadge :status="item.status" :is-overdue="item.isOverdue" />
      </template>

      <template #no-data>
        <EmptyState
          title="No loans found"
          message="Loan records will appear here once resources are checked out."
          icon="mdi-book-clock-outline"
        />
      </template>
    </v-data-table>

    <!-- Pagination -->
    <div v-if="store.pages > 1" class="d-flex justify-center mt-4">
      <v-pagination
        :model-value="store.page"
        :length="store.pages"
        :total-visible="7"
        @update:model-value="store.setPage($event)"
        aria-label="Loan history pagination"
      />
    </div>

  </div>
</template>
