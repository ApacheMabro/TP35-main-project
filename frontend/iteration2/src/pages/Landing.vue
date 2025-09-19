<template>
  <div class="landing">
    <!-- HERO (pinned) -->
    <section class="hero pinned">
      <!-- Background video -->
      <video class="hero-bg" autoplay muted loop playsinline poster="/leaf_hero.jpg">
        <source src="/leaf_hero.mp4" type="video/mp4" />
      </video>

      <!-- splash overlay that fades out -->
      <div v-if="showSplash" class="splash over-video" :class="{ done: splashDone }">
        <img class="tree" src="@/assets/leaf_hero.jpg" alt="Tree" />
      </div>

      <!-- Overlay to make text readable -->
      <div class="overlay"></div>

      <!-- Hero content -->
      <div class="hero-content">
        <h1>Are You Living Green Enough?</h1>
        <p>Upload your view, get your Green Score, and uncover how your surroundings affect your health and happiness.
        </p>

        <!-- cta button -->
        <div class = "cta-button"> 
          <button class="btn" @click="goNext('upload')">
            <span>Upload My Window View</span>
          </button>

          <button class="btn" @click="goNext('why')">
            <span>Find out why</span>
          </button>
        </div>

      </div>

      <!-- grows from bottom to top to COVER the hero (GSAP controls scaleY) -->
      <div class="cover" aria-hidden="true"></div>

      <!-- chevron points to services -->
      <a href="#services" class="scroll-down" aria-label="Scroll down">
        <svg width="36" height="36" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M19 9l-7 7-7-7" />
        </svg>
      </a>
    </section>

    <!-- Spacer: gives the page 1 viewport of scroll so the next section can cover the fixed hero -->
    <div class="hero-spacer" aria-hidden="true"></div>


    <!-- SERVICES -->
    <section id="services" class="cover services">
      <h2 class="services-title">Our Service</h2>
      <p class="services-sub">Explore how you can learn about living greener</p>

      <div class="services-wrap">
        <!-- arrows -->
        <button class="nav prev" ref="prevEl" aria-label="Previous">‹</button>
        <button class="nav next" ref="nextEl" aria-label="Next">›</button>

        <!-- Swiper -->
        <Swiper ref="swiperRef" :modules="[Navigation]" :navigation="{ prevEl: prevEl, nextEl: nextEl }"
          :space-between="20" :slides-per-view="1.1" :breakpoints="{
            640: { slidesPerView: 1.4 },
            768: { slidesPerView: 2 },
            1024: { slidesPerView: 3 }
          }" :speed="450" @after-init="onInit" @slide-change="onSlideChange" class="services-swiper">
          <SwiperSlide v-for="(s, i) in services" :key="i">
            <article class="card" :data-idx="i">
              <img class="thumb" :src="s.img" :alt="s.title" />
              <div class="body">
                <h3>{{ s.title }}</h3>
                <p class="desc">{{ s.desc }}</p>
                <button class="btn small" @click="s.action()">{{ s.cta }}</button>
              </div>
            </article>
          </SwiperSlide>
        </Swiper>
      </div>
    </section>

    <section id="rule-330300" class="cover rule">
      <div class="rule-wrap">
        <h2 class="rule-title">
          Understanding the <span class="accent">3-30-300 Rule</span>
        </h2>
        <p class="rule-sub">
          A science-based framework used by urban planners to ensure everyone has
          adequate access to nature for health and wellbeing.
        </p>

        <!-- 3 cards -->
        <div class="rule-grid">
          <article class="rule-card">
            <!-- <img class="icon" :src="new URL('@/assets/green.jpg', import.meta.url)"  /> -->
            <h3><strong>3</strong><br> Trees from your window</h3>
            <p>You should be able to see at least 3 trees from your home window for mental wellbeing and connection to
              nature.</p>
          </article>

          <article class="rule-card">
            <!-- <img class="icon" :src="new URL('@/assets/green.jpg', import.meta.url)"  /> -->
            <h3><strong>30%</strong><br> Neighbourhood canopy</h3>
            <p>Your local area needs 30% tree canopy coverage to reduce urban heat and improve air quality.</p>
          </article>

          <article class="rule-card">
            <!-- <img class="icon" :src="new URL('@/assets/green.jpg', import.meta.url)"  /> -->
            <h3><strong>300m</strong><br> Green space access</h3>
            <p>A quality green space should be within 300 metres (5–10 min walk) for regular nature contact.</p>
          </article>
        </div>

        <!-- why this matter for melbourne -->
        <aside class="rule-callout">
          <div class="tag" aria-hidden="true">!</div>
          <div>
            <h4>Why this matters for Melbourne</h4>
            <p>
              🔥🔥🔥Melbourne is heating up 🔥🔥🔥
            </p>
            <p>
              Some suburbs are up to 12°C hotter than leafy areas.
            </p>
          </div>
        </aside>
      </div>
    </section>

    <!-- nature is missing -->
    <section id="nature-missing" class="nature">
    <div class="nature-wrap">
      <h2>Nature Is Missing from Our Community</h2>
      <p>
        Our cities need more nature. Trees and parks help cool streets, improve health,
        and create sustainable, livable communities where everyone can thrive
      </p>

      <div class="nature-stats">
        <div><strong>75%</strong><br>Melbourne areas NOT have enough tree cover</div>
        <div><strong>5.3M+</strong><br>Population of people living in Melbourne</div>
        <div><strong>30</strong><br>Median age in the City of Melbourne</div>
        <div><strong>86%</strong><br>Residents are calling for more green spaces</div>
      </div>
    </div>
  </section>

    <!-- footer -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, nextTick } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import gsap from 'gsap'
