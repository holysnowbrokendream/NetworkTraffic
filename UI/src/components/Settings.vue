<template>
  <div class="settings-container">
    <div class="settings-header">
      <h1>用户设置</h1>
      <p>管理您的个人信息和账户设置</p>
    </div>
    
    <div class="settings-content">
      <!-- 用户信息卡片 -->
      <el-card class="user-profile-card">
        <div class="profile-header">
          <div class="avatar">{{ user?.username?.charAt(0)?.toUpperCase() }}</div>
          <div class="user-basic-info">
            <h2>{{ user?.username }}</h2>
            <p class="user-type">{{ getUserTypeLabel(user?.user_type) }}</p>
          </div>
        </div>
        
        <div class="profile-details">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="用户名">
              {{ user?.username }}
            </el-descriptions-item>
            <el-descriptions-item label="用户类型">
              {{ getUserTypeLabel(user?.user_type) }}
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              {{ user?.email || '未绑定' }}
            </el-descriptions-item>
            <el-descriptions-item label="手机号">
              {{ user?.phonenumber || '未绑定' }}
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">
              {{ formatDate(user?.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="更新时间">
              {{ formatDate(user?.updated_at) }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="profile-actions">
          <el-button type="primary" @click="showEditDialog = true">
            修改信息
          </el-button>
          <el-button type="danger" @click="handleLogout">
            退出登录
          </el-button>
        </div>
      </el-card>
      
      <!-- 系统设置卡片 -->
      <el-card class="system-settings-card">
        <h3>系统设置</h3>
        <div class="setting-item">
          <span>主题模式</span>
          <el-switch
            v-model="darkMode"
            active-text="深色"
            inactive-text="浅色"
            @change="toggleTheme"
          />
        </div>
        <div class="setting-item">
          <span>消息通知</span>
          <el-switch
            v-model="notifications"
            active-text="开启"
            inactive-text="关闭"
            @change="toggleNotifications"
          />
        </div>
        <div class="setting-item">
          <span>自动刷新</span>
          <el-switch
            v-model="autoRefresh"
            active-text="开启"
            inactive-text="关闭"
            @change="toggleAutoRefresh"
          />
        </div>
      </el-card>
    </div>
    
    <!-- 修改信息对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="修改个人信息"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="邮箱">
          <el-input
            v-model="editForm.email"
            placeholder="请输入邮箱"
            type="email"
          />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input
            v-model="editForm.phonenumber"
            placeholder="请输入手机号"
          />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="editForm.password"
            placeholder="不修改请留空"
            type="password"
            show-password
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveUserInfo" :loading="saving">
          {{ saving ? '保存中...' : '保存' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { apiService } from '../api/index.js';

export default {
  name: 'Settings',
  data() {
    return {
      user: null,
      showEditDialog: false,
      saving: false,
      editForm: {
        email: '',
        phonenumber: '',
        password: ''
      },
      // 系统设置
      darkMode: false,
      notifications: true,
      autoRefresh: true
    };
  },
  created() {
    this.loadUserInfo();
    this.loadSettings();
  },
  methods: {
    // 加载用户信息
    async loadUserInfo() {
      try {
        // 先从本地存储获取用户信息
        const userStr = localStorage.getItem('user');
        if (userStr) {
          this.user = JSON.parse(userStr);
          this.editForm.email = this.user.email || '';
          this.editForm.phonenumber = this.user.phonenumber || '';
        }
        
        // 从后端获取最新用户信息
        const response = await apiService.getUserInfo();
        if (response.data.status === 'success') {
          this.user = response.data.user;
          this.editForm.email = this.user.email || '';
          this.editForm.phonenumber = this.user.phonenumber || '';
          localStorage.setItem('user', JSON.stringify(this.user));
        }
      } catch (error) {
        console.error('加载用户信息失败:', error);
        this.$message.error('加载用户信息失败');
      }
    },
    
    // 保存用户信息
    async saveUserInfo() {
      this.saving = true;
      
      try {
        const updateData = {
          email: this.editForm.email,
          phonenumber: this.editForm.phonenumber
        };
        
        // 只有在输入了密码时才传递密码
        if (this.editForm.password) {
          updateData.password = this.editForm.password;
        }
        
        const response = await apiService.updateUserInfo(updateData);
        
        if (response.data.status === 'success') {
          this.$message.success('信息修改成功');
          this.user = response.data.user;
          localStorage.setItem('user', JSON.stringify(this.user));
          this.showEditDialog = false;
          this.editForm.password = ''; // 清空密码字段
        } else {
          this.$message.error(response.data.message || '修改失败');
        }
      } catch (error) {
        console.error('保存用户信息失败:', error);
        if (error.response?.data?.message) {
          this.$message.error(error.response.data.message);
        } else {
          this.$message.error('保存失败，请重试');
        }
      } finally {
        this.saving = false;
      }
    },
    
    // 退出登录
    handleLogout() {
      this.$confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('isLogin');
        this.$message.success('已退出登录');
        this.$router.replace('/login');
      }).catch(() => {
        // 取消退出
      });
    },
    
    // 格式化日期
    formatDate(dateString) {
      if (!dateString) return '-';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN');
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
    
    // 加载设置
    loadSettings() {
      const settings = localStorage.getItem('settings');
      if (settings) {
        const parsedSettings = JSON.parse(settings);
        this.darkMode = parsedSettings.darkMode || false;
        this.notifications = parsedSettings.notifications !== false;
        this.autoRefresh = parsedSettings.autoRefresh !== false;
      }
    },
    
    // 保存设置
    saveSettings() {
      const settings = {
        darkMode: this.darkMode,
        notifications: this.notifications,
        autoRefresh: this.autoRefresh
      };
      localStorage.setItem('settings', JSON.stringify(settings));
    },
    
    // 切换主题
    toggleTheme() {
      this.saveSettings();
      this.$message.info(this.darkMode ? '已切换到深色模式' : '已切换到浅色模式');
    },
    
    // 切换通知
    toggleNotifications() {
      this.saveSettings();
      this.$message.info(this.notifications ? '已开启消息通知' : '已关闭消息通知');
    },
    
    // 切换自动刷新
    toggleAutoRefresh() {
      this.saveSettings();
      this.$message.info(this.autoRefresh ? '已开启自动刷新' : '已关闭自动刷新');
    }
  }
};
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.settings-header {
  text-align: center;
  margin-bottom: 30px;
}

.settings-header h1 {
  color: #333;
  font-size: 2.5em;
  margin-bottom: 10px;
}

.settings-header p {
  color: #666;
  font-size: 1.1em;
}

.settings-content {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.user-profile-card {
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #4CAF50;
  color: white;
  font-size: 2em;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.user-basic-info h2 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 1.5em;
}

.user-type {
  color: #666;
  font-size: 1em;
  margin: 0;
}

.profile-details {
  margin-bottom: 30px;
}

.profile-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.system-settings-card {
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.system-settings-card h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3em;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-item span {
  color: #333;
  font-size: 1em;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .settings-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .settings-header h1 {
    font-size: 2em;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-actions {
    flex-direction: column;
  }
  
  .profile-actions .el-button {
    width: 100%;
  }
}
</style> 