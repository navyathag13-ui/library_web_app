/**
 * Centralised Axios API client — all backend calls go through here.
 * Merges ResourceHub's api/resources.ts with new loan + stats endpoints.
 */
import axios from 'axios'
import type { Resource, ResourceFormData, CheckoutFormData, Loan, Stats } from '../types'

const http = axios.create({ baseURL: '/api', headers: { 'Content-Type': 'application/json' } })

// ─── Resource responses ───────────────────────────────────────────────────────

interface ResourceListRes {
  resources: Resource[]
  total:     number
  page:      number
  perPage:   number
  pages:     number
}
interface ResourceRes  { resource: Resource;  message: string }
interface CheckoutRes  { resource: Resource;  loan: Loan;    message: string }
interface ReturnRes    { resource: Resource;  loan: Loan;    message: string }
interface MessageRes   { message: string }

// ─── Loan responses ───────────────────────────────────────────────────────────

interface LoanListRes {
  loans:   Loan[]
  total:   number
  page:    number
  perPage: number
  pages:   number
}

// ─── API ──────────────────────────────────────────────────────────────────────

export const api = {

  // Resources ─────────────────────────────────────────────────────────────────

  async getResources(params?: Record<string, string | number>): Promise<ResourceListRes> {
    return (await http.get<ResourceListRes>('/resources', { params })).data
  },

  async getResource(id: number): Promise<Resource> {
    return (await http.get<Resource>('/resources/' + id)).data
  },

  async createResource(data: ResourceFormData): Promise<ResourceRes> {
    return (await http.post<ResourceRes>('/resources', data)).data
  },

  async updateResource(id: number, data: Partial<ResourceFormData>): Promise<ResourceRes> {
    return (await http.put<ResourceRes>('/resources/' + id, data)).data
  },

  async deleteResource(id: number): Promise<MessageRes> {
    return (await http.delete<MessageRes>('/resources/' + id)).data
  },

  async checkoutResource(id: number, data: CheckoutFormData): Promise<CheckoutRes> {
    return (await http.post<CheckoutRes>(`/resources/${id}/checkout`, data)).data
  },

  async returnResource(id: number, loanId?: number): Promise<ReturnRes> {
    return (await http.patch<ReturnRes>(`/resources/${id}/return`, loanId ? { loanId } : {})).data
  },

  // Loans ─────────────────────────────────────────────────────────────────────

  async getLoans(params?: Record<string, string | number>): Promise<LoanListRes> {
    return (await http.get<LoanListRes>('/loans', { params })).data
  },

  // Stats & activity ──────────────────────────────────────────────────────────

  async getStats(): Promise<Stats> {
    return (await http.get<Stats>('/stats')).data
  },

  async getActivity(): Promise<{ activity: Loan[] }> {
    return (await http.get<{ activity: Loan[] }>('/activity')).data
  },
}
