<script setup lang="ts">
/**
 * ResourceTable — main data table for the Resources view.
 * New vs ResourceHub: Edit action, View (opens drawer), copy count column.
 */
import { ref } from 'vue'
import type { Resource } from '../types'
import StatusBadge   from './StatusBadge.vue'
import EmptyState    from './EmptyState.vue'
import ConfirmDialog from './ConfirmDialog.vue'

const props = defineProps<{
  resources:     Resource[]
  loading:       boolean
  actionLoading: number | null
}>()

const emit = defineEmits<{
  view:     [id: number]
  checkout: [id: number]
  return:   [id: number]
  edit:     [resource: Resource]
  remove:   [id: number]
}>()

// Confirm remove
const confirmOpen = ref(false)
const pendingId   = ref<number | null>(null)

function requestRemove(r: Resource) { pendingId.value = r.id; confirmOpen.value = true }
function handleConfirm() { if (pendingId.value) { emit('remove', pendingId.value) } confirmOpen.value = false }

const headers = [
  { title: 'Title',     key: 'title',           sortable: false },
  { title: 'Author',    key: 'author',           sortable: false },
  { title: 'Category',  key: 'category',         sortable: false },
  { title: 'Copies',    key: 'availableCopies',  sortable: false, align: 'center' as const },
  { title: 'Status',    key: 'status',           sortable: false },
  { title: 'Actions',   key: 'actions',          sortable: false, align: 'end' as const },
]

function fmt(iso: string | null) {
  if (!iso) return '—'
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(iso))
}
</script>

<template>
  <ConfirmDialog
    v-model="confirmOpen"
    title="Remove Resource"
    message="This resource and all its loan history will be permanently removed."
    confirm-label="Remove"
    @confirm="handleConfirm"
  />

  <v-data-table
    :headers="headers"
    :items="resources"
    :loading="loading"
    item-value="id"
    hover
    rounded="lg"
    class="elevation-1"
    :items-per-page="-1"
    hide-default-footer
    aria-label="Resources table"
  >
    <template #loading>
      <v-skeleton-loader v-for="i in 5" :key="i" type="table-row" />
    </template>

    <template #item.availableCopies="{ item }">
      <v-chip size="x-small" :color="item.availableCopies > 0 ? 'success' : 'error'" variant="tonal">
        {{ item.availableCopies }} / {{ item.totalCopies }}
      </v-chip>
    </template>

    <template #item.status="{ item }">
      <StatusBadge :status="item.status" />
    </template>

    <template #item.actions="{ item }">
      <div class="d-flex align-center justify-end gap-1">
        <!-- View detail -->
        <v-tooltip text="View details" location="top">
          <template #activator="{ props: tip }">
            <v-btn v-bind="tip" icon="mdi-eye-outline" size="small" variant="text"
              @click="emit('view', item.id)" :aria-label="`View ${item.title}`" />
          </template>
        </v-tooltip>

        <!-- Checkout -->
        <v-btn v-if="item.status === 'available'"
          size="small" variant="tonal" color="primary"
          prepend-icon="mdi-arrow-right-circle-outline"
          :loading="actionLoading === item.id"
          @click="emit('checkout', item.id)"
          :aria-label="`Check out ${item.title}`"
        >Out</v-btn>

        <!-- Return -->
        <v-btn v-else
          size="small" variant="tonal" color="success"
          prepend-icon="mdi-arrow-left-circle-outline"
          :loading="actionLoading === item.id"
          @click="emit('return', item.id)"
          :aria-label="`Return ${item.title}`"
        >In</v-btn>

        <!-- Edit -->
        <v-tooltip text="Edit" location="top">
          <template #activator="{ props: tip }">
            <v-btn v-bind="tip" icon="mdi-pencil-outline" size="small" variant="text"
              @click="emit('edit', item)" :aria-label="`Edit ${item.title}`" />
          </template>
        </v-tooltip>

        <!-- Remove -->
        <v-tooltip :text="item.status === 'checked-out' ? 'Cannot remove while checked out' : 'Remove'" location="top">
          <template #activator="{ props: tip }">
            <v-btn v-bind="tip" icon="mdi-trash-can-outline" size="small" variant="text" color="error"
              :disabled="item.status === 'checked-out'"
              @click="requestRemove(item)" :aria-label="`Remove ${item.title}`" />
          </template>
        </v-tooltip>
      </div>
    </template>

    <template #no-data>
      <EmptyState title="No resources found" message="Try adjusting your search or filters, or add a new resource." icon="mdi-book-search-outline" />
    </template>
  </v-data-table>
</template>
