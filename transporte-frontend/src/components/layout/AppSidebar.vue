<template>
  <Transition name="fade">
    <div
      v-if="ui.mobileMenuOpen"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm z-30 lg:hidden"
      @click="ui.cerrarMenuMovil()"
    />
  </Transition>

  <aside
    :class="[
      'fixed top-0 left-0 h-screen bg-white border-r border-gray-100 shadow-sm',
      'flex flex-col z-40 transition-all duration-300 ease-in-out',
      ui.sidebarCollapsed ? 'lg:w-[68px]' : 'lg:w-[260px]',
      ui.mobileMenuOpen
        ? 'translate-x-0 w-[260px]'
        : '-translate-x-full lg:translate-x-0',
    ]"
  >
    <!-- Logo -->
    <div
      class="flex items-center h-[60px] px-4 border-b border-gray-100 flex-shrink-0"
    >
      <div class="flex items-center gap-3 overflow-hidden">
        <div
          class="w-8 h-8 rounded-lg bg-orange-500 flex items-center justify-center flex-shrink-0"
        >
          <svg
            class="w-4 h-4 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
            />
          </svg>
        </div>
        <div
          v-show="!ui.sidebarCollapsed || ui.mobileMenuOpen"
          class="overflow-hidden"
        >
          <p class="text-sm font-bold text-gray-900 whitespace-nowrap">
            WJL Transportes
          </p>
          <p class="text-[10px] text-gray-400 whitespace-nowrap">
            Sistema de Gestión
          </p>
        </div>
      </div>
    </div>

    <!-- Navegación -->
    <nav class="flex-1 overflow-y-auto overflow-x-hidden py-3 px-2 space-y-0.5">
      <template v-for="seccion in seccionesVisibles" :key="seccion.etiqueta">
        <p
          v-if="!ui.sidebarCollapsed || ui.mobileMenuOpen"
          class="text-[10px] font-bold text-gray-400 px-3 mt-4 mb-2 uppercase tracking-widest"
        >
          {{ seccion.etiqueta }}
        </p>
        <div v-else class="mt-3 mb-1 px-2">
          <div class="h-px bg-gray-100"></div>
        </div>

        <template v-for="item in seccion.items" :key="item.nombre">
          <!-- Item sin hijos -->
          <router-link
            v-if="!item.hijos"
            :to="item.ruta"
            @click="ui.cerrarMenuMovil()"
            :class="['sidebar-nav-item', estaActivo(item) ? 'active' : '']"
            :title="ui.sidebarCollapsed ? item.etiqueta : ''"
          >
            <span
              v-html="item.icono"
              class="w-5 h-5 flex-shrink-0 [&>svg]:w-full [&>svg]:h-full"
            ></span>
            <span
              v-show="!ui.sidebarCollapsed || ui.mobileMenuOpen"
              class="truncate text-sm ml-3"
            >
              {{ item.etiqueta }}
            </span>
          </router-link>

          <!-- Item con hijos (grupo) -->
          <div v-else>
            <button
              @click="toggleGrupo(item.nombre)"
              :class="[
                'sidebar-nav-item w-full',
                estaGrupoActivo(item) ? 'active' : '',
              ]"
              :title="ui.sidebarCollapsed ? item.etiqueta : ''"
            >
              <span
                v-html="item.icono"
                class="w-5 h-5 flex-shrink-0 [&>svg]:w-full [&>svg]:h-full"
              ></span>
              <span
                v-show="!ui.sidebarCollapsed || ui.mobileMenuOpen"
                class="truncate flex-1 text-left text-sm ml-3"
              >
                {{ item.etiqueta }}
              </span>
              <svg
                v-show="!ui.sidebarCollapsed || ui.mobileMenuOpen"
                :class="[
                  'w-3.5 h-3.5 transition-transform',
                  gruposAbiertos.has(item.nombre) ? 'rotate-180' : '',
                ]"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2.5"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
            <div
              v-show="
                gruposAbiertos.has(item.nombre) &&
                (!ui.sidebarCollapsed || ui.mobileMenuOpen)
              "
              class="ml-4 pl-3 border-l-2 border-orange-100 mt-0.5"
            >
              <router-link
                v-for="hijo in item.hijos"
                :key="hijo.nombre"
                :to="hijo.ruta"
                @click="ui.cerrarMenuMovil()"
                :class="[
                  'flex items-center gap-2 px-3 py-2 rounded-lg text-sm',
                  estaActivoPorNombre(hijo.nombre)
                    ? 'text-orange-600 font-semibold bg-orange-50'
                    : 'text-gray-500 hover:bg-gray-50',
                ]"
              >
                <span class="w-1 h-1 rounded-full bg-current"></span>
                {{ hijo.etiqueta }}
              </router-link>
            </div>
          </div>
        </template>
      </template>
    </nav>

    <!-- Footer: info usuario -->
    <div class="flex-shrink-0 border-t border-gray-100 p-2">
      <div class="flex items-center gap-3 w-full p-2">
        <div
          class="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-bold text-sm flex-shrink-0"
        >
          {{ inicialesUsuario }}
        </div>
        <div
          v-show="!ui.sidebarCollapsed || ui.mobileMenuOpen"
          class="flex-1 overflow-hidden"
        >
          <p class="text-sm font-semibold text-gray-800 truncate">
            {{ auth.nombre_completo }}
          </p>
          <p class="text-[10px] text-gray-400 truncate">
            {{ auth.usuario?.correo }}
          </p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import { useUiStore } from "@/stores/ui.store";
