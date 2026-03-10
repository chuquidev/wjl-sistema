<template>
    <div class="space-y-5">

        <!-- Encabezado -->
        <div class="page-header">
            <div>
                <h1 class="page-title">Ubicaciones</h1>
                <p class="page-subtitle">Gestión de sucursales, ciudades y rutas</p>
            </div>
            <button @click="abrirModalCrear" class="btn-primary">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
                </svg>
                Nuevo {{ etiquetaTab }}
            </button>
        </div>

        <!-- Tabs -->
        <div class="flex gap-1 p-1 bg-gray-100 rounded-xl w-fit">
            <button v-for="tab in tabs" :key="tab.clave" @click="tabActivo = tab.clave" :class="[
                'px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-150',
                tabActivo === tab.clave
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-500 hover:text-gray-700'
            ]">
                {{ tab.etiqueta }}
                <span :class="[
                    'ml-1.5 px-1.5 py-0.5 rounded-md text-[10px] font-black',
                    tabActivo === tab.clave ? 'bg-orange-100 text-orange-600' : 'bg-gray-200 text-gray-500'
                ]">
                    {{ conteoTab(tab.clave) }}
                </span>
            </button>
        </div>

        <!-- Buscador -->
        <div class="relative w-full max-w-xs">
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input v-model="busqueda" type="text" :placeholder="`Buscar ${etiquetaTab.toLowerCase()}...`"
                class="form-input w-full" style="padding-left: 2.25rem" />
        </div>

        <!-- Tabla Sucursales -->
        <div v-if="tabActivo === 'sucursales'" class="card">
            <div class="table-wrapper">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Ciudad</th>
                            <th>Dirección</th>
                            <th>Teléfono</th>
                            <th>Principal</th>
                            <th>Estado</th>
                            <th class="text-right">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="store.cargando">
                            <td colspan="7">
                                <div class="flex justify-center py-10">
                                    <svg class="w-6 h-6 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4" />
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                    </svg>
                                </div>
                            </td>
                        </tr>
                        <tr v-else-if="!sucursalesFiltradas.length">
                            <td colspan="7" class="text-center py-12 text-gray-400 italic">
                                No se encontraron sucursales
                            </td>
                        </tr>
                        <tr v-for="s in sucursalesFiltradas" :key="s.id">
                            <td class="font-semibold text-gray-900">{{ s.nombre }}</td>
                            <td class="text-gray-600">{{ s.ciudad }}</td>
                            <td class="text-gray-600 max-w-[200px] truncate">{{ s.direccion }}</td>
                            <td class="text-gray-600">{{ s.telefono || '—' }}</td>
                            <td>
                                <span v-if="s.es_principal" class="badge badge-green">Principal</span>
                                <span v-else class="badge badge-gray">Secundaria</span>
                            </td>
                            <td>
                                <span :class="s.activo ? 'badge badge-blue' : 'badge badge-gray'">
                                    {{ s.activo ? 'Activo' : 'Inactivo' }}
                                </span>
                            </td>
                            <td class="text-right">
                                <div class="flex items-center justify-end gap-1">
                                    <button @click="abrirModalEditar(s)"
                                        class="w-8 h-8 rounded-lg hover:bg-blue-50 flex items-center justify-center text-gray-400 hover:text-blue-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                    </button>
                                    <button @click="confirmarEliminar(s)"
                                        class="w-8 h-8 rounded-lg hover:bg-red-50 flex items-center justify-center text-gray-400 hover:text-red-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Tabla Ciudades -->
        <div v-if="tabActivo === 'ciudades'" class="card">
            <div class="table-wrapper">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Departamento</th>
                            <th>Estado</th>
                            <th class="text-right">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="store.cargando">
                            <td colspan="4">
                                <div class="flex justify-center py-10">
                                    <svg class="w-6 h-6 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4" />
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                    </svg>
                                </div>
                            </td>
                        </tr>
                        <tr v-else-if="!ciudadesFiltradas.length">
                            <td colspan="4" class="text-center py-12 text-gray-400 italic">
                                No se encontraron ciudades
                            </td>
                        </tr>
                        <tr v-for="c in ciudadesFiltradas" :key="c.id">
                            <td class="font-semibold text-gray-900">{{ c.nombre }}</td>
                            <td class="text-gray-600">{{ c.departamento }}</td>
                            <td>
                                <span :class="c.activo ? 'badge badge-blue' : 'badge badge-gray'">
                                    {{ c.activo ? 'Activo' : 'Inactivo' }}
                                </span>
                            </td>
                            <td class="text-right">
                                <div class="flex items-center justify-end gap-1">
                                    <button @click="abrirModalEditar(c)"
                                        class="w-8 h-8 rounded-lg hover:bg-blue-50 flex items-center justify-center text-gray-400 hover:text-blue-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                    </button>
                                    <button @click="confirmarEliminar(c)"
                                        class="w-8 h-8 rounded-lg hover:bg-red-50 flex items-center justify-center text-gray-400 hover:text-red-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Tabla Rutas -->
        <div v-if="tabActivo === 'rutas'" class="card">
            <div class="table-wrapper">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Origen</th>
                            <th>Destino</th>
                            <th class="text-right">Precio base</th>
                            <th class="text-center">Duración</th>
                            <th class="text-center">Distancia</th>
                            <th>Estado</th>
                            <th class="text-right">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="store.cargando">
                            <td colspan="7">
                                <div class="flex justify-center py-10">
                                    <svg class="w-6 h-6 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                            stroke-width="4" />
                                        <path class="opacity-75" fill="currentColor"
                                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                    </svg>
                                </div>
                            </td>
                        </tr>
                        <tr v-else-if="!rutasFiltradas.length">
                            <td colspan="7" class="text-center py-12 text-gray-400 italic">
                                No se encontraron rutas
                            </td>
                        </tr>
                        <tr v-for="r in rutasFiltradas" :key="r.id">
                            <td class="font-semibold text-gray-900">{{ r.origen_nombre }}</td>
                            <td class="font-semibold text-gray-900">{{ r.destino_nombre }}</td>
                            <td class="text-right font-black text-gray-900">
                                S/. {{ r.precio_base }}
                            </td>
                            <td class="text-center text-gray-600">{{ r.duracion_horas }} h</td>
                            <td class="text-center text-gray-600">
                                {{ r.distancia_km ? r.distancia_km + ' km' : '—' }}
                            </td>
                            <td>
                                <span :class="r.activo ? 'badge badge-blue' : 'badge badge-gray'">
                                    {{ r.activo ? 'Activo' : 'Inactivo' }}
                                </span>
                            </td>
                            <td class="text-right">
                                <div class="flex items-center justify-end gap-1">
                                    <button @click="abrirModalEditar(r)"
                                        class="w-8 h-8 rounded-lg hover:bg-blue-50 flex items-center justify-center text-gray-400 hover:text-blue-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                    </button>
                                    <button @click="confirmarEliminar(r)"
                                        class="w-8 h-8 rounded-lg hover:bg-red-50 flex items-center justify-center text-gray-400 hover:text-red-600 transition-colors">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ── MODALES ─────────────────────────────────────────── -->

        <!-- Modal Sucursal -->
        <AppModal v-model="modalAbierto" :titulo="tituloModal" ancho="md">
            <form @submit.prevent="guardar" class="space-y-4">

                <template v-if="tabActivo === 'sucursales'">
                    <div>
                        <label class="form-label">Nombre <span class="text-red-500">*</span></label>
                        <input v-model="formulario.nombre" type="text" class="form-input"
                            :class="{ 'form-input-error': errores.nombre }" placeholder="Ej: Sucursal Chiclayo" />
                        <p v-if="errores.nombre" class="form-error">{{ errores.nombre }}</p>
                    </div>
                    <div>
                        <label class="form-label">Ciudad <span class="text-red-500">*</span></label>
                        <input v-model="formulario.ciudad" type="text" class="form-input"
                            :class="{ 'form-input-error': errores.ciudad }" placeholder="Ej: Chiclayo" />
                        <p v-if="errores.ciudad" class="form-error">{{ errores.ciudad }}</p>
                    </div>
                    <div>
                        <label class="form-label">Dirección <span class="text-red-500">*</span></label>
                        <input v-model="formulario.direccion" type="text" class="form-input"
                            :class="{ 'form-input-error': errores.direccion }" placeholder="Ej: Av. Balta 123" />
                        <p v-if="errores.direccion" class="form-error">{{ errores.direccion }}</p>
                    </div>
                    <div>
                        <label class="form-label">Teléfono</label>
                        <input v-model="formulario.telefono" type="text" class="form-input"
                            placeholder="Ej: 074-123456" />
                    </div>
                    <div class="flex items-center gap-3">
                        <input v-model="formulario.es_principal" type="checkbox" id="es_principal"
                            class="w-4 h-4 rounded text-blue-600" />
                        <label for="es_principal" class="text-sm text-gray-700 font-medium">Es sucursal
                            principal</label>
                    </div>
                </template>

                <template v-if="tabActivo === 'ciudades'">
                    <div>
                        <label class="form-label">Nombre <span class="text-red-500">*</span></label>
                        <input v-model="formulario.nombre" type="text" class="form-input"
                            :class="{ 'form-input-error': errores.nombre }" placeholder="Ej: Chiclayo" />
                        <p v-if="errores.nombre" class="form-error">{{ errores.nombre }}</p>
                    </div>
                    <div>
                        <label class="form-label">Departamento <span class="text-red-500">*</span></label>
                        <input v-model="formulario.departamento" type="text" class="form-input"
                            :class="{ 'form-input-error': errores.departamento }" placeholder="Ej: Lambayeque" />
                        <p v-if="errores.departamento" class="form-error">{{ errores.departamento }}</p>
                    </div>
                </template>

                <template v-if="tabActivo === 'rutas'">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="form-label">Origen <span class="text-red-500">*</span></label>
                            <select v-model="formulario.origen" class="form-input"
                                :class="{ 'form-input-error': errores.origen }">
                                <option value="">Seleccionar...</option>
                                <option v-for="c in store.ciudades" :key="c.id" :value="c.id">
                                    {{ c.nombre }}
                                </option>
                            </select>
                            <p v-if="errores.origen" class="form-error">{{ errores.origen }}</p>
                        </div>
                        <div>
                            <label class="form-label">Destino <span class="text-red-500">*</span></label>
                            <select v-model="formulario.destino" class="form-input"
                                :class="{ 'form-input-error': errores.destino }">
                                <option value="">Seleccionar...</option>
                                <option v-for="c in store.ciudades" :key="c.id" :value="c.id">
                                    {{ c.nombre }}
                                </option>
                            </select>
                            <p v-if="errores.destino" class="form-error">{{ errores.destino }}</p>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="form-label">Precio base (S/.) <span class="text-red-500">*</span></label>
                            <input v-model="formulario.precio_base" type="number" step="0.50" min="0" class="form-input"
                                :class="{ 'form-input-error': errores.precio_base }" placeholder="0.00" />
                            <p v-if="errores.precio_base" class="form-error">{{ errores.precio_base }}</p>
                        </div>
                        <div>
                            <label class="form-label">Duración (horas) <span class="text-red-500">*</span></label>
                            <input v-model="formulario.duracion_horas" type="number" step="0.5" min="0"
                                class="form-input" :class="{ 'form-input-error': errores.duracion_horas }"
                                placeholder="0.0" />
                            <p v-if="errores.duracion_horas" class="form-error">{{ errores.duracion_horas }}</p>
                        </div>
                    </div>
                    <div>
                        <label class="form-label">Distancia (km)</label>
                        <input v-model="formulario.distancia_km" type="number" step="0.1" min="0" class="form-input"
                            placeholder="Opcional" />
                        <p class="form-hint">Campo opcional</p>
                    </div>
                </template>

                <!-- Alerta error del servidor -->
                <div v-if="errorServidor"
                    class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                    <svg class="w-4 h-4 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p class="text-xs text-red-700 font-medium">{{ errorServidor }}</p>
                </div>
            </form>

            <template #footer>
                <button @click="modalAbierto = false" class="btn-secondary">
                    Cancelar
                </button>
                <button @click="guardar" :disabled="guardando" class="btn-primary">
                    <svg v-if="guardando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    {{ guardando ? 'Guardando...' : (modoEdicion ? 'Actualizar' : 'Guardar') }}
                </button>
            </template>
        </AppModal>

        <!-- Modal confirmación eliminar -->
        <AppModal v-model="modalEliminar" titulo="Confirmar eliminación" ancho="sm">
            <div class="text-center py-2">
                <div class="w-12 h-12 rounded-2xl bg-red-50 flex items-center justify-center mx-auto mb-3">
                    <svg class="w-6 h-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                </div>
                <p class="text-sm font-bold text-gray-900 mb-1">¿Eliminar este registro?</p>
                <p class="text-xs text-gray-500">Esta acción no se puede deshacer.</p>
            </div>
            <template #footer>
                <button @click="modalEliminar = false" class="btn-secondary">Cancelar</button>
                <button @click="eliminar" :disabled="guardando" class="btn-danger">
                    {{ guardando ? 'Eliminando...' : 'Sí, eliminar' }}
                </button>
            </template>
        </AppModal>

    </div>
