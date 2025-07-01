<template>
  <div style="max-width:480px;margin:32px auto;">
    <h2>系统设置</h2>
    <form @submit.prevent="save">
      <div style="margin-bottom:16px;">
        <label>模型参数：</label>
        <input v-model="modelParam" placeholder="如：0.8" style="width:120px;" />
      </div>
      <div style="margin-bottom:16px;">
        <label>告警阈值：</label>
        <input v-model="alarmThreshold" placeholder="如：100" style="width:120px;" />
      </div>
      <button type="submit">保存设置</button>
      <span v-if="msg" style="color:green;margin-left:16px;">{{ msg }}</span>
    </form>
  </div>
</template>

<script>
// import axios from 'axios'; // 后端接口接入时再启用
export default {
  name: 'SettingsPage',
  data() {
    return {
      modelParam: '',
      alarmThreshold: '',
      msg: '',
    };
  },
  mounted() {
    // 模拟获取设置
    // axios.get('/api/settings').then(res => { ... })
    const local = JSON.parse(localStorage.getItem('settings') || '{}');
    this.modelParam = local.modelParam || '';
    this.alarmThreshold = local.alarmThreshold || '';
  },
  methods: {
    save() {
      // axios.post('/api/settings', { modelParam: this.modelParam, alarmThreshold: this.alarmThreshold })
      localStorage.setItem('settings', JSON.stringify({ modelParam: this.modelParam, alarmThreshold: this.alarmThreshold }));
      this.msg = '保存成功！';
      setTimeout(()=>this.msg='', 2000);
    },
  },
};
</script> 