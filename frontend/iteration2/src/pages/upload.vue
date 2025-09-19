<template>
  <Header />

  <div class="hero" v-if="!showResults">
    <h1 class="hero-title">Upload My Window</h1>
    <p class="hero-subtitle">
      Share a photo from your window to discover if your area is green enough and see whether you live in a hotter or cooler spot compared to other suburbs.
    </p>

    <div class="carousel">
      <div
        v-for="(img, i) in images"
        :key="i"
        class="slide"
        :class="slideClass(i)"
        :style="{ backgroundImage: `url(${img.src})` }"
        role="img"
        :aria-label="img.alt"
      />
    </div>

    <div class="cta-row">
      <button class="btn primary" @click="openModal">Upload My Window</button>
      <button class="btn secondary">What is 3-30-300</button>
    </div>
  </div>

  <div v-if="showModal" class="modal-overlay" @click.self="closeModal()">
    <div class="modal">
      <div class="modal-header">
        <div class="steps">
          <span :class="['dot', modalStep===1?'active':'']">1</span>
          <span class="dash" />
          <span :class="['dot', modalStep===2?'active':'']">2</span>
        </div>
        <button class="icon-btn" aria-label="Close" @click="closeModal()">×</button>
      </div>

      <div v-if="modalStep===1" class="modal-body">
        <h3 class="modal-title">Upload a photo</h3>
        <div class="upload-box">
          <div v-if="previewUrl" class="preview">
            <img :src="previewUrl" alt="preview" />
          </div>
          <div v-else class="placeholder">
            <span class="ph-icon">📷</span>
            <p>Select a photo (JPG/PNG)</p>
          </div>
          <label class="upload-button">
            <input type="file" accept=".jpg,.jpeg,.png,image/jpeg,image/png" @change="onFileSelected" hidden />
            Choose Photo
          </label>
        </div>

        <label class="consent">
          <input type="checkbox" v-model="allowShow" :disabled="loading" />
          Allow us to use your image for display
        </label>

        <button
          class="fab-next"
          :disabled="!file || loading"
          @click="modalStep=2"
          title="Next"
          aria-label="Next"
        >
          ➜
        </button>
      </div>

      <div v-else-if="modalStep===2" class="modal-body">
        <h3 class="modal-title">Enter your address</h3>
        <div class="autocomplete">
          <input
            class="text-input"
            type="text"
            placeholder="Type your address"
            v-model.trim="address"
            :disabled="loading"
            @input="onAddressInput"
            @focus="predOpen = true"
            @blur="onAddressBlur"
            autocomplete="off"
          />
          <ul v-if="predOpen && predictions.length" class="pred-list">
            <li
              v-for="p in predictions"
              :key="(p as any).place_id || (p as any).placeId"
              class="pred-item"
              @mousedown.prevent="selectPrediction(p as any)"
            >
              <span class="pred-main">
                {{ (p as any).structured_formatting?.main_text
                    || ((p as any).description || (p as any).text?.text || '').split(',')[0] }}
              </span>
              <span class="pred-secondary">
                {{ (p as any).structured_formatting?.secondary_text
                    || ((p as any).description || (p as any).text?.text || '').split(',').slice(1).join(', ').trim() }}
              </span>
            </li>
          </ul>
        </div>

        <button
          class="btn primary full"
          :disabled="!address || !file || loading"
          @click="handleSeeMyScore"
        >
          <span v-if="!loading">See my score</span>
          <span v-else>Working...</span>
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </div>
  </div>

  <div v-if="showResults" class="results">
    <div class="results-actions">
      <div class="results-summary as-banner" :class="summaryLevel">
        <span class="summary-text large">{{ summaryText }}</span>
      </div>
      <div class="actions-right">
        <button class="btn secondary" @click="backToIntro">Back</button>
      </div>
    </div>

    <div class="results-grid">
      <div class="panel image-panel">
        <img :src="previewUrl" alt="Your window" />
      </div>

      <div class="panel">
        <div class="cards-mini">
          <div class="card mini" :class="{ ok: treesOK, bad: !treesOK, show: showTips3 }">
            <div class="mini-inner">
              <div class="mini-head">
                <span class="mini-title">Tree Visible</span>
                <span class="info-dot" aria-label="At least 3 trees should be visible" title="At least 3 trees should be visible">i</span>
              </div>
              <div class="mini-value">
                <strong>{{ typeof treesCount === 'number' ? treesCount : '—' }}</strong>
                <span class="unit">{{ treesCount === 1 ? ' Tree' : ' Trees' }}</span>
              </div>
              <div class="mini-sub">from your window</div>
              <button class="mini-expand" @click="showTips3 = true">
                <span>See what you can do</span>
                <span class="chev">▾</span>
              </button>
            </div>
            <div class="mini-overlay">
              <div class="mini-ov-body">
                <p>Create greener sustainable community from your hand. Snap your plant picture, and we will give tips to bring it back to life.</p>
                <div class="mini-ov-actions">
                  <button class="btn primary">Check Plant Health</button>
                  <button class="btn ghost" @click="showTips3 = false">Back</button>
                </div>
              </div>
            </div>
          </div>

          <div class="card mini" :class="{ ok: pass30, bad: !pass30, show: showTips30 }">
            <div class="mini-inner">
              <div class="mini-head">
                <span class="mini-title">Canopy Cover</span>
                <span class="info-dot" aria-label="Aim for 30% canopy cover" title="Aim for 30% canopy cover">i</span>
              </div>
              <div class="mini-value">
                <strong>{{ canopy }}</strong><span class="unit"> %</span>
              </div>
              <div class="mini-sub">
                <template v-if="canopyArea">from {{ canopyArea }}</template>
                <template v-else>from your area<span v-if="addressShort"> — {{ addressShort }}</span></template>
              </div>
              <button class="mini-expand" @click="showTips30 = true">
                <span>See what you can do</span>
                <span class="chev">▾</span>
              </button>
            </div>
            <div class="mini-overlay">
              <div class="mini-ov-body">
                <p>As cities grow, plants disappear and concrete takes over, trapping and radiating heat. Search your location to see heat data.</p>
                <div class="mini-ov-actions">
                  <button class="btn primary">Check your area heat</button>
                  <button class="btn ghost" @click="showTips30 = false">Back</button>
                </div>
              </div>
            </div>
          </div>

          <div class="card mini" :class="{ ok: pass300, bad: !pass300, show: showTips300 }">
            <div class="mini-inner">
              <div class="mini-head">
                <span class="mini-title">Nearest Park</span>
                <span class="info-dot" aria-label="Target is within 300 meters" title="Target is within 300 meters">i</span>
              </div>
              <div class="mini-value">
                <strong>{{ parkDistance }}</strong><span class="unit"> Meters</span>
              </div>
              <div class="mini-sub">
                <template v-if="nearestParkName && parkLink">
                  <a class="park-link" :href="parkLink" target="_blank" rel="noopener">{{ nearestParkName }}</a>
                </template>
                <template v-else>from your house</template>
              </div>
              <button class="mini-expand" @click="showTips300 = true">
                <span>See what you can do</span>
                <span class="chev">▾</span>
              </button>
            </div>
            <div class="mini-overlay">
              <div class="mini-ov-body">
                <p>Your voice is important to Melbourne, you can request directly to the government about your concern of green space in your surrounding.</p>
                <div class="mini-ov-actions">
                  <button class="btn primary">Contact Council</button>
                  <button class="btn ghost" @click="showTips300 = false">Back</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <Footer />

  <div class="toast" :class="[toastVisible ? 'on' : '', toastType]" role="status" aria-live="polite">
    {{ toastMessage }}
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, computed } from 'vue'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

