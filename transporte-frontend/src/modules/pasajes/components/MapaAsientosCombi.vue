<template>
  <div class="combi-wrapper">
    <div class="combi-body">

      <!-- Parabrisas -->
      <div class="combi-windshield">
        <div class="windshield-inner">
          <span class="windshield-text">🚌 FRENTE</span>
        </div>
      </div>

      <!-- Cabina: conductor + asientos 1 y 2 -->
      <div class="combi-cabin">
        <div class="seat seat-driver" title="Conductor">
          <svg viewBox="0 0 24 24" fill="currentColor" class="seat-icon">
            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
          </svg>
          <span class="seat-label">🚗</span>
        </div>
        <div class="cabin-gap"></div>
        <div class="cabin-passenger-seats">
          <button
            v-for="num in [1, 2]" :key="num"
            @click="toggleAsiento(num)"
            :disabled="estaOcupado(num)"
            :class="claseAsiento(num)"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" class="seat-icon-sm">
              <path d="M7 13c1.66 0 3-1.34 3-3S8.66 7 7 7s-3 1.34-3 3 1.34 3 3 3zm12-6h-8v7H3V5H1v15h2v-3h18v3h2v-9c0-2.21-1.79-4-4-4z"/>
            </svg>
            <span class="seat-num">{{ num }}</span>
          </button>
        </div>
      </div>

      <!-- Divisor cabina -->
      <div class="combi-divider"><div class="divider-line"></div></div>

      <!-- Filas centrales: 1 izq | pasillo | 2 der -->
      <div class="combi-rows">
        <div v-for="fila in filasCentrales" :key="'fila-' + fila.izq" class="combi-row">
          <button @click="toggleAsiento(fila.izq)" :disabled="estaOcupado(fila.izq)" :class="claseAsiento(fila.izq)">
            <svg viewBox="0 0 24 24" fill="currentColor" class="seat-icon-sm">
              <path d="M7 13c1.66 0 3-1.34 3-3S8.66 7 7 7s-3 1.34-3 3 1.34 3 3 3zm12-6h-8v7H3V5H1v15h2v-3h18v3h2v-9c0-2.21-1.79-4-4-4z"/>
            </svg>
            <span class="seat-num">{{ fila.izq }}</span>
          </button>
          <div class="row-aisle"></div>
          <div class="row-right">
            <button v-for="num in fila.der" :key="num" @click="toggleAsiento(num)" :disabled="estaOcupado(num)" :class="claseAsiento(num)">
              <svg viewBox="0 0 24 24" fill="currentColor" class="seat-icon-sm">
                <path d="M7 13c1.66 0 3-1.34 3-3S8.66 7 7 7s-3 1.34-3 3 1.34 3 3 3zm12-6h-8v7H3V5H1v15h2v-3h18v3h2v-9c0-2.21-1.79-4-4-4z"/>
              </svg>
              <span class="seat-num">{{ num }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Divisor fila trasera -->
      <div class="combi-divider"><div class="divider-line"></div></div>

      <!-- Fila trasera: 4 pegados -->
      <div class="fila-trasera">
        <button v-for="num in filaTrasera" :key="num" @click="toggleAsiento(num)" :disabled="estaOcupado(num)" :class="claseAsiento(num)">
          <svg viewBox="0 0 24 24" fill="currentColor" class="seat-icon-sm">
            <path d="M7 13c1.66 0 3-1.34 3-3S8.66 7 7 7s-3 1.34-3 3 1.34 3 3 3zm12-6h-8v7H3V5H1v15h2v-3h18v3h2v-9c0-2.21-1.79-4-4-4z"/>
          </svg>
          <span class="seat-num">{{ num }}</span>
        </button>
      </div>

      <div class="combi-rear"><div class="rear-line"></div></div>
    </div>

    <!-- Leyenda -->
    <div class="combi-legend">
      <div class="legend-item"><div class="legend-box seat-libre-demo"></div><span>Libre</span></div>
      <div class="legend-item"><div class="legend-box seat-ocupado-demo"></div><span>Ocupado</span></div>
      <div class="legend-item"><div class="legend-box seat-seleccionado-demo"></div><span>Seleccionado</span></div>
      <div class="legend-item"><div class="legend-box seat-driver-demo"></div><span>Conductor</span></div>
    </div>

    <!-- Resumen selección -->
    <div v-if="modelValue.length" class="seat-selected-msg">
      ✓ {{ modelValue.length }} asiento(s) seleccionado(s):
      <strong>{{ modelValue.slice().sort((a,b)=>a-b).join(', ') }}</strong>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Array,  default: () => [] }, // array de números seleccionados
  ocupados:   { type: Array,  default: () => [] },
  capacidad:  { type: Number, default: 18 },
})

const emit = defineEmits(['update:modelValue'])

const filaTrasera = computed(() => {
  const inicio = props.capacidad - 3
  return [inicio, inicio + 1, inicio + 2, inicio + 3]
})

