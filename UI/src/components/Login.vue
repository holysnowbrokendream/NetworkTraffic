<template>
  <!-- 登录页面主容器 -->
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">登录</h2>
      <!-- 登录表单 -->
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
      <!-- 注册入口 -->
      <div style="text-align:center;margin-top:8px;">
        <el-button type="text" @click="showRegister=true">没有账号？注册</el-button>
      </div>
      <!-- 登录错误提示 -->
      <div v-if="error" class="login-error">{{ error }}</div>
    </el-card>
    <!-- 注册弹窗 -->
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
      // 登录表单数据
      form: {
        username: '',
        password: ''
      },
      error: '', // 登录错误提示
      showRegister: false, // 注册弹窗显示状态
      // 注册表单数据
      registerForm: {
        username: '',
        password: ''
      },
      registerMsg: '' // 注册结果提示
    };
  },
  methods: {
    // 登录方法，调用后端接口校验
    async login() {
      this.error = '';
      try {
        const res = await axios.post('http://localhost:8000/token/', {
          username: this.form.username,
          password: this.form.password
        });
        // 登录成功后保存token和登录状态
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
    // 注册方法，调用后端注册接口
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
/* 登录页面主容器样式 */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
  box-sizing: border-box;
  padding: 0 12px;
}
/* 登录卡片样式 */
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