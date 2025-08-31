<template>
  <div>
    <!-- Hero carousel -->
    <div class="carousel">
      <div
        class="carousel-track"
        :style="{
          transform: `translateX(-${currentIndex * 100}%)`,
        }"
      >
        <div class="carousel-slide" v-for="(img, index) in backgroundimages" :key="index">
          <img :src="img" :alt="`Background ${index + 1}`" />
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
            <img :src="images[4]" alt="Abdul" />
            <h3>Abdul</h3>
            <p>Body text for Abdul's story...</p>
          </div>
          <div class="card">
            <img :src="images[5]" alt="Maria" />
            <h3>Maria</h3>
            <p>Body text for Maria's story...</p>
          </div>
          <div class="card">
            <img :src="images[6]" alt="Teacher" />
            <h3>Teacher</h3>
            <p>Body text for Teacher's story...</p>
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
          <!-- Question Section -->
          <div class="faq-question" @click="toggle(index)">
            <strong>{{ item.question }}</strong>
            <span
              class="arrow"
              :class="{ open: openIndex === index }"
            >▼</span>
          </div>

          <!-- Answer section -->
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
  new URL('@/assets/background1.png', import.meta.url).href,
  new URL('@/assets/background2.jpeg', import.meta.url).href,
  new URL('@/assets/background3.jpeg', import.meta.url).href,
  new URL('@/assets/WhyMatter.png', import.meta.url).href,
  new URL('@/assets/Abdul.png', import.meta.url).href,
  new URL('@/assets/Maria.png', import.meta.url).href,
  new URL('@/assets/Teacher.png', import.meta.url).href,
]
const backgroundimages = images.filter(img => img.includes("background"))
const currentIndex = ref(0)
let intervalId = null

onMounted(() => {
  // Carousel
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % backgroundimages.length
  }, 5000)

  // Cyclically triggered IntersectionObserver
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          // Enter the viewport: Add show -> Fade in
          entry.target.classList.add('show')
        } else {
          // To leave the viewport: Remove show -> Reset to fade state
          entry.target.classList.remove('show')
        }
      })
    },
    {
      // threshold: 0.15,         // It is triggered only when more than 15% is visible
      rootMargin: '0px 0px -5% 0px', // It can be triggered slightly earlier or disappear later, and can be adjusted as needed
    }
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
  {
    question: "Do I have to live in Melbourne?",
    answer: "No, anyone can use our website."
  },
  {
    question: "Why upload my window photo?",
    answer: "So we can measure tree visibility."
  },
  {
    question: "Where can I find the map?",
    answer: "On the homepage navigation bar."
  },
  {
    question: "Do you have a mobile app?",
    answer: "We are planning it soon."
  }
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

.faq ul {
  list-style: none;
  padding: 0;
}
.faq li {
  margin-bottom: 15px;
}

.stories {
  padding: 40px 80px;
}
.faq {
  max-width: 600px;
  margin: 0 auto;
}

.faq-item {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.arrow {
  transition: transform 0.3s ease;
}

.arrow.open {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 10px 0;
  color: #555;
}

/* Pull the drawing down */
.faq-enter-active, .faq-leave-active {
  transition: all 0.3s ease;
}
.faq-enter-from, .faq-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
.faq-enter-to, .faq-leave-from {
  max-height: 200px;
  opacity: 1;
}


.card {
  flex: 1;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.08);
  text-align: center;
  transition: transform 0.3s ease;
}

.card img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 15px;
}

.card:hover {
  transform: translateY(-5px);
}

/* --- Reveal animation --- */
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.8s ease, transform 0.8s ease;
  will-change: opacity, transform; /* Optional: Enhance the smoothness of repetitive animations */
}

.reveal.show {
  opacity: 1;
  transform: translateY(0);
}

/* Delay the effect of the card alone a little */
.story-cards .reveal:nth-child(1) { transition-delay: 0.1s; }
.story-cards .reveal:nth-child(2) { transition-delay: 0.2s; }
.story-cards .reveal:nth-child(3) { transition-delay: 0.3s; }

</style>

