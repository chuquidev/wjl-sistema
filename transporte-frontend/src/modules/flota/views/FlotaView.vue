<template>
  <div class="space-y-5">
    <!-- Encabezado -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Flota y Operaciones</h1>
        <p class="page-subtitle">Gestión de vehículos, conductores y viajes</p>
      </div>
      <button
        v-if="puedeGestionar"
        @click="abrirModalCrear"
        class="btn-primary"
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
            stroke-width="2.5"
            d="M12 4v16m8-8H4"
          />
        </svg>
        Nuevo {{ etiquetaTab }}
      </button>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 p-1 bg-gray-100 rounded-xl w-fit">
      <button
        v-for="tab in tabs"
        :key="tab.clave"
        @click="tabActivo = tab.clave"
        :class="[
          'px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-150',
          tabActivo === tab.clave
            ? 'bg-white text-gray-900 shadow-sm'
            : 'text-gray-500 hover:text-gray-700',
        ]"
      >
        {{ tab.etiqueta }}
        <span
          :class="[
            'ml-1.5 px-1.5 py-0.5 rounded-md text-[10px] font-black',
            tabActivo === tab.clave
              ? 'bg-orange-100 text-orange-600'
              : 'bg-gray-200 text-gray-500',
          ]"
          >{{ conteoTab(tab.clave) }}</span
        >
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
          :placeholder="`Buscar ${etiquetaTab.toLowerCase()}...`"
          class="form-input w-64"
          style="padding-left: 2.25rem"
        />
      </div>
      <select
        v-if="tabActivo !== 'viajes'"
        v-model="filtroEstado"
        class="form-input w-44"
      >
        <option value="">Todos los estados</option>
        <option value="disponible">Disponible</option>
        <option value="en_viaje">En viaje</option>
        <option value="inactivo">Inactivo</option>
        <option v-if="tabActivo === 'vehiculos'" value="mantenimiento">
          Mantenimiento
        </option>
      </select>

      <select
        v-if="tabActivo === 'viajes'"
        v-model="filtroEstado"
        class="form-input w-44"
      >
        <option value="">Todos los estados</option>
        <option value="programado">Programado</option>
        <option value="en_curso">En curso</option>
        <option value="completado">Completado</option>
        <option value="cancelado">Cancelado</option>
      </select>

      <input
        v-if="tabActivo === 'viajes'"
        v-model="filtroFecha"
        type="date"
        class="form-input w-44"
      />
    </div>

    <!-- ── TABLA VEHÍCULOS ───────────────────────────────── -->
    <div v-if="tabActivo === 'vehiculos'" class="card">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>Placa</th>
              <th>Vehículo</th>
              <th class="text-center">Año</th>
              <th class="text-center">Capacidad</th>
              <th>Estado</th>
              <th>Activo</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
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
            <tr v-else-if="!vehiculosFiltrados.length">
              <td colspan="7" class="text-center py-12 text-gray-400 italic">
                No se encontraron vehículos
              </td>
            </tr>
            <tr v-for="v in vehiculosFiltrados" :key="v.id">
              <td>
                <span
                  class="font-mono font-bold text-gray-900 bg-gray-100 px-2 py-1 rounded-lg text-sm"
                >
                  {{ v.placa }}
                </span>
              </td>
              <td>
                <p class="font-semibold text-gray-900">
                  {{ v.marca }} {{ v.modelo }}
                </p>
                <p
                  v-if="v.observacion"
                  class="text-xs text-gray-400 truncate max-w-[180px]"
                >
                  {{ v.observacion }}
                </p>
              </td>
              <td class="text-center text-gray-600">{{ v.anio }}</td>
              <td class="text-center">
                <span class="font-bold text-gray-900">{{ v.capacidad }}</span>
                <span class="text-xs text-gray-400 ml-1">asientos</span>
              </td>
              <td>
                <span :class="claseEstadoVehiculo(v.estado)">{{
                  etiquetaEstadoVehiculo(v.estado)
                }}</span>
              </td>
              <td>
                <span
                  :class="v.activo ? 'badge badge-green' : 'badge badge-gray'"
                  >{{ v.activo ? "Sí" : "No" }}</span
                >
              </td>
              <td class="text-right">
                <div
                  v-if="puedeGestionar"
                  class="flex items-center justify-end gap-1"
                >
                  <button
                    @click="abrirModalEditar(v)"
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
                    @click="abrirModalEstado(v)"
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
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
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

    <!-- ── TABLA CONDUCTORES ─────────────────────────────── -->
    <div v-if="tabActivo === 'conductores'" class="card">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>Conductor</th>
              <th>DNI</th>
              <th>Licencia</th>
              <th class="text-center">Categoría</th>
              <th>Vencimiento</th>
              <th>Estado</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
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
            <tr v-else-if="!conductoresFiltrados.length">
              <td colspan="7" class="text-center py-12 text-gray-400 italic">
                No se encontraron conductores
              </td>
            </tr>
            <tr v-for="c in conductoresFiltrados" :key="c.id">
              <td>
                <div class="flex items-center gap-3">
                  <div
                    class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xs flex-shrink-0"
                  >
                    {{ c.nombres?.[0] }}{{ c.apellidos?.[0] }}
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900 text-sm">
                      {{ c.apellidos }}, {{ c.nombres }}
                    </p>
                    <p class="text-xs text-gray-400">{{ c.telefono }}</p>
                  </div>
                </div>
              </td>
              <td class="font-mono text-sm text-gray-700">{{ c.dni }}</td>
              <td class="font-mono text-sm text-gray-700">{{ c.licencia }}</td>
              <td class="text-center">
                <span class="badge badge-blue">{{ c.categoria_licencia }}</span>
              </td>
              <td>
                <span
                  :class="
                    licenciaVencida(c.vencimiento_licencia)
                      ? 'badge badge-red'
                      : 'badge badge-green'
                  "
                >
                  {{ formatearFecha(c.vencimiento_licencia) }}
                </span>
              </td>
              <td>
                <span :class="claseEstadoConductor(c.estado)">{{
                  etiquetaEstadoConductor(c.estado)
                }}</span>
              </td>
              <td class="text-right">
                <div
                  v-if="puedeGestionar"
                  class="flex items-center justify-end gap-1"
                >
                  <button
                    @click="abrirModalEditar(c)"
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
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── TABLA VIAJES ──────────────────────────────────── -->
    <div v-if="tabActivo === 'viajes'" class="card">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>Ruta</th>
              <th>Vehículo</th>
              <th>Conductor</th>
              <th class="text-center">Salida</th>
              <th class="text-center">Ocupación</th>
              <th>Estado</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
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
            <tr v-else-if="!viajesFiltrados.length">
              <td colspan="7" class="text-center py-12 text-gray-400 italic">
                No se encontraron viajes
              </td>
            </tr>
            <tr v-for="v in viajesFiltrados" :key="v.id">
              <td>
                <p class="font-bold text-gray-900 text-sm">
                  {{ v.ruta_descripcion }}
                </p>
              </td>
              <td>
                <span
                  class="font-mono text-sm font-bold text-gray-700 bg-gray-100 px-2 py-0.5 rounded"
                >
                  {{ v.vehiculo_placa }}
                </span>
              </td>
              <td class="text-gray-600 text-sm">{{ v.conductor_nombre }}</td>
              <td class="text-center">
                <p
                  class="font-mono font-bold text-blue-600 text-xs bg-blue-50 px-2 py-1 rounded-lg"
                >
                  {{ formatearFechaHora(v.fecha_salida) }}
                </p>
              </td>
              <td class="text-center">
                <div class="flex items-center gap-2 justify-center">
                  <div
                    class="w-16 h-2 bg-gray-100 rounded-full overflow-hidden"
                  >
                    <div
                      class="h-full rounded-full transition-all"
                      :class="
                        porcentajeOcupacion(v) >= 80
                          ? 'bg-emerald-500'
                          : porcentajeOcupacion(v) >= 50
                            ? 'bg-amber-400'
                            : 'bg-red-400'
                      "
                      :style="{ width: porcentajeOcupacion(v) + '%' }"
                    ></div>
                  </div>
                  <span
                    class="text-xs font-bold text-gray-600 whitespace-nowrap"
                  >
                    {{ v.asientos_ocupados }}/{{
                      v.asientos_disponibles + v.asientos_ocupados
                    }}
                  </span>
                </div>
              </td>
              <td>
                <span :class="claseEstadoViaje(v.estado)">{{
                  etiquetaEstadoViaje(v.estado)
                }}</span>
              </td>
              <td class="text-right">
                <div
                  v-if="puedeGestionar"
                  class="flex items-center justify-end gap-1"
                >
                  <button
                    @click="abrirModalEditar(v)"
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
                    @click="abrirModalEstado(v)"
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
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
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
      :key="tabActivo"
      v-model="modalAbierto"
      :titulo="tituloModal"
      ancho="lg"
    >
      <form @submit.prevent="guardar" class="space-y-4">
        <!-- Vehículo -->
        <template v-if="tabActivo === 'vehiculos'">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label"
                >Placa <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.placa"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.placa }"
                placeholder="Ej: ABC-123"
                style="text-transform: uppercase"
              />
              <p v-if="errores.placa" class="form-error">{{ errores.placa }}</p>
            </div>
            <div>
              <label class="form-label"
                >Año <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.anio"
                type="number"
                min="1990"
                :max="anioActual"
                class="form-input"
                :class="{ 'form-input-error': errores.anio }"
                placeholder="Ej: 2020"
              />
              <p v-if="errores.anio" class="form-error">{{ errores.anio }}</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label"
                >Marca <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.marca"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.marca }"
                placeholder="Ej: Toyota"
              />
              <p v-if="errores.marca" class="form-error">{{ errores.marca }}</p>
            </div>
            <div>
              <label class="form-label"
                >Modelo <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.modelo"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.modelo }"
                placeholder="Ej: Hiace"
              />
              <p v-if="errores.modelo" class="form-error">
                {{ errores.modelo }}
              </p>
            </div>
          </div>
          <div>
            <label class="form-label"
              >Capacidad de asientos <span class="text-red-500">*</span></label
            >
            <input
              v-model="formulario.capacidad"
              type="number"
              min="1"
              max="60"
              class="form-input"
              :class="{ 'form-input-error': errores.capacidad }"
              placeholder="Ej: 15"
            />
            <p v-if="errores.capacidad" class="form-error">
              {{ errores.capacidad }}
            </p>
          </div>
          <div>
            <label class="form-label">Observación</label>
            <textarea
              v-model="formulario.observacion"
              rows="2"
              class="form-input resize-none"
              placeholder="Notas adicionales..."
            />
          </div>
        </template>

        <!-- Conductor -->
        <template v-if="tabActivo === 'conductores'">
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
                placeholder="Ej: Juan"
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
                placeholder="Ej: López"
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
              <label class="form-label"
                >Teléfono <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.telefono"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.telefono }"
                placeholder="Ej: 987654321"
              />
              <p v-if="errores.telefono" class="form-error">
                {{ errores.telefono }}
              </p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label"
                >N° Licencia <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.licencia"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.licencia }"
                placeholder="Ej: Q12345678"
              />
              <p v-if="errores.licencia" class="form-error">
                {{ errores.licencia }}
              </p>
            </div>
            <div>
              <label class="form-label"
                >Categoría <span class="text-red-500">*</span></label
              >
              <select
                v-model="formulario.categoria_licencia"
                class="form-input"
                :class="{ 'form-input-error': errores.categoria_licencia }"
              >
                <option value="">Seleccionar...</option>
                <option value="A-I">A-I</option>
                <option value="A-IIa">A-IIa</option>
                <option value="A-IIb">A-IIb</option>
                <option value="A-IIIa">A-IIIa</option>
                <option value="A-IIIb">A-IIIb</option>
                <option value="A-IIIc">A-IIIc</option>
              </select>
              <p v-if="errores.categoria_licencia" class="form-error">
                {{ errores.categoria_licencia }}
              </p>
            </div>
          </div>
          <div>
            <label class="form-label"
              >Vencimiento de licencia
              <span class="text-red-500">*</span></label
            >
            <input
              v-model="formulario.vencimiento_licencia"
              type="date"
              class="form-input"
              :class="{ 'form-input-error': errores.vencimiento_licencia }"
            />
            <p v-if="errores.vencimiento_licencia" class="form-error">
              {{ errores.vencimiento_licencia }}
            </p>
          </div>
        </template>

        <!-- Viaje -->
        <template v-if="tabActivo === 'viajes'">
          <div>
            <label class="form-label"
              >Ruta <span class="text-red-500">*</span></label
            >
            <select
              v-model="formulario.ruta"
              class="form-input"
              :class="{ 'form-input-error': errores.ruta }"
            >
              <option value="">Seleccionar ruta...</option>
              <option v-for="r in store.rutas" :key="r.id" :value="r.id">
                {{ r.origen_nombre }} → {{ r.destino_nombre }} (S/.
                {{ r.precio_base }})
              </option>
            </select>
            <p v-if="errores.ruta" class="form-error">{{ errores.ruta }}</p>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label"
                >Vehículo <span class="text-red-500">*</span></label
              >
              <select
                v-model="formulario.vehiculo"
                class="form-input"
                :class="{ 'form-input-error': errores.vehiculo }"
              >
                <option value="">Seleccionar vehículo...</option>
                <option v-for="v in store.vehiculos" :key="v.id" :value="v.id">
                  {{ v.placa }} — {{ v.marca }} {{ v.modelo }} ({{
                    v.capacidad
                  }}
                  asientos)
                </option>
              </select>
              <p v-if="errores.vehiculo" class="form-error">
                {{ errores.vehiculo }}
              </p>
            </div>
            <div>
              <label class="form-label"
                >Conductor <span class="text-red-500">*</span></label
              >
              <select
                v-model="formulario.conductor"
                class="form-input"
                :class="{ 'form-input-error': errores.conductor }"
              >
                <option value="">Seleccionar conductor...</option>
                <option
                  v-for="c in store.conductores"
                  :key="c.id"
                  :value="c.id"
                >
                  {{ c.apellidos }}, {{ c.nombres }}
                </option>
              </select>
              <p v-if="errores.conductor" class="form-error">
                {{ errores.conductor }}
              </p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label"
                >Fecha y hora de salida
                <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.fecha_salida"
                type="datetime-local"
                class="form-input"
                :class="{ 'form-input-error': errores.fecha_salida }"
              />
              <p v-if="errores.fecha_salida" class="form-error">
                {{ errores.fecha_salida }}
              </p>
            </div>
            <div>
              <label class="form-label">Fecha y hora de llegada</label>
              <input
                v-model="formulario.fecha_llegada"
                type="datetime-local"
                class="form-input"
              />
              <p class="form-hint">Opcional</p>
            </div>
          </div>
          <div>
            <label class="form-label">Observación</label>
            <textarea
              v-model="formulario.observacion"
              rows="2"
              class="form-input resize-none"
              placeholder="Notas del viaje..."
            />
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
            guardando ? "Guardando..." : modoEdicion ? "Actualizar" : "Guardar"
          }}
        </button>
      </template>
    </AppModal>

    <!-- ── MODAL CAMBIAR ESTADO ───────────────────────────── -->
    <AppModal v-model="modalEstado" titulo="Cambiar Estado" ancho="sm">
      <div class="space-y-3">
        <p
          v-if="errorServidor"
          class="text-xs text-red-700 font-medium p-3 rounded-lg bg-red-50 border border-red-200"
        >
          {{ errorServidor }}
        </p>
        <p class="text-sm text-gray-500 mb-4">
          Selecciona el nuevo estado para
          <span class="font-semibold text-gray-900">
            {{
              tabActivo === "vehiculos"
                ? itemSeleccionado?.placa
                : itemSeleccionado?.ruta_descripcion
            }}
          </span>
        </p>
        <template v-if="tabActivo === 'vehiculos'">
          <button
            v-for="est in estadosVehiculo"
            :key="est.valor"
            @click="nuevoEstado = est.valor"
            :class="[
              'w-full flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all text-left',
              nuevoEstado === est.valor
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-100 hover:border-gray-200 bg-white',
            ]"
          >
            <span
              :class="['w-2.5 h-2.5 rounded-full flex-shrink-0', est.punto]"
            ></span>
            <span class="text-sm font-semibold text-gray-800">{{
              est.etiqueta
            }}</span>
          </button>
        </template>
        <template v-if="tabActivo === 'viajes'">
          <button
            v-for="est in estadosViaje"
            :key="est.valor"
            @click="nuevoEstado = est.valor"
            :class="[
              'w-full flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all text-left',
              nuevoEstado === est.valor
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-100 hover:border-gray-200 bg-white',
            ]"
          >
            <span
              :class="['w-2.5 h-2.5 rounded-full flex-shrink-0', est.punto]"
            ></span>
            <span class="text-sm font-semibold text-gray-800">{{
              est.etiqueta
            }}</span>
          </button>
        </template>
      </div>
      <template #footer>
        <button @click="modalEstado = false" class="btn-secondary">
          Cancelar
        </button>
        <button
          @click="guardarEstado"
          :disabled="guardando || !nuevoEstado"
          class="btn-primary"
        >
          {{ guardando ? "Guardando..." : "Confirmar" }}
        </button>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch } from "vue";
