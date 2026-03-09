<template>
    <Teleport to="body">
        <Transition name="modal">
            <div v-if="modelValue"
                class="fixed inset-0 z-50 flex items-center justify-center p-4">

                <!-- Fondo -->
                <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"
                    @click="$emit('update:modelValue', false)" />

                <!-- Contenido -->
                <div :class="[
                    'relative bg-white rounded-2xl shadow-xl w-full flex flex-col max-h-[90vh]',
                    anchoClase
                ]">
                    <!-- Header -->
                    <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100 flex-shrink-0">
                        <h3 class="text-sm font-bold text-gray-900">{{ titulo }}</h3>
                        <button @click="$emit('update:modelValue', false)"
                            class="w-7 h-7 rounded-lg hover:bg-gray-100 flex items-center justify-center text-gray-400 hover:text-gray-600 transition-colors">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"
                                    d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>

                    <!-- Body con scroll -->
                    <div class="overflow-y-auto flex-1 px-5 py-4">
                        <slot />
                    </div>

                    <!-- Footer -->
                    <div v-if="$slots.footer"
                        class="flex items-center justify-end gap-2 px-5 py-4 border-t border-gray-100 flex-shrink-0 bg-gray-50/50 rounded-b-2xl">
                        <slot name="footer" />
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    modelValue: { type: Boolean, default: false },
    titulo:     { type: String,  default: '' },
    ancho:      { type: String,  default: 'md' }, // sm | md | lg | xl
})

defineEmits(['update:modelValue'])

const anchoClase = computed(() => ({
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
}[props.ancho] || 'max-w-md'))
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.2s ease;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
    transition: transform 0.2s ease, opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}
.modal-enter-from .relative,
.modal-leave-to .relative {
    transform: scale(0.95) translateY(-8px);
    opacity: 0;
}
</style>