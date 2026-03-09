import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
    const sidebarCollapsed = ref(false)
    const mobileMenuOpen   = ref(false)

    // Solo una función toggle que maneje ambos casos
    function toggleSidebar() {
        if (window.innerWidth < 1024) {
            mobileMenuOpen.value = !mobileMenuOpen.value
        } else {
            sidebarCollapsed.value = !sidebarCollapsed.value
        }
    }

    function cerrarMenuMovil() {
        mobileMenuOpen.value = false
    }

    function abrirMenuMovil() {
        mobileMenuOpen.value = true
    }

    return {
        sidebarCollapsed,
        mobileMenuOpen,
        toggleSidebar,
        cerrarMenuMovil,
        abrirMenuMovil,
    }
})