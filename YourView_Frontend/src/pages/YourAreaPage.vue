<template>
  <div class="area-page">
    <!-- Top introduction section -->
    <div class="intro-section">
      <!-- Left text -->
      <div class="intro-text">
        <h1>Heat Pocket Island</h1>
        <p>
Urban areas are usually warmer than their rural surroundings, creating what is known as the
'urban heat island effect'. As cities continue to grow,
vegetation is lost and surfaces are paved or covered with buildings, which absorb and radiate heat.
        </p>
      </div>

      <!-- Right images -->
      <div class="intro-images">
        <img src="@/assets/background5.png" alt="Heat Map Example 1" />
        <img src="@/assets/background6.png" alt="Heat Map Example 2" />
      </div>
    </div>

    <!-- Full screen map section -->
    <div class="map-wrapper">
      <div class="toolbar">
        <h2>Urban Heat Map - Melbourne</h2>
        <div style="display: flex; gap: 8px; align-items: center">
          <button class="btn" @click="loadDemo('day')">Daytime</button>
          <button class="btn ghost" @click="loadDemo('night')">Night</button>
        </div>
      </div>
      <div ref="mapRef" class="map"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'

const mapRef = ref(null)
let map, heat

const DEFAULT_CENTER = [-37.8136, 144.9631]

// Load demo heatmap points
function loadDemo(mode = 'day') {
  const pts =
    mode === 'day'
      ? [
          [-37.8136, 144.9631, 0.9],
          [-37.815, 144.965, 0.85],
          [-37.814, 144.97, 0.75],
          [-37.818, 144.97, 0.7],
          [-37.82, 144.965, 0.6],
          [-37.8205, 144.957, 0.55], // beside Yarra River
        ]
      : [
          [-37.8136, 144.9631, 0.6],
          [-37.815, 144.965, 0.58],
          [-37.814, 144.97, 0.52],
          [-37.818, 144.97, 0.5],
          [-37.82, 144.965, 0.42],
          [-37.8205, 144.957, 0.38],
        ]

  const latlngs = pts.map(([lat, lng, intensity]) => [lat, lng, intensity])
  if (!heat) {
    heat = L.heatLayer(latlngs, {
      radius: 28,
      blur: 18,
      maxZoom: 17,
      minOpacity: 0.35,
      max: 1.0,
    }).addTo(map)
  } else {
    heat.setLatLngs(latlngs)
  }
}

onMounted(() => {
  map = L.map(mapRef.value).setView(DEFAULT_CENTER, 14)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap',
  }).addTo(map)

  loadDemo('day')
})
</script>

<style scoped>
.area-page {
  display: flex;
  flex-direction: column;
}

/* Top introduction section */
.intro-section {
  height: 75vh;
  display: flex;
  padding: 2rem;
  gap: 2rem;
  align-items: center;
  background-color: #faffe8;
}

.intro-text {
  flex: 1;
}
.intro-text h1 {
  font-size: 2.8rem;
  font-weight: 800; /* bold title */
  margin-bottom: 1rem;
  color: #2d6a4f;
}
.intro-text p {
  font-size: 1rem;
  line-height: 1.6;
  color: #333;
}

.intro-images {
  flex: 1;
  display: flex;
  gap: 0; /* tight connection */
}
.intro-images img {
  width: 50%;
  height: auto;
  object-fit: cover;
  border-radius: 0px;
}

/* Full screen map section */
.map-wrapper {
  height: 75vh;
  width: 85vw;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px 12px;
}
.map {
  flex: 1;
  border-radius: 12px;
  overflow: hidden;
}
</style>