const UPLOADER_URL =
  'https://oelkz0pl2c.execute-api.ap-southeast-2.amazonaws.com/default/upload-image'
const ANALYZER_URL =
  'https://2piqweol0f.execute-api.ap-southeast-2.amazonaws.com/analyze'
const DELETE_URL =
  'https://oelkz0pl2c.execute-api.ap-southeast-2.amazonaws.com/default/delete-object'

import img23 from '@/assets/Group 23.png'
import img27 from '@/assets/Group 27.png'
import img28 from '@/assets/Group 28.png'

type PlacePrediction = google.maps.places.AutocompletePrediction | any

const images = [
  { src: img23, alt: 'Window 1' },
  { src: img27, alt: 'Window 2' },
  { src: img28, alt: 'Window 3' }
]

const active = ref(0)
let heroTimer: number | undefined

onMounted(() => {
  heroTimer = window.setInterval(() => {
    active.value = (active.value + 1) % images.length
  }, 3000)
})
onUnmounted(() => {
  if (heroTimer) window.clearInterval(heroTimer)
  if (predTimer) window.clearTimeout(predTimer)
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
})

function slideClass(i: number) {
  const prev = (active.value - 1 + images.length) % images.length
  const next = (active.value + 1) % images.length
  return {
    center: i === active.value,
    left: i === prev,
    right: i === next,
    hidden: !(i === active.value || i === prev || i === next)
  }
}