import { useAuthStore } from "@/modules/auth/stores/auth.store";

const ui = useUiStore();
const auth = useAuthStore();
const route = useRoute();

const gruposAbiertos = ref(
  new Set(["POS", "CAJA", "OPS", "ENC", "CAT", "ADM", "REP"]),
);

const ICONOS = {
  dashboard: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>`,
  pasaje: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/></svg>`,
  caja: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/></svg>`,
  flota: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2h8zm0 0l2-5h3l2 5m-7 0h7"/></svg>`,
  caja2: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>`,
  catalogo: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>`,
  admin: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>`,
  reporte: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>`,
};

const menuSecciones = [
  {
    etiqueta: "Principal",
    items: [
      {
        nombre: "dashboard",
        etiqueta: "Dashboard",
        icono: ICONOS.dashboard,
        ruta: "/",
      },
    ],
  },
  {
    etiqueta: "Punto de Venta",
    items: [
      {
        nombre: "POS",
        etiqueta: "Pasajes",
        icono: ICONOS.pasaje,
        hijos: [
          {
            nombre: "vender-pasaje",
            etiqueta: "Venta de Pasajes",
            ruta: "/pasajes/vender",
          },
          {
            nombre: "manifiesto-pasajes",
            etiqueta: "Manifiesto",
            ruta: "/pasajes/manifiesto",
          },
        ],
      },
    ],
  },
  {
    etiqueta: "Caja",
    items: [
      {
        nombre: "CAJA",
        etiqueta: "Caja",
        icono: ICONOS.caja,
        hijos: [
          { nombre: "caja", etiqueta: "Apertura", ruta: "/caja" },
          {
            nombre: "movimientos",
            etiqueta: "Movimientos",
            ruta: "/caja/movimientos",
          },
          {
            nombre: "arqueo",
            etiqueta: "Arqueo / Cierre",
            ruta: "/caja/arqueo",
          },
        ],
      },
    ],
  },
  {
    etiqueta: "Operaciones",
    items: [
      {
        nombre: "OPS",
        etiqueta: "Flota y Viajes",
        icono: ICONOS.flota,
        hijos: [
          { nombre: "viajes", etiqueta: "Viajes", ruta: "/flota/viajes" },
          {
            nombre: "vehiculos",
            etiqueta: "Vehículos",
            ruta: "/flota/vehiculos",
          },
          {
            nombre: "conductores",
            etiqueta: "Conductores",
            ruta: "/flota/conductores",
          },
        ],
      },
    ],
  },
  {
    etiqueta: "Encomiendas",
    items: [
      {
        nombre: "ENC",
        etiqueta: "Encomiendas",
        icono: ICONOS.caja2,
        hijos: [
          {
            nombre: "encomiendas",
            etiqueta: "Registro / Listado",
            ruta: "/encomiendas",
          },
        ],
      },
    ],
  },
  {
    etiqueta: "Administración",
    items: [
      {
        nombre: "ADM",
        etiqueta: "Administración",
        icono: ICONOS.admin,
        hijos: [
          { nombre: "usuarios", etiqueta: "Usuarios", ruta: "/admin/usuarios" },
          {
            nombre: "ubicaciones",
            etiqueta: "Ubicaciones",
            ruta: "/admin/ubicaciones",
          },
        ],
      },
    ],
  },
  {
    etiqueta: "Reportes",
    items: [
      {
        nombre: "reportes",
        etiqueta: "Reportes",
        icono: ICONOS.reporte,
        ruta: "/reportes",
      },
    ],
  },
];

// Administración (usuarios y ubicaciones) solo la ve el administrador
const seccionesVisibles = computed(() =>
  menuSecciones.filter((s) => s.etiqueta !== "Administración" || auth.esAdmin),
);

const inicialesUsuario = computed(() => {
  if (!auth.usuario) return "?";
  return (
    (auth.usuario.nombres?.[0] || "") + (auth.usuario.apellidos?.[0] || "")
  );
});

const estaActivo = (item) => route.name === item.nombre;
const estaActivoPorNombre = (nombre) => route.name === nombre;
const estaGrupoActivo = (item) =>
  item.hijos?.some((h) => route.name === h.nombre);
const toggleGrupo = (nombre) => {
  gruposAbiertos.value.has(nombre)
    ? gruposAbiertos.value.delete(nombre)
    : gruposAbiertos.value.add(nombre);
};
</script>
