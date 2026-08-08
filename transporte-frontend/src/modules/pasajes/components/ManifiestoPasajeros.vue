<template>
    <div class="space-y-5">

        <!-- Selector de viaje -->
        <div class="card">
            <div class="card-body">
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label class="form-label">Fecha</label>
                        <input v-model="filtroFecha" type="date" class="form-input" @change="cargarViajes" />
                    </div>
                    <div class="sm:col-span-2">
                        <label class="form-label">Viaje</label>
                        <select v-model="viajeId" class="form-input" @change="cargarManifiesto">
                            <option value="">-- Selecciona un viaje --</option>
                            <option v-for="v in viajes" :key="v.id" :value="v.id">
                                {{ v.ruta_descripcion }} | {{ formatFecha(v.fecha_salida) }} | {{ v.vehiculo_placa }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <!-- Loading -->
        <div v-if="cargando" class="flex justify-center py-16">
            <svg class="w-8 h-8 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
        </div>

        <!-- Estado vacio -->
        <div v-else-if="!viajeId" class="text-center py-20 text-gray-400">
            <svg class="w-14 h-14 mx-auto mb-4 text-gray-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2h8zm0 0l2-5h3l2 5m-7 0h7" />
            </svg>
            <p class="font-semibold text-gray-500">Selecciona una fecha y un viaje</p>
            <p class="text-sm mt-1">para ver el manifiesto completo</p>
        </div>

        <!-- Manifiesto -->
        <template v-else-if="viaje">

            <!-- Cabecera acciones -->
            <div class="flex flex-wrap items-center justify-between gap-3">
                <div>
                    <h2 class="text-lg font-black text-gray-900">Manifiesto del viaje</h2>
                    <p class="text-sm text-gray-500">
                        {{ viaje.ruta_descripcion }} &mdash; {{ formatFecha(viaje.fecha_salida) }}
                        &middot; {{ viaje.vehiculo_placa }}
                    </p>
                </div>
                <div class="flex gap-2">
                    <button @click="exportarExcel" class="btn-secondary">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        Exportar Excel
                    </button>
                    <button @click="imprimir" class="btn-primary">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                        </svg>
                        Imprimir
                    </button>
                </div>
            </div>

            <!-- KPIs -->
            <div class="grid grid-cols-2 lg:grid-cols-5 gap-3">
                <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 text-center">
                    <p class="text-2xl font-black text-gray-800">{{ viaje.capacidad || 18 }}</p>
                    <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wide mt-1">Capacidad</p>
                </div>
                <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 text-center">
                    <p class="text-2xl font-black text-blue-600">{{ pasajesActivos.length }}</p>
                    <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wide mt-1">Pasajeros</p>
                </div>
                <div class="bg-white rounded-2xl border border-emerald-100 shadow-sm p-4 text-center">
                    <p class="text-2xl font-black text-emerald-600">{{ totalEmbarcados }}</p>
                    <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wide mt-1">Embarcados</p>
                </div>
                <div class="bg-white rounded-2xl border border-orange-100 shadow-sm p-4 text-center">
                    <p class="text-2xl font-black text-orange-600">{{ encomiendas.length }}</p>
                    <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wide mt-1">Encomiendas</p>
                </div>
                <div class="bg-white rounded-2xl border border-emerald-100 shadow-sm p-4 text-center">
                    <p class="text-lg font-black text-emerald-700">S/. {{ totalRecaudado.toFixed(2) }}</p>
                    <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wide mt-1">Total</p>
                </div>
            </div>

            <!-- Area imprimible -->
            <div ref="printRef" id="print-content">

                <!-- Encabezado solo visible en impresion -->
                <div class="print-only mb-5">
                    <div class="flex justify-between items-start mb-3">
                        <div>
                            <p class="text-base font-black text-blue-900">TURISMO WJL E.I.R.L.</p>
                            <p class="text-xs text-gray-500">Uniendo Familias &middot; +51 999 713 436</p>
                        </div>
                        <div class="text-right">
                            <p class="text-base font-black text-gray-900 uppercase">Manifiesto de Pasajeros</p>
                            <p class="text-xs text-gray-500">Emitido: {{ ahora }}</p>
                        </div>
                    </div>
                    <div class="flex flex-wrap gap-4 text-xs bg-gray-50 rounded-lg p-3 border border-gray-200">
                        <span><strong>Ruta:</strong> {{ viaje.ruta_descripcion }}</span>
                        <span><strong>Salida:</strong> {{ formatFecha(viaje.fecha_salida) }}</span>
                        <span><strong>Vehiculo:</strong> {{ viaje.vehiculo_placa }}</span>
                        <span v-if="viaje.conductor_nombre"><strong>Conductor:</strong> {{ viaje.conductor_nombre
                            }}</span>
                        <span><strong>Pasajeros:</strong> {{ pasajesActivos.length }} / {{ viaje.capacidad || 18
                            }}</span>
                        <span><strong>Encomiendas:</strong> {{ encomiendas.length }}</span>
                    </div>
                </div>

                <!-- TABLA PASAJEROS -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h3 class="card-title">
                            Pasajeros
                            <span class="ml-2 text-sm font-normal text-gray-400">({{ pasajesActivos.length }} activos{{
                                totalAnulados ? `, ${totalAnulados} anulado(s)` : '' }})</span>
                        </h3>
                        <label class="no-print flex items-center gap-2 cursor-pointer">
                            <input v-model="mostrarAnulados" type="checkbox" class="rounded" />
                            <span class="text-xs text-gray-500">Mostrar anulados</span>
                        </label>
                    </div>
                    <div class="table-wrapper">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th class="text-center w-8">N&deg;</th>
                                    <th class="text-center w-14">Asiento</th>
                                    <th>Pasajero</th>
                                    <th>DNI</th>
                                    <th>Tel&eacute;fono</th>
                                    <th>Pago</th>
                                    <th class="text-right">Precio</th>
                                    <th class="text-right">Paquetes</th>
                                    <th class="text-center">Estado</th>
                                    <th class="text-center no-print">Embarcar</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!pasajerosFiltrados.length">
                                    <td colspan="10" class="text-center py-10 text-gray-400 italic">
                                        Sin pasajeros registrados en este viaje
                                    </td>
                                </tr>
                                <tr v-for="(p, i) in pasajerosFiltrados" :key="p.id"
                                    :class="{ 'opacity-50 bg-gray-50': p.estado === 'anulado' }">
                                    <td class="text-center text-xs font-bold text-gray-400">{{ i + 1 }}</td>
                                    <td class="text-center">
                                        <span class="font-black text-blue-600 bg-blue-50 px-2 py-1 rounded-lg text-sm">
                                            {{ p.asiento }}
                                        </span>
                                    </td>
                                    <td>
                                        <p class="font-semibold text-gray-900 text-sm">{{ p.pasajero_nombre }}</p>
                                    </td>
                                    <td class="font-mono text-xs text-gray-600">{{ p.pasajero_dni }}</td>
                                    <td class="text-xs text-gray-500 font-mono">{{ p.pasajero_telefono || '&mdash;' }}
                                    </td>
                                    <td class="text-xs">{{ metodoLabel(p.metodo_pago) }}</td>
                                    <td class="text-right font-black text-gray-900 text-sm">S/. {{ p.precio }}</td>
                                    <td class="text-right">
                                        <span v-if="p.tiene_paquetes"
                                            class="text-xs font-bold text-orange-600 bg-orange-50 px-2 py-0.5 rounded-lg whitespace-nowrap">
                                            +S/. {{ Number(p.total_paquetes || 0).toFixed(2) }}
                                        </span>
                                        <span v-else class="text-xs text-gray-300">&mdash;</span>
                                    </td>
                                    <td class="text-center">
                                        <span :class="claseEstadoPasaje(p.estado)">
                                            {{ etiquetaEstadoPasaje(p.estado) }}
                                        </span>
                                    </td>
                                    <td class="text-center no-print">
                                        <button v-if="p.estado === 'emitido'" @click="embarcar(p)"
                                            :disabled="embarcando === p.id"
                                            class="inline-flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 px-2 py-1 rounded-lg transition-colors disabled:opacity-50">
                                            <svg v-if="embarcando === p.id" class="w-3 h-3 animate-spin" fill="none"
                                                viewBox="0 0 24 24">
                                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                    stroke-width="4" />
                                                <path class="opacity-75" fill="currentColor"
                                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                            </svg>
                                            <svg v-else class="w-3 h-3" fill="none" viewBox="0 0 24 24"
                                                stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                                                    d="M5 13l4 4L19 7" />
                                            </svg>
                                            Embarcar
                                        </button>
                                        <span v-else-if="p.estado === 'embarcado'"
                                            class="text-xs font-black text-emerald-600">
                                            &#10003; OK
                                        </span>
                                        <span v-else class="text-xs text-gray-300">&mdash;</span>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot v-if="pasajesActivos.length">
                                <tr class="bg-gray-50">
                                    <td colspan="6" class="text-right text-xs font-bold text-gray-500 py-2 px-4">
                                        Subtotal pasajes:
                                    </td>
                                    <td class="text-right text-sm font-black text-gray-900 py-2 px-4">
                                        S/. {{ totalPasajes.toFixed(2) }}
                                    </td>
                                    <td class="text-right text-sm font-black text-orange-600 py-2 px-4">
                                        +S/. {{ totalPaquetesPasajes.toFixed(2) }}
                                    </td>
                                    <td colspan="2"></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>

                <!-- TABLA ENCOMIENDAS -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h3 class="card-title">
                            Encomiendas
                            <span class="ml-2 text-sm font-normal text-gray-400">({{ encomiendas.length }})</span>
                        </h3>
                    </div>
                    <div class="table-wrapper">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th class="text-center w-8">N&deg;</th>
                                    <th>C&oacute;digo</th>
                                    <th>Remitente</th>
                                    <th>Destinatario</th>
                                    <th>Descripci&oacute;n</th>
                                    <th class="text-center">Peso</th>
                                    <th>Pago</th>
                                    <th class="text-right">Precio</th>
                                    <th class="text-center">Estado</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="!encomiendas.length">
                                    <td colspan="9" class="text-center py-10 text-gray-400 italic">
                                        Sin encomiendas asignadas a este viaje
                                    </td>
                                </tr>
                                <tr v-for="(enc, i) in encomiendas" :key="enc.id">
                                    <td class="text-center text-xs font-bold text-gray-400">{{ i + 1 }}</td>
                                    <td>
                                        <span
                                            class="font-mono text-xs font-bold text-gray-700 bg-gray-100 px-2 py-1 rounded">
                                            {{ String(enc.codigo || '').slice(0, 8).toUpperCase() }}
                                        </span>
                                    </td>
                                    <td>
                                        <p class="text-sm font-semibold text-gray-900">{{ enc.remitente_nombre }}</p>
                                        <p class="text-xs text-gray-400 font-mono">{{ enc.remitente_dni }}</p>
                                    </td>
                                    <td>
                                        <p class="text-sm font-semibold text-gray-900">{{ enc.destinatario_nombre }}</p>
                                        <p class="text-xs text-gray-400 font-mono">{{ enc.destinatario_dni }}</p>
                                    </td>
                                    <td class="text-sm text-gray-600 max-w-[140px] truncate">{{ enc.descripcion }}</td>
                                    <td class="text-center text-sm font-bold text-gray-700">
                                        {{ enc.peso_kg ? enc.peso_kg + ' kg' : '&mdash;' }}
                                    </td>
                                    <td class="text-xs">{{ metodoLabel(enc.metodo_pago) }}</td>
                                    <td class="text-right font-black text-gray-900">S/. {{ enc.precio }}</td>
                                    <td class="text-center">
                                        <span :class="claseEstadoEnc(enc.estado)">
                                            {{ etiquetaEstadoEnc(enc.estado) }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot v-if="encomiendas.length">
                                <tr class="bg-gray-50">
                                    <td colspan="7" class="text-right text-xs font-bold text-gray-500 py-2 px-4">
                                        Subtotal encomiendas:
                                    </td>
                                    <td class="text-right text-sm font-black text-gray-900 py-2 px-4">
                                        S/. {{ totalEncomiendas.toFixed(2) }}
                                    </td>
                                    <td></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>

                <!-- Totales + Firma -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

                    <!-- Resumen recaudacion -->
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Resumen de recaudaci&oacute;n</h3>
                        </div>
                        <div class="card-body space-y-2">
                            <div class="flex justify-between text-sm">
                                <span class="text-gray-500">Pasajes ({{ pasajesActivos.length }})</span>
                                <span class="font-bold text-gray-900">S/. {{ totalPasajes.toFixed(2) }}</span>
                            </div>
                            <div v-if="totalPaquetesPasajes > 0" class="flex justify-between text-sm">
                                <span class="text-orange-500">Paquetes en pasajes</span>
                                <span class="font-bold text-orange-600">S/. {{ totalPaquetesPasajes.toFixed(2) }}</span>
                            </div>
                            <div class="flex justify-between text-sm">
                                <span class="text-gray-500">Encomiendas ({{ encomiendas.length }})</span>
                                <span class="font-bold text-gray-900">S/. {{ totalEncomiendas.toFixed(2) }}</span>
                            </div>
                            <div
                                class="flex justify-between items-center bg-emerald-50 border border-emerald-100 rounded-xl p-3 mt-2">
                                <span class="font-bold text-gray-700">TOTAL GENERAL</span>
                                <span class="text-xl font-black text-emerald-700">S/. {{ totalRecaudado.toFixed(2)
                                    }}</span>
                            </div>

                            <!-- Desglose por metodo de pago -->
                            <div v-if="resumenPago.length" class="pt-3 border-t border-gray-100 space-y-1">
                                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wide mb-2">Por
                                    m&eacute;todo de pago</p>
                                <div v-for="mp in resumenPago" :key="mp.clave" class="flex justify-between text-xs">
                                    <span class="text-gray-500">{{ mp.etiqueta }}</span>
                                    <span class="font-bold text-gray-700">S/. {{ mp.total.toFixed(2) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Firmas -->
                    <div class="card">
                        <div class="card-header">
                            <h3 class="card-title">Conformidad</h3>
                        </div>
                        <div class="card-body">
                            <div class="grid grid-cols-2 gap-8 mt-2">
                                <div class="text-center">
                                    <div class="h-16 border-b-2 border-dashed border-gray-300 mb-2"></div>
                                    <p class="text-xs font-bold text-gray-500 uppercase tracking-wide">Conductor</p>
                                    <p class="text-xs text-gray-400 mt-0.5">{{ viaje.conductor_nombre || 'N/A' }}</p>
                                </div>
                                <div class="text-center">
                                    <div class="h-16 border-b-2 border-dashed border-gray-300 mb-2"></div>
                                    <p class="text-xs font-bold text-gray-500 uppercase tracking-wide">Responsable</p>
                                    <p class="text-xs text-gray-400 mt-0.5">Agencia WJL</p>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
            <!-- /printRef -->

        </template>

    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { pasajesService } from '../services/pasajes.service'
import { useVueToPrint } from 'vue-to-print'

// ── Estado ─────────────────────────────────────────────────────
const filtroFecha = ref(new Date().toISOString().slice(0, 10))
const viajeId = ref('')
const viaje = ref(null)
const viajes = ref([])
const pasajes = ref([])
const encomiendas = ref([])
const cargando = ref(false)
const embarcando = ref(null)
const mostrarAnulados = ref(false)
const cargandoPasajes = ref(false)
const printRef = ref(null)

const { handlePrint } = useVueToPrint({
    content: printRef,
    documentTitle: `Manifiesto_${viaje.value?.ruta_descripcion || 'viaje'}`,
    pageStyle: `
        @page { size: A4 portrait; }
        body { font-family: Arial, sans-serif; font-size: 11px; margin: 0; padding: 0; }
        #print-content { padding: 15mm 15mm; }
        .no-print { display: none !important; }
        .print-only { display: block !important; }
        .card { box-shadow: none !important; border: 1px solid #e2e8f0 !important; break-inside: avoid; }
        .table th, .table td { font-size: 10px !important; padding: 4px 6px !important; }
        .badge { font-size: 9px !important; padding: 1px 4px !important; }
    `,
})
// ── Metodos de pago ────────────────────────────────────────────
const metodos = [
    { clave: 'cash', etiqueta: 'Efectivo' },
    { clave: 'yape', etiqueta: 'Yape' },
    { clave: 'plin', etiqueta: 'Plin' },
    { clave: 'card', etiqueta: 'Tarjeta' },
]

// ── Computed pasajeros ─────────────────────────────────────────
const pasajesActivos = computed(() => pasajes.value.filter(p => p.estado !== 'anulado'))
const totalAnulados = computed(() => pasajes.value.filter(p => p.estado === 'anulado').length)
const totalEmbarcados = computed(() => pasajes.value.filter(p => p.estado === 'embarcado').length)
const pasajerosFiltrados = computed(() =>
    mostrarAnulados.value ? pasajes.value : pasajesActivos.value
)

// ── Computed totales ───────────────────────────────────────────
const totalPasajes = computed(() =>
    pasajesActivos.value.reduce((s, p) => s + parseFloat(p.precio || 0), 0)
)
const totalPaquetesPasajes = computed(() =>
    pasajesActivos.value.reduce((s, p) => s + parseFloat(p.total_paquetes || 0), 0)
)
const totalEncomiendas = computed(() =>
    encomiendas.value.reduce((s, e) => s + parseFloat(e.precio || 0), 0)
)
const totalRecaudado = computed(() =>
    totalPasajes.value + totalPaquetesPasajes.value + totalEncomiendas.value
)

// ── Desglose por metodo de pago ────────────────────────────────
const resumenPago = computed(() => {
    const todos = [
        ...pasajesActivos.value.map(p => ({
            metodo_pago: p.metodo_pago,
            monto: parseFloat(p.precio || 0) + parseFloat(p.total_paquetes || 0),
        })),
        ...encomiendas.value.map(e => ({
            metodo_pago: e.metodo_pago,
            monto: parseFloat(e.precio || 0),
        })),
    ]
    return metodos
        .map(m => ({
            clave: m.clave,
            etiqueta: m.etiqueta,
            total: todos
                .filter(x => x.metodo_pago === m.clave)
                .reduce((s, x) => s + x.monto, 0),
        }))
        .filter(m => m.total > 0)
})

// ── Helpers ────────────────────────────────────────────────────
const ahora = computed(() =>
    new Date().toLocaleString('es-PE', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit',
    })
)

function formatFecha(f) {
    if (!f) return '-'
    return new Date(f).toLocaleString('es-PE', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit',
    })
}

function metodoLabel(c) {
    return metodos.find(m => m.clave === c)?.etiqueta || c || '-'
}

function claseEstadoPasaje(e) {
    return {
        emitido: 'badge badge-blue',
        embarcado: 'badge badge-green',
        anulado: 'badge badge-red',
    }[e] || 'badge badge-gray'
}

function etiquetaEstadoPasaje(e) {
    return { emitido: 'Emitido', embarcado: 'Embarcado', anulado: 'Anulado' }[e] || e
}

function claseEstadoEnc(e) {
    return {
        registrada: 'badge badge-gray',
        en_transito: 'badge badge-blue',
        entregada: 'badge badge-green',
        devuelta: 'badge badge-red',
    }[e] || 'badge badge-gray'
}

function etiquetaEstadoEnc(e) {
    return {
        registrada: 'Registrada',
        en_transito: 'En transito',
        entregada: 'Entregada',
        devuelta: 'Devuelta',
    }[e] || e
}

// ── Cargar viajes del dia ──────────────────────────────────────
async function cargarViajes() {
    viajeId.value = ''
    viaje.value = null
    pasajes.value = []
    encomiendas.value = []
    try {
        const { data } = await pasajesService.buscarViajes({
            fecha_salida__date: filtroFecha.value,
        })
        viajes.value = data.results ?? data
    } catch {
        viajes.value = []
    }
}


async function cargarPasajes() {
    if (!viajeId.value) return
    cargandoPasajes.value = true
    try {
        const { data: dataPasajes } = await pasajesService.obtenerPasajesPorViaje(viajeId.value)
        const activos = (dataPasajes.results ?? dataPasajes)
            .sort((a, b) => (parseInt(a.asiento) || 0) - (parseInt(b.asiento) || 0))

        if (mostrarAnulados.value) {
            const { data: dataAnulados } = await pasajesService.obtenerPasajes({
                viaje: viajeId.value,
                estado: 'anulado'
            })
            const anulados = (dataAnulados.results ?? dataAnulados)
                .sort((a, b) => (parseInt(a.asiento) || 0) - (parseInt(b.asiento) || 0))
            pasajes.value = [...activos, ...anulados]
        } else {
            pasajes.value = activos
        }
    } finally {
        cargandoPasajes.value = false
    }
}

// ✅ Solo recarga pasajes, no el viaje ni encomiendas
watch(mostrarAnulados, cargarPasajes)

// ── Cargar manifiesto del viaje seleccionado ───────────────────
async function cargarManifiesto() {
    if (!viajeId.value) return
    cargando.value = true
    try {
        viaje.value = viajes.value.find(v => v.id === parseInt(viajeId.value)) || null
        await cargarPasajes() // ← usar la función separada

        // Encomiendas
        try {
            const api = (await import('@/services/api')).default
            const { data: dataEnc } = await api.get('/encomiendas/', { params: { viaje: viajeId.value } })
            encomiendas.value = dataEnc.results ?? dataEnc
        } catch {
            encomiendas.value = []
        }
    } catch (e) {
        console.error('Error cargando manifiesto:', e)
    } finally {
        cargando.value = false
    }
}


// ── Embarcar pasajero ──────────────────────────────────────────
async function embarcar(pasaje) {
    embarcando.value = pasaje.id
    try {
        const api = (await import('@/services/api')).default
        await api.post(`/pasajes/${pasaje.id}/embarcar/`)
        // Actualizar estado localmente sin recargar todo
        const idx = pasajes.value.findIndex(p => p.id === pasaje.id)
        if (idx !== -1) {
            pasajes.value[idx] = { ...pasajes.value[idx], estado: 'embarcado' }
        }
    } catch (e) {
        console.error('Error al embarcar:', e.response?.data)
    } finally {
        embarcando.value = null
    }
}

// ── Imprimir ───────────────────────────────────────────────────
function imprimir() {
    handlePrint()
}

// ─────────────────────────────────────────────────────────────────
// Reemplaza la función exportarExcel() en ManifiestoPasajeros.vue
// Requiere: npm install exceljs  (usa ExcelJS que soporta más estilos)
// ─────────────────────────────────────────────────────────────────

async function exportarExcel() {
    if (!viaje.value || !pasajesActivos.value.length && !encomiendas.value.length) return

    try {
        const ExcelJS = (await import('exceljs')).default ?? (await import('exceljs'))
        const wb = new ExcelJS.Workbook()

        // ── Colores corporativos ──────────────────────────────
        const C = {
            azulOsc: 'FF1E3A8A',
            azulMed: 'FF2563EB',
            naranja: 'FFEA580C',
            naranjaClaro: 'FFF97316',
            verde: 'FF16A34A',
            rojo: 'FFDC2626',
            grisClaro: 'FFF8FAFC',
            grisHead: 'FFF1F5F9',
            blanco: 'FFFFFFFF',
            texto: 'FF111827',
            textoSub: 'FF374151',
            textoMuted: 'FF6B7280',
        }

        const borde = {
            top: { style: 'thin' },
            left: { style: 'thin' },
            bottom: { style: 'thin' },
            right: { style: 'thin' },
        }

        const bordeMedium = {
            top: { style: 'medium' },
            left: { style: 'medium' },
            bottom: { style: 'medium' },
            right: { style: 'medium' },
        }

        function fillSolid(argb) {
            return { type: 'pattern', pattern: 'solid', fgColor: { argb } }
        }

        function fontBase(opts = {}) {
            return {
                name: 'Arial',
                size: opts.size ?? 10,
                bold: opts.bold ?? false,
                italic: opts.italic ?? false,
                color: { argb: opts.color ?? C.texto },
            }
        }

        function alinear(h = 'left', v = 'middle', wrap = false) {
            return { horizontal: h, vertical: v, wrapText: wrap }
        }

        // Encabezado de empresa reutilizable
        function agregarCabecera(ws, cols, titulo, subtitulo, colorFondo, colorSub) {
            ws.mergeCells(`A1:${cols}1`)
            const c1 = ws.getCell('A1')
            c1.value = 'TURISMO WJL E.I.R.L.'
            c1.font = fontBase({ bold: true, color: C.blanco, size: 13 })
            c1.fill = fillSolid(C.azulOsc)
            c1.alignment = alinear('center')
            ws.getRow(1).height = 28

            ws.mergeCells(`A2:${cols}2`)
            const c2 = ws.getCell('A2')
            c2.value = 'Uniendo Familias  |  +51 999 713 436  |  Las 5 Esquinas - Huarmaca / Chiclayo'
            c2.font = fontBase({ italic: true, color: C.blanco, size: 9 })
            c2.fill = fillSolid(C.azulOsc)
            c2.alignment = alinear('center')
            ws.getRow(2).height = 16

            ws.mergeCells(`A3:${cols}3`)
            const c3 = ws.getCell('A3')
            c3.value = titulo
            c3.font = fontBase({ bold: true, color: C.azulOsc, size: 12 })
            c3.fill = fillSolid(C.grisHead)
            c3.alignment = alinear('center')
            ws.getRow(3).height = 22

            ws.mergeCells(`A4:${cols}4`)
            const c4 = ws.getCell('A4')
            c4.value = subtitulo
            c4.font = fontBase({ italic: true, color: C.blanco, size: 9 })
            c4.fill = fillSolid(colorSub)
            c4.alignment = alinear('center')
            ws.getRow(4).height = 16
        }

        const infoViaje = `Ruta: ${viaje.value.ruta_descripcion}  |  Salida: ${formatFecha(viaje.value.fecha_salida)}  |  Vehículo: ${viaje.value.vehiculo_placa}  |  Conductor: ${viaje.value.conductor_nombre || 'N/A'}`

        // ═══════════════════════════════════════════════════════
        // HOJA 1: RESUMEN
        // ═══════════════════════════════════════════════════════
        const ws1 = wb.addWorksheet('Resumen', {
            views: [{ showGridLines: false }]
        })
        ws1.columns = [
            { width: 22 }, { width: 22 }, { width: 22 },
            { width: 16 }, { width: 16 }, { width: 16 },
        ]

        agregarCabecera(ws1, 'F', 'MANIFIESTO DE PASAJEROS Y ENCOMIENDAS', infoViaje, C.azulMed, C.azulMed)

        // Datos del viaje (filas 5-9)
        const datosViaje = [
            ['Ruta:', viaje.value.ruta_descripcion],
            ['Fecha:', formatFecha(viaje.value.fecha_salida)],
            ['Vehículo:', viaje.value.vehiculo_placa],
            ['Conductor:', viaje.value.conductor_nombre || 'N/A'],
            ['Capacidad:', `${viaje.value.capacidad || 18} asientos`],
        ]
        datosViaje.forEach(([lbl, val], i) => {
            const fila = 5 + i
            ws1.mergeCells(`A${fila}:B${fila}`)
            const cLbl = ws1.getCell(`A${fila}`)
            cLbl.value = lbl
            cLbl.font = fontBase({ bold: true, color: C.azulOsc })
            cLbl.fill = fillSolid(C.grisClaro)
            cLbl.alignment = alinear('right')
            cLbl.border = borde
            ws1.mergeCells(`C${fila}:F${fila}`)
            const cVal = ws1.getCell(`C${fila}`)
            cVal.value = val
            cVal.font = fontBase({ color: C.texto })
            cVal.fill = fillSolid(C.grisClaro)
            cVal.alignment = alinear('left')
            cVal.border = borde
            ws1.getRow(fila).height = 18
        })

        // Separador
        ws1.getRow(10).height = 8

        // KPIs header
        ws1.mergeCells('A11:F11')
        const kpiH = ws1.getCell('A11')
        kpiH.value = 'RESUMEN DE OPERACIÓN'
        kpiH.font = fontBase({ bold: true, color: C.blanco, size: 11 })
        kpiH.fill = fillSolid(C.azulMed)
        kpiH.alignment = alinear('center')
        ws1.getRow(11).height = 22

        const kpis = [
            ['Pasajeros activos', pasajesActivos.value.length, C.azulMed],
            ['Embarcados', pasajesActivos.value.filter(p => p.estado === 'embarcado').length, C.verde],
            ['Encomiendas', encomiendas.value.length, C.naranja],
            ['Total pasajes S/.', totalPasajes.value.toFixed(2), C.azulOsc],
            ['Total paquetes S/.', totalPaquetesPasajes.value.toFixed(2), C.naranja],
            ['Total encomiendas S/.', totalEncomiendas.value.toFixed(2), C.naranja],
            ['TOTAL GENERAL S/.', totalRecaudado.value.toFixed(2), C.verde],
        ]

        kpis.forEach(([lbl, val, color], i) => {
            const fila = 12 + i
            const esTotal = lbl.startsWith('TOTAL')
            ws1.mergeCells(`A${fila}:C${fila}`)
            const cL = ws1.getCell(`A${fila}`)
            cL.value = lbl
            cL.font = fontBase({ bold: esTotal, color: C.textoSub, size: 10 })
            cL.fill = fillSolid(esTotal ? 'FFF0FDF4' : C.grisClaro)
            cL.alignment = alinear('right')
            cL.border = borde
            ws1.mergeCells(`D${fila}:F${fila}`)
            const cV = ws1.getCell(`D${fila}`)
            cV.value = esTotal ? `S/. ${val}` : val
            cV.font = fontBase({ bold: true, color: color, size: esTotal ? 13 : 11 })
            cV.fill = fillSolid(esTotal ? 'FFF0FDF4' : C.blanco)
            cV.alignment = alinear('center')
            cV.border = esTotal ? bordeMedium : borde
            ws1.getRow(fila).height = esTotal ? 24 : 20
        })

        // Desglose metodo pago
        const filaMP = 20
        ws1.getRow(filaMP).height = 8
        ws1.mergeCells(`A${filaMP + 1}:F${filaMP + 1}`)
        const mpH = ws1.getCell(`A${filaMP + 1}`)
        mpH.value = 'DESGLOSE POR MÉTODO DE PAGO'
        mpH.font = fontBase({ bold: true, color: C.blanco, size: 10 })
        mpH.fill = fillSolid(C.azulOsc)
        mpH.alignment = alinear('center')
        ws1.getRow(filaMP + 1).height = 20

        const todosTrans = [
            ...pasajesActivos.value.map(p => ({ mp: p.metodo_pago, monto: parseFloat(p.precio || 0) + parseFloat(p.total_paquetes || 0) })),
            ...encomiendas.value.map(e => ({ mp: e.metodo_pago, monto: parseFloat(e.precio || 0) })),
        ]
        const metodosMap = { cash: 'Efectivo', yape: 'Yape', plin: 'Plin', card: 'Tarjeta' }
        let filaOffset = filaMP + 2
        Object.entries(metodosMap).forEach(([clave, etiqueta]) => {
            const tot = todosTrans.filter(x => x.mp === clave).reduce((s, x) => s + x.monto, 0)
            if (tot <= 0) return
            ws1.mergeCells(`A${filaOffset}:C${filaOffset}`)
            const cL = ws1.getCell(`A${filaOffset}`)
            cL.value = etiqueta
            cL.font = fontBase({ color: C.textoSub })
            cL.fill = fillSolid(C.grisClaro)
            cL.alignment = alinear('right')
            cL.border = borde
            ws1.mergeCells(`D${filaOffset}:F${filaOffset}`)
            const cV = ws1.getCell(`D${filaOffset}`)
            cV.value = `S/. ${tot.toFixed(2)}`
            cV.font = fontBase({ bold: true, color: C.azulOsc })
            cV.fill = fillSolid(C.blanco)
            cV.alignment = alinear('center')
            cV.border = borde
            ws1.getRow(filaOffset).height = 18
            filaOffset++
        })

        // ═══════════════════════════════════════════════════════
        // HOJA 2: PASAJEROS
        // ═══════════════════════════════════════════════════════
        const ws2 = wb.addWorksheet('Pasajeros', {
            views: [{ showGridLines: false }]
        })
        ws2.columns = [
            { width: 5 },  // N
            { width: 8 },  // Asiento
            { width: 28 },  // Nombre
            { width: 12 },  // DNI
            { width: 14 },  // Telefono
            { width: 12 },  // Pago
            { width: 12 },  // Precio
            { width: 12 },  // Paquetes
            { width: 14 },  // Total
            { width: 13 },  // Estado
        ]

        agregarCabecera(ws2, 'J', 'LISTA DE PASAJEROS', infoViaje, C.azulMed, C.azulMed)

        // Headers
        const headersP = ['N°', 'Asiento', 'Nombres y Apellidos', 'DNI', 'Teléfono', 'Método Pago', 'Precio S/.', 'Paquetes S/.', 'Total S/.', 'Estado']
        const rowHP = ws2.addRow(headersP)
        rowHP.height = 20
        rowHP.eachCell(cell => {
            cell.font = fontBase({ bold: true, color: C.blanco, size: 10 })
            cell.fill = fillSolid(C.azulMed)
            cell.alignment = alinear('center')
            cell.border = borde
        })

        // Activos primero, luego anulados
        const ordenados = [...pasajesActivos.value, ...pasajes.value.filter(p => p.estado === 'anulado')]
        ordenados.forEach((p, i) => {
            const esAnulado = p.estado === 'anulado'
            const bg = esAnulado ? 'FFFEF2F2' : (i % 2 === 0 ? C.blanco : C.grisClaro)
            const colorEstado = { embarcado: C.verde, emitido: C.azulMed, anulado: C.rojo }[p.estado] || C.textoSub
            const total = parseFloat(p.precio || 0) + parseFloat(p.total_paquetes || 0)

            const row = ws2.addRow([
                i + 1,
                p.asiento,
                p.pasajero_nombre,
                p.pasajero_dni,
                p.pasajero_telefono || '—',
                metodosMap[p.metodo_pago] || p.metodo_pago,
                parseFloat(p.precio || 0),
                parseFloat(p.total_paquetes || 0),
                total,
                { embarcado: 'EMBARCADO', emitido: 'EMITIDO', anulado: 'ANULADO' }[p.estado] || p.estado,
            ])
            row.height = 18
            row.eachCell((cell, colNum) => {
                cell.fill = fillSolid(bg)
                cell.border = borde
                cell.font = fontBase({
                    color: colNum === 10 ? colorEstado : (esAnulado ? C.textoMuted : C.texto),
                    bold: colNum === 10,
                    italic: esAnulado,
                })
                cell.alignment = alinear(
                    [1, 2, 4, 6, 10].includes(colNum) ? 'center' : [7, 8, 9].includes(colNum) ? 'right' : 'left'
                )
                if ([7, 8, 9].includes(colNum)) cell.numFmt = '#,##0.00'
            })
        })

        // Fila total pasajeros
        const totalRow = ws2.addRow([
            '', '', '', '', '', 'TOTALES',
            totalPasajes.value,
            totalPaquetesPasajes.value,
            totalPasajes.value + totalPaquetesPasajes.value,
            `S/. ${(totalPasajes.value + totalPaquetesPasajes.value).toFixed(2)}`,
        ])
        totalRow.height = 24
        totalRow.eachCell((cell, colNum) => {
            cell.font = fontBase({ bold: true, color: C.blanco, size: colNum === 10 ? 12 : 10 })
            cell.fill = fillSolid(C.azulOsc)
            cell.alignment = alinear(colNum >= 6 ? 'right' : 'center')
            cell.border = colNum === 10 ? bordeMedium : borde
            if ([7, 8, 9].includes(colNum)) cell.numFmt = '#,##0.00'
        })

        // ═══════════════════════════════════════════════════════
        // HOJA 3: ENCOMIENDAS
        // ═══════════════════════════════════════════════════════
        const ws3 = wb.addWorksheet('Encomiendas', {
            views: [{ showGridLines: false }]
        })
        ws3.columns = [
            { width: 5 },  // N
            { width: 10 },  // Codigo
            { width: 22 },  // Remitente
            { width: 12 },  // DNI Rem
            { width: 22 },  // Destinatario
            { width: 12 },  // DNI Dest
            { width: 22 },  // Descripcion
            { width: 9 },  // Peso
            { width: 12 },  // Pago
            { width: 12 },  // Precio
            { width: 13 },  // Estado
        ]

        agregarCabecera(ws3, 'K', 'ENCOMIENDAS DEL VIAJE', infoViaje, C.naranja, C.naranjaClaro)

        const headersE = ['N°', 'Código', 'Remitente', 'DNI Rem.', 'Destinatario', 'DNI Dest.', 'Descripción', 'Peso kg', 'Método Pago', 'Precio S/.', 'Estado']
        const rowHE = ws3.addRow(headersE)
        rowHE.height = 20
        rowHE.eachCell(cell => {
            cell.font = fontBase({ bold: true, color: C.blanco, size: 10 })
            cell.fill = fillSolid(C.naranjaClaro)
            cell.alignment = alinear('center')
            cell.border = borde
        })

        encomiendas.value.forEach((e, i) => {
            const bg = i % 2 === 0 ? C.blanco : C.grisClaro
            const colorEstado = { registrada: C.textoMuted, en_transito: C.azulMed, entregada: C.verde, devuelta: C.rojo }[e.estado] || C.textoSub
            const etiquetaEst = { registrada: 'REGISTRADA', en_transito: 'EN TRANSITO', entregada: 'ENTREGADA', devuelta: 'DEVUELTA' }[e.estado] || e.estado

            const row = ws3.addRow([
                i + 1,
                String(e.codigo || '').slice(0, 8).toUpperCase(),
                e.remitente_nombre,
                e.remitente_dni,
                e.destinatario_nombre,
                e.destinatario_dni,
                e.descripcion,
                e.peso_kg ? parseFloat(e.peso_kg) : '—',
                metodosMap[e.metodo_pago] || e.metodo_pago,
                parseFloat(e.precio || 0),
                etiquetaEst,
            ])
            row.height = 18
            row.eachCell((cell, colNum) => {
                cell.fill = fillSolid(bg)
                cell.border = borde
                cell.font = fontBase({
                    color: colNum === 11 ? colorEstado : C.texto,
                    bold: colNum === 11,
                })
                cell.alignment = alinear(
                    [1, 2, 4, 6, 8, 9, 11].includes(colNum) ? 'center' : colNum === 10 ? 'right' : 'left'
                )
                if (colNum === 10) cell.numFmt = '#,##0.00'
            })
        })

        // Fila total encomiendas
        const totalRowE = ws3.addRow([
            '', '', '', '', '', '', '', '', 'TOTAL',
            totalEncomiendas.value,
            `S/. ${totalEncomiendas.value.toFixed(2)}`,
        ])
        totalRowE.height = 24
        totalRowE.eachCell((cell, colNum) => {
            cell.font = fontBase({ bold: true, color: C.blanco, size: colNum === 11 ? 12 : 10 })
            cell.fill = fillSolid(C.naranja)
            cell.alignment = alinear(colNum >= 9 ? 'right' : 'center')
            cell.border = colNum === 11 ? bordeMedium : borde
            if (colNum === 10) cell.numFmt = '#,##0.00'
        })

        // ── Descargar en el navegador ─────────────────────────
        const buffer = await wb.xlsx.writeBuffer()
        const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        const ruta = (viaje.value?.ruta_descripcion || 'viaje').replace(/[\s\/→]/g, '_')
        a.href = url
        a.download = `Manifiesto_${ruta}_${filtroFecha.value}.xlsx`
        a.click()
        URL.revokeObjectURL(url)

    } catch (e) {
        console.error('Error exportando Excel:', e)
        alert('Error al exportar. Verifica que exceljs esté instalado:\nnpm install exceljs')
    }
}

onMounted(cargarViajes)
</script>

<style scoped>
/* Ocultar en pantalla, mostrar solo al imprimir */
.print-only {
    display: none;
}

@media print {
    .no-print {
        display: none !important;
    }

    .print-only {
        display: block !important;
    }

    .card {
        box-shadow: none !important;
        border: 1px solid #e2e8f0 !important;
        break-inside: avoid;
        page-break-inside: avoid;
    }

    .table th,
    .table td {
        font-size: 10px !important;
        padding: 4px 6px !important;
    }

    .badge {
        font-size: 9px !important;
        padding: 1px 6px !important;
    }
}
</style>