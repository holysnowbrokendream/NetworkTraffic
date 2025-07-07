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
      <div v-if="msg" :style="{color:msgType==='success'?'green':'#e74c3c',textAlign:'center',marginTop:'8px'}">{{ msg }}</div>
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
  methods: {
    async register() {
      this.msg = '';
      try {
        const res = await axios.post('http://localhost:8000/register/', {
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
  background: #f6f8fa;
  box-sizing: border-box;
  padding: 0 12px;
}
.register-card {
  max-width: 360px;
  width: 100%;
  margin: 0 auto;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(60, 120, 200, 0.12);
  padding: 36px 32px 24px 32px;
  box-sizing: border-box;
}
.register-title {
  text-align: center;
  color: #3578e5;
  font-weight: 600;
  margin-bottom: 24px;
}
</style> 