<script setup lang="ts">
/**
 * EditResourceModal — pre-populated form for editing an existing resource.
 * New in final version (was not in ResourceHub).
 */
import { ref, watch } from 'vue'
import type { Resource, ResourceFormData } from '../types'

const props = defineProps<{ modelValue: boolean; resource: Resource | null; loading?: boolean }>()
const emit  = defineEmits<{
  'update:modelValue': [value: boolean]
  'submit': [data: Partial<ResourceFormData>]
}>()

const form        = ref<{ validate(): Promise<{ valid: boolean }> } | null>(null)
const title       = ref(''); const author   = ref('')
const category    = ref(''); const isbn     = ref('')
const description = ref(''); const copies   = ref(1)

const categories = ['Fiction', 'Non-Fiction', 'Technology', 'Science', 'History', 'Art', 'General', 'Reference']
const required   = (v: string) => !!v?.trim() || 'Required'
const posInt     = (v: number) => v >= 1 || 'At least 1 copy'

// Populate from the resource being edited
watch(() => props.resource, r => {
  if (r) {
    title.value = r.title; author.value = r.author; category.value = r.category
    isbn.value = r.isbn ?? ''; description.value = r.description ?? ''; copies.value = r.totalCopies
  }
}, { immediate: true })

async function submit() {
  const { valid } = await form.value!.validate()
  if (!valid) return
  emit('submit', {
    title: title.value.trim(), author: author.value.trim(),
    category: category.value, description: description.value.trim(),
    isbn: isbn.value.trim(), totalCopies: copies.value,
  })
}
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="520" @update:model-value="emit('update:modelValue', $event)">
    <v-card rounded="lg">
      <v-card-title class="pt-5 px-6">
        <v-icon icon="mdi-pencil-outline" color="primary" class="mr-2" />Edit Resource
      </v-card-title>
      <v-form ref="form" @submit.prevent="submit">
        <v-card-text class="px-6 pt-3">
          <v-row dense>
            <v-col cols="12">
              <v-text-field v-model="title" label="Title *" variant="outlined" :rules="[required]" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="author" label="Author *" variant="outlined" :rules="[required]" />
            </v-col>
            <v-col cols="6">
              <v-combobox v-model="category" :items="categories" label="Category" variant="outlined" />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="isbn" label="ISBN" variant="outlined" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="description" label="Description" variant="outlined" rows="2" auto-grow />
            </v-col>
            <v-col cols="6">
              <v-text-field v-model.number="copies" label="Total Copies *" type="number" variant="outlined" :rules="[posInt]" min="1" />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="px-6 pb-5">
          <v-spacer />
          <v-btn variant="text" :disabled="loading" @click="emit('update:modelValue', false)">Cancel</v-btn>
          <v-btn type="submit" color="primary" variant="tonal" :loading="loading">Save Changes</v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>
