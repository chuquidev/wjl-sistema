import api from "@/services/api";

const BASE = "/encomiendas/";
const PERSONAS = "/pasajes/pasajeros/";

export const encomiendasService = {
  // ── Encomiendas ───────────────────────────────────────────
  obtenerEncomiendas: (params) => api.get(BASE, { params }),
  crearEncomienda: (data) => api.post(BASE, data),
  obtenerEncomienda: (id) => api.get(`${BASE}${id}/`),
  actualizarEstado: (id, data) => api.patch(`${BASE}${id}/`, data),
  eliminarEncomienda: (id) => api.delete(`${BASE}${id}/`),
  registrarEntrega: (id, data) => api.post(`${BASE}${id}/entregar/`, data),
  resumenEncomiendas: (params) => api.get(`${BASE}resumen/`, { params }),

  // ── Buscar persona por DNI ────────────────────────────────
  buscarPersona: (dni) =>
    api.get(`${PERSONAS}consultar-dni/`, { params: { dni } }),

  // ── Viajes disponibles para el día seleccionado ───────────
  // Solo muestra viajes programados del día, hasta 20 min después de la salida
  buscarViajesDisponibles: (fecha) =>
    api.get(`${BASE}viajes-disponibles/`, { params: { fecha } }),
};