const showModal = ref(false)
const modalStep = ref<1 | 2>(1)
function openModal() {
  showModal.value = true
  modalStep.value = 1
}
function closeModal(force = false) {
  if (loading.value && !force) return
  showModal.value = false
}

const file = ref<File | null>(null)
const previewUrl = ref<string | null>(null)
const allowShow = ref(false)
const loading = ref(false)
const error = ref<string | null>(null)

const showResults = ref(false)
const treesCount = ref<number | null>(null)
const treesOK = computed(() => (typeof treesCount.value === 'number' ? treesCount.value >= 3 : false))

function onFileSelected(e: Event) {
  const input = e.target as HTMLInputElement
  const f = input.files?.[0] ?? null
  error.value = null
  treesCount.value = null
  showResults.value = false

  if (!f) {
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = null
    file.value = null
    return
  }
  const ok = /\.(jpe?g|png)$/i.test(f.name)
  if (!ok) {
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = null
    file.value = null
    error.value = 'Only JPG and PNG are allowed.'
    return
  }
  file.value = f
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = URL.createObjectURL(f)
}

async function parseMaybeLambdaProxyResponse(res: Response) {
  const data = await res.json().catch(() => null)
  if (!data) return null
  if ('statusCode' in (data as any) && 'body' in (data as any) && typeof (data as any).body === 'string') {
    try { return JSON.parse((data as any).body) } catch { return data }
  }
  return data
}

const GMAPS_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string
const SB_URL = import.meta.env.VITE_SUPABASE_URL as string
const SB_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY as string

const address = ref<string>('')
const predictions = ref<PlacePrediction[]>([])
const predOpen = ref<boolean>(false)

const lat = ref<number | null>(null)
const lng = ref<number | null>(null)

const canopy = ref<number>(0)
const canopyArea = ref<string>('')
const parkDistance = ref<number>(9999)
const nearestParkName = ref<string>('')
const nearestParkLat = ref<number | null>(null)
const nearestParkLng = ref<number | null>(null)
const nearestParkPlaceId = ref<string | null>(null)

const pass30 = computed(() => canopy.value >= 30)
const pass300 = computed(() => parkDistance.value <= 300)

const passes = computed(() =>
  (treesOK.value ? 1 : 0) + (pass30.value ? 1 : 0) + (pass300.value ? 1 : 0)
)

const summaryText = computed(() =>
  passes.value === 3
    ? 'Congratulations — you live in a very healthy green environment.'
    : 'Looks like your area needs more green space.'
)

