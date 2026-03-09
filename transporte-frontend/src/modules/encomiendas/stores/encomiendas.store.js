import { defineStore } from 'pinia'
import { ref } from 'vue'
import { encomiendasService } from '../services/encomiendas.service'

export const useEncomiendasStore = defineStore('encomiendas', () => {
    const encomiendas = ref([])
    const viajes      = ref([])
    const cargando    = ref(false)
    const error       = ref(null)

    async function cargarEncomiendas(params = {}) {
        cargando.value = true
        error.value    = null
        try {
            const { data } = await encomiendasService.obtenerEncomiendas(params)
            encomiendas.value = data.results ?? data
        } catch (e) {
            error.value = 'Error al cargar encomiendas'
        } finally {
            cargando.value = false
        }
    }

    async function cargarViajes(params = {}) {
        try {
            const { data } = await encomiendasService.buscarViajes({
                estado: 'programado',
                ...params,
            })
            viajes.value = data.results ?? data
        } catch (e) {
            error.value = 'Error al cargar viajes'
        }
    }

    return { encomiendas, viajes, cargando, error, cargarEncomiendas, cargarViajes }
})