import Footer from '@/components/Footer.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goNext = (type) => {
  if (type === 'upload') {
    router.push({ name: 'upload_window' })   
  } else if (type === 'why') {
    window.open("https://greenlifeindustryqld.org.au/news/3-30-300-rule/", "_blank")
  }
}

const showSplash = ref(false)
const splashDone = ref(false)

onMounted(() => {
  // If you came from step3 with a splash request, e.g. ?splash=1
  const hasSplash = new URLSearchParams(location.search).get('splash') === '1'
  if (!hasSplash) return

  showSplash.value = true
  setTimeout(() => { splashDone.value = true }, 1200)  // start fade
  setTimeout(() => { showSplash.value = false }, 1700) // remove from dom
})

// tiny fade/blur effect on scroll using CSS var (no library)
onMounted(() => {
  const onScroll = () => {
    const y = Math.min(window.scrollY, window.innerHeight)
    const p = y / window.innerHeight // 0 -> 1 while covering
    document.documentElement.style.setProperty('--hero-progress', p.toString())
  }
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})

// card carousel
const swiperRef = ref(null)
const prevEl = ref(null)
const nextEl = ref(null)

const services = [
  {
    // first service
    img: new URL('@/assets/our-service-window.png', import.meta.url),
    title: 'Check your green score',
    desc: 'Is your home green enough? Upload a photo and find out — trees, cover, and parks measured by the 3-30-300 rule.',
    cta: 'Upload my window',
    action: () => router.push({ name: 'upload_window' })
  },
  {
    // second service
    img: new URL('@/assets/our-service-heat.png', import.meta.url),
    title: 'Check your suburb heat',
    desc: 'Is your suburb overheating? Cities lose plants, gain concrete, and lock in heat — the Urban Heat Island Effect.',
    cta: 'Check suburb heat',
    action: () => router.push({ name: 'heatmap' })
  },
  {
    // third service
    img: new URL('@/assets/our-service-planth-health.png', import.meta.url),
    title: 'Keep your plant alive',
    desc: 'Got a struggling plant? Snap it, get instant tips, and bring the green back into your space.',
    cta: 'Open Plant Health',
    action: () => router.push({ name: 'plant_health' })
  },
  {
    // fourth service
    img: new URL('@/assets/our-service-plant-suggestion.png', import.meta.url),
    title: 'Find Your Green Companion',
    desc: 'Discover 3 plants made for you. Shuffle for more and learn how to care for them with ease.',
    cta: 'My Green Picks',
    action: () => router.push({ name: 'intro-step2' })
    // the page have not created
  },
  {
    // fifth service
    img: new URL('@/assets/our-service-ct-mel.png', import.meta.url),
    title: 'Raise your voice',
    desc: 'Your voice matters! Request more green space and vote for the next green laneway to cool our city. We want to hear from you!',
    cta: 'Contact council',
    action: () => router.push({ name: 'intro-step2' })
    // the petition page have not created
  },

]

