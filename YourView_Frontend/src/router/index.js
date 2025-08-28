import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import GreenIndex from '../pages/GreenIndex.vue'
import YourAreaPage from '../pages/YourAreaPage.vue'
import AboutPage from '../pages/AboutPage.vue'
import SourcePage from '../pages/SourcePage.vue'
import TempPage from '../pages/TempPage.vue'
import YourWindowPage from '../pages/YourWindowPage.vue'
const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/greenpage', name: 'green', component: GreenIndex },
  { path: '/YourArea', name: 'YourArea', component: YourAreaPage },
  { path: '/about', name: 'about', component: AboutPage },
  { path: '/source', name: 'source', component: SourcePage },
  { path: '/temp', name: 'temp', component: TempPage },
  { path: '/YourWindow', name: 'YourWindow', component: YourWindowPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
