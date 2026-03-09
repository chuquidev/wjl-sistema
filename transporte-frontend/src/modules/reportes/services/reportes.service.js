import api from '@/services/api'

const BASE = '/reportes/'

export const reportesService = {
    getDashboard:   (params) => api.get(`${BASE}dashboard/`, { params }),
    getVentas:      (params) => api.get(`${BASE}ventas/`, { params }),
    getCaja:        (params) => api.get(`${BASE}caja/`, { params }),
    getViajes:      (params) => api.get(`${BASE}viajes/`, { params }),
    getEncomiendas: (params) => api.get(`${BASE}encomiendas/`, { params }),
    exportarPDF:    (params) => api.get(`${BASE}exportar/pdf/`, { params, responseType: 'blob' }),
    exportarExcel:  (params) => api.get(`${BASE}exportar/excel/`, { params, responseType: 'blob' }),
}