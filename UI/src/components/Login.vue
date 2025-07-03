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
        <el-button type="text" @click="showRegister=true">没有账号？注册</el-button>
      </div>
      <div v-if="error" class="login-error">{{ error }}</div>
    </el-card>
    <el-dialog v-model="showRegister" title="注册新账号" width="340px" :close-on-click-modal="false">
      <el-form :model="registerForm">
        <el-form-item label="用户名">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRegister=false">取消</el-button>
        <el-button type="primary" @click="register">注册</el-button>
      </template>
      <div v-if="registerMsg" style="color:green;text-align:center;margin-top:8px;">{{ registerMsg }}</div>
    </el-dialog>
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
      error: '',
      showRegister: false,
      registerForm: {
        username: '',
        password: ''
      },
      registerMsg: ''
    };
  },
  methods: {
    async login() {
      this.error = '';
      try {
        const res = await axios.post('http://localhost:8000/token/', {
          username: this.form.username,
          password: this.form.password
        });
        localStorage.setItem('access', res.data.access);
        localStorage.setItem('refresh', res.data.refresh);
        localStorage.setItem('isLogin', '1');
        setTimeout(() => {
          this.$router.replace('/');
        }, 100);
      } catch (e) {
        this.error = '登录失败';
      }
    },
    async register() {
      this.registerMsg = '';
      try {
        const res = await fetch('http://localhost:8000/register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.registerForm.username,
            password: this.registerForm.password
          })
        });
        const data = await res.json();
        this.registerMsg = data.msg || '注册完成';
        if (data.status === 'success') {
          setTimeout(() => {
            this.showRegister = false;
            this.registerForm.username = '';
            this.registerForm.password = '';
            this.registerMsg = '';
          }, 1200);
        }
      } catch (e) {
        this.registerMsg = '注册请求失败';
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
  background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
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