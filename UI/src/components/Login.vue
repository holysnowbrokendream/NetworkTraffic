<template>
  <!-- 登录页面主容器 -->
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">用户登录</h2>
      <p class="login-subtitle">网络流量分析系统</p>
      
      <!-- 登录表单 -->
      <el-form :model="form" @submit.prevent="login" @keyup.enter="login">
        <el-form-item>
          <el-input 
            v-model="form.username" 
            placeholder="用户名/邮箱/手机号" 
            clearable 
            prefix-icon="el-icon-user"
            :disabled="loading"
          />
        </el-form-item>
        <el-form-item>
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="密码" 
            clearable 
            prefix-icon="el-icon-lock" 
            show-password
            :disabled="loading"
          />
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            style="width:100%;" 
            @click="login"
            :loading="loading"
            :disabled="!form.username || !form.password"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
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
    <el-dialog v-model="showRegister" title="用户注册" width="400px" :close-on-click-modal="false">
      <el-form :model="registerForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱（选填）" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="registerForm.phonenumber" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="registerForm.user_type" placeholder="请选择用户类型">
            <el-option label="普通用户" value="user"></el-option>
            <el-option label="管理员" value="admin"></el-option>
            <el-option label="访客" value="guest"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRegister=false">取消</el-button>
        <el-button type="primary" @click="register" :loading="registerLoading">
          {{ registerLoading ? '注册中...' : '注册' }}
        </el-button>
      </template>
      <div v-if="registerMsg" :style="{color: registerSuccess ? 'green' : 'red', textAlign: 'center', marginTop: '8px'}">
        {{ registerMsg }}
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { apiService } from '../api/index.js';

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
      loading: false, // 登录加载状态
      showRegister: false, // 注册弹窗显示状态
      registerLoading: false, // 注册加载状态
      // 注册表单数据
      registerForm: {
        username: '',
        email: '',
        phonenumber: '',
        password: '',
        user_type: 'user'
      },
      registerMsg: '', // 注册结果提示
      registerSuccess: false // 注册成功状态
    };
  },
  methods: {
    // 登录方法，调用后端API
    async login() {
      this.error = '';
      this.loading = true;
      
      try {
        const response = await apiService.login({
          username: this.form.username,
          password: this.form.password
        });
        
        if (response.data.status === 'success') {
          // 保存登录状态和用户信息
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('user', JSON.stringify(response.data.user));
          localStorage.setItem('isLogin', '1');
          
          // 显示成功消息
          this.$message.success(response.data.message);
          
          // 跳转到首页
          setTimeout(() => {
            this.$router.replace('/');
          }, 1000);
        } else {
          this.error = response.data.message || '登录失败';
        }
      } catch (error) {
        if (error.response?.data?.message) {
          this.error = error.response.data.message;
        } else {
          this.error = '登录失败，请检查网络连接';
        }
      } finally {
        this.loading = false;
      }
    },
    
    // 注册方法，调用后端API
    async register() {
      this.registerMsg = '';
      this.registerLoading = true;
      
      try {
        const response = await apiService.register({
          username: this.registerForm.username,
          email: this.registerForm.email,
          phonenumber: this.registerForm.phonenumber,
          password: this.registerForm.password,
          user_type: this.registerForm.user_type
        });
        
        if (response.data.status === 'success') {
          this.registerSuccess = true;
          this.registerMsg = response.data.message;
          
          // 成功后清空表单并关闭弹窗
          setTimeout(() => {
            this.showRegister = false;
            this.registerForm = {
              username: '',
              email: '',
              phonenumber: '',
              password: '',
              user_type: 'user'
            };
            this.registerMsg = '';
            this.registerSuccess = false;
          }, 2000);
        } else {
          this.registerSuccess = false;
          this.registerMsg = response.data.message || '注册失败';
        }
      } catch (error) {
        this.registerSuccess = false;
        if (error.response?.data?.message) {
          this.registerMsg = error.response.data.message;
        } else {
          this.registerMsg = '注册失败，请检查网络连接';
        }
      } finally {
        this.registerLoading = false;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-sizing: border-box;
  padding: 0 12px;
}

/* 登录卡片样式 */
.login-card {
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  padding: 40px 35px 30px 35px;
  box-sizing: border-box;
}

.login-title {
  text-align: center;
  color: #4CAF50;
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 2em;
}

.login-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1em;
}

.login-error {
  color: #f44336;
  margin-top: 12px;
  font-size: 14px;
  text-align: center;
  padding: 8px;
  background: #fff5f5;
  border-radius: 4px;
  border: 1px solid #ffebee;
}
</style> 