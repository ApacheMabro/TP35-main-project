<template>
  <div class="grid" style="grid-template-columns: 360px 1fr">
    <!-- On the left: Forms and rating cards -->
    <section class="card" style="padding: 16px">
      <h2 style="margin: 0 0 12px 0; color: var(--green-900)">Green Index — 3·30·300</h2>

      <div class="grid" style="grid-template-columns: 1fr; gap: 12px">
        <!-- 3 trees -->
        <label>
          <div style="margin-bottom: 6px; font-weight: 600">Trees visible from window (count)</div>
          <input class="input" type="number" min="0" v-model.number="trees" />
        </label>

        <!-- 30% Green coverage -->
        <label>
          <div style="margin-bottom: 6px; font-weight: 600">Green cover in neighbourhood (%)</div>
          <input class="input" type="number" min="0" max="100" v-model.number="canopy" />
        </label>

        <!-- 300m Park distance -->
        <label>
          <div style="margin-bottom: 6px; font-weight: 600">Distance to nearest park (m)</div>
          <input class="input" type="number" min="0" v-model.number="distance" />
        </label>

        <div class="grid" style="grid-template-columns: 1fr 1fr">
          <div class="card" style="padding: 12px">
            <div style="font-weight: 700; margin-bottom: 6px">3 Trees</div>
            <span :class="['badge', ok3 ? 'ok' : 'bad']">
              <span v-if="ok3">✅</span><span v-else>❌</span>
              {{ ok3 ? 'Pass' : 'Not met' }}
            </span>
          </div>

          <div class="card" style="padding: 12px">
            <div style="font-weight: 700; margin-bottom: 6px">30% Canopy</div>
            <span :class="['badge', ok30 ? 'ok' : 'bad']">
              <span v-if="ok30">✅</span><span v-else>❌</span>
              {{ ok30 ? 'Pass' : 'Not met' }}
            </span>
          </div>

          <div class="card" style="padding: 12px">
            <div style="font-weight: 700; margin-bottom: 6px">300m to Park</div>
            <span :class="['badge', ok300 ? 'ok' : 'bad']">
              <span v-if="ok300">✅</span><span v-else>❌</span>
              {{ ok300 ? 'Pass' : 'Not met' }}
            </span>
          </div>

          <div class="card" style="padding: 12px">
            <div style="font-weight: 700; margin-bottom: 6px">Overall</div>
            <span :class="['badge', allOk ? 'ok' : 'bad']">
              <span v-if="allOk">✅</span><span v-else>❌</span>
              {{ allOk ? 'Meets 3-30-300' : 'Does not meet' }}
            </span>
          </div>
        </div>

        <div class="grid" style="grid-template-columns: 1fr 1fr">
          <button class="btn" @click="useExample">Use example</button>
          <button class="btn ghost" @click="resetForm">Reset</button>
        </div>

        <p style="font-size: 12px; color: var(--fg-dim); margin: 0">
          Tip: Click the map on the right to set your location. A 300 m circle will be drawn
          automatically.
        </p>
      </div>
    </section>

    <!-- On the right: Map-->
    <section class="card" style="padding: 8px 8px 0 8px">
      <div ref="mapRef" class="map"></div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const trees = ref(0)
const canopy = ref(0) // percent
const distance = ref(400) // meters

const ok3 = ref(false)
const ok30 = ref(false)
const ok300 = ref(false)
const allOk = ref(false)

const mapRef = ref(null)
let map, marker, circle

const DEFAULT_CENTER = [-37.8136, 144.9631] // Melbourne CBD

function recompute() {
  ok3.value = Number(trees.value) >= 3
  ok30.value = Number(canopy.value) >= 30
  ok300.value = Number(distance.value) <= 300
  allOk.value = ok3.value && ok30.value && ok300.value
}

watch([trees, canopy, distance], recompute, { immediate: true })

function useExample() {
  trees.value = 4
  canopy.value = 32
  distance.value = 240
}
function resetForm() {
  trees.value = 0
  canopy.value = 0
  distance.value = 400
}

onMounted(() => {
  map = L.map(mapRef.value, { zoomControl: true }).setView(DEFAULT_CENTER, 15)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap',
  }).addTo(map)

  // Initialize a point and a circle with a radius of 300m
  marker = L.marker(DEFAULT_CENTER).addTo(map)
  circle = L.circle(DEFAULT_CENTER, { radius: 300, color: '#2f6d34' }).addTo(map)

  // Click on the map to set the location, and the "Distance" demonstration will be updated automatically (which can be replaced with the calculation of the actual nearest park distance).
  map.on('click', (e) => {
    const latlng = [e.latlng.lat, e.latlng.lng]
    marker.setLatLng(latlng)
    circle.setLatLng(latlng)

    // Demonstration: Click on the distance (in meters) from the location to the CBD center to simulate "the nearest park"
    const d = map.distance(e.latlng, L.latLng(DEFAULT_CENTER[0], DEFAULT_CENTER[1]))
    distance.value = Math.round(d % 600) // Just for demonstration, avoid making it too valuable
  })
})
</script>

<style scoped>
.map {
  height: calc(100vh - 140px);
  border-radius: 12px;
  overflow: hidden;
}
</style>
