import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import StatsCard from '../components/StatsCard.vue'

const vuetify = createVuetify({ components, directives })

function mountCard(props: Record<string, unknown>) {
  return mount(StatsCard, {
    props,
    global: { plugins: [vuetify] },
    attachTo: document.body,
  })
}

describe('StatsCard', () => {
  it('renders the label', () => {
    const w = mountCard({ label: 'Total Resources', value: 42, icon: 'mdi-bookshelf', color: 'primary', loading: false })
    expect(w.text()).toContain('Total Resources')
  })

  it('renders the numeric value', () => {
    const w = mountCard({ label: 'Available', value: 7, icon: 'mdi-check', color: 'success', loading: false })
    expect(w.text()).toContain('7')
  })

  it('shows skeleton loader when loading is true', () => {
    const w = mountCard({ label: 'Overdue', value: 0, icon: 'mdi-alert', color: 'error', loading: true })
    // Skeleton loader replaces value — the raw number should not appear
    expect(w.html()).toMatch(/skeleton/)
  })

  it('does not show skeleton when loading is false', () => {
    const w = mountCard({ label: 'Checked Out', value: 3, icon: 'mdi-clock', color: 'warning', loading: false })
    expect(w.html()).not.toMatch(/skeleton-loader/)
  })
})
