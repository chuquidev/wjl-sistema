<template>
    <div class="space-y-6">

        <div class="page-header">
            <div>
                <h1 class="page-title">Mi Perfil</h1>
                <p class="page-subtitle">Gestiona tu información personal y seguridad</p>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

            <!-- Columna izquierda: avatar + info fija -->
            <div class="space-y-4">

                <div class="card">
                    <div class="card-body flex flex-col items-center gap-4 py-8">
                        <div class="relative">
                            <div class="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center shadow-lg">
                                <span class="text-3xl font-black text-white select-none">{{ iniciales }}</span>
                            </div>
                            <span class="absolute -bottom-1 -right-1 w-7 h-7 rounded-full border-2 border-white flex items-center justify-center"
                                :class="usuario?.rol === 'administrador' ? 'bg-orange-500' : 'bg-emerald-500'">
                                <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path v-if="usuario?.rol === 'administrador'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                                        d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                            </span>
                        </div>
                        <div class="text-center">
                            <p class="font-black text-gray-900 text-lg leading-tight">{{ usuario?.nombre_completo }}</p>
                            <p class="text-sm text-gray-400 mt-0.5">{{ usuario?.correo }}</p>
                            <span class="inline-block mt-2 px-3 py-1 rounded-full text-xs font-black uppercase tracking-wide"
                                :class="usuario?.rol === 'administrador' ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700'">
                                {{ usuario?.rol_display || usuario?.rol }}
                            </span>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Información del sistema</h3>
                    </div>
                    <div class="card-body space-y-1">
                        <div class="flex justify-between items-center py-2 border-b border-gray-50">
                            <span class="text-sm text-gray-500">DNI</span>
                            <span class="font-mono font-bold text-gray-800 text-sm">{{ usuario?.dni || '—' }}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-gray-50">
                            <span class="text-sm text-gray-500">Rol</span>
                            <span class="font-bold text-gray-800 text-sm">{{ usuario?.rol_display || '—' }}</span>
                        </div>
                        <div class="flex justify-between items-center py-2">
                            <span class="text-sm text-gray-500">Sucursal</span>
                            <span class="font-bold text-gray-800 text-sm">{{ sucursalNombre }}</span>
                        </div>
                    </div>
                </div>

            </div>

            <!-- Columna derecha: formularios -->
            <div class="lg:col-span-2 space-y-5">

                <!-- Datos personales -->
                <div class="card">
                    <div class="card-header">
                        <div class="flex items-center gap-2">
                            <div class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
                                <svg class="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                            </div>
                            <h3 class="card-title">Datos personales</h3>
                        </div>
                    </div>
                    <div class="card-body space-y-4">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="form-label">Nombres <span class="text-red-500">*</span></label>
                                <input v-model="formPerfil.nombres" type="text" class="form-input"
                                    :class="{ 'form-input-error': erroresPerfil.nombres }"
                                    placeholder="Ej: Juan Carlos" />
                                <p v-if="erroresPerfil.nombres" class="form-error">{{ erroresPerfil.nombres }}</p>
                            </div>
                            <div>
                                <label class="form-label">Apellidos <span class="text-red-500">*</span></label>
                                <input v-model="formPerfil.apellidos" type="text" class="form-input"
                                    :class="{ 'form-input-error': erroresPerfil.apellidos }"
                                    placeholder="Ej: López Torres" />
                                <p v-if="erroresPerfil.apellidos" class="form-error">{{ erroresPerfil.apellidos }}</p>
                            </div>
                        </div>
                        <div>
                            <label class="form-label">Teléfono</label>
                            <input v-model="formPerfil.telefono" type="text" class="form-input"
                                placeholder="Ej: 987654321" maxlength="15" />
                            <p class="form-hint">Opcional</p>
                        </div>
                        <div>
                            <label class="form-label">Correo electrónico</label>
                            <input :value="usuario?.correo" type="email"
                                class="form-input bg-gray-50 cursor-not-allowed" disabled />
                            <p class="form-hint">El correo no puede modificarse</p>
                        </div>

                        <div v-if="alertaPerfil.mensaje" :class="[
                            'flex items-center gap-2 p-3 rounded-xl text-sm font-medium',
                            alertaPerfil.tipo === 'exito'
                                ? 'bg-emerald-50 border border-emerald-200 text-emerald-700'
                                : 'bg-red-50 border border-red-200 text-red-700'
                        ]">
                            <svg v-if="alertaPerfil.tipo === 'exito'" class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                            </svg>
                            <svg v-else class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {{ alertaPerfil.mensaje }}
                        </div>

                        <div class="flex justify-end pt-2">
                            <button @click="guardarPerfil" :disabled="guardandoPerfil" class="btn-primary">
                                <svg v-if="guardandoPerfil" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                </svg>
                                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                                {{ guardandoPerfil ? 'Guardando...' : 'Guardar cambios' }}
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Cambiar contraseña -->
                <div class="card">
                    <div class="card-header">
                        <div class="flex items-center gap-2">
                            <div class="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center">
                                <svg class="w-4 h-4 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </div>
                            <h3 class="card-title">Cambiar contraseña</h3>
                        </div>
                    </div>
                    <div class="card-body space-y-4">
                        <div>
                            <label class="form-label">Contraseña actual <span class="text-red-500">*</span></label>
                            <div class="relative">
                                <input v-model="formPassword.actual"
                                    :type="mostrarActual ? 'text' : 'password'"
                                    class="form-input pr-10"
                                    :class="{ 'form-input-error': erroresPassword.actual }"
                                    placeholder="Tu contraseña actual" />
                                <button type="button" @click="mostrarActual = !mostrarActual"
                                    class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path v-if="mostrarActual" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                                        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                    </svg>
                                </button>
                            </div>
                            <p v-if="erroresPassword.actual" class="form-error">{{ erroresPassword.actual }}</p>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="form-label">Nueva contraseña <span class="text-red-500">*</span></label>
                                <div class="relative">
                                    <input v-model="formPassword.nueva"
                                        :type="mostrarNueva ? 'text' : 'password'"
                                        class="form-input pr-10"
                                        :class="{ 'form-input-error': erroresPassword.nueva }"
                                        placeholder="Mínimo 8 caracteres" />
                                    <button type="button" @click="mostrarNueva = !mostrarNueva"
                                        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path v-if="mostrarNueva" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                                            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                    </button>
                                </div>
                                <p v-if="erroresPassword.nueva" class="form-error">{{ erroresPassword.nueva }}</p>
                            </div>
                            <div>
                                <label class="form-label">Confirmar contraseña <span class="text-red-500">*</span></label>
                                <div class="relative">
                                    <input v-model="formPassword.confirmar"
                                        :type="mostrarConfirmar ? 'text' : 'password'"
                                        class="form-input pr-10"
                                        :class="{ 'form-input-error': erroresPassword.confirmar }"
                                        placeholder="Repite la nueva contraseña" />
                                    <button type="button" @click="mostrarConfirmar = !mostrarConfirmar"
                                        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path v-if="mostrarConfirmar" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                                            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                    </button>
                                </div>
                                <p v-if="erroresPassword.confirmar" class="form-error">{{ erroresPassword.confirmar }}</p>
                            </div>
                        </div>

                        <!-- Indicador fortaleza -->
                        <div v-if="formPassword.nueva" class="space-y-1.5">
                            <div class="flex gap-1.5">
                                <div v-for="i in 4" :key="i"
                                    class="h-1.5 flex-1 rounded-full transition-all duration-300"
                                    :class="i <= fuerzaPassword ? colorFuerza : 'bg-gray-100'"></div>
                            </div>
                            <p class="text-xs font-semibold" :class="textoColorFuerza">{{ etiquetaFuerza }}</p>
                        </div>

                        <div v-if="alertaPassword.mensaje" :class="[
                            'flex items-center gap-2 p-3 rounded-xl text-sm font-medium',
                            alertaPassword.tipo === 'exito'
                                ? 'bg-emerald-50 border border-emerald-200 text-emerald-700'
                                : 'bg-red-50 border border-red-200 text-red-700'
                        ]">
                            <svg v-if="alertaPassword.tipo === 'exito'" class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                            </svg>
                            <svg v-else class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {{ alertaPassword.mensaje }}
                        </div>

                        <div class="flex justify-end pt-2">
                            <button @click="cambiarPassword" :disabled="guardandoPassword" class="btn-primary">
                                <svg v-if="guardandoPassword" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                </svg>
                                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                                {{ guardandoPassword ? 'Cambiando...' : 'Cambiar contraseña' }}
                            </button>
                        </div>
                    </div>
                </div>

            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '@/services/api'

