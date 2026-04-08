<script setup lang="ts">
/**
 * SearchFilter — search + status + category + sort controls.
 * Enhanced from ResourceHub: adds sort_by + sort_order dropdowns.
 */
import { ref, watch } from 'vue'
import type { ResourceStatus } from '../types'

const props = defineProps<{
  search:     string
  status:     ResourceStatus | ''
  category:   string
  sortBy:     string
  sortOrder:  'asc' | 'desc'
  categories: string[]
}>()

const emit = defineEmits<{
  'update:search':    [v: string]
  'update:status':    [v: ResourceStatus | '']
  'update:category':  [v: string]
  'update:sortBy':    [v: string]
  'update:sortOrder': [v: 'asc' | 'desc']
  'clear': []
}>()

const localSearch = ref(props.search)
let debounce: ReturnType<typeof setTimeout>
watch(localSearch, v => {
  clearTimeout(debounce)
  debounce = setTimeout(() => emit('update:search', v), 300)
})

const statusOpts = [
  { title: 'All statuses', value: '' },
  { title: 'Available',    value: 'available'   },
  { title: 'Checked Out',  value: 'checked-out' },
]
const sortOpts = [
  { title: 'Date Added',   value: 'dateAdded'       },
  { title: 'Title',        value: 'title'           },
  { title: 'Author',       value: 'author'          },
  { title: 'Category',     value: 'category'        },
  { title: 'Availability', value: 'availableCopies' },
]
</script>

<template>
  <v-row dense align="center">
    <v-col cols="12" sm="4" md="3">
      <v-text-field
        v-model="localSearch"
        prepend-inner-icon="mdi-magnify"
        label="Search title, author, ISBN"
        variant="outlined" density="compact" clearable hide-details
        @click:clear="emit('update:search', '')"
        aria-label="Search resources"
      />
    </v-col>
    <v-col cols="6" sm="3" md="2">
      <v-select
        :model-value="status" :items="statusOpts" item-title="title" item-value="value"
        label="Status" variant="outlined" density="compact" hide-details
        @update:model-value="emit('update:status', $event)" aria-label="Filter by status"
      />
    </v-col>
    <v-col cols="6" sm="3" md="2">
      <v-select
        :model-value="category"
        :items="[{ title: 'All categories', value: '' }, ...categories.map(c => ({ title: c, value: c }))]"
        item-title="title" item-value="value"
        label="Category" variant="outlined" density="compact" hide-details
        @update:model-value="emit('update:category', $event)" aria-label="Filter by category"
      />
    </v-col>
    <v-col cols="6" sm="3" md="2">
      <v-select
        :model-value="sortBy" :items="sortOpts" item-title="title" item-value="value"
        label="Sort by" variant="outlined" density="compact" hide-details
        @update:model-value="emit('update:sortBy', $event)" aria-label="Sort by field"
      />
    </v-col>
    <v-col cols="auto">
      <v-btn-toggle
        :model-value="sortOrder"
        density="compact" variant="outlined" divided
        @update:model-value="v => emit('update:sortOrder', v ?? 'desc')"
        aria-label="Sort direction"
      >
        <v-btn value="asc" icon="mdi-sort-ascending" aria-label="Ascending" size="small" />
        <v-btn value="desc" icon="mdi-sort-descending" aria-label="Descending" size="small" />
      </v-btn-toggle>
    </v-col>
    <v-col cols="auto">
      <v-btn variant="text" size="small" @click="emit('clear')" aria-label="Clear filters">Clear</v-btn>
    </v-col>
  </v-row>
</template>
