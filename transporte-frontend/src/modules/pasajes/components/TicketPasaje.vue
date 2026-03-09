<template>
  <AppModal v-model="show" titulo="Ticket de pasaje" ancho="sm">
    <div v-if="ticket" class="ticket-wrapper">
      <div class="ticket" ref="ticketRef">

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
          <span class="ticket-codigo-label">TICKET N°: </span>
          <span class="ticket-codigo">{{ ticket.codigo?.slice(0, 8).toUpperCase() }}</span>
          <span class="ticket-fecha-emision">Emitido: {{ ahora }}</span>
        </div>
        <div class="ticket-line-divider"></div>

        <div class="ticket-ruta">
          <div class="ticket-ciudad"><span class="ticket-ciudad-nombre">{{ ciudadOrigen }}</span><span class="ticket-ciudad-label">ORIGEN</span></div>
          <div class="ticket-flecha-wrapper"><ArrowRight :size="16" stroke-width="3" color="#1d4ed8" /></div>
          <div class="ticket-ciudad"><span class="ticket-ciudad-nombre">{{ ciudadDestino }}</span><span class="ticket-ciudad-label">DESTINO</span></div>
        </div>

        <div class="ticket-seccion-titulo"><User :size="10" stroke-width="2.5" /> DATOS DEL PASAJERO</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Pasajero: </span><span class="ticket-dato-val">{{ ticket.pasajero_nombre }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">DNI: </span><span class="ticket-dato-val ticket-mono">{{ ticket.pasajero_dni }}</span></div>
          <div class="ticket-dato-fila" v-if="telefonoPasajero"><span class="ticket-dato-key">Teléfono: </span><span class="ticket-dato-val ticket-mono">{{ telefonoPasajero }}</span></div>
        </div>

        <div class="ticket-seccion-titulo"><Bus :size="10" stroke-width="2.5" /> DATOS DEL VIAJE</div>
        <div class="ticket-datos">
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Fecha / Hora: </span><span class="ticket-dato-val ticket-mono">{{ formatearFechaHora(ticket.fecha_salida) }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Vehículo: </span><span class="ticket-dato-val ticket-mono">{{ ticket.vehiculo_placa }}</span></div>
          <div class="ticket-dato-fila"><span class="ticket-dato-key">Pago: </span><span class="ticket-dato-val">{{ metodoPagoLabel }}</span></div>
        </div>

        <!-- PAQUETES solo si tiene -->
        <template v-if="paquetes.length">
          <div class="ticket-seccion-titulo"><Package :size="10" stroke-width="2.5" /> PAQUETES / BULTOS</div>
          <div class="ticket-datos">
            <div v-for="(pkg, i) in paquetes" :key="i" class="ticket-paquete">
              <div class="ticket-dato-fila">
                <span class="ticket-dato-key">Paquete {{ i + 1 }}: </span>
                <span class="ticket-dato-val">{{ pkg.descripcion }}</span>
              </div>
              <div class="ticket-dato-fila ticket-dato-fila--sub">
                <span class="ticket-dato-key">Bultos: </span>
                <span class="ticket-dato-val ticket-mono">{{ pkg.cantidad_bultos }}</span>
              </div>
              <div v-if="pkg.peso_kg" class="ticket-dato-fila ticket-dato-fila--sub">
                <span class="ticket-dato-key">Peso: </span>
                <span class="ticket-dato-val ticket-mono">{{ pkg.peso_kg }} kg</span>
              </div>
              <div class="ticket-dato-fila ticket-dato-fila--sub">
                <span class="ticket-dato-key">Precio: </span>
                <span class="ticket-dato-val ticket-mono ticket-paquete-precio">S/. {{ pkg.precio_adicional }}</span>
              </div>
              <div v-if="i < paquetes.length - 1" class="ticket-line-divider" style="margin: 4px 0;"></div>
            </div>
            <div class="ticket-dato-fila ticket-total-paquetes">
              <span class="ticket-dato-key">Total paquetes: </span>
              <span class="ticket-dato-val">S/. {{ totalPaquetes.toFixed(2) }}</span>
            </div>
          </div>
        </template>

        <!-- BOX ASIENTO -->
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
      <button @click="imprimir" class="btn-primary"><Printer :size="16" style="margin-right:8px" /> Imprimir</button>
    </template>
  </AppModal>
</template>

<script setup>
import { computed, ref } from 'vue'
import AppModal from '@/components/common/AppModal.vue'
import { useVueToPrint } from 'vue-to-print'
import { MapPin, Phone, ArrowRight, User, Bus, Printer, Package } from 'lucide-vue-next'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  ticket:     { type: Object, default: null },
})
const emit = defineEmits(['update:modelValue'])
const show = computed({ get: () => props.modelValue, set: (val) => emit('update:modelValue', val) })

