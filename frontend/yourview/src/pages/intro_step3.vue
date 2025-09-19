<template>
  <main class="intro">

    <section class="center">
       <!-- BACKGROUND -->
      <img ref="bgEl" class="art bg" src="@/assets/BACKGROUND.png" alt="Decorative blob background" />
      <!-- PHONE OVERLAY -->
      <img ref="phoneEl" class="art phone" src="@/assets/step3.png" alt="Hand holding phone" />

      <h2 ref="titleEl">No Green View? You Can Change That!</h2>
      <p class="sub" ref="subEl">plant, explore, speak up - building a greener city for all.</p>

      <!-- button -->
      <button ref="btnEl" class="btn" data-flip-id="continue" @click="goNext">
        <span>Visit Home Page</span>
        <span class="arrow">→</span>
      </button>
      <span style="height:36px;">&nbsp;</span>
    </section>
  </main>
</template>

<script setup>
import { onMounted, nextTick, ref } from 'vue'
import { useRouter } from 'vue-router'


const router = useRouter()
const goNext = () => router.push({ name: 'landing', query: { splash: 1 } })

const btnEl = ref(null)
const bgEl = ref(null)
const phoneEl = ref(null)
const titleEl = ref(null)
const subEl = ref(null)

</script>

<style scoped>
.intro {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Full viewport height */
  background: #f8fef6;
  padding-inline: clamp(16px, 4vw, 32px);

}

.center {
  position: relative;
  align-self: center;
  justify-self: center;
  text-align: center;
   display: flex;
  flex-direction: column;
  gap: 8px; /* <--- this gives 16px vertical space */
  text-align: center;
  width: min(520px, 80vw);
}

.art {
  width: 100%;
  max-height: 52vh;
  object-fit: contain;
  margin: 0 auto 16px;
}

/* Layering */
.bg {
  position: relative;
  z-index: 1;
}

.phone {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  /* center horizontally */
  width: 100%;
  /* smaller than bg so bg shows around */
  z-index: 2;
  transform-origin: 50% 80%;
  pointer-events: none;
}

h2 {
  margin: 6px 0 4px;
  color: #103713;
  font-size: clamp(20px, 3.6vw, 28px);
  font-weight: 800;
}

.sub {
  margin: 0;
  color: #103713;
  opacity: 0.9;
  font-size: 14px;
}

/* Fixed, solid button */
.btn {
  width: 100%;
  height: 48px;
  border: none;
  border-radius: 12px;
  background: #103731;
  /* solid color (no var()) */
  color: #fff;
  /* readable text */
  font-weight: 700;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  margin-top: 16px;
  box-shadow:
    0 2px 0 rgba(0, 0, 0, 0.08),
    0 10px 24px rgba(17, 60, 46, 0.22);
  transition:
    background 0.15s ease,
    transform 0.06s ease;
}

.btn:hover {
  background: #0c2a22;
  transform: scale(1.05);
}

.btn:active {
  transform: translateY(1px);
}
</style>
