<template>
  <div class="empty">
    <div class="empty__badge">Crypturity</div>
    <h3>Tu panel de riesgo</h3>
    <p>
      Consulta una wallet para visualizar el origen de alertas, score consolidado y etiquetas más relevantes.
    </p>
    <ul class="empty__tips">
      <li>Incluye direcciones BTC (legacy, segwit) o EVM (0x...)</li>
      <li>Usa el dataset consolidado con OFAC, TRM Labs y Chainabuse</li>
      <li>Exporta resultados con la API para automatizar flujos AML</li>
    </ul>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.empty {
  text-align: center;
  padding: 2.5rem 1.5rem;
  color: var(--color-text-muted);
}

.empty__badge {
  display: inline-flex;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  background: rgba(245, 166, 35, 0.12);
  border: 1px solid rgba(245, 166, 35, 0.25);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.7rem;
  margin-bottom: 1rem;
}

h3 {
  margin: 0;
  font-size: 1.4rem;
  color: var(--color-text);
}

p {
  margin: 0.75rem auto 1.5rem;
  max-width: 28rem;
  line-height: 1.6;
}

.empty__tips {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.empty__tips li::before {
  content: '•';
  color: var(--color-accent);
  margin-right: 0.4rem;
}
</style>
