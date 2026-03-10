<template>
  <AppModal v-model="show" titulo="Comprobante de encomienda" ancho="sm">
    <div v-if="enc" class="ticket-wrapper">
      <div class="ticket" ref="ticketRef">

        <!-- Header -->
        <div class="ticket-header">
          <img src="/logo1.png" class="ticket-logo" @error="e => e.target.style.display = 'none'" />
          <h1 class="ticket-empresa">TURISMO WJL E.I.R.L.</h1>
          <p class="ticket-slogan">Uniendo Familias</p>
          <div class="ticket-contacto">
            <p class="contacto-item">📍 Las 5 Esquinas - Huarmaca / Chiclayo</p>
            <p class="contacto-item">📞 +51 999 713 436</p>
          </div>
        </div>

        <div class="ticket-line-divider"></div>
        <div class="ticket-codigo-wrapper">
          <span class="ticket-codigo-label">ENCOMIENDA N°: </span>
          <span class="ticket-codigo">{{ String(enc.codigo || '').slice(0, 8).toUpperCase() }}</span>
          <span class="ticket-fecha-emision">Emitido: {{ ahora }}</span>
        </div>
        <div class="ticket-line-divider"></div>

        <!-- Ruta origen → destino -->
        <div v-if="viajeOrigen || viajeDestino" class="ticket-ruta">
          <div class="ticket-ciudad">
            <span class="ticket-ciudad-nombre">{{ viajeOrigen || '-' }}</span>
            <span class="ticket-ciudad-label">ORIGEN</span>
          </div>
          <div class="ticket-flecha-wrapper">
            <ArrowRight :size="16" stroke-width="3" color="#ea580c" />
          </div>
          <div class="ticket-ciudad">
            <span class="ticket-ciudad-nombre">{{ viajeDestino || '-' }}</span>
            <span class="ticket-ciudad-label">DESTINO</span>
          </div>
        </div>

        <!-- Datos del vehiculo -->
        <div v-if="viajeFecha || viajePlaca" class="ticket-seccion-titulo">🚌 DATOS DEL VEHICULO</div>
        <div v-if="viajeFecha || viajePlaca" class="ticket-datos">
          <div v-if="viajeFecha" class="ticket-dato-fila">
            <span class="ticket-dato-key">Fecha / Hora: </span>
            <span class="ticket-dato-val ticket-mono">{{ viajeFecha }}</span>
          </div>
          <div v-if="viajePlaca" class="ticket-dato-fila">
            <span class="ticket-dato-key">Vehiculo: </span>
            <span class="ticket-dato-val ticket-mono">{{ viajePlaca }}</span>
          </div>
        </div>

        <!-- Remitente -->
        <div class="ticket-seccion-titulo">👤 REMITENTE (ENVIA)</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Nombre: </span><span class="ticket-dato-val">{{
            enc.remitente_nombre }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">DNI: </span><span
              class="ticket-dato-val ticket-mono">{{ enc.remitente_dni }}</span></div>
          <div v-if="enc.remitente_telefono" class="ticket-dato-fila"><span class="ticket-dato-key">Telefono:
            </span><span class="ticket-dato-val ticket-mono">{{ enc.remitente_telefono }}</span></div>
        </div>

        <!-- Destinatario -->
        <div class="ticket-seccion-titulo">✅ DESTINATARIO (RECIBE)</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Nombre: </span><span class="ticket-dato-val">{{
            enc.destinatario_nombre }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">DNI: </span><span
              class="ticket-dato-val ticket-mono">{{ enc.destinatario_dni }}</span></div>
          <div v-if="enc.destinatario_telefono" class="ticket-dato-fila"><span class="ticket-dato-key">Telefono:
            </span><span class="ticket-dato-val ticket-mono">{{ enc.destinatario_telefono }}</span></div>
        </div>

        <!-- Paquete -->
        <div class="ticket-seccion-titulo">📦 DATOS DEL PAQUETE</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Descripcion: </span><span
              class="ticket-dato-val">{{ enc.descripcion }}</span></div>
          <div v-if="enc.peso_kg" class="ticket-dato-fila"><span class="ticket-dato-key">Peso: </span><span
              class="ticket-dato-val ticket-mono">{{ enc.peso_kg }} kg</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Pago: </span><span class="ticket-dato-val">{{
              metodoPagoLabel }}</span></div>
          <div v-if="enc.observacion" class="ticket-dato-fila"><span class="ticket-dato-key">Obs.: </span><span
              class="ticket-dato-val">{{ enc.observacion }}</span></div>
        </div>

        <!-- Box estado + precio -->
        <div class="ticket-asiento-box">
          <div class="asiento-col col-izq">
            <span class="asiento-label">ESTADO</span>
            <span :class="claseEstado(enc.estado)" class="ticket-estado-badge">{{ etiquetaEstado(enc.estado) }}</span>
          </div>
          <div class="asiento-col col-der">
            <span class="asiento-label">TOTAL PAGADO</span>
            <span class="asiento-monto">S/. {{ enc.precio }}</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="ticket-footer">
          <p class="ticket-gracias">+ Gracias por confiar en WJL Transportes +</p>
          <p class="ticket-footer-sub">Conserve este comprobante para el seguimiento</p>
        </div>

      </div>
    </div>
    <template #footer>
      <button @click="show = false" class="btn-secondary">Cerrar</button>
      <button @click="imprimir" :disabled="generando" class="btn-primary">
        <svg v-if="generando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <Printer v-else :size="16" style="margin-right:8px" />
        {{ generando ? 'Generando...' : 'Imprimir / PDF' }}
      </button>
    </template>
  </AppModal>
</template>

<script setup>
import { computed, ref, nextTick } from 'vue'
import AppModal from '@/components/common/AppModal.vue'
import { ArrowRight, Printer } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  enc: { type: Object, default: null },
})
const emit = defineEmits(['update:modelValue'])
const show = computed({ get: () => props.modelValue, set: (val) => emit('update:modelValue', val) })

