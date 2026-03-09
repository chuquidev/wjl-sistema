<template>
    <div class="space-y-6">

        <!-- Encabezado -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
                <h1 class="page-title">Dashboard</h1>
                <p class="page-subtitle">Resumen del día · {{ hoyFormateado }}</p>
            </div>
            <button @click="cargarDatos" :disabled="cargando" class="btn-secondary">
                <svg :class="['w-3.5 h-3.5', cargando ? 'animate-spin' : '']" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Actualizar
            </button>
        </div>

        <!-- Alerta caja cerrada -->
        <Transition name="fade">
            <div v-if="!cargando && cajaCerrada"
                class="flex items-center gap-3 p-4 rounded-xl bg-amber-50 border border-amber-200">
                <svg class="w-5 h-5 text-amber-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <p class="text-sm font-medium text-amber-800">
                    No tienes una caja abierta.
                    <router-link :to="{ name: 'caja' }"
                        class="underline font-bold hover:text-amber-600 transition-colors">
                        Abrir caja
                    </router-link>
                    para registrar ventas.
                </p>
            </div>
        </Transition>

        <!-- Skeleton -->
        <div v-if="cargando" class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div v-for="i in 4" :key="i" class="h-24 bg-white rounded-2xl border border-gray-100 animate-pulse"></div>
        </div>

        <!-- ── KPIs ──────────────────────────────────────────── -->
        <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-4">

            <!-- Ventas del día -->
            <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-start gap-3">
                <div class="w-10 h-10 rounded-xl bg-orange-50 flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
                <div class="min-w-0">
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-wider mb-0.5">Ventas del día</p>
                    <p class="text-xl font-black text-gray-900 truncate">S/. {{ formatearMonto(datos.total_ventas) }}
                    </p>
                    <p class="text-xs text-gray-400 mt-0.5 font-medium">{{ datos.total_pasajes || 0 }} pasajes</p>
                </div>
            </div>

            <!-- Pasajeros hoy -->
            <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-start gap-3">
                <div class="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                </div>
                <div class="min-w-0">
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-wider mb-0.5">Pasajeros hoy</p>
                    <p class="text-xl font-black text-gray-900">{{ datos.total_pasajes || 0 }}</p>
                    <p class="text-xs text-gray-400 mt-0.5 font-medium">tickets activos</p>
                </div>
            </div>

            <!-- Viajes -->
            <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-start gap-3">
                <div class="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2h8zm0 0l2-5h3l2 5m-7 0h7" />
                    </svg>
                </div>
                <div class="min-w-0">
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-wider mb-0.5">Viajes hoy</p>
                    <p class="text-xl font-black text-gray-900">{{ datos.total_viajes || 0 }}</p>
                    <div class="flex items-center gap-2 mt-0.5">
                        <span class="text-[10px] font-bold text-emerald-600">
                            {{ datos.viajes_estado?.en_curso || 0 }} RUTA
                        </span>
                        <span class="text-[10px] font-bold text-blue-600">
                            {{ datos.viajes_estado?.programado || 0 }} PROG.
                        </span>
                    </div>
                </div>
            </div>

            <!-- Encomiendas -->
            <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-start gap-3">
                <div class="w-10 h-10 rounded-xl bg-violet-50 flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-violet-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                </div>
                <div class="min-w-0">
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-wider mb-0.5">Encomiendas</p>
                    <p class="text-xl font-black text-gray-900">{{ datos.encomiendas?.total || 0 }}</p>
                    <p class="text-xs text-gray-400 mt-0.5 font-medium">
                        S/. {{ formatearMonto(datos.encomiendas?.ingresos) }}
                    </p>
                </div>
            </div>
        </div>

        <!-- ── Segunda fila ───────────────────────────────────── -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">

            <!-- Estado de viajes -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Estado de viajes</h3>
                </div>
                <div class="card-body grid grid-cols-2 gap-3">
                    <div v-for="est in estadosViaje" :key="est.clave"
                        :class="['rounded-2xl p-4 border transition-all hover:shadow-md', est.bg]">
                        <p class="text-2xl font-black mb-1" :class="est.texto">
                            {{ cargando ? '—' : (datos.viajes_estado?.[est.clave] || 0) }}
                        </p>
                        <p class="text-[10px] font-bold uppercase tracking-widest" :class="est.texto">
                            {{ est.etiqueta }}
                        </p>
                    </div>
                </div>
            </div>

            <!-- Encomiendas -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Encomiendas del día</h3>
                </div>
                <div class="card-body space-y-3">
                    <div class="flex justify-between items-center py-2 border-b border-gray-50">
                        <span class="text-sm text-gray-500 font-medium">Total registradas</span>
                        <span class="font-black text-gray-900">{{ datos.encomiendas?.total || 0 }}</span>
                    </div>
                    <div class="flex justify-between items-center py-2 border-b border-gray-50">
                        <span class="text-sm text-gray-500 font-medium">En tránsito</span>
                        <span class="font-black text-blue-600">{{ datos.encomiendas?.en_transito || 0 }}</span>
                    </div>
                    <div class="flex justify-between items-center py-2">
                        <span class="text-sm text-gray-500 font-medium">Ingresos</span>
                        <span class="font-black text-emerald-600">S/. {{ formatearMonto(datos.encomiendas?.ingresos)
                        }}</span>
                    </div>
                    <router-link :to="{ name: 'encomiendas' }"
                        class="mt-2 flex items-center justify-center py-2.5 w-full bg-gray-50 border border-gray-200 rounded-xl text-xs font-bold text-gray-700 hover:bg-gray-100 transition-all">
                        Ver encomiendas →
                    </router-link>
                </div>
            </div>

            <!-- Estado de caja -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Estado de caja</h3>
                </div>
                <div class="card-body">
                    <template v-if="cajaStore.cajaAbierta">
                        <div
                            class="flex items-center gap-2 mb-5 p-3 bg-emerald-50 rounded-xl border border-emerald-100">
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                            <span class="text-xs font-bold text-emerald-700 uppercase tracking-tighter">
                                Abierta desde {{ formatearHora(cajaStore.sesionActiva?.fecha_apertura) }}
                            </span>
                        </div>
                        <div class="space-y-3 px-1">
                            <div class="flex justify-between text-sm">
                                <span class="text-gray-500 font-medium">Monto inicial</span>
                                <span class="font-black text-gray-900">
                                    S/. {{ formatearMonto(cajaStore.sesionActiva?.monto_inicial) }}
                                </span>
                            </div>
                            <div class="flex justify-between text-sm">
                                <span class="text-gray-500 font-medium">Ingresos hoy</span>
                                <span class="font-black text-emerald-600">
                                    S/. {{ formatearMonto(cajaStore.resumen.ingresos - cajaStore.resumen.anulaciones) }}
                                </span>
                            </div>
                            <div class="flex justify-between text-sm">
                                <span class="text-gray-500 font-medium">Saldo esperado</span>
                                <span class="font-black text-blue-600">
                                    S/. {{ formatearMonto(cajaStore.saldoEsperado) }}
                                </span>
                            </div>
                        </div>
                        <router-link :to="{ name: 'caja' }"
                            class="mt-5 flex items-center justify-center py-2.5 w-full bg-gray-50 border border-gray-200 rounded-xl text-xs font-bold text-gray-700 hover:bg-gray-100 transition-all">
                            Ver caja →
                        </router-link>
                    </template>
                    <template v-else>
                        <div class="text-center py-4">
                            <div
                                class="w-14 h-14 rounded-2xl bg-amber-50 flex items-center justify-center mx-auto mb-3">
                                <svg class="w-7 h-7 text-amber-500" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </div>
                            <p class="text-sm font-black text-gray-900 mb-1">Caja cerrada</p>
                            <p class="text-xs text-gray-400 mb-5 font-medium px-4 leading-tight">
                                Abre tu caja para iniciar el registro de ventas.
                            </p>
                            <router-link :to="{ name: 'caja' }"
                                class="btn-primary text-[11px] uppercase tracking-widest">
                                Abrir caja ahora
                            </router-link>
                        </div>
                    </template>
                </div>
            </div>
        </div>

        <!-- ── Métodos de pago ────────────────────────────────── -->
        <div v-if="datos.metodos_pago?.length" class="card">
            <div class="card-header">
                <h3 class="card-title">Métodos de pago del día</h3>
            </div>
            <div class="card-body grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div v-for="mp in datos.metodos_pago" :key="mp.metodo"
                    class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100">
                    <span class="text-2xl">{{ emojiPago(mp.metodo) }}</span>
                    <div class="flex-1 min-w-0">
                        <p class="text-xs font-bold text-gray-500 uppercase tracking-wide">{{ etiquetaPago(mp.metodo) }}
                        </p>
                        <p class="text-sm font-black text-gray-900">S/. {{ formatearMonto(mp.total) }}</p>
                        <p class="text-[10px] text-gray-400 font-medium">{{ mp.cantidad }} · {{ mp.porcentaje }}%</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ── Rutas top + Tabla viajes ───────────────────────── -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">

            <!-- Rutas top -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Rutas más vendidas</h3>
                </div>
                <div class="card-body">
                    <div v-if="cargando" class="space-y-3">
                        <div v-for="i in 4" :key="i" class="h-8 bg-gray-50 rounded-lg animate-pulse"></div>
                    </div>
                    <div v-else-if="!datos.rutas_top?.length" class="text-center py-10 text-gray-400 italic text-sm">
                        Sin datos hoy
                    </div>
                    <div v-else class="space-y-3">
                        <div v-for="(ruta, i) in datos.rutas_top" :key="i" class="flex items-center gap-3">
                            <span :class="[
                                'w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-black flex-shrink-0',
                                i === 0 ? 'bg-yellow-400 text-white' :
                                    i === 1 ? 'bg-gray-300 text-white' :
                                        i === 2 ? 'bg-amber-600 text-white' : 'bg-gray-100 text-gray-500'
                            ]">{{ i + 1 }}</span>
                            <div class="flex-1 min-w-0">
                                <p class="text-sm font-bold text-gray-900 truncate">{{ ruta.ruta }}</p>
                                <div class="h-1.5 bg-gray-100 rounded-full mt-1 overflow-hidden">
                                    <div class="h-full bg-blue-500 rounded-full transition-all duration-500"
                                        :style="{ width: (ruta.total / datos.rutas_top[0].total * 100) + '%' }"></div>
                                </div>
                            </div>
                            <div class="text-right flex-shrink-0">
                                <p class="text-sm font-black text-gray-900">{{ ruta.total }}</p>
                                <p class="text-[10px] text-gray-400">pasajes</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tabla próximos viajes -->
            <div class="card lg:col-span-2">
                <div class="card-header">
                    <h3 class="card-title">Viajes de hoy</h3>
                    <router-link :to="{ name: 'viajes' }" class="text-xs text-orange-600 font-bold hover:underline">
                        Ver todos →
                    </router-link>
                </div>
                <div v-if="cargando" class="p-5 space-y-3">
                    <div v-for="i in 3" :key="i"
                        class="h-14 bg-gray-50 border border-gray-100 rounded-xl animate-pulse"></div>
                </div>
                <div v-else class="table-wrapper">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Ruta</th>
                                <th class="text-center">Salida</th>
                                <th>Ocupación</th>
                                <th>Estado</th>
                                <th class="text-right">Acción</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="!viajesHoy.length">
                                <td colspan="5" class="text-center py-12 text-gray-400 italic">
                                    No hay viajes programados para hoy
                                </td>
                            </tr>
                            <tr v-for="v in viajesHoy" :key="v.id">
                                <td>
                                    <p class="font-bold text-gray-900 text-sm">{{ v.ruta_descripcion }}</p>
                                    <p class="text-xs text-gray-400">{{ v.vehiculo_placa }} · {{ v.conductor_nombre }}
                                    </p>
                                </td>
                                <td class="text-center">
                                    <span
                                        class="font-mono font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded-lg text-xs">
                                        {{ formatearHora(v.fecha_salida) }}
                                    </span>
                                </td>
                                <td>
                                    <div class="flex items-center gap-2">
                                        <div class="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                            <div class="h-full rounded-full transition-all"
                                                :class="pctOcupacion(v) >= 80 ? 'bg-emerald-500' : pctOcupacion(v) >= 50 ? 'bg-amber-400' : 'bg-red-400'"
                                                :style="{ width: pctOcupacion(v) + '%' }"></div>
                                        </div>
                                        <span class="text-xs font-bold text-gray-500 whitespace-nowrap">
                                            {{ v.asientos_ocupados }}/{{ (v.asientos_ocupados || 0) +
                                                (v.asientos_disponibles ||
                                                    0) }}
                                        </span>
                                    </div>
                                </td>
                                <td>
                                    <span :class="claseEstado(v.estado)">{{ etiquetaEstado(v.estado) }}</span>
                                </td>
                                <td class="text-right">
                                    <router-link :to="{ name: 'vender-pasaje' }"
                                        class="btn-primary text-[11px] uppercase">
                                        Vender
                                    </router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { useCajaStore }  from '@/modules/caja/stores/caja.store'
