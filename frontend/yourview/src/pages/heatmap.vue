<template>
  <div class="page-wrapper">
    <!-- Header -->
    <Header />

    <!-- Page content -->
    <main class="heatmap-main">
      <section class="intro-text">
        <div class="content-wrapper">
          <div class="text-content">
            <h2>Urban Trees, Cooler Cities</h2>
            <p>
              Cities get hot because concrete and roads soak up the sun. Trees give shade
              and act like nature’s air-conditioners, making neighborhoods up to 4° cooler.
            </p>
            <div class="address-search">
              <input type="text" placeholder="Enter your address" ref="autocompleteInput" />
              <button @click="onSuburbSelected">Show My Suburb</button>
            </div>
          </div>
          <div class="image-content">
            <img src="@/assets/UHI_Illustration.png" alt="Urban Heat Island Illustration" />
          </div>
        </div>
      </section>

      <!-- Heatmap Section -->
      <section class="heatmap-section">
        <h2>Melbourne’s Heat Map</h2>
        <div class="heatmap-placeholder">
          <iframe 
            src="/kepler_heatmap.gl.html#10/-37.8136/144.9631"
            width="100%" 
            height="100%" 
            frameborder="0" 
            style="border-radius: 8px;">
          </iframe>
        </div>

        <!-- Insights Section: Hidden until suburb selected -->
        <div v-if="suburbSelected" class="insights-section">
          <h3>Insights for {{ suburbName }}</h3>
          <div class="insights-table">
            <div class="insight-header">🌡️ Temperature Difference</div>
            <div class="insight-header">☀️ Very Hot Days</div>
            <div class="insight-header">🌿 Ozone Levels</div>
            <div class="insight-header">📈 Warming Rates</div>
          </div>
          <div class="suburb-highlight">
            <div class="highlight-item">
              <div class="highlight-number accent-teal">2.5°F</div>
              <div class="highlight-text">warmer than rural</div>
            </div>
            <div class="highlight-item">
              <div class="highlight-number accent-orange">5 MORE</div>
              <div class="highlight-text">very hot days</div>
            </div>
            <div class="highlight-item">
              <div class="highlight-number accent-teal">+3 ppb</div>
              <div class="highlight-text">ozone higher</div>
            </div>
            <div class="highlight-item">
              <div class="highlight-number accent-orange">0.2°F</div>
              <div class="highlight-text">per decade higher</div>
            </div>
          </div>
        </div>
      </section>

      <!--
      <section class="bg-section bg1"></section>
      <section class="bg-section bg2"></section>
      <section class="bg-section bg3"></section>
      -->
      <section class="melbourne-city-section"></section>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { onMounted, ref } from 'vue'

const autocompleteInput = ref(null)

onMounted(() => {
  if (window.google && window.google.maps && window.google.maps.places && autocompleteInput.value) {
    new window.google.maps.places.Autocomplete(autocompleteInput.value, {
      componentRestrictions: { country: 'au' }
    })
  }
})

const suburbSelected = ref(false)
const suburbName = ref('')
const insights = ref({
  temperatureDifference: "—",
  hotDays: "—",
  ozone: "—",
  warmingRate: "—"
})

