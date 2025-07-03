<template>
  <!-- 首页布局，包含欢迎语、统计信息、趋势图和告警表格 -->
  <el-row justify="center" style="margin-top:8px;">
    <el-col :span="24">
      <el-card class="home-card">
        <!-- 欢迎标题 -->
        <div class="home-title">欢迎来到网络流量大模型平台</div>
        <!-- 平台描述 -->
        <div class="home-desc">这里可以查看网络流量总览、模型分析等信息。</div>
        <!-- 统计信息区 -->
        <el-row :gutter="24" class="stats-list">
          <el-col :span="8">
            <el-statistic title="今日流量" :value="'- GB'" />
          </el-col>
          <el-col :span="8">
            <el-statistic title="异常流量" :value="'- 次'" />
          </el-col>
          <el-col :span="8">
            <el-statistic title="模型告警" :value="'- 条'" />
          </el-col>
        </el-row>
        <el-divider />
        <el-row :gutter="32">
          <!-- 左侧趋势图 -->
          <el-col :xs="24" :md="12">
            <div class="chart-area">
              <div style="font-weight:500;color:#3578e5;margin-bottom:8px;">流量趋势</div>
              <div ref="chart" style="width:100%;max-width:520px;height:300px;margin:0 auto;"></div>
            </div>
            <div class="chart-area" style="margin-top:18px;">
              <div style="font-weight:500;color:#e67e22;margin-bottom:8px;">异常趋势</div>
              <div ref="abnormalChart" style="width:100%;max-width:520px;height:220px;margin:0 auto;"></div>
            </div>
          </el-col>
          <!-- 右侧告警表格 -->
          <el-col :xs="24" :md="12">
            <el-card shadow="never" class="alarm-card">
              <div style="font-weight:500;color:#e74c3c;margin-bottom:8px;">最新告警</div>
              <el-table :data="alarmData" border stripe size="small" style="width:100%;">
                <el-table-column prop="time" label="时间" width="120" align="center" />
                <el-table-column prop="type" label="类型" width="100" align="center" />
                <el-table-column prop="desc" label="描述" align="center" />
              </el-table>
              <div v-if="alarmData.length === 0" style="text-align:center;color:#888;margin:12px 0;">暂无告警</div>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
// import axios from 'axios'; // 后端接口接入时再启用
import * as echarts from 'echarts';

export default {
  name: 'TrafficHome',
  data() {
    return {
      timer: null, // 定时器句柄-流量趋势
      abnormalTimer: null, // 定时器句柄-异常趋势
      alarmData: [
        { time: '2024-06-01', type: 'DDoS', desc: '检测到大流量攻击' },
        { time: '2024-06-02', type: '端口扫描', desc: '异常端口扫描行为' },
        { time: '2024-06-03', type: '恶意登录', desc: '多次失败登录尝试' },
      ],
    };
  },
  mounted() {
    this.initChart();
    this.initAbnormalChart();
    this.timer = setInterval(this.initChart, 10000); // 每10秒刷新流量趋势
    this.abnormalTimer = setInterval(this.initAbnormalChart, 10000); // 每10秒刷新异常趋势
  },
  beforeUnmount() {
    clearInterval(this.timer);
    clearInterval(this.abnormalTimer);
  },
  methods: {
    // 初始化流量趋势图
    async initChart() {
      // 模拟接口请求
      // const res = await axios.get('/api/traffic/trend');
      // const data = res.data;
      const data = {
        x: ['周一','周二','周三','周四','周五','周六','周日'],
        y: [120, 200, 150, 80, 70, 110, 130],
      };
      const chart = echarts.init(this.$refs.chart);
      chart.setOption({
        title: { text: '', left: 'center' },
        tooltip: {},
        xAxis: { type: 'category', data: data.x },
        yAxis: { type: 'value' },
        series: [{ name: '流量', type: 'line', data: data.y, smooth: true, lineStyle: { width: 3, color: '#3578e5' }, areaStyle: { color: '#e0eafc' } }],
        grid: { left: 40, right: 20, top: 30, bottom: 30 },
      });
    },
    // 初始化异常趋势图
    async initAbnormalChart() {
      // 模拟异常趋势数据
      const data = {
        x: ['周一','周二','周三','周四','周五','周六','周日'],
        y: [5, 8, 6, 2, 1, 4, 7],
      };
      const chart = echarts.init(this.$refs.abnormalChart);
      chart.setOption({
        title: { text: '', left: 'center' },
        tooltip: {},
        xAxis: { type: 'category', data: data.x },
        yAxis: { type: 'value' },
        series: [{ name: '异常', type: 'bar', data: data.y, itemStyle: { color: '#e67e22' } }],
        grid: { left: 40, right: 20, top: 30, bottom: 30 },
      });
    },
  },
};
</script>

<style scoped>
/* 首页卡片样式 */
.home-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(53,120,229,0.08);
  padding: 32px 28px 24px 28px;
  margin: 0 auto;
  max-width: 1200px;
}
.home-title {
  color: #3578e5;
  font-size: 26px;
  font-weight: 600;
  margin-bottom: 12px;
  text-align: center;
}
.home-desc {
  color: #666;
  font-size: 16px;
  margin-bottom: 24px;
  text-align: center;
}
.stats-list {
  margin-bottom: 16px;
}
.chart-area {
  margin-top: 12px;
  background: #f8fafc;
  border-radius: 10px;
  padding: 18px 12px 8px 12px;
  box-shadow: 0 1px 4px rgba(53,120,229,0.04);
}
.alarm-card {
  min-height: 400px;
  margin-top: 0;
}
</style> 