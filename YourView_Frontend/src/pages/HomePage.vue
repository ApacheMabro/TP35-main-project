<template>
  <div class="card" style="padding: 24px; text-align: center">
    <h1 style="color: var(--green-900); margin-bottom: 16px">🌳 Welcome to TP35 Main Project</h1>
    <p style="margin-bottom: 24px; color: var(--fg-dim); font-size: 16px">
      Explore Melbourne’s greening levels and urban heat patterns.
    </p>

    <div style="display: flex; justify-content: center; gap: 16px">
      <RouterLink to="/greenpage">
        <button class="btn">Check 3·30·300 Rule</button>
      </RouterLink>
      <RouterLink to="/heat">
        <button class="btn ghost">View Urban Heat Map</button>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
// nothing needed
</script>