const usuario           = ref(null)
const guardandoPerfil   = ref(false)
const guardandoPassword = ref(false)
const mostrarActual     = ref(false)
const mostrarNueva      = ref(false)
const mostrarConfirmar  = ref(false)

const alertaPerfil   = reactive({ mensaje: '', tipo: '' })
const alertaPassword = reactive({ mensaje: '', tipo: '' })

const formPerfil      = reactive({ nombres: '', apellidos: '', telefono: '' })
const erroresPerfil   = reactive({ nombres: '', apellidos: '' })
const formPassword    = reactive({ actual: '', nueva: '', confirmar: '' })
const erroresPassword = reactive({ actual: '', nueva: '', confirmar: '' })

const iniciales = computed(() => {
    if (!usuario.value) return 'U'
    const n = usuario.value.nombres?.[0]   || ''
    const a = usuario.value.apellidos?.[0] || ''
    return (n + a).toUpperCase() || 'U'
})

const sucursalNombre = computed(() => {
    const s = usuario.value?.sucursal_nombre || usuario.value?.sucursal
    if (!s) return '—'
    return typeof s === 'object' ? s.nombre : s
})

const fuerzaPassword = computed(() => {
    const p = formPassword.nueva
    if (!p) return 0
    let score = 0
    if (p.length >= 8)           score++
    if (/[A-Z]/.test(p))         score++
    if (/[0-9]/.test(p))         score++
    if (/[^A-Za-z0-9]/.test(p))  score++
    return score
})

