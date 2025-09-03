<template>
  <div>
    <!-- Hero carousel -->
    <div class="carousel">
      <div
        class="carousel-track"
        :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
      >
        <div class="carousel-slide" v-for="(img, index) in backgroundimages" :key="index">
          <img :src="img" :alt="`Background ${index + 1}`" />
        </div>
      </div>

      <!--  Left overlay card -->
      <div class="hero-overlay">
        <div class="overlay-card">
          <h1 class="overlay-title">Turn Green Data Into Local Action</h1>

          <p class="overlay-text">
            Less than 25% of Melbourne has enough tree cover. You can check if your neighborhood
            meets the 3-30-300 standard.
          </p>

          <p class="overlay-text">
            YourView makes it simple to measure tree cover, find nearby parks, and show why your
            area deserves more green space.
          </p>

          <div class="overlay-actions">
            <RouterLink to="/yourwindow">
              <button class="btn btn-green">See My Green Score</button>
            </RouterLink>
            <RouterLink to="/yourarea">
              <button class="btn btn-amber">Check My Area Heat</button>
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Indicator dots -->
      <div class="carousel-dots">
        <span
          v-for="(dot, index) in backgroundimages"
          :key="index"
          class="dot"
          :class="{ active: index === currentIndex }"
          @click="goToSlide(index)"
        ></span>
      </div>
    </div>

    <!--  Content starts here -->
    <section class="content">
      <!-- Why It Matters -->
      <div class="why-section reveal">
        <h2>Why It Matters To You</h2>
        <div class="why-container">
          <img :src="images[3]" alt="Why It Matters" />
          <p>
            Melbourne residents do not have easy ways to check if their neighborhoods have enough trees and green spaces. Less green space effect your well-being, physical activities, and mental health.
            <br /><br />
            Research shows less than 25% of Melbourne areas have enough tree cover, and while 86% of people want more nature, they cannot measure their local environment or ask councils for improvements effectively (Croeser et al., 2024).
            <br /><br />
            Without simple tools to assess green spaces, residents cannot prove their area needs more trees or parks to stay cool and healthy. People cannot use data to convince councils to plant trees or create parks in their neighborhoods. Without easy to use environmental tools, residents stay stuck in hot areas with few trees and cannot fight for the green spaces they need. We're empowering residents with the first accessible tool to assess and advocate for green infrastructure using the 3-30-300 standard (3 trees visible, 30% tree cover, parks within 300m).
          </p>
        </div>
      </div>

      <!-- Our Stories -->
      <div class="stories reveal">
        <h2>Our Stories</h2>
        <div class="story-cards">
          <div class="card">
            <img :src="images[5]" alt="Maria" />
            <h3>Maria</h3>
            <p>“I just want shady walks to uni and a park to study in. With YourView,
              I can check if my area meets green standards and call for trees in my laneway.”</p>
          </div>
          <div class="card">
            <img :src="images[4]" alt="Abdul" />
            <h3>Abdul</h3>
            <p>“Hot, treeless streets exhaust me on my bike and make every delivery harder. With YourView,
              I can spot where shade is missing and push for cooler, safer routes for my health.”</p>
          </div>
          <div class="card">
            <img :src="images[6]" alt="Teacher" />
            <h3>Janet</h3>
            <p>“My students are stuck in concrete. With YourView,
              I get the data to fight for green school zones where kids can learn and play safely.”</p>
          </div>
        </div>
      </div>

      <!-- FAQ -->
      <div class="faq reveal">
        <h2>FAQ</h2>
        <div
          v-for="(item, index) in faqItems"
          :key="index"
          class="faq-item"
        >
          <div class="faq-question" @click="toggle(index)">
            <strong>{{ item.question }}</strong>
            <span class="arrow" :class="{ open: openIndex === index }">▼</span>
          </div>

          <transition name="faq">
            <div v-show="openIndex === index" class="faq-answer">
              {{ item.answer }}
            </div>
          </transition>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const images = [
  new URL('@/assets/background1.jpg', import.meta.url).href,
  new URL('@/assets/background2.jpg', import.meta.url).href,
  new URL('@/assets/background3.jpg', import.meta.url).href,
  new URL('@/assets/WhyMatter.png', import.meta.url).href,
  new URL('@/assets/Abdul.jpg', import.meta.url).href,
  new URL('@/assets/Maria.jpg', import.meta.url).href,
  new URL('@/assets/Janet.jpg', import.meta.url).href,
]
const backgroundimages = images.filter(img => img.includes("background"))
const currentIndex = ref(0)
let intervalId = null

onMounted(() => {
  // Carousel
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % backgroundimages.length
  }, 5000)

  // Cyclic IntersectionObserver for reveal sections
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show')
        } else {
          entry.target.classList.remove('show')
        }
      })
    },
    { rootMargin: '0px 0px -5% 0px' }
  )
  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el))
})

