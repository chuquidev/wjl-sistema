<template>
  <AppModal v-model="show" titulo="Comprobante de encomienda" ancho="sm">
    <div v-if="enc" class="ticket-wrapper">
      <div class="ticket" ref="ticketRef">

        <!-- Header -->
        <div class="ticket-header">
          <img src="/logo1.png" class="ticket-logo" @error="e => e.target.style.display='none'" />
          <h1 class="ticket-empresa">TURISMO WJL E.I.R.L.</h1>
          <p class="ticket-slogan">Uniendo Familias</p>
          <div class="ticket-contacto">
            <div class="contacto-item"><MapPin :size="10" stroke-width="2.5" color="black" /><span>Las 5 Esquinas - Huarmaca / Chiclayo</span></div>
            <div class="contacto-item"><Phone :size="10" stroke-width="2.5" color="black" /><span>+51 999 713 436</span></div>
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
          <div class="ticket-flecha-wrapper"><ArrowRight :size="16" stroke-width="3" color="#ea580c" /></div>
          <div class="ticket-ciudad">
            <span class="ticket-ciudad-nombre">{{ viajeDestino || '-' }}</span>
            <span class="ticket-ciudad-label">DESTINO</span>
          </div>
        </div>

        <!-- Datos del vehiculo (fecha + placa) -->
        <div v-if="viajeFecha || viajePlaca" class="ticket-seccion-titulo">
          <Bus :size="10" stroke-width="2.5" /> DATOS DEL VEHICULO
        </div>
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
        <div class="ticket-seccion-titulo"><User :size="10" stroke-width="2.5" /> REMITENTE (ENVIA)</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Nombre: </span><span class="ticket-dato-val">{{ enc.remitente_nombre }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">DNI: </span><span class="ticket-dato-val ticket-mono">{{ enc.remitente_dni }}</span></div>
          <div v-if="enc.remitente_telefono" class="ticket-dato-fila"><span class="ticket-dato-key">Telefono: </span><span class="ticket-dato-val ticket-mono">{{ enc.remitente_telefono }}</span></div>
        </div>

        <!-- Destinatario -->
        <div class="ticket-seccion-titulo"><UserCheck :size="10" stroke-width="2.5" /> DESTINATARIO (RECIBE)</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Nombre: </span><span class="ticket-dato-val">{{ enc.destinatario_nombre }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">DNI: </span><span class="ticket-dato-val ticket-mono">{{ enc.destinatario_dni }}</span></div>
          <div v-if="enc.destinatario_telefono" class="ticket-dato-fila"><span class="ticket-dato-key">Telefono: </span><span class="ticket-dato-val ticket-mono">{{ enc.destinatario_telefono }}</span></div>
        </div>

        <!-- Paquete -->
        <div class="ticket-seccion-titulo"><Package :size="10" stroke-width="2.5" /> DATOS DEL PAQUETE</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Descripcion: </span><span class="ticket-dato-val">{{ enc.descripcion }}</span></div>
          <div v-if="enc.peso_kg" class="ticket-dato-fila"><span class="ticket-dato-key">Peso: </span><span class="ticket-dato-val ticket-mono">{{ enc.peso_kg }} kg</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Pago: </span><span class="ticket-dato-val">{{ metodoPagoLabel }}</span></div>
          <div v-if="enc.observacion" class="ticket-dato-fila"><span class="ticket-dato-key">Obs.: </span><span class="ticket-dato-val">{{ enc.observacion }}</span></div>
        </div>

        <!-- Box estado + precio — mismo diseño que TicketPasaje -->
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
      <button @click="imprimir" class="btn-primary"><Printer :size="16" style="margin-right:8px" /> Imprimir</button>
    </template>
  </AppModal>
</template>

<script setup>
import { computed, ref } from 'vue'
import AppModal from '@/components/common/AppModal.vue'
import { useVueToPrint } from 'vue-to-print'
import { MapPin, Phone, ArrowRight, User, UserCheck, Package, Printer, Bus } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  enc:        { type: Object,  default: null  },
})
const emit = defineEmits(['update:modelValue'])
const show = computed({ get: () => props.modelValue, set: (val) => emit('update:modelValue', val) })