import { useFlotaStore } from '@/modules/flota/stores/flota.store'
import { useAuthStore }  from '@/modules/auth/stores/auth.store'
import Swal from 'sweetalert2'

const cajaStore  = useCajaStore()
const flotaStore = useFlotaStore()
const authStore  = useAuthStore()

const datos = ref({})
const cargando = ref(false)

const hoyFormateado = new Date().toLocaleDateString('es-PE', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
})
const hoy = new Date().toISOString().slice(0, 10)

// ── Computed ──────────────────────────────────────────────
const cajaCerrada = computed(() => !cajaStore.cajaAbierta)

const viajesHoy = computed(() =>
    flotaStore.viajes.filter(v => v.fecha_salida?.startsWith(hoy)).slice(0, 6)
)

const estadosViaje = [
    { clave: 'programado', etiqueta: 'Programado', bg: 'bg-gray-50 border-gray-200', texto: 'text-gray-500' },
    { clave: 'en_curso', etiqueta: 'En Ruta', bg: 'bg-emerald-50 border-emerald-200', texto: 'text-emerald-600' },
    { clave: 'completado', etiqueta: 'Completado', bg: 'bg-blue-50 border-blue-200', texto: 'text-blue-600' },
    { clave: 'cancelado', etiqueta: 'Cancelado', bg: 'bg-red-50 border-red-200', texto: 'text-red-500' },
]