onMounted(() => {
  const cards = document.querySelectorAll('.services-swiper .card')

  cards.forEach((card) => {
    card.addEventListener('mouseenter', () => {
      gsap.to(card, {
        scale: 1.05,
        y: -8,
        boxShadow: '0 16px 32px rgba(0,0,0,0.15)',
        duration: 0.3,
        ease: 'power3.out'
      })
    })
    card.addEventListener('mouseleave', () => {
      gsap.to(card, {
        scale: 1,
        y: 0,
        boxShadow: '0 10px 24px rgba(0,0,0,0.1)',
        duration: 0.3,
        ease: 'power3.out'
      })
    })
  })
})

</script>

<style scoped>
/* entry splash */
.splash.over-video{
  position: fixed; inset:0; z-index: 5;         /* above video, below hero text if you want */
  background: #F8FEF6; display:grid; place-items:center;
  transition: opacity .5s ease;
}
.splash.over-video.done{ opacity: 0; pointer-events: none;  }

.splash .tree{
  width: 200px; animation: grow 1.2s ease-out forwards;
}
@keyframes grow{
  0% { transform: scale(.7); opacity: 0; }
  60% { transform: scale(1.06); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}

:root {
  /* 0 at top, 1 when the next section fully covers the hero */
  --hero-progress: 0;
}

/* ===== HERO (pinned) ===== */
.hero.pinned {
  position: fixed;
  inset: 0;
  z-index: 0;
}

.hero-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  object-fit: cover;
}

.overlay {
  pointer-events: none;
  position: absolute;
  inset: 0;
  z-index: 1;
  background: rgba(0, 0, 0, calc(0.35 + 0.25 * var(--hero-progress)));
  transition: background 0.2s linear;
  
}

.hero-content {
  position: relative;
  z-index: 3;
  text-align: center;
  color: #ffffff;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1.25rem;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  min-height: 100vh;
  gap: 1rem;

  opacity: calc(1 - 0.75 * var(--hero-progress));
  transform: translateY(calc(-10px * var(--hero-progress)));
  transition: opacity 0.2s linear, transform 0.2s linear;
}

.cta-button {
  display: flex;
  gap: 20px;               
  justify-content: center; 
  align-items: center;
}

.btn {
  background: transparent;   /* transparent background */
  color: white;              
  border: 2px solid white;   /* white border */
  border-radius: 8px;        /* rounded corners */
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:hover {
  background: white;   /* hover effect */
  color: black;
}

/* hero wording */
h1 {
  font-size: clamp(2rem, 4.5vw, 3.5rem);
  line-height: 1.1;
}

h2 {
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  margin-bottom: 1rem;
}

p {
  max-width: 60ch;
  margin: 0 auto 1rem;
}

/* ===== COVER SECTIONS (scrolling content) ===== */
.cover {
  position: relative;
  z-index: 1;
  /* above the fixed hero */
  background: #F8FEF6;
  min-height: 80vh;
  padding: 6rem 1.5rem;
}

/* Creates the initial scroll area so the next section can slide over the fixed hero */
.hero-spacer {
  height: 100vh;
}


/* SERVICES */
.services {
  padding-top: 4rem;
  padding-bottom: 5rem;
}

.services-title {
  text-align: center;
  font-size: clamp(1.6rem, 2.5vw, 2.2rem);
  margin-bottom: .25rem;
}

.services-sub {
  text-align: center;
  color: #566;
  margin-bottom: 1.5rem;
}

.services-wrap {
  position: relative;
  max-width: 1100px;
  margin: 0 auto;
}

.services-swiper .swiper-wrapper {
  display: flex;
  justify-content: center;
}

/* arrows */
.nav {
  position: absolute;
  top: 42%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 999px;
  border: 1px solid #cfd9d4;
  background: #fff;
  cursor: pointer;
  z-index: 3;
  display: grid;
  place-items: center;
  font-size: 22px;
  line-height: 1;
  box-shadow: 0 4px 14px rgba(0, 0, 0, .07);
}

.nav:hover {
  background: #f7fbf9;
}

.nav.prev {
  left: -8px;
}

.nav.next {
  right: -8px;
}

/* cards */
.services-swiper {
  max-width: 1000px;
  margin: 0 auto;
  padding: .5rem 1.25rem;
}

.card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transform-origin: center;
  transition: box-shadow .3s ease;

  width: 300px;
  height: 380px;
  display: flex;
  flex-direction: column;
}

