import api from '@/services/api'

const BASE = '/caja/'

export const cajaService = {
    // Sesiones
    obtenerSesiones:    (params)   => api.get(`${BASE}sesiones/`, { params }),
    miSesionActiva:     ()         => api.get(`${BASE}sesiones/mi_sesion/`),
    abrirCaja:          (data)     => api.post(`${BASE}sesiones/`, data),
    cerrarCaja:         (id, data) => api.post(`${BASE}sesiones/${id}/cerrar/`, data),

    // Transacciones
    obtenerMovimientos: (params)   => api.get(`${BASE}transacciones/`, { params }),
    registrarEgreso:    (data)     => api.post(`${BASE}transacciones/`, data),
    consolidado: (params) => api.get(`${BASE}sesiones/consolidado/`, { params }),
}