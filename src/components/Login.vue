<template>
  <div style="max-width:320px;margin:80px auto;padding:32px;border:1px solid #eee;border-radius:8px;box-shadow:0 2px 8px #eee;">
    <h2 style="text-align:center;">登录</h2>
    <div style="margin-bottom:16px;">
      <input v-model="username" placeholder="用户名" style="width:100%;padding:8px;margin-bottom:8px;" />
      <input v-model="password" type="password" placeholder="密码" style="width:100%;padding:8px;" />
    </div>
    <button @click="login" style="width:100%;padding:8px;">登录</button>
    <div v-if="error" style="color:red;margin-top:8px;text-align:center;">{{ error }}</div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      error: '',
    };
  },
  methods: {
    login() {
      if (this.username === 'admin' && this.password === 'admin') {
        localStorage.setItem('isLogin', '1');
        this.$router.replace('/');
      } else {
        this.error = '用户名或密码错误（admin/admin）';
      }
    },
  },
};
</script> 