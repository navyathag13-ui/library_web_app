import { describe, it, expect, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import LoanStatusBadge from '../components/LoanStatusBadge.vue'

const vuetify = createVuetify({ components, directives })

afterEach(() => { document.body.innerHTML = '' })

function mountBadge(status: string, isOverdue = false) {
  return mount(LoanStatusBadge, {
    props: { status, isOverdue },
    global: { plugins: [vuetify] },
    attachTo: document.body,
  })
}

describe('LoanStatusBadge', () => {
  it('shows "Active" for active non-overdue loan', () => {
    const w = mountBadge('active', false)
    expect(w.text()).toContain('Active')
  })

  it('shows "Overdue" when isOverdue is true regardless of status', () => {
    const w = mountBadge('active', true)
    expect(w.text()).toContain('Overdue')
  })

  it('shows "Returned" for returned loan', () => {
    const w = mountBadge('returned', false)
    expect(w.text()).toContain('Returned')
  })

  it('shows "Overdue" for overdue status', () => {
    const w = mountBadge('overdue', false)
    expect(w.text()).toContain('Overdue')
  })

  it('applies error color for overdue', () => {
    const w = mountBadge('active', true)
    expect(w.html()).toMatch(/error/)
  })

  it('applies success color for returned', () => {
    const w = mountBadge('returned', false)
    expect(w.html()).toMatch(/success/)
  })

  it('applies info color for active', () => {
    const w = mountBadge('active', false)
    expect(w.html()).toMatch(/info/)
  })
})
