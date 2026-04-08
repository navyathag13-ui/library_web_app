import { describe, it, expect, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import ConfirmDialog from '../components/ConfirmDialog.vue'

const vuetify = createVuetify({ components, directives })

afterEach(() => { document.body.innerHTML = '' })

function mountDialog(modelValue: boolean, props: Record<string, unknown> = {}) {
  return mount(ConfirmDialog, {
    props: {
      modelValue,
      title: 'Delete item',
      message: 'Are you sure you want to delete this item?',
      confirmLabel: 'Delete',
      ...props,
    },
    global: { plugins: [vuetify] },
    attachTo: document.body,
  })
}

describe('ConfirmDialog', () => {
  it('renders title and message when open', async () => {
    mountDialog(true)
    await new Promise(r => setTimeout(r, 50))
    expect(document.body.textContent).toContain('Delete item')
    expect(document.body.textContent).toContain('Are you sure you want to delete this item?')
  })

  it('shows the confirm label on the confirm button', async () => {
    mountDialog(true)
    await new Promise(r => setTimeout(r, 50))
    const buttons = [...document.querySelectorAll('button')]
    const labels = buttons.map(b => b.textContent?.trim())
    expect(labels).toContain('Delete')
  })

  it('emits confirm when confirm button is clicked', async () => {
    const w = mountDialog(true)
    await new Promise(r => setTimeout(r, 50))
    const buttons = [...document.querySelectorAll('button')]
    const confirmBtn = buttons.find(b => b.textContent?.trim() === 'Delete')
    expect(confirmBtn).toBeTruthy()
    confirmBtn!.click()
    await new Promise(r => setTimeout(r, 50))
    expect(w.emitted('confirm')).toBeTruthy()
  })

  it('emits update:modelValue false when Cancel is clicked', async () => {
    const w = mountDialog(true)
    await new Promise(r => setTimeout(r, 50))
    const buttons = [...document.querySelectorAll('button')]
    const cancelBtn = buttons.find(b => b.textContent?.trim() === 'Cancel')
    expect(cancelBtn).toBeTruthy()
    cancelBtn!.click()
    await new Promise(r => setTimeout(r, 50))
    const emitted = w.emitted('update:modelValue')
    expect(emitted).toBeTruthy()
    expect(emitted![0]).toEqual([false])
  })
})