.card .thumb {
  width: 100%;
  height: 170px;
  object-fit: cover;
  display: block;
}

.card .body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 14px 14px 16px;
}

.card h3 {
  font-size: 1rem;
  margin: 0 0 .35rem;
}

.card .desc {
  font-size: .9rem;
  color: #4c5a53;
  line-height: 1.45;
  min-height: 3.5em;
  margin-bottom: .75rem;
}

.btn.small {
  padding: .5rem .75rem;
  font-size: .9rem;
  border-radius: 10px;
  background: #103731;
  color: #fff;
  border: none;
  cursor: pointer;
}

.btn.small:hover {
  filter: brightness(1.05);
}

.cover.services {
  min-height: 100vh;
  display: grid;
  place-content: center;
  padding: 3rem 1.5rem;
  background: #F8FEF6;
}

/* 3-30-300 */
.cover.rule {
  background: #ffffff;
  padding: 20rem 2rem;

}

.rule-wrap {
  max-width: 1100px;
  margin: 0 auto;
  border-radius: 16px;
  padding: 3rem 2rem;
  box-shadow: 0 8px 30px rgba(0,0,0,0.2); 
  border: 1px solid #e6e6e6;
}

.rule-title {
  text-align: center;
  font-size: clamp(1.6rem, 2.8vw, 2.2rem);
  margin: 0 0 .25rem;
}

.rule-title .accent {
  color: #0f7b4a;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.rule-sub {
  text-align: center;
  color: #5b6963;
  max-width: 60ch;
  margin: 0 auto 2rem;
}

/* grid of 3 cards */
.rule-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
  margin-bottom: 1.25rem;
}

@media (max-width: 900px) {
  .rule-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .rule-grid {
    grid-template-columns: 1fr;
  }
}

.rule-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px 18px;
  display: flex;
  flex-direction: column;
  text-align: center;
  gap: 10px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, .08);
  transition: transform .25s ease, box-shadow .25s ease;
  min-height: 210px;
}

.rule-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, .12);
}

.rule-card .icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  font-size: 20px;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .06);
}

.rule-card .icon.blue {
  background: #edf3ff;
}

.rule-card .icon.green {
  background: #eaf7ee;
}

.rule-card .icon.teal {
  background: #e9f8f3;
}

.rule-card h3 {
  line-height: 1.2;
  margin: 4px 0 2px;
  font-size: 1.05rem;
}

.rule-card p {
  color: #4c5a53;
  margin: 0;
}

/* callout */
.rule-callout {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 12px;
  background: #FAF0F0;
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, .06);
  border: 1px solid #e6eee9;
}

.rule-callout .tag {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: grid;
  place-items: center;
  background: #ffedd5;
  color: #b45309;
  font-weight: 700;
}

.rule-callout h4 {
  margin: 0 0 4px;
  font-size: 1rem;
}

.rule-callout p {
  margin: 0;
  color: #4c5a53;
}


/* nature is missing */
.nature {
  background: linear-gradient(135deg, #1a7733, #77a947);
  color: #fff;
  padding: 4rem 1.5rem;
  position: relative;   
  
}

.nature-wrap {
  max-width: 1100px;
  margin: 0 auto;
  text-align: center;
}

.nature h2 {
  font-size: clamp(1.8rem, 3vw, 2.2rem);
  margin-bottom: 1rem;
}

.nature p {
  max-width: 60ch;
  margin: 0 auto 2rem;
  opacity: 0.9;
}

.nature-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.nature-stats strong {
  font-size: 1.8rem;
}

@media (max-width: 800px) {
  .nature-stats { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 500px) {
  .nature-stats { grid-template-columns: 1fr; }
}

footer {
  position: relative;
  z-index: 2;
}
</style>
