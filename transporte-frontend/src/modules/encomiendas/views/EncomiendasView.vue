<template>
  <div class="space-y-5">
    <!-- Encabezado -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Encomiendas</h1>
        <p class="page-subtitle">Registro y seguimiento de encomiendas</p>
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
        Nueva Encomienda
      </button>
    </div>

    <!-- Filtros -->
    <div class="flex flex-wrap gap-3">
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
          placeholder="Buscar por codigo, remitente o destinatario..."
          class="form-input w-80"
          style="padding-left: 2.25rem"
        />
      </div>
      <select v-model="filtroEstado" class="form-input w-44">
        <option value="">Todos los estados</option>
        <option value="registrada">Registrada</option>
        <option value="en_transito">En transito</option>
        <option value="entregada">Entregada</option>
        <option value="devuelta">Devuelta</option>
      </select>
      <input v-model="filtroFecha" type="date" class="form-input w-44" />
      <button @click="cargarEncomiendas" class="btn-secondary">
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
        Actualizar
      </button>
    </div>

    <!-- Tarjetas resumen -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="estado in estadosSummary"
        :key="estado.clave"
        class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4"
      >
        <div class="flex items-center justify-between mb-2">
          <p class="text-xs font-bold uppercase tracking-wide text-gray-400">
            {{ estado.etiqueta }}
          </p>
          <span :class="['w-2.5 h-2.5 rounded-full', estado.punto]"></span>
        </div>
        <p :class="['text-2xl font-black', estado.color]">
          {{ resumen[estado.clave] ?? 0 }}
        </p>
      </div>
    </div>

    <!-- Tabla -->
    <div class="card">
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>Codigo</th>
              <th>Remitente</th>
              <th>Destinatario</th>
              <th>Descripcion</th>
              <th class="text-center">Peso</th>
              <th>Viaje</th>
              <th class="text-right">Precio</th>
              <th>Estado</th>
              <th class="text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="store.cargando">
              <td colspan="9">
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
            <tr v-else-if="!encomiendasFiltradas.length">
              <td colspan="9" class="text-center py-12 text-gray-400 italic">
                No se encontraron encomiendas
              </td>
            </tr>
            <tr v-for="e in encomiendasFiltradas" :key="e.id">
              <td>
                <span
                  class="font-mono text-xs font-bold text-gray-700 bg-gray-100 px-2 py-1 rounded"
                >
                  {{
                    String(e.codigo || "")
                      .slice(0, 8)
                      .toUpperCase()
                  }}
                </span>
              </td>
              <td>
                <p class="font-semibold text-gray-900 text-sm">
                  {{ e.remitente_nombre }}
                </p>
                <p class="text-xs text-gray-400 font-mono">
                  {{ e.remitente_dni }}
                </p>
              </td>
              <td>
                <p class="font-semibold text-gray-900 text-sm">
                  {{ e.destinatario_nombre }}
                </p>
                <p class="text-xs text-gray-400 font-mono">
                  {{ e.destinatario_dni }}
                </p>
              </td>
              <td class="text-sm text-gray-600 max-w-[160px] truncate">
                {{ e.descripcion }}
              </td>
              <td class="text-center">
                <span class="text-sm font-bold text-gray-700">
                  {{ e.peso_kg ? e.peso_kg + " kg" : "-" }}
                </span>
              </td>
              <td class="text-xs text-gray-500">
                {{ e.viaje_descripcion || "-" }}
              </td>
              <td class="text-right font-black text-gray-900">
                S/. {{ e.precio }}
              </td>
              <td>
                <span :class="claseEstado(e.estado)">{{
                  etiquetaEstado(e.estado)
                }}</span>
              </td>
              <td class="text-right">
                <div class="flex items-center justify-end gap-1">
                  <!-- Ver comprobante -->
                  <button
                    @click="verComprobante(e)"
                    title="Ver comprobante"
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
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                  </button>
                  <!-- Reimprimir ticket físico -->
                  <button
                    @click="reimprimirEncomienda(e)"
                    title="Imprimir ticket"
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
                        d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
                      />
                    </svg>
                  </button>
                  <!-- Editar -->
                  <button
                    v-if="['registrada', 'en_transito'].includes(e.estado)"
                    @click="abrirModalEditar(e)"
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

                  <!-- Marcar como entregada -->
                  <button
                    v-if="['registrada', 'en_transito'].includes(e.estado)"
                    @click="abrirModalEntrega(e)"
                    title="Marcar como entregado"
                    class="w-8 h-8 rounded-lg hover:bg-emerald-50 flex items-center justify-center text-gray-400 hover:text-emerald-600 transition-colors"
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
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  </button>

                  <!-- Eliminar -->
                  <button
                    v-if="e.estado === 'registrada'"
                    @click="abrirModalEliminar(e)"
                    title="Eliminar"
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
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Paginación -->
        <div
          v-if="totalPaginas > 1"
          class="flex items-center justify-between px-4 py-3 bg-white rounded-2xl border border-gray-100"
        >
          <p class="text-sm text-gray-500">
            Página
            <span class="font-bold text-gray-900">{{ paginaActual }}</span> de
            <span class="font-bold text-gray-900">{{ totalPaginas }}</span> ·
            {{ totalRegistros }} registros
          </p>
          <div class="flex items-center gap-2">
            <button
              @click="
                paginaActual--;
                cargarEncomiendas();
              "
              :disabled="paginaActual === 1"
              class="btn-secondary py-1.5 px-3 text-sm disabled:opacity-40"
            >
              ← Anterior
            </button>
            <button
              @click="
                paginaActual++;
                cargarEncomiendas();
              "
              :disabled="paginaActual === totalPaginas"
              class="btn-secondary py-1.5 px-3 text-sm disabled:opacity-40"
            >
              Siguiente →
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL REGISTRAR / EDITAR ENCOMIENDA -->
    <AppModal
      v-model="modalCrear"
      :titulo="modoEdicion ? 'Editar Encomienda' : 'Nueva Encomienda'"
      ancho="xl"
    >
      <form @submit.prevent="guardar" class="space-y-5">
        <!-- Fecha y hora de envío -->
        <div>
          <h4
            class="text-sm font-black text-gray-700 uppercase tracking-wide mb-3 flex items-center gap-2"
          >
            <span
              class="w-5 h-5 rounded-full bg-violet-100 text-violet-600 flex items-center justify-center text-[10px] font-black"
              >📅</span
            >
            Fecha y hora de envío
          </h4>
          <div class="grid grid-cols-1 gap-4">
            <div>
              <label class="form-label"
                >Fecha de envío <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.fecha_envio"
                type="date"
                class="form-input"
                :min="hoy"
                @change="onFechaEnvioChange"
              />
            </div>
          </div>
        </div>

        <div class="border-t border-gray-100"></div>

        <!-- Remitente -->
        <div>
          <h4
            class="text-sm font-black text-gray-700 uppercase tracking-wide mb-3 flex items-center gap-2"
          >
            <span
              class="w-5 h-5 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-[10px] font-black"
              >1</span
            >
            Remitente (quien envia)
          </h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label"
                >DNI <span class="text-red-500">*</span></label
              >
              <div class="flex gap-2">
                <input
                  v-model="formulario.remitente_dni"
                  type="text"
                  maxlength="8"
                  class="form-input"
                  :class="{ 'form-input-error': errores.remitente_dni }"
                  placeholder="12345678"
                  @keyup.enter="buscarRemitente"
                />
                <button
                  type="button"
                  @click="buscarRemitente"
                  :disabled="buscandoRemitente"
                  class="btn-secondary flex-shrink-0 px-3"
                >
                  <svg
                    :class="[
                      'w-4 h-4',
                      buscandoRemitente ? 'animate-spin' : '',
                    ]"
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
                </button>
              </div>
              <p v-if="errores.remitente_dni" class="form-error">
                {{ errores.remitente_dni }}
              </p>
              <p
                v-if="remitenteEncontrado"
                class="text-xs text-emerald-600 font-bold mt-1"
              >
                ✓ Datos autocargados
              </p>
            </div>
            <div>
              <label class="form-label">Telefono remitente</label>
              <input
                v-model="formulario.remitente_telefono"
                type="text"
                class="form-input"
                placeholder="987654321"
              />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 mt-3">
            <div>
              <label class="form-label"
                >Nombres <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.remitente_nombres"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.remitente_nombres }"
                placeholder="Nombres del remitente"
              />
              <p v-if="errores.remitente_nombres" class="form-error">
                {{ errores.remitente_nombres }}
              </p>
            </div>
            <div>
              <label class="form-label"
                >Apellidos <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.remitente_apellidos"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.remitente_apellidos }"
                placeholder="Apellidos del remitente"
              />
              <p v-if="errores.remitente_apellidos" class="form-error">
                {{ errores.remitente_apellidos }}
              </p>
            </div>
          </div>
        </div>

        <div class="border-t border-gray-100"></div>

        <!-- Destinatario -->
        <div>
          <h4
            class="text-sm font-black text-gray-700 uppercase tracking-wide mb-3 flex items-center gap-2"
          >
            <span
              class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-[10px] font-black"
              >2</span
            >
            Destinatario (quien recibe)
          </h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="form-label"
                >DNI <span class="text-red-500">*</span></label
              >
              <div class="flex gap-2">
                <input
                  v-model="formulario.destinatario_dni"
                  type="text"
                  maxlength="8"
                  class="form-input"
                  :class="{ 'form-input-error': errores.destinatario_dni }"
                  placeholder="12345678"
                  @keyup.enter="buscarDestinatario"
                />
                <button
                  type="button"
                  @click="buscarDestinatario"
                  :disabled="buscandoDestinatario"
                  class="btn-secondary flex-shrink-0 px-3"
                >
                  <svg
                    :class="[
                      'w-4 h-4',
                      buscandoDestinatario ? 'animate-spin' : '',
                    ]"
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
                </button>
              </div>
              <p v-if="errores.destinatario_dni" class="form-error">
                {{ errores.destinatario_dni }}
              </p>
              <p
                v-if="destinatarioEncontrado"
                class="text-xs text-emerald-600 font-bold mt-1"
              >
                ✓ Datos autocargados
              </p>
            </div>
            <div>
              <label class="form-label">Telefono destinatario</label>
              <input
                v-model="formulario.destinatario_telefono"
                type="text"
                class="form-input"
                placeholder="987654321"
              />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 mt-3">
            <div>
              <label class="form-label"
                >Nombres <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.destinatario_nombres"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.destinatario_nombres }"
                placeholder="Nombres del destinatario"
              />
              <p v-if="errores.destinatario_nombres" class="form-error">
                {{ errores.destinatario_nombres }}
              </p>
            </div>
            <div>
              <label class="form-label"
                >Apellidos <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.destinatario_apellidos"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.destinatario_apellidos }"
                placeholder="Apellidos del destinatario"
              />
              <p v-if="errores.destinatario_apellidos" class="form-error">
                {{ errores.destinatario_apellidos }}
              </p>
            </div>
          </div>
        </div>

        <div class="border-t border-gray-100"></div>

        <!-- Datos de la encomienda -->
        <div>
          <h4
            class="text-sm font-black text-gray-700 uppercase tracking-wide mb-3 flex items-center gap-2"
          >
            <span
              class="w-5 h-5 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center text-[10px] font-black"
              >3</span
            >
            Datos de la encomienda
          </h4>
          <div class="grid grid-cols-3 gap-4">
            <div class="col-span-2">
              <label class="form-label"
                >Descripcion <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.descripcion"
                type="text"
                class="form-input"
                :class="{ 'form-input-error': errores.descripcion }"
                placeholder="Ej: Ropa, documentos, electrodomestico..."
              />
              <p v-if="errores.descripcion" class="form-error">
                {{ errores.descripcion }}
              </p>
            </div>
            <div>
              <label class="form-label">Peso (kg)</label>
              <input
                v-model="formulario.peso_kg"
                type="number"
                step="0.1"
                min="0"
                class="form-input"
                placeholder="Ej: 2.5"
              />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 mt-3">
            <div>
              <label class="form-label"
                >Precio (S/.) <span class="text-red-500">*</span></label
              >
              <input
                v-model="formulario.precio"
                type="number"
                step="0.50"
                min="0"
                class="form-input text-lg font-bold"
                :class="{ 'form-input-error': errores.precio }"
                placeholder="0.00"
              />
              <p v-if="errores.precio" class="form-error">
                {{ errores.precio }}
              </p>
            </div>
            <div>
              <label class="form-label"
                >Metodo de pago <span class="text-red-500">*</span></label
              >
              <select
                v-model="formulario.metodo_pago"
                class="form-input"
                :class="{ 'form-input-error': errores.metodo_pago }"
              >
                <option value="">Seleccionar...</option>
                <option value="cash">Efectivo</option>
                <option value="yape">Yape</option>
                <option value="plin">Plin</option>
                <option value="card">Tarjeta</option>
              </select>
              <p v-if="errores.metodo_pago" class="form-error">
                {{ errores.metodo_pago }}
              </p>
            </div>
          </div>

          <!-- Viaje del día seleccionado -->
          <div class="mt-3">
            <label class="form-label">
              Viaje
              <span class="text-xs text-gray-400"
                >(viajes disponibles del día seleccionado)</span
              >
            </label>
            <div
              v-if="cargandoViajes"
              class="flex items-center gap-2 text-sm text-gray-400 py-2"
            >
              <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
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
              Cargando viajes...
            </div>
            <select v-else v-model="formulario.viaje" class="form-input">
              <option value="">Sin asignar a viaje</option>
              <option v-for="v in viajesDisponibles" :key="v.id" :value="v.id">
                {{ v.ruta_descripcion }} |
                {{ formatearFechaHora(v.fecha_salida) }} |
                {{ v.vehiculo_placa }}
              </option>
            </select>
            <p v-if="!formulario.fecha_envio" class="form-hint">
              Selecciona una fecha de envío para ver los viajes disponibles
            </p>
            <p
              v-else-if="viajesDisponibles.length === 0 && !cargandoViajes"
              class="form-hint text-amber-600"
            >
              No hay viajes disponibles para ese día
            </p>
          </div>

          <div class="mt-3">
            <label class="form-label">Observaciones</label>
            <textarea
              v-model="formulario.observacion"
              rows="2"
              class="form-input resize-none"
              placeholder="Instrucciones especiales, fragilidad, etc."
            />
          </div>
        </div>

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
        <button @click="modalCrear = false" class="btn-secondary">
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
              ? modoEdicion
                ? "Guardando..."
                : "Registrando..."
              : modoEdicion
                ? "Guardar cambios"
                : "Registrar encomienda"
          }}
        </button>
      </template>
    </AppModal>

    <!-- MODAL REGISTRAR ENTREGA -->
    <AppModal v-model="modalEntrega" titulo="Registrar entrega" ancho="sm">
      <div class="space-y-4">
        <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
          <p class="text-sm font-bold text-emerald-800 mb-1">
            Confirmando entrega a:
            {{ encomiendaSeleccionada?.destinatario_nombre }}
          </p>
          <p class="text-xs text-emerald-600">
            DNI: {{ encomiendaSeleccionada?.destinatario_dni }}
          </p>
        </div>
        <div>
          <label class="form-label">Observaciones de entrega</label>
          <textarea
            v-model="formEntrega.observaciones"
            rows="2"
            class="form-input resize-none"
            placeholder="Estado del paquete, notas..."
          />
        </div>
        <div
          v-if="erroresEntrega.servidor"
          class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200"
        >
          <p class="text-xs text-red-700 font-medium">
            {{ erroresEntrega.servidor }}
          </p>
        </div>
      </div>
      <template #footer>
        <button @click="modalEntrega = false" class="btn-secondary">
          Cancelar
        </button>
        <button
          @click="registrarEntrega"
          :disabled="guardando"
          class="btn-primary"
        >
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
          {{ guardando ? "Registrando..." : "Confirmar entrega" }}
        </button>
      </template>
    </AppModal>

    <!-- MODAL CONFIRMAR ELIMINAR -->
    <AppModal v-model="modalEliminar" titulo="Eliminar encomienda" ancho="sm">
      <div class="text-center py-2 space-y-3">
        <div
          class="w-14 h-14 rounded-2xl bg-red-50 flex items-center justify-center mx-auto"
        >
          <svg
            class="w-7 h-7 text-red-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </div>
        <p class="text-sm font-bold text-gray-900">
          ¿Eliminar esta encomienda?
        </p>
        <p class="text-xs text-gray-500">
          Código:
          <strong>{{
            String(encomiendaSeleccionada?.codigo || "")
              .slice(0, 8)
              .toUpperCase()
          }}</strong
          ><br />
          {{ encomiendaSeleccionada?.remitente_nombre }} →
          {{ encomiendaSeleccionada?.destinatario_nombre }}
        </p>
        <p class="text-xs text-red-500 font-medium">
          Esta acción no se puede deshacer.
        </p>
      </div>
      <template #footer>
        <button @click="modalEliminar = false" class="btn-secondary">
          Cancelar
        </button>
        <button
          @click="eliminarEncomienda"
          :disabled="guardando"
          class="btn-danger"
        >
          {{ guardando ? "Eliminando..." : "Confirmar eliminación" }}
        </button>
      </template>
    </AppModal>

    <!-- MODAL COMPROBANTE -->
    <TicketEncomienda v-model="modalComprobante" :enc="encomiendaComprobante" />
  </div>
