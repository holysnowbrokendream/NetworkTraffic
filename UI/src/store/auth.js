// 认证状态管理
export const authStore = {
  // 状态
  state: {
    isLogin: false,
    user: null,
    token: null
  },
  
  // 初始化状态
  init() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    const isLogin = localStorage.getItem('isLogin');
    
    if (token && user && isLogin === '1') {
      this.state.token = token;
      this.state.user = JSON.parse(user);
      this.state.isLogin = true;
    }
  },
  
  // 登录
  login(token, user) {
    this.state.token = token;
    this.state.user = user;
    this.state.isLogin = true;
    
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('isLogin', '1');
  },
  
  // 登出
  logout() {
    this.state.token = null;
    this.state.user = null;
    this.state.isLogin = false;
    
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('isLogin');
  },
  
  // 更新用户信息
  updateUser(user) {
    this.state.user = user;
    localStorage.setItem('user', JSON.stringify(user));
  },
  
  // 获取用户信息
  getUser() {
    return this.state.user;
  },
  
  // 获取令牌
  getToken() {
    return this.state.token;
  },
  
  // 检查是否已登录
  isAuthenticated() {
    return this.state.isLogin && this.state.token;
  }
};

// 初始化认证状态
authStore.init(); 