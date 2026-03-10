<template>
    <div class="space-y-5">

        <!-- Encabezado -->
        <div class="page-header">
            <div>
                <h1 class="page-title">Caja</h1>
                <p class="page-subtitle">Control de apertura, movimientos y cierre</p>
            </div>
            <div v-if="store.cajaAbierta"
                class="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-50 border border-emerald-200">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span class="text-sm font-bold text-emerald-700">
                    Caja abierta desde {{ formatearHora(store.sesionActiva?.fecha_apertura) }}
                </span>
            </div>
            <div v-else class="flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-50 border border-amber-200">
                <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                <span class="text-sm font-bold text-amber-700">Caja cerrada</span>
            </div>
        </div>

        <!-- Tabs -->
        <div class="flex gap-1 p-1 bg-gray-100 rounded-xl w-fit">
            <button v-for="tab in tabsVisibles" :key="tab.clave" @click="tabActivo = tab.clave" :class="[
                'px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-150',
                tabActivo === tab.clave
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-500 hover:text-gray-700'
            ]">
                {{ tab.etiqueta }}
            </button>
        </div>

        <!-- TAB APERTURA -->
        <div v-if="tabActivo === 'apertura'">
            <div v-if="store.cajaAbierta" class="max-w-lg">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Sesión activa</h3>
                        <span class="badge badge-green">Abierta</span>
                    </div>
                    <div class="card-body space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-gray-50 rounded-xl p-4">
                                <p class="text-xs text-gray-500 font-medium mb-1">Apertura</p>
                                <p class="text-sm font-bold text-gray-900">{{
                                    formatearFechaHora(store.sesionActiva?.fecha_apertura) }}</p>
                            </div>
                            <div class="bg-orange-50 rounded-xl p-4">
                                <p class="text-xs text-gray-500 font-medium mb-1">Monto inicial</p>
                                <p class="text-lg font-black text-orange-600">S/. {{
                                    formatearMonto(store.sesionActiva?.monto_inicial) }}</p>
                            </div>
                        </div>
                        <div class="grid grid-cols-3 gap-3">
                            <div class="bg-emerald-50 rounded-xl p-3 text-center">
                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Ingresos</p>
                                <p class="text-sm font-black text-emerald-600">S/. {{
                                    formatearMonto(store.resumen.ingresos - store.resumen.anulaciones) }}</p>

                            </div>
                            <div class="bg-red-50 rounded-xl p-3 text-center">
                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Egresos</p>
                                <p class="text-sm font-black text-red-600">S/. {{ formatearMonto(store.resumen.egresos)
                                    }}</p>
                            </div>
                            <div class="bg-blue-50 rounded-xl p-3 text-center">
                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Saldo</p>
                                <p class="text-sm font-black text-blue-600">S/. {{ formatearMonto(store.saldoEsperado)
                                    }}</p>
                            </div>
                        </div>
                        <button @click="tabActivo = 'arqueo'" class="btn-secondary w-full justify-center">
                            Ver arqueo y cerrar caja →
                        </button>
                    </div>
                </div>
            </div>
            <div v-else class="max-w-md">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Abrir caja</h3>
                    </div>
                    <div class="card-body space-y-4">
                        <div class="flex items-start gap-3 p-3 rounded-xl bg-blue-50 border border-blue-100">
                            <svg class="w-4 h-4 text-blue-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p class="text-xs text-blue-700 font-medium leading-relaxed">
                                Ingresa el monto en efectivo con el que inicias la jornada. Este monto será el punto de
                                partida para el arqueo al cierre.
                            </p>
                        </div>
                        <div>
                            <label class="form-label">Monto inicial (S/.) <span class="text-red-500">*</span></label>
                            <input v-model="formApertura.monto_inicial" type="number" step="0.50" min="0"
                                class="form-input text-lg font-bold"
                                :class="{ 'form-input-error': erroresApertura.monto_inicial }" placeholder="0.00" />
                            <p v-if="erroresApertura.monto_inicial" class="form-error">{{ erroresApertura.monto_inicial
                                }}</p>
                        </div>
                        <div>
                            <label class="form-label">Observación</label>
                            <textarea v-model="formApertura.observacion" rows="2" class="form-input resize-none"
                                placeholder="Notas de apertura (opcional)..." />
                        </div>
                        <div v-if="errorApertura"
                            class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                            <svg class="w-4 h-4 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <p class="text-xs text-red-700 font-medium">{{ errorApertura }}</p>
                        </div>
                        <button @click="abrirCaja" :disabled="guardando" class="btn-primary w-full justify-center py-3">
                            <svg v-if="guardando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4" />
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                            </svg>
                            <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                            </svg>
                            {{ guardando ? 'Abriendo...' : 'Abrir caja ahora' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB MOVIMIENTOS -->
        <div v-if="tabActivo === 'movimientos'" class="space-y-4">
            <div v-if="!store.cajaAbierta"
                class="flex items-center gap-3 p-4 rounded-xl bg-amber-50 border border-amber-200">
                <svg class="w-5 h-5 text-amber-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <p class="text-sm font-medium text-amber-800">
                    Debes <button @click="tabActivo = 'apertura'" class="underline font-bold">abrir la caja</button>
                    para registrar movimientos.
                </p>
            </div>
            <div v-if="store.cajaAbierta" class="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm">
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-wide mb-1">Monto inicial</p>
                    <p class="text-xl font-black text-gray-900">S/. {{ formatearMonto(store.sesionActiva?.monto_inicial)
                        }}</p>
                </div>
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm">
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-wide mb-1">Ingresos</p>
                    <p class="text-xl font-black text-emerald-600">S/. {{ formatearMonto(store.resumen.ingresos -
                        store.resumen.anulaciones) }}</p>

                </div>
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm">
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-wide mb-1">Egresos</p>
                    <p class="text-xl font-black text-red-600">S/. {{ formatearMonto(store.resumen.egresos) }}</p>
                </div>
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm">
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-wide mb-1">Saldo esperado</p>
                    <p class="text-xl font-black text-blue-600">S/. {{ formatearMonto(store.saldoEsperado) }}</p>
                </div>
            </div>
            <div v-if="store.cajaAbierta" class="flex justify-end">
                <button @click="modalEgreso = true" class="btn-secondary">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    Registrar gasto / egreso
                </button>
            </div>
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Movimientos del día</h3>
                    <button @click="store.cargarMovimientos()" class="btn-ghost text-xs">
                        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Actualizar
                    </button>
                </div>
                <div class="table-wrapper">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Hora</th>
                                <th>Tipo</th>
                                <th>Descripción</th>
                                <th>Referencia</th>
                                <th class="text-right">Monto</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="store.cargando">
                                <td colspan="5">
                                    <div class="flex justify-center py-8"><svg
                                            class="w-6 h-6 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                stroke-width="4" />
                                            <path class="opacity-75" fill="currentColor"
                                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                        </svg></div>
                                </td>
                            </tr>
                            <tr v-else-if="!store.movimientos.length">
                                <td colspan="5" class="text-center py-12 text-gray-400 italic">No hay movimientos
                                    registrados</td>
                            </tr>
                            <tr v-for="m in store.movimientos" :key="m.id">
                                <td class="font-mono text-xs text-gray-500">{{ formatearHora(m.creado_en) }}</td>
                                <td><span :class="claseTipo(m.tipo)">{{ etiquetaTipo(m.tipo) }}</span></td>
                                <td class="text-gray-700 text-sm max-w-[200px] truncate">{{ m.descripcion || '—' }}</td>
                                <td class="text-xs text-gray-400 font-mono">{{ m.referencia_pasaje ||
                                    m.referencia_encomienda || '—' }}</td>
                                <td class="text-right">
                                    <span
                                        :class="['font-black text-sm', esIngreso(m.tipo) ? 'text-emerald-600' : 'text-red-600']">
                                        {{ esIngreso(m.tipo) ? '+' : '-' }} S/. {{ formatearMonto(m.monto) }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB ARQUEO / CIERRE -->
        <div v-if="tabActivo === 'arqueo'" class="space-y-5">
            <div v-if="!store.cajaAbierta">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Historial de sesiones</h3>
                    </div>
                    <div class="table-wrapper">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Fecha</th>
                                    <th>Cajero</th>
                                    <th class="text-right">Inicial</th>
                                    <th class="text-right">Final</th>
                                    <th>Estado</th>
                                    <th>Duración</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="store.cargando">
                                    <td colspan="6">
                                        <div class="flex justify-center py-8"><svg
                                                class="w-6 h-6 text-gray-300 animate-spin" fill="none"
                                                viewBox="0 0 24 24">
                                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                    stroke-width="4" />
                                                <path class="opacity-75" fill="currentColor"
                                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                            </svg></div>
                                    </td>
                                </tr>
                                <tr v-else-if="!store.sesiones.length">
                                    <td colspan="6" class="text-center py-12 text-gray-400 italic">No hay sesiones
                                        anteriores</td>
                                </tr>
                                <tr v-for="s in store.sesiones" :key="s.id">
                                    <td class="text-sm text-gray-700">{{ formatearFecha(s.fecha_apertura) }}</td>
                                    <td class="text-sm font-medium text-gray-900">{{ s.cajero_nombre }}</td>
                                    <td class="text-right font-bold text-gray-900">S/. {{
                                        formatearMonto(s.monto_inicial) }}</td>
                                    <td class="text-right font-bold text-gray-900">{{ s.monto_final ? 'S/. ' +
                                        formatearMonto(s.monto_final) : '—' }}</td>
                                    <td><span
                                            :class="s.estado === 'abierta' ? 'badge badge-green' : 'badge badge-gray'">{{
                                                s.estado === 'abierta' ? 'Abierta' : 'Cerrada' }}</span></td>
                                    <td class="text-sm text-gray-500">{{ calcularDuracion(s.fecha_apertura,
                                        s.fecha_cierre) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-5">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Arqueo en tiempo real</h3>
                        <span class="text-xs text-gray-400 font-medium">Sesión del {{
                            formatearFecha(store.sesionActiva?.fecha_apertura) }}</span>
                    </div>
                    <div class="card-body space-y-3">
                        <div class="flex justify-between items-center py-2 border-b border-gray-50">
                            <span class="text-sm text-gray-600 font-medium">Monto inicial</span>
                            <span class="font-bold text-gray-900">S/. {{
                                formatearMonto(store.sesionActiva?.monto_inicial) }}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-gray-50">
                            <span class="text-sm text-emerald-600 font-medium">+ Ingresos (ventas)</span>
                            <p class="text-sm font-black text-emerald-600">S/. {{ formatearMonto(store.resumen.ingresos
                                - store.resumen.anulaciones) }}</p>

                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-gray-50">
                            <span class="text-sm text-red-500 font-medium">- Egresos (gastos)</span>
                            <span class="font-bold text-red-500">S/. {{ formatearMonto(store.resumen.egresos) }}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-gray-50">
                            <span class="text-sm text-orange-500 font-medium">- Anulaciones</span>
                            <span class="font-bold text-orange-500">S/. {{ formatearMonto(store.resumen.anulaciones)
                                }}</span>
                        </div>
                        <div class="flex justify-between items-center py-3 bg-blue-50 rounded-xl px-3 mt-2">
                            <span class="text-sm font-bold text-blue-700">Saldo esperado en caja</span>
                            <span class="text-xl font-black text-blue-700">S/. {{ formatearMonto(store.saldoEsperado)
                                }}</span>
                        </div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Cerrar caja</h3>
                    </div>
                    <div class="card-body space-y-4">
                        <div class="flex items-start gap-3 p-3 rounded-xl bg-amber-50 border border-amber-100">
                            <svg class="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            <p class="text-xs text-amber-700 font-medium leading-relaxed">Ingresa el monto físico
                                contado en caja. Se calculará la diferencia con el saldo esperado del sistema.</p>
                        </div>
                        <div>
                            <label class="form-label">Monto contado en físico (S/.) <span
                                    class="text-red-500">*</span></label>
                            <input v-model="formCierre.monto_final" type="number" step="0.50" min="0"
                                class="form-input text-lg font-bold"
                                :class="{ 'form-input-error': erroresCierre.monto_final }" placeholder="0.00"
                                @input="calcularDiferencia" />
                            <p v-if="erroresCierre.monto_final" class="form-error">{{ erroresCierre.monto_final }}</p>
                        </div>
                        <div v-if="formCierre.monto_final !== ''" :class="['flex justify-between items-center p-3 rounded-xl border',
                            diferencia === 0 ? 'bg-emerald-50 border-emerald-200' :
                                diferencia > 0 ? 'bg-blue-50 border-blue-200' : 'bg-red-50 border-red-200']">
                            <span class="text-sm font-bold"
                                :class="diferencia >= 0 ? 'text-gray-700' : 'text-red-700'">{{ diferencia >= 0 ?
                                    'Sobrante' : 'Faltante' }}</span>
                            <span class="font-black text-lg"
                                :class="diferencia > 0 ? 'text-blue-600' : diferencia < 0 ? 'text-red-600' : 'text-emerald-600'">
                                {{ diferencia >= 0 ? '+' : '' }} S/. {{ formatearMonto(Math.abs(diferencia)) }}
                            </span>
                        </div>
                        <div>
                            <label class="form-label">Observación de cierre</label>
                            <textarea v-model="formCierre.observacion" rows="2" class="form-input resize-none"
                                placeholder="Notas del cierre (opcional)..." />
                        </div>
                        <div v-if="errorCierre"
                            class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                            <p class="text-xs text-red-700 font-medium">{{ errorCierre }}</p>
                        </div>
                        <button @click="modalConfirmarCierre = true" :disabled="guardando || !formCierre.monto_final"
                            class="btn-danger w-full justify-center py-3">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                            Cerrar caja
                        </button>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Historial de sesiones</h3>
                </div>
                <div class="table-wrapper">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Fecha apertura</th>
                                <th>Cajero</th>
                                <th class="text-right">Inicial</th>
                                <th class="text-right">Final</th>
                                <th class="text-right">Diferencia</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="store.cargando">
                                <td colspan="6">
                                    <div class="flex justify-center py-8"><svg
                                            class="w-6 h-6 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                                stroke-width="4" />
                                            <path class="opacity-75" fill="currentColor"
                                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                        </svg></div>
                                </td>
                            </tr>
                            <tr v-else-if="!store.sesiones.length">
                                <td colspan="6" class="text-center py-10 text-gray-400 italic">No hay sesiones
                                    registradas</td>
                            </tr>
                            <tr v-for="s in store.sesiones" :key="s.id">
                                <td class="text-sm text-gray-700">{{ formatearFechaHora(s.fecha_apertura) }}</td>
                                <td class="text-sm font-medium text-gray-900">{{ s.cajero_nombre }}</td>
                                <td class="text-right font-bold text-gray-900">S/. {{ formatearMonto(s.monto_inicial) }}
                                </td>
                                <td class="text-right font-bold text-gray-900">{{ s.monto_final ? 'S/. ' +
                                    formatearMonto(s.monto_final) : '—' }}</td>
                                <td class="text-right">
                                    <span v-if="s.monto_final"
                                        :class="['font-bold text-sm', diferenciaHistorial(s) > 0 ? 'text-blue-600' : diferenciaHistorial(s) < 0 ? 'text-red-600' : 'text-emerald-600']">
                                        {{ diferenciaHistorial(s) >= 0 ? '+' : '' }} S/. {{
                                            formatearMonto(Math.abs(diferenciaHistorial(s))) }}
                                    </span>
                                    <span v-else class="text-gray-400">—</span>
                                </td>
                                <td><span :class="s.estado === 'abierta' ? 'badge badge-green' : 'badge badge-gray'">{{
                                    s.estado === 'abierta' ? 'Abierta' : 'Cerrada' }}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB CONSOLIDADO (solo admin) -->
        <div v-if="tabActivo === 'consolidado'" class="space-y-5">
            <div class="card">
                <div class="card-body">
                    <div class="flex flex-wrap items-end gap-3 min-w-0">
                        <div>
                            <label class="form-label">Desde</label>
                            <input v-model="filtroConsolidado.fecha_desde" type="date" class="form-input w-44" />
                        </div>
                        <div>
                            <label class="form-label">Hasta</label>
                            <input v-model="filtroConsolidado.fecha_hasta" type="date" class="form-input w-44" />
                        </div>
                        <button @click="cargarConsolidado" :disabled="cargandoConsolidado" class="btn-primary">
                            <svg :class="['w-4 h-4', cargandoConsolidado ? 'animate-spin' : '']" fill="none"
                                viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                            Actualizar
                        </button>
                        <button @click="limpiarFiltros" class="btn-ghost text-sm">Limpiar filtros</button>
                    </div>
                </div>
            </div>

            <div v-if="consolidado" class="grid grid-cols-2 lg:grid-cols-5 gap-4">
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm text-center">
                    <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Total Ingresos</p>
                    <p class="text-xl font-black text-emerald-600">{{ formatearMonto(consolidado.total_global.ingresos - consolidado.total_global.egresos -
                            consolidado.total_global.anulaciones) }}</p>

                </div>
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm text-center">
                    <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Total Egresos</p>
                    <p class="text-xl font-black text-red-600">S/. {{ formatearMonto(consolidado.total_global.egresos)
                        }}</p>
                </div>
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm text-center">
                    <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Anulaciones</p>
                    <p class="text-xl font-black text-orange-500">S/. {{
                        formatearMonto(consolidado.total_global.anulaciones) }}</p>
                </div>
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm text-center">
                    <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Cajas Abiertas</p>
                    <p class="text-xl font-black text-blue-600">{{ consolidado.total_global.cajas_abiertas }}</p>
                </div>
                <div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm text-center">
                    <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Saldo Neto Total</p>
                    <p class="text-xl font-black text-gray-900">
                        S/. {{ formatearMonto(consolidado.total_global.ingresos - consolidado.total_global.egresos -
                            consolidado.total_global.anulaciones) }}
                    </p>
                </div>
            </div>

            <div v-if="consolidado" class="grid grid-cols-1 lg:grid-cols-2 gap-5">
                <div v-for="sede in consolidado.sedes" :key="sede.sucursal_id" class="card">
                    <div class="card-header">
                        <div class="flex items-center gap-2">
                            <div class="w-8 h-8 rounded-xl bg-blue-100 flex items-center justify-center">
                                <svg class="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-2 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                </svg>
                            </div>
                            <h3 class="card-title">{{ sede.sucursal_nombre }}</h3>
                        </div>
                        <span v-if="sede.cajas_abiertas > 0"
                            class="inline-flex items-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-1 rounded-lg">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                            {{ sede.cajas_abiertas }} abierta(s)
                        </span>
                        <span v-else
                            class="text-xs font-bold text-gray-400 bg-gray-50 border border-gray-200 px-2 py-1 rounded-lg">Sin
                            caja activa</span>
                    </div>
                    <div class="card-body space-y-3">
                        <div class="grid grid-cols-3 gap-3">
                            <div class="bg-emerald-50 rounded-xl p-3 text-center">
                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Ingresos</p>
                                <p class="text-sm font-black text-emerald-600">S/. {{ formatearMonto(sede.ingresos -
                                    sede.anulaciones) }}</p>
                            </div>
                            <div class="bg-red-50 rounded-xl p-3 text-center">
                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Egresos</p>
                                <p class="text-sm font-black text-red-600">S/. {{ formatearMonto(sede.egresos) }}</p>
                            </div>
                            <div class="bg-blue-50 rounded-xl p-3 text-center">
                                <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide mb-1">Saldo neto
                                </p>
                                <p class="text-sm font-black text-blue-600">S/. {{ formatearMonto(sede.saldo_neto) }}
                                </p>
                            </div>
                        </div>
                        <div>
                            <div class="flex justify-between text-xs text-gray-500 mb-1">
                                <span class="font-medium">Participación en ingresos totales</span>
                                <span class="font-bold">{{ porcentajeSede(sede) }}%</span>
                            </div>
                            <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                                <div class="h-full bg-blue-500 rounded-full transition-all duration-500"
                                    :style="{ width: porcentajeSede(sede) + '%' }"></div>
                            </div>
                        </div>
                        <div v-if="sede.sesiones_activas.length" class="border-t border-gray-100 pt-3">
                            <p class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Cajeros activos
                                ahora</p>
                            <div v-for="sa in sede.sesiones_activas" :key="sa.id"
                                class="flex items-center justify-between py-1.5 text-sm">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                    <span class="font-medium text-gray-700">{{ sa.cajero }}</span>
                                </div>
                                <div class="text-right">
                                    <span class="text-xs text-gray-400">desde {{ formatearHora(sa.fecha_apertura)
                                        }}</span>
                                    <span class="ml-2 text-xs font-bold text-gray-600">S/. {{
                                        formatearMonto(sa.monto_inicial) }}</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex items-center gap-3 pt-1 border-t border-gray-50 text-xs text-gray-500">
                            <span>{{ sede.total_sesiones }} sesión(es)</span>
                            <span>·</span>
                            <span class="text-emerald-600 font-bold">{{ sede.cajas_abiertas }} abiertas</span>
                            <span>·</span>
                            <span>{{ sede.cajas_cerradas }} cerradas</span>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="!cargandoConsolidado && !consolidado" class="text-center py-16 text-gray-400">
                <svg class="w-12 h-12 mx-auto mb-3 text-gray-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <p class="font-medium">Sin datos aún</p>
                <p class="text-sm mt-1">Presiona "Actualizar" para cargar el consolidado</p>
            </div>
            <div v-if="cargandoConsolidado" class="flex justify-center py-16">
                <svg class="w-8 h-8 text-gray-300 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
            </div>
        </div>

        <!-- MODAL REGISTRAR EGRESO -->
        <AppModal v-model="modalEgreso" titulo="Registrar Gasto / Egreso" ancho="sm">
            <form @submit.prevent="registrarEgreso" class="space-y-4">
                <div>
                    <label class="form-label">Monto (S/.) <span class="text-red-500">*</span></label>
                    <input v-model="formEgreso.monto" type="number" step="0.50" min="0.01"
                        class="form-input text-lg font-bold" :class="{ 'form-input-error': erroresEgreso.monto }"
                        placeholder="0.00" />
                    <p v-if="erroresEgreso.monto" class="form-error">{{ erroresEgreso.monto }}</p>
                </div>
                <div>
                    <label class="form-label">Descripción <span class="text-red-500">*</span></label>
                    <input v-model="formEgreso.descripcion" type="text" class="form-input"
                        :class="{ 'form-input-error': erroresEgreso.descripcion }"
                        placeholder="Ej: Compra de útiles, pasajes, etc." />
                    <p v-if="erroresEgreso.descripcion" class="form-error">{{ erroresEgreso.descripcion }}</p>
                </div>
                <div v-if="erroresEgreso.servidor"
                    class="flex items-center gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
                    <p class="text-xs text-red-700 font-medium">{{ erroresEgreso.servidor }}</p>
                </div>
            </form>
            <template #footer>
                <button @click="modalEgreso = false" class="btn-secondary">Cancelar</button>
                <button @click="registrarEgreso" :disabled="guardando" class="btn-danger">
                    <svg v-if="guardando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    {{ guardando ? 'Registrando...' : 'Registrar egreso' }}
                </button>
            </template>
        </AppModal>

        <!-- MODAL CONFIRMAR CIERRE -->
        <AppModal v-model="modalConfirmarCierre" titulo="Confirmar cierre de caja" ancho="sm">
            <div class="text-center py-2 space-y-3">
                <div class="w-14 h-14 rounded-2xl bg-red-50 flex items-center justify-center mx-auto">
                    <svg class="w-7 h-7 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                </div>
                <div>
                    <p class="text-sm font-bold text-gray-900 mb-1">¿Cerrar la caja?</p>
                    <p class="text-xs text-gray-500">Esta acción no se puede deshacer.</p>
                </div>
                <div class="bg-gray-50 rounded-xl p-4 text-left space-y-2">
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Saldo esperado</span>
                        <span class="font-bold">S/. {{ formatearMonto(store.saldoEsperado) }}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500">Monto contado</span>
                        <span class="font-bold">S/. {{ formatearMonto(formCierre.monto_final) }}</span>
                    </div>
                    <div class="flex justify-between text-sm border-t border-gray-200 pt-2">
                        <span class="font-bold" :class="diferencia >= 0 ? 'text-blue-600' : 'text-red-600'">{{
                            diferencia >= 0 ?
                                'Sobrante' : 'Faltante' }}</span>
                        <span class="font-black" :class="diferencia >= 0 ? 'text-blue-600' : 'text-red-600'">
                            {{ diferencia >= 0 ? '+' : '' }} S/. {{ formatearMonto(Math.abs(diferencia)) }}
                        </span>
                    </div>
                </div>
            </div>
            <template #footer>
                <button @click="modalConfirmarCierre = false" class="btn-secondary">Cancelar</button>
                <button @click="cerrarCaja" :disabled="guardando" class="btn-danger">{{ guardando ? 'Cerrando...' :
                    'Confirmar cierre' }}</button>
            </template>
        </AppModal>

    </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCajaStore } from '../stores/caja.store'
import { cajaService } from '../services/caja.service'
import AppModal from '@/components/common/AppModal.vue'

const store = useCajaStore()
const route = useRoute()

// Usuario y permisos
const usuarioActual = JSON.parse(localStorage.getItem('usuario') || 'null')
const esAdmin = computed(() => usuarioActual?.rol === 'administrador' || usuarioActual?.is_staff)

// Tabs
const tabActivo = ref(
    route.path.includes('movimientos') ? 'movimientos' :
        route.path.includes('arqueo') ? 'arqueo' : 'apertura'
)

const todosLosTabs = [
    { clave: 'apertura', etiqueta: 'Apertura' },
    { clave: 'movimientos', etiqueta: 'Movimientos' },
    { clave: 'arqueo', etiqueta: 'Arqueo / Cierre' },
    { clave: 'consolidado', etiqueta: '📊 Consolidado', soloAdmin: true },
]
const tabsVisibles = computed(() => todosLosTabs.filter(t => !t.soloAdmin || esAdmin.value))

const guardando = ref(false)
const modalEgreso = ref(false)
const modalConfirmarCierre = ref(false)
const errorApertura = ref('')
const errorCierre = ref('')

const formApertura = reactive({ monto_inicial: '', observacion: '' })
const erroresApertura = reactive({ monto_inicial: '' })
const formCierre = reactive({ monto_final: '', observacion: '' })
const erroresCierre = reactive({ monto_final: '' })
const formEgreso = reactive({ monto: '', descripcion: '' })
const erroresEgreso = reactive({ monto: '', descripcion: '', servidor: '' })

// Consolidado
const consolidado = ref(null)
const cargandoConsolidado = ref(false)
const filtroConsolidado = reactive({
    fecha_desde: new Date().toISOString().slice(0, 10),
    fecha_hasta: new Date().toISOString().slice(0, 10),
})

async function cargarConsolidado() {
    cargandoConsolidado.value = true
    try {
        const params = {}
        if (filtroConsolidado.fecha_desde) params.fecha_desde = filtroConsolidado.fecha_desde
        if (filtroConsolidado.fecha_hasta) params.fecha_hasta = filtroConsolidado.fecha_hasta
        const { data } = await cajaService.consolidado(params)
        consolidado.value = data
    } catch (e) {
        console.error('Error consolidado:', e)
    } finally {
        cargandoConsolidado.value = false
    }
}

function limpiarFiltros() {
    filtroConsolidado.fecha_desde = ''
    filtroConsolidado.fecha_hasta = ''
    cargarConsolidado()
}

function porcentajeSede(sede) {
    const total = consolidado.value?.total_global?.ingresos || 0
    if (!total) return 0
    return Math.round((sede.ingresos / total) * 100)
}

// Computed
const diferencia = computed(() => {
    const contado = parseFloat(formCierre.monto_final || 0)
    const esperado = store.saldoEsperado
    return parseFloat((contado - esperado).toFixed(2))
})

// Helpers
function formatearMonto(val) {
    return (parseFloat(val) || 0).toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
function formatearHora(fecha) {
    if (!fecha) return '—'
    return new Date(fecha).toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit' })
}
function formatearFecha(fecha) {
    if (!fecha) return '—'
    return new Date(fecha).toLocaleDateString('es-PE')
}
function formatearFechaHora(fecha) {
    if (!fecha) return '—'
    return new Date(fecha).toLocaleString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}
function calcularDuracion(apertura, cierre) {
    if (!apertura || !cierre) return '—'
    const mins = Math.round((new Date(cierre) - new Date(apertura)) / 60000)
    const h = Math.floor(mins / 60), m = mins % 60
    return h > 0 ? `${h}h ${m}m` : `${m}m`
}
function diferenciaHistorial(s) {
    if (!s.monto_final) return 0
    return parseFloat((parseFloat(s.monto_final) - parseFloat(s.saldo_esperado || 0)).toFixed(2))
}
function esIngreso(tipo) { return ['venta_pasaje', 'venta_encomienda'].includes(tipo) }
function claseTipo(tipo) {
    return { venta_pasaje: 'badge badge-green', venta_encomienda: 'badge badge-blue', gasto: 'badge badge-red', anulacion: 'badge badge-yellow' }[tipo] || 'badge badge-gray'
}
function etiquetaTipo(tipo) {
    return { venta_pasaje: 'Pasaje', venta_encomienda: 'Encomienda', gasto: 'Gasto', anulacion: 'Anulación' }[tipo] || tipo
}
function calcularDiferencia() { /* reactivo via computed */ }

// Watchers
watch(() => route.path, (path) => {
    if (path.includes('movimientos')) tabActivo.value = 'movimientos'
    else if (path.includes('arqueo')) tabActivo.value = 'arqueo'
    else tabActivo.value = 'apertura'
}, { immediate: false })

watch(tabActivo, (nuevo) => {
    if (nuevo === 'movimientos' && store.cajaAbierta) store.cargarMovimientos()
    if (nuevo === 'arqueo') store.cargarSesiones()
    if (nuevo === 'consolidado') cargarConsolidado()
}, { immediate: false })

// Acciones
async function abrirCaja() {
    erroresApertura.monto_inicial = ''
    errorApertura.value = ''
    if (!formApertura.monto_inicial && formApertura.monto_inicial !== 0) {
        erroresApertura.monto_inicial = 'Ingresa el monto inicial'; return
    }
    guardando.value = true
    try {
        await cajaService.abrirCaja({ monto_inicial: formApertura.monto_inicial, observacion: formApertura.observacion })
        await store.cargarMiSesion()
        await store.cargarMovimientos()
        formApertura.monto_inicial = ''; formApertura.observacion = ''
        tabActivo.value = 'movimientos'
    } catch (e) {
        const data = e.response?.data
        if (data?.monto_inicial) erroresApertura.monto_inicial = data.monto_inicial[0]
        else errorApertura.value = 'No se pudo abrir la caja. Verifica sucursal y vuelve a intentarlo.'
    } finally { guardando.value = false }
}

async function registrarEgreso() {
    erroresEgreso.monto = ''; erroresEgreso.descripcion = ''; erroresEgreso.servidor = ''
    let valido = true
    if (!formEgreso.monto || parseFloat(formEgreso.monto) <= 0) { erroresEgreso.monto = 'Ingresa un monto válido'; valido = false }
    if (!formEgreso.descripcion.trim()) { erroresEgreso.descripcion = 'La descripción es obligatoria'; valido = false }
    if (!valido) return
    guardando.value = true
    try {
        await cajaService.registrarEgreso({ sesion: store.sesionActiva.id, tipo: 'gasto', monto: formEgreso.monto, descripcion: formEgreso.descripcion })
        modalEgreso.value = false; formEgreso.monto = ''; formEgreso.descripcion = ''
        await store.cargarMovimientos()
    } catch { erroresEgreso.servidor = 'No se pudo registrar. Intenta de nuevo.' }
    finally { guardando.value = false }
}

async function cerrarCaja() {
    erroresCierre.monto_final = ''; errorCierre.value = ''
    if (!formCierre.monto_final) { erroresCierre.monto_final = 'Ingresa el monto contado'; modalConfirmarCierre.value = false; return }
    guardando.value = true
    try {
        await cajaService.cerrarCaja(store.sesionActiva.id, { monto_final: formCierre.monto_final, observacion: formCierre.observacion })
        modalConfirmarCierre.value = false; formCierre.monto_final = ''; formCierre.observacion = ''
        await store.cargarMiSesion(); await store.cargarSesiones()
        tabActivo.value = 'apertura'
    } catch { errorCierre.value = 'No se pudo cerrar la caja. Intenta de nuevo.'; modalConfirmarCierre.value = false }
    finally { guardando.value = false }
}

onMounted(async () => {
    await store.cargarMiSesion()
    if (store.cajaAbierta) await store.cargarMovimientos()
    store.cargarSesiones()
})
</script>