<script setup lang="ts">
/**
 * ResourcesView — full resource management page.
 * New vs ResourceHub: Edit modal, Checkout modal with borrower name,
 *   ResourceDetailDrawer, server-side pagination, sort controls.
 */
import { onMounted, ref, watch }    from 'vue'
import { useResourceStore }         from '../stores/resources'
import ResourceTable                from '../components/ResourceTable.vue'
import SearchFilter                 from '../components/SearchFilter.vue'
import AddResourceModal             from '../components/AddResourceModal.vue'
import EditResourceModal            from '../components/EditResourceModal.vue'
import CheckoutModal                from '../components/CheckoutModal.vue'
import ResourceDetailDrawer         from '../components/ResourceDetailDrawer.vue'
import type { Resource, ResourceFormData, CheckoutFormData } from '../types'

const store = useResourceStore()

onMounted(() => store.fetchResources())

// Reload when filters change (debounced via SearchFilter)
watch(
  () => ({ ...store.filters }),
  () => store.fetchResources(true),
  { deep: true },
)

// ── Add modal ─────────────────────────────────────────────────────────────────
const showAdd  = ref(false)
const addBusy  = ref(false)
async function handleAdd(data: ResourceFormData) {
  addBusy.value = true
  const ok = await store.addResource(data)
  addBusy.value = false
  if (ok) showAdd.value = false
}

// ── Edit modal ────────────────────────────────────────────────────────────────
const showEdit   = ref(false)
const editTarget = ref<Resource | null>(null)
const editBusy   = ref(false)
function openEdit(r: Resource) { editTarget.value = r; showEdit.value = true }
async function handleEdit(data: Partial<ResourceFormData>) {
  if (!editTarget.value) return
  editBusy.value = true
  const ok = await store.editResource(editTarget.value.id, data)
  editBusy.value = false
  if (ok) showEdit.value = false
}

// ── Checkout modal ────────────────────────────────────────────────────────────
const showCheckout      = ref(false)
const checkoutTarget    = ref<Resource | null>(null)
const checkoutBusy      = ref(false)
function openCheckout(id: number) {
  checkoutTarget.value = store.resources.find(r => r.id === id) ?? null
  showCheckout.value = true
}
async function handleCheckout(data: CheckoutFormData) {
  if (!checkoutTarget.value) return
  checkoutBusy.value = true
  const ok = await store.checkoutResource(checkoutTarget.value.id, data)
  checkoutBusy.value = false
  if (ok) showCheckout.value = false
}

// ── Return ────────────────────────────────────────────────────────────────────
async function handleReturn(id: number) {
  await store.returnResource(id)
}

// ── Detail drawer ─────────────────────────────────────────────────────────────
const showDrawer = ref(false)
async function openDrawer(id: number) {
  await store.fetchResourceDetail(id)
  showDrawer.value = true
}

// ── Remove ────────────────────────────────────────────────────────────────────
async function handleRemove(id: number) { await store.removeResource(id) }
</script>

<template>
  <div>

    <!-- Page header -->
    <div class="d-flex align-start justify-space-between mb-6 flex-wrap gap-3">
      <div>
        <h1 class="text-h5 font-weight-bold mb-1">Resources</h1>
        <p class="text-body-2 text-medium-emphasis">
          Manage inventory, check-outs, and availability. {{ store.total ? `(${store.total} items)` : '' }}
        </p>
      </div>
      <v-btn color="primary" variant="tonal" prepend-icon="mdi-plus" @click="showAdd = true" aria-label="Add new resource">
        Add Resource
      </v-btn>
    </div>

    <!-- Error banner -->
    <v-alert v-if="store.error" type="error" variant="tonal" rounded="lg" class="mb-4" closable>
      {{ store.error }}
    </v-alert>

    <!-- Search + filter + sort -->
    <v-card rounded="lg" elevation="1" class="pa-4 mb-4">
      <SearchFilter
        :search="store.filters.search"
        :status="store.filters.status"
        :category="store.filters.category"
        :sort-by="store.filters.sortBy"
        :sort-order="store.filters.sortOrder"
        :categories="store.categories"
        @update:search="store.setFilter('search', $event)"
        @update:status="store.setFilter('status', $event)"
        @update:category="store.setFilter('category', $event)"
        @update:sort-by="store.setFilter('sortBy', $event)"
        @update:sort-order="store.setFilter('sortOrder', $event)"
        @clear="store.clearFilters()"
      />
    </v-card>

    <!-- Table -->
    <ResourceTable
      :resources="store.resources"
      :loading="store.loading"
      :action-loading="store.actionLoading"
      @view="openDrawer"
      @checkout="openCheckout"
      @return="handleReturn"
      @edit="openEdit"
      @remove="handleRemove"
    />

    <!-- Pagination -->
    <div v-if="store.pages > 1" class="d-flex justify-center mt-4">
      <v-pagination
        :model-value="store.page"
        :length="store.pages"
        :total-visible="7"
        @update:model-value="store.setPage($event)"
        aria-label="Resource pagination"
      />
    </div>

    <!-- Modals & drawer -->
    <AddResourceModal      v-model="showAdd"      :loading="addBusy"      @submit="handleAdd"     />
    <EditResourceModal     v-model="showEdit"     :resource="editTarget"  :loading="editBusy"      @submit="handleEdit"    />
    <CheckoutModal         v-model="showCheckout" :resource="checkoutTarget" :loading="checkoutBusy" @submit="handleCheckout" />
    <ResourceDetailDrawer
      v-model="showDrawer"
      :resource="store.selectedResource"
      @checkout="id => { showDrawer = false; openCheckout(id) }"
      @return="id  => { showDrawer = false; handleReturn(id)  }"
      @edit="r    => { showDrawer = false; openEdit(r)        }"
    />

  </div>
</template>
