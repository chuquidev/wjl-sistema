import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

const INACTIVIDAD_MS = 60 * 60 * 1000 // 1 hora en ms

export const useAuthStore = defineStore('auth', () => {
    const token        = ref(localStorage.getItem('token') || null)
    const refreshToken = ref(localStorage.getItem('refresh_token') || null)
    const usuario      = ref(JSON.parse(localStorage.getItem('usuario') || 'null'))
    let   _timer       = null

    const estaAutenticado = computed(() => !!token.value)
    const esAdmin         = computed(() => usuario.value?.rol === 'administrador')
    const esSupervisor    = computed(() => usuario.value?.rol === 'supervisor')
    const esCajero        = computed(() => usuario.value?.rol === 'cajero')
    const nombre_completo = computed(() => {
        if (!usuario.value) return ''
        return `${usuario.value.nombres} ${usuario.value.apellidos}`
    })

    function _iniciarTimerInactividad() {
        _limpiarTimer()
        console.log('Timer inactividad iniciado: 1 hora')
        _timer = setTimeout(() => {
            console.log('Inactividad detectada, cerrando sesión...')
            cerrarSesion()
            window.location.href = '/login'
        }, INACTIVIDAD_MS)
    }

    function _limpiarTimer() {
        if (_timer) {
            clearTimeout(_timer)
            _timer = null
        }
    }

    // Escucha eventos del usuario y reinicia el timer
    function _escucharActividad() {
        const eventos = ['mousemove', 'keydown', 'click', 'scroll', 'touchstart']
        const resetear = () => {
            if (token.value) {
                _iniciarTimerInactividad()
            }
        }
        eventos.forEach(evento => window.addEventListener(evento, resetear))
    }

    async function iniciarSesion(correo, password) {
        const { data } = await api.post('/auth/token/', { correo, password })
        token.value        = data.access
        refreshToken.value = data.refresh
        localStorage.setItem('token', data.access)
        localStorage.setItem('refresh_token', data.refresh)
        console.log('Sesión iniciada')
        _iniciarTimerInactividad()
        _escucharActividad()
        await cargarPerfil()
    }

    async function cargarPerfil() {
        const { data } = await api.get('/usuarios/perfil/')
        usuario.value  = data
        localStorage.setItem('usuario', JSON.stringify(data))
    }

    function setToken(nuevoToken) {
        token.value = nuevoToken
        localStorage.setItem('token', nuevoToken)
        console.log('Token renovado')
    }

    function cerrarSesion() {
        console.log('Cerrando sesión...')
        _limpiarTimer()
        token.value        = null
        refreshToken.value = null
        usuario.value      = null
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('usuario')
    }

    // Si recarga la página con sesión activa
    if (token.value) {
        console.log('Sesión activa encontrada, escuchando actividad...')
        _iniciarTimerInactividad()
        _escucharActividad()
    }

    return {
        token, refreshToken, usuario,
        estaAutenticado, esAdmin, esSupervisor, esCajero,
        nombre_completo,
        iniciarSesion, cargarPerfil, cerrarSesion, setToken,
        _escucharActividad,
    }
})