<template>
  <router-view />
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      collapsed: true
    };
  },
  computed: {
    // 判断是否已登录，控制登出按钮显示
    isLogin() {
      return localStorage.getItem('isLogin') === '1';
    }
  },
  methods: {
    // 登出方法，清除登录状态并跳转到登录页
    logout() {
      localStorage.removeItem('isLogin');
      this.$router.replace('/login');
    }
  }
};
</script>
