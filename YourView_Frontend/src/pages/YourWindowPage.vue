<template>
  <div class="green-page">
    <div class="page">
      <!-- Top large background image -->
        <div class="hero">
          <img class="hero-img" src="@/assets/background4.jpeg" alt="Hero background" />
          <div class="overlay">
            <h1 class="title">Snap & Share</h1>
            <p class="subtitle">See your green score with in few steps</p>
          </div>
        </div>


      <!-- How Does It Work Section -->
      <section class="how-it-works">
        <h2>How Does It Work</h2>

        <div class="steps">
          <!-- Step 1 -->
          <div class="step">
            <img src="@/assets/photo.png" alt="Upload Photo" />
            <p>Take or upload your window photo</p>
          </div>

          <!-- Step 2 -->
          <div class="step">
            <img src="@/assets/tree.png" alt="Count Trees" />
            <p>Count the number of visible trees</p>
          </div>

          <!-- Step 3 -->
          <div class="step">
            <img src="@/assets/coordinate.png" alt="Add Location" />
            <p>Enter your address / coordinates</p>
          </div>

          <!-- Step 4 -->
          <div class="step">
            <img src="@/assets/eye.png" alt="View Score" />
            <p>See your 3-30-300 score instantly</p>
          </div>
        </div>
                <!-- Upload button -->
        <div class="upload-btn-wrapper">
          <button class="upload-btn">Upload My Window</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// 空
</script>

<style scoped>
.green-page {
  background-color: #faffe8;
  min-height: 100vh;
}

.page {
  font-family: "Arial", sans-serif;
}

/* Hero banner */
.hero {
  height: 75vh;
  position: relative;
  overflow: hidden;
}

.hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  color: white;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
}
.subtitle {
  font-size: 1.2rem;
  margin-top: 0.5rem;
}

/* How it works */
.how-it-works {
  margin-top: 3rem;
  text-align: center;
}

.how-it-works h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2d6a4f;
}

.steps {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.step {
  flex: 1 1 200px;
  max-width: 220px;
}

.step img {
  width: 80px;
  height: 80px;
  object-fit: contain;
  margin-bottom: 1rem;
}

.step p {
  font-size: 0.95rem;
  color: #333;
}

/* Upload button */
.upload-btn-wrapper {
  margin-top: 2.5rem;
  text-align: center;
}
.upload-btn {
  background: black;
  color: white;
  font-size: 1.1rem;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 8px; /* 钝边 */
  cursor: pointer;
  transition: background 0.3s;
}
.upload-btn:hover {
  background: #333;
}
</style>