</template>

<script setup>
import { ref, computed, reactive, watch, onMounted } from 'vue'
import { useUbicacionesStore } from '../stores/ubicaciones.store'
import { ubicacionesService } from '../services/ubicaciones.service'

import AppModal from '@/components/common/AppModal.vue'


const store = useUbicacionesStore()
const tabActivo = ref('sucursales')
const busqueda = ref('')
const modalAbierto = ref(false)
const modalEliminar = ref(false)
const modoEdicion = ref(false)
const guardando = ref(false)
const errorServidor = ref('')
const itemSeleccionado = ref(null)

const tabs = [
    { clave: 'sucursales', etiqueta: 'Sucursales' },
    { clave: 'ciudades', etiqueta: 'Ciudades' },
    { clave: 'rutas', etiqueta: 'Rutas' },
]

// ── Formulario dinámico ──────────────────────────────────
const formulario = reactive({
    nombre: '', ciudad: '', direccion: '', telefono: '',
    es_principal: false, departamento: '',
    origen: '', destino: '', precio_base: '',
    duracion_horas: '', distancia_km: '',
})

const errores = reactive({
    nombre: '', ciudad: '', direccion: '', departamento: '',
    origen: '', destino: '', precio_base: '', duracion_horas: '',
})

// ── Computed ─────────────────────────────────────────────
const etiquetaTab = computed(() =>
    tabs.find(t => t.clave === tabActivo.value)?.etiqueta.slice(0, -1) || ''
)