</template>

<script setup>
import {
  ref,
  reactive,
  computed,
  onMounted,
  onBeforeUnmount,
  watch,
} from "vue";
import { useEncomiendasStore } from "../stores/encomiendas.store";
import { encomiendasService } from "../services/encomiendas.service";
import AppModal from "@/components/common/AppModal.vue";
import TicketEncomienda from "../components/TicketEncomienda.vue";
import { printerService } from "@/services/printer.service";

const store = useEncomiendasStore();

// ── Estado UI ─────────────────────────────────────────────
const busqueda = ref("");
const filtroEstado = ref("");
const filtroFecha = ref("");
const guardando = ref(false);
const errorServidor = ref("");
const modalCrear = ref(false);
const modalEntrega = ref(false);
const modalEliminar = ref(false);
const modalComprobante = ref(false);
const encomiendaSeleccionada = ref(null);
const encomiendaComprobante = ref(null);
const modoEdicion = ref(false);
const idEdicion = ref(null);

// ── Búsqueda personas ─────────────────────────────────────
const buscandoRemitente = ref(false);
const buscandoDestinatario = ref(false);
const remitenteEncontrado = ref(false);
const destinatarioEncontrado = ref(false);

// ── Viajes disponibles ────────────────────────────────────
const viajesDisponibles = ref([]);
const cargandoViajes = ref(false);

