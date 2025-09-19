<template>
  <main class="intro">

    <section class="center">
      <!-- BACKGROUND -->
      <img ref="bgEl" class="art bg" src="@/assets/BACKGROUND.png" alt="Decorative blob background" />
      <!-- PHONE OVERLAY -->
      <img ref="phoneEl" class="art phone" src="@/assets/step1.png" alt="Hand holding phone" />

      <h2 ref="titleEl">Are You Living in a Green Place?</h2>
      <p class="sub" ref="subEl">Snap your window to see your 3-30-300 check</p>

      <!-- button -->
      <button ref="btnEl" class="btn" data-flip-id="continue" @click="goNext">
        <span>Continue</span>
        <span class="arrow">→</span>
      </button>
      <RouterLink class="skip mt-3" :to="{ name: 'landing', query: { splash: 1 } }">SKIP</RouterLink>
    </section>
  </main>
</template>

<script setup>
import { onMounted, nextTick, ref } from 'vue'
import { useRouter } from 'vue-router'
import { gsap } from 'gsap'

const router = useRouter()
const goNext = () => router.push('/intro/step2')

const btnEl = ref(null)
const bgEl = ref(null)
const phoneEl = ref(null)
const titleEl = ref(null)
const subEl = ref(null)

onMounted(async () => {
  await nextTick()

  // Respect reduced motion
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReduced) {
    gsap.set([bgEl.value, phoneEl.value, titleEl.value, subEl.value], {
      clearProps: 'all',
      opacity: 1,
      y: 0,
      scale: 1,
      rotation: 0,
    })
    return
  }

  const tl = gsap.timeline({ defaults: { ease: 'power2.out' } })

  // 1) Background enters first
  tl.from(bgEl.value, {
    opacity: 0,
    scale: 0.85,
    duration: 0.9,
  })

  // 2) Phone slides up with a subtle swing
  tl.from(
    phoneEl.value,
    {
      y: 180,
      rotation: -6,
      opacity: 0,
      duration: 1.1,
      ease: 'back.out(1.4)',
    },
    '-=0.25',
  ) // slight overlap for flow

  // 3) Text lifts in
  tl.from(
    [titleEl.value, subEl.value],
    {
      y: 20,
      opacity: 0,
      duration: 0.5,
      stagger: 0.08,
    },
    '-=0.4',
  )
})
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
  display: block;
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
  width: min(520px, 86vw);
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
  margin-top: 16px;
  cursor: pointer;
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
