<template>
  <div class="area-page">
    <!-- Top introduction area -->
    <div class="intro-section">
      <div class="intro-text">
        <h1>Heat Pocket Island</h1>
        <p>
          Urban areas are usually warmer than their rural surroundings, creating what is known as the
          'urban heat island effect'. As cities continue to grow, vegetation is lost and surfaces are
          paved or covered with buildings, which absorb and radiate heat.
        </p>
      </div>
      <div class="intro-images">
        <img src="@/assets/background5.png" alt="Heat Map Example 1" />
        <img src="@/assets/background6.png" alt="Heat Map Example 2" />
      </div>
    </div>

    <!-- Maps and toolbars -->
    <div class="map-wrapper">
      <div class="toolbar">
        <h2>Urban Heat Map - Melbourne</h2>

        <div class="controls">
          <!-- Search + Auto-completion -->
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
        </div>
      </div>

      <div ref="mapRef" class="map"></div>
<div class="map-footer">
  <div class="map-footer-title">Make Your Area Cooler</div>
  <RouterLink to="/yourvoice">
    <button class="btn-black">Nominate Green Landway 🌳</button>
  </RouterLink>
</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'

// "Through?" Obtain the packaged static resource url through the URL method
import geojsonUrl from '@/assets/sa2_heatmap.geojson?url'

/** Leaflet map refs */
const mapRef = ref(null)
let map, searchMarker

/** Choropleth refs */
let choroplethLayer
let legendControl

/** Search state */
const searchQuery = ref('')
const searching = ref(false)
const suggestions = ref([])
const showDropdown = ref(false)
const activeIndex = ref(-1)
let debounceId = null

/** Default center: Melbourne CBD */
const DEFAULT_CENTER = [-37.8136, 144.9631]

/** Color table (Light -> dark) */
const PALETTE = ['#fee5d9', '#fcbba1', '#fc9272', '#fb6a4a', '#de2d26', '#a50f15']

/** Create isometric grading color codes based on numerical values */
function makeColorScale(values, k = PALETTE.length) {
  const nums = values.filter(v => typeof v === 'number' && !Number.isNaN(v))
  const min = Math.min(...nums)
  const max = Math.max(...nums)
  const step = (max - min) / k
  const breaks = Array.from({ length: k + 1 }, (_, i) => (i === k ? max : min + i * step))
  return {
    breaks,
    colorOf(v) {
      if (v == null || Number.isNaN(v)) return '#ccc'
      for (let i = k - 1; i >= 0; i--) {
        if (v >= breaks[i]) return PALETTE[i]
      }
      return PALETTE[0]
    },
    range: [min, max],
  }
}

/** Hover HighLight */
function highlightFeature(e) {
  const layer = e.target
  layer.setStyle({ weight: 2, color: '#111', fillOpacity: 0.85 })
  layer.bringToFront()
}
function resetHighlight(e) {
  choroplethLayer?.resetStyle(e.target)
}

/** Load and render the SA2 UHI hierarchical shading map */
async function loadUHIChoropleth() {
  try {
    const res = await fetch(geojsonUrl, { headers: { Accept: 'application/json' } })
    const gj = await res.json()

    // Collect numerical values
    const allVals = []
    for (const f of gj.features || []) {
      const v = Number(f?.properties?.uhi_value)
      if (!Number.isNaN(v)) allVals.push(v)
    }
    if (!allVals.length) {
      console.warn('No numeric uhi_value found in GeoJSON.')
      return
    }
    const scale = makeColorScale(allVals)

    // Create a GeoJSON layer (supports Polygon/MultiPolygon)
    choroplethLayer = L.geoJSON(gj, {
      style: feat => {
        const v = Number(feat?.properties?.uhi_value)
        return {
          weight: 1,
          color: '#555',
          opacity: 0.8,
          fillOpacity: 0.7,
          fillColor: scale.colorOf(v),
        }
      },
      onEachFeature: (feat, layer) => {
        const p = feat.properties || {}
        const name = p.sa2_name21 ?? 'Unknown SA2'
        const code = p.sa2_code21 ?? '-'
        const uhi = (p.uhi_value ?? '—')
        layer.bindPopup(
          `<div style="min-width:220px">
             <div style="font-weight:700;margin-bottom:4px">${name}</div>
             <div>SA2 Code: ${code}</div>
             <div>UHI Value: <b>${uhi}</b></div>
           </div>`
        )
        layer.on({
          mouseover: highlightFeature,
          mouseout: resetHighlight,
          click: e => layer.openPopup(e.latlng),
        })
      },
    }).addTo(map)

    // Click on the block to automatically scale
    choroplethLayer.on('click', e => {
      if (e.layer && e.layer.getBounds) {
        map.fitBounds(e.layer.getBounds(), { maxZoom: 14, animate: true })
      }
    })

    // Add a legend
    addLegend(scale)
  } catch (err) {
    console.error('Failed to load choropleth:', err)
    alert('The UHI heatmap failed to load. Please check if the assets/sa2_heatmap.geojson exists and is in the correct format.')
  }
}

