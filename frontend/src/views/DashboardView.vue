<template>
  <section class="dashboard">
    <div class="dashboard__grid">
      <article class="dashboard__panel dashboard__panel--form">
        <WalletLookupForm @lookup="handleLookup" :loading="loading" />
      </article>
      <article class="dashboard__panel dashboard__panel--result">
        <WalletSummaryCard
          v-if="summary"
          :summary="summary"
          :address="currentAddress"
          :metadata="metadata"
        />
        <template v-else>
          <div v-if="errorMessage" class="dashboard__error">{{ errorMessage }}</div>
          <EmptyState v-else />
        </template>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useWalletStore } from '@/store/walletStore';
import WalletLookupForm from '@/components/WalletLookupForm.vue';
import WalletSummaryCard from '@/components/WalletSummaryCard.vue';
import EmptyState from '@/components/EmptyState.vue';

const store = useWalletStore();
const loading = ref(false);
const { summary, lastQuery, errorMessage, metadata } = storeToRefs(store);
const currentAddress = computed(() => lastQuery.value ?? '');

onMounted(() => {
  if (!metadata.value) {
    store.loadMetadata();
  }
});

const handleLookup = async (address: string) => {
  loading.value = true;
  try {
    await store.verifyWallet(address);
  } catch (error) {
    // El store ya gestiona el mensaje de error.
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.dashboard {
  width: 100%;
  max-width: var(--max-content-width);
}

.dashboard__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
}

.dashboard__panel {
  background: var(--color-surface);
  border-radius: 24px;
  padding: 1.75rem;
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(245, 166, 35, 0.12);
}

.dashboard__panel--result {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.dashboard__error {
  padding: 1rem 1.2rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 77, 79, 0.4);
  background: rgba(255, 77, 79, 0.12);
  color: #ffb3b3;
  font-size: 0.95rem;
  text-align: center;
}

@media (max-width: 1024px) {
  .dashboard__grid {
    grid-template-columns: 1fr;
  }
}
</style>