// ── Hoy ───────────────────────────────────────────────────
const hoy = new Date().toLocaleDateString("en-CA");

// Paginación
const resumen = reactive({
  registrada: 0,
  en_transito: 0,
  entregada: 0,
  devuelta: 0,
});
const paginaActual = ref(1);
const totalPaginas = ref(1);
const totalRegistros = ref(0);

// ── Formulario ────────────────────────────────────────────
const formulario = reactive({
  fecha_envio: hoy,
  remitente_dni: "",
  remitente_nombres: "",
  remitente_apellidos: "",
  remitente_telefono: "",
  destinatario_dni: "",
  destinatario_nombres: "",
  destinatario_apellidos: "",
  destinatario_telefono: "",
  descripcion: "",
  peso_kg: "",
  precio: "",
  metodo_pago: "",
  viaje: "",
  observacion: "",
});

const errores = reactive({
  remitente_dni: "",
  remitente_nombres: "",
  remitente_apellidos: "",
  destinatario_dni: "",
  destinatario_nombres: "",
  destinatario_apellidos: "",
  descripcion: "",
  precio: "",
  metodo_pago: "",
});

const formEntrega = reactive({ observaciones: "" });
const erroresEntrega = reactive({ servidor: "" });

// ── Stats ─────────────────────────────────────────────────
const estadosSummary = [
  {
    clave: "registrada",
    etiqueta: "Registradas",
    punto: "bg-gray-400",
    color: "text-gray-700",
  },
  {
    clave: "en_transito",
    etiqueta: "En transito",
    punto: "bg-blue-500",
    color: "text-blue-600",
  },
  {
    clave: "entregada",
    etiqueta: "Entregadas",
    punto: "bg-emerald-500",
    color: "text-emerald-600",
  },
  {
    clave: "devuelta",
    etiqueta: "Devueltas",
    punto: "bg-red-400",
    color: "text-red-500",
  },
];

