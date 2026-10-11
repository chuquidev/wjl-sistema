import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/services/api";

const INACTIVIDAD_MS = 60 * 60 * 1000; // 1 hora
const KEY_ULTIMA_ACT = "ultima_actividad"; // localStorage key

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token") || null);
  const refreshToken = ref(localStorage.getItem("refresh_token") || null);
  const usuario = ref(JSON.parse(localStorage.getItem("usuario") || "null"));
  let _timer = null;

  const estaAutenticado = computed(() => !!token.value);
  const esAdmin = computed(() => usuario.value?.rol === "administrador");
  const esSupervisor = computed(() => usuario.value?.rol === "supervisor");
  const esCajero = computed(() => usuario.value?.rol === "cajero");
  const nombre_completo = computed(() => {
    if (!usuario.value) return "";
    return `${usuario.value.nombres} ${usuario.value.apellidos}`;
  });

  // ── Helpers de tiempo ────────────────────────────────────
  function _guardarActividad() {
    localStorage.setItem(KEY_ULTIMA_ACT, Date.now().toString());
  }

  function _tiempoInactivo() {
    const ultima = parseInt(localStorage.getItem(KEY_ULTIMA_ACT) || "0");
    if (!ultima) return 0;
    return Date.now() - ultima;
  }

  function _sesionExpirada() {
    return _tiempoInactivo() >= INACTIVIDAD_MS;
  }

  // ── Timer de inactividad ─────────────────────────────────
  function _iniciarTimerInactividad() {
    _limpiarTimer();
    // Calcular cuánto tiempo queda antes de expirar
    const transcurrido = _tiempoInactivo();
    const restante = Math.max(INACTIVIDAD_MS - transcurrido, 0);

    _timer = setTimeout(() => {
      console.log("Sesión expirada por inactividad");
      cerrarSesion();
      window.location.href = "/login";
    }, restante);
  }

  function _limpiarTimer() {
    if (_timer) {
      clearTimeout(_timer);
      _timer = null;
    }
  }

  function _escucharActividad() {
    const eventos = ["mousemove", "keydown", "click", "scroll", "touchstart"];
    const resetear = () => {
      if (!token.value) return;
      _guardarActividad();
      _iniciarTimerInactividad();
    };
    // Remover listeners anteriores para evitar duplicados al recargar
    eventos.forEach((ev) => {
      window.removeEventListener(ev, resetear);
      window.addEventListener(ev, resetear, { passive: true });
    });
  }

  // ── Auth actions ─────────────────────────────────────────
  async function iniciarSesion(correo, password) {
    const { data } = await api.post("/auth/token/", { correo, password });
    token.value = data.access;
    refreshToken.value = data.refresh;
    localStorage.setItem("token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    _guardarActividad();
    _iniciarTimerInactividad();
    _escucharActividad();
    await cargarPerfil();
  }

  async function cargarPerfil() {
    const { data } = await api.get("/usuarios/perfil/");
    usuario.value = data;
    localStorage.setItem("usuario", JSON.stringify(data));
  }

  function setToken(nuevoToken, nuevoRefresh = null) {
    token.value = nuevoToken;
    localStorage.setItem("token", nuevoToken);
    // El backend rota el refresh en cada renovación: el anterior queda
    // en lista negra, así que hay que guardar el nuevo.
    if (nuevoRefresh) {
      refreshToken.value = nuevoRefresh;
      localStorage.setItem("refresh_token", nuevoRefresh);
    }
    _guardarActividad();
  }

  function cerrarSesion() {
    _limpiarTimer();
    token.value = null;
    refreshToken.value = null;
    usuario.value = null;
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("usuario");
    localStorage.removeItem(KEY_ULTIMA_ACT);
  }

  // ── Al recargar: verificar si la sesión sigue vigente ────
  if (token.value) {
    if (_sesionExpirada()) {
      // Han pasado más de 1 hora desde la última actividad → cerrar
      console.log("Sesión expirada al recargar");
      cerrarSesion();
    } else {
      // Sesión vigente → continuar con el tiempo restante real
      console.log(
        `Sesión activa. Inactividad: ${Math.round(_tiempoInactivo() / 60000)} min`,
      );
      _iniciarTimerInactividad();
      _escucharActividad();
    }
  }

  return {
    token,
    refreshToken,
    usuario,
    estaAutenticado,
    esAdmin,
    esSupervisor,
    esCajero,
    nombre_completo,
    iniciarSesion,
    cargarPerfil,
    cerrarSesion,
    setToken,
    _escucharActividad,
  };
});
