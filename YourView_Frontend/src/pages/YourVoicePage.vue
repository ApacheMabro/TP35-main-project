<template>

  <div class="view-page">
    <!-- Hero: top half screen -->
    <section class="voice-hero">
      <div class="hero-left">
        <h1>Raise Your Voice</h1>
        <p>
Your voice is important to Melbourne,
you can request directly to the government about your concern of green space in your surrounding,
also you can email to Urban Environmental Department if you see any tree is dying.
Vote for the next green laneway to reduce heat pocket island in our city.
We want to hear from you!
        </p>
      </div>
      <div class="hero-right">
        <img src="@/assets/yourvoice.png" alt="Raise Your Voice" />
      </div>
    </section>

    <!-- Reveal section -->
    <section ref="revealRoot" class="reveal-root">
      <h2 class="reveal item-1">Save your neighbourhood</h2>

      <div class="cards">
        <!-- Left: Nominate form -->
        <div class="card nominate reveal item-2">
          <h3>Nominate The Next Green Laneway</h3>

          <!-- Searchable laneway dropdown (click-to-select only) -->
          <label class="label">Choose a laneway</label>
          <div class="combo" ref="comboRef">
            <!-- Input only filters; does NOT set form.laneway -->
            <input
              class="combo-input"
              type="text"
              v-model="laneSearch"
              placeholder="Type to filter laneways…"
              @focus="laneOpen = true"
              @keydown.enter.prevent
            />
            <div class="selected" v-if="form.laneway">Selected: {{ form.laneway }}</div>

            <ul v-show="laneOpen" class="combo-list">
              <li
                v-for="name in filteredLaneways"
                :key="name"
                class="combo-item"
                @mousedown.prevent="pickLaneway(name)"
              >
                {{ name }}
              </li>
              <li v-if="!filteredLaneways.length" class="combo-empty">No results</li>
            </ul>
          </div>

          <!-- Address with autocomplete -->
          <label class="label">Address (with suggestions)</label>
          <div class="search-wrap" ref="addrWrapRef">
            <input
              v-model="addrQuery"
              class="input"
              type="text"
              placeholder="e.g. 200 Flinders St, Melbourne"
              @input="onAddrInput"
              @keydown.down.prevent="moveActive(1)"
              @keydown.up.prevent="moveActive(-1)"
              @keydown.enter.prevent="chooseActive"
              @focus="openAddrDropdown"
            />
            <ul v-if="showAddrDropdown" class="suggestions">
              <li
                v-for="(s, i) in addrSuggestions"
                :key="s.place_id || s.osm_id || i"
                :class="['sug-item', { active: i === activeIndex }]"
                @mousedown.prevent="pickSuggestion(s)"
                @mouseenter="activeIndex = i"
              >
                {{ s.display_name }}
              </li>
              <li v-if="!addrSuggestions.length" class="sug-empty">No results</li>
            </ul>
          </div>

          <!-- Reason -->
          <label class="label">Why are you nominating this?</label>
          <textarea
            v-model="form.reason"
            class="input textarea"
            rows="4"
            placeholder="Share the reason (e.g., hot pavement, pedestrian traffic, schools nearby)…"
          ></textarea>

          <button class="btn-black" @click="submitNomination">Nominate Green Landway 🌳</button>
        </div>

        <!-- Right: Inform council -->
<div class="card council reveal item-3">
  <h3>Inform Melbourne City Council</h3>
  <p class="muted">“I want more trees outside my window.”</p>
  <p class="muted">“The tree in Collins Street is dying.”</p>
  <p class="muted">“Why is there no tree around Flinders Station?”</p>
  <p class="muted">“Footscray trees are dying.”</p>
  <p class="muted">“I need someone to have a look at Albert Park.”</p>

  <button class="btn-black" @click="goToCouncil">
    Request tree to council
  </button>
</div>

      </div>
    </section>
  </div>

</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

/* ---------------- Form model ---------------- */
const form = ref({
  laneway: '',
  address: '',
  reason: ''
})

/* ---------------- Searchable Laneway (runtime fetch) ---------------- */
// Final options list
const lanewayList = ref([])
// Input text for filtering
const laneSearch = ref('')
// Dropdown state
const laneOpen = ref(false)
// Root element for outside-click
const comboRef = ref(null)

