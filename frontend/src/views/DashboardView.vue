<script setup lang="ts">
/**
 * DashboardView — enhanced from ResourceHub.
 * New: overdue count card, category breakdown bars, activity feed with loan details.
 */
import { onMounted, computed, ref } from 'vue'
import { useResourceStore } from '../stores/resources'
import { api }              from '../api'
import StatsCard            from '../components/StatsCard.vue'
import StatusBadge          from '../components/StatusBadge.vue'
import LoanStatusBadge      from '../components/LoanStatusBadge.vue'
import type { Loan }        from '../types'

const store    = useResourceStore()
const activity = ref<Loan[]>([])
const actLoad  = ref(true)

onMounted(async () => {
  await Promise.all([
    store.fetchResources(),
    store.fetchResources().then(() => {}),  // warms cache
    api.getStats().then(s => { store.fetchResources() }),
  ])
  // fetch stats separately so cards show immediately
  const [, actRes] = await Promise.all([
    api.getStats(),
    api.getActivity(),
  ])
  activity.value = actRes.activity
  actLoad.value  = false
})

// Re-fetch stats after any resource/loan change
const stats = ref<{ total: number; available: number; checkedOut: number; overdue: number; categories: { name: string; count: number }[] } | null>(null)
onMounted(async () => {
  stats.value = await api.getStats()
  actLoad.value = false
})

const statCards = computed(() => [
  { label: 'Total Resources', value: stats.value?.total      ?? 0, icon: 'mdi-bookshelf',            color: 'primary' },
  { label: 'Available',       value: stats.value?.available  ?? 0, icon: 'mdi-check-circle-outline', color: 'success' },
  { label: 'Checked Out',     value: stats.value?.checkedOut ?? 0, icon: 'mdi-clock-outline',         color: 'warning' },
  { label: 'Overdue',         value: stats.value?.overdue    ?? 0, icon: 'mdi-alert-circle-outline',  color: 'error'   },
])

const maxCategory = computed(() =>
  Math.max(1, ...( stats.value?.categories.map(c => c.count) ?? [1] ))
)

function fmtDate(iso: string) {
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric' }).format(new Date(iso))
}
function fmtTime(iso: string) {
  return new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: '2-digit' }).format(new Date(iso))
}
</script>

<template>
  <div>

    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-h5 font-weight-bold mb-1">Dashboard</h1>
      <p class="text-body-2 text-medium-emphasis">Real-time overview of library circulation.</p>
    </div>

    <!-- Stat cards -->
    <v-row class="mb-6">
      <v-col v-for="card in statCards" :key="card.label" cols="6" sm="3">
        <StatsCard v-bind="card" :loading="!stats" />
      </v-col>
    </v-row>

    <v-row>

      <!-- Category breakdown -->
      <v-col cols="12" md="4">
        <v-card rounded="lg" elevation="1" height="100%">
          <v-card-title class="pt-4 px-5 text-body-1 font-weight-semibold">
            <v-icon icon="mdi-tag-multiple-outline" class="mr-2" size="18" />By Category
          </v-card-title>
          <v-divider />
          <v-card-text v-if="stats" class="pa-4">
            <div v-for="cat in stats.categories" :key="cat.name" class="mb-3">
              <div class="d-flex justify-space-between text-body-2 mb-1">
                <span>{{ cat.name }}</span>
                <span class="font-weight-medium">{{ cat.count }}</span>
              </div>
              <v-progress-linear
                :model-value="(cat.count / maxCategory) * 100"
                color="primary" rounded height="6" bg-color="grey-lighten-3"
                :aria-label="`${cat.name}: ${cat.count}`"
              />
            </div>
            <div v-if="!stats.categories.length" class="text-center text-body-2 text-disabled py-4">
              No categories yet
            </div>
          </v-card-text>
          <div v-else class="pa-4">
            <v-skeleton-loader v-for="i in 4" :key="i" type="text" class="mb-3" />
          </div>
        </v-card>
      </v-col>

      <!-- Activity feed -->
      <v-col cols="12" md="8">
        <v-card rounded="lg" elevation="1">
          <v-card-title class="pt-4 px-5 text-body-1 font-weight-semibold d-flex align-center">
            <v-icon icon="mdi-history" class="mr-2" size="18" />Recent Loan Activity
          </v-card-title>
          <v-divider />

          <v-list v-if="!actLoad" density="compact" lines="two">
            <v-list-item
              v-for="loan in activity"
              :key="loan.id"
            >
              <template #prepend>
                <v-avatar
                  :color="loan.status === 'returned' ? 'success' : loan.isOverdue ? 'error' : 'primary'"
                  variant="tonal" size="36"
                >
                  <v-icon
                    :icon="loan.status === 'returned' ? 'mdi-arrow-left-circle-outline' : 'mdi-arrow-right-circle-outline'"
                    size="18"
                  />
                </v-avatar>
              </template>

              <template #title>
                <span class="text-body-2 font-weight-medium">{{ loan.resourceTitle }}</span>
              </template>
              <template #subtitle>
                <span class="text-caption text-medium-emphasis">
                  {{ loan.borrowerName }} ·
                  {{ loan.status === 'returned' ? 'Returned' : 'Checked out' }}
                  {{ fmtDate(loan.checkoutDate) }} at {{ fmtTime(loan.checkoutDate) }}
                </span>
              </template>

              <template #append>
                <LoanStatusBadge :status="loan.status" :is-overdue="loan.isOverdue" />
              </template>
            </v-list-item>

            <v-list-item v-if="!activity.length">
              <template #title>
                <span class="text-body-2 text-disabled">No loan activity yet</span>
              </template>
            </v-list-item>
          </v-list>

          <div v-else class="pa-4">
            <v-skeleton-loader v-for="i in 5" :key="i" type="list-item-two-line" class="mb-1" />
          </div>
        </v-card>
      </v-col>

    </v-row>
  </div>
</template>
