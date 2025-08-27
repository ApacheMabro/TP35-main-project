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

    <!-- 👇 Content starts here -->
    <section class="content">
      <!-- Why It Matters -->
      <div class="why-section">
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
      <div class="stories">
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
      <div class="faq">
        <h2>FAQ</h2>
        <ul>
          <li><strong>Do I have to live in Melbourne?</strong><br />No, anyone can use our website.</li>
          <li><strong>Why upload my window photo?</strong><br />So we can measure tree visibility.</li>
          <li><strong>Where can I find the map?</strong><br />On the homepage navigation bar.</li>
          <li><strong>Do you have a mobile app?</strong><br />We are planning it soon.</li>
        </ul>
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
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % backgroundimages.length
  }, 5000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})

const goToSlide = (index) => {
  currentIndex.value = index
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
  max-width: 1000px;
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
  width: 250px;
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
</style>