const tituloModal = computed(() =>
    `${modoEdicion.value ? 'Editar' : 'Nuevo'} ${etiquetaTab.value}`
)

const conteoTab = (clave) => ({
    sucursales: store.sucursales.length,
    ciudades: store.ciudades.length,
    rutas: store.rutas.length,
}[clave] || 0)

const sucursalesFiltradas = computed(() =>
    store.sucursales.filter(s =>
        s.nombre.toLowerCase().includes(busqueda.value.toLowerCase()) ||
        s.ciudad.toLowerCase().includes(busqueda.value.toLowerCase())
    )
)

const ciudadesFiltradas = computed(() =>
    store.ciudades.filter(c =>
        c.nombre.toLowerCase().includes(busqueda.value.toLowerCase()) ||
        c.departamento.toLowerCase().includes(busqueda.value.toLowerCase())
    )
)

const rutasFiltradas = computed(() =>
    store.rutas.filter(r =>
        r.origen_nombre?.toLowerCase().includes(busqueda.value.toLowerCase()) ||
        r.destino_nombre?.toLowerCase().includes(busqueda.value.toLowerCase())
    )
)

// ── Cargar datos al cambiar tab ──────────────────────────
watch(tabActivo, (nuevo) => {
    busqueda.value = ''
    cargarTab(nuevo)
}, { immediate: false })

