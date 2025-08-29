<!-- src/pages/YourAreaPage.vue -->
<template>
  <div class="area-page">
    <!-- Top introduction section -->
    <div class="intro-section">
      <!-- Left text -->
      <div class="intro-text">
        <h1>Heat Pocket Island</h1>
        <p>
          Urban areas are usually warmer than their rural surroundings, creating what is known as the
          'urban heat island effect'. As cities continue to grow, vegetation is lost and surfaces are
          paved or covered with buildings, which absorb and radiate heat.
        </p>
      </div>

      <!-- Right images -->
      <div class="intro-images">
        <img src="@/assets/background5.png" alt="Heat Map Example 1" />
        <img src="@/assets/background6.png" alt="Heat Map Example 2" />
      </div>
    </div>

    <!-- Map section below -->
    <div class="map-wrapper">
      <div class="toolbar">
        <h2>Urban Heat Map - Melbourne</h2>

        <!-- Controls: search (with autocomplete) + demo toggles -->
        <div class="controls">
          <!-- Search box + suggestions dropdown -->
          <div class="search-wrap">
            <input
              v-model="searchQuery"
              class="search-box"
              type="text"
              placeholder="Search location (e.g. 'Federation Square, Melbourne')"
              @keyup.enter="searchLocation"
              @input="onSearchInput"
              @keydown.down.prevent="moveActive(1)"
              @keydown.up.prevent="moveActive(-1)"
              @keydown.enter.prevent="chooseActive"
            />
            <ul v-if="showDropdown" class="suggestions">
              <li
                v-for="(s, i) in suggestions"
                :key="s.place_id || s.osm_id || i"
                :class="['sug-item', { active: i === activeIndex }]"
                @mousedown.prevent="pickSuggestion(s)"
                @mouseenter="activeIndex = i"
              >
                {{ s.display_name }}
              </li>
              <li v-if="!suggestions.length" class="sug-empty">No results</li>
            </ul>
          </div>

          <button class="btn" @click="searchLocation" :disabled="searching">
            {{ searching ? 'Searching...' : 'Search' }}
          </button>

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

/** Leaflet map refs */
const mapRef = ref(null)
let map, heat, searchMarker

/** Search state */
const searchQuery = ref('')
const searching = ref(false)
const suggestions = ref([])
const showDropdown = ref(false)
const activeIndex = ref(-1)
let debounceId = null

/** Default center: Melbourne CBD */
const DEFAULT_CENTER = [-37.8136, 144.9631]

/** Demo heat points loader */
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

/** Search via Nominatim (when pressing Search button or Enter) */
async function searchLocation() {
  const q = searchQuery.value.trim()
  if (!q) return
  searching.value = true
  try {
    const url = `https://nominatim.openstreetmap.org/search?format=json&limit=1&addressdetails=1&q=${encodeURIComponent(
      q
    )}`
    const res = await fetch(url, { headers: { Accept: 'application/json' } })
    const data = await res.json()
    if (!Array.isArray(data) || !data.length) {
      alert('No results found.')
      return
    }
    const { lat, lon, display_name } = data[0]
    goToCoords(parseFloat(lat), parseFloat(lon), display_name)
  } catch (e) {
    console.error(e)
    alert('Search failed. Please try again.')
  } finally {
    searching.value = false
  }
}

/** Debounced input to fetch autocomplete suggestions */
function onSearchInput() {
  const q = searchQuery.value.trim()
  if (!q) {
    suggestions.value = []
    showDropdown.value = false
    activeIndex.value = -1
    return
  }
  if (debounceId) clearTimeout(debounceId)
  debounceId = setTimeout(fetchSuggestions, 250)
}

/** Fetch top-5 suggestions from Nominatim */
async function fetchSuggestions() {
  const q = searchQuery.value.trim()
  if (!q) return
  try {
    const url = `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=5&q=${encodeURIComponent(
      q
    )}`
    const res = await fetch(url, { headers: { Accept: 'application/json' } })
    const data = await res.json()
    suggestions.value = Array.isArray(data) ? data : []
    showDropdown.value = true
    activeIndex.value = suggestions.value.length ? 0 : -1
  } catch {
    suggestions.value = []
    showDropdown.value = true
    activeIndex.value = -1
  }
}

/** Pick a suggestion from dropdown */
function pickSuggestion(s) {
  searchQuery.value = s.display_name || ''
  showDropdown.value = false
  goToCoords(parseFloat(s.lat), parseFloat(s.lon), s.display_name)
}

/** Keyboard navigation on dropdown */
function moveActive(delta) {
  if (!showDropdown.value || !suggestions.value.length) return
  const n = suggestions.value.length
  activeIndex.value = (activeIndex.value + delta + n) % n
}
function chooseActive() {
  if (!showDropdown.value || activeIndex.value < 0) return
  const s = suggestions.value[activeIndex.value]
  pickSuggestion(s)
}

/** Move map + drop/update a single marker and popup */
function goToCoords(lat, lon, name = '') {
  const coords = [lat, lon]
  map.setView(coords, 15, { animate: true })
  if (!searchMarker) {
    searchMarker = L.marker(coords, { title: name }).addTo(map)
  } else {
    searchMarker.setLatLng(coords)
  }
  if (name) searchMarker.bindPopup(`<b>${name}</b>`).openPopup()
  showDropdown.value = false
}

/** Init Leaflet */
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

.intro-text { flex: 1; }
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
  border-radius: 0;
}

/* Map section (centered, custom width/height) */
.map-wrapper {
  height: 75vh;
  width: 85vw;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

/* Toolbar and controls */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px 12px;
}
.controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Search input + suggestions dropdown */
.search-wrap { position: relative; }
.search-box {
  height: 34px;
  padding: 0 10px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  outline: none;
  min-width: 280px;
}
.search-box:focus {
  border-color: #93c5fd;
  box-shadow: 0 0 0 3px rgba(59,130,246,.18);
}
.suggestions {
  position: absolute;
  top: calc(100% + 6px);
  left: 0; right: 0;
  z-index: 5000;
  margin: 0; padding: 6px 0;
  list-style: none;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 12px 30px rgba(0,0,0,.12);
  max-height: 280px;
  overflow: auto;
}
.sug-item {
  padding: 10px 12px;
  cursor: pointer;
  font-size: 14px;
  color: #111827;
}
.sug-item:hover,
.sug-item.active { background: #f3f4f6; }
.sug-empty { padding: 10px 12px; color: #6b7280; font-size: 13px; }

/* Map container */
.map {
  flex: 1;
  border-radius: 12px;
  overflow: hidden;
}
</style>



