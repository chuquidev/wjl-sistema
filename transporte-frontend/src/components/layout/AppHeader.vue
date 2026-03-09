<template>
    <header class="fixed top-0 right-0 z-20 h-[60px] bg-white border-b border-gray-100
                   flex items-center justify-between px-3 sm:px-4 gap-2 transition-all duration-300 left-0"
        :class="[ui.sidebarCollapsed ? 'lg:left-[68px]' : 'lg:left-[260px]']">

        <!-- Izquierda: toggle + breadcrumb -->
        <div class="flex items-center gap-2 sm:gap-3">
            <button @click="ui.toggleSidebar()"
                class="w-9 h-9 rounded-lg hover:bg-gray-100 flex items-center justify-center text-gray-500 hover:text-gray-700 transition-colors">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>

            <div class="hidden xs:flex items-center gap-2 text-sm">
                <span class="text-gray-400 whitespace-nowrap">{{ seccionActual }}</span>
                <template v-if="paginaActual !== seccionActual">
                    <svg class="w-3 h-3 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                    <span class="font-semibold text-gray-800 whitespace-nowrap">{{ paginaActual }}</span>
                </template>
            </div>
        </div>

        <!-- Derecha: estado caja + sucursal + reloj + usuario -->
        <div class="flex items-center gap-2">

            <!-- Estado de caja -->
            <div v-if="cajaAbierta"
                class="flex items-center gap-2 px-2 py-1.5 rounded-lg bg-emerald-50 border border-emerald-100">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span class="text-[10px] sm:text-xs font-semibold text-emerald-700 whitespace-nowrap">Caja Abierta</span>
            </div>
            <div v-else
                class="flex items-center gap-2 px-2 py-1.5 rounded-lg bg-amber-50 border border-amber-100">
                <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                <span class="text-[10px] sm:text-xs font-semibold text-amber-700 whitespace-nowrap">Sin caja</span>
            </div>

            <!-- Sucursal del usuario -->
            <div v-if="auth.usuario?.sucursal_nombre"
                class="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-orange-50 border border-orange-100">
                <svg class="w-3.5 h-3.5 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span class="text-xs font-semibold text-orange-700 whitespace-nowrap">
                    {{ auth.usuario.sucursal_nombre }}
                </span>
            </div>

            <!-- Reloj -->
            <div class="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-50 border border-gray-100">
                <svg class="w-3.5 h-3.5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-xs font-mono text-gray-600">{{ horaActual }}</span>
            </div>

            <!-- Menú usuario -->
            <div class="relative" ref="menuRef">
                <button @click="menuAbierto = !menuAbierto"
                    class="flex items-center gap-2 pl-2 pr-1 sm:pr-3 py-1.5 rounded-lg hover:bg-gray-100 transition-colors">
                    <div class="w-7 h-7 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-bold text-xs">
                        {{ inicialesUsuario }}
                    </div>
                    <span class="hidden sm:block text-sm font-medium text-gray-700 max-w-[100px] truncate">
                        {{ auth.nombre_completo }}
                    </span>
                    <svg class="w-3 h-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7" />
                    </svg>
                </button>

                <Transition name="fade">
                    <div v-if="menuAbierto"
                        class="absolute right-0 top-full mt-2 w-56 bg-white rounded-xl border border-gray-100 shadow-lg overflow-hidden z-50">

                        <!-- Info usuario -->
                        <div class="px-4 py-3 border-b border-gray-50">
                            <p class="text-sm font-semibold text-gray-900">{{ auth.nombre_completo }}</p>
                            <p class="text-xs text-gray-400">{{ auth.usuario?.correo }}</p>
                            <span class="mt-1 inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-bold bg-blue-50 text-blue-600 uppercase tracking-wide">
                                {{ auth.usuario?.rol_display }}
                            </span>
                        </div>

                        <!-- Opciones -->
                        <div class="p-1.5">
                            <button @click="irAPerfil"
                                class="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">
                                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                Mi perfil
                            </button>
                        </div>

                        <!-- Cerrar sesión -->
                        <div class="p-1.5 border-t border-gray-50">
                            <button @click="cerrarSesion"
                                class="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm text-red-600 hover:bg-red-50 transition-colors">
                                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                </svg>
                                Cerrar sesión
                            </button>
                        </div>
                    </div>
                </Transition>
            </div>
        </div>
    </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUiStore }   from '@/stores/ui.store'
import { useAuthStore } from '@/modules/auth/stores/auth.store'
import { useCajaStore } from '@/modules/caja/stores/caja.store'

const ui     = useUiStore()
const auth   = useAuthStore()
const caja   = useCajaStore()
const route  = useRoute()
const router = useRouter()

const menuAbierto = ref(false)
const menuRef     = ref(null)
const horaActual  = ref('')

const cajaAbierta = computed(() => caja.sesionActiva !== null)

const nombresRuta = {
    'dashboard':            { seccion: 'Principal',   pagina: 'Dashboard'        },
    'vender-pasaje':        { seccion: 'Pasajes',     pagina: 'Venta de Pasajes' },
    'pasajes':              { seccion: 'Pasajes',     pagina: 'Buscar / Anular'  },
    'manifiesto-pasajes':   { seccion: 'Pasajes',     pagina: 'Manifiesto'       },
    'encomiendas':          { seccion: 'Encomiendas', pagina: 'Listado'          },
    'registrar-encomienda': { seccion: 'Encomiendas', pagina: 'Registrar'        },
    'caja':                 { seccion: 'Caja',        pagina: 'Apertura / Cierre'},
    'caja-movimientos':     { seccion: 'Caja',        pagina: 'Movimientos'      },
    'caja-arqueo':          { seccion: 'Caja',        pagina: 'Arqueo'           },
    'viajes':               { seccion: 'Operaciones', pagina: 'Viajes'           },
    'vehiculos':            { seccion: 'Operaciones', pagina: 'Vehículos'        },
    'conductores':          { seccion: 'Operaciones', pagina: 'Conductores'      },
    'usuarios':             { seccion: 'Admin',       pagina: 'Usuarios'         },
    'ubicaciones':          { seccion: 'Admin',       pagina: 'Ubicaciones'      },
    'reportes':             { seccion: 'Reportes',    pagina: 'Reportes'         },
    'perfil':               { seccion: 'Mi cuenta',   pagina: 'Mi Perfil'        },
}

const seccionActual = computed(() => nombresRuta[route.name]?.seccion || '')
const paginaActual  = computed(() => nombresRuta[route.name]?.pagina  || '')

const inicialesUsuario = computed(() => {
    if (!auth.usuario) return '?'
    return (auth.usuario.nombres?.[0] || '') + (auth.usuario.apellidos?.[0] || '')
})

function actualizarHora() {
    horaActual.value = new Date().toLocaleTimeString('es-PE', {
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    })
}

function manejarClickFuera(e) {
    if (menuRef.value && !menuRef.value.contains(e.target)) {
        menuAbierto.value = false
    }
}

function irAPerfil() {
    menuAbierto.value = false
    router.push({ name: 'perfil' })
}

async function cerrarSesion() {
    menuAbierto.value = false
    auth.cerrarSesion()
    router.push('/login')
}

let intervalo
onMounted(() => {
    actualizarHora()
    intervalo = setInterval(actualizarHora, 1000)
    document.addEventListener('click', manejarClickFuera)
})

onUnmounted(() => {
    clearInterval(intervalo)
    document.removeEventListener('click', manejarClickFuera)
})
</script>