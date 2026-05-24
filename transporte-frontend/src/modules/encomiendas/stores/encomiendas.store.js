import { defineStore } from "pinia";
import { ref } from "vue";
import { encomiendasService } from "../services/encomiendas.service";

export const useEncomiendasStore = defineStore("encomiendas", () => {
  const encomiendas = ref([]);
  const viajes = ref([]);
  const cargando = ref(false);
  const error = ref(null);
  const total = ref(0); // ← ref, no "total: 0"

  async function cargarEncomiendas(params = {}) {
    cargando.value = true; // ← .value, no this.
    try {
      const { data } = await encomiendasService.obtenerEncomiendas(params);
      encomiendas.value = data.results ?? data;
      total.value = data.count ?? data.length;
    } catch (e) {
      error.value = "Error al cargar encomiendas";
    } finally {
      cargando.value = false;
    }
  }

  async function cargarViajes(params = {}) {
    try {
      const { data } = await encomiendasService.buscarViajes({
        estado: "programado",
        ...params,
      });
      viajes.value = data.results ?? data;
    } catch (e) {
      error.value = "Error al cargar viajes";
    }
  }

  return {
    encomiendas,
    viajes,
    cargando,
    error,
    total, // ← exportar total
    cargarEncomiendas,
    cargarViajes,
  };
});