const filasCentrales = computed(() => {
  const resultado = []
  let num = 3
  const fin = props.capacidad - 4
  while (num <= fin) {
    const izq = num; num++
    const der = []
    if (num <= fin) { der.push(num); num++ }
    if (num <= fin) { der.push(num); num++ }
    resultado.push({ izq, der })
  }
  return resultado
})

function estaOcupado(num) {
  return props.ocupados.includes(num)
}

function estaSeleccionado(num) {
  return props.modelValue.includes(num)
}

function toggleAsiento(num) {
  if (estaOcupado(num)) return
  const actual = [...props.modelValue]
  const idx = actual.indexOf(num)
  if (idx === -1) {
    actual.push(num)
  } else {
    actual.splice(idx, 1)
  }
  emit('update:modelValue', actual)
}

function claseAsiento(num) {
  const ocupado      = estaOcupado(num)
  const seleccionado = estaSeleccionado(num)
  return [
    'seat-btn',
    ocupado      ? 'seat-ocupado'      : '',
    seleccionado ? 'seat-seleccionado' : '',
    !ocupado && !seleccionado ? 'seat-libre' : '',
  ]
}
</script>

<style scoped>
.combi-wrapper { display: flex; flex-direction: column; align-items: center; gap: 16px; padding: 16px 0; }

.combi-body {
  background: #f8fafc; border: 2.5px solid #cbd5e1;
  border-radius: 28px 28px 16px 16px;
  padding: 0 14px 14px; width: 210px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.combi-windshield { margin: 0 -14px; border-radius: 24px 24px 0 0; background: linear-gradient(180deg, #bfdbfe 0%, #dbeafe 100%); border-bottom: 2px solid #93c5fd; padding: 10px 14px 8px; }
.windshield-inner { display: flex; justify-content: center; }
.windshield-text  { font-size: 10px; font-weight: 800; color: #1e40af; letter-spacing: 1px; text-transform: uppercase; }

.combi-cabin { display: flex; align-items: center; gap: 6px; padding: 10px 2px 6px; }
.cabin-gap   { flex: 1; }
.cabin-passenger-seats { display: flex; gap: 4px; }

.combi-divider { padding: 4px 0; }
.divider-line  { height: 2px; background: repeating-linear-gradient(90deg, #cbd5e1 0px, #cbd5e1 6px, transparent 6px, transparent 12px); border-radius: 2px; }

.combi-rows { display: flex; flex-direction: column; gap: 5px; padding: 6px 0; }
.combi-row  { display: flex; align-items: center; }
.row-aisle  { flex: 1; min-width: 14px; }
.row-right  { display: flex; gap: 4px; }

.fila-trasera { display: flex; gap: 3px; justify-content: center; margin-top: 6px; margin-bottom: 4px; }
.fila-trasera .seat-btn { flex: 1; }

.combi-rear { padding: 8px 0 0; }
.rear-line  { height: 3px; background: #cbd5e1; border-radius: 2px; }

.seat-driver { width: 42px; height: 42px; border-radius: 8px; background: #e2e8f0; border: 2px solid #94a3b8; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: not-allowed; gap: 1px; }
.seat-icon   { width: 14px; height: 14px; color: #64748b; }
.seat-label  { font-size: 8px; color: #64748b; font-weight: 700; }

.seat-btn { width: 42px; height: 42px; border-radius: 8px; border: 2px solid; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1px; cursor: pointer; transition: all 0.15s ease; font-family: inherit; padding: 0; }
.seat-btn:not(:disabled):hover { transform: scale(1.08); }
.seat-icon-sm { width: 13px; height: 13px; }
.seat-num     { font-size: 9px; font-weight: 800; line-height: 1; }

.seat-libre       { background: #ffffff; border-color: #cbd5e1; color: #64748b; }
.seat-libre:hover { background: #eff6ff; border-color: #93c5fd; color: #2563eb; }
.seat-ocupado     { background: #fee2e2; border-color: #fca5a5; color: #ef4444; cursor: not-allowed; opacity: 0.8; }
.seat-seleccionado { background: #2563eb; border-color: #1d4ed8; color: #ffffff; box-shadow: 0 0 0 3px #bfdbfe; transform: scale(1.08); }

.combi-legend { display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; }
.legend-item  { display: flex; align-items: center; gap: 5px; font-size: 11px; color: #64748b; font-weight: 500; }
.legend-box   { width: 14px; height: 14px; border-radius: 3px; border: 1.5px solid; }
.seat-libre-demo        { background: #fff;     border-color: #cbd5e1; }
.seat-ocupado-demo      { background: #fee2e2;  border-color: #fca5a5; }
.seat-seleccionado-demo { background: #2563eb;  border-color: #1d4ed8; }
.seat-driver-demo       { background: #e2e8f0;  border-color: #94a3b8; }

.seat-selected-msg { font-size: 12px; color: #2563eb; font-weight: 600; text-align: center; }
</style>