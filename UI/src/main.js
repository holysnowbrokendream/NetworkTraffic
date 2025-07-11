import { createApp } from 'vue'
import App from './App.vue'
import Home from './components/Home.vue'
import LoginPage from './components/Login.vue'
import RegisterPage from './components/Register.vue'
import { createRouter, createWebHistory } from 'vue-router'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import { ElMessage } from 'element-plus'
import axios from 'axios'

// 添加全局样式来防止滚动，并支持主题切换
const style = document.createElement('style')
style.textContent = `
  :root {
    /* 过渡动画时间统一变量 */
    --theme-transition: 0.4s ease;
    --ui-transition: 0.25s ease;
    
    /* 暗色主题变量 */
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d3748;
    --bg-tertiary: #4a5568;
    --bg-quaternary: #718096;
    --text-primary: #e2e8f0;
    --text-secondary: #a0aec0;
    --text-accent: #81c784;
    --text-danger: #e53e3e;
    --text-danger-hover: #fc8181;
    --text-warning: #f687b3;
    --border-color: #4a5568;
    --hover-bg: rgba(74, 85, 104, 0.3);
    --hover-bg-light: rgba(74, 85, 104, 0.2);
    --shadow-color: rgba(0,0,0,0.3);
    --accent-color: #81c784;
    --accent-hover: #68d391;
    --button-hover: #1a202c;
    --accent-shadow: rgba(129, 199, 132, 0.4);
    --accent-shadow-light: rgba(129, 199, 132, 0.2);
    --accent-shadow-strong: rgba(129, 199, 132, 0.6);
  }
  
  [data-theme="light"] {
    /* 亮色主题变量 - 温暖明亮的色彩方案 */
    --bg-primary: #fefefe;
    --bg-secondary: #f8f4f0;
    --bg-tertiary: #f0e6d8;
    --bg-quaternary: #e8d5c4;
    --text-primary: #2d3748;
    --text-secondary: #5a6c7d;
    --text-accent: #d97706;
    --text-danger: #dc2626;
    --text-danger-hover: #ef4444;
    --text-warning: #c53030;
    --border-color: #e2d1c3;
    --hover-bg: rgba(248, 244, 240, 0.8);
    --hover-bg-light: rgba(240, 230, 216, 0.5);
    --shadow-color: rgba(45, 55, 72, 0.12);
    --accent-color: #d97706;
    --accent-hover: #b45309;
    --button-hover: #fef7ed;
    --accent-shadow: rgba(217, 119, 6, 0.25);
    --accent-shadow-light: rgba(217, 119, 6, 0.12);
    --accent-shadow-strong: rgba(217, 119, 6, 0.4);
  }

  /* 全局主题过渡动画统一设置 */
  *, *::before, *::after {
    transition: background-color var(--theme-transition), 
                color var(--theme-transition), 
                border-color var(--theme-transition), 
                box-shadow var(--theme-transition), 
                text-shadow var(--theme-transition) !important;
  }
  
  /* UI交互元素使用更快的过渡动画 */
  button, .el-button, .el-input, .el-dropdown, 
  button:hover, .el-button:hover, .el-input:hover,
  [class*="btn"]:hover, [class*="button"]:hover {
    transition: all var(--ui-transition) !important;
  }
  
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
    width: 100vw !important;
    overflow: hidden !important;
    background: var(--bg-primary) !important;
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
    background: var(--bg-primary) !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    transition: background-color 0.3s ease, color 0.3s ease;
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

// 添加axios响应拦截器处理token过期
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // 如果响应状态码是401，说明token过期或无效
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // 如果正在刷新token，将请求加入队列
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return axios(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem('refreshToken');
      
      if (refreshToken) {
        try {
          // 尝试使用refresh token获取新的access token
          const response = await axios.post('http://localhost:8000/api/userauth/token/refresh/', {
            refresh: refreshToken
          });
          
          const newToken = response.data.access;
          localStorage.setItem('token', newToken);
          
          // 更新所有待处理的请求
          processQueue(null, newToken);
          
          // 更新原始请求的header并重新发送
          originalRequest.headers['Authorization'] = 'Bearer ' + newToken;
          return axios(originalRequest);
          
        } catch (refreshError) {
          // refresh token也失效了，清除所有token并跳转到登录页
          processQueue(refreshError, null);
          localStorage.removeItem('isLogin');
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          ElMessage.warning('登录已过期，请重新登录');
          router.push('/login');
          return Promise.reject(refreshError);
        } finally {
          isRefreshing = false;
        }
      } else {
        // 没有refresh token，直接跳转到登录页
        localStorage.removeItem('isLogin');
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        ElMessage.warning('登录已过期，请重新登录');
        router.push('/login');
        return Promise.reject(error);
      }
    }
    
    return Promise.reject(error);
  }
);

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
