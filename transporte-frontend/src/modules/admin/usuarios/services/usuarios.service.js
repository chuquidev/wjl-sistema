import api from "@/services/api";

const BASE = "/usuarios/";

export const usuariosService = {
  obtenerUsuarios: (params) => api.get(BASE, { params }),
  crearUsuario: (data) => api.post(BASE, data),
  actualizarUsuario: (id, data) => api.patch(`${BASE}${id}/`, data),
  desactivarUsuario: (id) => api.post(`${BASE}${id}/desactivar/`),
  cambiarPassword: (data) => api.post(`${BASE}cambiar_password/`, data),
  obtenerSucursales: () => api.get("/ubicaciones/sucursales/"),
  restablecerPassword: (id, data) =>
    api.post(`${BASE}${id}/restablecer_password/`, data),
};
