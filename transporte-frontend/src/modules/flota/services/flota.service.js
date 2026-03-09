import api from '@/services/api'

const BASE = {
    vehiculos:   '/flota/vehiculos/',
    conductores: '/flota/conductores/',
    viajes:      '/flota/viajes/',
}

export const flotaService = {
    // Vehículos
    obtenerVehiculos:      (params)    => api.get(BASE.vehiculos, { params }),
    crearVehiculo:         (data)      => api.post(BASE.vehiculos, data),
    actualizarVehiculo:    (id, data)  => api.patch(`${BASE.vehiculos}${id}/`, data),
    cambiarEstadoVehiculo: (id, estado) => api.post(`${BASE.vehiculos}${id}/cambiar_estado/`, { estado }),

    // Conductores
    obtenerConductores:    (params)    => api.get(BASE.conductores, { params }),
    crearConductor:        (data)      => api.post(BASE.conductores, data),
    actualizarConductor:   (id, data)  => api.patch(`${BASE.conductores}${id}/`, data),

    // Viajes
    obtenerViajes:         (params)    => api.get(BASE.viajes, { params }),
    crearViaje:            (data)      => api.post(BASE.viajes, data),
    actualizarViaje:       (id, data)  => api.patch(`${BASE.viajes}${id}/`, data),
    cambiarEstadoViaje:    (id, estado) => api.post(`${BASE.viajes}${id}/cambiar_estado/`, { estado }),
    obtenerAsientos:       (id)        => api.get(`${BASE.viajes}${id}/asientos/`),

    // Auxiliares para formularios
    obtenerRutas:          ()          => api.get('/ubicaciones/rutas/'),
}