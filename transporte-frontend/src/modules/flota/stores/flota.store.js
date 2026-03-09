import { defineStore } from 'pinia'
import { ref } from 'vue'
import { flotaService } from '../services/flota.service'

export const useFlotaStore = defineStore('flota', () => {
    const vehiculos   = ref([])
    const conductores = ref([])
    const viajes      = ref([])
    const rutas       = ref([])
    const cargando    = ref(false)
    const error       = ref(null)

    async function cargarVehiculos(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await flotaService.obtenerVehiculos(params)
            vehiculos.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar vehículos'
        } finally {
            cargando.value = false
        }
    }

    async function cargarConductores(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await flotaService.obtenerConductores(params)
            conductores.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar conductores'
        } finally {
            cargando.value = false
        }
    }

    async function cargarViajes(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await flotaService.obtenerViajes(params)
            viajes.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar viajes'
        } finally {
            cargando.value = false
        }
    }

    async function cargarRutas() {
        try {
            const { data } = await flotaService.obtenerRutas()
            rutas.value = data.results ?? data
        } catch { /* silencioso */ }
    }

    return {
        vehiculos, conductores, viajes, rutas,
        cargando, error,
        cargarVehiculos, cargarConductores, cargarViajes, cargarRutas,
    }
})