// ── Helpers ───────────────────────────────────────────────
function formatearMonto(val) {
    return (parseFloat(val) || 0).toLocaleString('es-PE', {
        minimumFractionDigits: 2, maximumFractionDigits: 2,
    })
}
function formatearHora(fecha) {
    if (!fecha) return '—'
    return new Date(fecha).toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
}
function pctOcupacion(v) {
    const total = (v.asientos_ocupados || 0) + (v.asientos_disponibles || 0)
    return total > 0 ? Math.round((v.asientos_ocupados / total) * 100) : 0
}
function claseEstado(estado) {
    return {
        programado: 'badge badge-gray',
        en_curso: 'badge badge-green',
        completado: 'badge badge-blue',
        cancelado: 'badge badge-red',
    }[estado] || 'badge badge-gray'
}
function etiquetaEstado(estado) {
    return { programado: 'Programado', en_curso: 'En ruta', completado: 'Completado', cancelado: 'Cancelado' }[estado] || estado
}
function emojiPago(mp) {
    return { cash: '💵', yape: '📱', plin: '📲', card: '💳' }[mp] || '💰'
}
function etiquetaPago(mp) {
    return { cash: 'Efectivo', yape: 'Yape', plin: 'Plin', card: 'Tarjeta' }[mp] || mp
}

// ── Cargar datos ──────────────────────────────────────────
async function cargarDatos() {
    cargando.value = true
    try {
        // Dashboard del día (desde y hasta = hoy)
        const [{ data: dashboard }] = await Promise.all([
            api.get('/reportes/dashboard/', { params: { desde: hoy, hasta: hoy } }),
            flotaStore.cargarViajes({ fecha_salida__date: hoy }),
            cajaStore.cargarMiSesion(),
        ])
        datos.value = dashboard
        if (cajaStore.cajaAbierta) cajaStore.cargarMovimientos()
    } catch (e) {
        console.error('Error dashboard:', e)
    } finally {
        cargando.value = false
    }
}

onMounted(async () => {
    await cargarDatos()
    if (history.state?.bienvenida) {
        await Swal.fire({
            icon: 'success',
            title: `¡Bienvenido, ${authStore.nombre_completo}!`,
            text: 'Sesión iniciada correctamente.',
            timer: 2500,
            timerProgressBar: true,
            showConfirmButton: false,
        })
    }
})
</script>