/** Extract 'mapbase_1' from various JSON shapes */
function extractLanewayNames(json) {
  const out = []

  // Case 1: direct array [{ mapbase_1 }]
  if (Array.isArray(json)) {
    for (const r of json) {
      const v = r?.mapbase_1 ?? r?.Mapbase_1 ?? r?.MAPBASE_1
      if (v) out.push(String(v).trim())
    }
  }

  // Case 2: GeoJSON features[].properties.mapbase_1
  if (json?.features && Array.isArray(json.features)) {
    for (const f of json.features) {
      const v =
        f?.properties?.mapbase_1 ??
        f?.properties?.Mapbase_1 ??
        f?.properties?.MAPBASE_1
      if (v) out.push(String(v).trim())
    }
  }

  // Case 3: wrapped in records/data
  const rec = json?.records || json?.data
  if (Array.isArray(rec)) {
    for (const r of rec) {
      const v = r?.mapbase_1 ?? r?.Mapbase_1 ?? r?.MAPBASE_1
      if (v) out.push(String(v).trim())
    }
  }

  // Deduplicate + sort
  return Array.from(new Set(out.filter(Boolean))).sort((a, b) => a.localeCompare(b))
}

/** Load JSON at runtime (robust to size/path) */
async function loadLaneways() {
  try {
    const url = new URL('@/assets/laneways-with-greening-potential.json', import.meta.url).href
    const res = await fetch(url)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const json = await res.json()
    lanewayList.value = extractLanewayNames(json)
  } catch (e) {
    console.error('Failed to load laneways JSON:', e)
    lanewayList.value = []
  }
}

const filteredLaneways = computed(() => {
  const q = laneSearch.value.trim().toLowerCase()
  if (!q) return lanewayList.value
  return lanewayList.value.filter(n => n.toLowerCase().includes(q))
})

function pickLaneway(name) {
  form.value.laneway = name          // only click sets the form value
  laneSearch.value = name            // optionally mirror into input
  laneOpen.value = false
}

/* ---------------- Address Autocomplete (Nominatim) ---------------- */
const addrWrapRef = ref(null)
const addrQuery = ref('')
const addrSuggestions = ref([])
const showAddrDropdown = ref(false)
const activeIndex = ref(-1)
let debounceId = null

// Melbourne bbox (lon,lat): left,top,right,bottom
const VIEWBOX = {
  left: 144.4,
  top: -37.4,
  right: 145.7,
  bottom: -38.5
}

function onAddrInput () {
  const q = addrQuery.value.trim()
  if (!q) {
    addrSuggestions.value = []
    showAddrDropdown.value = false
    activeIndex.value = -1
    return
  }
  if (debounceId) clearTimeout(debounceId)
  debounceId = setTimeout(fetchAddrSuggestions, 250)
}

function openAddrDropdown() {
  if (addrSuggestions.value.length) showAddrDropdown.value = true
}

async function fetchAddrSuggestions () {
  const q = addrQuery.value.trim()
  if (!q) return
  try {
    const url = `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=5&bounded=1&viewbox=${VIEWBOX.left},${VIEWBOX.top},${VIEWBOX.right},${VIEWBOX.bottom}&q=${encodeURIComponent(q)}`
    const res = await fetch(url, { headers: { Accept: 'application/json' } })
    const data = await res.json()
    addrSuggestions.value = Array.isArray(data) ? data : []
    showAddrDropdown.value = true
    activeIndex.value = addrSuggestions.value.length ? 0 : -1
  } catch {
    addrSuggestions.value = []
    showAddrDropdown.value = true
    activeIndex.value = -1
  }
}

function pickSuggestion (s) {
  const name = s.display_name || ''
  form.value.address = name
  addrQuery.value = name
  showAddrDropdown.value = false
}

function moveActive (delta) {
  if (!showAddrDropdown.value || !addrSuggestions.value.length) return
  const n = addrSuggestions.value.length
  activeIndex.value = (activeIndex.value + delta + n) % n
}

function chooseActive () {
  if (!showAddrDropdown.value || activeIndex.value < 0) return
  const s = addrSuggestions.value[activeIndex.value]
  pickSuggestion(s)
}

/* ---------------- Submit ---------------- */
function submitNomination () {
  if (!form.value.laneway || !addrQuery.value || !form.value.reason) {
    alert('Please complete laneway, address, and reason.')
    return
  }
  // TODO: Replace with real POST
  console.log('Nomination submitted:', {
    laneway: form.value.laneway,
    address: addrQuery.value,
    reason: form.value.reason
  })
  alert('Thanks for your nomination!')
  form.value = { laneway: '', address: '', reason: '' }
  laneSearch.value = ''
  addrQuery.value = ''
  addrSuggestions.value = []
  showAddrDropdown.value = false
  activeIndex.value = -1
}

/* ---------------- Council link ---------------- */
function goToCouncil() {
  window.open('https://services.melbourne.vic.gov.au/report/treemaintenance', '_blank')
}

