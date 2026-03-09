import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cajaService } from '../services/caja.service'

export const useCajaStore = defineStore('caja', () => {
    const sesionActiva  = ref(null)
    const sesiones      = ref([])
    const movimientos   = ref([])
    const cargando      = ref(false)
    const error         = ref(null)

    const cajaAbierta = computed(() => sesionActiva.value?.estado === 'abierta')

    const resumen = computed(() => {
        if (!movimientos.value.length) return { ingresos: 0, egresos: 0, anulaciones: 0 }
        return movimientos.value.reduce((acc, m) => {
            if (m.tipo === 'venta_pasaje' || m.tipo === 'venta_encomienda') {
                acc.ingresos += parseFloat(m.monto || 0)
            } else if (m.tipo === 'gasto') {
                acc.egresos += parseFloat(m.monto || 0)
            } else if (m.tipo === 'anulacion') {
                acc.anulaciones += parseFloat(m.monto || 0)
            }
            return acc
        }, { ingresos: 0, egresos: 0, anulaciones: 0 })
    })

    const saldoEsperado = computed(() => {
        if (!sesionActiva.value) return 0
        const { ingresos, egresos, anulaciones } = resumen.value
        return parseFloat(sesionActiva.value.monto_inicial || 0) + ingresos - egresos - anulaciones
    })

    async function cargarMiSesion() {
        try {
            const { data } = await cajaService.miSesionActiva()
            sesionActiva.value = data
        } catch {
            sesionActiva.value = null
        }
    }

    async function cargarSesiones(params = {}) {
        cargando.value = true
        try {
            const { data } = await cajaService.obtenerSesiones(params)
            sesiones.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar sesiones'
        } finally {
            cargando.value = false
        }
    }

    async function cargarMovimientos(params = {}) {
        cargando.value = true
        try {
            const { data } = await cajaService.obtenerMovimientos({
                sesion: sesionActiva.value?.id,
                ...params,
            })
            movimientos.value = data.results ?? data
        } catch (e) {
            error.value = e.response?.data || 'Error al cargar movimientos'
        } finally {
            cargando.value = false
        }
    }

    return {
        sesionActiva, sesiones, movimientos,
        cargando, error,
        cajaAbierta, resumen, saldoEsperado,
        cargarMiSesion, cargarSesiones, cargarMovimientos,
    }
})