const encomiendasFiltradas = computed(() => store.encomiendas);

// ── Helpers ───────────────────────────────────────────────
function claseEstado(estado) {
  return (
    {
      registrada: "badge badge-gray",
      en_transito: "badge badge-blue",
      entregada: "badge badge-green",
      devuelta: "badge badge-red",
    }[estado] || "badge badge-gray"
  );
}

function etiquetaEstado(estado) {
  return (
    {
      registrada: "Registrada",
      en_transito: "En transito",
      entregada: "Entregada",
      devuelta: "Devuelta",
    }[estado] || estado
  );
}

function formatearHora12(fecha) {
  if (!fecha) return "";
  return new Date(fecha).toLocaleTimeString("es-PE", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

function formatearFechaHora(fecha) {
  if (!fecha) return "";
  return new Date(fecha).toLocaleString("es-PE", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

// ── Cargar viajes disponibles ─────────────────────────────
async function onFechaEnvioChange() {
  formulario.viaje = "";
  viajesDisponibles.value = [];
  if (!formulario.fecha_envio) return;
  cargandoViajes.value = true;
  try {
    const { data } = await encomiendasService.buscarViajesDisponibles(
      formulario.fecha_envio,
    );
    viajesDisponibles.value = data.results ?? data;
  } catch {
    viajesDisponibles.value = [];
  } finally {
    cargandoViajes.value = false;
  }
}

async function reimprimirEncomienda(enc) {
  try {
    await printerService.imprimirEncomienda(enc);
  } catch (e) {
    console.error("Error reimprimir:", e.message);
  }
}

// ── Buscar personas por DNI ───────────────────────────────
async function buscarPersona(dni, tipo) {
  if (!dni || dni.length !== 8) return;
  if (tipo === "remitente") {
    buscandoRemitente.value = true;
    remitenteEncontrado.value = false;
  } else {
    buscandoDestinatario.value = true;
    destinatarioEncontrado.value = false;
  }

  try {
    const { data } = await encomiendasService.buscarPersona(dni);
    const p = Array.isArray(data) ? data[0] : data;
    if (p && (p.nombres || p.id)) {
      if (tipo === "remitente") {
        formulario.remitente_nombres = p.nombres;
        formulario.remitente_apellidos = p.apellidos;
        formulario.remitente_telefono = p.telefono || "";
        remitenteEncontrado.value = true;
      } else {
        formulario.destinatario_nombres = p.nombres;
        formulario.destinatario_apellidos = p.apellidos;
        formulario.destinatario_telefono = p.telefono || "";
        destinatarioEncontrado.value = true;
      }
    }
  } catch {
  } finally {
    buscandoRemitente.value = false;
    buscandoDestinatario.value = false;
  }
}

const buscarRemitente = () =>
  buscarPersona(formulario.remitente_dni, "remitente");
const buscarDestinatario = () =>
  buscarPersona(formulario.destinatario_dni, "destinatario");

// ── Limpiar formulario ────────────────────────────────────
function limpiarFormulario() {
  Object.keys(formulario).forEach((k) => (formulario[k] = ""));
  Object.keys(errores).forEach((k) => (errores[k] = ""));
  formulario.fecha_envio = hoy;
  errorServidor.value = "";
  remitenteEncontrado.value = false;
  destinatarioEncontrado.value = false;
  viajesDisponibles.value = [];
  modoEdicion.value = false;
  idEdicion.value = null;
}

// ── Abrir modal crear ─────────────────────────────────────
async function abrirModalCrear() {
  limpiarFormulario();
  modalCrear.value = true;
  await onFechaEnvioChange();
}

// ── Abrir modal editar ────────────────────────────────────
async function abrirModalEditar(enc) {
  limpiarFormulario();
  modoEdicion.value = true;
  idEdicion.value = enc.id;

  // Separar nombre completo en nombres/apellidos (aproximado)
  const partesRem = (enc.remitente_nombre || "").split(" ");
  const parteDes = (enc.destinatario_nombre || "").split(" ");

  formulario.remitente_dni = enc.remitente_dni || "";
  formulario.remitente_nombres = partesRem
    .slice(0, Math.ceil(partesRem.length / 2))
    .join(" ");
  formulario.remitente_apellidos = partesRem
    .slice(Math.ceil(partesRem.length / 2))
    .join(" ");
  formulario.remitente_telefono = enc.remitente_telefono || "";
  formulario.destinatario_dni = enc.destinatario_dni || "";
  formulario.destinatario_nombres = parteDes
    .slice(0, Math.ceil(parteDes.length / 2))
    .join(" ");
  formulario.destinatario_apellidos = parteDes
    .slice(Math.ceil(parteDes.length / 2))
    .join(" ");
  formulario.destinatario_telefono = enc.destinatario_telefono || "";
  formulario.descripcion = enc.descripcion || "";
  formulario.peso_kg = enc.peso_kg || "";
  formulario.precio = enc.precio || "";
  formulario.metodo_pago = enc.metodo_pago || "";
  formulario.viaje = enc.viaje || "";
  formulario.observacion = enc.observacion || "";
  formulario.fecha_envio = hoy;

  modalCrear.value = true;
  await onFechaEnvioChange();
  // Restaurar viaje si tenía uno
  if (enc.viaje) formulario.viaje = enc.viaje;
}

// ── Validar ───────────────────────────────────────────────
function validar() {
  let valido = true;
  Object.keys(errores).forEach((k) => (errores[k] = ""));
  if (!formulario.remitente_dni || formulario.remitente_dni.length !== 8) {
    errores.remitente_dni = "DNI de 8 digitos";
    valido = false;
  }
  if (!formulario.remitente_nombres.trim()) {
    errores.remitente_nombres = "Obligatorio";
    valido = false;
  }
  if (!formulario.remitente_apellidos.trim()) {
    errores.remitente_apellidos = "Obligatorio";
    valido = false;
  }
  if (
    !formulario.destinatario_dni ||
    formulario.destinatario_dni.length !== 8
  ) {
    errores.destinatario_dni = "DNI de 8 digitos";
    valido = false;
  }
  if (!formulario.destinatario_nombres.trim()) {
    errores.destinatario_nombres = "Obligatorio";
    valido = false;
  }
  if (!formulario.destinatario_apellidos.trim()) {
    errores.destinatario_apellidos = "Obligatorio";
    valido = false;
  }
  if (!formulario.descripcion.trim()) {
    errores.descripcion = "Obligatorio";
    valido = false;
  }
  if (!formulario.precio || parseFloat(formulario.precio) <= 0) {
    errores.precio = "Ingresa un precio valido";
    valido = false;
  }
  if (!formulario.metodo_pago) {
    errores.metodo_pago = "Selecciona un metodo de pago";
    valido = false;
  }
  return valido;
}

// ── Guardar (crear o editar) ──────────────────────────────
async function guardar() {
  if (!validar()) return;
  guardando.value = true;
  errorServidor.value = "";
  try {
    const payload = {
      remitente_dni: formulario.remitente_dni,
      remitente_nombres: formulario.remitente_nombres,
      remitente_apellidos: formulario.remitente_apellidos,
      remitente_telefono: formulario.remitente_telefono || "",
      destinatario_dni: formulario.destinatario_dni,
      destinatario_nombres: formulario.destinatario_nombres,
      destinatario_apellidos: formulario.destinatario_apellidos,
      destinatario_telefono: formulario.destinatario_telefono || "",
      descripcion: formulario.descripcion,
      peso_kg: formulario.peso_kg ? parseFloat(formulario.peso_kg) : null,
      precio: formulario.precio,
      metodo_pago: formulario.metodo_pago,
      viaje: formulario.viaje ? parseInt(formulario.viaje) : null,
      observacion: formulario.observacion || "",
    };

    if (modoEdicion.value) {
      await encomiendasService.actualizarEstado(idEdicion.value, payload);
      modalCrear.value = false;
    } else {
      const { data: nuevaEnc } =
        await encomiendasService.crearEncomienda(payload);
      modalCrear.value = false;
      try {
        await printerService.imprimirEncomienda(nuevaEnc);
      } catch (e) {
        console.warn("Impresion no disponible:", e.message);
      }
    }
    cargarEncomiendas();
  } catch (e) {
    const data = e.response?.data;
    if (data && typeof data === "object") {
      Object.keys(data).forEach((k) => {
        if (k in errores)
          errores[k] = Array.isArray(data[k]) ? data[k][0] : data[k];
      });
      const noMapeados = Object.entries(data)
        .filter(([k]) => !(k in errores))
        .map(([k, v]) => `${k}: ${Array.isArray(v) ? v[0] : v}`)
        .join(" | ");
      errorServidor.value =
        noMapeados || "Verifica los campos e intenta de nuevo.";
    } else {
      errorServidor.value = "Error de conexion. Intenta de nuevo.";
    }
  } finally {
    guardando.value = false;
  }
}

// ── Entrega ───────────────────────────────────────────────
function abrirModalEntrega(enc) {
  encomiendaSeleccionada.value = enc;
  Object.keys(formEntrega).forEach((k) => (formEntrega[k] = ""));
  Object.keys(erroresEntrega).forEach((k) => (erroresEntrega[k] = ""));
  modalEntrega.value = true;
}

async function registrarEntrega() {
  Object.keys(erroresEntrega).forEach((k) => (erroresEntrega[k] = ""));
  guardando.value = true;
  try {
    await encomiendasService.registrarEntrega(encomiendaSeleccionada.value.id, {
      entregado_a: encomiendaSeleccionada.value.destinatario_nombre,
    });
    modalEntrega.value = false;
    cargarEncomiendas();
  } catch {
    erroresEntrega.servidor =
      "No se pudo registrar la entrega. Intenta de nuevo.";
  } finally {
    guardando.value = false;
  }
}

// ── Eliminar ──────────────────────────────────────────────
function abrirModalEliminar(enc) {
  encomiendaSeleccionada.value = enc;
  modalEliminar.value = true;
}

async function eliminarEncomienda() {
  guardando.value = true;
  try {
    await encomiendasService.eliminarEncomienda(
      encomiendaSeleccionada.value.id,
    );
    modalEliminar.value = false;
    cargarEncomiendas();
  } catch (e) {
    console.error("Error eliminar:", e.response?.data);
  } finally {
    guardando.value = false;
  }
}

// ── Comprobante ───────────────────────────────────────────
function verComprobante(enc) {
  encomiendaComprobante.value = enc;
  modalComprobante.value = true;
}

// ── Cargar datos ──────────────────────────────────────────
async function cargarEncomiendas() {
  const filtros = {};
  if (busqueda.value.trim()) filtros.search = busqueda.value.trim();
  if (filtroFecha.value) filtros.fecha = filtroFecha.value;
  const params = { ...filtros, page: paginaActual.value };
  if (filtroEstado.value) params.estado = filtroEstado.value;
  await store.cargarEncomiendas(params);
  totalRegistros.value = store.total;
  totalPaginas.value = Math.max(1, Math.ceil(store.total / 10));
  try {
    const { data } = await encomiendasService.resumenEncomiendas(filtros);
    Object.assign(resumen, data);
  } catch {
    /* los contadores quedan como estaban */
  }
}

// Los filtros se aplican solos: texto con una pequeña espera, el resto al instante
let temporizador = null;
watch([busqueda, filtroEstado, filtroFecha], () => {
  clearTimeout(temporizador);
  temporizador = setTimeout(() => {
    paginaActual.value = 1;
    cargarEncomiendas();
  }, 300);
});
onBeforeUnmount(() => clearTimeout(temporizador));

onMounted(cargarEncomiendas);
</script>