import { useRoute } from "vue-router";
import { useFlotaStore } from "../stores/flota.store";
import { flotaService } from "../services/flota.service";
import AppModal from "@/components/common/AppModal.vue";
import { useAuthStore } from "@/modules/auth/stores/auth.store";

const store = useFlotaStore();
const auth = useAuthStore();
const route = useRoute();

// El backend solo deja crear/editar flota a administrador y supervisor
const puedeGestionar = computed(() => auth.esAdmin || auth.esSupervisor);

// ── Tab inicial según URL ────────────────────────────────
const tabActivo = ref(
  route.path.includes("conductores")
    ? "conductores"
    : route.path.includes("viajes")
      ? "viajes"
      : "vehiculos",
);

const busqueda = ref("");
const filtroEstado = ref("");
const filtroFecha = ref("");
const modalAbierto = ref(false);
const modalEstado = ref(false);
const modoEdicion = ref(false);
const guardando = ref(false);
const errorServidor = ref("");
const itemSeleccionado = ref(null);
const nuevoEstado = ref("");
const anioActual = new Date().getFullYear();

const tabs = [
  { clave: "vehiculos", etiqueta: "Vehículos" },
  { clave: "conductores", etiqueta: "Conductores" },
  { clave: "viajes", etiqueta: "Viajes" },
];

