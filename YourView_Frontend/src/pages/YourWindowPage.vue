<template>

  <div class="green-page">
    <div class="page">
      <div class="hero">
        <img class="hero-img" src="@/assets/background4.jpeg" alt="Hero background" />
        <div class="overlay">
          <h1 class="title">Snap & Share</h1>
          <p class="subtitle">See your green score with in few steps</p>
        </div>
      </div>

      <section class="how-it-works">
        <h2>How Does It Work</h2>
        <div class="steps">
          <div class="step">
            <img src="@/assets/photo.png" alt="Upload Photo" />
            <p>Take or upload your window photo</p>
          </div>
          <div class="step">
            <img src="@/assets/tree.png" alt="Count Trees" />
            <p>Count the number of visible trees</p>
          </div>
          <div class="step">
            <img src="@/assets/coordinate.png" alt="Add Location" />
            <p>Enter your address / coordinates</p>
          </div>
          <div class="step">
            <img src="@/assets/eye.png" alt="View Score" />
            <p>See your 3-30-300 score instantly</p>
          </div>
        </div>
        <div class="upload-btn-wrapper">
          <button class="upload-btn" @click="openModal">Upload My Window</button>
        </div>
      </section>
    </div>

    <section v-if="showResult" ref="resultRef" id="result-section" class="result-wrap">
      <div class="result-header">
        <h2 class="result-title">{{ headline }}</h2>
        <p class="result-sub">Let's see if you are living in a cool & greener & healthier space</p>
      </div>

      <div class="result-grid">
        <div class="result-photo">
          <img :src="previewUrl || placeholder" alt="Your window" />
        </div>

        <div class="result-cards">
          <div class="result-cards">
            <div class="check-card" :class="pass3 ? 'ok' : 'bad'">
              <div class="card-body">
                <div class="check-icon-wrap">
                  <img src="/src/assets/tree.png" class="check-icon" />
                </div>
                <div class="check-content">
                  <div class="check-title">3 Trees Visible</div>
                  <div class="check-sub">Trees visible from your window</div>
                  <div class="badge" :class="pass3 ? 'b-ok' : 'b-bad'">
                    <span>{{ pass3 ? '✔ Compliant' : '✘ Not compliant' }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="check-card" :class="pass30 ? 'ok' : 'bad'">
              <div class="card-body">
                <div class="check-icon-wrap">
                  <img src="/src/assets/tree.png" class="check-icon" />
                </div>
                <div class="check-content">
                  <div class="check-title">30% Canopy Cover</div>
                  <div class="check-sub">Neighborhood tree coverage</div>
                  <div class="badge" :class="pass30 ? 'b-ok' : 'b-bad'">
                    <span>{{ pass30 ? '✔ Compliant' : '✘ Needs Improvement' }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="check-card" :class="pass300 ? 'ok' : 'bad'">
              <div class="card-body">
                <div class="check-icon-wrap">
                  <img src="/src/assets/tree.png" class="check-icon" />
                </div>
                <div class="check-content">
                  <div class="check-title">300m Green Space</div>
                  <div class="check-sub">Distance to nearest park</div>
                  <div class="badge" :class="pass300 ? 'b-ok' : 'b-bad'">
                    <span>{{ pass300 ? '✔ Compliant' : '✘ Needs Improvement' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="metric-row">
        <div class="metric">
          <div class="metric-icon-title">
            <img src="@/assets/tree.png" alt="Tree Icon" class="metric-icon" />
            <div class="m-title">Trees Visible</div>
          </div>
          <div class="m-value">{{ trees }} Trees</div>
          <div class="m-sub">from your window</div>
        </div>
        <div class="metric">
          <div class="metric-icon-title">
            <img src="@/assets/tree.png" alt="Canopy Icon" class="metric-icon" />
            <div class="m-title">Canopy Cover</div>
          </div>
          <div class="m-value">{{ canopy }}%</div>
          <div class="m-sub">from your area</div>
        </div>
        <div class="metric">
          <div class="metric-icon-title">
            <img src="@/assets/tree.png" alt="Park Icon" class="metric-icon" />
            <div class="m-title">Nearest Park</div>
          </div>
          <div class="m-value">{{ parkDistance }}m</div>
          <div class="m-sub">from your house</div>
        </div>
        <div class="metric">
          <div class="metric-icon-title">
            <img src="@/assets/tree.png" alt="Heat Icon" class="metric-icon" />
            <div class="m-title">Heat Risk</div>
          </div>
          <div class="m-value">1/5</div>
          <div class="m-sub">urban heat island</div>
          <button class="heatmap-btn" @click="goToHeatMap">Explore Heat Map</button>
        </div>
      </div>
    </section>

    <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-card">
        <button class="modal-close" @click="closeModal" aria-label="Close">
          <svg viewBox="0 0 24 24" width="18" height="18">
            <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/>
          </svg>
        </button>
        <div v-if="step === 1" class="step-pane">
          <div class="upload-grid">
            <div
              class="dropzone"
              :class="{ 'is-filled': !!previewUrl }"
              @dragover.prevent
              @dragenter.prevent
              @drop.prevent="handleDrop"
            >
              <template v-if="!previewUrl">
                <div class="dz-inner">
                  <div class="dz-icon">
                    <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                      <circle cx="8.5" cy="8.5" r="1.5"></circle>
                      <path d="M21 15l-5-5L5 21"></path>
                    </svg>
                  </div>
                  <p>Drag picture here to upload</p>
                  <div class="dz-or">or</div>
                </div>
              </template>
              <template v-else>
                <img :src="previewUrl" alt="Preview" class="dz-preview" />
              </template>
              <input ref="fileInput" type="file" accept="image/*,.jpg,.jpeg,.png,.gif,.webp,.bmp,.jfif,.heic,.heif,.tif,.tiff" class="hidden-input" @change="handleFile" />
            </div>

            <div class="dz-actions">
              <button class="select-btn" @click="fileInput?.click()">
                {{ previewUrl ? 'Upload an other picture' : 'Select file' }}
              </button>
            </div>
          </div>

          <div class="step-actions">
            <button class="circle-btn next" :disabled="!file" @click="step = 2" aria-label="Next">
              <svg class="icon" viewBox="0 0 24 24" width="18" height="18">
                <path d="M5 12h14M13 5l7 7-7 7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>

        <div v-else class="step-pane">
          <div class="form-field">
            <label class="label">Number of trees outside your window</label>
            <input type="text" inputmode="numeric" pattern="[0-9]*" v-model.trim="form.trees" @input="validateTrees('input')" @blur="validateTrees('blur')" placeholder="eg,. 3"/>
            <div class="error" v-if="errors.trees">The input number should be an integer >= 0</div>
          </div>
          <div class="form-field">
            <label class="label">Address</label>
            <div class="address-row" ref="dropdownRef">
              <span class="addr-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="18" height="18">
                  <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" fill="none" />
                  <line x1="16.65" y1="16.65" x2="21" y2="21" stroke="currentColor" stroke-width="2" />
                </svg>
              </span>
              <input
                type="text"
                v-model="form.address"
                @input="onInput"
                @focus="showDropdown = predictions.length > 0"
                @keydown.down.prevent="moveActive(1)"
                @keydown.up.prevent="moveActive(-1)"
                @keydown.enter.prevent="confirmActive"
                @keydown.esc.prevent="hideDropdown"
                placeholder="Search address"/>
              <ul v-if="showDropdown && predictions.length" class="autocomplete-list">
                <li v-for="(item, i) in predictions"
                  :key="item.place_id"
                  :class="{ active: i === activeIndex }"
                  @mousedown.prevent="selectPrediction(item)">
                  <div class="primary" v-html="formatPrimary(item)"></div>
                  <div class="secondary">{{ item.structured_formatting?.secondary_text }}</div>
                </li>
              </ul>
            </div>
            <div class="error" v-if="errors.address">Address is required</div>
          </div>

          <div class="tc-row">
            <label class="checkbox-wrapper">
              <input type="checkbox" v-model="form.agree" />
              <span class="checkmark"></span>
              <span class="tc-label"> I agree to the Terms</span>
            </label>
            <button type="button" class="tc-link" :aria-expanded="showTC" aria-controls="tc-panel" @click="showTC = !showTC">View Terms</button>
          </div>

          <transition name="accordion">
            <div v-if="showTC" id="tc-panel" class="tc-panel">
              <div class="tc-content">
                <h4>Terms & Conditions</h4>
                <ul>
                  <li>By uploading an image, you confirm we have the right to store it.</li>
                  <li>Personal information you provide is used to compute your score.</li>
                  <li>Do not upload sensitive or offensive content.</li>
                  <li>Results are indicative and may use approximations.</li>
                </ul>
              </div>
              <div class="tc-actions">
                <button class="tc-close" @click="showTC = false">Close</button>
              </div>
            </div>
          </transition>

          <div class="actions-row">
            <button class="circle-btn back" @click="step = 1" aria-label="Back">
              <svg class="icon" viewBox="0 0 24 24" width="18" height="18">
                <path d="M19 12H5M11 19l-7-7 7-7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <button class="primary-btn" :disabled="!canSubmit" @click="submit">See my score</button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, reactive, computed, nextTick } from "vue";

const showModal = ref(false);
const step = ref(1);
const showTC = ref(false);

const fileInput = ref(null);
const file = ref(null);
const previewUrl = ref("");
const placeholder = "https://via.placeholder.com/800x500?text=Your+window";

const form = reactive({
  trees: "",
  address: "",
  agree: false,
});
const errors = reactive({ trees: "", address: "" });

const showResult = ref(false);
const resultRef = ref(null);

const trees = ref(0);
const canopy = ref(36);
const parkDistance = ref(256);

const pass3 = computed(() => trees.value >= 3);
const pass30 = computed(() => canopy.value >= 30);
const pass300 = computed(() => parkDistance.value <= 300);

const headline = computed(() => (pass3.value && pass30.value && pass300.value ? "Congratulations, your living environment is excellent" : "You need more green"));

function openModal() {
  showModal.value = true;
  step.value = 1;
}

function resetState() {
  file.value = null;
  previewUrl.value = "";
  form.trees = "";
  form.address = "";
  form.agree = false;
  errors.trees = "";
  errors.address = "";
}

function closeModal() {
  showModal.value = false;
}
function handleFile(e) {
  const f = e.target.files?.[0];
  if (f) loadFile(f);
}
function handleDrop(e) {
  const f = e.dataTransfer?.files?.[0];
  if (f) loadFile(f);
}
function loadFile(f) {
  const name = (f.name || "").toLowerCase();
  const mime = (f.type || "").toLowerCase();
  const byMime = mime.startsWith("image/");
  const byExt = /\.(png|jpe?g|jfif|gif|webp|bmp|heic|heif|tiff?)$/i.test(name);
  if (!byMime && !byExt) return;
  file.value = f;
  previewUrl.value = URL.createObjectURL(f);
}


function validateTrees(mode) {
  const v = String(form.trees).trim();
  if (v === "") {
    errors.trees = mode === "blur" ? "bad" : "";
    return;
  }
  errors.trees = /^\d+$/.test(v) ? "" : "bad";
}


function validateAddress() {
  errors.address = form.address ? "" : "bad";
}
const canSubmit = computed(() => {
  return !!file.value && form.trees !== "" && form.address !== "" && !errors.trees && !errors.address && form.agree;
});
async function submit() {
  validateTrees();
  validateAddress();
  if (!canSubmit.value) return;
  trees.value = Number(form.trees);
  showResult.value = true;
  showModal.value = false;
  await nextTick();
  resultRef.value?.scrollIntoView({ behavior: "smooth", block: "start" });
}

import { onMounted, onBeforeUnmount } from 'vue'

let acSvc = null
let sessionToken = null

const predictions = ref([])
const showDropdown = ref(false)
const activeIndex = ref(-1)
const dropdownRef = ref(null)

function loadGoogle() {
  if (window.google?.maps) {
    acSvc = new google.maps.places.AutocompleteService()
    newSession()
  }
}

function newSession() {
  sessionToken = new google.maps.places.AutocompleteSessionToken()
}

function onInput() {
  if (!form.address.trim()) {
    predictions.value = []
    showDropdown.value = false
    activeIndex.value = -1
    return
  }
  fetchPredictionsDebounced()
}

let debounceId = null
function fetchPredictionsDebounced() {
  if (debounceId) clearTimeout(debounceId)
  debounceId = setTimeout(fetchPredictions, 200)
}

function fetchPredictions() {
  if (!form.address.trim()) return

  const req = {
    input: form.address,
    sessionToken,
    componentRestrictions: { country: 'AU' },
    types: ['address'],
  }

  acSvc.getPlacePredictions(req, (res, status) => {
    if (status !== google.maps.places.PlacesServiceStatus.OK || !res) {
      predictions.value = []
      showDropdown.value = false
      return
    }
    predictions.value = res
    activeIndex.value = -1
    showDropdown.value = true
  })
}

function selectPrediction(p) {
  form.address = p.description
  predictions.value = []
  showDropdown.value = false
  newSession()
}

function moveActive(delta) {
  const len = predictions.value.length
  if (!len) return
  activeIndex.value = (activeIndex.value + delta + len) % len
}

function confirmActive() {
  if (activeIndex.value >= 0 && activeIndex.value < predictions.value.length) {
    selectPrediction(predictions.value[activeIndex.value])
  }
}

function hideDropdown() {
  showDropdown.value = false
  activeIndex.value = -1
}

function formatPrimary(p) {
  const sf = p.structured_formatting
  if (!sf) return p.description
  let text = sf.main_text
  if (sf.main_text_matched_substrings?.length) {
    const [{ offset, length }] = sf.main_text_matched_substrings
    const a = text.slice(0, offset)
    const b = text.slice(offset, offset + length)
    const c = text.slice(offset + length)
    return `${a}<strong>${b}</strong>${c}`
  }
  return text
}

function handleClickOutside(e) {
  if (!dropdownRef.value?.contains(e.target)) {
    hideDropdown()
  }
}

function loadGoogleMapsScript() {
  return new Promise((resolve, reject) => {
    if (window.google?.maps) return resolve()
    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}&libraries=places`
    script.async = true
    script.defer = true
    script.onload = resolve
    script.onerror = () => reject(new Error('Google Maps script failed to load'))
    document.head.appendChild(script)
  })
}

onMounted(async () => {
  await loadGoogleMapsScript()
  loadGoogle()
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

</script>

<style scoped>
.green-page { background-color: #faffe8; min-height: 100vh; }
.page { font-family: "Arial", sans-serif; }
.hero { height: 75vh; position: relative; overflow: hidden; }
.hero-img { width: 100%; height: 100%; object-fit: cover; }
.overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; flex-direction: column; color: white; text-align: center; }
.title { font-size: 2.5rem; font-weight: bold; }
.subtitle { font-size: 1.2rem; margin-top: 0.5rem; }
.how-it-works { margin-top: 3rem; text-align: center; }
.how-it-works h2 { font-size: 2rem; margin-bottom: 2rem; color: #2d6a4f; }
.steps { display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; }
.step { flex: 1 1 200px; max-width: 220px; }
.step img { width: 80px; height: 80px; object-fit: contain; margin-bottom: 1rem; }
.step p { font-size: 0.95rem; color: #333; }
.upload-btn-wrapper { margin-top: 2.5rem; text-align: center; }
.upload-btn { background: black; color: white; font-size: 1.1rem; padding: 0.8rem 2rem; border: none; border-radius: 8px; cursor: pointer; transition: background 0.3s; }
.upload-btn:hover { background: #333; }
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: grid; place-items: center; z-index: 999; }
.modal-card { width: min(720px, 92vw); background: #fff; border: 1px solid #222; border-radius: 8px; padding: 24px 24px 16px; position: relative; }
.modal-close { position: absolute; top: -14px; right: -14px; width: 36px; height: 36px; border-radius: 999px; border: 1px solid #d9d9d9; background: #fff; display: grid; place-items: center; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,.12); z-index: 3; }
.modal-close svg { display: block; }
@media (max-width: 480px) { .modal-close { top: 8px; right: 8px; } }
.step-pane { display: grid; gap: 16px; }
.dropzone { border: 2px dashed #333; border-radius: 8px; min-height: 220px; display: grid; place-items: center; padding: 16px; }
.upload-grid { display: grid; grid-template-columns: 1fr; gap: 18px; }
.dropzone.is-filled { border-style: solid; }
.dz-inner { text-align: center; }
.dz-icon { margin-bottom: 8px; }
.dz-icon svg { width: 36px; height: 36px; }
.dz-or { margin: 8px 0; color: #888; }
.select-btn { background: #bdbdbd; border: none; padding: 8px 14px; border-radius: 18px; cursor: pointer; }
.hidden-input { display: none; }
.step-actions { display: flex; justify-content: flex-end; }
.circle-btn { width: 40px; height: 40px; border-radius: 999px; border: 1px solid #222; background: #fff; cursor: pointer; display: inline-grid; place-items: center; }
.circle-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.icon { display: block; }
.form-field { display: grid; gap: 6px; }
.label { font-weight: 600; }
.address-row { position: relative; }
.address-row input { width: 100%; padding-left: 38px; }
.addr-icon { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: #666; display: inline-flex; align-items: center; justify-content: center; pointer-events: none; }
.addr-icon svg { width: 18px; height: 18px; }
.error { color: #d12; font-size: 12px; margin-top: -2px; }
.actions-row { display: flex; gap: 12px; justify-content: center; margin-top: 8px; }
.primary-btn { background: #111; color: #fff; padding: 8px 18px; border-radius: 18px; border: none; cursor: pointer; }
.primary-btn:disabled { opacity: 0.5; cursor: not-allowed; }
@media (max-width: 720px) { .upload-grid { grid-template-columns: 1fr; } }
.result-wrap { padding: 56px 6vw 80px; }
.result-header { margin-bottom: 18px; }
.result-title { font-size: 2rem; margin-bottom: 4px; }
.result-sub { color: #333; }
.result-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; align-items: start; margin-top: 18px; }
.result-photo img { max-width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; }
.result-cards { display: grid; gap: 16px; }
.check-card { border: 1px solid #ddd; border-radius: 12px; padding: 16px; background: #f7faf7; }
.check-card.bad { background: #fdeeee; }


.badge { display: inline-flex; align-items: center; gap: 8px; margin-top: 10px; padding: 6px 10px; border-radius: 999px; font-size: 0.9rem; }
.b-ok { background: #dff4e6; color: #0a6b3b; }
.b-bad { background: #ffe0e0; color: #9c1a1a; }
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-top: 22px; }
.metric { border: 1px solid #e6e6e6; border-radius: 8px; padding: 14px; background: #fff; }
.m-value { font-size: 1.4rem; margin: 6px 0; }
.m-sub { color: #666; }
@media (max-width: 980px) { .result-grid { grid-template-columns: 1fr; } .metric-row { grid-template-columns: 1fr 1fr; } }
@media (max-width: 560px) { .metric-row { grid-template-columns: 1fr; } }
.tc-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 10px; }
.tc-link { border: none; background: transparent; text-decoration: underline; color: #2d6a4f; cursor: pointer; padding: 4px 6px; border-radius: 6px; }
.tc-panel { margin-top: 10px; border: 1px solid #e6e6e6; border-radius: 8px; background: #fff; padding: 12px; max-height: 240px; overflow: auto; }
.tc-content h4 { margin: 0 0 8px 0; font-size: 1rem; }
.tc-content ul { margin: 0; padding-left: 18px; }
.tc-actions { display: flex; justify-content: flex-end; margin-top: 10px; }
.tc-close { background: #111; color: #fff; padding: 6px 12px; border: none; border-radius: 16px; cursor: pointer; }
.accordion-enter-from, .accordion-leave-to { max-height: 0; opacity: 0; }
.accordion-enter-to, .accordion-leave-from { max-height: 240px; opacity: 1; }
.accordion-enter-active, .accordion-leave-active { transition: max-height 0.25s ease, opacity 0.25s ease; }
.dz-preview { max-width: 100%; max-height: 300px; object-fit: contain; }
.dz-actions { text-align: center; }
.autocomplete-list { position: absolute; z-index: 999; width: 100%; background: #fff; border: 1px solid #ccc; border-radius: 6px; max-height: 240px; overflow-y: auto; list-style: none; padding: 6px 0; margin: 2px 0 0; }
.autocomplete-list li { padding: 8px 12px; cursor: pointer; }
.autocomplete-list li.active,
.autocomplete-list li:hover { background: #f0f0f0; }
.primary { font-weight: bold; }
.secondary { font-size: 12px; color: #666; }
.check-card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
  background: #f7faf7;
  transition: box-shadow 0.3s;
}

.check-card.ok {
  background: #f0fdf4;
}

.check-card.bad {
  background: #fff5f5;
}

.card-body {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.check-icon-wrap {
  width: 48px;
  height: 48px;
  background-color: #e6e6e6;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  margin-top: 2px;
}

.check-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.check-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.check-title {
  font-weight: 700;
  font-size: 1rem;
  color: #111;
}

.check-sub {
  font-size: 0.875rem;
  color: #555;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  font-size: 0.85rem;
  border-radius: 999px;
  font-weight: 500;
  width: fit-content;
}

.b-ok {
  background: #e6f6eb;
  color: #107c41;
}

.b-bad {
  background: #ffe0e0;
  color: #9c1a1a;
}

.check-card:hover {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.metric {
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  padding: 14px;
  background: #fff;
}

.metric-icon-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.metric-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
  flex-shrink: 0;
}

.m-title {
  color: #222;
  font-weight: 600;
  font-size: 1rem;
  line-height: 1.2;
}

.m-value {
  font-size: 1.4rem;
  font-weight: 500;
  color: #111;
  margin: 6px 0;
}

.m-sub {
  color: #666;
  font-size: 0.875rem;
}
</style>

