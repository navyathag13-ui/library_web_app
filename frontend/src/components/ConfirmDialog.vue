<script setup lang="ts">
withDefaults(defineProps<{
  modelValue:    boolean
  title?:        string
  message?:      string
  confirmLabel?: string
  confirmColor?: string
  loading?:      boolean
}>(), {
  title:        'Are you sure?',
  message:      'This action cannot be undone.',
  confirmLabel: 'Confirm',
  confirmColor: 'error',
  loading:      false,
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'confirm': []
}>()
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="420" @update:model-value="emit('update:modelValue', $event)">
    <v-card rounded="lg">
      <v-card-title class="pt-5 px-5">
        <v-icon icon="mdi-alert-outline" color="warning" class="mr-2" />{{ title }}
      </v-card-title>
      <v-card-text class="px-5 pb-2 text-medium-emphasis">{{ message }}</v-card-text>
      <v-card-actions class="px-5 pb-5">
        <v-spacer />
        <v-btn variant="text" :disabled="loading" @click="emit('update:modelValue', false)">Cancel</v-btn>
        <v-btn :color="confirmColor" variant="tonal" :loading="loading" @click="emit('confirm')">
          {{ confirmLabel }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
