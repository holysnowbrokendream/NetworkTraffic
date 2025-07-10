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
  methods: {
    async login() {
      this.error = '';
      try {
        const res = await axios.post('http://localhost:8000/login/', {
          username: this.form.username,
          password: this.form.password
        });
        if (res.data.status === 'success') {
          localStorage.setItem('isLogin', '1');
          localStorage.setItem('token', res.data.token); // 保存token
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
  background: #f6f8fa;
  box-sizing: border-box;
  padding: 0 12px;
}
.login-card {
  max-width: 360px;
  width: 100%;
  margin: 0 auto;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(60, 120, 200, 0.12);
  padding: 36px 32px 24px 32px;
  box-sizing: border-box;
}
.login-title {
  text-align: center;
  color: #3578e5;
  font-weight: 600;
  margin-bottom: 24px;
}
.login-error {
  color: #e74c3c;
  margin-top: 8px;
  font-size: 15px;
  text-align: center;
}
</style> 