const summaryLevel = computed(() =>
  passes.value === 3 ? 'great' : 'bad'
)

const parkLink = computed(() => {
  const name = nearestParkName.value?.trim()
  const pid = nearestParkPlaceId.value?.trim() || ''
  const plat = nearestParkLat.value
  const plng = nearestParkLng.value
  if (name && pid) {
    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(name)}&query_place_id=${encodeURIComponent(pid)}`
  }
  if (plat != null && plng != null) {
    return `https://www.google.com/maps/search/?api=1&query=${plat},${plng}`
  }
  if (name) {
    return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(name)}`
  }
  return ''
})

const addressShort = computed(() => {
  const a = (address.value || '').trim()
  if (!a) return ''
  const parts = a.split(',').map(s => s.trim()).filter(Boolean)
  if (parts.length >= 2) return parts.slice(-2).join(', ')
  return parts[0] || ''
})

let googleLoaded = false
let autoService: google.maps.places.AutocompleteService | null = null
let detailsService: google.maps.places.PlacesService | null = null
let sessionToken: google.maps.places.AutocompleteSessionToken | null = null

function loadGoogleMaps() {
  return new Promise<void>((resolve, reject) => {
    if (googleLoaded && (window as any).google) return resolve()
    const s = document.createElement('script')
    s.src = `https://maps.googleapis.com/maps/api/js?key=${GMAPS_KEY}&libraries=places,geometry&v=quarterly`
    s.async = true
    s.onerror = () => reject(new Error('Failed to load Google Maps JS'))
    s.onload = () => { googleLoaded = true; resolve() }
    document.head.appendChild(s)
  })
}

async function ensureAutocomplete() {
  await loadGoogleMaps()
  const g = (window as any).google
  if (!autoService) autoService = new g.maps.places.AutocompleteService()
  if (!detailsService) detailsService = new g.maps.places.PlacesService(document.createElement('div'))
  if (!sessionToken) sessionToken = new g.maps.places.AutocompleteSessionToken()
}

let predTimer: number | null = null
function onAddressInput() {
  error.value = null
  if (predTimer) window.clearTimeout(predTimer)
  const q = address.value
  if (!q) { predictions.value = []; return }
  predTimer = window.setTimeout(() => fetchPredictions(q), 220)
}

async function fetchPredictions(q: string) {
  try {
    await ensureAutocomplete()
    const g = (window as any).google
    autoService!.getPlacePredictions({ input: q, sessionToken: sessionToken! }, (res: any, status: any) => {
      if (status !== g.maps.places.PlacesServiceStatus.OK || !res) {
        predictions.value = []
        return
      }
      predictions.value = res
    })
  } catch {
    predictions.value = []
  }
}

async function selectPrediction(p: PlacePrediction) {
  try {
    await ensureAutocomplete()
    const g = (window as any).google
    const req = { placeId: (p as any).place_id || (p as any).placeId, fields: ['geometry'] }
    detailsService!.getDetails(req as any, (place: any, status: any) => {
      if (status !== g.maps.places.PlacesServiceStatus.OK || !place?.geometry?.location) {
        error.value = 'Failed to resolve address location.'
        return
      }
      address.value = (p as any).description || (p as any).text?.text || address.value
      lat.value = place.geometry.location.lat()
      lng.value = place.geometry.location.lng()
      predictions.value = []
      predOpen.value = false
    })
  } catch {
    error.value = 'Failed to resolve address.'
  }
}

function onAddressBlur() {
  setTimeout(() => { predOpen.value = false }, 120)
}

