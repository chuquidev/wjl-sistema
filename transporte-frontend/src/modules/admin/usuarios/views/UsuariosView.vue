<template>
  <div class="space-y-5">
    <!-- Encabezado -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Usuarios</h1>
        <p class="page-subtitle">Gestión de accesos y roles del sistema</p>
      </div>
      <button @click="abrirModalCrear" class="btn-primary">
        <svg
          class="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2.5"
            d="M12 4v16m8-8H4"
          />
        </svg>
        Nuevo Usuario
      </button>
    </div>

    <!-- Filtros -->
    <div class="flex flex-wrap items-center gap-3">
      <div class="relative">
        <svg
          class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <input
          v-model="busqueda"
          type="text"
          placeholder="Buscar usuario..."
          class="form-input pl-9 w-64"
        />
      </div>

      <select v-model="filtroRol" class="form-input w-44">
        <option value="">Todos los roles</option>
        <option value="administrador">Administrador</option>
        <option value="supervisor">Supervisor</option>
        <option value="cajero">Cajero</option>
      </select>

      <select v-model="filtroSucursal" class="form-input w-48">
        <option value="">Todas las sucursales</option>
        <option v-for="s in store.sucursales" :key="s.id" :value="s.id">
          {{ s.nombre }}
        </option>
      </select>
    </div>

    <!-- Tabla -->
    <div class="card">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>Usuario</th>
              <th>DNI</th>
              <th>Correo</th>
              <th>Rol</th>
              <th>Sucursal</th>
              <th>Estado</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <!-- Cargando -->
            <tr v-if="store.cargando">
              <td colspan="7">
                <div class="flex justify-center py-10">
                  <svg
                    class="w-6 h-6 text-gray-300 animate-spin"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    />
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                    />
                  </svg>
                </div>
              </td>
            </tr>
            <!-- Sin resultados -->
            <tr v-else-if="!usuariosFiltrados.length">
              <td colspan="7" class="text-center py-12 text-gray-400 italic">
                No se encontraron usuarios
              </td>
            </tr>
            <!-- Filas -->
            <tr v-for="u in usuariosFiltrados" :key="u.id">
              <td>
                <div class="flex items-center gap-3">
                  <div
                    class="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-bold text-xs flex-shrink-0"
                  >
                    {{ iniciales(u) }}
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900 text-sm">
                      {{ u.nombre_completo }}
                    </p>
                    <p class="text-xs text-gray-400">{{ u.telefono || "—" }}</p>
                  </div>
                </div>
              </td>
              <td class="font-mono text-sm text-gray-700">{{ u.dni }}</td>
              <td class="text-gray-600 text-sm">{{ u.correo }}</td>
              <td>
                <span :class="claseRol(u.rol)">{{ u.rol_display }}</span>
              </td>
              <td class="text-gray-600 text-sm">
                {{ u.sucursal_nombre || "—" }}
              </td>
              <td>
                <span
                  :class="u.activo ? 'badge badge-green' : 'badge badge-red'"
                >
                  {{ u.activo ? "Activo" : "Inactivo" }}
                </span>
              </td>
              <td class="text-right">
                <div class="flex items-center justify-end gap-1">
                  <button
                    @click="abrirModalEditar(u)"
                    title="Editar"
                    class="w-8 h-8 rounded-lg hover:bg-blue-50 flex items-center justify-center text-gray-400 hover:text-blue-600 transition-colors"
                  >
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                      />
                    </svg>
                  </button>
                  <button
                    @click="abrirModalPassword(u)"
                    title="Cambiar contraseña"
                    class="w-8 h-8 rounded-lg hover:bg-amber-50 flex items-center justify-center text-gray-400 hover:text-amber-600 transition-colors"
                  >
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"
                      />
                    </svg>
                  </button>
                  <button
                    v-if="u.activo"
                    @click="confirmarDesactivar(u)"
                    title="Desactivar"
                    class="w-8 h-8 rounded-lg hover:bg-red-50 flex items-center justify-center text-gray-400 hover:text-red-600 transition-colors"
                  >
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"
                      />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── MODAL CREAR / EDITAR ───────────────────────────── -->
    <AppModal
      v-model="modalAbierto"
      :titulo="modoEdicion ? 'Editar Usuario' : 'Nuevo Usuario'"
      ancho="lg"
    >
      <form @submit.prevent="guardar" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="form-label"
              >Nombres <span class="text-red-500">*</span></label
            >
            <input
              v-model="formulario.nombres"
              type="text"
              class="form-input"
              :class="{ 'form-input-error': errores.nombres }"
              placeholder="Ej: Juan Carlos"
            />
            <p v-if="errores.nombres" class="form-error">
              {{ errores.nombres }}
            </p>
          </div>
          <div>
            <label class="form-label"
              >Apellidos <span class="text-red-500">*</span></label
            >
            <input
              v-model="formulario.apellidos"
              type="text"
              class="form-input"
              :class="{ 'form-input-error': errores.apellidos }"
              placeholder="Ej: López Torres"
            />
            <p v-if="errores.apellidos" class="form-error">
              {{ errores.apellidos }}
            </p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="form-label"
              >DNI <span class="text-red-500">*</span></label
            >
            <input
              v-model="formulario.dni"
              type="text"
              maxlength="8"
              class="form-input"
              :class="{ 'form-input-error': errores.dni }"
              placeholder="12345678"
            />
            <p v-if="errores.dni" class="form-error">{{ errores.dni }}</p>
          </div>
          <div>
            <label class="form-label">Teléfono</label>
            <input
              v-model="formulario.telefono"
              type="text"
              class="form-input"
              placeholder="Ej: 987654321"
            />
          </div>
        </div>

        <div>
          <label class="form-label"
            >Correo electrónico <span class="text-red-500">*</span></label
          >
          <input
            v-model="formulario.correo"
            type="email"
            class="form-input"
            :class="{ 'form-input-error': errores.correo }"
            :disabled="modoEdicion"
            placeholder="usuario@correo.com"
          />
          <p v-if="modoEdicion" class="form-hint">
            El correo no se puede modificar
          </p>
          <p v-if="errores.correo" class="form-error">{{ errores.correo }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="form-label"
              >Rol <span class="text-red-500">*</span></label
            >
            <select
              v-model="formulario.rol"
              class="form-input"
              :class="{ 'form-input-error': errores.rol }"
            >
              <option value="">Seleccionar...</option>
              <option value="administrador">Administrador</option>
              <option value="supervisor">Supervisor</option>
              <option value="cajero">Cajero</option>
            </select>
            <p v-if="errores.rol" class="form-error">{{ errores.rol }}</p>
          </div>
          <div>
            <label class="form-label">Sucursal</label>
            <select v-model="formulario.sucursal" class="form-input">
              <option value="">Sin sucursal</option>
              <option v-for="s in store.sucursales" :key="s.id" :value="s.id">
                {{ s.nombre }}
              </option>
            </select>
          </div>
        </div>

        <!-- Solo en creación -->
        <template v-if="!modoEdicion">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label"
                >Contraseña <span class="text-red-500">*</span></label
              >
              <div class="relative">
                <input
                  v-model="formulario.password"
                  :type="mostrarPass ? 'text' : 'password'"
                  class="form-input pr-10"
                  :class="{ 'form-input-error': errores.password }"
                  placeholder="Mínimo 8 caracteres"
                />
                <button
                  type="button"
                  @click="mostrarPass = !mostrarPass"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      v-if="!mostrarPass"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                    <path
                      v-else
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                    />
                  </svg>
                </button>
              </div>
              <p v-if="errores.password" class="form-error">
                {{ errores.password }}
              </p>
            </div>
            <div>
              <label class="form-label"
                >Confirmar contraseña <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.confirmar_password"
                :type="mostrarPass ? 'text' : 'password'"
                class="form-input"
                :class="{ 'form-input-error': errores.confirmar_password }"
                placeholder="Repite la contraseña"
              />
              <p v-if="errores.confirmar_password" class="form-error">
                {{ errores.confirmar_password }}
              </p>
            </div>
          </div>
        </template>

        <!-- Error servidor -->
        <div
          v-if="errorServidor"
          class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200"
        >
          <svg
            class="w-4 h-4 text-red-500 flex-shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p class="text-xs text-red-700 font-medium">{{ errorServidor }}</p>
        </div>
      </form>

      <template #footer>
        <button @click="modalAbierto = false" class="btn-secondary">
          Cancelar
        </button>
        <button @click="guardar" :disabled="guardando" class="btn-primary">
          <svg
            v-if="guardando"
            class="w-4 h-4 animate-spin"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
          {{
            guardando
              ? "Guardando..."
              : modoEdicion
                ? "Actualizar"
                : "Crear usuario"
          }}
        </button>
      </template>
    </AppModal>

    <!-- ── MODAL CAMBIAR CONTRASEÑA ───────────────────────── -->
    <AppModal v-model="modalPassword" titulo="Cambiar Contraseña" ancho="sm">
      <form @submit.prevent="guardarPassword" class="space-y-4">
        <p class="text-sm text-gray-500">
          Cambiando contraseña de
          <span class="font-semibold text-gray-900">{{
            usuarioSeleccionado?.nombre_completo
          }}</span>
        </p>
        <div>
          <label class="form-label"
            >Nueva contraseña <span class="text-red-500">*</span></label
          >
          <input
            v-model="formPassword.password_nuevo"
            type="password"
            class="form-input"
            :class="{ 'form-input-error': erroresPass.password_nuevo }"
            placeholder="Mínimo 8 caracteres"
          />
          <p v-if="erroresPass.password_nuevo" class="form-error">
            {{ erroresPass.password_nuevo }}
          </p>
        </div>
        <div>
          <label class="form-label"
            >Confirmar contraseña <span class="text-red-500">*</span></label
          >
          <input
            v-model="formPassword.confirmar_password"
            type="password"
            class="form-input"
            :class="{ 'form-input-error': erroresPass.confirmar_password }"
            placeholder="Repite la contraseña"
          />
          <p v-if="erroresPass.confirmar_password" class="form-error">
            {{ erroresPass.confirmar_password }}
          </p>
        </div>
        <div
          v-if="errorServidor"
          class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200"
        >
          <p class="text-xs text-red-700 font-medium">{{ errorServidor }}</p>
        </div>
      </form>
      <template #footer>
        <button @click="modalPassword = false" class="btn-secondary">
          Cancelar
        </button>
        <button
          @click="guardarPassword"
          :disabled="guardando"
          class="btn-primary"
        >
          {{ guardando ? "Guardando..." : "Actualizar contraseña" }}
        </button>
      </template>
    </AppModal>

    <!-- ── MODAL CONFIRMAR DESACTIVAR ─────────────────────── -->
    <AppModal v-model="modalDesactivar" titulo="Desactivar Usuario" ancho="sm">
      <div class="text-center py-2">
        <div
          class="w-12 h-12 rounded-2xl bg-red-50 flex items-center justify-center mx-auto mb-3"
        >
          <svg
            class="w-6 h-6 text-red-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <p class="text-sm font-bold text-gray-900 mb-1">
          ¿Desactivar a {{ usuarioSeleccionado?.nombre_completo }}?
        </p>
        <p class="text-xs text-gray-500">
          El usuario no podrá ingresar al sistema.
        </p>
      </div>
      <template #footer>
        <button @click="modalDesactivar = false" class="btn-secondary">
          Cancelar
        </button>
        <button @click="desactivar" :disabled="guardando" class="btn-danger">
          {{ guardando ? "Procesando..." : "Sí, desactivar" }}
        </button>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from "vue";
import { useUsuariosStore } from "../stores/usuarios.store";
import { usuariosService } from "../services/usuarios.service";
import AppModal from "@/components/common/AppModal.vue";

const store = useUsuariosStore();

const busqueda = ref("");
const filtroRol = ref("");
const filtroSucursal = ref("");
const modalAbierto = ref(false);
const modalPassword = ref(false);
const modalDesactivar = ref(false);
const modoEdicion = ref(false);
const guardando = ref(false);
const mostrarPass = ref(false);
const errorServidor = ref("");
const usuarioSeleccionado = ref(null);

const formulario = reactive({
  nombres: "",
  apellidos: "",
  dni: "",
  telefono: "",
  correo: "",
  rol: "",
  sucursal: "",
  password: "",
  confirmar_password: "",
});

const errores = reactive({
  nombres: "",
  apellidos: "",
  dni: "",
  correo: "",
  rol: "",
  password: "",
  confirmar_password: "",
});

const formPassword = reactive({
  password_nuevo: "",
  confirmar_password: "",
});

const erroresPass = reactive({
  password_nuevo: "",
  confirmar_password: "",
});

// ── Computed ─────────────────────────────────────────────
const usuariosFiltrados = computed(() => {
  return store.usuarios.filter((u) => {
    const coincideBusqueda =
      !busqueda.value ||
      u.nombre_completo?.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      u.correo?.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      u.dni?.includes(busqueda.value);

    const coincideRol = !filtroRol.value || u.rol === filtroRol.value;
    const coincideSucursal =
      !filtroSucursal.value || u.sucursal === filtroSucursal.value;

    return coincideBusqueda && coincideRol && coincideSucursal;
  });
});

// ── Helpers ──────────────────────────────────────────────
function iniciales(u) {
  return (u.nombres?.[0] || "") + (u.apellidos?.[0] || "");
}

function claseRol(rol) {
  const mapa = {
    administrador: "badge badge-red",
    supervisor: "badge badge-yellow",
    cajero: "badge badge-blue",
  };
  return mapa[rol] || "badge badge-gray";
}

// ── Modal crear/editar ───────────────────────────────────
function limpiarFormulario() {
  Object.keys(formulario).forEach((k) => (formulario[k] = ""));
  Object.keys(errores).forEach((k) => (errores[k] = ""));
  errorServidor.value = "";
  mostrarPass.value = false;
}

function abrirModalCrear() {
  modoEdicion.value = false;
  limpiarFormulario();
  modalAbierto.value = true;
}

function abrirModalEditar(u) {
  modoEdicion.value = true;
  usuarioSeleccionado.value = u;
  limpiarFormulario();
  Object.assign(formulario, {
    nombres: u.nombres,
    apellidos: u.apellidos,
    dni: u.dni,
    telefono: u.telefono || "",
    correo: u.correo,
    rol: u.rol,
    sucursal: u.sucursal || "",
  });
  modalAbierto.value = true;
}

function abrirModalPassword(u) {
  usuarioSeleccionado.value = u;
  formPassword.password_nuevo = "";
  formPassword.confirmar_password = "";
  Object.keys(erroresPass).forEach((k) => (erroresPass[k] = ""));
  errorServidor.value = "";
  modalPassword.value = true;
}

function confirmarDesactivar(u) {
  usuarioSeleccionado.value = u;
  modalDesactivar.value = true;
}

// ── Validaciones ─────────────────────────────────────────
function validar() {
  let valido = true;
  Object.keys(errores).forEach((k) => (errores[k] = ""));

  if (!formulario.nombres) {
    errores.nombres = "Obligatorio";
    valido = false;
  }
  if (!formulario.apellidos) {
    errores.apellidos = "Obligatorio";
    valido = false;
  }
  if (!formulario.rol) {
    errores.rol = "Obligatorio";
    valido = false;
  }

  if (!formulario.dni || formulario.dni.length !== 8) {
    errores.dni = "El DNI debe tener 8 dígitos";
    valido = false;
  }

  if (!modoEdicion.value) {
    if (!formulario.correo) {
      errores.correo = "Obligatorio";
      valido = false;
    }
    if (!formulario.password || formulario.password.length < 8) {
      errores.password = "Mínimo 8 caracteres";
      valido = false;
    }
    if (formulario.password !== formulario.confirmar_password) {
      errores.confirmar_password = "Las contraseñas no coinciden";
      valido = false;
    }
  }

  return valido;
}

// ── Guardar ──────────────────────────────────────────────
async function guardar() {
  if (!validar()) return;

  guardando.value = true;
  errorServidor.value = "";

  try {
    if (modoEdicion.value) {
      const payload = {
        nombres: formulario.nombres,
        apellidos: formulario.apellidos,
        telefono: formulario.telefono,
        rol: formulario.rol,
        sucursal: formulario.sucursal || null,
      };
      await usuariosService.actualizarUsuario(
        usuarioSeleccionado.value.id,
        payload,
      );
    } else {
      const payload = {
        nombres: formulario.nombres,
        apellidos: formulario.apellidos,
        dni: formulario.dni,
        telefono: formulario.telefono,
        correo: formulario.correo,
        rol: formulario.rol,
        sucursal: formulario.sucursal || null,
        password: formulario.password,
        confirmar_password: formulario.confirmar_password,
      };
      await usuariosService.crearUsuario(payload);
    }

    modalAbierto.value = false;
    store.cargarUsuarios();
  } catch (e) {
    console.error("Error:", e.response?.data);
    const data = e.response?.data;
    if (data && typeof data === "object") {
      Object.keys(data).forEach((k) => {
        if (k in errores)
          errores[k] = Array.isArray(data[k]) ? data[k][0] : data[k];
      });
    }
    const primero = (v) => (Array.isArray(v) ? v[0] : v);
    const general =
      data && typeof data === "object"
        ? Object.entries(data)
            .filter(([k]) => !(k in errores))
            .map(([, v]) => primero(v))[0]
        : "";
    errorServidor.value = general || "Verifica los campos e intenta de nuevo.";
  } finally {
    guardando.value = false;
  }
}

// ── Cambiar contraseña ───────────────────────────────────
async function guardarPassword() {
  Object.keys(erroresPass).forEach((k) => (erroresPass[k] = ""));
  errorServidor.value = "";

  if (!formPassword.password_nuevo || formPassword.password_nuevo.length < 8) {
    erroresPass.password_nuevo = "Mínimo 8 caracteres";
    return;
  }
  if (formPassword.password_nuevo !== formPassword.confirmar_password) {
    erroresPass.confirmar_password = "Las contraseñas no coinciden";
    return;
  }

  guardando.value = true;
  try {
    await usuariosService.restablecerPassword(usuarioSeleccionado.value.id, {
      password_nuevo: formPassword.password_nuevo,
      confirmar_password: formPassword.confirmar_password,
    });
    modalPassword.value = false;
  } catch (e) {
    const data = e.response?.data;
    erroresPass.password_nuevo = data?.password_nuevo?.[0] || "";
    erroresPass.confirmar_password = data?.confirmar_password?.[0] || "";
    errorServidor.value =
      data?.password_nuevo?.[0] ||
      data?.detail ||
      "No se pudo actualizar la contraseña.";
  } finally {
    guardando.value = false;
  }
}

// ── Desactivar ───────────────────────────────────────────
async function desactivar() {
  guardando.value = true;
  try {
    await usuariosService.desactivarUsuario(usuarioSeleccionado.value.id);
    modalDesactivar.value = false;
    store.cargarUsuarios();
  } catch {
    errorServidor.value = "No se pudo desactivar el usuario.";
  } finally {
    guardando.value = false;
  }
}

// ── Inicializar ──────────────────────────────────────────
onMounted(() => {
  store.cargarUsuarios();
  store.cargarSucursales();
});
</script>
