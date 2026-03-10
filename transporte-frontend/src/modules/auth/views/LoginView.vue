<template>
  <div class="login-page">

    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <div class="login-card">

      <!-- Logo -->
      <div class="card-logo">
        <img src="/logo1.png" alt="WJL" class="logo-img" @error="e => e.target.style.display='none'" />
      </div>

      <div class="card-top">
        <h1 class="card-title">Bienvenido</h1>
        <p class="card-sub">Sistema de Gestión</p>
      </div>

      <!-- Alerta error -->
      <Transition name="slide-down">
        <div v-if="errorMensaje" class="alert-error">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span>{{ errorMensaje }}</span>
        </div>
      </Transition>

      <form @submit.prevent="manejarLogin" class="login-form">

        <!-- Correo -->
        <div class="field">
          <label class="field-label">Correo electrónico</label>
          <div class="field-wrap">
            <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            <input
              v-model="formulario.correo"
              type="email"
              autocomplete="email"
              placeholder="ejemplo@correo.com"
              :class="['field-input', errores.correo ? 'field-input--error' : '']"
              @input="errores.correo = ''"
            />
          </div>
          <p v-if="errores.correo" class="field-error">{{ errores.correo }}</p>
        </div>

        <!-- Contraseña -->
        <div class="field">
          <label class="field-label">Contraseña</label>
          <div class="field-wrap">
            <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
            <input
              v-model="formulario.password"
              :type="mostrarPassword ? 'text' : 'password'"
              autocomplete="current-password"
              placeholder="••••••••"
              :class="['field-input', errores.password ? 'field-input--error' : '']"
              @input="errores.password = ''"
            />
            <button type="button" class="field-toggle" @click="mostrarPassword = !mostrarPassword">
              <svg v-if="!mostrarPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
              </svg>
            </button>
          </div>
          <p v-if="errores.password" class="field-error">{{ errores.password }}</p>
        </div>

        <button type="submit" :disabled="cargando" class="btn-login">
          <svg v-if="cargando" class="spin" viewBox="0 0 24 24" fill="none">
            <circle style="opacity:.25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path style="opacity:.75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
          </svg>
          {{ cargando ? 'Ingresando...' : 'Ingresar al sistema' }}
        </button>

      </form>

      <p class="card-footer">© {{ anioActual }} Turismo WJL · Sistema</p>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const router    = useRouter()
const authStore = useAuthStore()

const cargando        = ref(false)
const mostrarPassword = ref(false)
const errorMensaje    = ref('')
const anioActual      = new Date().getFullYear()

const formulario = reactive({ correo: '', password: '' })
const errores    = reactive({ correo: '', password: '' })

function validar() {
  let valido = true
  if (!formulario.correo) {
    errores.correo = 'El correo es obligatorio.'; valido = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formulario.correo)) {
    errores.correo = 'Ingresa un correo válido.'; valido = false
  }
  if (!formulario.password) {
    errores.password = 'La contraseña es obligatoria.'; valido = false
  } else if (formulario.password.length < 6) {
    errores.password = 'Mínimo 6 caracteres.'; valido = false
  }
  return valido
}

async function manejarLogin() {
  errorMensaje.value = ''
  if (!validar()) return
  cargando.value = true
  try {
    await authStore.iniciarSesion(formulario.correo, formulario.password)
    router.push({ name: 'dashboard', state: { bienvenida: true } })
  } catch (error) {
    const status = error.response?.status
    if      (status === 401) errorMensaje.value = 'Correo o contraseña incorrectos.'
    else if (status === 400) errorMensaje.value = 'Datos inválidos. Verifica tu correo y contraseña.'
    else                     errorMensaje.value = 'Error de conexión. Intenta nuevamente.'
  } finally {
    cargando.value = false
  }
}
</script>

<style scoped>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
  background: #f1f5f9;
  position: relative;
  overflow: hidden;
}

/* Fondo */
.bg-shapes { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.shape { position: absolute; border-radius: 50%; filter: blur(90px); opacity: 0.09; animation: float 10s ease-in-out infinite; }
.shape-1 { width: 500px; height: 500px; background: #1d4ed8; top: -150px; left: -150px; animation-delay: 0s; }
.shape-2 { width: 350px; height: 350px; background: #dc2626; bottom: -80px; right: -80px; animation-delay: -4s; }
.shape-3 { width: 250px; height: 250px; background: #1d4ed8; top: 50%; left: 65%; animation-delay: -7s; }
@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50%       { transform: translate(18px, -18px); }
}

/* Card */
.login-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06), 0 20px 60px -10px rgba(0,0,0,0.12);
  padding: 36px 32px 28px;
  position: relative;
  z-index: 1;
  animation: card-in 0.45s ease both;
}
@keyframes card-in {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Logo */
.card-logo {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}
.logo-img {
  width: 140px;
  height: auto;
  object-fit: contain;
}

/* Títulos */
.card-top { text-align: center; margin-bottom: 24px; }
.card-title { font-size: 26px; font-weight: 900; color: #0f172a; letter-spacing: -0.5px; margin-bottom: 4px; }
.card-sub   { font-size: 13px; color: #94a3b8; font-weight: 500; }

/* Alert */
.alert-error {
  display: flex; align-items: center; gap: 10px;
  background: #fef2f2; border: 1px solid #fecaca;
  border-radius: 12px; padding: 11px 14px; margin-bottom: 18px;
  font-size: 13px; color: #b91c1c; font-weight: 500;
}
.alert-error svg { width: 16px; height: 16px; flex-shrink: 0; }

/* Form */
.login-form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 13px; font-weight: 700; color: #374151; }
.field-wrap { position: relative; display: flex; align-items: center; }
.field-icon {
  position: absolute; left: 13px;
  width: 16px; height: 16px;
  color: #94a3b8; pointer-events: none;
}
.field-input {
  width: 100%;
  padding: 11px 14px 11px 38px;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px; color: #0f172a;
  background: #f8fafc;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}
.field-input:focus {
  border-color: #1d4ed8;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(29,78,216,0.08);
}
.field-input--error { border-color: #f87171; background: #fff; }
.field-input--error:focus { box-shadow: 0 0 0 3px rgba(248,113,113,0.12); }
.field-toggle {
  position: absolute; right: 12px;
  background: none; border: none; cursor: pointer; padding: 4px;
  color: #94a3b8; display: flex; align-items: center;
  transition: color 0.15s;
}
.field-toggle:hover { color: #475569; }
.field-toggle svg { width: 16px; height: 16px; }
.field-error { font-size: 12px; color: #dc2626; font-weight: 500; }

/* Botón */
.btn-login {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  width: 100%; padding: 13px 20px; margin-top: 4px;
  background: linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%);
  color: #fff; font-size: 15px; font-weight: 700;
  border: none; border-radius: 12px; cursor: pointer;
  box-shadow: 0 6px 20px rgba(29,78,216,0.28);
  transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s;
}
.btn-login:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 10px 28px rgba(29,78,216,0.36); }
.btn-login:active:not(:disabled) { transform: translateY(0); }
.btn-login:disabled { opacity: 0.65; cursor: not-allowed; }
.btn-login svg { width: 18px; height: 18px; }
.spin { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Footer */
.card-footer { text-align: center; font-size: 11px; color: #cbd5e1; font-weight: 500; margin-top: 24px; }

/* Transitions */
.slide-down-enter-active, .slide-down-leave-active { transition: all 0.25s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-8px); }
</style>