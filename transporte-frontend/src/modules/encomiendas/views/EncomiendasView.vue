<template>
    <div class="space-y-5">

        <!-- Encabezado -->
        <div class="page-header">
            <div>
                <h1 class="page-title">Encomiendas</h1>
                <p class="page-subtitle">Registro y seguimiento de encomiendas</p>
            </div>
            <button @click="abrirModalCrear" class="btn-primary">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
                </svg>
                Nueva Encomienda
            </button>
        </div>

        <!-- Filtros -->
        <div class="flex flex-wrap gap-3">
            <div class="relative">
                <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input v-model="busqueda" type="text" placeholder="Buscar por codigo, remitente o destinatario..." class="form-input pl-9 w-80" />
            </div>
            <select v-model="filtroEstado" class="form-input w-44">
                <option value="">Todos los estados</option>
                <option value="registrada">Registrada</option>
                <option value="en_transito">En transito</option>
                <option value="entregada">Entregada</option>
                <option value="devuelta">Devuelta</option>
            </select>
            <input v-model="filtroFecha" type="date" class="form-input w-44" />
            <button @click="cargarEncomiendas" class="btn-secondary">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Actualizar
            </button>
        </div>

        <!-- Tarjetas resumen -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div v-for="estado in estadosSummary" :key="estado.clave" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4">
                <div class="flex items-center justify-between mb-2">
                    <p class="text-xs font-bold uppercase tracking-wide text-gray-400">{{ estado.etiqueta }}</p>
                    <span :class="['w-2.5 h-2.5 rounded-full', estado.punto]"></span>
                </div>
                <p :class="['text-2xl font-black', estado.color]">
                    {{ store.encomiendas.filter(e => e.estado === estado.clave).length }}
                </p>
            </div>
        </div>

        <!-- Tabla -->
        <div class="card">
            <div class="table-wrapper">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Codigo</th>
                            <th>Remitente</th>
                            <th>Destinatario</th>
                            <th>Descripcion</th>
                            <th class="text-center">Peso</th>
                            <th>Viaje</th>
                            <th class="text-right">Precio</th>
                            <th>Estado</th>
                            <th class="text-right">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="store.cargando">
                            <td colspan="9">
                                <div class="flex justify-center py-10">
                                    <svg class="w-6 h-6 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                    </svg>
                                </div>
                            </td>
                        </tr>
                        <tr v-else-if="!encomiendasFiltradas.length">
                            <td colspan="9" class="text-center py-12 text-gray-400 italic">
                                No se encontraron encomiendas
                            </td>
                        </tr>
                        <tr v-for="e in encomiendasFiltradas" :key="e.id">
                            <td>
                                <span class="font-mono text-xs font-bold text-gray-700 bg-gray-100 px-2 py-1 rounded">
                                    {{ String(e.codigo || '').slice(0, 8).toUpperCase() }}
                                </span>
                            </td>
                            <td>
                                <p class="font-semibold text-gray-900 text-sm">{{ e.remitente_nombre }}</p>
                                <p class="text-xs text-gray-400 font-mono">{{ e.remitente_dni }}</p>
                            </td>
                            <td>
                                <p class="font-semibold text-gray-900 text-sm">{{ e.destinatario_nombre }}</p>
                                <p class="text-xs text-gray-400 font-mono">{{ e.destinatario_dni }}</p>
                            </td>
                            <td class="text-sm text-gray-600 max-w-[160px] truncate">{{ e.descripcion }}</td>
                            <td class="text-center">
                                <span class="text-sm font-bold text-gray-700">{{ e.peso_kg ? e.peso_kg + ' kg' : '-' }}</span>
                            </td>
                            <td class="text-xs text-gray-500">{{ e.viaje_descripcion || '-' }}</td>
                            <td class="text-right font-black text-gray-900">S/. {{ e.precio }}</td>
                            <td><span :class="claseEstado(e.estado)">{{ etiquetaEstado(e.estado) }}</span></td>
                            <td class="text-right">
                                <div class="flex items-center justify-end gap-1">
                                    <button @click="verComprobante(e)" title="Ver comprobante"
                                        class="w-8 h-8 rounded-lg hover:bg-blue-50 flex items-center justify-center text-gray-400 hover:text-blue-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                    </button>
                                    <button v-if="['registrada', 'en_transito'].includes(e.estado)"
                                        @click="abrirModalEstado(e)" title="Cambiar estado"
                                        class="w-8 h-8 rounded-lg hover:bg-amber-50 flex items-center justify-center text-gray-400 hover:text-amber-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                        </svg>
                                    </button>
                                    <button v-if="e.estado === 'en_transito'" @click="abrirModalEntrega(e)"
                                        title="Registrar entrega"
                                        class="w-8 h-8 rounded-lg hover:bg-emerald-50 flex items-center justify-center text-gray-400 hover:text-emerald-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- MODAL REGISTRAR ENCOMIENDA -->
        <AppModal v-model="modalCrear" titulo="Nueva Encomienda" ancho="xl">
            <form @submit.prevent="guardar" class="space-y-5">
                <div>
                    <h4 class="text-sm font-black text-gray-700 uppercase tracking-wide mb-3 flex items-center gap-2">
                        <span class="w-5 h-5 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-[10px] font-black">1</span>
                        Remitente (quien envia)
                    </h4>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="form-label">DNI <span class="text-red-500">*</span></label>
                            <div class="flex gap-2">
                                <input v-model="formulario.remitente_dni" type="text" maxlength="8" class="form-input"
                                    :class="{ 'form-input-error': errores.remitente_dni }" placeholder="12345678"
                                    @keyup.enter="buscarRemitente" />
                                <button type="button" @click="buscarRemitente" class="btn-secondary flex-shrink-0 px-3">
                                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                </button>
                            </div>
                            <p v-if="errores.remitente_dni" class="form-error">{{ errores.remitente_dni }}</p>
                        </div>
                        <div>
                            <label class="form-label">Telefono remitente</label>
                            <input v-model="formulario.remitente_telefono" type="text" class="form-input" placeholder="987654321" />
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4 mt-3">
                        <div>
                            <label class="form-label">Nombres <span class="text-red-500">*</span></label>
                            <input v-model="formulario.remitente_nombres" type="text" class="form-input"
                                :class="{ 'form-input-error': errores.remitente_nombres }" placeholder="Nombres del remitente" />
                            <p v-if="errores.remitente_nombres" class="form-error">{{ errores.remitente_nombres }}</p>
                        </div>
                        <div>
                            <label class="form-label">Apellidos <span class="text-red-500">*</span></label>
                            <input v-model="formulario.remitente_apellidos" type="text" class="form-input"
                                :class="{ 'form-input-error': errores.remitente_apellidos }" placeholder="Apellidos del remitente" />
                            <p v-if="errores.remitente_apellidos" class="form-error">{{ errores.remitente_apellidos }}</p>
                        </div>
                    </div>
                </div>

                <div class="border-t border-gray-100"></div>

                <div>
                    <h4 class="text-sm font-black text-gray-700 uppercase tracking-wide mb-3 flex items-center gap-2">
                        <span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-[10px] font-black">2</span>
                        Destinatario (quien recibe)
                    </h4>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="form-label">DNI <span class="text-red-500">*</span></label>
                            <div class="flex gap-2">
                                <input v-model="formulario.destinatario_dni" type="text" maxlength="8" class="form-input"
                                    :class="{ 'form-input-error': errores.destinatario_dni }" placeholder="12345678"
                                    @keyup.enter="buscarDestinatario" />
                                <button type="button" @click="buscarDestinatario" class="btn-secondary flex-shrink-0 px-3">
                                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                </button>
                            </div>
                            <p v-if="errores.destinatario_dni" class="form-error">{{ errores.destinatario_dni }}</p>
                        </div>
                        <div>
                            <label class="form-label">Telefono destinatario</label>
                            <input v-model="formulario.destinatario_telefono" type="text" class="form-input" placeholder="987654321" />
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4 mt-3">
                        <div>
                            <label class="form-label">Nombres <span class="text-red-500">*</span></label>
                            <input v-model="formulario.destinatario_nombres" type="text" class="form-input"
                                :class="{ 'form-input-error': errores.destinatario_nombres }" placeholder="Nombres del destinatario" />
                            <p v-if="errores.destinatario_nombres" class="form-error">{{ errores.destinatario_nombres }}</p>
                        </div>
                        <div>
                            <label class="form-label">Apellidos <span class="text-red-500">*</span></label>
                            <input v-model="formulario.destinatario_apellidos" type="text" class="form-input"
                                :class="{ 'form-input-error': errores.destinatario_apellidos }" placeholder="Apellidos del destinatario" />
                            <p v-if="errores.destinatario_apellidos" class="form-error">{{ errores.destinatario_apellidos }}</p>
                        </div>
                    </div>
                </div>

                <div class="border-t border-gray-100"></div>

                <div>
                    <h4 class="text-sm font-black text-gray-700 uppercase tracking-wide mb-3 flex items-center gap-2">
                        <span class="w-5 h-5 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center text-[10px] font-black">3</span>
                        Datos de la encomienda
                    </h4>
                    <div class="grid grid-cols-3 gap-4">
                        <div class="col-span-2">
                            <label class="form-label">Descripcion <span class="text-red-500">*</span></label>
                            <input v-model="formulario.descripcion" type="text" class="form-input"
                                :class="{ 'form-input-error': errores.descripcion }" placeholder="Ej: Ropa, documentos, electrodomestico..." />
                            <p v-if="errores.descripcion" class="form-error">{{ errores.descripcion }}</p>
                        </div>
                        <div>
                            <label class="form-label">Peso (kg)</label>
                            <input v-model="formulario.peso_kg" type="number" step="0.1" min="0" class="form-input" placeholder="Ej: 2.5" />
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4 mt-3">
                        <div>
                            <label class="form-label">Precio (S/.) <span class="text-red-500">*</span></label>
                            <input v-model="formulario.precio" type="number" step="0.50" min="0"
                                class="form-input text-lg font-bold" :class="{ 'form-input-error': errores.precio }" placeholder="0.00" />
                            <p v-if="errores.precio" class="form-error">{{ errores.precio }}</p>
                        </div>
                        <div>
                            <label class="form-label">Metodo de pago <span class="text-red-500">*</span></label>
                            <select v-model="formulario.metodo_pago" class="form-input" :class="{ 'form-input-error': errores.metodo_pago }">
                                <option value="">Seleccionar...</option>
                                <option value="cash">Efectivo</option>
                                <option value="yape">Yape</option>
                                <option value="plin">Plin</option>
                                <option value="card">Tarjeta</option>
                            </select>
                            <p v-if="errores.metodo_pago" class="form-error">{{ errores.metodo_pago }}</p>
                        </div>
                    </div>
                    <div class="mt-3">
                        <label class="form-label">Viaje (opcional)</label>
                        <select v-model="formulario.viaje" class="form-input">
                            <option value="">Sin asignar a viaje</option>
                            <option v-for="v in store.viajes" :key="v.id" :value="v.id">
                                {{ v.ruta_descripcion }} - {{ formatearFechaHora(v.fecha_salida) }} ({{ v.vehiculo_placa }})
                            </option>
                        </select>
                        <p class="form-hint">Puedes asignarla a un viaje despues</p>
                    </div>
                    <div class="mt-3">
                        <label class="form-label">Observaciones</label>
                        <textarea v-model="formulario.observacion" rows="2" class="form-input resize-none" placeholder="Instrucciones especiales, fragilidad, etc." />
                    </div>
                </div>

                <div v-if="errorServidor" class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                    <svg class="w-4 h-4 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p class="text-xs text-red-700 font-medium">{{ errorServidor }}</p>
                </div>
            </form>
            <template #footer>
                <button @click="modalCrear = false" class="btn-secondary">Cancelar</button>
                <button @click="guardar" :disabled="guardando" class="btn-primary">
                    <svg v-if="guardando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    {{ guardando ? 'Registrando...' : 'Registrar encomienda' }}
                </button>
            </template>
        </AppModal>

        <!-- MODAL CAMBIAR ESTADO -->
        <AppModal v-model="modalEstado" titulo="Cambiar estado" ancho="sm">
            <div class="space-y-3">
                <p class="text-sm text-gray-500 mb-2">
                    Encomienda: <span class="font-bold text-gray-900">{{ String(encomiendaSeleccionada?.codigo || '').slice(0, 8).toUpperCase() }}</span>
                </p>
                <button v-for="est in estadosDisponibles" :key="est.valor" @click="nuevoEstado = est.valor"
                    :class="['w-full flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all text-left',
                        nuevoEstado === est.valor ? 'border-blue-500 bg-blue-50' : 'border-gray-100 hover:border-gray-200 bg-white']">
                    <span :class="['w-2.5 h-2.5 rounded-full flex-shrink-0', est.punto]"></span>
                    <span class="text-sm font-semibold text-gray-800">{{ est.etiqueta }}</span>
                </button>
            </div>
            <template #footer>
                <button @click="modalEstado = false" class="btn-secondary">Cancelar</button>
                <button @click="cambiarEstado" :disabled="guardando || !nuevoEstado" class="btn-primary">
                    {{ guardando ? 'Guardando...' : 'Confirmar' }}
                </button>
            </template>
        </AppModal>

        <!-- MODAL REGISTRAR ENTREGA -->
        <AppModal v-model="modalEntrega" titulo="Registrar entrega" ancho="sm">
            <div class="space-y-4">
                <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
                    <p class="text-sm font-bold text-emerald-800 mb-1">Confirmando entrega a: {{ encomiendaSeleccionada?.destinatario_nombre }}</p>
                    <p class="text-xs text-emerald-600">DNI: {{ encomiendaSeleccionada?.destinatario_dni }}</p>
                </div>
                <div>
                    <label class="form-label">DNI de quien recibe <span class="text-red-500">*</span></label>
                    <input v-model="formEntrega.dni_receptor" type="text" maxlength="8" class="form-input"
                        :class="{ 'form-input-error': erroresEntrega.dni_receptor }" placeholder="DNI del receptor" />
                    <p v-if="erroresEntrega.dni_receptor" class="form-error">{{ erroresEntrega.dni_receptor }}</p>
                    <p class="form-hint">Puede ser el destinatario u otra persona autorizada</p>
                </div>
                <div>
                    <label class="form-label">Nombre de quien recibe <span class="text-red-500">*</span></label>
                    <input v-model="formEntrega.nombre_receptor" type="text" class="form-input"
                        :class="{ 'form-input-error': erroresEntrega.nombre_receptor }" placeholder="Nombre completo" />
                    <p v-if="erroresEntrega.nombre_receptor" class="form-error">{{ erroresEntrega.nombre_receptor }}</p>
                </div>
                <div>
                    <label class="form-label">Observaciones de entrega</label>
                    <textarea v-model="formEntrega.observaciones" rows="2" class="form-input resize-none" placeholder="Estado del paquete, notas..." />
                </div>
                <div v-if="erroresEntrega.servidor" class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                    <p class="text-xs text-red-700 font-medium">{{ erroresEntrega.servidor }}</p>
                </div>
            </div>
            <template #footer>
                <button @click="modalEntrega = false" class="btn-secondary">Cancelar</button>
                <button @click="registrarEntrega" :disabled="guardando" class="btn-primary">
                    <svg v-if="guardando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    {{ guardando ? 'Registrando...' : 'Confirmar entrega' }}
                </button>
            </template>
        </AppModal>

        <!-- MODAL COMPROBANTE — TicketEncomienda lo maneja todo -->
        <TicketEncomienda v-model="modalComprobante" :enc="encomiendaComprobante" />

    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useEncomiendasStore } from '../stores/encomiendas.store'
