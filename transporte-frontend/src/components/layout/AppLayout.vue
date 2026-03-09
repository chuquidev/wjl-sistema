<template>
    <div class="min-h-screen bg-gray-50">
        <AppSidebar />
        <AppHeader />
        <main class="transition-all duration-300 ease-in-out pt-[60px] min-h-screen ml-0"
            :class="[ui.sidebarCollapsed ? 'lg:ml-[68px]' : 'lg:ml-[260px]']">
            <div class="p-3 sm:p-6 max-w-screen-2xl mx-auto">
                <RouterView />
            </div>
        </main>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUiStore }   from '@/stores/ui.store'
import { useCajaStore } from '@/modules/caja/stores/caja.store'
import AppSidebar from './AppSidebar.vue'
import AppHeader  from './AppHeader.vue'

const ui   = useUiStore()
const caja = useCajaStore()

// Cargar estado de caja al iniciar el layout (una sola vez)
// Así el header siempre refleja el estado real sin importar
// desde qué módulo se recarga la página
onMounted(async () => {
    await caja.cargarMiSesion()
})
</script>