const colorFuerza = computed(() =>
    ['bg-red-400', 'bg-orange-400', 'bg-amber-400', 'bg-emerald-500'][fuerzaPassword.value - 1] || 'bg-red-400'
)
const textoColorFuerza = computed(() =>
    ['text-red-500', 'text-orange-500', 'text-amber-500', 'text-emerald-600'][fuerzaPassword.value - 1] || 'text-red-500'
)
const etiquetaFuerza = computed(() =>
    ['Muy débil', 'Débil', 'Regular', 'Fuerte'][fuerzaPassword.value - 1] || 'Muy débil'
)

async function cargarPerfil() {
    try {
        const { data }        = await api.get('/usuarios/perfil/')
        usuario.value         = data
        formPerfil.nombres    = data.nombres   || ''
        formPerfil.apellidos  = data.apellidos || ''
        formPerfil.telefono   = data.telefono  || ''
        localStorage.setItem('usuario', JSON.stringify(data))
    } catch {
        const local = localStorage.getItem('usuario')
        if (local) {
            const u               = JSON.parse(local)
            usuario.value         = u
            formPerfil.nombres    = u.nombres   || ''
            formPerfil.apellidos  = u.apellidos || ''
            formPerfil.telefono   = u.telefono  || ''
        }
    }
}

function validarPerfil() {
    erroresPerfil.nombres   = ''
    erroresPerfil.apellidos = ''
    let valido = true
    if (!formPerfil.nombres.trim())   { erroresPerfil.nombres   = 'Obligatorio'; valido = false }
    if (!formPerfil.apellidos.trim()) { erroresPerfil.apellidos = 'Obligatorio'; valido = false }
    return valido
}

async function guardarPerfil() {
    if (!validarPerfil()) return
    guardandoPerfil.value = true
    alertaPerfil.mensaje  = ''
    try {
        const { data } = await api.patch('/usuarios/perfil/', {
            nombres:   formPerfil.nombres.trim(),
            apellidos: formPerfil.apellidos.trim(),
            telefono:  formPerfil.telefono.trim(),
        })
        usuario.value = data
        localStorage.setItem('usuario', JSON.stringify(data))
        alertaPerfil.tipo    = 'exito'
        alertaPerfil.mensaje = 'Datos actualizados correctamente.'
        setTimeout(() => { alertaPerfil.mensaje = '' }, 4000)
    } catch (e) {
        alertaPerfil.tipo    = 'error'
        alertaPerfil.mensaje = e.response?.data?.detail || 'Error al guardar los datos.'
    } finally {
        guardandoPerfil.value = false
    }
}

function validarPassword() {
    erroresPassword.actual    = ''
    erroresPassword.nueva     = ''
    erroresPassword.confirmar = ''
    let valido = true
    if (!formPassword.actual) {
        erroresPassword.actual = 'Ingresa tu contraseña actual'; valido = false
    }
    if (!formPassword.nueva) {
        erroresPassword.nueva = 'Ingresa la nueva contraseña'; valido = false
    } else if (formPassword.nueva.length < 8) {
        erroresPassword.nueva = 'Mínimo 8 caracteres'; valido = false
    }
    if (!formPassword.confirmar) {
        erroresPassword.confirmar = 'Confirma la nueva contraseña'; valido = false
    } else if (formPassword.nueva !== formPassword.confirmar) {
        erroresPassword.confirmar = 'Las contraseñas no coinciden'; valido = false
    }
    return valido
}

async function cambiarPassword() {
    if (!validarPassword()) return
    guardandoPassword.value = true
    alertaPassword.mensaje  = ''
    try {
        await api.post('/usuarios/cambiar_password/', {
            password_actual:    formPassword.actual,
            password_nuevo:     formPassword.nueva,
            confirmar_password: formPassword.confirmar,
        })
        alertaPassword.tipo    = 'exito'
        alertaPassword.mensaje = 'Contraseña cambiada correctamente.'
        formPassword.actual    = ''
        formPassword.nueva     = ''
        formPassword.confirmar = ''
        setTimeout(() => { alertaPassword.mensaje = '' }, 4000)
    } catch (e) {
        const data = e.response?.data
        alertaPassword.tipo    = 'error'
        alertaPassword.mensaje = (
            data?.password_actual?.[0]  ||
            data?.detail                ||
            data?.non_field_errors?.[0] ||
            'Error al cambiar la contraseña.'
        )
    } finally {
        guardandoPassword.value = false
    }
}

onMounted(cargarPerfil)
</script>