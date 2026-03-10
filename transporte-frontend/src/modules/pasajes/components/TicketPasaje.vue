<template>
  <AppModal v-model="show" titulo="Ticket de pasaje" ancho="sm">
    <div v-if="ticket" class="ticket-wrapper">
      <div class="ticket" ref="ticketRef">

        <!-- HEADER -->
        <div class="ticket-header">
          <img src="/logo1.png" class="ticket-logo" @error="e => e.target.style.display='none'" />
          <h1 class="ticket-empresa">TURISMO WJL E.I.R.L.</h1>
          <p class="ticket-slogan">Uniendo Familias</p>
          <div class="ticket-contacto">
            <p class="contacto-item">📍 Las 5 Esquinas - Huarmaca / Chiclayo</p>
            <p class="contacto-item">📞 +51 999 713 436</p>
          </div>
        </div>

        <div class="ticket-line-divider"></div>
        <div class="ticket-codigo-wrapper">
          <span class="ticket-codigo-label">TICKET N°:</span>
          <span class="ticket-codigo">{{ ticket.codigo?.slice(0, 8).toUpperCase() }}</span>
          <span class="ticket-fecha-emision">Emitido: {{ ahora }}</span>
        </div>
        <div class="ticket-line-divider"></div>

        <div class="ticket-ruta">
          <div class="ticket-ciudad">
            <span class="ticket-ciudad-nombre">{{ ciudadOrigen }}</span>
            <span class="ticket-ciudad-label">ORIGEN</span>
          </div>
          <div class="ticket-flecha-wrapper">
            <ArrowRight :size="16" stroke-width="3" color="#1d4ed8" />
          </div>
          <div class="ticket-ciudad">
            <span class="ticket-ciudad-nombre">{{ ciudadDestino }}</span>
            <span class="ticket-ciudad-label">DESTINO</span>
          </div>
        </div>

        <div class="ticket-seccion-titulo">👤 DATOS DEL PASAJERO</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Pasajero:</span><span class="ticket-dato-val">{{ ticket.pasajero_nombre }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">DNI:</span><span class="ticket-dato-val ticket-mono">{{ ticket.pasajero_dni }}</span></div>
          <div class="ticket-dato-fila" v-if="telefonoPasajero"><span class="ticket-dato-key">Teléfono:</span><span class="ticket-dato-val ticket-mono">{{ telefonoPasajero }}</span></div>
        </div>

        <div class="ticket-seccion-titulo">🚌 DATOS DEL VIAJE</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Fecha / Hora:</span><span class="ticket-dato-val ticket-mono">{{ formatearFechaHora(ticket.fecha_salida) }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Vehículo:</span><span class="ticket-dato-val ticket-mono">{{ ticket.vehiculo_placa }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Pago:</span><span class="ticket-dato-val">{{ metodoPagoLabel }}</span></div>
        </div>

        <template v-if="paquetes.length">
          <div class="ticket-seccion-titulo">📦 PAQUETES / BULTOS</div>
          <div class="ticket-datos">
            <div v-for="(pkg, i) in paquetes" :key="i" class="ticket-paquete">
              <div class="ticket-dato-fila">
                <span class="ticket-dato-key">Paquete {{ i + 1 }}:</span>
                <span class="ticket-dato-val">{{ pkg.descripcion }}</span>
              </div>
              <div class="ticket-dato-fila ticket-dato-fila--sub">
                <span class="ticket-dato-key">Bultos:</span>
                <span class="ticket-dato-val ticket-mono">{{ pkg.cantidad_bultos }}</span>
              </div>
              <div v-if="pkg.peso_kg" class="ticket-dato-fila ticket-dato-fila--sub">
                <span class="ticket-dato-key">Peso:</span>
                <span class="ticket-dato-val ticket-mono">{{ pkg.peso_kg }} kg</span>
              </div>
              <div class="ticket-dato-fila ticket-dato-fila--sub">
                <span class="ticket-dato-key">Precio:</span>
                <span class="ticket-dato-val ticket-mono ticket-paquete-precio">S/. {{ pkg.precio_adicional }}</span>
              </div>
              <div v-if="i < paquetes.length - 1" class="ticket-line-divider" style="margin: 4px 0;"></div>
            </div>
            <div class="ticket-dato-fila ticket-total-paquetes">
              <span class="ticket-dato-key">Total paquetes:</span>
              <span class="ticket-dato-val">S/. {{ totalPaquetes.toFixed(2) }}</span>
            </div>
          </div>
        </template>

        <div class="ticket-asiento-box">
          <div class="asiento-col col-izq">
            <span class="asiento-label">ASIENTO N°:</span>
            <span class="asiento-num">{{ ticket.asiento }}</span>
          </div>
          <div class="asiento-col col-der">
            <span class="asiento-label">PASAJE</span>
            <span class="asiento-monto">S/. {{ ticket.precio }}</span>
            <template v-if="paquetes.length">
              <span class="asiento-label" style="margin-top:4px;">PAQUETES</span>
              <span class="asiento-monto asiento-monto--paquete">+ S/. {{ totalPaquetes.toFixed(2) }}</span>
              <div style="border-top:1px dashed #000;width:100%;margin:4px 0;"></div>
              <span class="asiento-label">TOTAL</span>
              <span class="asiento-monto asiento-monto--total">S/. {{ totalGeneral.toFixed(2) }}</span>
            </template>
          </div>
        </div>

        <div class="ticket-estado-wrapper">
          <span :class="claseEstado(ticket.estado)" class="ticket-estado-badge">{{ etiquetaEstado(ticket.estado) }}</span>
        </div>

        <div class="ticket-footer">
          <p class="ticket-gracias">✦ Gracias por viajar con WJL Transportes ✦</p>
          <p class="ticket-footer-sub">Su seguridad es nuestra prioridad</p>
        </div>

      </div>
    </div>
    <template #footer>
      <button @click="show = false" class="btn-secondary">Cerrar</button>
      <button @click="imprimir" :disabled="generando" class="btn-primary">
        <svg v-if="generando" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
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
  ticket:     { type: Object, default: null },
})
const emit = defineEmits(['update:modelValue'])
const show = computed({ get: () => props.modelValue, set: (val) => emit('update:modelValue', val) })

const ticketRef = ref(null)
const generando = ref(false)

function fixOklchColors(doc) {
  const elements = doc.querySelectorAll('*')
  const oklchRegex = /oklch\([^)]*\)/g
  const colorMap = {
    'oklch(0.985 0 0)': '#fafafa',
    'oklch(0.97 0 0)':  '#f5f5f5',
    'oklch(0.922 0 0)': '#e5e5e5',
    'oklch(0.87 0 0)':  '#d4d4d4',
    'oklch(0.708 0 0)': '#a3a3a3',
    'oklch(0.556 0 0)': '#737373',
    'oklch(0.439 0 0)': '#525252',
    'oklch(0.269 0 0)': '#1a1a1a',
    'oklch(0.145 0 0)': '#0a0a0a',
    'oklch(1 0 0)':     '#ffffff',
    'oklch(0 0 0)':     '#000000',
  }
  elements.forEach(el => {
    try {
      const cs = doc.defaultView.getComputedStyle(el)
      const cssProps = ['color','background-color','border-color','border-top-color',
        'border-bottom-color','border-left-color','border-right-color','outline-color']
      cssProps.forEach(prop => {
        const val = cs.getPropertyValue(prop)
        if (val && val.includes('oklch')) {
          const fixed = colorMap[val.trim()] || val.replace(oklchRegex, '#666666')
          el.style.setProperty(prop, fixed, 'important')
        }
      })
      const inlineStyle = el.getAttribute('style') || ''
      if (inlineStyle.includes('oklch')) {
        el.setAttribute('style', inlineStyle.replace(oklchRegex, m => colorMap[m] || '#666666'))
      }
    } catch (_) {}
  })
}

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
      scale:           3,
      useCORS:         true,
      allowTaint:      true,
      backgroundColor: '#ffffff',
      logging:         false,
      windowWidth:     el.scrollWidth,
      windowHeight:    el.scrollHeight,
      onclone: (clonedDoc) => fixOklchColors(clonedDoc),
    })
    const pdfW = 80
    const pdfH = Math.ceil((canvas.height * pdfW) / canvas.width)
    const pdf  = new jsPDF({ orientation: 'portrait', unit: 'mm', format: [pdfW, pdfH] })
    pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, pdfW, pdfH)
    pdf.save(`Ticket_${props.ticket?.codigo?.slice(0, 8).toUpperCase() || 'WJL'}.pdf`)
  } catch (err) {
    console.error('Error al generar PDF:', err)
    alert('Error: ' + err.message)
  } finally {
    generando.value = false
  }
}

