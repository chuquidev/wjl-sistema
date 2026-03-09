import { defineStore } from 'pinia'
import { ref } from 'vue'
import { usuariosService } from '../services/usuarios.service'

export const useUsuariosStore = defineStore('usuarios', () => {
    const usuarios   = ref([])
    const sucursales = ref([])
    const cargando   = ref(false)
    const error      = ref(null)

    async function cargarUsuarios(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await usuariosService.obtenerUsuarios(params)
            usuarios.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar usuarios'
        } finally {
            cargando.value = false
        }
    }

    async function cargarSucursales() {
        try {
            const { data } = await usuariosService.obtenerSucursales()
            sucursales.value = data.results ?? data
        } catch { /* silencioso */ }
    }

    return { usuarios, sucursales, cargando, error, cargarUsuarios, cargarSucursales }
})