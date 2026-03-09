import api from '@/services/api'

const BASE = {
    sucursales: '/ubicaciones/sucursales/',
    ciudades:   '/ubicaciones/ciudades/',
    rutas:      '/ubicaciones/rutas/',
}

export const ubicacionesService = {
    // Sucursales
    obtenerSucursales:   (params) => api.get(BASE.sucursales, { params }),
    crearSucursal:       (data)   => api.post(BASE.sucursales, data),
    actualizarSucursal:  (id, data) => api.patch(`${BASE.sucursales}${id}/`, data),
    eliminarSucursal:    (id)     => api.delete(`${BASE.sucursales}${id}/`),

    // Ciudades
    obtenerCiudades:     (params) => api.get(BASE.ciudades, { params }),
    crearCiudad:         (data)   => api.post(BASE.ciudades, data),
    actualizarCiudad:    (id, data) => api.patch(`${BASE.ciudades}${id}/`, data),
    eliminarCiudad:      (id)     => api.delete(`${BASE.ciudades}${id}/`),

    // Rutas
    obtenerRutas:        (params) => api.get(BASE.rutas, { params }),
    crearRuta:           (data)   => api.post(BASE.rutas, data),
    actualizarRuta:      (id, data) => api.patch(`${BASE.rutas}${id}/`, data),
    eliminarRuta:        (id)     => api.delete(`${BASE.rutas}${id}/`),
}