import { encomiendasService } from '../services/encomiendas.service'
import AppModal from '@/components/common/AppModal.vue'
import TicketEncomienda from '../components/TicketEncomienda.vue'

const store = useEncomiendasStore()

const busqueda              = ref('')
const filtroEstado          = ref('')
const filtroFecha           = ref('')
const guardando             = ref(false)
const errorServidor         = ref('')
const modalCrear            = ref(false)
const modalEstado           = ref(false)
const modalEntrega          = ref(false)
const modalComprobante      = ref(false)
const encomiendaSeleccionada = ref(null)
const encomiendaComprobante  = ref(null)
const nuevoEstado            = ref('')

const formulario = reactive({
    remitente_dni: '', remitente_nombres: '', remitente_apellidos: '', remitente_telefono: '',
    destinatario_dni: '', destinatario_nombres: '', destinatario_apellidos: '', destinatario_telefono: '',
    descripcion: '', peso_kg: '', precio: '', metodo_pago: '', viaje: '', observacion: '',
})

const errores = reactive({
    remitente_dni: '', remitente_nombres: '', remitente_apellidos: '',
    destinatario_dni: '', destinatario_nombres: '', destinatario_apellidos: '',
    descripcion: '', precio: '', metodo_pago: '',
})

const formEntrega    = reactive({ dni_receptor: '', nombre_receptor: '', observaciones: '' })
const erroresEntrega = reactive({ dni_receptor: '', nombre_receptor: '', servidor: '' })

