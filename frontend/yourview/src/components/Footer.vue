<template>
  <footer class="footer">
    <div class="footer-inner">
      <!-- Logo -->
      <div class="footer-col">
        <img src="@/assets/logo_only.png" alt="Logo" class="logo" />
      </div>

      <!-- Features -->
      <div class="footer-col">
        <h3>Features</h3>
        <ul>
          <li><RouterLink :to="{ name: 'upload_window' }">Upload My Window</RouterLink></li>
          <li><RouterLink :to="{ name: 'heatmap' }">Suburb Heat</RouterLink></li>
          <li><RouterLink :to="{ name: 'plant_health' }">Plant Health</RouterLink></li>
          <li>
            <a
              href="https://services.melbourne.vic.gov.au/report/treemaintenance"
              target="_blank"
              rel="noopener noreferrer"
            >
              Contact Council
            </a>
          </li>
          <li><RouterLink :to="{ name: 'gallery' }">Window Gallery</RouterLink></li>
        </ul>
      </div>

      <!-- Contact -->
      <div class="footer-col">
        <h3>Contact Us</h3>
        <p>Wellington Road, Clayton<br />Victoria 3800, Australia</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.footer {
  background: #fff;
  border-top: 1px solid #ddd;
  padding: 2rem 1rem;
}

.footer-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 3rem;
}

.footer-col {
  flex: 1;
}

.logo {
  max-width: 60px;
}

h3 {
  font-size: 1rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin-bottom: 0.5rem;
}

a,
.router-link-active,
.router-link-exact-active {
  text-decoration: none;
  color: #111;
}

a:hover,
.router-link-active:hover {
  text-decoration: underline;
}
</style>