const ticketRef = ref(null)
const generando = ref(false)

// ── Fix oklch (Tailwind v4 no soportado por html2canvas) ─
function fixOklchColors(doc) {
  const elements = doc.querySelectorAll('*')
  const oklchRegex = /oklch\([^)]*\)/g
  const colorMap = {
    'oklch(0.985 0 0)': '#fafafa', 'oklch(0.97 0 0)': '#f5f5f5',
    'oklch(0.922 0 0)': '#e5e5e5', 'oklch(0.87 0 0)': '#d4d4d4',
    'oklch(0.708 0 0)': '#a3a3a3', 'oklch(0.556 0 0)': '#737373',
    'oklch(0.439 0 0)': '#525252', 'oklch(0.269 0 0)': '#1a1a1a',
    'oklch(0.145 0 0)': '#0a0a0a', 'oklch(1 0 0)': '#ffffff',
    'oklch(0 0 0)': '#000000',
  }
  elements.forEach(el => {
    try {
      const cs = doc.defaultView.getComputedStyle(el)
      const cssProps = ['color', 'background-color', 'border-color', 'border-top-color',
        'border-bottom-color', 'border-left-color', 'border-right-color', 'outline-color']
      cssProps.forEach(prop => {
        const val = cs.getPropertyValue(prop)
        if (val && val.includes('oklch')) {
          el.style.setProperty(prop, colorMap[val.trim()] || val.replace(oklchRegex, '#666666'), 'important')
        }
      })
      const inlineStyle = el.getAttribute('style') || ''
      if (inlineStyle.includes('oklch'))
        el.setAttribute('style', inlineStyle.replace(oklchRegex, m => colorMap[m] || '#666666'))
    } catch (_) { }
  })
}

// ── Generar PDF ───────────────────────────────────────────
async function imprimir() {
  if (!ticketRef.value) return
  generando.value = true
  await nextTick()
  await new Promise(r => setTimeout(r, 400))
  try {
    const [{ default: html2canvas }, { default: jsPDF }] = await Promise.all([
      import('html2canvas'),
      import('jspdf'),
    ])
    const el = ticketRef.value
    const canvas = await html2canvas(el, {
      scale: 3,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      logging: false,
      windowWidth: el.scrollWidth,
      windowHeight: el.scrollHeight,
      onclone: (clonedDoc) => fixOklchColors(clonedDoc),
    })
    const pdfW = 80
    const pdfH = Math.ceil((canvas.height * pdfW) / canvas.width)
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: [pdfW, pdfH] })
    pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, pdfW, pdfH)
    pdf.save(`Encomienda_${String(props.enc?.codigo || 'WJL').slice(0, 8).toUpperCase()}.pdf`)
  } catch (err) {
    console.error('Error PDF:', err)
    alert('Error: ' + err.message)
  } finally {
    generando.value = false
  }
}

// ── Helpers ───────────────────────────────────────────────
const metodosPago = [
  { clave: 'cash', etiqueta: 'Efectivo' },
  { clave: 'yape', etiqueta: 'Yape' },
  { clave: 'plin', etiqueta: 'Plin' },
  { clave: 'card', etiqueta: 'Tarjeta' },
]
const metodoPagoLabel = computed(() =>
  metodosPago.find(x => x.clave === props.enc?.metodo_pago)?.etiqueta || '-'
)

const viajePartes = computed(() => {
  const desc = props.enc?.viaje_descripcion || ''
  if (!desc) return { origen: '', destino: '', fecha: '', placa: '' }
  const partesPipe = desc.split('|').map(s => s.trim())
  const rutaParte = partesPipe[0] || ''
  const fechaParte = partesPipe[1] || ''
  const placaParte = partesPipe[2] || ''
  const flechaIdx = rutaParte.indexOf('→') !== -1
    ? rutaParte.indexOf('→')
    : rutaParte.indexOf('->')
  let origen = '', destino = ''
  if (flechaIdx !== -1) {
    origen = rutaParte.substring(0, flechaIdx).trim()
    destino = rutaParte.substring(flechaIdx + 1).replace('>', '').trim()
  } else {
    origen = rutaParte.trim()
  }
  return { origen, destino, fecha: fechaParte, placa: placaParte }
})

