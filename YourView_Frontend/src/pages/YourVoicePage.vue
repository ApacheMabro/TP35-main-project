<template>
  <div class="view-page">
    <!-- Hero: top half screen -->
    <section class="voice-hero">
      <div class="hero-left">
        <h1>Raise Your Voice</h1>
        <p>
          Help make Melbourne greener. Nominate laneways that deserve trees and shade,
          and tell the council why it matters.
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

          <!-- Laneway select -->
          <label class="label">Choose a laneway</label>
          <select v-model="form.laneway" class="input">
            <option disabled value="">Select a laneway…</option>
            <option v-for="lane in laneways" :key="lane" :value="lane">{{ lane }}</option>
          </select>

          <!-- Address with autocomplete -->
          <label class="label">Address (with suggestions)</label>
          <div class="search-wrap">
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

          <button class="btn-black" @click="submitNomination">Submit Nomination</button>
        </div>

        <!-- Right: Inform council (dead button) -->
        <div class="card council reveal item-3">
          <h3>Inform Melbourne City Council</h3>
          <p class="muted">
            Share your concern and feedback about urban heat in your neighbourhood.
            Let’s encourage more shade, trees, and green infrastructure.
          </p>
          <button class="btn-black" disabled title="Coming soon">Notify Council (Coming Soon)</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

/** ————— Laneway options (example list) ————— */
const laneways = [
  'AC/DC Lane',
  'Degraves Street',
  'Hardware Lane',
  'Hosier Lane',
  'Tattersalls Lane',
  'Centre Place',
]

/** ————— Form state ————— */
const form = ref({
  laneway: '',
  address: '',
  reason: ''
})

/** ————— Address autocomplete state ————— */
const addrQuery = ref('')
const addrSuggestions = ref([])
const showAddrDropdown = ref(false)
const activeIndex = ref(-1)
let debounceId = null

/** Melbourne bounding box for Nominatim (lon,lat): left,top,right,bottom */
const VIEWBOX = {
  left: 144.4,
  top: -37.4,
  right: 145.7,
  bottom: -38.5
}

/** Fetch suggestions from Nominatim (debounced) */
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

/** Click outside to close dropdown */
function onDocClick(e) {
  const wrap = document.querySelector('.search-wrap')
  if (wrap && !wrap.contains(e.target)) {
    showAddrDropdown.value = false
  }
}

/** ————— Submit (stub) ————— */
function submitNomination () {
  // simple validation
  if (!form.value.laneway || !addrQuery.value || !form.value.reason) {
    alert('Please complete laneway, address, and reason.')
    return
  }
  // In real app: POST to backend
  console.log('Nomination submitted:', {
    laneway: form.value.laneway,
    address: addrQuery.value,
    reason: form.value.reason
  })
  alert('Thanks for your nomination!')
  // reset (optional)
  form.value = { laneway: '', address: '', reason: '' }
  addrQuery.value = ''
  addrSuggestions.value = []
  showAddrDropdown.value = false
  activeIndex.value = -1
}

/** ————— Scroll reveal ————— */
const revealRoot = ref(null)
let io = null

onMounted(() => {
  document.addEventListener('click', onDocClick)

  // reveal animation
  io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('reveal-in')
        io.unobserve(e.target)
      }
    })
  }, { threshold: 0.15 })

  // observe targets
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
  margin: 0 0 12px;
  font-size: 1.2rem;
  color: #1f2937;
}

/* Inputs */
.label {
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

/* Search dropdown */
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
.btn-black[disabled] {
  opacity: .5;
  cursor: not-allowed;
}

/* Text */
.muted {
  color: #4b5563;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 900px) {
  .voice-hero { grid-template-columns: 1fr; }
  .hero-right { order: -1; } /* image first on small screens */
  .cards { grid-template-columns: 1fr; }
}
</style>

