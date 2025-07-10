import { createApp } from 'vue'
import App from './App.vue'
import Home from './components/Home.vue'
import LoginPage from './components/Login.vue'
import RegisterPage from './components/Register.vue'
import { createRouter, createWebHistory } from 'vue-router'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'

// 添加全局样式来防止滚动
const style = document.createElement('style')
style.textContent = `
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
    width: 100vw !important;
    overflow: hidden !important;
    background: #1a1a1a !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
  }
  
  * {
    box-sizing: border-box;
  }
  
  #app {
    height: 100vh !important;
    width: 100vw !important;
    overflow: hidden !important;
    background: #1a1a1a !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
  }
`
document.head.appendChild(style)

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
