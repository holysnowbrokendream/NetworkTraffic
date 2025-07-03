<template>
  <!-- 系统设置页面，包含模型参数、告警阈值和系统信息展示 -->
  <el-row justify="center" style="margin-top:40px;">
    <el-col :span="24">
      <el-card class="settings-card">
        <!-- 标题 -->
        <div class="settings-title">系统设置</div>
        <!-- 设置表单 -->
        <el-form :model="form" label-width="120px" class="settings-form">
          <el-divider>模型参数</el-divider>
          <!-- 置信度阈值设置 -->
          <el-form-item label="置信度阈值">
            <el-slider v-model="form.confidence" :min="0.5" :max="1" :step="0.01" style="width:220px;" />
            <span style="margin-left:12px;">{{ form.confidence }}</span>
          </el-form-item>
          <!-- 最大并发数设置 -->
          <el-form-item label="最大并发数">
            <el-input-number v-model="form.maxConcurrent" :min="1" :max="32" />
          </el-form-item>
          <!-- 模型选择 -->
          <el-form-item label="模型选择">
            <el-select v-model="form.model" placeholder="请选择模型" style="width:180px;">
              <el-option label="大模型V1" value="v1" />
              <el-option label="大模型V2" value="v2" />
              <el-option label="实验模型" value="exp" />
            </el-select>
          </el-form-item>
          <el-divider>告警阈值</el-divider>
          <!-- 各类告警阈值设置 -->
          <el-form-item label="DDoS 阈值">
            <el-input-number v-model="form.ddosThreshold" :min="10" :max="10000" />
          </el-form-item>
          <el-form-item label="端口扫描阈值">
            <el-input-number v-model="form.portScanThreshold" :min="1" :max="1000" />
          </el-form-item>
          <el-form-item label="恶意登录阈值">
            <el-input-number v-model="form.loginThreshold" :min="1" :max="1000" />
          </el-form-item>
          <el-divider>系统信息</el-divider>
          <!-- 系统信息展示 -->
          <el-descriptions :column="2" border size="small" style="margin-bottom:18px;">
            <el-descriptions-item label="模型版本">{{ form.model }}</el-descriptions-item>
            <el-descriptions-item label="前端版本">v1.0.0</el-descriptions-item>
            <el-descriptions-item label="后端服务">运行中</el-descriptions-item>
            <el-descriptions-item label="上次保存">{{ lastSave }}</el-descriptions-item>
          </el-descriptions>
          <!-- 操作按钮 -->
          <el-form-item>
            <el-button type="primary" @click="save">保存设置</el-button>
            <el-button @click="reset">恢复默认</el-button>
            <span v-if="msg" style="color:green;margin-left:16px;">{{ msg }}</span>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
// import axios from 'axios'; // 后端接口接入时再启用
export default {
  name: 'SettingsPage',
  data() {
    return {
      // 设置表单数据
      form: {
        confidence: 0.8, // 置信度阈值
        maxConcurrent: 4, // 最大并发数
        model: 'v1', // 当前模型
        ddosThreshold: 100, // DDoS告警阈值
        portScanThreshold: 10, // 端口扫描告警阈值
        loginThreshold: 5, // 恶意登录告警阈值
      },
      msg: '', // 操作提示
      lastSave: '', // 上次保存时间
    };
  },
  mounted() {
    // 组件挂载后加载本地设置
    const local = JSON.parse(localStorage.getItem('settings') || '{}');
    Object.assign(this.form, local);
    this.lastSave = local.lastSave || '-';
  },
  methods: {
    // 保存设置到本地存储
    save() {
      const now = new Date().toLocaleString();
      localStorage.setItem('settings', JSON.stringify({ ...this.form, lastSave: now }));
      this.msg = '保存成功！';
      this.lastSave = now;
      setTimeout(()=>this.msg='', 2000);
    },
    // 恢复默认设置
    reset() {
      this.form = {
        confidence: 0.8,
        maxConcurrent: 4,
        model: 'v1',
        ddosThreshold: 100,
        portScanThreshold: 10,
        loginThreshold: 5,
      };
      this.msg = '已恢复默认';
      setTimeout(()=>this.msg='', 2000);
    },
  },
};
</script>

<style scoped>
/* 系统设置卡片样式 */
.settings-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(53,120,229,0.08);
  padding: 32px 28px 24px 28px;
  margin: 0 auto;
  max-width: 700px;
}
.settings-title {
  color: #3578e5;
  font-size: 26px;
  font-weight: 600;
  margin-bottom: 12px;
  text-align: center;
}
.settings-form {
  margin-top: 18px;
}
</style> 