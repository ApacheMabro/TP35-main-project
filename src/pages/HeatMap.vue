<template>
  <div class="card" style="padding: 8px">
    <div class="toolbar">
      <h2 style="margin: 0; color: var(--green-900)">Urban Heat Map — Melbourne</h2>
      <div style="display: flex; gap: 8px; align-items: center">
        <button class="btn" @click="loadDemo('day')">Daytime</button>
        <button class="btn ghost" @click="loadDemo('night')">Night</button>
      </div>
    </div>
    <div ref="mapRef" class="map"></div>
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

function loadDemo(mode = 'day') {
  //
  // Day: The CBD is relatively hot, while the area along the Yarra River is lower. Night: Overall intensity decreases
  const pts =
    mode === 'day'
      ? [
          [-37.8136, 144.9631, 0.9],
          [-37.815, 144.965, 0.85],
          [-37.814, 144.97, 0.75],
          [-37.818, 144.97, 0.7],
          [-37.82, 144.965, 0.6],
          [-37.8205, 144.957, 0.55], // It is lower beside Yarra
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
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px 12px;
}
.map {
  height: calc(100vh - 140px);
  border-radius: 12px;
  overflow: hidden;
}
</style>
