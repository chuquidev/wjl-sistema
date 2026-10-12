<template>
  <div class="space-y-5">
    <!-- Tabs -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Pasajes</h1>
        <p class="page-subtitle">Venta y gestión de pasajes</p>
      </div>
      <div class="flex gap-1 p-1 bg-gray-100 rounded-xl">
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
        </button>
      </div>
    </div>

    <!-- ── TAB VENTA ─────────────────────────────────────── -->
    <div v-if="tabActivo === 'venta'">
      <!-- PASO 1: Buscar viaje -->
      <div v-if="paso === 1" class="space-y-4">
        <div class="flex items-center gap-2 mb-2">
          <div
            class="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-black"
          >
            1
          </div>
          <h2 class="text-base font-bold text-gray-900">
            Buscar viaje disponible
          </h2>
        </div>
        <div class="card">
          <div class="card-body">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label class="form-label">Origen</label>
                <select v-model="busqueda.origen" class="form-input">
                  <option value="">Todos los orígenes</option>
                  <option v-for="c in ciudades" :key="c.id" :value="c.id">
                    {{ c.nombre }}
                  </option>
                </select>
              </div>
              <div>
                <label class="form-label">Destino</label>
                <select v-model="busqueda.destino" class="form-input">
                  <option value="">Todos los destinos</option>
                  <option v-for="c in ciudades" :key="c.id" :value="c.id">
                    {{ c.nombre }}
                  </option>
                </select>
              </div>
              <div>
                <label class="form-label">Fecha</label>
                <input
                  v-model="busqueda.fecha"
                  type="date"
                  class="form-input"
                />
              </div>
            </div>
            <div class="flex justify-end mt-4">
              <button
                @click="buscarViajes"
                :disabled="store.cargando"
                class="btn-primary"
              >
                <svg
                  :class="['w-4 h-4', store.cargando ? 'animate-spin' : '']"
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
                Buscar viajes
              </button>
            </div>
          </div>
        </div>

        <div
          v-if="errorSeleccion"
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
          <p class="text-sm text-red-700 font-medium">{{ errorSeleccion }}</p>
        </div>

        <div v-if="store.viajes.length" class="space-y-3">
          <p class="text-sm text-gray-500 font-medium">
            {{ store.viajes.length }} viaje(s) encontrado(s)
          </p>
          <div
            v-for="viaje in store.viajes"
            :key="viaje.id"
            @click="seleccionarViaje(viaje)"
            :class="[
              'card transition-all duration-150 group',
              !viaje.acepta_venta
                ? 'opacity-60 cursor-not-allowed border-gray-100'
                : 'cursor-pointer hover:border-blue-300 hover:shadow-md',
            ]"
          >
            <div class="card-body">
              <div class="flex items-center justify-between gap-4">
                <div class="flex-1">
                  <div class="flex items-center gap-3 mb-2 flex-wrap">
                    <p class="font-black text-gray-900 text-base">
                      {{ viaje.ruta_descripcion }}
                    </p>
                    <span class="badge badge-blue">{{
                      viaje.vehiculo_placa
                    }}</span>
                    <span v-if="!viaje.acepta_venta" class="badge badge-red"
                      >Venta cerrada</span
                    >
                    <span
                      v-else-if="viaje.asientos_disponibles === 0"
                      class="badge badge-red"
                      >Sin asientos</span
                    >
                    <span v-else class="badge badge-green">Disponible</span>
                  </div>
                  <div class="flex items-center gap-4 text-sm text-gray-500">
                    <span class="flex items-center gap-1">
                      <svg
                        class="w-3.5 h-3.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      {{ formatearFechaHora(viaje.fecha_salida) }}
                    </span>
                    <span class="flex items-center gap-1">
                      <svg
                        class="w-3.5 h-3.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                        />
                      </svg>
                      {{ viaje.conductor_nombre }}
                    </span>
                  </div>
                </div>
                <div class="text-right flex-shrink-0">
                  <p class="text-2xl font-black text-orange-600">
                    S/. {{ viaje.precio_base }}
                  </p>
                  <div class="flex items-center gap-2 mt-1 justify-end">
                    <div
                      class="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden"
                    >
                      <div
                        class="h-full rounded-full"
                        :class="
                          ocupacion(viaje) >= 80
                            ? 'bg-red-400'
                            : ocupacion(viaje) >= 50
                              ? 'bg-amber-400'
                              : 'bg-emerald-500'
                        "
                        :style="{ width: ocupacion(viaje) + '%' }"
                      ></div>
                    </div>
                    <span class="text-xs font-bold text-gray-500"
                      >{{ viaje.asientos_disponibles }} libres</span
                    >
                  </div>
                </div>
                <svg
                  v-if="viaje.acepta_venta"
                  class="w-5 h-5 text-gray-300 group-hover:text-blue-500 transition-colors flex-shrink-0"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div
          v-else-if="busquedaRealizada && !store.cargando"
          class="text-center py-16 text-gray-400"
        >
          <svg
            class="w-12 h-12 mx-auto mb-3 text-gray-200"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10l2 2h8zm0 0l2-5h3l2 5m-7 0h7"
            />
          </svg>
          <p class="font-medium">No hay viajes disponibles</p>
          <p class="text-sm mt-1">Intenta con otra fecha o ruta</p>
        </div>
      </div>

      <!-- PASO 2: Seleccionar asientos -->
      <div v-if="paso === 2" class="space-y-4">
        <div class="flex items-center gap-3">
          <button
            @click="
              paso = 1;
              viajeSeleccionado = null;
              errorSeleccion = '';
            "
            class="btn-ghost"
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
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Volver
          </button>
          <div
            class="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-black"
          >
            2
          </div>
          <h2 class="text-base font-bold text-gray-900">
            Seleccionar asientos
          </h2>
        </div>

        <div class="card bg-blue-50 border-blue-200">
          <div class="card-body">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-black text-blue-900">
                  {{ viajeSeleccionado?.ruta_descripcion }}
                </p>
                <p class="text-sm text-blue-600 mt-0.5">
                  {{ formatearFechaHora(viajeSeleccionado?.fecha_salida) }} ·
                  {{ viajeSeleccionado?.vehiculo_placa }}
                </p>
              </div>
              <p class="text-2xl font-black text-blue-700">
                S/. {{ viajeSeleccionado?.precio_base }}
              </p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Mapa de asientos</h3>
              <span class="text-xs text-gray-400 font-medium"
                >Toca para seleccionar varios</span
              >
            </div>
            <div class="card-body flex justify-center">
              <div v-if="cargandoAsientos" class="flex justify-center py-8">
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
              <MapaAsientosCombi
                v-else
                v-model="asientosSeleccionados"
                :ocupados="asientosOcupados"
                :capacidad="viajeSeleccionado?.capacidad || 18"
              />
            </div>
          </div>

          <div class="space-y-4">
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">Disponibilidad</h3>
              </div>
              <div class="card-body grid grid-cols-3 gap-3">
                <div class="text-center p-3 bg-emerald-50 rounded-xl">
                  <p class="text-2xl font-black text-emerald-600">
                    {{ asientosLibres }}
                  </p>
                  <p
                    class="text-[10px] font-bold text-gray-500 uppercase tracking-wide mt-1"
                  >
                    Libres
                  </p>
                </div>
                <div class="text-center p-3 bg-red-50 rounded-xl">
                  <p class="text-2xl font-black text-red-500">
                    {{ asientosOcupados.length }}
                  </p>
                  <p
                    class="text-[10px] font-bold text-gray-500 uppercase tracking-wide mt-1"
                  >
                    Ocupados
                  </p>
                </div>
                <div class="text-center p-3 bg-gray-50 rounded-xl">
                  <p class="text-2xl font-black text-gray-700">
                    {{ viajeSeleccionado?.capacidad || 18 }}
                  </p>
                  <p
                    class="text-[10px] font-bold text-gray-500 uppercase tracking-wide mt-1"
                  >
                    Total
                  </p>
                </div>
              </div>
            </div>

            <div
              v-if="asientosSeleccionados.length"
              class="card border-blue-200 bg-blue-50"
            >
              <div class="card-body">
                <p class="text-sm font-bold text-blue-800 mb-2">
                  {{ asientosSeleccionados.length }} asiento(s) seleccionado(s)
                </p>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="n in asientosSeleccionados
                      .slice()
                      .sort((a, b) => a - b)"
                    :key="n"
                    class="px-2 py-1 bg-blue-600 text-white rounded-lg text-xs font-black"
                    >Asiento {{ n }}</span
                  >
                </div>
                <p class="text-xs text-blue-600 font-semibold mt-2">
                  Total estimado: S/.
                  {{
                    (
                      asientosSeleccionados.length *
                      viajeSeleccionado?.precio_base
                    ).toFixed(2)
                  }}
                </p>
              </div>
            </div>

            <button
              @click="irAPaso3"
              :disabled="!asientosSeleccionados.length"
              class="btn-primary w-full justify-center py-3"
            >
              Continuar con {{ asientosSeleccionados.length || 0 }} asiento(s)
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
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- PASO 3: Datos pasajeros y pago -->
      <div v-if="paso === 3" class="space-y-4">
        <div class="flex items-center gap-3">
          <button @click="paso = 2" class="btn-ghost">
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
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Volver
          </button>
          <div
            class="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-black"
          >
            3
          </div>
          <h2 class="text-base font-bold text-gray-900">
            Datos de los pasajeros
          </h2>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div class="lg:col-span-2 space-y-4">
            <!-- Card por pasajero -->
            <div
              v-for="(form, idx) in formulariosPasajeros"
              :key="form.asiento"
              class="card"
            >
              <div class="card-header">
                <div class="flex items-center gap-2">
                  <span
                    class="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-black"
                    >{{ idx + 1 }}</span
                  >
                  <h3 class="card-title">Asiento {{ form.asiento }}</h3>
                </div>
                <span
                  v-if="form.pasajeroEncontrado"
                  class="inline-flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-1 rounded-lg"
                >
                  <svg
                    class="w-3 h-3"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="3"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  Registrado
                </span>
                <span
                  v-else-if="form.buscado"
                  class="inline-flex items-center gap-1 text-xs font-bold text-amber-700 bg-amber-50 border border-amber-200 px-2 py-1 rounded-lg"
                >
                  ⚠ Nuevo pasajero
                </span>
              </div>
              <div class="card-body space-y-3">
                <!-- DNI -->
                <div>
                  <label class="form-label"
                    >DNI <span class="text-red-500">*</span></label
                  >
                  <div class="flex gap-2">
                    <input
                      v-model="form.dni"
                      type="text"
                      maxlength="8"
                      class="form-input"
                      :class="{ 'form-input-error': form.errores.dni }"
                      placeholder="12345678"
                      @keyup.enter="buscarPorDni(idx)"
                    />
                    <button
                      @click="buscarPorDni(idx)"
                      :disabled="form.buscando"
                      class="btn-secondary flex-shrink-0"
                    >
                      <svg
                        :class="[
                          'w-4 h-4',
                          form.buscando ? 'animate-spin' : '',
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
                      Buscar
                    </button>
                  </div>
                  <p v-if="form.errores.dni" class="form-error">
                    {{ form.errores.dni }}
                  </p>
                  <p
                    v-else-if="form.pasajeroEncontrado"
                    class="text-xs text-emerald-600 font-bold mt-1"
                  >
                    ✓ Pasajero encontrado — datos autocargados
                  </p>
                  <p
                    v-else-if="form.buscado && !form.pasajeroEncontrado"
                    class="text-xs text-amber-600 font-bold mt-1"
                  >
                    ⚠ No registrado — completa los datos manualmente
                  </p>
                </div>

                <!-- Nombres y apellidos -->
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="form-label"
                      >Nombres <span class="text-red-500">*</span></label
                    >
                    <input
                      v-model="form.nombres"
                      type="text"
                      class="form-input"
                      :class="{ 'form-input-error': form.errores.nombres }"
                      placeholder="Ej: Juan Carlos"
                    />
                    <p v-if="form.errores.nombres" class="form-error">
                      {{ form.errores.nombres }}
                    </p>
                  </div>
                  <div>
                    <label class="form-label"
                      >Apellidos <span class="text-red-500">*</span></label
                    >
                    <input
                      v-model="form.apellidos"
                      type="text"
                      class="form-input"
                      :class="{ 'form-input-error': form.errores.apellidos }"
                      placeholder="Ej: López Torres"
                    />
                    <p v-if="form.errores.apellidos" class="form-error">
                      {{ form.errores.apellidos }}
                    </p>
                  </div>
                </div>

                <!-- Teléfono -->
                <div>
                  <label class="form-label">Teléfono</label>
                  <input
                    v-model="form.telefono"
                    type="text"
                    class="form-input"
                    placeholder="Ej: 987654321"
                  />
                  <p class="form-hint">Opcional — para envío por WhatsApp</p>
                </div>

                <!-- ── PRECIO POR PASAJERO ──────────────────── -->
                <div class="border-t border-gray-100 pt-3">
                  <label class="form-label">
                    Precio del pasaje
                    <span class="ml-2 text-xs font-normal text-gray-400"
                      >(precio base: S/.
                      {{ viajeSeleccionado?.precio_base }})</span
                    >
                  </label>
                  <div class="flex items-center gap-3">
                    <div class="flex items-center gap-2 flex-1 max-w-[200px]">
                      <span
                        class="text-sm font-bold text-gray-500 flex-shrink-0"
                        >S/.</span
                      >
                      <input
                        v-model.number="form.precio"
                        type="number"
                        min="0"
                        step="0.50"
                        class="form-input font-black text-orange-600"
                        :class="{
                          'form-input-error': form.errores.precio,
                          'border-amber-300 bg-amber-50':
                            form.precio < viajeSeleccionado?.precio_base,
                          'border-gray-200':
                            form.precio >= viajeSeleccionado?.precio_base,
                        }"
                      />
                    </div>
                    <!-- Indicador si el precio es menor al base -->
                    <div
                      v-if="form.precio < viajeSeleccionado?.precio_base"
                      class="flex items-center gap-1.5 text-xs font-bold text-amber-600 bg-amber-50 border border-amber-200 px-2 py-1.5 rounded-lg"
                    >
                      <svg
                        class="w-3.5 h-3.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"
                        />
                      </svg>
                      Descuento S/.
                      {{
                        (viajeSeleccionado?.precio_base - form.precio).toFixed(
                          2,
                        )
                      }}
                    </div>
                    <!-- Botón restaurar precio base -->
                    <button
                      v-if="form.precio !== viajeSeleccionado?.precio_base"
                      @click="form.precio = viajeSeleccionado?.precio_base"
                      class="text-xs text-blue-500 hover:text-blue-700 font-semibold underline whitespace-nowrap"
                    >
                      Restaurar
                    </button>
                  </div>
                  <p v-if="form.errores.precio" class="form-error">
                    {{ form.errores.precio }}
                  </p>
                </div>
                <!-- ── FIN PRECIO ──────────────────────────── -->

                <!-- ── SECCIÓN PAQUETES ─────────────────────── -->
                <div class="border-t border-gray-100 pt-3">
                  <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center gap-2">
                      <svg
                        class="w-4 h-4 text-orange-500"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                        />
                      </svg>
                      <span class="text-sm font-bold text-gray-700"
                        >Paquetes / Bultos</span
                      >
                      <span class="text-xs text-gray-400">(opcional)</span>
                    </div>
                    <button
                      type="button"
                      @click="agregarPaquete(idx)"
                      class="inline-flex items-center gap-1 text-xs font-bold text-orange-600 hover:text-orange-700 bg-orange-50 hover:bg-orange-100 border border-orange-200 px-3 py-1.5 rounded-lg transition-colors"
                    >
                      <svg
                        class="w-3 h-3"
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
                      Agregar paquete
                    </button>
                  </div>

                  <div v-if="form.paquetes.length" class="space-y-3">
                    <div
                      v-for="(pkg, pidx) in form.paquetes"
                      :key="pidx"
                      class="p-3 bg-orange-50 border border-orange-100 rounded-xl space-y-3"
                    >
                      <div class="flex items-center justify-between">
                        <span
                          class="text-xs font-black text-orange-700 uppercase tracking-wide"
                          >Paquete {{ pidx + 1 }}</span
                        >
                        <button
                          type="button"
                          @click="quitarPaquete(idx, pidx)"
                          class="w-6 h-6 rounded-lg hover:bg-red-100 flex items-center justify-center text-gray-400 hover:text-red-500 transition-colors"
                        >
                          <svg
                            class="w-3.5 h-3.5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2.5"
                              d="M6 18L18 6M6 6l12 12"
                            />
                          </svg>
                        </button>
                      </div>
                      <div>
                        <label class="form-label text-xs"
                          >Descripción
                          <span class="text-red-500">*</span></label
                        >
                        <input
                          v-model="pkg.descripcion"
                          type="text"
                          class="form-input text-sm"
                          :class="{
                            'form-input-error': pkg.errores?.descripcion,
                          }"
                          placeholder="Ej: Ropa, alimentos, herramientas..."
                        />
                        <p v-if="pkg.errores?.descripcion" class="form-error">
                          {{ pkg.errores.descripcion }}
                        </p>
                      </div>
                      <div class="grid grid-cols-3 gap-2">
                        <div>
                          <label class="form-label text-xs"
                            >Bultos <span class="text-red-500">*</span></label
                          >
                          <input
                            v-model.number="pkg.cantidad_bultos"
                            type="number"
                            min="1"
                            class="form-input text-sm"
                            :class="{
                              'form-input-error': pkg.errores?.cantidad_bultos,
                            }"
                            placeholder="1"
                          />
                          <p
                            v-if="pkg.errores?.cantidad_bultos"
                            class="form-error"
                          >
                            {{ pkg.errores.cantidad_bultos }}
                          </p>
                        </div>
                        <div>
                          <label class="form-label text-xs">Peso (kg)</label>
                          <input
                            v-model.number="pkg.peso_kg"
                            type="number"
                            step="0.1"
                            min="0"
                            class="form-input text-sm"
                            placeholder="0.0"
                          />
                        </div>
                        <div>
                          <label class="form-label text-xs"
                            >Precio S/.
                            <span class="text-red-500">*</span></label
                          >
                          <input
                            v-model.number="pkg.precio_adicional"
                            type="number"
                            step="0.50"
                            min="0"
                            class="form-input text-sm font-bold"
                            :class="{
                              'form-input-error': pkg.errores?.precio_adicional,
                            }"
                            placeholder="0.00"
                          />
                          <p
                            v-if="pkg.errores?.precio_adicional"
                            class="form-error"
                          >
                            {{ pkg.errores.precio_adicional }}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div
                      class="flex justify-between items-center px-3 py-2 bg-orange-100 rounded-xl"
                    >
                      <span class="text-xs font-bold text-orange-700"
                        >{{ totalBultosForm(form) }} bulto(s) en total</span
                      >
                      <span class="text-sm font-black text-orange-700"
                        >+ S/. {{ totalPaquetesForm(form).toFixed(2) }}</span
                      >
                    </div>
                  </div>

                  <p v-else class="text-xs text-gray-400 italic">
                    Sin paquetes — este pasajero solo lleva equipaje de mano
                  </p>
                </div>
                <!-- ── FIN PAQUETES ─────────────────────────── -->
              </div>
            </div>

            <!-- Método de pago -->
            <div class="card">
              <div class="card-header">
                <h3 class="card-title">Método de pago</h3>
              </div>
              <div class="card-body">
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <button
                    v-for="mp in metodosPago"
                    :key="mp.clave"
                    @click="metodoPago = mp.clave"
                    :class="[
                      'flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all',
                      metodoPago === mp.clave
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-100 hover:border-gray-200 bg-white',
                    ]"
                  >
                    <span class="text-2xl">{{ mp.emoji }}</span>
                    <span class="text-xs font-bold text-gray-700">{{
                      mp.etiqueta
                    }}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Resumen lateral -->
          <div class="space-y-4">
            <div class="card sticky top-20">
              <div class="card-header">
                <h3 class="card-title">Resumen</h3>
              </div>
              <div class="card-body space-y-3">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">Ruta</span>
                  <span
                    class="font-bold text-gray-900 text-right max-w-[140px]"
                    >{{ viajeSeleccionado?.ruta_descripcion }}</span
                  >
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">Salida</span>
                  <span class="font-bold text-gray-900">{{
                    formatearFechaHora(viajeSeleccionado?.fecha_salida)
                  }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">Vehículo</span>
                  <span class="font-mono font-bold text-gray-900">{{
                    viajeSeleccionado?.vehiculo_placa
                  }}</span>
                </div>

                <!-- Desglose por pasajero -->
                <div class="border-t border-gray-100 pt-3 space-y-2">
                  <p
                    class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2"
                  >
                    Detalle
                  </p>
                  <div
                    v-for="form in formulariosPasajeros"
                    :key="form.asiento"
                    class="space-y-1"
                  >
                    <div class="flex justify-between text-sm">
                      <span class="font-black text-blue-600"
                        >Asiento {{ form.asiento }}</span
                      >
                      <div class="text-right">
                        <!-- Precio modificado: mostrar tachado y nuevo -->
                        <template
                          v-if="form.precio !== viajeSeleccionado?.precio_base"
                        >
                          <span class="text-xs text-gray-300 line-through block"
                            >S/. {{ viajeSeleccionado?.precio_base }}</span
                          >
                          <span class="font-black text-amber-600"
                            >S/. {{ form.precio }}</span
                          >
                        </template>
                        <span v-else class="font-bold text-gray-700"
                          >S/. {{ form.precio }}</span
                        >
                      </div>
                    </div>
                    <div
                      v-if="form.paquetes.length"
                      class="flex justify-between text-xs pl-3"
                    >
                      <span class="text-orange-600"
                        >📦 {{ totalBultosForm(form) }} bulto(s)</span
                      >
                      <span class="font-bold text-orange-600"
                        >+ S/. {{ totalPaquetesForm(form).toFixed(2) }}</span
                      >
                    </div>
                  </div>
                </div>

                <div
                  class="flex justify-between text-sm border-t border-gray-100 pt-3"
                >
                  <span class="text-gray-500">Pago</span>
                  <span class="font-bold text-gray-700">{{
                    metodosPago.find((m) => m.clave === metodoPago)?.etiqueta ||
                    "—"
                  }}</span>
                </div>

                <!-- Subtotales -->
                <div class="space-y-1 border-t border-gray-100 pt-2">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-500">Pasajes</span>
                    <span class="font-bold text-gray-900"
                      >S/. {{ totalPasajes.toFixed(2) }}</span
                    >
                  </div>
                  <div
                    v-if="totalPaquetesGeneral > 0"
                    class="flex justify-between text-sm"
                  >
                    <span class="text-orange-500">Paquetes</span>
                    <span class="font-bold text-orange-600"
                      >+ S/. {{ totalPaquetesGeneral.toFixed(2) }}</span
                    >
                  </div>
                </div>

                <div
                  class="flex justify-between items-center bg-orange-50 rounded-xl p-3"
                >
                  <span class="font-bold text-gray-700">Total</span>
                  <span class="text-2xl font-black text-orange-600"
                    >S/. {{ totalGeneral.toFixed(2) }}</span
                  >
                </div>

                <div
                  v-if="errorVenta"
                  class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200"
                >
                  <p class="text-xs text-red-700 font-medium">
                    {{ errorVenta }}
                  </p>
                </div>

                <button
                  @click="confirmarVenta"
                  :disabled="guardando"
                  class="btn-primary w-full justify-center py-3"
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
                  {{
                    guardando
                      ? "Procesando..."
                      : `Confirmar ${formulariosPasajeros.length}
                                    pasaje(s)`
                  }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── TAB BUSCAR / ANULAR ───────────────────────────── -->
    <div v-if="tabActivo === 'listado'" class="space-y-4">
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
            v-model="filtroBusqueda"
            type="text"
            placeholder="Buscar por código, DNI o pasajero..."
            class="form-input w-72"
            style="padding-left: 2.25rem"
          />
        </div>
        <input v-model="filtroFecha" type="date" class="form-input w-44" />
        <select v-model="filtroEstado" class="form-input w-44">
          <option value="">Todos los estados</option>
          <option value="emitido">Emitido</option>
          <option value="embarcado">Embarcado</option>
          <option value="anulado">Anulado</option>
        </select>

        <!-- Filtro por viaje -->
        <select
          v-model="filtroViaje"
          class="form-input w-64"
          @change="cargarPasajes"
        >
          <option value="">Todos los viajes</option>
          <option v-for="v in viajesDisponibles" :key="v.id" :value="v.id">
            {{ v.ruta_descripcion }} — {{ formatearFecha(v.fecha_salida) }}
          </option>
        </select>

        <button @click="cargarPasajes" class="btn-secondary">
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

      <div class="card">
        <div class="table-wrapper">
          <table class="table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Pasajero</th>
                <th>Ruta</th>
                <th class="text-center">Asiento</th>
                <th>Salida</th>
                <th>Pago</th>
                <th class="text-right">Precio</th>
                <th class="text-right">Paquetes</th>
                <th>Estado</th>
                <th class="text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="store.cargando">
                <td colspan="10">
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
              <tr v-else-if="!pasajesFiltrados.length">
                <td colspan="10" class="text-center py-12 text-gray-400 italic">
                  No se encontraron pasajes
                </td>
              </tr>
              <tr v-for="p in pasajesFiltrados" :key="p.id">
                <td>
                  <span
                    class="font-mono text-xs font-bold text-gray-700 bg-gray-100 px-2 py-1 rounded"
                  >
                    {{ p.codigo?.slice(0, 8).toUpperCase() }}
                  </span>
                </td>
                <td>
                  <p class="font-semibold text-gray-900 text-sm">
                    {{ p.pasajero_nombre }}
                  </p>
                  <p class="text-xs text-gray-400 font-mono">
                    {{ p.pasajero_dni }}
                  </p>
                </td>
                <td class="text-sm font-medium text-gray-700">
                  {{ p.ruta_descripcion }}
                </td>
                <td class="text-center">
                  <span
                    class="font-black text-blue-600 bg-blue-50 px-2 py-1 rounded-lg text-sm"
                    >{{ p.asiento }}</span
                  >
                </td>
                <td class="text-sm text-gray-600">
                  {{ formatearFechaHora(p.fecha_salida) }}
                </td>
                <td>
                  <span class="text-sm">
                    {{
                      metodosPago.find((m) => m.clave === p.metodo_pago)?.emoji
                    }}
                    {{
                      metodosPago.find((m) => m.clave === p.metodo_pago)
                        ?.etiqueta
                    }}
                  </span>
                </td>
                <td class="text-right font-black text-gray-900">
                  S/. {{ p.precio }}
                </td>
                <td class="text-right">
                  <span
                    v-if="p.tiene_paquetes"
                    class="text-xs font-bold text-orange-600 bg-orange-50 px-2 py-1 rounded-lg"
                  >
                    📦 +S/. {{ p.total_paquetes }}
                  </span>
                  <span v-else class="text-xs text-gray-300">—</span>
                </td>
                <td>
                  <span :class="claseEstadoPasaje(p.estado)">{{
                    etiquetaEstadoPasaje(p.estado)
                  }}</span>
                </td>
                <td class="text-right">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      @click="verTicket(p)"
                      title="Ver ticket"
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
                          d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"
                        />
                      </svg>
                    </button>
                    <button
                      v-if="p.pasajero_telefono"
                      @click="enviarWhatsapp(p)"
                      title="WhatsApp"
                      class="w-8 h-8 rounded-lg hover:bg-green-50 flex items-center justify-center text-gray-400 hover:text-green-600 transition-colors"
                    >
                      <svg
                        class="w-4 h-4"
                        viewBox="0 0 24 24"
                        fill="currentColor"
                      >
                        <path
                          d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"
                        />
                        <path
                          d="M12 0C5.373 0 0 5.373 0 12c0 2.124.558 4.121 1.529 5.849L.057 23.547a.75.75 0 00.921.919l5.765-1.457A11.945 11.945 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.891 0-3.667-.523-5.183-1.432l-.371-.22-3.844.972.998-3.768-.242-.389A9.96 9.96 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"
                        />
                      </svg>
                    </button>
                    <!-- Reimprimir ticket físico -->
                    <button
                      @click="reimprimirTicket(p)"
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
                    <button
                      v-if="p.estado === 'emitido'"
                      @click="abrirModalAnular(p)"
                      title="Anular"
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
                          d="M6 18L18 6M6 6l12 12"
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
    </div>

    <!-- ── TAB MANIFIESTO ───────────────────────────────── -->
    <div v-if="tabActivo === 'manifiesto'">
      <ManifiestoPasajeros />
    </div>

    <!-- ── MODALES ───────────────────────────────────────── -->
    <AppModal v-model="modalTickets" titulo="Tickets generados" ancho="sm">
      <div class="space-y-3">
        <p class="text-sm text-gray-500">
          Se generaron {{ ticketsGenerados.length }} ticket(s) correctamente.
        </p>
        <div
          v-for="t in ticketsGenerados"
          :key="t.codigo"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-100"
        >
          <div>
            <p class="font-bold text-gray-900 text-sm">
              {{ t.pasajero_nombre }}
            </p>
            <p class="text-xs text-gray-500">
              Asiento {{ t.asiento }} ·
              {{ t.codigo?.slice(0, 8).toUpperCase() }}
            </p>
          </div>
          <button @click="verTicket(t)" class="btn-secondary text-xs py-1 px-3">
            Ver ticket
          </button>
        </div>
      </div>
      <template #footer
        ><button @click="modalTickets = false" class="btn-primary">
          Cerrar
        </button></template
      >
    </AppModal>

    <TicketPasaje v-model="modalTicket" :ticket="ticketActual" />

    <AppModal v-model="modalAnular" titulo="Anular pasaje" ancho="sm">
      <div class="space-y-4">
        <div
          class="flex items-start gap-3 p-3 rounded-xl bg-red-50 border border-red-200"
        >
          <svg
            class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5"
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
          <div>
            <p class="text-sm font-bold text-red-700">¿Anular este pasaje?</p>
            <p class="text-xs text-red-600 mt-0.5">
              Pasajero: <strong>{{ pasajeAnular?.pasajero_nombre }}</strong> —
              Asiento: <strong>{{ pasajeAnular?.asiento }}</strong>
            </p>
          </div>
        </div>
        <div>
          <label class="form-label"
            >Motivo de anulación <span class="text-red-500">*</span></label
          >
          <textarea
            v-model="motivoAnulacion"
            rows="3"
            class="form-input resize-none"
            :class="{ 'form-input-error': !motivoAnulacion && intentoAnular }"
            placeholder="Describe el motivo de la anulación..."
          />
          <p v-if="!motivoAnulacion && intentoAnular" class="form-error">
            El motivo es obligatorio
          </p>
        </div>
      </div>
      <template #footer>
        <button @click="modalAnular = false" class="btn-secondary">
          Cancelar
        </button>
        <button @click="anularPasaje" :disabled="guardando" class="btn-danger">
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
          {{ guardando ? "Anulando..." : "Confirmar anulación" }}
        </button>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue";
import { usePasajesStore } from "../stores/pasajes.store";
import { pasajesService } from "../services/pasajes.service";
import AppModal from "@/components/common/AppModal.vue";
import TicketPasaje from "../components/TicketPasaje.vue";
import MapaAsientosCombi from "../components/MapaAsientosCombi.vue";
import ManifiestoPasajeros from "../components/ManifiestoPasajeros.vue";
import { printerService } from "@/services/printer.service";

const store = usePasajesStore();

const tabActivo = ref("venta");
const tabs = [
  { clave: "venta", etiqueta: "Venta de Pasajes" },
  { clave: "listado", etiqueta: "Buscar / Anular" },
  { clave: "manifiesto", etiqueta: "Manifiesto" },
];

const paso = ref(1);
const busquedaRealizada = ref(false);
const viajeSeleccionado = ref(null);
const cargandoAsientos = ref(false);
const asientos = ref([]);
const errorSeleccion = ref("");
const asientosSeleccionados = ref([]);
const formulariosPasajeros = ref([]);
const metodoPago = ref("cash");
const errorVenta = ref("");
const guardando = ref(false);

const busqueda = reactive({
  origen: "",
  destino: "",
  fecha: new Date().toISOString().slice(0, 10),
});
const ciudades = ref([]);

const filtroBusqueda = ref("");
const filtroFecha = ref("");
watch(filtroFecha, (fecha) => {
  filtroViaje.value = ""; // limpiar viaje seleccionado
  cargarViajesDisponibles(fecha);
});

const filtroEstado = ref("");

const modalTicket = ref(false);
const modalTickets = ref(false);
const modalAnular = ref(false);
const ticketActual = ref(null);
const ticketsGenerados = ref([]);
const pasajeAnular = ref(null);
const motivoAnulacion = ref("");
const intentoAnular = ref(false);

const filtroViaje = ref("");
const viajesDisponibles = ref([]);

const metodosPago = [
  { clave: "cash", etiqueta: "Efectivo", emoji: "💵" },
  { clave: "yape", etiqueta: "Yape", emoji: "📱" },
  { clave: "plin", etiqueta: "Plin", emoji: "📲" },
  { clave: "card", etiqueta: "Tarjeta", emoji: "💳" },
];

// ── Computed totales ──────────────────────────────────────
// Usa el precio de cada form (editable), no el precio_base fijo
const totalPasajes = computed(() =>
  formulariosPasajeros.value.reduce(
    (sum, f) => sum + (parseFloat(f.precio) || 0),
    0,
  ),
);

const totalPaquetesGeneral = computed(() =>
  formulariosPasajeros.value.reduce(
    (sum, form) => sum + totalPaquetesForm(form),
    0,
  ),
);

const totalGeneral = computed(
  () => totalPasajes.value + totalPaquetesGeneral.value,
);

const pasajesFiltrados = computed(() =>
  store.pasajes.filter((p) => {
    const texto = filtroBusqueda.value.toLowerCase();
    const coincideTexto =
      !texto ||
      p.codigo?.toLowerCase().includes(texto) ||
      p.pasajero_dni?.includes(texto) ||
      p.pasajero_nombre?.toLowerCase().includes(texto);
    const coincideFecha =
      !filtroFecha.value || p.fecha_salida?.startsWith(filtroFecha.value);
    const coincideEstado =
      !filtroEstado.value || p.estado === filtroEstado.value;
    return coincideTexto && coincideFecha && coincideEstado;
  }),
);

const asientosOcupados = computed(() =>
  asientos.value.filter((a) => a.ocupado).map((a) => a.numero),
);
const asientosLibres = computed(
  () =>
    (viajeSeleccionado.value?.capacidad || 18) - asientosOcupados.value.length,
);

// ── Helpers paquetes ──────────────────────────────────────
function totalPaquetesForm(form) {
  return form.paquetes.reduce(
    (sum, pkg) => sum + (parseFloat(pkg.precio_adicional) || 0),
    0,
  );
}

function totalBultosForm(form) {
  return form.paquetes.reduce(
    (sum, pkg) => sum + (parseInt(pkg.cantidad_bultos) || 1),
    0,
  );
}

function crearPaquete() {
  return reactive({
    descripcion: "",
    cantidad_bultos: 1,
    peso_kg: null,
    precio_adicional: 0,
    errores: { descripcion: "", cantidad_bultos: "", precio_adicional: "" },
  });
}

function agregarPaquete(idx) {
  formulariosPasajeros.value[idx].paquetes.push(crearPaquete());
}
function quitarPaquete(idx, pidx) {
  formulariosPasajeros.value[idx].paquetes.splice(pidx, 1);
}

// ── Helpers generales ─────────────────────────────────────
function formatearFecha(fecha) {
  if (!fecha) return "";
  return new Date(fecha).toLocaleDateString("es-PE", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

function ocupacion(viaje) {
  const total =
    (viaje.asientos_ocupados || 0) + (viaje.asientos_disponibles || 0);
  return total > 0 ? Math.round((viaje.asientos_ocupados / total) * 100) : 0;
}

function claseEstadoPasaje(estado) {
  return (
    {
      emitido: "badge badge-blue",
      embarcado: "badge badge-green",
      anulado: "badge badge-red",
    }[estado] || "badge badge-gray"
  );
}

function etiquetaEstadoPasaje(estado) {
  return (
    { emitido: "Emitido", embarcado: "Embarcado", anulado: "Anulado" }[
      estado
    ] || estado
  );
}

// ── Formulario pasajero ───────────────────────────────────
function crearFormulario(asiento) {
  return reactive({
    asiento,
    // precio editable, por defecto = precio_base del viaje
    precio: viajeSeleccionado.value?.precio_base || 0,
    dni: "",
    nombres: "",
    apellidos: "",
    telefono: "",
    pasajero_id: null,
    buscando: false,
    buscado: false,
    pasajeroEncontrado: false,
    errores: { dni: "", nombres: "", apellidos: "", precio: "" },
    paquetes: [],
  });
}

// ── Buscar pasajero por DNI ───────────────────────────────
async function buscarPorDni(idx) {
  const form = formulariosPasajeros.value[idx];
  if (!form.dni || form.dni.length !== 8) {
    form.errores.dni = "Ingresa un DNI de 8 dígitos";
    return;
  }
  form.buscando = true;
  form.buscado = false;
  form.pasajeroEncontrado = false;
  form.errores.dni = "";
  try {
    const { data } = await pasajesService.buscarPasajero(form.dni);
    // ✅ El nuevo endpoint devuelve objeto directo, no array
    const p = Array.isArray(data) ? data[0] : data;
    if (p && (p.nombres || p.id)) {
      form.nombres = p.nombres;
      form.apellidos = p.apellidos;
      form.telefono = p.telefono || "";
      form.pasajero_id = p.id || null;
      form.pasajeroEncontrado = true;
    } else {
      form.nombres = "";
      form.apellidos = "";
      form.telefono = "";
      form.pasajero_id = null;
    }
  } catch {
    form.pasajero_id = null;
  } finally {
    form.buscando = false;
    form.buscado = true;
  }
}

// ── Buscar viajes ─────────────────────────────────────────
async function buscarViajes() {
  busquedaRealizada.value = true;
  errorSeleccion.value = "";
  const params = {};
  if (busqueda.origen) params["ruta__origen"] = busqueda.origen;
  if (busqueda.destino) params["ruta__destino"] = busqueda.destino;
  if (busqueda.fecha) params["fecha_salida__date"] = busqueda.fecha;
  await store.buscarViajes(params);
}

async function cargarViajesDisponibles(fecha = "") {
  try {
    const params = {};
    if (fecha) {
      params.fecha_salida__date = fecha;
    } else {
      // Sin fecha: últimos 30 días y futuros
      const hace30dias = new Date();
      hace30dias.setDate(hace30dias.getDate() - 30);
      params.fecha_salida__date__gte = hace30dias.toISOString().slice(0, 10);
    }
    const { data } = await pasajesService.buscarViajes(params);
    viajesDisponibles.value = data.results ?? data;
  } catch (e) {
    console.error("Error cargando viajes:", e);
  }
}

async function reimprimirTicket(pasaje) {
  try {
    await printerService.imprimirPasaje({
      ...pasaje,
      metodo_pago: pasaje.metodo_pago,
      paquetes: pasaje.paquetes || [],
      precio_pasaje: pasaje.precio,
      precio_paquetes:
        pasaje.paquetes
          ?.reduce((sum, pkg) => sum + parseFloat(pkg.precio_adicional || 0), 0)
          .toFixed(2) || "0.00",
      total_general: (
        parseFloat(pasaje.precio || 0) +
        (pasaje.paquetes?.reduce(
          (sum, pkg) => sum + parseFloat(pkg.precio_adicional || 0),
          0,
        ) || 0)
      ).toFixed(2),
    });
  } catch (e) {
    console.error("Error reimprimir:", e.message);
  }
}

function seleccionarViaje(viaje) {
  errorSeleccion.value = "";
  if (["cancelado", "completado"].includes(viaje.estado)) {
    errorSeleccion.value = `No se pueden vender pasajes: el viaje está ${viaje.estado}.`;
    return;
  }
  if (viaje.asientos_disponibles <= 0) {
    errorSeleccion.value = "Este viaje no tiene asientos disponibles.";
    return;
  }
  const ahora = new Date();
  const salida = new Date(viaje.fecha_salida);
  const limite = new Date(salida.getTime() + 15 * 60 * 1000);
  if (ahora > limite) {
    const min = Math.floor((ahora - salida) / 60000);
    errorSeleccion.value = `Venta cerrada: el viaje salió hace ${min} minutos (límite 15 min).`;
    return;
  }
  viajeSeleccionado.value = viaje;
  asientosSeleccionados.value = [];
  paso.value = 2;
  cargarAsientos(viaje.id);
}

async function cargarAsientos(viajeId) {
  cargandoAsientos.value = true;
  try {
    const { data } = await pasajesService.obtenerAsientos(viajeId);
    asientos.value = (data.asientos || data).map((a) => ({
      numero: a.numero,
      ocupado: a.ocupado,
    }));
  } catch {
    asientos.value = [];
  } finally {
    cargandoAsientos.value = false;
  }
}

function irAPaso3() {
  if (!asientosSeleccionados.value.length) return;
  formulariosPasajeros.value = asientosSeleccionados.value
    .slice()
    .sort((a, b) => a - b)
    .map(crearFormulario);
  paso.value = 3;
}

function formatearFechaHora(fecha) {
  if (!fecha) return "—";
  return new Date(fecha).toLocaleString("es-PE", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

// ── Validar formularios ───────────────────────────────────
function validarTodo() {
  let valido = true;
  for (const form of formulariosPasajeros.value) {
    form.errores.dni = "";
    form.errores.nombres = "";
    form.errores.apellidos = "";
    form.errores.precio = "";

    if (!form.dni || form.dni.length !== 8) {
      form.errores.dni = "DNI inválido";
      valido = false;
    }
    if (!form.nombres.trim()) {
      form.errores.nombres = "Obligatorio";
      valido = false;
    }
    if (!form.apellidos.trim()) {
      form.errores.apellidos = "Obligatorio";
      valido = false;
    }
    if (!form.precio && form.precio !== 0) {
      form.errores.precio = "Ingresa un precio";
      valido = false;
    }
    if (form.precio < 0) {
      form.errores.precio = "El precio no puede ser negativo";
      valido = false;
    }

    for (const pkg of form.paquetes) {
      pkg.errores.descripcion = "";
      pkg.errores.cantidad_bultos = "";
      pkg.errores.precio_adicional = "";
      if (!pkg.descripcion.trim()) {
        pkg.errores.descripcion = "Obligatorio";
        valido = false;
      }
      if (!pkg.cantidad_bultos || pkg.cantidad_bultos < 1) {
        pkg.errores.cantidad_bultos = "Mínimo 1";
        valido = false;
      }
      if (
        pkg.precio_adicional === "" ||
        pkg.precio_adicional === null ||
        pkg.precio_adicional < 0
      ) {
        pkg.errores.precio_adicional = "Ingresa un precio válido";
        valido = false;
      }
    }
  }
  return valido;
}

// ── Confirmar venta

// Busca o crea al pasajero y devuelve su id (crear pasajeros no mueve dinero)
async function resolverPasajeroId(form) {
  if (form.pasajero_id) return form.pasajero_id;
  try {
    const { data: nuevo } = await pasajesService.crearPasajero({
      dni: form.dni,
      nombres: form.nombres,
      apellidos: form.apellidos,
      telefono: form.telefono || "",
    });
    return nuevo.id;
  } catch (e) {
    if (e.response?.data?.dni) {
      const { data: existente } = await pasajesService.buscarPasajero(form.dni);
      const p = Array.isArray(existente) ? existente[0] : existente;
      if (p) return p.id;
    }
    throw e;
  }
}

// Texto claro cuando el lote falla: indica qué pasajero/asiento causó el error
function mensajeErrorLote(data) {
  const err = data.errores || {};
  const primero = (v) => (Array.isArray(v) ? v[0] : v);
  const detalle =
    primero(err.non_field_errors) ||
    primero(err.asiento) ||
    primero(err.precio) ||
    primero(err.detail) ||
    primero(Object.values(err)[0]) ||
    "Error al registrar el pasaje.";
  const quien =
    data.indice != null
      ? `Pasajero ${data.indice + 1} (asiento ${data.asiento}): `
      : "";
  return `${quien}${detalle} No se vendió ningún pasaje; corrige y vuelve a intentar.`;
}

async function confirmarVenta() {
  if (!validarTodo()) return;

  const ahora = new Date();
  const limite = new Date(
    new Date(viajeSeleccionado.value.fecha_salida).getTime() + 20 * 60 * 1000,
  );
  if (ahora > limite) {
    errorVenta.value =
      "El tiempo de venta ha expirado (máx. 20 min después de la salida).";
    return;
  }

  guardando.value = true;
  errorVenta.value = "";
  let resultados = [];
  try {
    // 1) Resolver pasajeros y armar el lote
    const items = [];
    for (const form of formulariosPasajeros.value) {
      items.push({
        pasajero: await resolverPasajeroId(form),
        asiento: form.asiento,
        precio: form.precio,
        paquetes: form.paquetes.map((pkg) => ({
          descripcion: pkg.descripcion,
          cantidad_bultos: pkg.cantidad_bultos,
          peso_kg: pkg.peso_kg || null,
          precio_adicional: pkg.precio_adicional,
        })),
      });
    }

    // 2) Una sola llamada: o se venden todos o no se vende ninguno
    const { data: pasajes } = await pasajesService.venderLote({
      viaje: viajeSeleccionado.value.id,
      metodo_pago: metodoPago.value,
      pasajes: items,
    });

    // 3) Armar los tickets (misma orden que los formularios)
    resultados = pasajes.map((pasaje, i) => {
      const form = formulariosPasajeros.value[i];
      return {
        ...pasaje,
        ruta_descripcion: viajeSeleccionado.value.ruta_descripcion,
        vehiculo_placa: viajeSeleccionado.value.vehiculo_placa,
        fecha_salida: viajeSeleccionado.value.fecha_salida,
        precio: form.precio,
        estado: "emitido",
        pasajero_nombre: `${form.nombres} ${form.apellidos}`.trim(),
        pasajero_dni: form.dni,
        pasajero_telefono: form.telefono || "",
        paquetes: items[i].paquetes,
        vendido_por_nombre: pasaje.vendido_por_nombre || "",
        sucursal_nombre: pasaje.sucursal_nombre || "",
      };
    });

    ticketsGenerados.value = resultados;
    if (resultados.length === 1) {
      ticketActual.value = resultados[0];
      modalTicket.value = true;
    } else {
      modalTickets.value = true;
    }

    // ✅ Imprimir ANTES de resetear
    for (const ticket of resultados) {
      try {
        await printerService.imprimirPasaje(ticket);
      } catch (e) {
        console.error("Error impresion completo:", e);
        console.error("Stack:", e.stack);
      }
    }

    resetearVenta();
  } catch (e) {
    const data = e.response?.data;
    if (data?.errores) errorVenta.value = mensajeErrorLote(data);
    else if (data?.detail) errorVenta.value = data.detail;
    else if (data?.pasajes)
      errorVenta.value = Array.isArray(data.pasajes)
        ? data.pasajes[0]
        : data.pasajes;
    else if (data?.asiento) errorVenta.value = `Asiento: ${data.asiento[0]}`;
    else if (data?.precio)
      errorVenta.value = Array.isArray(data.precio)
        ? data.precio[0]
        : data.precio;
    else if (data?.non_field_errors)
      errorVenta.value = data.non_field_errors[0];
    else if (typeof data === "string") errorVenta.value = data;
    else errorVenta.value = JSON.stringify(data);
  } finally {
    guardando.value = false;
  }
}

function resetearVenta() {
  paso.value = 1;
  viajeSeleccionado.value = null;
  asientosSeleccionados.value = [];
  formulariosPasajeros.value = [];
  asientos.value = [];
  busquedaRealizada.value = false;
  metodoPago.value = "cash";
  errorVenta.value = "";
  errorSeleccion.value = "";
}

function enviarWhatsapp(pasaje) {
  const raw = (pasaje.pasajero_telefono || "").replace(/[\s\-\(\)\+]/g, "");
  const numero = raw.startsWith("51") ? raw : `51${raw}`;
  const mp =
    metodosPago.find((m) => m.clave === pasaje.metodo_pago)?.etiqueta ||
    pasaje.metodo_pago;
  const est =
    { emitido: "✅ EMITIDO", embarcado: "🚌 EMBARCADO", anulado: "❌ ANULADO" }[
      pasaje.estado
    ] || pasaje.estado;

  let seccionPaquetes = "";
  const pkgs = pasaje.paquetes || [];
  if (pkgs.length) {
    const lineas = pkgs
      .map((pkg, i) => {
        const peso = pkg.peso_kg ? ` · ${pkg.peso_kg} kg` : "";
        return `   ${i + 1}. ${pkg.descripcion} (${pkg.cantidad_bultos} bulto(s)${peso}) — S/. ${pkg.precio_adicional}`;
      })
      .join("\n");
    const totalPkgs = pkgs.reduce(
      (s, p) => s + parseFloat(p.precio_adicional || 0),
      0,
    );
    seccionPaquetes = `\n\n *PAQUETES*\n${lineas}\n   *Total paquetes: S/. ${totalPkgs.toFixed(2)}*`;
  }

  const totalMsg =
    parseFloat(pasaje.precio || 0) +
    pkgs.reduce((s, p) => s + parseFloat(p.precio_adicional || 0), 0);
  const totalLinea = pkgs.length
    ? `Pasaje: S/. ${pasaje.precio}\n Total general: *S/. ${totalMsg.toFixed(2)}*`
    : `Pasaje: *S/. ${pasaje.precio}*`;

  const msg = [
    `*TICKET DE PASAJE - TURISMO WJL*`,
    `━━━━━━━━━━━━━━━━━━━━━━`,
    `Código: *${pasaje.codigo?.slice(0, 8).toUpperCase()}*`,
    ``,
    `*PASAJERO*`,
    `Nombre: ${pasaje.pasajero_nombre}`,
    `DNI: ${pasaje.pasajero_dni}`,
    ``,
    `*VIAJE*`,
    `Ruta: ${pasaje.ruta_descripcion}`,
    `Salida: ${formatearFechaHora(pasaje.fecha_salida)}`,
    `Vehículo: ${pasaje.vehiculo_placa}`,
    ``,
    `Asiento: *${pasaje.asiento}*`,
    `Pago: ${mp}`,
    totalLinea,
    seccionPaquetes,
    ``,
    `Estado: ${est}`,
    `━━━━━━━━━━━━━━━━━━━━━━`,
    `✦ Gracias por viajar con WJL Transportes ✦`,
    `📍 Las 5 Esquinas - Huarmaca / Chiclayo`,
    `📞 +51 999 713 436`,
  ].join("\n");

  window.open(
    `https://wa.me/${numero}?text=${encodeURIComponent(msg)}`,
    "_blank",
  );
}

function verTicket(p) {
  ticketActual.value = p;
  modalTicket.value = true;
}
function abrirModalAnular(p) {
  pasajeAnular.value = p;
  motivoAnulacion.value = "";
  intentoAnular.value = false;
  modalAnular.value = true;
}

async function anularPasaje() {
  intentoAnular.value = true;
  if (!motivoAnulacion.value.trim()) return;
  guardando.value = true;
  try {
    await pasajesService.anularPasaje(pasajeAnular.value.id, {
      motivo: motivoAnulacion.value,
    });
    modalAnular.value = false;
    cargarPasajes();
  } catch {
  } finally {
    guardando.value = false;
  }
}

async function cargarPasajes() {
  const params = {};
  if (filtroBusqueda.value) params.search = filtroBusqueda.value;
  if (filtroEstado.value) params.estado = filtroEstado.value;
  if (filtroViaje.value) params.viaje = filtroViaje.value; // ← agregar
  await store.cargarPasajes(params);
}

async function cargarCiudades() {
  try {
    const api = (await import("@/services/api")).default;
    const { data } = await api.get("/ubicaciones/ciudades/");
    ciudades.value = data.results ?? data;
  } catch {}
}

onMounted(() => {
  cargarCiudades();
  cargarPasajes();
  cargarViajesDisponibles();
  busqueda.fecha = new Date().toISOString().slice(0, 10);
});
</script>
