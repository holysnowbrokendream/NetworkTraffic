<template>
  <el-row justify="center" style="margin-top:40px;">
    <el-col :span="24">
      <el-card class="model-card">
        <div class="model-title">模型分析</div>
        <div class="model-desc">此处展示大模型对网络流量的分析结果。</div>
        <el-row :gutter="32" style="margin-bottom:24px;">
          <el-col :xs="24" :md="12">
            <el-card shadow="never" class="stat-card">
              <el-row :gutter="16">
                <el-col :span="12">
                  <el-statistic title="预测异常流量" :value="'- 条'" />
                </el-col>
                <el-col :span="12">
                  <el-statistic title="最新告警" :value="'- 条'" />
                </el-col>
              </el-row>
              <el-divider />
              <div style="font-weight:500;color:#3578e5;margin-bottom:8px;">异常类型分布</div>
              <div ref="pieChart" style="width:100%;max-width:340px;height:260px;margin:0 auto;"></div>
            </el-card>
          </el-col>
          <el-col :xs="24" :md="12">
            <el-card shadow="never" class="alarm-card">
              <div style="font-weight:500;color:#3578e5;margin-bottom:8px;">告警历史</div>
              <el-table :data="alarmData" border stripe size="small" style="width:100%;">
                <el-table-column prop="time" label="时间" width="120" align="center" />
                <el-table-column prop="type" label="类型" width="100" align="center" />
                <el-table-column prop="desc" label="描述" align="center" />
              </el-table>
              <div v-if="alarmData.length === 0" style="text-align:center;color:#888;margin:12px 0;">暂无告警</div>
            </el-card>
          </el-col>
        </el-row>
        <div style="text-align:right;color:#888;font-size:14px;">模型版本：-</div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
// import axios from 'axios'; // 后端接口接入时再启用
import * as echarts from 'echarts';

export default {
  name: 'ModelAnalysis',
  data() {
    return {
      timer: null,
      alarmData: [
        // 示例数据，后端接入时替换
        { time: '2024-06-01', type: 'DDoS', desc: '检测到大流量攻击' },
        { time: '2024-06-02', type: '端口扫描', desc: '异常端口扫描行为' },
        { time: '2024-06-03', type: '恶意登录', desc: '多次失败登录尝试' },
      ],
    };
  },
  mounted() {
    this.initPie();
    this.timer = setInterval(this.initPie, 10000); // 每10秒刷新
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  methods: {
    async initPie() {
      // 模拟接口请求
      // const res = await axios.get('/api/model/abnormal-distribution');
      // const data = res.data;
      const data = [
        { value: 1048, name: '端口扫描' },
        { value: 735, name: 'DDoS' },
        { value: 580, name: '恶意登录' },
        { value: 484, name: '数据泄露' },
      ];
      const chart = echarts.init(this.$refs.pieChart);
      chart.setOption({
        title: { text: '', left: 'center' },
        tooltip: { trigger: 'item' },
        legend: { orient: 'horizontal', bottom: 0, left: 'center' },
        series: [
          {
            name: '异常类型',
            type: 'pie',
            radius: ['50%', '75%'],
            center: ['50%', '45%'],
            data,
            label: {
              show: true,
              formatter: '{b}',
              overflow: 'break',
              alignTo: 'edge',
              minMargin: 5,
              edgeDistance: 10,
              lineHeight: 18,
            },
            labelLayout: {
              hideOverlap: true
            },
            emphasis: {
              itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.15)' }
            }
          }
        ]
      });
    },
  },
};
</script>

<style scoped>
.model-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(53,120,229,0.08);
  padding: 32px 28px 24px 28px;
  margin: 0 auto;
  max-width: 1200px;
}
.model-title {
  color: #3578e5;
  font-size: 26px;
  font-weight: 600;
  margin-bottom: 12px;
  text-align: center;
}
.model-desc {
  color: #666;
  font-size: 16px;
  margin-bottom: 24px;
  text-align: center;
}
.stat-card, .alarm-card {
  margin-bottom: 0;
  min-height: 340px;
}
</style> 