const estadosSummary = [
    { clave: 'registrada',  etiqueta: 'Registradas', punto: 'bg-gray-400',    color: 'text-gray-700'    },
    { clave: 'en_transito', etiqueta: 'En transito', punto: 'bg-blue-500',    color: 'text-blue-600'    },
    { clave: 'entregada',   etiqueta: 'Entregadas',  punto: 'bg-emerald-500', color: 'text-emerald-600' },
    { clave: 'devuelta',    etiqueta: 'Devueltas',   punto: 'bg-red-400',     color: 'text-red-500'     },
]

const estadosDisponibles = computed(() => {
    const actual = encomiendaSeleccionada.value?.estado
    const flujo = {
        registrada: [
            { valor: 'en_transito', etiqueta: 'En transito', punto: 'bg-blue-500' },
            { valor: 'devuelta',    etiqueta: 'Devuelta',    punto: 'bg-red-400'  },
        ],
        en_transito: [
            { valor: 'entregada', etiqueta: 'Entregada', punto: 'bg-emerald-500' },
            { valor: 'devuelta',  etiqueta: 'Devuelta',  punto: 'bg-red-400'     },
        ],
    }
    return flujo[actual] || []
})

const encomiendasFiltradas = computed(() =>
    store.encomiendas.filter(e => {
        const texto = busqueda.value.toLowerCase()
        const coincideTexto = !texto ||
            String(e.codigo || '').toLowerCase().includes(texto) ||
            e.remitente_nombre?.toLowerCase().includes(texto) ||
            e.destinatario_nombre?.toLowerCase().includes(texto) ||
            e.remitente_dni?.includes(texto) ||
            e.destinatario_dni?.includes(texto)
        const coincideEstado = !filtroEstado.value || e.estado === filtroEstado.value
        const coincideFecha  = !filtroFecha.value  || e.creado_en?.startsWith(filtroFecha.value)
        return coincideTexto && coincideEstado && coincideFecha
    })
)