const viajeOrigen = computed(() => viajePartes.value.origen)
const viajeDestino = computed(() => viajePartes.value.destino)
const viajeFecha = computed(() => viajePartes.value.fecha)
const viajePlaca = computed(() => viajePartes.value.placa)

const ahora = computed(() => new Date().toLocaleString('es-PE', {
  day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit',
}))

const claseEstado = (e) => ({ registrada: 't-registrada', en_transito: 't-transito', entregada: 't-entregada', devuelta: 't-devuelta' }[e] || 't-registrada')
const etiquetaEstado = (e) => ({ registrada: 'REGISTRADA', en_transito: 'EN TRANSITO', entregada: 'ENTREGADA', devuelta: 'DEVUELTA' }[e] || e)
</script>

<style scoped>
.ticket,
.ticket * {
  box-sizing: border-box;
}

.ticket-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  background-color: #f1f5f9;
}

.ticket {
  width: 100%;
  max-width: 290px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  font-family: 'Helvetica', Arial, sans-serif;
  color: #000;
  margin: 0 auto;
}

.ticket-header {
  padding: 12px 15px 8px;
  text-align: center;
  background: #f8fafc;
}

.ticket-logo {
  width: 72px;
  height: auto;
  margin: 0 auto 6px;
  display: block;
  object-fit: contain;
}

.ticket-empresa {
  font-size: 12px;
  font-weight: 800;
  color: #1e3a8a;
  margin: 0 0 1px;
}

.ticket-slogan {
  font-size: 9px;
  color: #4a5460;
  margin: 0 0 6px;
  font-style: italic;
}

.ticket-contacto {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.contacto-item {
  font-size: 9px;
  color: #111;
  font-weight: 600;
  margin: 0;
  line-height: 1.4;
}

.ticket-line-divider {
  border-top: 1px dashed #e2e8f0;
  margin: 5px 15px;
}

.ticket-codigo-wrapper {
  text-align: center;
  padding: 8px 10px;
}

.ticket-codigo-label {
  font-size: 9px;
  color: #4a5460;
  display: block;
}

.ticket-codigo {
  font-size: 15px;
  font-weight: 800;
  color: #111827;
  display: block;
  letter-spacing: 1px;
}

.ticket-fecha-emision {
  font-size: 9px;
  color: #4a5460;
  display: block;
}

.ticket-ruta {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10px 15px;
}

.ticket-ciudad {
  text-align: center;
  flex: 1;
}

.ticket-ciudad-label {
  font-size: 8px;
  color: #4a5460;
  font-weight: bold;
}

.ticket-flecha-wrapper {
  padding: 0 10px;
}

.ticket-ciudad-nombre {
  font-size: 9px;
  font-weight: 800;
  display: block;
  text-transform: uppercase;
}

.ticket-seccion-titulo {
  font-size: 9px;
  font-weight: 800;
  color: #4a5460;
  background: #f1f5f9;
  padding: 5px 15px;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

.ticket-datos {
  padding: 8px 15px;
}

.ticket-dato-fila {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  padding: 3px 0;
  gap: 10px;
}

.ticket-dato-key {
  color: #4a5460;
  flex-shrink: 0;
}

.ticket-dato-val {
  font-weight: bold;
  color: #000;
  text-align: right;
  word-break: break-word;
}

.ticket-mono {
  font-family: monospace;
}

.ticket-asiento-box {
  display: flex;
  margin: 10px 15px;
  border: 1.5px solid #000;
  border-radius: 8px;
  overflow: hidden;
}

.asiento-col {
  flex: 1;
  padding: 10px 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.col-izq {
  border-right: 1.5px solid #000;
  background: #f8fafc;
}

.col-der {
  background: #fff7ed;
}

.asiento-label {
  font-size: 9px;
  font-weight: 800;
  color: #000;
  margin-bottom: 4px;
}

.asiento-monto {
  font-size: 12px;
  font-weight: 900;
  color: #ea580c;
  line-height: 1;
}

.ticket-estado-badge {
  font-size: 9px;
  font-weight: 800;
  display: inline-block;
  text-align: center;
  border: none;
}

.t-registrada {
  color: #6b7280;
}

.ticket-ciudad-nombre .t-transito {
  color: #1d4ed8;
}

.t-entregada {
  color: #16a34a;
}

.t-devuelta {
  color: #dc2626;
}

.ticket-footer {
  text-align: center;
  padding: 12px 15px;
  border-top: 1px dashed #e2e8f0;
}

.ticket-gracias {
  font-size: 10px;
  font-weight: bold;
  margin-bottom: 3px;
}

.ticket-footer-sub {
  font-size: 9px;
  color: #4a5460;
  font-style: italic;
}
</style>