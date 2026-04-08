/**
 * Resource store — enhanced version of ResourceHub's store.
 *
 * New in final version:
 *   - Server-side pagination (no longer keeping all resources in memory)
 *   - Sort controls
 *   - checkoutResource / returnResource with loan data
 *   - updateResource (for edit modal)
 *   - fetchResourceDetail (single resource + loan history)
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { api } from '../api'
import { useUiStore } from './ui'
import type {
  Resource, ResourceFormData, CheckoutFormData, FilterState,
} from '../types'

export const useResourceStore = defineStore('resources', () => {
  const ui = useUiStore()

  // ── State ─────────────────────────────────────────────────────────────────
  const resources     = ref<Resource[]>([])
  const selectedResource = ref<Resource | null>(null)  // for detail drawer
  const loading       = ref(false)
  const actionLoading = ref<number | null>(null)       // id being actioned
  const error         = ref<string | null>(null)
  const total         = ref(0)
  const page          = ref(1)
  const perPage       = ref(20)
  const pages         = ref(1)

  const filters = ref<FilterState>({
    search:    '',
    status:    '',
    category:  '',
    sortBy:    'dateAdded',
    sortOrder: 'desc',
  })

  // ── Derived ───────────────────────────────────────────────────────────────
  const categories = computed(() =>
    [...new Set(resources.value.map(r => r.category))].sort()
  )

  // ── Actions ───────────────────────────────────────────────────────────────

  async function fetchResources(resetPage = false) {
    if (resetPage) page.value = 1
    loading.value = true
    error.value   = null
    try {
      const res = await api.getResources({
        search:     filters.value.search,
        status:     filters.value.status,
        category:   filters.value.category,
        sort_by:    filters.value.sortBy,
        sort_order: filters.value.sortOrder,
        page:       page.value,
        per_page:   perPage.value,
      })
      resources.value = res.resources
      total.value     = res.total
      pages.value     = res.pages
    } catch {
      error.value = 'Could not load resources. Is the backend running?'
    } finally {
      loading.value = false
    }
  }

  async function fetchResourceDetail(id: number) {
    try {
      selectedResource.value = await api.getResource(id)
    } catch {
      ui.showError('Could not load resource details')
    }
  }

  async function addResource(data: ResourceFormData): Promise<boolean> {
    try {
      const res = await api.createResource(data)
      ui.showSuccess(res.message)
      await fetchResources()
      return true
    } catch (e: unknown) {
      ui.showError(_apiError(e, 'Failed to add resource'))
      return false
    }
  }

  async function editResource(id: number, data: Partial<ResourceFormData>): Promise<boolean> {
    try {
      const res = await api.updateResource(id, data)
      _replaceInList(res.resource)
      if (selectedResource.value?.id === id) selectedResource.value = res.resource
      ui.showSuccess(res.message)
      return true
    } catch (e: unknown) {
      ui.showError(_apiError(e, 'Failed to update resource'))
      return false
    }
  }

  async function removeResource(id: number): Promise<boolean> {
    actionLoading.value = id
    try {
      const res = await api.deleteResource(id)
      resources.value = resources.value.filter(r => r.id !== id)
      if (selectedResource.value?.id === id) selectedResource.value = null
      total.value = Math.max(0, total.value - 1)
      ui.showSuccess(res.message)
      return true
    } catch (e: unknown) {
      ui.showError(_apiError(e, 'Failed to remove resource'))
      return false
    } finally {
      actionLoading.value = null
    }
  }

  async function checkoutResource(id: number, data: CheckoutFormData): Promise<boolean> {
    actionLoading.value = id
    try {
      const res = await api.checkoutResource(id, data)
      _replaceInList(res.resource)
      if (selectedResource.value?.id === id) await fetchResourceDetail(id)
      ui.showSuccess(res.message)
      return true
    } catch (e: unknown) {
      ui.showError(_apiError(e, 'Checkout failed'))
      return false
    } finally {
      actionLoading.value = null
    }
  }

  async function returnResource(id: number, loanId?: number): Promise<boolean> {
    actionLoading.value = id
    try {
      const res = await api.returnResource(id, loanId)
      _replaceInList(res.resource)
      if (selectedResource.value?.id === id) await fetchResourceDetail(id)
      ui.showSuccess(res.message)
      return true
    } catch (e: unknown) {
      ui.showError(_apiError(e, 'Return failed'))
      return false
    } finally {
      actionLoading.value = null
    }
  }

  function setFilter(key: keyof FilterState, value: string) {
    (filters.value as Record<string, string>)[key] = value
  }

  function clearFilters() {
    filters.value = { search: '', status: '', category: '', sortBy: 'dateAdded', sortOrder: 'desc' }
  }

  function setPage(p: number) {
    page.value = p
    fetchResources()
  }

  // ── Private ───────────────────────────────────────────────────────────────

  function _replaceInList(updated: Resource) {
    const idx = resources.value.findIndex(r => r.id === updated.id)
    if (idx !== -1) resources.value[idx] = updated
  }

  function _apiError(e: unknown, fallback: string): string {
    return (e as { response?: { data?: { error?: string } } })?.response?.data?.error ?? fallback
  }

  return {
    resources, selectedResource, loading, actionLoading, error,
    total, page, perPage, pages, filters, categories,
    fetchResources, fetchResourceDetail,
    addResource, editResource, removeResource,
    checkoutResource, returnResource,
    setFilter, clearFilters, setPage,
  }
})
