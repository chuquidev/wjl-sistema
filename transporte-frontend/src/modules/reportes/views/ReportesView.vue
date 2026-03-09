<template>
    <div class="space-y-6">

        <!-- Encabezado -->
        <div class="page-header">
            <div>
                <h1 class="page-title">Reportes</h1>
                <p class="page-subtitle">Dashboard general y análisis del negocio</p>
            </div>
            <div class="flex items-center gap-2">
                <button @click="exportar('excel')" :disabled="exportando" class="btn-secondary">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Excel
                </button>
                <button @click="exportar('pdf')" :disabled="exportando" class="btn-secondary">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                    </svg>
                    PDF
                </button>
                <button @click="cargarDatos" :disabled="cargando" class="btn-primary">
                    <svg :class="['w-4 h-4', cargando ? 'animate-spin' : '']"
                        fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Actualizar
                </button>
            </div>
        </div>

        <!-- Filtros de período -->
        <div class="flex flex-wrap items-center gap-3 p-4 bg-white rounded-2xl border border-gray-100 shadow-sm">
            <div class="flex gap-1 p-1 bg-gray-100 rounded-xl">
                <button v-for="p in periodos" :key="p.clave" @click="selectPeriodo(p.clave)"
                    :class="[
                        'px-3 py-1.5 rounded-lg text-xs font-bold transition-all',
                        periodo === p.clave ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'
                    ]">
                    {{ p.etiqueta }}
                </button>
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-500">
                <span>Desde</span>
                <input v-model="fechaDesde" type="date" class="form-input py-1.5 text-sm w-38" @change="cargarDatos" />
                <span>hasta</span>
                <input v-model="fechaHasta" type="date" class="form-input py-1.5 text-sm w-38" @change="cargarDatos" />
            </div>
        </div>

        <!-- ── KPIs principales ──────────────────────────────── -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div v-for="kpi in kpis" :key="kpi.clave"
                class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 relative overflow-hidden">
                <div :class="['absolute top-0 right-0 w-16 h-16 rounded-bl-3xl opacity-10', kpi.bg]"></div>
                <div :class="['w-10 h-10 rounded-xl flex items-center justify-center mb-3', kpi.bg]">
                    <component :is="'svg'" class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="kpi.icono" />
                    </component>
                </div>
                <p class="text-xs font-bold uppercase tracking-wide text-gray-400 mb-1">{{ kpi.etiqueta }}</p>
                <p v-if="cargando" class="h-8 bg-gray-100 rounded-lg animate-pulse w-24"></p>
                <p v-else :class="['text-2xl font-black', kpi.color]">{{ kpi.valor }}</p>
                <p v-if="kpi.subtexto" class="text-xs text-gray-400 mt-1">{{ kpi.subtexto }}</p>
            </div>
        </div>

        <!-- ── Gráficas ──────────────────────────────────────── -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">

            <!-- Ventas por día -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Ventas diarias</h3>
                    <span class="text-xs text-gray-400">Pasajes + Paquetes + Encomiendas</span>
                </div>
                <div class="card-body">
                    <div v-if="cargando" class="h-48 bg-gray-50 rounded-xl animate-pulse"></div>
                    <div v-else-if="!datos.ventas_diarias?.length"
                        class="h-48 flex items-center justify-center text-gray-400 italic text-sm">
                        Sin datos en el período
                    </div>
                    <div v-else class="h-48 relative">
                        <svg class="w-full h-full" :viewBox="`0 0 ${chartW} ${chartH}`" preserveAspectRatio="none">
                            <defs>
                                <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stop-color="#3b82f6"/>
                                    <stop offset="100%" stop-color="#6366f1"/>
                                </linearGradient>
                            </defs>
                            <line v-for="g in guias" :key="g.y"
                                :x1="paddingL" :y1="g.y" :x2="chartW - paddingR" :y2="g.y"
                                stroke="#f3f4f6" stroke-width="1"/>
                            <g v-for="(b, i) in barsVentas" :key="i">
                                <rect :x="b.x" :y="b.y" :width="b.w" :height="b.h"
                                    fill="url(#barGrad)" rx="3" class="transition-all duration-300"/>
                                <text :x="b.x + b.w/2" :y="chartH - 5"
                                    text-anchor="middle" font-size="8" fill="#9ca3af">
                                    {{ b.label }}
                                </text>
                            </g>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Métodos de pago -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Métodos de pago</h3>
                </div>
                <div class="card-body">
                    <div v-if="cargando" class="h-48 bg-gray-50 rounded-xl animate-pulse"></div>
                    <div v-else-if="!datos.metodos_pago?.length"
                        class="h-48 flex items-center justify-center text-gray-400 italic text-sm">
                        Sin datos en el período
                    </div>
                    <div v-else class="space-y-3">
                        <div v-for="mp in datos.metodos_pago" :key="mp.metodo"
                            class="flex items-center gap-3">
                            <span class="text-lg w-6">{{ emojiPago(mp.metodo) }}</span>
                            <div class="flex-1">
                                <div class="flex justify-between text-xs font-bold text-gray-700 mb-1">
                                    <span>{{ etiquetaPago(mp.metodo) }}</span>
                                    <span>{{ mp.porcentaje }}%</span>
                                </div>
                                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                                    <div class="h-full rounded-full transition-all duration-500"
                                        :class="colorBarraPago(mp.metodo)"
                                        :style="{ width: mp.porcentaje + '%' }">
                                    </div>
                                </div>
                            </div>
                            <span class="text-xs font-black text-gray-900 w-20 text-right">
                                S/. {{ formatearMonto(mp.total) }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Rutas más vendidas -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Rutas más vendidas</h3>
                </div>
                <div class="card-body">
                    <div v-if="cargando" class="space-y-3">
                        <div v-for="i in 4" :key="i" class="h-8 bg-gray-50 rounded-lg animate-pulse"></div>
                    </div>
                    <div v-else-if="!datos.rutas_top?.length"
                        class="text-center py-10 text-gray-400 italic text-sm">
                        Sin datos en el período
                    </div>
                    <div v-else class="space-y-3">
                        <div v-for="(ruta, i) in datos.rutas_top" :key="ruta.ruta"
                            class="flex items-center gap-3">
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
                                        :style="{ width: (ruta.total / datos.rutas_top[0].total * 100) + '%' }">
                                    </div>
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

            <!-- Estado de viajes -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Estado de viajes</h3>
                </div>
                <div class="card-body">
                    <div v-if="cargando" class="h-40 bg-gray-50 rounded-xl animate-pulse"></div>
                    <div v-else-if="!datos.viajes_estado" class="text-center py-10 text-gray-400 italic text-sm">
                        Sin datos en el período
                    </div>
                    <div v-else>
                        <div class="flex items-center gap-6">
                            <svg class="w-32 h-32 flex-shrink-0" viewBox="0 0 100 100">
                                <circle cx="50" cy="50" r="40" fill="none" stroke="#f3f4f6" stroke-width="18"/>
                                <circle v-for="(seg, i) in donutSegments" :key="i"
                                    cx="50" cy="50" r="40" fill="none"
                                    :stroke="seg.color" stroke-width="18"
                                    :stroke-dasharray="`${seg.dash} ${seg.gap}`"
                                    :stroke-dashoffset="seg.offset"
                                    transform="rotate(-90 50 50)"/>
                                <text x="50" y="46" text-anchor="middle" font-size="14" font-weight="900" fill="#111827">
                                    {{ totalViajes }}
                                </text>
                                <text x="50" y="58" text-anchor="middle" font-size="7" fill="#9ca3af">viajes</text>
                            </svg>
                            <div class="space-y-2 flex-1">
                                <div v-for="est in estadosViaje" :key="est.clave"
                                    class="flex items-center justify-between">
                                    <div class="flex items-center gap-2">
                                        <span class="w-2.5 h-2.5 rounded-full" :style="{ background: est.color }"></span>
                                        <span class="text-xs font-medium text-gray-600">{{ est.etiqueta }}</span>
                                    </div>
                                    <span class="text-xs font-black text-gray-900">
                                        {{ datos.viajes_estado?.[est.clave] || 0 }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ── Encomiendas y Caja ────────────────────────────── -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">

            <!-- Resumen encomiendas -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Encomiendas</h3>
                </div>
                <div class="card-body grid grid-cols-2 gap-3">
                    <div v-for="enc in encomiendаsStats" :key="enc.clave"
                        :class="['rounded-xl p-4 text-center', enc.bg]">
                        <p class="text-2xl font-black" :class="enc.color">
                            {{ cargando ? '—' : enc.clave === 'ingresos'
                                ? 'S/. ' + formatearMonto(datos.encomiendas?.ingresos)
                                : (datos.encomiendas?.[enc.clave] ?? 0)
                            }}
                        </p>
                        <p class="text-[10px] font-bold uppercase tracking-wide text-gray-400 mt-1">
                            {{ enc.etiqueta }}
                        </p>
                    </div>
                </div>
            </div>

            <!-- Resumen caja -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Resumen de caja</h3>
                    <span class="text-xs text-gray-400">Incluye pasajes, paquetes y encomiendas</span>
                </div>
                <div class="card-body space-y-3">
                    <div v-if="cargando" class="space-y-3">
                        <div v-for="i in 3" :key="i" class="h-10 bg-gray-50 rounded-xl animate-pulse"></div>
                    </div>
                    <template v-else>
                        <div class="flex justify-between items-center p-3 bg-emerald-50 rounded-xl">
                            <span class="text-sm font-bold text-emerald-700">Total ingresos</span>
                            <span class="font-black text-emerald-700">
                                S/. {{ formatearMonto(datos.caja?.total_ingresos) }}
                            </span>
                        </div>
                        <div class="flex justify-between items-center p-3 bg-red-50 rounded-xl">
                            <span class="text-sm font-bold text-red-600">Total egresos</span>
                            <span class="font-black text-red-600">
                                S/. {{ formatearMonto(datos.caja?.total_egresos) }}
                            </span>
                        </div>
                        <div class="flex justify-between items-center p-3 bg-blue-50 rounded-xl">
                            <span class="text-sm font-bold text-blue-700">Neto</span>
                            <span class="font-black text-blue-700 text-lg">
                                S/. {{ formatearMonto((datos.caja?.total_ingresos || 0) - (datos.caja?.total_egresos || 0)) }}
                            </span>
                        </div>
                        <div class="flex justify-between items-center p-3 bg-gray-50 rounded-xl">
                            <span class="text-sm font-medium text-gray-600">Sesiones de caja</span>
                            <span class="font-black text-gray-900">
                                {{ datos.caja?.total_sesiones || 0 }}
                            </span>
                        </div>
                    </template>
                </div>
            </div>
        </div>

        <!-- ── Tabla detalle ventas ───────────────────────────── -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Detalle de ventas por día</h3>
            </div>
            <div class="table-wrapper">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th class="text-right">Pasajes</th>
                            <th class="text-right">Ing. Pasajes</th>
                            <th class="text-right">Ing. Paquetes</th>
                            <th class="text-right">Encomiendas</th>
                            <th class="text-right">Ing. Encomiendas</th>
                            <th class="text-right">Total del día</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="cargando">
                            <td colspan="7">
                                <div class="flex justify-center py-8">
                                    <svg class="w-6 h-6 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                                    </svg>
                                </div>
                            </td>
                        </tr>
                        <tr v-else-if="!datos.ventas_diarias?.length">
                            <td colspan="7" class="text-center py-10 text-gray-400 italic">
                                Sin datos en el período seleccionado
                            </td>
                        </tr>
                        <tr v-for="d in datos.ventas_diarias" :key="d.fecha">
                            <td class="font-medium text-gray-900">{{ formatearFecha(d.fecha) }}</td>
                            <td class="text-right font-bold text-blue-600">{{ d.pasajes }}</td>
                            <td class="text-right font-bold text-gray-900">S/. {{ formatearMonto(d.ingresos_pasajes) }}</td>
                            <td class="text-right font-bold text-violet-600">S/. {{ formatearMonto(d.ingresos_paquetes) }}</td>
                            <td class="text-right font-bold text-orange-600">{{ d.encomiendas }}</td>
                            <td class="text-right font-bold text-gray-900">S/. {{ formatearMonto(d.ingresos_encomiendas) }}</td>
                            <td class="text-right font-black text-emerald-600">
                                S/. {{ formatearMonto(
                                    (d.ingresos_pasajes || 0) +
                                    (d.ingresos_paquetes || 0) +
                                    (d.ingresos_encomiendas || 0)
                                ) }}
                            </td>
                        </tr>
                        <!-- Total -->
                        <tr v-if="datos.ventas_diarias?.length" class="bg-gray-50 font-black">
                            <td class="text-gray-900">TOTAL</td>
                            <td class="text-right text-blue-600">{{ totales.pasajes }}</td>
                            <td class="text-right text-gray-900">S/. {{ formatearMonto(totales.ingresosPasajes) }}</td>
                            <td class="text-right text-violet-600">S/. {{ formatearMonto(totales.ingresosPaquetes) }}</td>
                            <td class="text-right text-orange-600">{{ totales.encomiendas }}</td>
                            <td class="text-right text-gray-900">S/. {{ formatearMonto(totales.ingresosEncomiendas) }}</td>
                            <td class="text-right text-emerald-600">S/. {{ formatearMonto(totales.total) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reportesService } from '../services/reportes.service'

// ── Estado ────────────────────────────────────────────────
const cargando   = ref(false)
const exportando = ref(false)
const datos      = ref({})
const periodo    = ref('mes')

const hoy = new Date()
const fechaHasta = ref(hoy.toISOString().slice(0, 10))
const fechaDesde = ref(new Date(hoy.getFullYear(), hoy.getMonth(), 1).toISOString().slice(0, 10))

const periodos = [
    { clave: 'hoy',    etiqueta: 'Hoy' },
    { clave: 'semana', etiqueta: 'Semana' },
    { clave: 'mes',    etiqueta: 'Mes' },
    { clave: 'anio',   etiqueta: 'Año' },
]

// ── Chart config ──────────────────────────────────────────
const chartW   = 400
const chartH   = 160
const paddingL = 10
const paddingR = 10
const paddingT = 10
const paddingB = 20

// ── Helpers ───────────────────────────────────────────────
function formatearMonto(val) {
    return (parseFloat(val) || 0).toLocaleString('es-PE', {
        minimumFractionDigits: 2, maximumFractionDigits: 2,
    })
}
function formatearFecha(fecha) {
    if (!fecha) return '—'
    return new Date(fecha + 'T00:00:00').toLocaleDateString('es-PE', {
        weekday: 'short', day: '2-digit', month: '2-digit',
    })
}
function formatearNum(val) {
    return (parseInt(val) || 0).toLocaleString('es-PE')
}
function emojiPago(mp) {
    return { cash: '💵', yape: '📱', plin: '📲', card: '💳' }[mp] || '💰'
}
function etiquetaPago(mp) {
    return { cash: 'Efectivo', yape: 'Yape', plin: 'Plin', card: 'Tarjeta' }[mp] || mp
}
function colorBarraPago(mp) {
    return { cash: 'bg-emerald-500', yape: 'bg-purple-500', plin: 'bg-blue-500', card: 'bg-orange-500' }[mp] || 'bg-gray-400'
}

// helper para sumar total de una fila del día
function totalDia(d) {
    return (parseFloat(d.ingresos_pasajes) || 0)
        + (parseFloat(d.ingresos_paquetes) || 0)
        + (parseFloat(d.ingresos_encomiendas) || 0)
}

// ── Período ───────────────────────────────────────────────
function selectPeriodo(p) {
    periodo.value = p
    const hoyDate = new Date()
    fechaHasta.value = hoyDate.toISOString().slice(0, 10)

    if (p === 'hoy') {
        fechaDesde.value = fechaHasta.value
    } else if (p === 'semana') {
        const lunes = new Date(hoyDate)
        lunes.setDate(hoyDate.getDate() - hoyDate.getDay() + 1)
        fechaDesde.value = lunes.toISOString().slice(0, 10)
    } else if (p === 'mes') {
        fechaDesde.value = new Date(hoyDate.getFullYear(), hoyDate.getMonth(), 1).toISOString().slice(0, 10)
    } else if (p === 'anio') {
        fechaDesde.value = new Date(hoyDate.getFullYear(), 0, 1).toISOString().slice(0, 10)
    }
    cargarDatos()
}

// ── KPIs ──────────────────────────────────────────────────
const kpis = computed(() => [
    {
        clave:    'ventas',
        etiqueta: 'Total ventas',
        valor:    `S/. ${formatearMonto(datos.value.total_ventas)}`,
        subtexto: `${datos.value.total_pasajes || 0} pasajes`,
        bg:       'bg-blue-500',
        color:    'text-blue-600',
        icono:    'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    },
    {
        clave:    'encomiendas',
        etiqueta: 'Encomiendas',
        valor:    formatearNum(datos.value.encomiendas?.total),
        subtexto: `S/. ${formatearMonto(datos.value.encomiendas?.ingresos)}`,
        bg:       'bg-orange-500',
        color:    'text-orange-600',
        icono:    'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4',
    },
    {
        clave:    'viajes',
        etiqueta: 'Viajes',
        valor:    formatearNum(datos.value.total_viajes),
        subtexto: `${datos.value.viajes_estado?.completado || 0} completados`,
        bg:       'bg-emerald-500',
        color:    'text-emerald-600',
        icono:    'M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0zM13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2h8zm0 0l2-5h3l2 5m-7 0h7',
    },
    {
        clave:    'neto',
        etiqueta: 'Neto caja',
        valor:    `S/. ${formatearMonto((datos.value.caja?.total_ingresos || 0) - (datos.value.caja?.total_egresos || 0))}`,
        subtexto: `Egresos: S/. ${formatearMonto(datos.value.caja?.total_egresos)}`,
        bg:       'bg-purple-500',
        color:    'text-purple-600',
        icono:    'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z',
    },
])

// ── Totales tabla ─────────────────────────────────────────
const totales = computed(() => {
    const filas = datos.value.ventas_diarias || []
    return filas.reduce((acc, d) => {
        acc.pasajes             += d.pasajes || 0
        acc.ingresosPasajes     += parseFloat(d.ingresos_pasajes || 0)
        acc.ingresosPaquetes    += parseFloat(d.ingresos_paquetes || 0)  // ← nuevo
        acc.encomiendas         += d.encomiendas || 0
        acc.ingresosEncomiendas += parseFloat(d.ingresos_encomiendas || 0)
        acc.total               += totalDia(d)
        return acc
    }, { pasajes: 0, ingresosPasajes: 0, ingresosPaquetes: 0, encomiendas: 0, ingresosEncomiendas: 0, total: 0 })
})

// ── Chart barras ventas ───────────────────────────────────
const guias = computed(() => {
    const filas = datos.value.ventas_diarias || []
    if (!filas.length) return []
    return [0.25, 0.5, 0.75, 1].map(f => ({
        y: paddingT + (chartH - paddingT - paddingB) * (1 - f),
    }))
})

const barsVentas = computed(() => {
    const filas = datos.value.ventas_diarias || []
    if (!filas.length) return []
    // ← usa totalDia que incluye paquetes
    const maxVal = Math.max(...filas.map(d => totalDia(d))) || 1
    const innerW = chartW - paddingL - paddingR
    const innerH = chartH - paddingT - paddingB
    const barW   = Math.max(4, (innerW / filas.length) * 0.6)
    const gap    = innerW / filas.length

    return filas.map((d, i) => {
        const val   = totalDia(d)
        const h     = Math.max(2, (val / maxVal) * innerH)
        const x     = paddingL + i * gap + (gap - barW) / 2
        const y     = paddingT + innerH - h
        const label = d.fecha?.slice(8)
        return { x, y, w: barW, h, label }
    })
})

// ── Donut viajes ──────────────────────────────────────────
const estadosViaje = [
    { clave: 'programado', etiqueta: 'Programado', color: '#9ca3af' },
    { clave: 'en_curso',   etiqueta: 'En curso',   color: '#10b981' },
    { clave: 'completado', etiqueta: 'Completado', color: '#3b82f6' },
    { clave: 'cancelado',  etiqueta: 'Cancelado',  color: '#ef4444' },
]

const totalViajes = computed(() => {
    const v = datos.value.viajes_estado || {}
    return Object.values(v).reduce((a, b) => a + (b || 0), 0)
})

const donutSegments = computed(() => {
    const total  = totalViajes.value || 1
    const circum = 2 * Math.PI * 40
    let offset   = 0
    return estadosViaje.map(est => {
        const val  = datos.value.viajes_estado?.[est.clave] || 0
        const dash = (val / total) * circum
        const gap  = circum - dash
        const seg  = { color: est.color, dash, gap, offset }
        offset    += dash
        return seg
    })
})

// ── Encomiendas stats ─────────────────────────────────────
const encomiendаsStats = [
    { clave: 'total',       etiqueta: 'Total',        bg: 'bg-gray-50',    color: 'text-gray-900' },
    { clave: 'en_transito', etiqueta: 'En tránsito',  bg: 'bg-blue-50',    color: 'text-blue-600' },
    { clave: 'entregado',   etiqueta: 'Entregadas',   bg: 'bg-emerald-50', color: 'text-emerald-600' },
    { clave: 'ingresos',    etiqueta: 'Ingresos S/.', bg: 'bg-orange-50',  color: 'text-orange-600' },
]

// ── Cargar datos ──────────────────────────────────────────
async function cargarDatos() {
    cargando.value = true
    try {
        const params = { desde: fechaDesde.value, hasta: fechaHasta.value }
        const { data } = await reportesService.getDashboard(params)
        datos.value = data
    } catch (e) {
        console.error('Error reportes:', e.response?.data)
    } finally {
        cargando.value = false
    }
}

// ── Exportar ──────────────────────────────────────────────
async function exportar(tipo) {
    exportando.value = true
    try {
        const params    = { desde: fechaDesde.value, hasta: fechaHasta.value }
        const { data }  = tipo === 'pdf'
            ? await reportesService.exportarPDF(params)
            : await reportesService.exportarExcel(params)

        const ext  = tipo === 'pdf' ? 'pdf' : 'xlsx'
        const mime = tipo === 'pdf'
            ? 'application/pdf'
            : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        const blob = new Blob([data], { type: mime })
        const url  = URL.createObjectURL(blob)
        const a    = document.createElement('a')
        a.href     = url
        a.download = `reporte_${fechaDesde.value}_${fechaHasta.value}.${ext}`
        a.click()
        URL.revokeObjectURL(url)
    } catch {
        alert('No se pudo exportar. Verifica que el backend tenga los endpoints de exportación.')
    } finally {
        exportando.value = false
    }
}

onMounted(() => {
    cargarDatos()
})
</script>