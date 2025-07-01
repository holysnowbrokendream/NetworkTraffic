<template>
  <div id="app">
    <nav>
      <router-link to="/">首页</router-link> |
      <router-link to="/traffic">流量明细</router-link> |
      <router-link to="/model">模型分析</router-link> |
      <router-link to="/settings">系统设置</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
nav {
  padding: 16px;
  background: #f5f5f5;
}
nav a {
  margin: 0 8px;
  text-decoration: none;
  color: #333;
}
nav a.router-link-exact-active {
  font-weight: bold;
  color: #42b983;
}
</style>
