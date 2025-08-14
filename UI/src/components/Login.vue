<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">登录</h2>
      <el-form :model="form" @submit.prevent="login" @keyup.enter="login">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" clearable prefix-icon="el-icon-user" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" clearable prefix-icon="el-icon-lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width:100%;" @click="login">登录</el-button>
        </el-form-item>
      </el-form>
      <div style="text-align:center;margin-top:8px;">
        <el-button type="text" @click="$router.push('/register')">没有账号？注册</el-button>
      </div>
      <div v-if="error" class="login-error">{{ error }}</div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'LoginPage',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      error: ''
    };
  },
  mounted() {
    // 初始化主题
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
      // 默认为亮色主题
      localStorage.setItem('theme', 'light');
      document.documentElement.setAttribute('data-theme', 'light');
    }
  },
  methods: {
    async login() {
      this.error = '';
      try {
        const res = await axios.post('/login/', {
          username: this.form.username,
          password: this.form.password
        });
        if (res.data.status === 'success') {
          localStorage.setItem('isLogin', '1');
          localStorage.setItem('token', res.data.token); // 保存access token
          localStorage.setItem('refreshToken', res.data.refresh); // 保存refresh token
          this.$router.replace('/');
        } else {
          this.error = res.data.msg || '登录失败';
        }
      } catch (e) {
        this.error = '登录失败';
      }
    }
  },
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  box-sizing: border-box;
  padding: 0 12px;
  transition: background-color var(--theme-transition);
}
.login-card {
  max-width: 360px;
  width: 100%;
  margin: 0 auto;
  border-radius: 16px;
  background: var(--bg-secondary);
  border: 2px solid var(--border-color);
  box-shadow: 0 12px 48px var(--shadow-color);
  padding: 36px 32px 24px 32px;
  box-sizing: border-box;
  transition: all var(--theme-transition);
}
.login-title {
  text-align: center;
  color: var(--text-accent);
  font-weight: 600;
  margin-bottom: 24px;
  font-size: 28px;
  transition: color var(--theme-transition);
}
.login-error {
  color: var(--text-danger);
  margin-top: 8px;
  font-size: 15px;
  text-align: center;
  transition: color var(--theme-transition);
}

/* 主题适配的Element Plus组件样式覆盖 */
.login-card :deep(.el-input__wrapper) {
  background-color: var(--bg-tertiary) !important;
  border-color: var(--bg-quaternary) !important;
  box-shadow: 0 0 0 1px var(--bg-quaternary) inset !important;
  border-radius: 12px !important;
  transition: all 0.3s ease !important;
}

.login-card :deep(.el-input__inner) {
  color: var(--text-primary) !important;
  font-size: 16px !important;
}

.login-card :deep(.el-input__inner::placeholder) {
  color: var(--text-secondary) !important;
}

.login-card :deep(.el-input__wrapper:hover) {
  border-color: var(--text-accent) !important;
  box-shadow: 0 0 0 1px var(--text-accent) inset !important;
}

.login-card :deep(.el-input__wrapper.is-focus) {
  border-color: var(--text-accent) !important;
  box-shadow: 0 0 0 1px var(--text-accent) inset !important;
}

.login-card :deep(.el-button--primary) {
  background-color: var(--text-accent) !important;
  border-color: var(--text-accent) !important;
  color: var(--button-hover) !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  padding: 12px 24px !important;
  font-size: 16px !important;
  box-shadow: 0 4px 16px var(--accent-shadow) !important;
  transition: all 0.25s ease !important;
}

.login-card :deep(.el-button--primary:hover) {
  background-color: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px var(--accent-shadow-strong) !important;
}

.login-card :deep(.el-button--text) {
  color: var(--text-accent) !important;
  font-size: 15px !important;
  transition: color 0.3s ease !important;
}

.login-card :deep(.el-button--text:hover) {
  color: var(--accent-hover) !important;
}

.login-card :deep(.el-form-item) {
  margin-bottom: 20px !important;
}

.login-card :deep(.el-input__prefix-inner) {
  color: var(--text-secondary) !important;
}

.login-card :deep(.el-input__suffix-inner) {
  color: var(--text-secondary) !important;
}
</style> 