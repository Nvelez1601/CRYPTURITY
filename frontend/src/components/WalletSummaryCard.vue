<template>
  <section class="summary">
    <header class="summary__header">
      <span class="summary__label">Resultado</span>
      <h2>{{ address }}</h2>
      <RiskIndicator
        :score="summary.risk_score_numeric ?? summary.risk_level_numeric"
        :level="summary.risk_level ?? 'DESCONOCIDO'"
      />
      <p class="summary__networks">Redes detectadas: {{ networksLabel }}</p>
    </header>

    <dl class="summary__facts">
      <div class="summary__fact">
        <dt>Riesgo consolidado</dt>
        <dd>{{ summary.risk_level ?? 'Sin clasificar' }} · Índice {{ summary.risk_level_numeric }}</dd>
      </div>
      <div class="summary__fact">
        <dt>Primer avistamiento</dt>
        <dd>{{ summary.first_seen ?? 'Desconocido' }}</dd>
      </div>
      <div class="summary__fact">
        <dt>Último reporte</dt>
        <dd>{{ summary.last_seen ?? 'Desconocido' }}</dd>
      </div>
      <div class="summary__fact">
        <dt>Categorías detectadas</dt>
        <dd>{{ summary.scam_categories.length ? summary.scam_categories.join(', ') : 'Sin categorías asociadas' }}</dd>
      </div>
      <div class="summary__fact">
        <dt>Dominios vinculados</dt>
        <dd>{{ summary.domains.length ? summary.domains.join(', ') : 'Sin dominios registrados' }}</dd>
      </div>
    </dl>

    <section class="summary__sources" v-if="summary.sources.length">
      <h3>Fuentes de inteligencia</h3>
      <ul>
        <li v-for="source in summary.sources" :key="source.source + (source.detail ?? '')">
          <strong>{{ source.source }}</strong>
          <span v-if="source.risk_level"> · {{ source.risk_level }}</span>
          <span v-if="source.detail"> — {{ source.detail }}</span>
        </li>
      </ul>
    </section>

    <footer class="summary__footer">
      <div class="summary__score">
        <span>Score TRM normalizado</span>
        <strong>{{ displayScore }}</strong>
      </div>
    </footer>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import RiskIndicator from '@/components/RiskIndicator.vue';
import type { WalletSummary } from '@/types/wallet';

const props = defineProps<{
  summary: WalletSummary;
  address: string;
}>();

const networksLabel = computed(() => props.summary.networks.join(' · '));
const displayScore = computed(() => {
  if (props.summary.risk_score_numeric == null) {
    return 'N/D';
  }
  return props.summary.risk_score_numeric.toString();
});
</script>

<style scoped>
.summary {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.summary__header .summary__label {
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.summary__header h2 {
  margin: 0.35rem 0 0;
  font-size: 1.1rem;
  word-break: break-all;
}

.summary__networks {
  margin: 0.65rem 0 0;
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

.summary__facts {
  display: grid;
  gap: 1.1rem;
}

.summary__fact dt {
  color: var(--color-text-muted);
  font-size: 0.8rem;
  margin-bottom: 0.2rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.summary__fact dd {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.5;
}

.summary__sources {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(245, 166, 35, 0.2);
}

.summary__sources h3 {
  margin: 0 0 0.75rem;
  font-size: 0.95rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}

.summary__sources ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.6rem;
  font-size: 0.9rem;
}

.summary__sources li strong {
  color: var(--color-text);
}

.summary__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.summary__score span {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--color-text-muted);
  letter-spacing: 0.08em;
}

.summary__score strong {
  font-size: 2.3rem;
  color: var(--color-accent);
  line-height: 1;
}
</style>