/* ---------------- Scroll reveal (loopable) ---------------- */
const revealRoot = ref(null)
let io = null

function onDocClick(e) {
  if (comboRef.value && !comboRef.value.contains(e.target)) laneOpen.value = false
  if (addrWrapRef.value && !addrWrapRef.value.contains(e.target)) showAddrDropdown.value = false
}

onMounted(() => {
  document.addEventListener('click', onDocClick)
  loadLaneways()

  io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('reveal-in')
        else entry.target.classList.remove('reveal-in')
      })
    },
    { threshold: 0.15, rootMargin: '0px 0px -5% 0px' }
  )
  const targets = revealRoot.value?.querySelectorAll('.reveal') || []
  targets.forEach(el => io.observe(el))
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocClick)
  if (io) io.disconnect()
})
</script>

<style scoped>
.view-page {
  min-height: 100vh;
  background: #FAFFE8;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* Hero (top half screen) */
.voice-hero {
  min-height: 50vh;
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 24px;
  align-items: center;
  padding: 40px 24px;
}

.hero-left h1 {
  font-size: 3rem;
  font-weight: 800;
  margin: 0 0 12px;
  color: #1b4332;
}
.hero-left p {
  font-size: 1.05rem;
  color: #2f3e46;
  margin: 0;
  line-height: 1.6;
}

.hero-right img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Reveal section */
.reveal-root {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
}

.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: all .6s ease;
  will-change: opacity, transform;
}
.reveal.reveal-in {
  opacity: 1;
  transform: translateY(0);
}

/* stagger */
.item-1 { transition-delay: .05s; }
.item-2 { transition-delay: .15s; }
.item-3 { transition-delay: .25s; }

.reveal-root > h2 {
  text-align: center;
  font-size: 2.2rem;
  font-weight: 800;
  color: #2d6a4f;
  margin: 24px 0 28px;
}

/* Two cards */
.card.council {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  text-align: center;
  padding: 20px;
  min-height: 350px;
}

.card.council p {
  font-weight: bold;
  margin: 10px 0;
}

.card.council .btn-black {
  margin-top: 20px;
  align-self: center;
}


.card.council .muted {
  font-weight: bold;
  color: #111;
  margin: 8px 0;
}

.cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.card {
  background: #ffffff;
  border-radius: 14px;
  padding: 18px;
  box-shadow: 0 8px 24px rgba(0,0,0,.08);
}

.card h3 {
  font-weight: bold;
  margin: 0 0 12px;
  font-size: 1.2rem;
  color: #1f2937;
}

/* Labels & Inputs */
.label {
  font-weight: bold;
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin: 12px 0 6px;
}

.input {
  width: 100%;
  box-sizing: border-box;
  height: 38px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 0 10px;
  outline: none;
  background: #fff;
}
.input:focus {
  border-color: #93c5fd;
  box-shadow: 0 0 0 4px rgba(59,130,246,.15);
}

.textarea {
  height: auto;
  padding: 10px;
  resize: vertical;
}

/* Search dropdown (address) */
.search-wrap { position: relative; }
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

/* Buttons */
.btn-black {
  background: #000;
  color: #fff;
  border: 0;
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 0.98rem;
  cursor: pointer;
  margin-top: 12px;
  transition: background .2s ease, transform .05s ease;
}
.btn-black:hover { background: #222; }
.btn-black:active { transform: translateY(1px); }
.btn-black[disabled] { opacity: .5; cursor: not-allowed; }

/* Text */
.muted {
  color: #4b5563;
  line-height: 1.6;
}

/* Searchable combo (laneway) */
.combo {
  position: relative;
  width: 100%;
  max-width: 520px;
}
.combo-input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
}
.combo-input:focus {
  border-color: #cbd5e1;
  box-shadow: 0 0 0 3px rgba(59,130,246,.15);
}
.selected {
  margin-top: 6px;
  font-size: 12px;
  color: #475569;
}
.combo-list {
  position: absolute;
  z-index: 50;
  left: 0;
  right: 0;
  margin: 6px 0 0;
  max-height: 280px;
  overflow: auto;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 12px 30px rgba(0,0,0,.12);
  list-style: none;
  padding: 6px 0;
}
.combo-item {
  padding: 10px 12px;
  cursor: pointer;
  line-height: 1.1;
}
.combo-item:hover { background: #f8fafc; }
.combo-empty {
  padding: 12px;
  color: #6b7280;
  font-size: 13px;
}

/* Responsive */
@media (max-width: 900px) {
  .voice-hero { grid-template-columns: 1fr; }
  .hero-right { order: -1; }
  .cards { grid-template-columns: 1fr; }
}



</style>