async function computeNearestParkDistance(lon: number, latNum: number): Promise<number> {
  const url = 'https://places.googleapis.com/v1/places:searchNearby'
  const body = {
    includedTypes: ['park'],
    maxResultCount: 1,
    locationRestriction: { circle: { center: { latitude: latNum, longitude: lon }, radius: 5000 } },
    rankPreference: 'DISTANCE'
  }
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Goog-Api-Key': GMAPS_KEY,
      'X-Goog-FieldMask': 'places.id,places.displayName,places.location'
    },
    body: JSON.stringify(body)
  })
  if (!res.ok) throw new Error('Nearby search failed')
  const data = await res.json()
  const place = data.places?.[0]
  if (!place?.location) throw new Error('No nearby park found')
  nearestParkName.value = place.displayName?.text || 'Nearest park'
  nearestParkLat.value = place.location.latitude ?? null
  nearestParkLng.value = place.location.longitude ?? null
  nearestParkPlaceId.value = place.id ?? null

  await loadGoogleMaps()
  const g = (window as any).google
  const a = new g.maps.LatLng(latNum, lon)
  const b = new g.maps.LatLng(place.location.latitude, place.location.longitude)
  const d = g.maps.geometry.spherical.computeDistanceBetween(a, b)
  return Math.round(d)
}

