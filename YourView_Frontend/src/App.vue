<template>
  <div id="app" class="app">
    <header class="topbar">
      <div class="brand">
  <RouterLink to="/">
    <img :src="logo" alt="Logo" class="logo cursor-pointer" />
  </RouterLink>
</div>


      <nav class="nav">
        <RouterLink to="/about" class="link" active-class="active">About Us</RouterLink>
        <RouterLink to="/YourWindow" class="link" active-class="active">Your Window</RouterLink>
        <RouterLink to="/YourArea" class="link" active-class="active">Your Area</RouterLink>
        <RouterLink to="/YourVoice" class="link" active-class="active">Your Voice</RouterLink>
        <RouterLink to="/greenpage" class="link" active-class="active">Green Index</RouterLink>
        <RouterLink to="/source" class="link" active-class="active">Source</RouterLink>


      </nav>
    </header>

    <main class="main">
      <RouterView />
    </main>

    <footer class="footer">© 2025 TP35 — Melbourne Greening • Theme: Green</footer>
  </div>
</template>

<script setup>
import logo from '@/assets/logo.png'
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background: var(--green-900);
  color: #fff;
}
.brand {
  font-weight: 700;
  letter-spacing: 0.3px;
}
.nav {
  display: flex;
  gap: 12px;
}
.link {
  color: #c8facc;
  text-decoration: none;
  padding: 6px 10px;
  border-radius: 8px;
}
.link:hover {
  background: rgba(255, 255, 255, 0.12);
}
.active {
  background: var(--green-700);
  color: #fff;
}
.main {
  flex: 1;
  padding: 16px;
  background: var(--bg);
}
.footer {
  padding: 12px 16px;
  color: var(--fg-dim);
  background: 0;
}
.logo {
  height: 40px;   /* Change size */
  width: auto;
}
</style>
