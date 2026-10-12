import api from "@/services/api";

const BASE = "/pasajes/";
const PASAJEROS = "/pasajes/pasajeros/";
const VIAJES = "/flota/viajes/";

export const pasajesService = {
  // ── Viajes ───────────────────────────────────────────────
  buscarViajes: (params) => api.get(VIAJES, { params }),
  obtenerAsientos: (viajeId) => api.get(`${VIAJES}${viajeId}/asientos/`),

  // ── Pasajeros ─────────────────────────────────────────────
  buscarPasajero: (dni) =>
    api.get("/pasajes/pasajeros/consultar-dni/", { params: { dni } }),
  crearPasajero: (data) => api.post(PASAJEROS, data),

  // ── Pasajes ───────────────────────────────────────────────
  obtenerPasajes: (params) => api.get(BASE, { params }),
  obtenerPasajesPorViaje: (viajeId) =>
    api.get(`/pasajes/por_viaje/`, { params: { viaje_id: viajeId } }),
  venderPasaje: (data) => api.post(BASE, data),
    // Vende varios pasajes en una sola operación: todo o nada
  venderLote: (data) => api.post(`${BASE}vender-lote/`, data),
  anularPasaje: (id, data) => api.post(`${BASE}${id}/anular/`, data),
  obtenerPasaje: (id) => api.get(`${BASE}${id}/`),
  // ── Embarcar pasajero (manifiesto) ────────────────────────
  embarcarPasajero: (id) => api.post(`${BASE}${id}/embarcar/`),
};
