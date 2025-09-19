<template>
  <div class="page-wrapper">
    <!-- Header -->
    <Header />

    <!-- Page content -->
    <main>
      <h1 class="title">Window Gallery</h1>

      <!-- Grid -->
      <ul class="grid" aria-live="polite">
        <!-- images -->
        <li v-for="it in items" :key="it.key" class="card">
          <img
            :src="it.url"
            :alt="it.key.split('/').pop() || 'Window view'"
            loading="lazy"
          />
        </li>

        <!-- skeletons -->
        <li v-if="loading" v-for="n in 6" :key="'sk'+n" class="card skel" />
      </ul>

      <!-- error & actions -->
      <p v-if="error" class="err">{{ error }}</p>
      <button v-if="token && !loading" class="btn" @click="fetchPage(false)">Load more</button>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

// --- AWS SDK (v3) ---
import { S3Client, ListObjectsV2Command, GetObjectCommand } from '@aws-sdk/client-s3'
import { fromCognitoIdentityPool } from '@aws-sdk/credential-providers'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'


// VITE_COGNITO_ID_POOL=ap-southeast-2:xxxx-xxxx-xxxx-xxxx
const REGION = import.meta.env.VITE_AWS_REGION || 'ap-southeast-2'
const BUCKET = import.meta.env.VITE_S3_BUCKET
const ID_POOL = import.meta.env.VITE_COGNITO_ID_POOL
const PREFIX = 'YourWindow/'

const s3 = new S3Client({
  region: REGION,
  credentials: fromCognitoIdentityPool({
    clientConfig: { region: REGION },
    identityPoolId: ID_POOL
  })
})

const items = ref([]) // { key, url, size?, lastModified? }
const token = ref(undefined)
const loading = ref(false)
const error = ref(null)

async function fetchPage(initial = false) {
  if (loading.value) return
  loading.value = true
  error.value = null
  try {
    const out = await s3.send(new ListObjectsV2Command({
      Bucket: BUCKET,
      Prefix: PREFIX,
      ContinuationToken: initial ? undefined : token.value,
      MaxKeys: 30
    }))

    const list = (out.Contents ?? []).filter(o => o.Key && !o.Key.endsWith('/'))
    const page = []
    for (const o of list) {
      const key = o.Key
      const url = await getSignedUrl(
        s3,
        new GetObjectCommand({ Bucket: BUCKET, Key: key }),
        { expiresIn: 1800 }
      )
      page.push({
        key,
        url,
        size: o.Size,
        lastModified: o.LastModified?.toISOString?.()
      })
    }
    items.value.push(...page)
    token.value = out.IsTruncated ? out.NextContinuationToken : undefined
  } catch (e) {
    error.value = e?.message || String(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchPage(true))
</script>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  padding: 24px;
}

.title {
  margin: 0 0 12px;
  font-size: 28px;
  font-weight: 900;
  color: #064e3b;
}

/* grid */
.grid {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 14px;
  grid-template-columns: 1fr;
}
@media (min-width: 680px) { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 980px) { .grid { grid-template-columns: repeat(3, 1fr); } }

.card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  min-height: 220px;
}
.card img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  max-height: 360px;
}

/* skeleton */
.skel {
  background: linear-gradient(90deg,#eee 25%,#f6f6f6 50%,#eee 75%);
  background-size: 200% 100%;
  animation: sh 1.1s infinite;
}
@keyframes sh {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.btn {
  margin: 16px auto 0;
  display: block;
  padding: 10px 16px;
  border-radius: 9999px;
  border: 2px solid #064e3b;
  background: #064e3b;
  color: #fff;
  font-weight: 800;
  cursor: pointer;
}

.err { color: #b91c1c; margin-top: 10px; }
</style>
