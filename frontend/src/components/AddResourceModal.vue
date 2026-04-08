<script setup lang="ts">
import { ref, watch } from 'vue'
import type { ResourceFormData } from '../types'

const props = defineProps<{ modelValue: boolean; loading?: boolean }>()
const emit  = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [data: ResourceFormData]
}>()

const form        = ref<{ validate(): Promise<{ valid: boolean }> } | null>(null)
const title       = ref(''); const author   = ref('')
const category    = ref(''); const isbn     = ref('')
const description = ref(''); const copies   = ref(1)

const categories = ['Fiction', 'Non-Fiction', 'Technology', 'Science', 'History', 'Art', 'General', 'Reference']
const required   = (v: string) => !!v?.trim() || 'Required'
const posInt     = (v: number) => v >= 1 || 'At least 1 copy'

watch(() => props.modelValue, open => {
  if (open) { title.value = ''; author.value = ''; category.value = ''; isbn.value = ''; description.value = ''; copies.value = 1 }
})

async function submit() {
  const { valid } = await form.value!.validate()
  if (!valid) return
  emit('submit', {
    title: title.value.trim(), author: author.value.trim(),
    category: category.value || 'General', description: description.value.trim(),
    isbn: isbn.value.trim(), totalCopies: copies.value,
  })
}
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="520" @update:model-value="emit('update:modelValue', $event)">
    <v-card rounded="lg">
      <v-card-title class="pt-5 px-6">
        <v-icon icon="mdi-plus-circle-outline" color="primary" class="mr-2" />Add Resource
      </v-card-title>
      <v-form ref="form" @submit.prevent="submit">
        <v-card-text class="px-6 pt-3">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="title" label="Title *" variant="outlined" :rules="[required]" autofocus />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="author" label="Author *" variant="outlined" :rules="[required]" />
            </v-col>
            <v-col cols="6">
              <v-combobox v-model="category" :items="categories" label="Category" variant="outlined" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="isbn" label="ISBN (optional)" variant="outlined" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="description" label="Description (optional)" variant="outlined" rows="2" auto-grow />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model.number="copies" label="Total Copies *" type="number" variant="outlined" :rules="[posInt]" min="1" />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="px-6 pb-5">
          <v-spacer />
          <v-btn variant="text" :disabled="loading" @click="emit('update:modelValue', false)">Cancel</v-btn>
          <v-btn type="submit" color="primary" variant="tonal" :loading="loading">Add Resource</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>