const ticketRef = ref(null)
const { handlePrint } = useVueToPrint({
  content: () => ticketRef.value,
  documentTitle: `Encomienda_${props.enc?.codigo || ''}`,
  removeAfterPrint: true,
})
const imprimir = () => handlePrint()

const metodosPago = [
  { clave: 'cash', etiqueta: 'Efectivo' },
  { clave: 'yape', etiqueta: 'Yape'     },
  { clave: 'plin', etiqueta: 'Plin'     },
  { clave: 'card', etiqueta: 'Tarjeta'  },
]
const metodoPagoLabel = computed(() =>
  metodosPago.find(x => x.clave === props.enc?.metodo_pago)?.etiqueta || '-'
)

// Parsear viaje_descripcion: "Chiclayo - Lambayeque -> Huarmaca - Piura | 04/03/2026 01:00 | ABC-12J"
// Formato: ORIGEN → DESTINO | FECHA HORA | PLACA
const viajePartes = computed(() => {
  const desc = props.enc?.viaje_descripcion || ''
  if (!desc) return { origen: '', destino: '', fecha: '', placa: '' }

  // Separar por "|"
  const partesPipe = desc.split('|').map(s => s.trim())
  // La primera parte tiene "ORIGEN → DESTINO"
  const rutaParte = partesPipe[0] || ''
  const fechaParte = partesPipe[1] || ''   // ej: "04/03/2026 01:00"
  const placaParte = partesPipe[2] || ''   // ej: "ABC-12J"

  // Separar origen y destino por "→" o "->"
  const flechaIdx = rutaParte.indexOf('→') !== -1
    ? rutaParte.indexOf('→')
    : rutaParte.indexOf('->')

  let origen = ''
  let destino = ''
  if (flechaIdx !== -1) {
    origen  = rutaParte.substring(0, flechaIdx).trim()
    destino = rutaParte.substring(flechaIdx + 1).replace('>', '').trim()
  } else {
    origen = rutaParte.trim()
  }

  return {
    origen:  origen,
    destino: destino,
    fecha:   fechaParte,
    placa:   placaParte,
  }
})

const viajeOrigen  = computed(() => viajePartes.value.origen)
const viajeDestino = computed(() => viajePartes.value.destino)
const viajeFecha   = computed(() => viajePartes.value.fecha)
const viajePlaca   = computed(() => viajePartes.value.placa)

const ahora = computed(() => new Date().toLocaleString('es-PE', {
  day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit',
}))

const claseEstado = (e) => ({
  registrada:  't-registrada',
  en_transito: 't-transito',
  entregada:   't-entregada',
  devuelta:    't-devuelta',
}[e] || 't-registrada')

const etiquetaEstado = (e) => ({
  registrada:  'REGISTRADA',
  en_transito: 'EN TRANSITO',
  entregada:   'ENTREGADA',
  devuelta:    'DEVUELTA',
}[e] || e)
</script>

