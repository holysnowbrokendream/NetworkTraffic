import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import TrafficHome from './components/Home.vue'
import TrafficDetail from './components/Traffic.vue'
import ModelAnalysis from './components/Model.vue'
import LoginPage from './components/Login.vue'
import SettingsPage from './components/Settings.vue'

const routes = [
  { path: '/login', component: LoginPage },
  { path: '/', component: TrafficHome },
  { path: '/traffic', component: TrafficDetail },
  { path: '/model', component: ModelAnalysis },
  { path: '/settings', component: SettingsPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isLogin = localStorage.getItem('isLogin') === '1'
  if (to.path !== '/login' && !isLogin) {
    next('/login')
  } else if (to.path === '/login' && isLogin) {
    next('/')
  } else {
    next()
  }
})

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
