import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/NTBack/api', // 后端API基础URL
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // 令牌无效，清除本地存储并跳转到登录页
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('isLogin');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API接口
export const apiService = {
  // 获取首页信息
  getHomeInfo() {
    return api.get('/home/');
  },

  // 用户注册
  register(userData) {
    return api.post('/register/', userData);
  },

  // 用户登录
  login(credentials) {
    return api.post('/login/', credentials);
  },

  // 获取用户信息
  getUserInfo() {
    return api.get('/user/');
  },

  // 更新用户信息
  updateUserInfo(userData) {
    return api.put('/user/update/', userData);
  },

  // 获取CSRF令牌
  getCsrfToken() {
    return api.get('/csrf/');
  },
};

export default api; 