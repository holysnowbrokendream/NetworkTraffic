import { createApp } from 'vue'
import App from './App.vue'
import Home from './components/Home.vue'
import LoginPage from './components/Login.vue'
import RegisterPage from './components/Register.vue'
import { createRouter, createWebHistory } from 'vue-router'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫，未登录只能访问登录/注册页
router.beforeEach((to, from, next) => {
  const isLogin = localStorage.getItem('isLogin') === '1';
  if ((to.path === '/login' || to.path === '/register') && isLogin) {
    next('/');
  } else {
    next();
  }
});

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