const formulario = reactive({
  // Vehículo
  placa: "",
  marca: "",
  modelo: "",
  anio: "",
  capacidad: "",
  observacion: "",
  // Conductor
  nombres: "",
  apellidos: "",
  dni: "",
  telefono: "",
  licencia: "",
  categoria_licencia: "",
  vencimiento_licencia: "",
  // Viaje
  ruta: "",
  vehiculo: "",
  conductor: "",
  fecha_salida: "",
  fecha_llegada: "",
});

const errores = reactive({
  placa: "",
  marca: "",
  modelo: "",
  anio: "",
  capacidad: "",
  nombres: "",
  apellidos: "",
  dni: "",
  telefono: "",
  licencia: "",
  categoria_licencia: "",
  vencimiento_licencia: "",
  ruta: "",
  vehiculo: "",
  conductor: "",
  fecha_salida: "",
});

const estadosVehiculo = [
  { valor: "disponible", etiqueta: "Disponible", punto: "bg-emerald-500" },
  { valor: "en_viaje", etiqueta: "En viaje", punto: "bg-blue-500" },
  { valor: "mantenimiento", etiqueta: "Mantenimiento", punto: "bg-amber-500" },
  { valor: "inactivo", etiqueta: "Inactivo", punto: "bg-gray-400" },
];