onUnmounted(() => {
  clearInterval(intervalId)
})

const goToSlide = (index) => {
  currentIndex.value = index
}

const openIndex = ref(null)
const faqItems = [
  { question: "Do I have to live in Melbourne?", answer: "No, anyone can use our website." },
  { question: "Why upload my window photo?", answer: "So we can measure tree visibility." },
  { question: "Where can I find the map?", answer: "On the homepage navigation bar." },
  { question: "Do you have a mobile app?", answer: "We are planning it soon." },
]
const toggle = (index) => {
  openIndex.value = openIndex.value === index ? null : index
}
</script>

<style scoped>
/* --- Carousel --- */
.carousel {
  position: relative;
  width: 100%;
  height: 75vh;
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.8s ease-in-out;
  width: 100%;
  height: 100%;
}

.carousel-slide {
  min-width: 100%;
  height: 100%;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/*  Overlay card on the left + entrance animation */
.hero-overlay {
  position: absolute;
  top: 10%;
  left: 6%;
  z-index: 3;
  width: min(520px, 86vw);
}

.overlay-card {
  background: rgba(255, 255, 255, 0.65);
  color: #0b1f16;
  border-radius: 0;
  padding: 100px 30px;
  min-height: 320px;
  width: min(800px, 92vw);
  box-shadow: 0 10px 32px rgba(0,0,0,.18);
  backdrop-filter: blur(4px);


  opacity: 0;
  transform: translateX(-10px) translateY(8px) scale(0.99);
  animation: overlayEnter .8s ease forwards .2s;
}


@keyframes overlayEnter {
  to {
    opacity: 1;
    transform: none;
  }
}

.overlay-title {
  font-size: clamp(20px, 3.2vw, 32px);
  font-weight: 900;
  margin: 0 0 10px;
  line-height: 1.2;
}
.overlay-text {
  margin: 10px 0 0;
  font-size: clamp(13px, 1.4vw, 16px);
  line-height: 1.55;
  color: #133a2a;
}
.overlay-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

/* Buttons */
.btn {
  appearance: none;
  border: 0;
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 0.98rem;
  cursor: pointer;
  transition: transform .05s ease, filter .2s ease, opacity .2s ease;
  color: #fff;
}
.btn:active { transform: translateY(1px); }

.btn-green { background: #2e7d32; }
.btn-green:hover { filter: brightness(1.05); }

.btn-amber { background: #b7791f; }
.btn-amber:hover { filter: brightness(1.05); }

/* Dots */
.carousel-dots {
  position: absolute;
  bottom: 20px;
  width: 100%;
  text-align: center;
}
.dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin: 0 5px;
  background: white;
  border-radius: 50%;
  opacity: 0.5;
  cursor: pointer;
}
.dot.active {
  opacity: 1;
  background: #2ecc71;
}

/* --- Content --- */
.content {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.why-section h2,
.stories h2,
.faq h2 {
  text-align: center;
  margin-bottom: 20px;
}

.why-container {
  display: flex;
  gap: 20px;
  align-items: center;
}
.why-container img {
  width: 50%;
  border-radius: 8px;
}
.why-container p {
  flex: 1;
  line-height: 1.6;
}

.stories .story-cards {
  display: flex;
  gap: 20px;
  justify-content: center;
}
.card {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  width: 450px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.card img {
  width: 100%;
  border-radius: 8px;
}

.faq ul { list-style: none; padding: 0; }
.faq li { margin-bottom: 15px; }

.stories { padding: 40px 80px; }
.faq { max-width: 600px; margin: 0 auto; }

.faq-item { border-bottom: 1px solid #ddd; padding: 10px 0; }
.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}
.arrow { transition: transform 0.3s ease; }
.arrow.open { transform: rotate(180deg); }
.faq-answer { padding: 10px 0; color: #555; }

/* Accordion animation */
.faq-enter-active, .faq-leave-active { transition: all 0.3s ease; }
.faq-enter-from, .faq-leave-to { max-height: 0; opacity: 0; overflow: hidden; }
.faq-enter-to, .faq-leave-from { max-height: 200px; opacity: 1; }

/* --- Reveal on scroll --- */
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s ease, transform 0.8s ease;
  will-change: opacity, transform;
}
.reveal.show {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger */
.story-cards .reveal:nth-child(1) { transition-delay: 0.1s; }
.story-cards .reveal:nth-child(2) { transition-delay: 0.2s; }
.story-cards .reveal:nth-child(3) { transition-delay: 0.3s; }

/* Responsive tweaks */
@media (max-width: 900px) {
  .hero-overlay { left: 4%; top: 6%; width: 92vw; }
  .overlay-actions { flex-direction: column; }
  .why-container { flex-direction: column; }
  .card { width: 100%; }
}
</style>


