<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="brand">
        <span class="logo-dot" />
        <h1>Crypturity Intelligence</h1>
      </div>
      <p class="subtitle">Verifica wallets y gestiona el riesgo en segundos</p>
    </header>
    <main class="app-main">
      <RouterView />
    </main>
    <footer class="app-footer">
      <small>Dataset consolidado OFAC · TRM Labs · Chainabuse</small>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>
