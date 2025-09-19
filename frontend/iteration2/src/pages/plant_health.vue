<template>
  <Header />
  <div class="page-wrapper">
    <div class="container">
      <h1 class="title">Track Your Plant Health With AI</h1>
      <h3 class="subtitle">
        Upload a photo and describe your plant — we’ll check how it’s doing and provide personalized care recommendations
      </h3>

      <form class="card" @submit.prevent="handleSubmit">

        <div v-if="result && !lowConfidence" class="status-strip">
          <div class="status-left">
            <div class="species" v-if="result?.species">
              {{ result.species }}
              <span v-if="result?.common_name" class="species-aka">({{ result.common_name }})</span>
            </div>
            <div class="status-big">
              {{ displayStatus }}
            </div>
          </div>
          <div class="score-box" v-if="result?.health_score">
            <span class="score-label">Health</span>
            <span class="score-value">{{ result.health_score }}</span>
          </div>
        </div>


        <div class="upload-box">
          <div v-if="previewUrl" class="preview inside-upload-box">
            <div>
              <img :src="previewUrl" alt="preview" />
            </div>
            <label class="upload-button" @click="resetPreview">
              <img src="@/assets/icon_camera.png" width="16" alt="Camera Icon" />
              <span>Change Photo</span>
            </label>
          </div>

          <div v-else class="inside-upload-box">
            <img src="@/assets/icon_upload.png" width="40" class="center-self" alt="" />
            <h2 class="upload-title">Upload a photo of your plant</h2>
            <label class="upload-button">
              <input type="file" accept=".jpg,.jpeg,.png,image/jpeg,image/png" @change="onFileSelected" hidden />
              <img src="@/assets/icon_camera.png" width="16" alt="Camera Icon" />
              <span>Choose Photo</span>
            </label>
          </div>
        </div>


        <button class="analyze-button" :disabled="!file || loading">
          <span v-if="!loading" class="btn-content">
            <img src="@/assets/icon_analyze.png" width="16" alt="Analyze Icon" />
            Analyze Plant Health
          </span>
          <span v-else class="btn-loading">
            <span class="spinner" aria-hidden="true"></span>
            Analyzing…
          </span>
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </form>


      <div v-if="lowConfidence" class="card warn-card">
        <p class="warn-big">Unable to analyze. Please upload photos of the plants.</p>
        <p class="warn-sub">
          We cannot confidently identify this image as a plant (Identification confidence ≤ 10%). 
          Please try to change to a clearer close-up of the plant.
        </p>
      </div>

      <!-- normal card -->
      <div v-if="result && !lowConfidence" class="card" style="margin-top:1rem;">
        <!-- Hidden but not deleted fields -->
        <ul class="kv" style="display:none;">
          <li v-if="result?.family">
            <strong>Family:</strong> {{ result.family }}
          </li>
          <li v-if="result?.confidence !== undefined">
            <strong>Identification confidence:</strong> {{ result.confidence }}%
          </li>
          <li v-if="result?.confidence_level">
            <strong>Assessment confidence:</strong> {{ result.confidence_level }}
          </li>
        </ul>

        <!-- Summary container -->
        <div v-if="result?.quick_summary" class="summary-card">
          <div class="summary-title">Summary</div>
          <p class="summary-text">{{ result.quick_summary }}</p>
        </div>

        <div class="accordion">
          <button class="acc-header" @click="openCare = !openCare">
            <span class="acc-left">
              <span class="bulb" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                  <path d="M9 21h6v-1H9v1zm3-20C7.925 1 5 3.925 5 7c0 2.013 1.004 3.784 2.536 4.873.51.363.922.84 1.183 1.404L9 14h6l.281-.723c.26-.564.672-1.041 1.183-1.404C17.996 10.784 19 9.013 19 7c0-3.075-2.925-6-7-6zm-3 17h6v-2H9v2z"/>
                </svg>
              </span>
              Care recommendations
            </span>
            <span class="chev">{{ openCare ? '−' : '+' }}</span>
          </button>
          <div v-show="openCare" class="acc-body">
            <ul class="green-bullets">
              <li v-for="(rec, idx) in filteredCare" :key="idx">
                <strong>{{ rec.category }}:</strong> {{ rec.recommendation }}
              </li>
            </ul>
          </div>
        </div>

        <div class="accordion">
          <button class="acc-header" @click="openMore = !openMore">
            <span>More details</span>
            <span class="chev">{{ openMore ? '−' : '+' }}</span>
          </button>
          <div v-show="openMore" class="acc-body">
            <div v-if="otherCare.length">
              <h4 class="subhead">More care tips</h4>
              <ul class="disc">
                <li v-for="(rec, idx) in otherCare" :key="idx">
                  <strong>{{ rec.category }}:</strong> {{ rec.recommendation }}
                </li>
              </ul>
            </div>

            <div v-if="result?.issues_identified?.length" class="mt8">
              <h4 class="subhead">Issues identified</h4>
              <ul class="disc">
                <li v-for="(it, idx) in result.issues_identified" :key="idx">
                  <strong>{{ it.type }}</strong> — {{ it.severity }}. {{ it.description }}
                  <span v-if="it.treatment"><em> Treatment:</em> {{ it.treatment }}</span>
                </li>
              </ul>
            </div>

            <div v-if="result?.healthy_reference" class="mt8">
              <h4 class="subhead">Healthy reference</h4>
              <p>{{ result.healthy_reference.description }}</p>
              <ul class="disc">
                <li v-for="(k, i) in result.healthy_reference.key_indicators" :key="i">• {{ k }}</li>
              </ul>
            </div>
          </div>
        </div>

        <p class="disclaimer">
          This is an AI-generated assessment for reference only. For professional advice about plant health, please consult a horticulture expert.
        </p>
      </div>
    </div>
  </div>
  <Footer />