const estadosViaje = [
  { valor: "programado", etiqueta: "Programado", punto: "bg-gray-400" },
  { valor: "en_curso", etiqueta: "En curso", punto: "bg-emerald-500" },
  { valor: "completado", etiqueta: "Completado", punto: "bg-blue-500" },
  { valor: "cancelado", etiqueta: "Cancelado", punto: "bg-red-500" },
];

// ── Computed ─────────────────────────────────────────────
const etiquetaTab = computed(
  () =>
    ({ vehiculos: "Vehículo", conductores: "Conductor", viajes: "Viaje" })[
      tabActivo.value
    ] || "",
);

const tituloModal = computed(
  () => `${modoEdicion.value ? "Editar" : "Nuevo"} ${etiquetaTab.value}`,
);

const conteoTab = (clave) =>
  ({
    vehiculos: store.vehiculos.length,
    conductores: store.conductores.length,
    viajes: store.viajes.length,
  })[clave] || 0;

const vehiculosFiltrados = computed(() =>
  store.vehiculos.filter(
    (v) =>
      (!busqueda.value ||
        v.placa.toLowerCase().includes(busqueda.value.toLowerCase()) ||
        `${v.marca} ${v.modelo}`
          .toLowerCase()
          .includes(busqueda.value.toLowerCase())) &&
      (!filtroEstado.value || v.estado === filtroEstado.value),
  ),
);

