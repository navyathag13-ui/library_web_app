/**
 * UI store — global snackbar/toast state.
 *
 * Replaces the provide/inject pattern used in ResourceHub with a
 * proper Pinia store: any component can call ui.showSuccess() / ui.showError().
 */
import { ref } from 'vue'
import { defineStore } from 'pinia'

type SnackColor = 'success' | 'error' | 'info' | 'warning'

export const useUiStore = defineStore('ui', () => {
  const show    = ref(false)
  const message = ref('')
  const color   = ref<SnackColor>('success')

  function showSuccess(msg: string) { _show(msg, 'success') }
  function showError(msg: string)   { _show(msg, 'error')   }
  function showInfo(msg: string)    { _show(msg, 'info')    }
  function hide()                   { show.value = false     }

  function _show(msg: string, c: SnackColor) {
    message.value = msg
    color.value   = c
    show.value    = true
  }

  return { show, message, color, showSuccess, showError, showInfo, hide }
})
