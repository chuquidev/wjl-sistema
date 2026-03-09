import { defineStore } from 'pinia'
import { ref } from 'vue'
import { pasajesService } from '../services/pasajes.service'

export const usePasajesStore = defineStore('pasajes', () => {
    const viajes      = ref([])
    const pasajes     = ref([])
    const cargando    = ref(false)
    const error       = ref(null)

    async function buscarViajes(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await pasajesService.buscarViajes({
                estado: 'programado',
                ...params,
            })
            viajes.value = data.results ?? data
        } catch (e) {
            error.value = 'Error al buscar viajes'
        } finally {
            cargando.value = false
        }
    }

    async function cargarPasajes(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await pasajesService.obtenerPasajes(params)
            pasajes.value = data.results ?? data
        } catch (e) {
            error.value = 'Error al cargar pasajes'
        } finally {
            cargando.value = false
        }
    }

    return { viajes, pasajes, cargando, error, buscarViajes, cargarPasajes }
})