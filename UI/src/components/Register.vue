<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2 class="register-title">注册</h2>
      <el-form :model="form" @submit.prevent="register" @keyup.enter="register">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" clearable prefix-icon="el-icon-user" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" clearable prefix-icon="el-icon-lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width:100%;" @click="register">注册</el-button>
        </el-form-item>
      </el-form>
      <div style="text-align:center;margin-top:8px;">
        <el-button type="text" @click="$router.push('/login')">已有账号？登录</el-button>
      </div>
      <div v-if="msg" class="register-message" :class="{'success': msgType==='success', 'error': msgType==='error'}">{{ msg }}</div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'RegisterPage',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      msg: '',
      msgType: 'success'
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
    async register() {
      this.msg = '';
      try {
        const res = await axios.post('/register/', {
          username: this.form.username,
          password: this.form.password
        });
        if (res.data.status === 'success') {
          this.msg = '注册成功，请登录';
          this.msgType = 'success';
          setTimeout(() => {
            this.$router.replace('/login');
          }, 1200);
        } else {
          this.msg = res.data.msg || '注册失败';
          this.msgType = 'error';
        }
      } catch (e) {
        this.msg = '注册失败';
        this.msgType = 'error';
      }
    }
  },
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  box-sizing: border-box;
  padding: 0 12px;
  transition: background-color 0.3s ease;
}
.register-card {
  max-width: 360px;
  width: 100%;
  margin: 0 auto;
  border-radius: 16px;
  background: var(--bg-secondary);
  border: 2px solid var(--border-color);
  box-shadow: 0 12px 48px var(--shadow-color);
  padding: 36px 32px 24px 32px;
  box-sizing: border-box;
  transition: all 0.3s ease;
}
.register-title {
  text-align: center;
  color: var(--text-accent);
  font-weight: 600;
  margin-bottom: 24px;
  font-size: 28px;
  transition: color 0.3s ease;
}
.register-message {
  text-align: center;
  margin-top: 8px;
  font-size: 15px;
  transition: color 0.3s ease;
}
.register-message.success {
  color: var(--text-accent);
}
.register-message.error {
  color: var(--text-danger);
}

/* 主题适配的Element Plus组件样式覆盖 */
.register-card :deep(.el-input__wrapper) {
  background-color: var(--bg-tertiary) !important;
  border-color: var(--bg-quaternary) !important;
  box-shadow: 0 0 0 1px var(--bg-quaternary) inset !important;
  border-radius: 12px !important;
  transition: all 0.3s ease !important;
}

.register-card :deep(.el-input__inner) {
  color: var(--text-primary) !important;
  font-size: 16px !important;
}

.register-card :deep(.el-input__inner::placeholder) {
  color: var(--text-secondary) !important;
}

.register-card :deep(.el-input__wrapper:hover) {
  border-color: var(--text-accent) !important;
  box-shadow: 0 0 0 1px var(--text-accent) inset !important;
}

.register-card :deep(.el-input__wrapper.is-focus) {
  border-color: var(--text-accent) !important;
  box-shadow: 0 0 0 1px var(--text-accent) inset !important;
}

.register-card :deep(.el-button--primary) {
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

.register-card :deep(.el-button--primary:hover) {
  background-color: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px var(--accent-shadow-strong) !important;
}

.register-card :deep(.el-button--text) {
  color: var(--text-accent) !important;
  font-size: 15px !important;
  transition: color 0.3s ease !important;
}

.register-card :deep(.el-button--text:hover) {
  color: var(--accent-hover) !important;
}

.register-card :deep(.el-form-item) {
  margin-bottom: 20px !important;
}

.register-card :deep(.el-input__prefix-inner) {
  color: var(--text-secondary) !important;
}

.register-card :deep(.el-input__suffix-inner) {
  color: var(--text-secondary) !important;
}
</style> 