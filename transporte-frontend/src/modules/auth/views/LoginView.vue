<template>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div class="w-full max-w-md">

            <!-- Logo y título -->
            <div class="text-center mb-8">
                <div
                    class="w-14 h-14 rounded-2xl bg-orange-500 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-orange-200">
                    <svg class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                    </svg>
                </div>
                <h1 class="text-2xl font-black text-gray-900 tracking-tight">Turismo WJL</h1>
                <p class="text-sm text-gray-500 mt-1 font-medium">Sistema de Gestión</p>
            </div>

            <!-- Card del formulario -->
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Iniciar sesión</h2>
                    <span class="text-xs text-gray-400 font-medium">Ingresa tus credenciales</span>
                </div>

                <div class="card-body">
                    <!-- Alerta de error -->
                    <Transition name="fade">
                        <div v-if="errorMensaje"
                            class="flex items-center gap-3 p-3 mb-5 rounded-lg bg-red-50 border border-red-200">
                            <svg class="w-4 h-4 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p class="text-sm text-red-700 font-medium">{{ errorMensaje }}</p>
                        </div>
                    </Transition>

                    <form @submit.prevent="manejarLogin" class="space-y-4">
                        <!-- Correo -->
                        <div>
                            <label class="form-label">Correo electrónico</label>
                            <input v-model="formulario.correo" type="email" autocomplete="email"
                                placeholder="ejemplo@correo.com"
                                :class="['form-input', errores.correo ? 'form-input-error' : '']"
                                @input="errores.correo = ''" />
                            <p v-if="errores.correo" class="form-error">{{ errores.correo }}</p>
                        </div>

                        <!-- Contraseña -->
                        <div>
                            <label class="form-label">Contraseña</label>
                            <div class="relative">
                                <input v-model="formulario.password" :type="mostrarPassword ? 'text' : 'password'"
                                    autocomplete="current-password" placeholder="••••••••"
                                    :class="['form-input pr-10', errores.password ? 'form-input-error' : '']"
                                    @input="errores.password = ''" />
                                <button type="button" @click="mostrarPassword = !mostrarPassword"
                                    class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors">
                                    <!-- Ojo abierto -->
                                    <svg v-if="!mostrarPassword" class="w-4 h-4" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                    </svg>
                                    <!-- Ojo cerrado -->
                                    <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                                    </svg>
                                </button>
                            </div>
                            <p v-if="errores.password" class="form-error">{{ errores.password }}</p>
                        </div>

                        <!-- Botón submit -->
                        <button type="submit" :disabled="cargando"
                            class="btn-primary w-full justify-center py-2.5 mt-2">
                            <svg v-if="cargando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4" />
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                            </svg>
                            <span>{{ cargando ? 'Ingresando...' : 'Ingresar' }}</span>
                        </button>
                    </form>
                </div>
            </div>

            <!-- Footer -->
            <p class="text-center text-xs text-gray-400 mt-6 font-medium">
                © {{ anioActual }} Turismo WJL · Sistema interno
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/auth.store'


const router = useRouter()
const authStore = useAuthStore()

const cargando = ref(false)
const mostrarPassword = ref(false)
const errorMensaje = ref('')
const anioActual = new Date().getFullYear()

const formulario = reactive({
    correo: '',
    password: '',
})

const errores = reactive({
    correo: '',
    password: '',
})

function validar() {
    let valido = true

    if (!formulario.correo) {
        errores.correo = 'El correo es obligatorio.'
        valido = false
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formulario.correo)) {
        errores.correo = 'Ingresa un correo válido.'
        valido = false
    }

    if (!formulario.password) {
        errores.password = 'La contraseña es obligatoria.'
        valido = false
    } else if (formulario.password.length < 6) {
        errores.password = 'Mínimo 6 caracteres.'
        valido = false
    }

    return valido
}

async function manejarLogin() {
    errorMensaje.value = ''
    if (!validar()) return
    cargando.value = true

    try {
        await authStore.iniciarSesion(formulario.correo, formulario.password)

        router.push({
            name: 'dashboard',
            state: { bienvenida: true }  // 👈 dentro del objeto
        })

    } catch (error) {
        const status = error.response?.status

        if (status === 401) {
            errorMensaje.value = 'Correo o contraseña incorrectos.'
        } else if (status === 400) {
            errorMensaje.value = 'Datos inválidos. Verifica tu correo y contraseña.'
        } else {
            errorMensaje.value = 'Error de conexión. Intenta nuevamente.'
        }
    } finally {
        cargando.value = false
    }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-4px);
}
</style>