</template>

<script setup>
/** === Replace these with your real endpoints === */
const UPLOADER_URL =
  'https://oelkz0pl2c.execute-api.ap-southeast-2.amazonaws.com/default/upload-image';
const DELETE_URL =
  'https://oelkz0pl2c.execute-api.ap-southeast-2.amazonaws.com/default/delete-object';
const PLANT_ANALYZER_URL =
  'https://efmnjv0lr3.execute-api.ap-southeast-2.amazonaws.com/plant-health';

import { computed, ref } from 'vue';
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';

const LOW_CONFIDENCE_THRESHOLD = 10; // ≤10% is considered unanalyzable and should be deleted

// state
const file = ref(null);
const previewUrl = ref(null);
const loading = ref(false);
const error = ref(null);
// const deleteInfo = ref(null); // 
const allowShow = ref(false);   // If you don't want it to be deleted by default, change it to true
const result = ref(null);
const lowConfidence = ref(false);

const openCare = ref(true);     // The first paragraph is expanded by default
const openMore = ref(false);    // The second paragraph is collapsed by default

// S3 folder name
const S3_FOLDER = 'PlantHealth';

// Display overall status, default to "Healthy" if missing/empty
const displayStatus = computed(() => {
  const s = result.value?.overall_status;
  return (typeof s === 'string' && s.trim()) ? s : 'Healthy';
});

// Care: Only show Watering/Light/Pruning
const filteredCare = computed(() => {
  const wanted = new Set(['Watering', 'Light', 'Pruning']);
  const list = result.value?.care_recommendations || [];
  return list.filter((x) => wanted.has(x?.category));
});
// Other care
const otherCare = computed(() => {
  const wanted = new Set(['Watering', 'Light', 'Pruning']);
  const list = result.value?.care_recommendations || [];
  return list.filter((x) => !wanted.has(x?.category));
});

function onFileSelected(e) {
  const f = e.target.files?.[0];
  error.value = null;
  result.value = null;
  lowConfidence.value = false;

  if (!f) {
    resetPreview();
    return;
  }
  const ok = /\.(jpe?g|png)$/i.test(f.name);
  if (!ok) {
    error.value = 'Only JPG and PNG are allowed.';
    return;
  }
  file.value = f;
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = URL.createObjectURL(f);
}