function claseEstado(estado) {
    return {
        registrada:  'badge badge-gray',
        en_transito: 'badge badge-blue',
        entregada:   'badge badge-green',
        devuelta:    'badge badge-red',
    }[estado] || 'badge badge-gray'
}

function etiquetaEstado(estado) {
    return {
        registrada:  'Registrada',
        en_transito: 'En transito',
        entregada:   'Entregada',
        devuelta:    'Devuelta',
    }[estado] || estado
}

function formatearFechaHora(fecha) {
    if (!fecha) return ''
    return new Date(fecha).toLocaleString('es-PE', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function buscarPersona(dni, tipo) {
    if (!dni || dni.length !== 8) return
    try {
        const { default: api } = await import('@/services/api')
        const { data } = await api.get('/pasajes/pasajeros/', { params: { dni } })
        const p = data.results?.[0] || data[0]
        if (!p) return
        if (tipo === 'remitente') {
            formulario.remitente_nombres   = p.nombres
            formulario.remitente_apellidos = p.apellidos
            formulario.remitente_telefono  = p.telefono || ''
        } else {
            formulario.destinatario_nombres   = p.nombres
            formulario.destinatario_apellidos = p.apellidos
            formulario.destinatario_telefono  = p.telefono || ''
        }
    } catch {}
}

const buscarRemitente    = () => buscarPersona(formulario.remitente_dni, 'remitente')
const buscarDestinatario = () => buscarPersona(formulario.destinatario_dni, 'destinatario')

function limpiarFormulario() {
    Object.keys(formulario).forEach(k => formulario[k] = '')
    Object.keys(errores).forEach(k => errores[k] = '')
    errorServidor.value = ''
}

function abrirModalCrear() {
    limpiarFormulario()
    store.cargarViajes()
    modalCrear.value = true
}

function validar() {
    let valido = true
    Object.keys(errores).forEach(k => errores[k] = '')
    if (!formulario.remitente_dni || formulario.remitente_dni.length !== 8)       { errores.remitente_dni = 'DNI de 8 digitos'; valido = false }
    if (!formulario.remitente_nombres.trim())                                      { errores.remitente_nombres = 'Obligatorio'; valido = false }
    if (!formulario.remitente_apellidos.trim())                                    { errores.remitente_apellidos = 'Obligatorio'; valido = false }
    if (!formulario.destinatario_dni || formulario.destinatario_dni.length !== 8)  { errores.destinatario_dni = 'DNI de 8 digitos'; valido = false }
    if (!formulario.destinatario_nombres.trim())                                   { errores.destinatario_nombres = 'Obligatorio'; valido = false }
    if (!formulario.destinatario_apellidos.trim())                                 { errores.destinatario_apellidos = 'Obligatorio'; valido = false }
    if (!formulario.descripcion.trim())                                            { errores.descripcion = 'Obligatorio'; valido = false }
    if (!formulario.precio || parseFloat(formulario.precio) <= 0)                  { errores.precio = 'Ingresa un precio valido'; valido = false }
    if (!formulario.metodo_pago)                                                   { errores.metodo_pago = 'Selecciona un metodo de pago'; valido = false }
    return valido
}

async function guardar() {
    if (!validar()) return
    guardando.value = true
    errorServidor.value = ''
    try {
        const payload = {
            remitente_dni:          formulario.remitente_dni,
            remitente_nombres:      formulario.remitente_nombres,
            remitente_apellidos:    formulario.remitente_apellidos,
            remitente_telefono:     formulario.remitente_telefono || '',
            destinatario_dni:       formulario.destinatario_dni,
            destinatario_nombres:   formulario.destinatario_nombres,
            destinatario_apellidos: formulario.destinatario_apellidos,
            destinatario_telefono:  formulario.destinatario_telefono || '',
            descripcion:            formulario.descripcion,
            peso_kg:                formulario.peso_kg ? parseFloat(formulario.peso_kg) : null,
            precio:                 formulario.precio,
            metodo_pago:            formulario.metodo_pago,
            viaje:                  formulario.viaje ? parseInt(formulario.viaje) : null,
            observacion:            formulario.observacion || '',
        }
        await encomiendasService.crearEncomienda(payload)
        modalCrear.value = false
        cargarEncomiendas()
    } catch (e) {
        const data = e.response?.data
        if (data && typeof data === 'object') {
            Object.keys(data).forEach(k => {
                if (k in errores) errores[k] = Array.isArray(data[k]) ? data[k][0] : data[k]
            })
            const noMapeados = Object.entries(data)
                .filter(([k]) => !(k in errores))
                .map(([k, v]) => `${k}: ${Array.isArray(v) ? v[0] : v}`)
                .join(' | ')
            errorServidor.value = noMapeados || 'Verifica los campos e intenta de nuevo.'
        } else {
            errorServidor.value = 'Error de conexion. Intenta de nuevo.'
        }
    } finally {
        guardando.value = false
    }
}

function abrirModalEstado(enc) {
    encomiendaSeleccionada.value = enc
    nuevoEstado.value = ''
    modalEstado.value = true
}

async function cambiarEstado() {
    if (!nuevoEstado.value) return
    guardando.value = true
    try {
        await encomiendasService.actualizarEstado(encomiendaSeleccionada.value.id, { estado: nuevoEstado.value })
        modalEstado.value = false
        cargarEncomiendas()
    } catch (e) {
        console.error('Error cambiar estado:', e.response?.data)
    } finally {
        guardando.value = false
    }
}

function abrirModalEntrega(enc) {
    encomiendaSeleccionada.value = enc
    Object.keys(formEntrega).forEach(k => formEntrega[k] = '')
    Object.keys(erroresEntrega).forEach(k => erroresEntrega[k] = '')
    modalEntrega.value = true
}

async function registrarEntrega() {
    Object.keys(erroresEntrega).forEach(k => erroresEntrega[k] = '')
    let valido = true
    if (!formEntrega.dni_receptor || formEntrega.dni_receptor.length !== 8) { erroresEntrega.dni_receptor = 'DNI de 8 digitos'; valido = false }
    if (!formEntrega.nombre_receptor.trim()) { erroresEntrega.nombre_receptor = 'Obligatorio'; valido = false }
    if (!valido) return
    guardando.value = true
    try {
        await encomiendasService.registrarEntrega(encomiendaSeleccionada.value.id, {
            entregado_a: `${formEntrega.nombre_receptor} (DNI: ${formEntrega.dni_receptor})`,
        })
        modalEntrega.value = false
        cargarEncomiendas()
    } catch {
        erroresEntrega.servidor = 'No se pudo registrar la entrega. Intenta de nuevo.'
    } finally {
        guardando.value = false
    }
}

function verComprobante(enc) {
    encomiendaComprobante.value = enc
    modalComprobante.value = true
}

async function cargarEncomiendas() {
    const params = {}
    if (filtroEstado.value) params.estado = filtroEstado.value
    if (filtroFecha.value)  params.creado_en__date = filtroFecha.value
    await store.cargarEncomiendas(params)
}

onMounted(cargarEncomiendas)
</script>