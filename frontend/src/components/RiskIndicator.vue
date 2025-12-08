<template>
  <div class="indicator" :data-risk="riskClass">
    <span class="indicator__pulse" />
    <div class="indicator__meta">
      <strong>{{ displayLabel }}</strong>
      <small>Riesgo {{ level }}</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  score: number;
  level: string;
}>();

const displayLabel = computed(() => {
  const normalized = props.level?.toUpperCase?.() ?? '';
  switch (normalized) {
    case 'CRÍTICO':
      return 'Crítico';
    case 'ALTO':
      return 'Alto';
    case 'MEDIO':
      return 'Moderado';
    case 'BAJO':
      return 'Bajo';
    default:
      if (props.score >= 80) return 'Crítico';
      if (props.score >= 60) return 'Alto';
      if (props.score >= 40) return 'Moderado';
      if (props.score >= 20) return 'Bajo';
      return 'Mínimo';
  }
});

const riskClass = computed(() => {
  const normalized = props.level?.toUpperCase?.();
  if (!normalized) {
    return 'DESCONOCIDO';
  }
  return normalized;
});
</script>

<style scoped>
.indicator {
  display: inline-flex;
  gap: 0.85rem;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 999px;
  background: rgba(245, 166, 35, 0.16);
  border: 1px solid rgba(245, 166, 35, 0.35);
  width: fit-content;
}

.indicator__pulse {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--color-accent);
  box-shadow: 0 0 0 0 rgba(245, 166, 35, 0.6);
  animation: pulse 2s infinite;
}

.indicator__meta strong {
  display: block;
  font-size: 0.9rem;
  letter-spacing: 0.05em;
}

.indicator__meta small {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--color-text-muted);
}

.indicator[data-risk="CRÍTICO"] {
  background: rgba(255, 77, 79, 0.12);
  border-color: rgba(255, 77, 79, 0.45);
}

.indicator[data-risk="CRÍTICO"] .indicator__pulse {
  background: var(--color-danger);
  box-shadow: 0 0 0 0 rgba(255, 77, 79, 0.65);
}

.indicator[data-risk="BAJO"] {
  background: rgba(3, 201, 136, 0.12);
  border-color: rgba(3, 201, 136, 0.35);
}

.indicator[data-risk="BAJO"] .indicator__pulse {
  background: var(--color-success);
  box-shadow: 0 0 0 0 rgba(3, 201, 136, 0.5);
}

.indicator[data-risk="MEDIO"] {
  background: rgba(245, 166, 35, 0.12);
  border-color: rgba(245, 166, 35, 0.35);
}

.indicator[data-risk="ALTO"] {
  background: rgba(245, 166, 35, 0.18);
  border-color: rgba(245, 166, 35, 0.45);
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 166, 35, 0.6);
  }
  70% {
    box-shadow: 0 0 0 12px rgba(245, 166, 35, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 166, 35, 0);
  }
}
</style>
