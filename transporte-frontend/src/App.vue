<template>
  <RouterView />
</template>

<script setup>
// App.vue corregido
import { onMounted } from 'vue'
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const authStore = useAuthStore()

onMounted(async () => {
  if (authStore.estaAutenticado) {
    // Verificar/renovar token al cargar la app
    try {
      await authStore.cargarPerfil()
    } catch {
      // Si falla cargarPerfil el interceptor ya maneja el refresh
    }
    authStore._escucharActividad()
  }
})
</script>