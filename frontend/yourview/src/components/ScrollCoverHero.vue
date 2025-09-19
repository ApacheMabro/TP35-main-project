<template>
  <section class="scroller">
    <!-- Sticky, always on screen while we scroll past this section -->
    <div ref="sticky" class="sticky">
      <video
        class="hero-video"
        :poster="poster"
        :src="src"
        autoplay
        muted
        loop
        playsinline
      ></video>

      <!-- The cover grows with scroll; keep it above the video -->
      <div class="cover" :style="coverStyle">
        <slot />
      </div>
    </div>

    <!-- Spacer defines how long the animation lasts (in viewport heights) -->
    <div :style="{ height: `${durationVH}vh` }"></div>
  </section>
</template>

<script>
export default {
  name: "ScrollCoverHero",
  props: {
    src: { type: String, required: true },
    poster: { type: String, default: "" },
    coverColor: { type: String, default: "#F7F1E5" }, // match your next section bg
    durationVH: { type: Number, default: 180 }, // how long the scroll animation runs
    ease: { type: Number, default: 0.15 }, // smoothing for progress
  },
  data() {
    return { rawProgress: 0, smoothProgress: 0, io: null, inView: false };
  },
  computed: {
    coverStyle() {
      // Scale from bottom to top; when =1 it fully hides the video
      return {
        background: this.coverColor,
        transform: `scaleY(${this.smoothProgress})`,
        transformOrigin: "bottom center",
      };
    },
  },
  mounted() {
    const sticky = this.$refs.sticky;

    // Observe when the sticky block enters/leaves the viewport
    this.io = new IntersectionObserver(
      (entries) => (this.inView = entries[0].isIntersecting),
      { threshold: 0 }
    );
    this.io.observe(sticky);

    const onScroll = () => {
      // progress 0..1 across the sticky element’s scroll span
      const rect = sticky.getBoundingClientRect();
      const h = window.innerHeight || document.documentElement.clientHeight;
      // When top goes from 0 to -duration (rect height + spacer), map to 0..1
      const total = h * (this.durationVH / 100); // px scroll length
      const y = Math.min(Math.max(-rect.top, 0), total);
      this.rawProgress = y / total;
    };

    const tick = () => {
      // small ease for buttery motion
      this.smoothProgress += (this.rawProgress - this.smoothProgress) * this.ease;
      if (this.inView) requestAnimationFrame(tick);
    };

    const start = () => {
      onScroll();
      if (this.inView) requestAnimationFrame(tick);
    };

    start();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);

    this.$once("hook:beforeUnmount", () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (this.io) this.io.disconnect();
    });
  },
};
</script>

<style scoped>
.scroller { position: relative; }
.sticky {
  position: sticky;
  top: 0;
  height: 100vh;      /* full viewport */
  overflow: hidden;   /* crop video to viewport */
}
.hero-video {
  width: 100%;
  height: 100%;
  object-fit: cover; /* keep the kid centered while filling screen */
  display: block;
}
.cover {
  position: absolute;
  inset: 0;
  /* Start hidden (scaleY 0). JS sets transform each frame. */
  transform: scaleY(0);
  will-change: transform;
  pointer-events: none;
}

/* Motion safety */
@media (prefers-reduced-motion: reduce) {
  .cover { transition: none; }
}
</style>