const conductoresFiltrados = computed(() =>
  store.conductores.filter(
    (c) =>
      (!busqueda.value ||
        `${c.nombres} ${c.apellidos}`
          .toLowerCase()
          .includes(busqueda.value.toLowerCase()) ||
        c.dni?.includes(busqueda.value) ||
        c.licencia?.toLowerCase().includes(busqueda.value.toLowerCase())) &&
      (!filtroEstado.value || c.estado === filtroEstado.value),
  ),
);

const viajesFiltrados = computed(() =>
  store.viajes.filter(
    (v) =>
      (!busqueda.value ||
        v.ruta_descripcion
          ?.toLowerCase()
          .includes(busqueda.value.toLowerCase()) ||
        v.vehiculo_placa
          ?.toLowerCase()
          .includes(busqueda.value.toLowerCase())) &&
      (!filtroEstado.value || v.estado === filtroEstado.value) &&
      (!filtroFecha.value || v.fecha_salida?.startsWith(filtroFecha.value)),
  ),
);

// ── Helpers visuales ─────────────────────────────────────
function claseEstadoVehiculo(estado) {
  return (
    {
      disponible: "badge badge-green",
      en_viaje: "badge badge-blue",
      mantenimiento: "badge badge-yellow",
      inactivo: "badge badge-gray",
    }[estado] || "badge badge-gray"
  );
}
function etiquetaEstadoVehiculo(estado) {
  return (
    {
      disponible: "Disponible",
      en_viaje: "En viaje",
      mantenimiento: "Mantenimiento",
      inactivo: "Inactivo",
    }[estado] || estado
  );
}
function claseEstadoConductor(estado) {
  return (
    {
      disponible: "badge badge-green",
      en_viaje: "badge badge-blue",
      inactivo: "badge badge-gray",
    }[estado] || "badge badge-gray"
  );
}
function etiquetaEstadoConductor(estado) {
  return (
    { disponible: "Disponible", en_viaje: "En viaje", inactivo: "Inactivo" }[
      estado
    ] || estado
  );
}
function claseEstadoViaje(estado) {
  return (
    {
      programado: "badge badge-gray",
      en_curso: "badge badge-green",
      completado: "badge badge-blue",
      cancelado: "badge badge-red",
    }[estado] || "badge badge-gray"
  );
}
function etiquetaEstadoViaje(estado) {
  return (
    {
      programado: "Programado",
      en_curso: "En curso",
      completado: "Completado",
      cancelado: "Cancelado",
    }[estado] || estado
  );
}
function formatearFecha(fecha) {
  if (!fecha) return "—";
  return new Date(fecha + "T00:00:00").toLocaleDateString("es-PE");
}
function formatearFechaHora(fecha) {
  if (!fecha) return "—";
  return new Date(fecha).toLocaleTimeString("es-PE", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}
function licenciaVencida(fecha) {
  if (!fecha) return false;
  return new Date(fecha) < new Date();
}
function porcentajeOcupacion(viaje) {
  const total =
    (viaje.asientos_ocupados || 0) + (viaje.asientos_disponibles || 0);
  return total > 0 ? Math.round((viaje.asientos_ocupados / total) * 100) : 0;
}

// ── Cargar datos por tab ──────────────────────────────────
function cargarTab(tab) {
  if (tab === "vehiculos") store.cargarVehiculos();
  if (tab === "conductores") store.cargarConductores();
  if (tab === "viajes") {
    store.cargarViajes();
    store.cargarVehiculos();
    store.cargarConductores();
    store.cargarRutas();
  }
}

// ── Watchers ─────────────────────────────────────────────

// Sincronizar tab al navegar desde el sidebar
watch(
  () => route.path,
  (path) => {
    if (path.includes("conductores")) tabActivo.value = "conductores";
    else if (path.includes("viajes")) tabActivo.value = "viajes";
    else tabActivo.value = "vehiculos";
    cargarTab(tabActivo.value);
  },
  { immediate: true },
);

// Resetear filtros al cambiar tab manualmente
watch(tabActivo, () => {
  busqueda.value = "";
  filtroEstado.value = "";
  filtroFecha.value = "";
});

// ── Modal crear/editar ───────────────────────────────────
function limpiarFormulario() {
  Object.keys(formulario).forEach((k) => (formulario[k] = ""));
  Object.keys(errores).forEach((k) => (errores[k] = ""));
  errorServidor.value = "";
}

function abrirModalCrear() {
  modoEdicion.value = false;
  limpiarFormulario();
  if (tabActivo.value === "viajes") {
    store.cargarVehiculos();
    store.cargarConductores();
    store.cargarRutas();
  }
  modalAbierto.value = true;
}

function abrirModalEditar(item) {
  modoEdicion.value = true;
  itemSeleccionado.value = item;
  limpiarFormulario();

  if (tabActivo.value === "vehiculos") {
    Object.assign(formulario, {
      placa: item.placa,
      marca: item.marca,
      modelo: item.modelo,
      anio: item.anio,
      capacidad: item.capacidad,
      observacion: item.observacion || "",
    });
  } else if (tabActivo.value === "conductores") {
    Object.assign(formulario, {
      nombres: item.nombres,
      apellidos: item.apellidos,
      dni: item.dni,
      telefono: item.telefono,
      licencia: item.licencia,
      categoria_licencia: item.categoria_licencia,
      vencimiento_licencia: item.vencimiento_licencia,
    });
  } else if (tabActivo.value === "viajes") {
    store.cargarVehiculos();
    store.cargarConductores();
    store.cargarRutas();
    Object.assign(formulario, {
      ruta: item.ruta,
      vehiculo: item.vehiculo,
      conductor: item.conductor,
      fecha_salida: item.fecha_salida?.slice(0, 16) || "",
      fecha_llegada: item.fecha_llegada?.slice(0, 16) || "",
      observacion: item.observacion || "",
    });
  }

  modalAbierto.value = true;
}

function abrirModalEstado(item) {
  itemSeleccionado.value = item;
  nuevoEstado.value = item.estado;
  errorServidor.value = "";
  modalEstado.value = true;
}

// ── Validaciones ─────────────────────────────────────────
function validar() {
  let valido = true;
  Object.keys(errores).forEach((k) => (errores[k] = ""));

  if (tabActivo.value === "vehiculos") {
    if (!formulario.placa) {
      errores.placa = "Obligatorio";
      valido = false;
    }
    if (!formulario.marca) {
      errores.marca = "Obligatorio";
      valido = false;
    }
    if (!formulario.modelo) {
      errores.modelo = "Obligatorio";
      valido = false;
    }
    if (!formulario.anio) {
      errores.anio = "Obligatorio";
      valido = false;
    }
    if (!formulario.capacidad) {
      errores.capacidad = "Obligatorio";
      valido = false;
    }
  }

  if (tabActivo.value === "conductores") {
    if (!formulario.nombres) {
      errores.nombres = "Obligatorio";
      valido = false;
    }
    if (!formulario.apellidos) {
      errores.apellidos = "Obligatorio";
      valido = false;
    }
    if (!formulario.telefono) {
      errores.telefono = "Obligatorio";
      valido = false;
    }
    if (!formulario.licencia) {
      errores.licencia = "Obligatorio";
      valido = false;
    }
    if (!formulario.categoria_licencia) {
      errores.categoria_licencia = "Obligatorio";
      valido = false;
    }
    if (!formulario.vencimiento_licencia) {
      errores.vencimiento_licencia = "Obligatorio";
      valido = false;
    }
    if (!formulario.dni || formulario.dni.length !== 8) {
      errores.dni = "El DNI debe tener 8 dígitos";
      valido = false;
    }
  }

  if (tabActivo.value === "viajes") {
    if (!formulario.ruta) {
      errores.ruta = "Obligatorio";
      valido = false;
    }
    if (!formulario.vehiculo) {
      errores.vehiculo = "Obligatorio";
      valido = false;
    }
    if (!formulario.conductor) {
      errores.conductor = "Obligatorio";
      valido = false;
    }
    if (!formulario.fecha_salida) {
      errores.fecha_salida = "Obligatorio";
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
    let payload = {};

    if (tabActivo.value === "vehiculos") {
      payload = {
        placa: formulario.placa.toUpperCase(),
        marca: formulario.marca,
        modelo: formulario.modelo,
        anio: formulario.anio,
        capacidad: formulario.capacidad,
        observacion: formulario.observacion,
      };
    } else if (tabActivo.value === "conductores") {
      payload = {
        nombres: formulario.nombres,
        apellidos: formulario.apellidos,
        dni: formulario.dni,
        telefono: formulario.telefono,
        licencia: formulario.licencia,
        categoria_licencia: formulario.categoria_licencia,
        vencimiento_licencia: formulario.vencimiento_licencia,
      };
    } else if (tabActivo.value === "viajes") {
      payload = {
        ruta: formulario.ruta,
        vehiculo: formulario.vehiculo,
        conductor: formulario.conductor,
        fecha_salida: formulario.fecha_salida,
        fecha_llegada: formulario.fecha_llegada || null,
        observacion: formulario.observacion,
      };
    }

    if (modoEdicion.value) {
      if (tabActivo.value === "vehiculos")
        await flotaService.actualizarVehiculo(
          itemSeleccionado.value.id,
          payload,
        );
      if (tabActivo.value === "conductores")
        await flotaService.actualizarConductor(
          itemSeleccionado.value.id,
          payload,
        );
      if (tabActivo.value === "viajes")
        await flotaService.actualizarViaje(itemSeleccionado.value.id, payload);
    } else {
      if (tabActivo.value === "vehiculos")
        await flotaService.crearVehiculo(payload);
      if (tabActivo.value === "conductores")
        await flotaService.crearConductor(payload);
      if (tabActivo.value === "viajes") await flotaService.crearViaje(payload);
    }

    modalAbierto.value = false;
    cargarTab(tabActivo.value);
  } catch (e) {
    console.error("Error al guardar:", e.response?.data);
    errorServidor.value = mensajeErrorServidor(e, e.response?.data);
  } finally {
    guardando.value = false;
  }
}

// Errores por campo (vehiculo, conductor...) y mensaje general del backend
function mensajeErrorServidor(e, data) {
  if (e.response?.status === 403) {
    return data?.detail || "No tienes permiso para realizar esta acción.";
  }
  if (!data || typeof data !== "object")
    return "No se pudo guardar. Intenta de nuevo.";
  const primero = (v) => (Array.isArray(v) ? v[0] : v);
  let general = "";
  Object.keys(data).forEach((k) => {
    if (k in errores) errores[k] = primero(data[k]);
    else general = general || primero(data[k]);
  });
  return general || "Verifica los campos e intenta de nuevo.";
}

// ── Cambiar estado ───────────────────────────────────────
async function guardarEstado() {
  if (!nuevoEstado.value) return;
  guardando.value = true;
  try {
    if (tabActivo.value === "vehiculos") {
      await flotaService.cambiarEstadoVehiculo(
        itemSeleccionado.value.id,
        nuevoEstado.value,
      );
    } else if (tabActivo.value === "viajes") {
      await flotaService.cambiarEstadoViaje(
        itemSeleccionado.value.id,
        nuevoEstado.value,
      );
    }
    modalEstado.value = false;
    cargarTab(tabActivo.value);
  } catch (e) {
    errorServidor.value =
      e.response?.data?.error ||
      e.response?.data?.detail ||
      "No se pudo cambiar el estado.";
  } finally {
    guardando.value = false;
  }
}
</script>