function cargarTab(tab) {
    if (tab === 'sucursales') store.cargarSucursales()
    if (tab === 'ciudades') store.cargarCiudades()
    if (tab === 'rutas') {
        store.cargarRutas()
        store.cargarCiudades() // necesario para el select
    }
}

// ── Acciones Modal ───────────────────────────────────────
function limpiarFormulario() {
    Object.keys(formulario).forEach(k => {
        formulario[k] = k === 'es_principal' ? false : ''
    })
    Object.keys(errores).forEach(k => errores[k] = '')
    errorServidor.value = ''
}

function abrirModalCrear() {
    modoEdicion.value = false
    limpiarFormulario()
    modalAbierto.value = true
}

function abrirModalEditar(item) {
    modoEdicion.value = true
    itemSeleccionado.value = item
    limpiarFormulario()

    if (tabActivo.value === 'sucursales') {
        Object.assign(formulario, {
            nombre: item.nombre, ciudad: item.ciudad,
            direccion: item.direccion, telefono: item.telefono || '',
            es_principal: item.es_principal,
        })
    } else if (tabActivo.value === 'ciudades') {
        Object.assign(formulario, {
            nombre: item.nombre, departamento: item.departamento,
        })
    } else if (tabActivo.value === 'rutas') {
        Object.assign(formulario, {
            origen: item.origen, destino: item.destino,
            precio_base: item.precio_base, duracion_horas: item.duracion_horas,
            distancia_km: item.distancia_km || '',
        })
    }

    modalAbierto.value = true
}