function getRandomFloat(min, max, decimals = 1) {
  const factor = Math.pow(10, decimals)
  return Math.round((Math.random() * (max - min) + min) * factor) / factor
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function onSuburbSelected() {
  suburbSelected.value = true
  suburbName.value = autocompleteInput.value.value || "Selected Suburb"

  const temperatureDifference = getRandomFloat(1.5, 4.0, 1)
  const hotDays = getRandomInt(2, 10)
  const ozone = getRandomInt(1, 5)
  const warmingRate = getRandomFloat(0.1, 0.4, 1)

  insights.value = {
    temperatureDifference: `${temperatureDifference}°F warmer than rural`,
    hotDays: `${hotDays} more very hot days`,
    ozone: `Ozone higher by +${ozone} ppb`,
    warmingRate: `${warmingRate}°F per decade higher`
  }
}
</script>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.heatmap-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.bg-section {
  flex: 1;
  min-height: 100vh;
  background-size: cover;
  background-position: center;
}

.bg1 {
  background-image: url('@/assets/heatmapbg1.png');
}

.bg2 {
  background-image: url('@/assets/heatmapbg2.png');
}

.bg3 {
  background-image: url('@/assets/heatmapbg3.png');
}

.melbourne-city-section {
  height: 250px;
  background-image: url('@/assets/City_Melbourne.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  width: 100%;
}

.intro-text {
  text-align: left;
  padding: 3rem 1rem;
  background: rgba(255, 255, 255, 0.75);
  font-family: 'Arial', sans-serif;
  border-radius: 8px;
  width: 100%;
  box-sizing: border-box;
}

.intro-text h2 {
  color: #00796b;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.intro-text p {
  color: #2e7d32;
  font-size: 1.2rem;
  line-height: 1.6;
  max-width: 700px;
  margin: 0 auto 1.5rem auto;
}

.address-search {
  display: flex;
  max-width: 700px;
  margin: 0 auto;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.address-search input {
  flex: 1 1 auto;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: 2px solid #00796b;
  border-radius: 4px;
  min-width: 0;
}

.address-search button {
  padding: 0.5rem 1.5rem;
  font-size: 1rem;
  background-color: #00796b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  flex: 0 0 auto;
  transition: background-color 0.3s ease;
}

.address-search button:hover {
  background-color: #004d40;
}

.content-wrapper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
  width: 100%;
}

.text-content {
  flex: 1;
  min-width: 300px;
}

.image-content {
  flex: 2;
  min-width: 400px;
}

.image-content img {
  width: 100%;
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: contain;
}

.heatmap-section {
  padding: 3rem 1rem;
  background: #ffffff;
  text-align: center;
  border-radius: 8px;
  margin: 2rem auto;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.heatmap-section h2 {
  font-size: 2rem;
  color: #00796b;
  margin-bottom: 1.5rem;
}

.heatmap-placeholder {
  width: 100%;
  max-width: 100%;
  height: 500px;
  border: 2px dashed #00796b;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #555;
  font-size: 1.2rem;
  background-color: #f9f9f9;
}

.insights-section {
  margin-top: 2.5rem;
  background: #fdf6f0;
  padding: 2rem 2.5rem 3rem 2.5rem;
  border-radius: 12px;
  box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.03);
}

.insights-section h3 {
  color: #b85c3b;
  font-weight: 900;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  letter-spacing: 0.05em;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* New styles for insights table and suburb highlight */

.insights-table {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  background-color: #f5f5f5;
  padding: 1rem 2rem;
  border-radius: 10px 10px 0 0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 700;
  color: #555;
  font-size: 1rem;
  user-select: none;
}

.insight-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  opacity: 0.7;
  font-weight: 600;
  font-size: 1.1rem;
}

/* Reduce emoji size and opacity */
.insight-header > *:first-child {
  font-size: 1.2rem;
  opacity: 0.6;
}

/* Suburb highlight row */

.suburb-highlight {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  background-color: #ffffff;
  padding: 1.8rem 2rem;
  border-radius: 0 0 10px 10px;
  box-shadow: 0 4px 12px rgba(231, 111, 81, 0.15);
  gap: 0 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.highlight-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.highlight-number {
  font-size: 2.8rem;
  font-weight: 900;
  line-height: 1;
  user-select: text;
}

.accent-orange {
  color: #e76f51;
}

.accent-teal {
  color: #00796b;
}

.highlight-text {
  font-size: 0.9rem;
  font-weight: 600;
  color: #555555;
  margin-top: 0.25rem;
  text-transform: lowercase;
  user-select: text;
}
</style>