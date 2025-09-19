<template>
  <main class="landing">
    <!-- logo -> header -> btn -> term -->

    <!-- logo -->
    <figure ref="logoEl" class="logo">
      <img src="@/assets/logo_only.png" alt="" aria-hidden="true" />
    </figure>

    <!-- header -->
    <header class="brand">
      <h1 ref="titleEl" class="title">Welcome to YourView</h1>
      <p ref="taglineEl" class="tagline">Sustainable City of Melbourne</p>
      <p ref="taglineEl" class="tagline">Green spaces for all</p>
    </header>

    <!-- button -->
    <section class="cta">
      <button ref="btnEl" class="btn" data-flip-id="continue" @click="goNext">
        <span>Continue</span>
        <span class="arrow">→</span>
      </button>

      <!-- term -->
      <p ref="legalEl" class="legal">
        By clicking Continue, you agree to our
        <RouterLink to="/terms">Terms of Service</RouterLink>
        and confirm you have read our
        <RouterLink to="/privacy">Privacy Policy</RouterLink>.
      </p>
    </section>

    <!-- bush - bottom art-->
    <figure ref="illustrationEl" class="illustration">
      <!-- <img src="@/assets/intro_bush.png" alt="" aria-hidden="true" /> -->
    </figure>
  </main>
</template>

<script setup>
import { onMounted, ref, nextTick } from "vue"
import { gsap } from "gsap"
import Flip from 'gsap/Flip'
import { useRouter } from "vue-router"

const router = useRouter()
gsap.registerPlugin(Flip)

// Refs
const titleEl = ref(null)
const taglineEl = ref(null)
const btnEl = ref(null)
const legalEl = ref(null)
const illustrationEl = ref(null)
const logoEl = ref(null)

onMounted(() => {
  const tl = gsap.timeline({ defaults: { ease: "power3.out" } })

  tl.from(logoEl.value, { y: -10, opacity: 0, duration: 0.5, delay: 0.3 })
    .from(titleEl.value, { y: -50, opacity: 0, duration: 1 })
    .from(taglineEl.value, { y: 20, opacity: 0, duration: 0.8 }, "-=0.5")
    .from(btnEl.value, { scale: 1, opacity: 0, duration: 0.6, ease: "power3.out", clearProps: "transform" }, "-=0.3")
    .from(legalEl.value, { opacity: 0, duration: 0.8 }, "-=0.3")
    .from(illustrationEl.value, { opacity: 0, y: 40, duration: 1 }, "-=0.6")
})

const goNext = async () => {
  const state = Flip.getState('[data-flip-id="continue"]')

  await router.push({ name: 'intro-step1' })
  await nextTick()
  await new Promise(requestAnimationFrame)

  // animate old -> new
  Flip.from(state, {
    duration: 0.6,
    ease: 'power3.inOut',
    absolute: true, 
    nested: true,
    scale: true,
    simple: true
  })
}
</script>

<style scoped>

.landing {
  position: relative;
  min-height: 100dvh;
  background: #f8fef6;
  display: grid;
  grid-template-rows: 1fr auto auto auto 1fr;
  align-items: center;
  justify-items: center;
  padding: clamp(16px, 3vw, 32px);
  text-align: center;
  gap: var(--spacing-between-elements, clamp(16px, 4vh, 40px));
}

.logo {
  grid-row: 2;
  margin: 0;
}

.logo img {
  width: clamp(96px, 14vw, 180px);
  height: auto;
  display: block;
}

.brand {
  grid-row: 3;
  margin: 0;
}

h1 {
  color: #103713;
  font-size: clamp(28px, 6vw, 56px);
  line-height: 1.1;
  margin: 10px 0 8px;
  font-weight: 800;
}

.tagline {
  color: #103713;
  opacity: 0.9;
  font-weight: 600;
  margin: 0;
}

.cta {
  grid-row: 4;
  margin: 0;
  margin-top: clamp(24px, 5vh, 40px);
  max-width: 680px;
  width: min(92vw, 520px);
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
  cursor: pointer;
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.08), 0 10px 24px rgba(17, 60, 46, 0.22);
  transition: background 0.15s ease, transform 0.06s ease;
}

.btn:hover {
  background: #0c2a22;
  transform: scale(1.05);
}

.btn:active {
  transform: translateY(1px);
}

.arrow {
  font-size: 18px;
  margin-left: 6px;
}

.legal {
  margin: 10px auto 0;
  font-size: 12px;
  color: #103731;
  max-width: 520px;
  opacity: 0.9;
}

.legal a {
  color: #103731;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.illustration {
  width: 100%;
  max-width: none;
  margin: 0;
  position: absolute;
  bottom: 0;
  left: 0;
}

.illustration img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
}
</style>