async function getCanopy(lon: number, latNum: number): Promise<{ pct: number; area?: string | null }> {
  const res = await fetch(`${SB_URL}/rest/v1/rpc/api_canopy_for_point`, {
    method: 'POST',
    headers: {
      apikey: SB_KEY,
      Authorization: `Bearer ${SB_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ p_lon: lon, p_lat: latNum })
  })
  if (!res.ok) throw new Error('Canopy RPC failed')
  const data = await res.json()
  const pick = (obj: any, keys: string[]) =>
    keys.map(k => obj?.[k]).find(v => v != null)
  let pct: number | null = null
  let area: string | null = null
  if (Array.isArray(data) && data.length) {
    const row = data[0]
    pct  = Number(pick(row, ['canopy_percent','canopy_pct','canopy']))
    area = pick(row, ['area_name','region','suburb','lga','locality','area','area_text']) ?? null
  } else if (data && typeof data === 'object') {
    pct  = Number(pick(data, ['canopy_percent','canopy_pct','canopy']))
    area = pick(data, ['area_name','region','suburb','lga','locality','area','area_text']) ?? null
  }
  if (!Number.isFinite(pct)) throw new Error('Invalid canopy payload')
  return { pct: Math.round(pct!), area }
}

const toastVisible = ref(false)
const toastMessage = ref('')
const toastType = ref<'info' | 'success' | 'error'>('info')
let toastTimer: number | null = null
function showToast(msg: string, type: 'info' | 'success' | 'error' = 'info', ms = 2800) {
  toastMessage.value = msg
  toastType.value = type
  toastVisible.value = true
  if (toastTimer) window.clearTimeout(toastTimer)
  toastTimer = window.setTimeout(() => {
    toastVisible.value = false
    toastTimer = null
  }, ms)
}

async function handleSeeMyScore() {
  error.value = null
  treesCount.value = null
  showResults.value = false

  if (!file.value) { error.value = 'Please choose a JPG or PNG file.'; return }
  if (!address.value.trim()) { error.value = 'Please enter your address.'; return }
  if (lat.value == null || lng.value == null) { error.value = 'Please pick an address from suggestions.'; return }
  if (!GMAPS_KEY || !SB_URL || !SB_KEY) { error.value = 'Missing API keys or endpoints. Please check environment variables.'; return }

  loading.value = true

  try {
    const form = new FormData()
    form.append('file', file.value)
    form.append('folder', 'YourWindow')
    const up = await fetch(UPLOADER_URL, { method: 'POST', body: form })
    if (!up.ok) {
      const text = await up.text().catch(() => '')
      let detail = ''
      try { const j = JSON.parse(text); detail = (j as any)?.detail ?? '' } catch {}
      throw new Error(detail || `Upload failed (${up.status})`)
    }
    const upJson = await up.json()
    const uploadedBucket = (upJson.bucket || upJson.s3_bucket || upJson.Bucket) as string
    const uploadedKey    = (upJson.key    || upJson.s3_key    || upJson.Key) as string
    if (!uploadedBucket || !uploadedKey) throw new Error('Upload did not return bucket/key.')

    const payload = { bucket: uploadedBucket, key: uploadedKey, include_details: true, check_compliance: true }
    const an = await fetch(ANALYZER_URL, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (!an.ok) {
      const text = await an.text().catch(() => '')
      throw new Error(text || `Analyzer failed (${an.status})`)
    }
    const analyze = (await parseMaybeLambdaProxyResponse(an)) ?? {}
    const count =
      (analyze as any)?.trees_counted ??
      (analyze as any)?.tree_count ??
      (analyze as any)?.analysis_details?.tree_count
    treesCount.value = (typeof count === 'number') ? count : null

    if (!allowShow.value) {
      try {
        const del = await fetch(DELETE_URL, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ bucket: uploadedBucket, key: uploadedKey })
        })
        if (del.ok) {
          showToast('We won’t display your photo and it has been deleted.', 'info')
        } else {
          showToast('We couldn’t delete the uploaded image.', 'error')
          console.warn('Delete failed:', await del.text().catch(() => String(del.status)))
        }
      } catch (e: any) {
        showToast('We couldn’t delete the uploaded image.', 'error')
        console.warn('Delete error:', e?.message || e)
      }
    }

    const lon = Number(lng.value)
    const latNum = Number(lat.value)
    const [c30Res, d300Res] = await Promise.allSettled([
      getCanopy(lon, latNum),
      computeNearestParkDistance(lon, latNum)
    ])
    if (c30Res.status === 'fulfilled') {
      canopy.value = c30Res.value.pct
      canopyArea.value = c30Res.value.area || ''
    }
    if (d300Res.status === 'fulfilled') parkDistance.value = d300Res.value

    showResults.value = true
    closeModal(true)
  } catch (e: any) {
    error.value = e?.message || String(e)
  } finally {
    loading.value = false
  }
}

function resetForNewUpload() {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = null
  file.value = null
  allowShow.value = false
  address.value = ''
  predictions.value = []
  predOpen.value = false
  lat.value = null
  lng.value = null
  canopy.value = 0
  canopyArea.value = ''
  parkDistance.value = 9999
  nearestParkName.value = ''
  nearestParkLat.value = null
  nearestParkLng.value = null
  nearestParkPlaceId.value = null
  treesCount.value = null
  error.value = null
  showTips3.value = false
  showTips30.value = false
  showTips300.value = false
}

function backToIntro() {
  resetForNewUpload()
  showResults.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const showTips3 = ref(false)
const showTips30 = ref(false)
const showTips300 = ref(false)
</script>

<style scoped>
.hero {
  max-width: 980px;
  margin: 32px auto 0;
  padding: 0 16px;
  text-align: center;
}
.hero-title { color:#064e3b; font-size:36px; font-weight:800; margin:0 0 8px; }
.hero-subtitle { color:#55646a; font-size:14px; max-width:740px; margin:0 auto 18px; line-height:1.5; }

.carousel { position:relative; height:280px; margin:8px auto 16px; perspective:1000px; overflow:hidden; }
.slide { position:absolute; top:50%; left:50%; width:300px; height:180px; background-size:cover; background-position:center; border-radius:14px; box-shadow:0 10px 30px rgba(0,0,0,.15); transform:translate(-50%,-50%) scale(.6) rotateY(0deg); opacity:0; transition:all .8s ease; }
.slide.center { transform:translate(-50%,-50%) scale(1) rotateY(0); opacity:1; z-index:3; }
.slide.left { transform:translate(calc(-50% - 200px), -50%) scale(.5) rotateY(30deg); opacity:.6; z-index:2; }
.slide.right { transform:translate(calc(-50% + 200px), -50%) scale(.5) rotateY(-30deg); opacity:.6; z-index:2; }
.slide.hidden { opacity:0; z-index:1; }
@media (min-width:900px){ .carousel{height:340px;} .slide{width:420px;height:240px;} .slide.left{transform:translate(calc(-50% - 260px), -50%) scale(.55) rotateY(30deg);} .slide.right{transform:translate(calc(-50% + 260px), -50%) scale(.55) rotateY(-30deg);} }

.cta-row { display:flex; gap:12px; justify-content:center; margin-top:8px; margin-bottom:24px; }
.btn { padding:10px 18px; border-radius:9999px; font-weight:700; font-size:14px; cursor:pointer; border:2px solid #064e3b; transition:all .2s ease; }
.btn.primary{ background:#064e3b; color:#fff; } .btn.primary:hover{ filter:brightness(1.05); }
.btn.secondary{ background:#fff; color:#064e3b; } .btn.secondary:hover{ background:#ecfdf5; }

.modal-overlay{ position:fixed; inset:0; background:rgba(0,0,0,.35); display:grid; place-items:center; z-index:50; }
.modal{ width:min(720px,92vw); background:#fff; border-radius:16px; padding:16px; box-shadow:0 20px 60px rgba(0,0,0,.25); position:relative; }
.modal-header{ display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.icon-btn{ all:unset; font-size:22px; line-height:1; padding:4px 8px; cursor:pointer; color:#374151; }
.steps{ display:inline-flex; align-items:center; gap:10px; }
.dot{ width:28px; height:28px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; border:2px solid #10b981; color:#065f46; font-weight:800; background:#fff; }
.dot.active{ background:#ecfdf5; }
.dash{ width:36px; height:2px; background:#d1fae5; border-radius:2px; }
.modal-title{ font-weight:800; color:#064e3b; margin:6px 0 10px; }
.modal-body{ padding:6px 4px 16px; }
.upload-box{ border:2px dashed #e5e7eb; border-radius:14px; padding:16px; display:grid; gap:12px; place-items:center; background:#fafafa; }
.preview img{ max-width:100%; max-height:280px; object-fit:contain; border-radius:10px; }
.placeholder{ color:#6b7280; text-align:center; }
.ph-icon{ font-size:28px; display:block; margin-bottom:6px; }
.upload-button{ border:1px solid #cbd5e1; background:#fff; border-radius:10px; padding:10px 14px; cursor:pointer; font-weight:600; }
.upload-button:hover{ background:#f8fafc; }
.consent{ display:flex; align-items:center; gap:8px; margin-top:10px; color:#374151; }
.fab-next{ position:absolute; right:24px; bottom:18px; width:46px; height:46px; border-radius:9999px; border:none; cursor:pointer; background:#064e3b; color:#fff; font-size:20px; display:grid; place-items:center; }
.fab-next:disabled{ opacity:.5; cursor:not-allowed; }
.text-input{ width:100%; border:1px solid #cbd5e1; border-radius:10px; padding:12px; font-size:14px; margin:8px 0 12px; }
.btn.full{ width:100%; }
.error{ color:#b91c1c; margin-top:.5rem; }

.autocomplete{ position: relative; }
.pred-list{
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(0,0,0,.12);
  max-height: 280px;
  overflow: auto;
  z-index: 1000;
  padding: 4px 0;
}
.pred-item{
  padding: 10px 12px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.pred-item + .pred-item{ border-top: 1px solid #f3f4f6; }
.pred-item:hover{ background: #f8fafc; }
.pred-main{ font-weight: 800; color: #111827; line-height: 1.2; }
.pred-secondary{ font-size: 12px; color: #6b7280; line-height: 1.2; }

.results{ max-width:1080px; margin:16px auto 32px; padding:0 16px; }
.results-grid{ display:grid; gap:16px; grid-template-columns:1fr; }
.panel{ background:#fff; border:1px solid #e5e7eb; border-radius:16px; padding:14px; }
.image-panel img{ width:100%; border-radius:12px; }
@media (min-width:900px){ .results-grid{ grid-template-columns:1fr 1fr; } }

.results-actions{
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
@media (min-width: 900px){
  .results-actions{
    grid-template-columns: 1fr 1fr;
  }
  .actions-right{ justify-self: end; }
}

.cards-mini{
  display: grid;
  gap: 14px;
}
.card.mini{
  background:#fff;
  border-radius: 14px;
  padding: 14px 14px 8px;
  border: 2px solid #e5e7eb;
  position: relative;
  overflow: hidden;
}
.mini-head{ display:flex; align-items:center; justify-content:space-between; margin-bottom:6px; }
.mini-title{ font-weight:700; color:#111827; }
.info-dot{
  display:inline-flex; align-items:center; justify-content:center;
  width:20px; height:20px; border-radius:50%;
  background:#f3f4f6; color:#111827; font-size:12px; font-weight:800;
  border:1px solid #e5e7eb;
}
.mini-value{ font-size:28px; font-weight:900; letter-spacing:.2px; display:flex; align-items:baseline; gap:6px; color:#111827; }
.mini-value .unit{ font-size:18px; font-weight:800; }
.mini-sub{ color:#6b7280; font-size:12px; margin-top:2px; }
.mini-expand{
  margin-top:10px; width:100%; display:flex; align-items:center; justify-content:space-between;
  background:#f8fafc; border:1px solid #e5e7eb; color:#064e3b;
  border-radius:10px; padding:8px 10px; font-weight:700; cursor:pointer;
}
.mini-inner{ position: relative; z-index: 1; }
.mini-overlay{
  position: absolute;
  inset: 0;
  background: #fff;
  padding: 14px;
  display: grid;
  place-items: stretch;
  transform: translateY(100%);
  opacity: 0;
  transition: transform .28s ease, opacity .28s ease;
  z-index: 2;
  border-radius: 12px;
}
.card.mini.show .mini-overlay{
  transform: translateY(0);
  opacity: 1;
}
.mini-ov-body{ display: grid; gap: 12px; align-content: start; }
.mini-ov-actions{ display:flex; gap:10px; }
.btn.ghost{
  background: #fff;
  color:#064e3b;
  border:2px solid #064e3b;
  padding:10px 14px;
  border-radius:9999px;
  font-weight:700;
  font-size:14px;
}

.card.mini.ok{ background:#dcfce7; border-color:#16a34a; box-shadow:0 0 0 3px rgba(22,163,74,.2) inset; }
.card.mini.bad{ background:#fee2e2; border-color:#dc2626; box-shadow:0 0 0 3px rgba(220,38,38,.2) inset; }

.park-link{ text-decoration: underline; color:#065f46; }

.results-summary{
  display:flex; justify-content:center; align-items:center; text-align:center;
  padding:12px 14px; border-radius:12px; border:2px solid; font-weight:800; line-height:1.35;
}
.results-summary.great{ background:#bbf7d0; border-color:#16a34a; color:#064e3b; }
.results-summary.bad{ background:#fecaca; border-color:#dc2626; color:#7f1d1d; }
.results-summary.as-banner{ width:100%; }
.summary-text{ font-size:16px; }
.summary-text.large{ font-size:20px; }
@media (min-width:900px){ .summary-text.large{ font-size:22px; } }

.toast{
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%) translateY(8px);
  opacity: 0;
  pointer-events: none;
  z-index: 60;
  padding: 10px 14px;
  border-radius: 10px;
  font-weight: 700;
  line-height: 1.3;
  box-shadow: 0 10px 30px rgba(0,0,0,.2);
  transition: opacity .25s ease, transform .25s ease;
  background: #111827;
  color: #fff;
}
.toast.on{ opacity: 1; transform: translateX(-50%) translateY(0); }
.toast.success{ background:#065f46; }
.toast.error{ background:#7f1d1d; }
.toast.info{ background:#111827; }
</style>
