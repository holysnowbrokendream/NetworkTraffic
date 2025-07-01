<template>
  <div>
    <h2>模型分析</h2>
    <p>此处展示大模型对网络流量的分析结果。</p>
    <div style="margin-top: 24px;">
      <h3>分析结果（占位）</h3>
      <ul>
        <li>预测异常流量：- 条</li>
        <li>最新告警：- 条</li>
        <li>模型版本：-</li>
      </ul>
    </div>
    <div style="margin-top: 32px;">
      <h3>异常分布</h3>
      <div ref="pieChart" style="width:100%;max-width:480px;height:320px;"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
// import axios from 'axios'; // 后端接口接入时再启用

export default {
  name: 'ModelAnalysis',
  mounted() {
    this.initPie();
    this.timer = setInterval(this.initPie, 10000); // 每10秒刷新
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
        title: { text: '异常类型分布', left: 'center' },
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', left: 'left' },
        series: [
          {
            name: '异常类型',
            type: 'pie',
            radius: '50%',
            data,
            emphasis: {
              itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
            }
          }
        ]
      });
    },
  },
};
</script> 