<script setup lang="ts">
/**
 * CheckoutModal — new in final version.
 * Collects borrower name + due date before checking out a resource.
 */
import { ref, computed, watch } from 'vue'
import type { Resource, CheckoutFormData } from '../types'

const props = defineProps<{ modelValue: boolean; resource: Resource | null; loading?: boolean }>()
const emit  = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [data: CheckoutFormData]
}>()

const form         = ref<{ validate(): Promise<{ valid: boolean }> } | null>(null)
const borrowerName = ref('')
const dueDate      = ref('')

// Default due date: 14 days from today
const defaultDue = computed(() => {
  const d = new Date()
  d.setDate(d.getDate() + 14)
  return d.toISOString().slice(0, 10)
})

watch(() => props.modelValue, open => {
  if (open) { borrowerName.value = ''; dueDate.value = defaultDue.value }
})

const required = (v: string) => !!v?.trim() || 'Required'

async function submit() {
  const { valid } = await form.value!.validate()
  if (!valid) return
  emit('submit', { borrowerName: borrowerName.value.trim(), dueDate: dueDate.value })
}
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="420" @update:model-value="emit('update:modelValue', $event)">
    <v-card rounded="lg">
      <v-card-title class="pt-5 px-6">
        <v-icon icon="mdi-arrow-right-circle-outline" color="primary" class="mr-2" />Check Out
      </v-card-title>
      <v-card-subtitle v-if="resource" class="px-6 pb-0 text-truncate">
        {{ resource.title }} · {{ resource.availableCopies }} cop{{ resource.availableCopies === 1 ? 'y' : 'ies' }} available
      </v-card-subtitle>

      <v-form ref="form" @submit.prevent="submit">
        <v-card-text class="px-6 pt-4">
          <v-text-field
            v-model="borrowerName"
            label="Borrower name *"
            variant="outlined"
            :rules="[required]"
            prepend-inner-icon="mdi-account-outline"
            placeholder="e.g. Alice Johnson"
            class="mb-3"
            autofocus
          />
          <v-text-field
            v-model="dueDate"
            label="Due date *"
            type="date"
            variant="outlined"
            :rules="[required]"
            prepend-inner-icon="mdi-calendar-outline"
            :min="new Date().toISOString().slice(0, 10)"
          />
        </v-card-text>
        <v-card-actions class="px-6 pb-5">
          <v-spacer />
          <v-btn variant="text" :disabled="loading" @click="emit('update:modelValue', false)">Cancel</v-btn>
          <v-btn type="submit" color="primary" variant="tonal" :loading="loading">Confirm Checkout</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>
