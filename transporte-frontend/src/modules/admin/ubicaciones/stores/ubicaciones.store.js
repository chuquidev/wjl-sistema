import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ubicacionesService } from '../services/ubicaciones.service'

export const useUbicacionesStore = defineStore('ubicaciones', () => {
    const sucursales = ref([])
    const ciudades   = ref([])
    const rutas      = ref([])
    const cargando   = ref(false)
    const error      = ref(null)

    async function cargarSucursales(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await ubicacionesService.obtenerSucursales(params)
            sucursales.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar sucursales'
        } finally {
            cargando.value = false
        }
    }

    async function cargarCiudades(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await ubicacionesService.obtenerCiudades(params)
            ciudades.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar ciudades'
        } finally {
            cargando.value = false
        }
    }

    async function cargarRutas(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await ubicacionesService.obtenerRutas(params)
            rutas.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar rutas'
        } finally {
            cargando.value = false
        }
    }

    return {
        sucursales, ciudades, rutas,
        cargando, error,
        cargarSucursales, cargarCiudades, cargarRutas,
    }
})