/** Legend Control */
function addLegend(scale) {
  // First, remove the old legend
  if (legendControl) map.removeControl(legendControl)

  const { breaks, range } = scale
  legendControl = L.control({ position: 'bottomright' })
  legendControl.onAdd = function () {
    const div = L.DomUtil.create('div', 'info legend')
    div.style.background = 'white'
    div.style.padding = '8px 10px'
    div.style.borderRadius = '8px'
    div.style.boxShadow = '0 6px 20px rgba(0,0,0,.12)'
    div.style.fontSize = '12px'
    div.innerHTML = `<div style="font-weight:700;margin-bottom:6px">UHI Value</div>`
    for (let i = 0; i < PALETTE.length; i++) {
      const from = breaks[i]
      const to = breaks[i + 1]
      const label = (i === PALETTE.length - 1)
        ? `${from.toFixed(2)}+`
        : `${from.toFixed(2)} – ${to.toFixed(2)}`
      div.innerHTML += `
        <div style="display:flex;align-items:center;margin:4px 0;">
          <i style="width:16px;height:12px;background:${PALETTE[i]};display:inline-block;margin-right:8px;border:1px solid #999"></i>
          <span>${label}</span>
        </div>`
    }
    div.innerHTML += `<div style="margin-top:6px;color:#6b7280">min: ${range[0].toFixed(2)} · max: ${range[1].toFixed(2)}</div>`
    return div
  }
  legendControl.addTo(map)
}

/** Search */
async function searchLocation() {
  const q = searchQuery.value.trim()
  if (!q) return
  searching.value = true
  try {
    const url = `https://nominatim.openstreetmap.org/search?format=json&limit=1&addressdetails=1&q=${encodeURIComponent(q)}`
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

/** Auto-completion (anti-shake) */
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
async function fetchSuggestions() {
  const q = searchQuery.value.trim()
  if (!q) return
  try {
    const url = `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=5&q=${encodeURIComponent(q)}`
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
function pickSuggestion(s) {
  searchQuery.value = s.display_name || ''
  showDropdown.value = false
  goToCoords(parseFloat(s.lat), parseFloat(s.lon), s.display_name)
}
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

/** The map locates the coordinates and places/updates individual markers */
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

/** Initialize the Leaflet map and load the heat map */
onMounted(() => {
  const BOUNDS = L.latLngBounds(
    L.latLng(-38.3, 144.4), // SW
    L.latLng(-37.4, 145.7)  // NE
  )

  map = L.map(mapRef.value, {
    center: DEFAULT_CENTER,
    zoom: 13,
    maxBounds: BOUNDS,
    maxBoundsViscosity: 1.0,
    zoomSnap: 0.5,
    zoomDelta: 0.5,
    wheelDebounceTime: 40,
  })

  // Minimum scaling: Just accommodate the boundary, and then expand by 2 stops for a more visually friendly look
  const minFitZoom = map.getBoundsZoom(BOUNDS, true)
  map.setMinZoom(minFitZoom - 2)

  // The initial view fits the boundary
  map.fitBounds(BOUNDS, { animate: false })

  // Base map
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap',
  }).addTo(map)

  // Listen for window changes and dynamically update the minimum scaling
  window.addEventListener('resize', handleResize)

  // === Render a hierarchical shading heatmap using real SA2 polygons and uhi_value ===
  loadUHIChoropleth()
})

function handleResize () {
  if (!map) return
  const BOUNDS = L.latLngBounds(L.latLng(-38.3, 144.4), L.latLng(-37.4, 145.7))
  const minFitZoom = map.getBoundsZoom(BOUNDS, true)
  map.setMinZoom(minFitZoom - 2)
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
.area-page {
  display: flex;
  flex-direction: column;
}

/* Top introduction */
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
  font-weight: 800;
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
  gap: 0;
}
.intro-images img {
  width: 50%;
  height: auto;
  object-fit: cover;
  border-radius: 0;
}

/* Map area */
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
.controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Search input and drop-down */
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

/* Refine the small square of legend (the main style has already been inline in JS, and here it serves as a supplement) */
.leaflet-control .legend i { opacity: .9; }

.map-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}

.map-footer-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #000;
  text-align: center;
}


.btn-black {
  background: #000;
  color: #fff;
  border: 0;
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 0.98rem;
  cursor: pointer;
  transition: background .2s ease, transform .05s ease;
  text-decoration: none;
}
.btn-black:hover { background: #222; }
.btn-black:active { transform: translateY(1px); }

</style>



