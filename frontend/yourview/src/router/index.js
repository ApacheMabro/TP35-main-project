import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'intro', component: () => import('@/pages/intro.vue') },
  { path: '/intro/step1', name: 'intro-step1', component: () => import('@/pages/intro_step1.vue') },
  { path: '/intro/step2', name: 'intro-step2', component: () => import('@/pages/intro_step2.vue') },
  { path: '/intro/step3', name: 'intro-step3', component: () => import('@/pages/intro_step3.vue') },
  // { path: '/intro/step4', name: 'intro-step4', component: () => import('@/pages/intro_step4.vue') },  
  { path: '/landing', name: 'landing', component: () => import('@/pages/Landing.vue') },
  { path: '/upload_window', name: 'upload_window', component: () => import('@/pages/upload_my_window.vue') },
  { path: '/heatmap', name: 'heatmap', component: () => import('@/pages/heatmap.vue') },
  { path: '/plant_health', name: 'plant_health', component: () => import('@/pages/plant_health.vue') },
  { path: '/gallery', name: 'gallery', component: () => import('@/pages/gallery.vue') },
  { path: '/upload', name: 'upload', component: () => import('@/pages/upload.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})