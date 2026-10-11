import axios from "axios";
import { useAuthStore } from "@/modules/auth/stores/auth.store";

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Endpoints de autenticación: un 401 aquí NO significa "token vencido"
// (login con clave incorrecta, refresh inválido), así que no se reintentan.
const esEndpointAuth = (url = "") => url.includes("/auth/token/");

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error) => {
  failedQueue.forEach(({ resolve, reject }) => {
    error ? reject(error) : resolve();
  });
  failedQueue = [];
};

const irALogin = (authStore) => {
  authStore.cerrarSesion();
  window.location.href = "/login";
};

// Interceptor: agrega token a cada petición
api.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

// Interceptor: maneja token expirado
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore();
    const originalRequest = error.config;

    const noReintentar =
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry ||
      esEndpointAuth(originalRequest.url);

    if (noReintentar) {
      return Promise.reject(error);
    }

    // Si ya hay un refresh en curso, encolar la petición hasta que termine
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      }).then(() => {
        originalRequest._retry = true;
        return api(originalRequest);
      });
    }

    originalRequest._retry = true;

    // Sin refresh token no hay nada que renovar: cerrar sesión
    if (!authStore.refreshToken) {
      irALogin(authStore);
      return Promise.reject(error);
    }

    isRefreshing = true;
    try {
      // Se usa axios "limpio" (no `api`) para que esta petición NO pase por
      // los interceptors; si no, su propio 401 quedaría esperando en la cola.
      const { data } = await axios.post(`${API_URL}/auth/token/refresh/`, {
        refresh: authStore.refreshToken,
      });

      // El backend rota el refresh: hay que guardar también el nuevo
      authStore.setToken(data.access, data.refresh);
      processQueue(null);

      originalRequest.headers.Authorization = `Bearer ${data.access}`;
      return api(originalRequest);
    } catch (refreshError) {
      processQueue(refreshError);
      // Solo cerrar sesión si el refresh fue rechazado (no por caída de red)
      if (
        refreshError.response?.status === 401 ||
        refreshError.response?.status === 400
      ) {
        irALogin(authStore);
      }
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  },
);

export default api;
