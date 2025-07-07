<template>
  <div class="home-container">
    <div class="home-header">
      <h1 class="home-title">网络流量分析系统</h1>
      <p class="home-subtitle">Network Traffic Analysis System</p>
    </div>
    
    <div class="home-content">
      <!-- 欢迎信息 -->
      <div class="welcome-section">
        <h2>欢迎使用网络流量分析系统</h2>
        <p>这是一个基于Vue3和Django的现代化网络流量分析平台</p>
        <p>系统状态：<span class="status-badge">{{ systemStatus }}</span></p>
      </div>
      
      <!-- 系统信息 -->
      <div class="info-section">
        <h3>系统信息：</h3>
        <ul class="info-list">
          <li v-for="(item, index) in systemInfo" :key="index" class="info-item">
            {{ item }}
          </li>
        </ul>
      </div>
      
      <!-- 用户信息卡片 -->
      <div v-if="user" class="user-card">
        <div class="user-avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
        <div class="user-info">
          <h3>{{ user.username }}</h3>
          <p>{{ getUserTypeLabel(user.user_type) }}</p>
          <p>注册时间：{{ formatDate(user.created_at) }}</p>
        </div>
      </div>
      
      <!-- 快捷操作 -->
      <div class="quick-actions">
        <h3>快捷操作</h3>
        <div class="action-buttons">
          <el-button type="primary" icon="el-icon-s-data" @click="goToTraffic">
            流量监控
          </el-button>
          <el-button type="success" icon="el-icon-pie-chart" @click="goToModel">
            模型分析
          </el-button>
          <el-button type="info" icon="el-icon-setting" @click="goToSettings">
            系统设置
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 页脚 -->
    <div class="home-footer">
      <p>&copy; 2024 网络流量分析系统. 版权所有.</p>
      <p>当前时间：{{ currentTime }}</p>
    </div>
  </div>
</template>

<script>
import { apiService } from '../api/index.js';

export default {
  name: 'Home',
  data() {
    return {
      systemInfo: [],
      systemStatus: '加载中...',
      currentTime: '',
      user: null,
      loading: false
    };
  },
  created() {
    this.loadHomeData();
    this.loadUserInfo();
    this.updateCurrentTime();
    // 每秒更新一次时间
    setInterval(this.updateCurrentTime, 1000);
  },
  methods: {
    // 加载首页数据
    async loadHomeData() {
      try {
        this.loading = true;
        const response = await apiService.getHomeInfo();
        
        if (response.data.status === 'success') {
          this.systemInfo = response.data.data.index;
          this.systemStatus = response.data.data.system_status;
        }
      } catch (error) {
        console.error('加载首页数据失败:', error);
        this.systemStatus = '系统异常';
        this.systemInfo = ['系统数据加载失败', '请检查网络连接', '或联系管理员'];
      } finally {
        this.loading = false;
      }
    },
    
    // 加载用户信息
    async loadUserInfo() {
      try {
        const userStr = localStorage.getItem('user');
        if (userStr) {
          this.user = JSON.parse(userStr);
        }
        
        // 从后端获取最新用户信息
        const response = await apiService.getUserInfo();
        if (response.data.status === 'success') {
          this.user = response.data.user;
          localStorage.setItem('user', JSON.stringify(this.user));
        }
      } catch (error) {
        console.error('加载用户信息失败:', error);
        // 如果API调用失败，使用本地存储的用户信息
      }
    },
    
    // 更新当前时间
    updateCurrentTime() {
      const now = new Date();
      this.currentTime = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    },
    
    // 格式化日期
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN');
    },
    
    // 获取用户类型标签
    getUserTypeLabel(userType) {
      const typeMap = {
        'admin': '管理员',
        'user': '普通用户',
        'guest': '访客'
      };
      return typeMap[userType] || '未知';
    },
    
    // 导航到流量监控
    goToTraffic() {
      this.$router.push('/traffic');
    },
    
    // 导航到模型分析
    goToModel() {
      this.$router.push('/model');
    },
    
    // 导航到系统设置
    goToSettings() {
      this.$router.push('/settings');
    }
  }
};
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.home-header {
  background: linear-gradient(45deg, #4CAF50, #45a049);
  color: white;
  padding: 40px 20px;
  text-align: center;
  border-radius: 15px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.home-title {
  font-size: 2.5em;
  font-weight: 300;
  margin: 0 0 10px 0;
}

.home-subtitle {
  font-size: 1.2em;
  opacity: 0.9;
  margin: 0;
}

.home-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.welcome-section, .info-section, .user-card, .quick-actions {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.welcome-section {
  grid-column: 1 / -1;
  text-align: center;
}

.welcome-section h2 {
  color: #4CAF50;
  margin-bottom: 15px;
}

.welcome-section p {
  font-size: 1.1em;
  color: #666;
  margin-bottom: 10px;
}

.status-badge {
  background: #4CAF50;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: 600;
}

.info-section h3, .quick-actions h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3em;
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-item {
  background: #f8f9fa;
  margin: 15px 0;
  padding: 15px 20px;
  border-radius: 8px;
  border-left: 4px solid #4CAF50;
  font-size: 1em;
  color: #333;
  transition: all 0.3s ease;
}

.info-item:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #4CAF50;
  color: white;
  font-size: 1.5em;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.user-info h3 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 1.2em;
}

.user-info p {
  margin: 5px 0;
  color: #666;
  font-size: 0.9em;
}

.action-buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  flex: 1;
  min-width: 120px;
  padding: 12px 20px;
  font-size: 1em;
}

.home-footer {
  text-align: center;
  padding: 30px 20px;
  color: white;
  margin-top: 40px;
  border-top: 1px solid rgba(255,255,255,0.2);
}

.home-footer p {
  margin: 5px 0;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .home-header {
    padding: 30px 15px;
  }
  
  .home-title {
    font-size: 2em;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .el-button {
    width: 100%;
  }
}
</style> 