<style scoped>
/* CSS 100% identico al TicketPasaje */
.ticket, .ticket * { box-sizing: border-box; }
.ticket-wrapper { display: flex; justify-content: center; padding: 20px 0; background-color: #f1f5f9; }
.ticket { width: 100%; max-width: 290px; background: white; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; font-family: 'Helvetica', Arial, sans-serif; color: #000; margin: 0 auto; }
.ticket-header { padding: 15px; text-align: center; color: #1e3a8a; background: #f8fafc; }
.ticket-logo { width: 80px; height: auto; margin: 0 auto 10px; display: block; object-fit: contain; }
.ticket-empresa { font-size: 13px; font-weight: 800; margin: 0; }
.ticket-slogan { font-size: 10px; color: #4a5460; margin: 2px 0; }
.ticket-contacto { display: flex; flex-direction: column; align-items: center; gap: 3px; margin-top: 5px; }
.contacto-item { display: flex; align-items: center; gap: 4px; font-size: 9px; color: #000; font-weight: 600; text-align: center; }
.ticket-line-divider { border-top: 1px dashed #e2e8f0; margin: 5px 15px; }
.ticket-codigo-wrapper { text-align: center; padding: 10px; }
.ticket-codigo-label { font-size: 9px; color: #4a5460; display: block; }
.ticket-codigo { font-size: 16px; font-weight: 800; color: #111827; display: block; letter-spacing: 1px; }
.ticket-fecha-emision { font-size: 9px; color: #4a5460; }
.ticket-ruta { display: flex; justify-content: space-around; align-items: center; padding: 10px 15px; }
.ticket-ciudad { text-align: center; flex: 1; }
.ticket-ciudad-nombre { font-size: 12px; font-weight: 800; display: block; text-transform: uppercase; }
.ticket-ciudad-label { font-size: 8px; color: #4a5460; font-weight: bold; }
.ticket-flecha-wrapper { padding: 0 10px; }
.ticket-seccion-titulo { font-size: 9px; font-weight: 800; color: #4a5460; background: #f1f5f9; padding: 5px 15px; display: flex; align-items: center; gap: 5px; border-top: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }
.ticket-datos { padding: 8px 15px; }
.ticket-dato-fila { display: flex; justify-content: space-between; font-size: 11px; padding: 3px 0; gap: 10px; }
.ticket-dato-key { color: #4a5460; flex-shrink: 0; }
.ticket-dato-val { font-weight: bold; color: #000; text-align: right; word-break: break-word; }
.ticket-mono { font-family: monospace; }
.ticket-asiento-box { display: flex; margin: 10px 15px; border: 1.5px solid #000; border-radius: 8px; overflow: hidden; }
.asiento-col { flex: 1; padding: 10px 5px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.col-izq { border-right: 1.5px solid #000; background: #f8fafc; }
.col-der { background: #fff7ed; }
.asiento-label { font-size: 9px; font-weight: 800; color: #000; margin-bottom: 4px; }
.asiento-monto { font-size: 20px; font-weight: 900; color: #ea580c; line-height: 1; }
.ticket-estado-badge { padding: 3px 10px; border-radius: 99px; font-size: 9px; font-weight: 800; border: 1.5px solid currentColor; display: inline-block; text-align: center; }
.t-registrada { color: #6b7280; }
.t-transito   { color: #1d4ed8; }
.t-entregada  { color: #16a34a; }
.t-devuelta   { color: #dc2626; }
.ticket-footer { text-align: center; padding: 15px; border-top: 1px dashed #e2e8f0; }
.ticket-gracias { font-size: 10px; font-weight: bold; margin-bottom: 3px; }
.ticket-footer-sub { font-size: 9px; color: #4a5460; font-style: italic; }
@media print {
  @page { margin: 0; }
  .ticket-wrapper { padding: 0; background: white; display: flex !important; justify-content: center !important; width: 100% !important; }
  .ticket { width: 72mm !important; max-width: 72mm !important; border: none !important; margin: 0 auto !important; }
  .ticket-header { background: white !important; }
  .ticket-logo { filter: none !important; -webkit-print-color-adjust: exact; }
  .ticket-seccion-titulo { background: #eee !important; -webkit-print-color-adjust: exact; }
  .ticket-asiento-box { border: 1.5px solid #000 !important; display: flex !important; }
  .col-izq { border-color: #000 !important; }
  .col-der { background: #fff7ed !important; -webkit-print-color-adjust: exact; }
  .asiento-monto { color: #ea580c !important; -webkit-print-color-adjust: exact; }
}
</style>