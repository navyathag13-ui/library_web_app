/**
 * Loans store — for the History view.
 */
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { api } from '../api'
import type { Loan, LoanFilterState } from '../types'

export const useLoanStore = defineStore('loans', () => {
  const loans   = ref<Loan[]>([])
  const loading = ref(false)
  const total   = ref(0)
  const page    = ref(1)
  const perPage = ref(20)
  const pages   = ref(1)

  const filters = ref<LoanFilterState>({ search: '', status: '' })

  async function fetchLoans(resetPage = false) {
    if (resetPage) page.value = 1
    loading.value = true
    try {
      const res = await api.getLoans({
        search:   filters.value.search,
        status:   filters.value.status,
        page:     page.value,
        per_page: perPage.value,
      })
      loans.value = res.loans
      total.value = res.total
      pages.value = res.pages
    } finally {
      loading.value = false
    }
  }

  function setFilter(key: keyof LoanFilterState, value: string) {
    (filters.value as Record<string, string>)[key] = value
  }

  function setPage(p: number) {
    page.value = p
    fetchLoans()
  }

  return { loans, loading, total, page, perPage, pages, filters, fetchLoans, setFilter, setPage }
})
