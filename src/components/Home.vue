<template>
  <div>
    <h2>欢迎来到网络流量大模型平台</h2>
    <p>这里可以查看网络流量总览、模型分析等信息。</p>
    <div style="margin-top: 32px;">
      <h3>统计总览（占位）</h3>
      <ul>
        <li>今日流量：- GB</li>
        <li>异常流量：- 次</li>
        <li>模型告警：- 条</li>
      </ul>
    </div>
    <div style="margin-top: 32px;">
      <h3>流量趋势</h3>
      <div ref="chart" style="width:100%;max-width:600px;height:320px;"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
// import axios from 'axios'; // 后端接口接入时再启用

export default {
  name: 'TrafficHome',
  mounted() {
    this.initChart();
    this.timer = setInterval(this.initChart, 10000); // 每10秒刷新
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  data() {
    return {
      timer: null,
    };
  },
  methods: {
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
        title: { text: '本周流量趋势' },
        tooltip: {},
        xAxis: { type: 'category', data: data.x },
        yAxis: { type: 'value' },
        series: [{ name: '流量', type: 'line', data: data.y }],
      });
    },
  },
};
</script> 