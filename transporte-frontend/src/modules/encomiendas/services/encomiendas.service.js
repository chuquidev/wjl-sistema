import api from "@/services/api";

const BASE      = "/encomiendas/";
const PERSONAS  = "/pasajes/pasajeros/";
const VIAJES    = "/flota/viajes/";

export const encomiendasService = {
  // Encomiendas
  obtenerEncomiendas: (params) => api.get(BASE, { params }),
  crearEncomienda:    (data)   => api.post(BASE, data),
  obtenerEncomienda:  (id)     => api.get(`${BASE}${id}/`),
  actualizarEstado:   (id, data) => api.patch(`${BASE}${id}/`, data),
  registrarEntrega:   (id, data) => api.post(`${BASE}${id}/entregar/`, data),

  // Buscar persona por DNI (mismo endpoint que pasajes)
  buscarPersona(dni) {
    return api.get(`${PERSONAS}?dni=${dni}`);
  },

  // Viajes disponibles para asignar
  buscarViajes: (params) => api.get(VIAJES, { params }),
};