const metodosPago = [
  { clave: 'cash', etiqueta: 'Efectivo' },
  { clave: 'yape', etiqueta: 'Yape' },
  { clave: 'plin', etiqueta: 'Plin' },
  { clave: 'card', etiqueta: 'Tarjeta' },
]

const metodoPagoLabel  = computed(() => metodosPago.find(x => x.clave === props.ticket?.metodo_pago)?.etiqueta || '—')
const telefonoPasajero = computed(() => (props.ticket?.pasajero_telefono || props.ticket?.telefono || props.ticket?.pasajero?.telefono || '').toString().trim())
const paquetes         = computed(() => props.ticket?.paquetes || [])
const totalPaquetes    = computed(() => paquetes.value.reduce((sum, pkg) => sum + parseFloat(pkg.precio_adicional || 0), 0))
const totalGeneral     = computed(() => parseFloat(props.ticket?.precio || 0) + totalPaquetes.value)
const ciudadOrigen     = computed(() => props.ticket?.ruta_descripcion?.split('→')[0]?.trim() || '')
const ciudadDestino    = computed(() => props.ticket?.ruta_descripcion?.split('→')[1]?.trim() || '')
const ahora            = computed(() => new Date().toLocaleString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }))
const formatearFechaHora = (f) => f ? new Date(f).toLocaleString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'
const claseEstado    = (e) => ({ emitido: 't-emitido', embarcado: 't-embarcado', anulado: 't-anulado' }[e] || 't-emitido')
const etiquetaEstado = (e) => ({ emitido: 'EMITIDO', embarcado: 'EMBARCADO', anulado: 'ANULADO' }[e] || e)
</script>

