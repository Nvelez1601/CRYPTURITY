<template>
  <form class="lookup" @submit.prevent="submit">
    <header class="lookup__header">
      <h2>Analiza una wallet</h2>
      <p>Ingresa una dirección BTC o EVM para evaluar el riesgo consolidado.</p>
    </header>
    <label class="lookup__field">
      <span>Dirección de wallet</span>
      <div class="lookup__input-wrapper" :data-loading="loading">
        <input
          v-model.trim="address"
          type="text"
          placeholder="0x47ce0c6ac56edb84e2ad330bec0b500ad6e71bee"
          autocomplete="off"
          spellcheck="false"
          :disabled="loading"
          required
        />
        <button class="lookup__submit" type="submit" :disabled="loading || !address">
          <span v-if="!loading">Verificar</span>
          <span v-else class="loader" aria-hidden="true"></span>
        </button>
      </div>
    </label>
    <footer class="lookup__footer">
      <small>
        Tus consultas no se almacenan. Dataset actualizado: {{ metadataSummary?.records ?? 'n/a' }} registros.
      </small>
    </footer>
  </form>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useWalletStore } from '@/store/walletStore';

const props = defineProps<{ loading: boolean }>();
const loading = computed(() => props.loading);
const emit = defineEmits<{ lookup: [address: string] }>();

const store = useWalletStore();
const { lastQuery, metadata } = storeToRefs(store);
const address = ref(lastQuery.value ?? '');
const metadataSummary = computed(() => metadata.value);

watch(lastQuery, (value) => {
  address.value = value ?? '';
});

const submit = () => {
  if (!address.value) {
    return;
  }
  emit('lookup', address.value);
};
</script>

<style scoped>
.lookup {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.lookup__header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.lookup__header p {
  margin: 0.35rem 0 0;
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.lookup__field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.lookup__field span {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-muted);
}

.lookup__input-wrapper {
  display: flex;
  align-items: stretch;
  background: var(--color-surface-elevated);
  border-radius: 16px;
  padding: 0.35rem;
  border: 1px solid transparent;
  transition: border-color 0.2s ease;
}

.lookup__input-wrapper:focus-within {
  border-color: rgba(245, 166, 35, 0.4);
  box-shadow: 0 0 0 2px rgba(245, 166, 35, 0.1);
}

.lookup__input-wrapper input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--color-text);
  font-size: 1rem;
  padding: 0.75rem 1rem;
}

.lookup__input-wrapper input:disabled {
  opacity: 0.5;
}

.lookup__submit {
  border: none;
  border-radius: 12px;
  margin-left: 0.5rem;
  padding: 0 1.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-dark));
  color: #101010;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: filter 0.2s ease, transform 0.2s ease;
}

.lookup__submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.lookup__submit:not(:disabled):hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}

.loader {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  border: 2px solid rgba(0, 0, 0, 0.15);
  border-top-color: rgba(0, 0, 0, 0.65);
  animation: spin 0.8s linear infinite;
}

.lookup__footer {
  color: var(--color-text-muted);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
