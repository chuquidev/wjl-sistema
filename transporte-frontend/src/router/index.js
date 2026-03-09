import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/modules/auth/stores/auth.store";
const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/modules/auth/views/LoginView.vue"),
    meta: { publica: true },
  },
  {
    path: "/",
    component: () => import("@/components/layout/AppLayout.vue"),
    meta: { requiereAuth: true },
    children: [
      {
        path: "",
        name: "dashboard",
        component: () => import("@/modules/dashboard/views/DashboardView.vue"),
      },
      // Flota
      {
        path: "flota/vehiculos",
        name: "vehiculos",
        component: () => import("@/modules/flota/views/FlotaView.vue"),
      },
      {
        path: "flota/conductores",
        name: "conductores",
        component: () => import("@/modules/flota/views/FlotaView.vue"),
      },
      {
        path: "flota/viajes",
        name: "viajes",
        component: () => import("@/modules/flota/views/FlotaView.vue"),
      },

      // Pasajes
      {
        path: "pasajes",
        name: "pasajes",
        component: () => import("@/modules/pasajes/views/PasajesView.vue"),
      },
      {
        path: "pasajes/vender",
        name: "vender-pasaje",
        component: () => import("@/modules/pasajes/views/PasajesView.vue"),
      },
      {
        path: "pasajes/manifiesto",
        name: "manifiesto-pasajes",
        component: () => import("@/modules/pasajes/views/ManifiestoView.vue"),
      },

      // Encomiendas
      {
        path: "encomiendas",
        name: "encomiendas",
        component: () =>
          import("@/modules/encomiendas/views/EncomiendasView.vue"),
      },
      // Caja
      {
        path: "caja",
        name: "caja",
        component: () => import("@/modules/caja/views/CajaView.vue"),
      },
      {
        path: "caja/movimientos",
        name: "caja-movimientos",
        component: () => import("@/modules/caja/views/CajaView.vue"),
      },
      {
        path: "caja/arqueo",
        name: "caja-arqueo",
        component: () => import("@/modules/caja/views/CajaView.vue"),
      },

      // {
      //   path: "caja/consolidado",
      //   name: "caja-consolidado",
      //   component: () => import("@/modules/caja/views/CajaView.vue"),
      // },
      
      // Admin
      {
        path: "admin/usuarios",
        name: "usuarios",
        component: () =>
          import("@/modules/admin/usuarios/views/UsuariosView.vue"),
        meta: { soloAdmin: true },
      },
      {
        path: "perfil",
        name: "perfil",
        component: () => import("@/modules/admin/usuarios/views/PerfilView.vue"),
      },
      {
        path: "admin/ubicaciones",
        name: "ubicaciones",
        component: () =>
          import("@/modules/admin/ubicaciones/views/UbicacionesView.vue"),
        meta: { soloAdmin: true },
      },
      {
        path: "reportes",
        name: "reportes",
        component: () => import("@/modules/reportes/views/ReportesView.vue"),
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guard global
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (!to.meta.publica && !authStore.estaAutenticado) {
    return next({ name: "login" });
  }
  if (to.meta.soloAdmin && !authStore.esAdmin) {
    return next({ name: "dashboard" });
  }
  if (to.name === "login" && authStore.estaAutenticado) {
    return next({ name: "dashboard" });
  }

  next();
});

export default router;
