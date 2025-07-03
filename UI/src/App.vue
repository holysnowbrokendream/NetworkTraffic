<template>
  <div id="app">
    <el-container style="min-height:100vh;">
      <template v-if="$route.path !== '/login'">
        <el-aside
          :width="collapsed ? '56px' : '180px'"
          class="side-nav"
          @mouseenter="collapsed=false"
          @mouseleave="collapsed=true"
        >
          <div class="side-nav-inner">
            <div class="side-logo" :class="{hide: collapsed}">网络流量平台</div>
            <ul class="side-menu">
              <li :class="['side-menu-item', {active: $route.path==='/' }]" @click="$router.push('/')">
                <i class="el-icon-house"></i>
                <span class="side-menu-text" :class="{hide: collapsed}">首页</span>
              </li>
              <li :class="['side-menu-item', {active: $route.path==='/traffic' }]" @click="$router.push('/traffic')">
                <i class="el-icon-s-data"></i>
                <span class="side-menu-text" :class="{hide: collapsed}">流量明细</span>
              </li>
              <li :class="['side-menu-item', {active: $route.path==='/model' }]" @click="$router.push('/model')">
                <i class="el-icon-pie-chart"></i>
                <span class="side-menu-text" :class="{hide: collapsed}">模型分析</span>
              </li>
              <li :class="['side-menu-item', {active: $route.path==='/settings' }]" @click="$router.push('/settings')">
                <i class="el-icon-setting"></i>
                <span class="side-menu-text" :class="{hide: collapsed}">系统设置</span>
              </li>
            </ul>
            <div v-if="isLogin" class="side-logout">
              <el-button type="danger" size="small" @click="logout" style="width:100%;display:flex;align-items:center;justify-content:center;">
                <i class="el-icon-switch-button" style="margin-right:6px;"></i>
                <span v-if="!collapsed">登出</span>
              </el-button>
            </div>
          </div>
        </el-aside>
      </template>
      <el-container>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
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
    isLogin() {
      return localStorage.getItem('isLogin') === '1';
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('isLogin');
      this.$router.replace('/login');
    }
  }
};
</script>

<style>
.side-nav {
  background: linear-gradient(180deg, #3578e5 0%, #5fa8ef 100%);
  min-height: 100vh;
  transition: width 0.2s;
  box-shadow: 2px 0 8px rgba(53,120,229,0.08);
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 0;
}
.side-nav-inner {
  display: flex;
  flex-direction: column;
  height: 100vh;
  min-height: 0;
  justify-content: flex-start;
  position: relative;
  transition: background 0.2s;
}
.side-logo {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  padding: 18px 0 12px 0;
  letter-spacing: 2px;
  transition: opacity 0.18s, width 0.18s;
  opacity: 1;
  width: 100%;
}
.side-logo.hide {
  opacity: 0;
  width: 0;
  pointer-events: none;
}
.side-menu {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1 1 auto;
  min-height: 0;
}
.side-menu-item {
  display: flex;
  align-items: center;
  color: #fff;
  font-size: 16px;
  border-radius: 6px;
  margin: 4px 8px;
  padding: 10px 12px;
  cursor: pointer;
  transition: background 0.18s, color 0.18s;
  opacity: 1;
}
.side-menu-item.active {
  background: #fff !important;
  color: #3578e5 !important;
  font-weight: bold;
}
.side-menu-item:not(.active):hover {
  background: #e0eafc !important;
  color: #3578e5 !important;
}
.side-menu-text {
  margin-left: 12px;
  transition: opacity 0.18s, width 0.18s;
  opacity: 1;
  white-space: nowrap;
}
.side-menu-text.hide {
  opacity: 0;
  width: 0;
  pointer-events: none;
}
.side-logout {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  padding: 16px 12px 24px 12px;
  background: transparent;
  box-sizing: border-box;
  transition: opacity 0.18s, width 0.18s;
  opacity: 1;
  z-index: 10;
}
.side-logout.hide {
  opacity: 0;
  width: 0;
  pointer-events: none;
}
.el-main {
  background: #f6f8fa;
  min-height: 100vh;
  padding: 0;
  margin: 0;
}
#app {
  font-family: 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', Arial, sans-serif;
  background: #f6f8fa;
  min-height: 100vh;
}
</style>
