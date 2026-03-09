<template>
  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const authStore = useAuthStore()

onMounted(() => {
  if (authStore.estaAutenticado) {
    authStore._escucharActividad()
  }
})
</script>