function confirmarEliminar(item) {
    itemSeleccionado.value = item
    modalEliminar.value = true
}

// ── Validaciones ─────────────────────────────────────────
function validar() {
    let valido = true
    Object.keys(errores).forEach(k => errores[k] = '')

    if (tabActivo.value === 'sucursales') {
        if (!formulario.nombre) { errores.nombre = 'Obligatorio'; valido = false }
        if (!formulario.ciudad) { errores.ciudad = 'Obligatorio'; valido = false }
        if (!formulario.direccion) { errores.direccion = 'Obligatorio'; valido = false }
    }
    if (tabActivo.value === 'ciudades') {
        if (!formulario.nombre) { errores.nombre = 'Obligatorio'; valido = false }
        if (!formulario.departamento) { errores.departamento = 'Obligatorio'; valido = false }
    }
    if (tabActivo.value === 'rutas') {
        if (!formulario.origen) { errores.origen = 'Obligatorio'; valido = false }
        if (!formulario.destino) { errores.destino = 'Obligatorio'; valido = false }
        if (!formulario.precio_base) { errores.precio_base = 'Obligatorio'; valido = false }
        if (!formulario.duracion_horas) { errores.duracion_horas = 'Obligatorio'; valido = false }
        if (formulario.origen === formulario.destino && formulario.origen) {
            errores.destino = 'El destino no puede ser igual al origen'
            valido = false
        }
    }

    return valido
}

// ── Guardar ──────────────────────────────────────────────
async function guardar() {
    if (!validar()) return

    guardando.value = true
    errorServidor.value = ''

    try {
        // Construir payload según tab activo
        let payload = {}

        if (tabActivo.value === 'sucursales') {
            payload = {
                nombre: formulario.nombre,
                ciudad: formulario.ciudad,
                direccion: formulario.direccion,
                telefono: formulario.telefono,
                es_principal: formulario.es_principal,
            }
        } else if (tabActivo.value === 'ciudades') {
            payload = {
                nombre: formulario.nombre,
                departamento: formulario.departamento,
            }
        } else if (tabActivo.value === 'rutas') {
            payload = {
                origen: formulario.origen,
                destino: formulario.destino,
                precio_base: formulario.precio_base,
                duracion_horas: formulario.duracion_horas,
                distancia_km: formulario.distancia_km || null,
            }
        }

        // Llamar servicio correcto
        if (tabActivo.value === 'sucursales') {
            modoEdicion.value
                ? await ubicacionesService.actualizarSucursal(itemSeleccionado.value.id, payload)
                : await ubicacionesService.crearSucursal(payload)
        } else if (tabActivo.value === 'ciudades') {
            modoEdicion.value
                ? await ubicacionesService.actualizarCiudad(itemSeleccionado.value.id, payload)
                : await ubicacionesService.crearCiudad(payload)
        } else if (tabActivo.value === 'rutas') {
            modoEdicion.value
                ? await ubicacionesService.actualizarRuta(itemSeleccionado.value.id, payload)
                : await ubicacionesService.crearRuta(payload)
        }

        modalAbierto.value = false
        cargarTab(tabActivo.value)

    } catch (e) {
        console.error('Error al guardar:', e.response?.data)
        const data = e.response?.data
        if (data && typeof data === 'object') {
            Object.keys(data).forEach(k => {
                if (k in errores) {
                    errores[k] = Array.isArray(data[k]) ? data[k][0] : data[k]
                }
            })
        }
        errorServidor.value = 'Verifica los campos e intenta de nuevo.'
    } finally {
        guardando.value = false
    }
}

// ── Eliminar ─────────────────────────────────────────────
async function eliminar() {
    guardando.value = true
    const eliminar = `eliminar${etiquetaTab.value}`
    try {
        await ubicacionesService[eliminar](itemSeleccionado.value.id)
        modalEliminar.value = false
        cargarTab(tabActivo.value)
    } catch {
        errorServidor.value = 'No se pudo eliminar. Puede estar en uso.'
    } finally {
        guardando.value = false
    }
}

// ── Inicializar ──────────────────────────────────────────
onMounted(() => {
    store.cargarSucursales()
})
</script>