<style scoped>
.ticket, .ticket * { box-sizing: border-box; }

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

/* ── HEADER ── */
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

/* ── CÓDIGO ── */
.ticket-line-divider { border-top: 1px dashed #e2e8f0; margin: 5px 15px; }

.ticket-codigo-wrapper { text-align: center; padding: 8px 10px; }
.ticket-codigo-label   { font-size: 10px; font-weight: 600; color: #4a5460; display: block; }
.ticket-codigo         { font-size: 15px; font-weight: 800; color: #111827; display: block; letter-spacing: 1px; }
.ticket-fecha-emision  { font-size: 9px; color: #4a5460; display: block; }

/* ── RUTA ── */
.ticket-ruta { display: flex; justify-content: space-around; align-items: center; padding: 10px 15px; }
.ticket-ciudad { text-align: center; flex: 1; }
.ticket-ciudad-nombre { font-size: 12px; font-weight: 800; display: block; text-transform: uppercase; }
.ticket-ciudad-label  { font-size: 8px; color: #4a5460; font-weight: bold; }
.ticket-flecha-wrapper { padding: 0 10px; }

/* ── SECCIONES ── */
.ticket-seccion-titulo {
  font-size: 9px;
  font-weight: 800;
  color: #4a5460;
  background: #f1f5f9;
  padding: 5px 15px;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

.ticket-datos { padding: 8px 15px; }

.ticket-dato-fila {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  padding: 3px 0;
  gap: 10px;
}

.ticket-dato-fila--sub { font-size: 10px; color: #555; padding-left: 8px; }
.ticket-dato-key { color: #4a5460; flex-shrink: 0; }
.ticket-dato-val { font-weight: bold; color: #000; text-align: right; word-break: break-word; }
.ticket-mono { font-family: monospace; }
.ticket-paquete { margin-bottom: 2px; }
.ticket-paquete-precio { color: #ea580c; }
.ticket-total-paquetes { margin-top: 6px; padding-top: 5px; border-top: 1px solid #e2e8f0; font-weight: 800; color: #ea580c; }

/* ── ASIENTO ── */
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

.col-izq { border-right: 1.5px solid #000; background: #f8fafc; }
.asiento-label { font-size: 9px; font-weight: 800; color: #000; margin-bottom: 2px; }
.asiento-num   { font-size: 20px; font-weight: 900; color: #1d4ed8; line-height: 1; }
.asiento-monto { font-size: 13px; font-weight: 900; color: #000; line-height: 1.2; }
.asiento-monto--paquete { font-size: 11px; color: #ea580c; }
.asiento-monto--total   { font-size: 14px; color: #000; }

/* ── ESTADO ── */
.ticket-estado-wrapper {
  text-align: center;
  padding: 10px;
  width: 100%;
}

.ticket-estado-badge {
  padding: 3px 14px;
  border-radius: 99px;
  font-size: 9px;
  font-weight: 800;
  border: 1.5px solid currentColor;
  display: inline-block;
}

.t-emitido  { color: #1d4ed8; }
.t-embarcado { color: #16a34a; }
.t-anulado  { color: #dc2626; }

/* ── FOOTER ── */
.ticket-footer { text-align: center; padding: 12px 15px; border-top: 1px dashed #e2e8f0; }
.ticket-gracias    { font-size: 10px; font-weight: bold; margin-bottom: 3px; }
.ticket-footer-sub { font-size: 9px; color: #4a5460; font-style: italic; }
</style>