const ticketRef = ref(null)
const { handlePrint } = useVueToPrint({
  content: () => ticketRef.value,
  documentTitle: `Ticket_${props.ticket?.codigo || 'pasaje'}`,
  removeAfterPrint: true,
})
const imprimir = () => handlePrint()

const metodosPago = [
  { clave: 'cash', etiqueta: 'Efectivo' },
  { clave: 'yape', etiqueta: 'Yape' },
  { clave: 'plin', etiqueta: 'Plin' },
  { clave: 'card', etiqueta: 'Tarjeta' },
]
const metodoPagoLabel = computed(() => metodosPago.find(x => x.clave === props.ticket?.metodo_pago)?.etiqueta || '—')
const telefonoPasajero = computed(() => (props.ticket?.pasajero_telefono || props.ticket?.telefono || props.ticket?.pasajero?.telefono || '').toString().trim())

// Paquetes
const paquetes      = computed(() => props.ticket?.paquetes || [])
const totalPaquetes = computed(() => paquetes.value.reduce((sum, pkg) => sum + parseFloat(pkg.precio_adicional || 0), 0))
const totalGeneral  = computed(() => parseFloat(props.ticket?.precio || 0) + totalPaquetes.value)

const ciudadOrigen  = computed(() => props.ticket?.ruta_descripcion?.split('→')[0]?.trim() || '')
const ciudadDestino = computed(() => props.ticket?.ruta_descripcion?.split('→')[1]?.trim() || '')
const ahora = computed(() => new Date().toLocaleString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }))
const formatearFechaHora = (f) => f ? new Date(f).toLocaleString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'
const claseEstado    = (e) => ({ emitido: 't-emitido', embarcado: 't-embarcado', anulado: 't-anulado' }[e] || 't-emitido')
const etiquetaEstado = (e) => ({ emitido: 'EMITIDO', embarcado: 'EMBARCADO', anulado: 'ANULADO' }[e] || e)
</script>

<style scoped>
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
.ticket-dato-fila--sub { font-size: 10px; color: #555; padding-left: 8px; }
.ticket-dato-key { color: #4a5460; flex-shrink: 0; }
.ticket-dato-val { font-weight: bold; color: #000; text-align: right; word-break: break-word; }
.ticket-mono { font-family: monospace; }
.ticket-paquete { margin-bottom: 2px; }
.ticket-paquete-precio { color: #ea580c; }
.ticket-total-paquetes { margin-top: 6px; padding-top: 5px; border-top: 1px solid #e2e8f0; font-weight: 800; color: #ea580c; }
.ticket-asiento-box { display: flex; margin: 10px 15px; border: 1.5px solid #000; border-radius: 8px; overflow: hidden; }
.asiento-col { flex: 1; padding: 10px 5px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.col-izq { border-right: 1.5px solid #000; background: #f8fafc; }
.asiento-label { font-size: 9px; font-weight: 800; color: #000; margin-bottom: 2px; }
.asiento-num { font-size: 26px; font-weight: 900; color: #1d4ed8; line-height: 1; }
.asiento-monto { font-size: 18px; font-weight: 900; color: #000; line-height: 1; }
.asiento-monto--paquete { font-size: 14px; color: #ea580c; }
.asiento-monto--total { font-size: 20px; color: #000; }
.ticket-estado-wrapper { text-align: center; padding: 10px; }
.ticket-estado-badge { padding: 3px 12px; border-radius: 99px; font-size: 9px; font-weight: 800; border: 1.5px solid currentColor; display: inline-block; }
.t-emitido { color: #1d4ed8; }
.t-embarcado { color: #16a34a; }
.t-anulado { color: #dc2626; }
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
  .asiento-col { border-color: #000 !important; }
  .asiento-num, .asiento-monto { color: black !important; }
  .ticket-paquete-precio, .asiento-monto--paquete { color: #ea580c !important; -webkit-print-color-adjust: exact; }
}
</style>