function resetPreview() {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = null;
  file.value = null;
  result.value = null;
  lowConfidence.value = false;
}

async function parseMaybeLambdaProxyResponse(res) {
  const data = await res.json().catch(() => null);
  if (!data) return null;
  if ('statusCode' in data && 'body' in data && typeof data.body === 'string') {
    try { return JSON.parse(data.body); } catch { return data; }
  }
  return data;
}

async function handleSubmit() {
  error.value = null;
  result.value = null;
  lowConfidence.value = false;

  if (!file.value) {
    error.value = 'Please choose a JPG or PNG file.';
    return;
  }

  loading.value = true;
  let uploadedBucket = '';
  let uploadedKey = '';

  try {
    // 1) Upload S3 uploader
    const form = new FormData();
    form.append('file', file.value);
    form.append('folder', S3_FOLDER);

    const uploadRes = await fetch(UPLOADER_URL, { method: 'POST', body: form });
    if (!uploadRes.ok) {
      const text = await uploadRes.text().catch(() => '');
      let detail = '';
      try { const j = JSON.parse(text); detail = j?.detail ?? ''; } catch {}
      throw new Error(detail || `Upload failed (${uploadRes.status})`);
    }
    const uploadJson = await uploadRes.json();
    uploadedBucket = uploadJson.bucket || uploadJson.s3_bucket || uploadJson.Bucket;
    uploadedKey    = uploadJson.key    || uploadJson.s3_key    || uploadJson.Key;
    if (!uploadedBucket || !uploadedKey) throw new Error('Upload did not return bucket/key.');

    // 2) plant-health-checker
    const analyzePayload = {
      bucket: uploadedBucket,
      key: uploadedKey,
      include_details: true,
      check_compliance: true
    };
    const analyzeRes = await fetch(PLANT_ANALYZER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(analyzePayload)
    });
    if (!analyzeRes.ok) {
      const text = await analyzeRes.text().catch(() => '');
      throw new Error(text || `Analyzer failed (${analyzeRes.status})`);
    }
    const analyze = await parseMaybeLambdaProxyResponse(analyzeRes) ?? {};

    // 3) Normalize result
    const species = analyze?.analysis_result?.species_identification;
    const sa = analyze?.analysis_result?.structured_analysis;
    const normalized = {
      species: species?.species,
      common_name: species?.common_name,
      family: species?.family,
      confidence: species?.confidence, // %
      overall_status: sa?.health_assessment?.overall_status,
      health_score: sa?.health_assessment?.health_score, // "7/10"
      confidence_level: sa?.health_assessment?.confidence_level,
      quick_summary: sa?.health_assessment?.quick_summary,
      care_recommendations: sa?.care_recommendations || [],
      issues_identified: sa?.issues_identified || [],
      healthy_reference: sa?.healthy_reference || null,
      raw: analyze
    };

    // 3.1) Low confidence: show warning + forced delete
    const conf = typeof normalized.confidence === 'number' ? normalized.confidence : NaN;
    if (!Number.isNaN(conf) && conf <= LOW_CONFIDENCE_THRESHOLD) {
      lowConfidence.value = true;
      // FORCE DELETE
      try {
        await fetch(DELETE_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ bucket: uploadedBucket, key: uploadedKey })
        });
      } catch (e) {
        console.warn('Forced delete (low-confidence) errored', e);
      }
      
      result.value = null;
      return;
    }

    // 3.2) Normal case: show result
    result.value = normalized;

    // 4) If not allowed to show, delete the uploaded file
    if (!allowShow.value) {
      try {
        await fetch(DELETE_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ bucket: uploadedBucket, key: uploadedKey })
        });
      } catch (e) {
        console.warn('Delete attempt errored', e);
      }
    }
  } catch (e) {
    error.value = e?.message || String(e);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background-image: url('/bg_plant_health_check.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.container {
  max-width: 800px;
  margin: auto;
  padding: 1rem;
}
.title {
  font-size: 2rem;
  margin-bottom: 1rem;
  text-align: center;
}
.subtitle {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  text-align: center;
  font-weight: normal;
  color: #616161;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.4;
}
.card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  margin-top: 1rem;
  background: #fff;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.status-strip {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  margin-bottom: 14px;
  border: 1px solid #bbf7d0;
  background: #ecfdf5;
  border-radius: 14px;
}
.status-left { display: flex; flex-direction: column; gap: 6px; }
.species { font-weight: 600; color: #065f46; font-size: 14px; }
.species-aka { color: #0f766e; font-weight: 500; margin-left: 6px; }
.status-big { font-weight: 800; color: #059669; font-size: 26px; line-height: 1.1; }
.score-box { display: flex; flex-direction: column; align-items: flex-end; justify-content: space-between; }
.score-label {
  color: #065f46; font-weight: 700; font-size: 12px; letter-spacing: .3px; text-transform: uppercase;
}
.score-value { color: #064e3b; font-weight: 900; font-size: 28px; }

/* Upload */
.upload-box {
  width: 100%;
  background: white;
  border: 2px dashed #e9e9e9;
  border-radius: 16px;
  padding: 32px;
}
.inside-upload-box { text-align: center; display: flex; flex-direction: column; gap: 16px; }
.upload-title { font-size: 20px; font-weight: bold; margin: 0; }
.upload-button {
  display: inline-flex; align-items: center; justify-content: center;
  margin: auto; gap: 8px; width: 100%; padding: 12px 16px;
  border: 1px solid #ccc; border-radius: 8px; background: #fff;
  cursor: pointer; font-size: 14px; font-weight: 500; transition: background 0.2s ease;
}
.upload-button:hover { background: #f1f1f1; }
.center-self { align-self: center; }
.preview img { max-width: 100%; max-height: 250px; object-fit: contain; }

/* Analyze animate */
.analyze-button {
  margin-top: 1.25rem;
  width: 100%;
  background: #103731;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.analyze-button:disabled { background: #b0d5cf; cursor: not-allowed; }
.btn-content { display: inline-flex; gap: 8px; align-items: center; }
.btn-loading { display: inline-flex; gap: 10px; align-items: center; }
.spinner {
  width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.4);
  border-top-color: #fff; border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.error { color: #b91c1c; margin-top: .75rem; }

/* Warning card */
.warn-card { border-color: #fecaca; background: #fff1f2; }
.warn-big { color: #b91c1c; font-weight: 800; margin: 0 0 4px; }
.warn-sub { color: #7f1d1d; margin: 0; }

/* Result card */
.kv { list-style: none; padding: 0; margin: .5rem 0 0; }
.kv li { margin: .2rem 0; }
.summary-card {
  margin-top: 10px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  border-radius: 12px;
  padding: 12px 14px;
}
.summary-title { font-weight: 800; color: #064e3b; margin-bottom: 6px; }
.summary-text { color: #1f2937; }

/* Accordion */
.accordion { border: 1px solid #e5e7eb; border-radius: 12px; margin-top: 12px; overflow: hidden; }
.acc-header {
  width: 100%; text-align: left; padding: 12px 14px; background: #fff;
  border: none; cursor: pointer; display: flex; align-items: center; justify-content: space-between;
  color: #064e3b; font-weight: 800;
}
.acc-body { padding: 10px 14px 12px; background: #fff; }
.acc-left { display: inline-flex; align-items: center; gap: 8px; }
.bulb { color: #059669; display: inline-flex; }
.chev { color: #065f46; }

.green-bullets { list-style: disc; padding-left: 20px; margin: 0; }
.green-bullets li::marker { color: #059669; }
.green-bullets li { margin: .2rem 0; }

.subhead { color: #065f46; font-weight: 800; margin-bottom: 6px; }
.disc { list-style: disc; padding-left: 20px; margin: 0; }
.mt8 { margin-top: 8px; }


.disclaimer {
  margin-top: 12px;
  font-size: 12px;
  color: #6b7280;
}

@media screen and (min-width: 1024px) {
  .container { padding: 3rem; }
  .upload-button { width: 300px; }
}
</style>
