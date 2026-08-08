// printer.service.js
// Conecta con el servidor local de impresión en ws://localhost:8765

const WS_URL = "ws://localhost:8765";

function formatearHora12(fecha) {
  if (!fecha) return "";
  return new Date(fecha).toLocaleString("es-PE", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

function etiquetaPago(clave) {
  return (
    { cash: "Efectivo", yape: "Yape", plin: "Plin", card: "Tarjeta" }[clave] ||
    clave
  );
}

async function enviarImpresion(datos) {
  return new Promise((resolve, reject) => {
    let ws;
    try {
      ws = new WebSocket(WS_URL);
    } catch (e) {
      reject(new Error("No se pudo conectar con la impresora"));
      return;
    }

    const timeout = setTimeout(() => {
      ws.close();
      reject(
        new Error(
          "Tiempo de espera agotado — verifica que el servidor de impresion este corriendo",
        ),
      );
    }, 5000);

    ws.onopen = () => {
      ws.send(JSON.stringify(datos));
    };

    ws.onmessage = (event) => {
      clearTimeout(timeout);
      const respuesta = JSON.parse(event.data);
      ws.close();
      if (respuesta.ok) resolve(respuesta);
      else reject(new Error(respuesta.error || "Error al imprimir"));
    };

    ws.onerror = () => {
      clearTimeout(timeout);
      reject(
        new Error(
          "Servidor de impresion no disponible — abre servidor.py en la PC de caja",
        ),
      );
    };
  });
}

export const printerService = {
  // ── Imprimir ticket de pasaje ─────────────────────────
  async imprimirPasaje(ticket) {
    console.log("vendido_por_nombre:", ticket.vendido_por_nombre);
    console.log("sucursal_nombre:", ticket.sucursal_nombre);
    const paquetes = ticket.paquetes || [];

    // Total = precio pasaje + suma de paquetes
    const totalPaquetes = paquetes.reduce(
      (sum, pkg) => sum + parseFloat(pkg.precio_adicional || 0),
      0,
    );
    const totalGeneral = (
      parseFloat(ticket.precio || 0) + totalPaquetes
    ).toFixed(2);

    const datos = {
      tipo: "pasaje",
      codigo: ticket.codigo,
      // Ruta
      ruta_descripcion: ticket.ruta_descripcion,
      fecha_salida_fmt: formatearHora12(ticket.fecha_salida),
      vehiculo_placa: ticket.vehiculo_placa,
      // Pasajero
      pasajero_nombre: ticket.pasajero_nombre,
      pasajero_dni: ticket.pasajero_dni,
      // Asiento
      asiento: ticket.asiento,
      estado: ticket.estado || "EMITIDO",
      // Pago
      metodo_pago_label: etiquetaPago(ticket.metodo_pago),
      // Vendedor y sucursal
      vendido_por: ticket.vendido_por_nombre || "---",
      sucursal: ticket.sucursal_nombre || "",
      // Precios
      precio_pasaje: parseFloat(ticket.precio || 0).toFixed(2),
      precio_paquetes: totalPaquetes.toFixed(2),
      total_general: totalGeneral,
      // Paquetes
      paquetes: paquetes,
    };
    return await enviarImpresion(datos);
  },

  // ── Imprimir ticket de encomienda ─────────────────────
  async imprimirEncomienda(enc) {
    const datos = {
      tipo: "encomienda",
      codigo: enc.codigo,
      viaje_descripcion: enc.viaje_descripcion || "Sin viaje asignado",
      remitente_nombre: enc.remitente_nombre,
      remitente_dni: enc.remitente_dni,
      remitente_telefono: enc.remitente_telefono || "",
      destinatario_nombre: enc.destinatario_nombre,
      destinatario_dni: enc.destinatario_dni,
      destinatario_telefono: enc.destinatario_telefono || "",
      descripcion: enc.descripcion,
      peso_kg: enc.peso_kg || null,
      precio: parseFloat(enc.precio || 0).toFixed(2),
      metodo_pago_label: etiquetaPago(enc.metodo_pago),
      sucursal: enc.sucursal_nombre || "",
    };
    return await enviarImpresion(datos);
  },

  // ── Verificar conexión ────────────────────────────────
  async verificarConexion() {
    return new Promise((resolve) => {
      let ws;
      try {
        ws = new WebSocket(WS_URL);
      } catch {
        resolve(false);
        return;
      }
      const timeout = setTimeout(() => {
        ws.close();
        resolve(false);
      }, 3000);
      ws.onopen = () => {
        clearTimeout(timeout);
        ws.close();
        resolve(true);
      };
      ws.onerror = () => {
        clearTimeout(timeout);
        resolve(false);
      };
    });
  },
};
