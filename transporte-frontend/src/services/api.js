import axios from 'axios'
import { useAuthStore } from '@/modules/auth/stores/auth.store'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' },
})

let isRefreshing = false
let failedQueue  = []

const processQueue = (error) => {
  failedQueue.forEach(({ resolve, reject }) => {
    error ? reject(error) : resolve()
  })
  failedQueue = []
}

// Interceptor: agrega token a cada petición
api.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

// Interceptor: maneja token expirado
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore       = useAuthStore()
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then(() => api(originalRequest))
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing           = true

      try {
        const { data } = await api.post('/auth/token/refresh/', {
          refresh: authStore.refreshToken,
        })

        authStore.setToken(data.access)
        originalRequest.headers.Authorization = `Bearer ${data.access}`
        processQueue(null)
        return api(originalRequest)

      } catch (refreshError) {
        processQueue(refreshError)
        authStore.cerrarSesion()
        window.location.href = '/login'
        return Promise.reject(refreshError)

      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default api