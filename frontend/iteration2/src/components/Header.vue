<template>
  <header class="site-header" :class="{ 'is-open': mobileOpen }">
    <div class="wrap">
      <!-- Logo -->
      <router-link to="/landing" class="brand" aria-label="Go to Landing Page">
        <img :src="logo" alt="YourView logo" class="logo-img" />
      </router-link>

      <!-- Desktop nav -->
      <nav class="nav desktop" aria-label="Primary">
        <router-link to="/upload_window" class="nav-link" active-class="active">Upload My Window</router-link>
        <router-link to="/heatmap" class="nav-link" active-class="active">Suburb Heat</router-link>
        <router-link to="/plant_health" class="nav-link" active-class="active">Plant Health</router-link>
        <router-link to="/gallery" class="nav-link" active-class="active">Window Gallery</router-link>
      </nav>

      <!-- Mobile menu button -->
      <button
        class="menu-btn"
        :aria-expanded="mobileOpen ? 'true' : 'false'"
        aria-controls="mobile-menu"
        @click="toggle()"
      >
        <span class="sr-only">Toggle menu</span>
        <span class="bar"></span><span class="bar"></span><span class="bar"></span>
      </button>
    </div>

    <!-- Mobile drawer -->
    <nav id="mobile-menu" class="nav mobile" aria-label="Primary Mobile" v-if="mobileOpen">
      <router-link @click="close()" to="/upload_window" class="nav-link" active-class="active">Upload My Window</router-link>
      <router-link @click="close()" to="/heatmap" class="nav-link" active-class="active">Suburb Heat</router-link>
      <router-link @click="close()" to="/plant_health" class="nav-link" active-class="active">Plant Health</router-link>
      <router-link @click="close()" to="/gallery" class="nav-link" active-class="active">Window Gallery</router-link>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
const mobileOpen = ref(false)
const toggle = () => (mobileOpen.value = !mobileOpen.value)
const close = () => (mobileOpen.value = false)

// Close on ESC
const onKey = (e) => { if (e.key === 'Escape') mobileOpen.value = false }
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))

import logo from '@/assets/logo.png'
</script>

<style scoped>
/* Header */
.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: #103731;           /* dark green background */
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.wrap {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
}

/* Logo/brand */
.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  letter-spacing: .2px;
  text-decoration: none;
  color: #ffffff;                /* white text */
}

.logo-img {
  height: 60px;
  width: auto;
  display: block;
}

/* Desktop nav links */
.nav {
  display: flex;
  gap: 16px;
}

.nav-link {
  padding: 8px 10px;
  border-radius: 8px;
  text-decoration: none;
  color: #ffffff;                /* inactive text white */
  font-weight: 500;
  transition: background 0.18s ease, box-shadow 0.18s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* Active tab styling */
.active {
  background: #ffffff;            /* active page box */
  color: #103731;                 /* active text dark green */
  border: 1px solid #ffffff;
}

/* Mobile menu button */
.menu-btn {
  display: none;
  position: relative;
  width: 42px;
  height: 36px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: #103731;
}

.menu-btn .bar {
  display: block;
  height: 2px;
  margin: 6px 8px;
  background: #ffffff;
}

/* Mobile drawer */
.nav.mobile {
  display: none;
  flex-direction: column;
  padding: 8px 16px 16px;
}

.is-open .nav.mobile {
  display: flex;
}

/* Responsive switch */
@media (max-width: 840px) {
  .nav.desktop { display: none; }
  .menu-btn { display: inline-block; }
}

/* Screen-reader utility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  white-space: nowrap;
  border: 0;
}
</style>
