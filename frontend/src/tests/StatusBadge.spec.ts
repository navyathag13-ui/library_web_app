import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import StatusBadge from '../components/StatusBadge.vue'

const vuetify = createVuetify({ components, directives })

function mountBadge(status: string) {
  return mount(StatusBadge, {
    props: { status },
    global: { plugins: [vuetify] },
    attachTo: document.body,
  })
}

describe('StatusBadge', () => {
  it('renders "Available" for available status', () => {
    const w = mountBadge('available')
    expect(w.text()).toContain('Available')
  })

  it('renders "Checked Out" for checked-out status', () => {
    const w = mountBadge('checked-out')
    expect(w.text()).toContain('Checked Out')
  })

  it('applies success color for available', () => {
    const w = mountBadge('available')
    // VChip renders color as a class
    expect(w.html()).toMatch(/success/)
  })

  it('applies warning color for checked-out', () => {
    const w = mountBadge('checked-out')
    expect(w.html()).toMatch(/warning/)
  })
})
