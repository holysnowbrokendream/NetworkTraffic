<template>
  <el-card class="traffic-card">
    <h2 style="color:#3578e5;margin-bottom:18px;">流量明细</h2>
    <div class="upload-area">
      <el-upload
        class="upload-demo"
        drag
        :show-file-list="false"
        :before-upload="beforeUpload"
        :http-request="uploadFile"
        accept=".csv,.pcap,.psap,.txt"
      >
        <el-button type="primary">点击或拖拽上传流量数据</el-button>
        <template #tip>
          <div class="el-upload__tip">支持 .csv, .pcap, .psap, .txt 文件</div>
        </template>
      </el-upload>
      <el-alert v-if="uploadMsg" :title="uploadMsg" :type="uploadSuccess ? 'success' : 'error'" show-icon style="margin-left:12px;" :closable="false" />
    </div>
    <div class="filter-area">
      <el-input v-model="search" placeholder="搜索IP/状态" clearable style="width:180px;" />
      <el-select v-model="filterStatus" placeholder="全部状态" clearable style="width:120px;">
        <el-option label="全部状态" value="" />
        <el-option label="正常" value="正常" />
        <el-option label="异常" value="异常" />
      </el-select>
      <el-button @click="resetFilter">重置</el-button>
    </div>
    <el-table :data="pagedData" border stripe style="width: 100%;margin-bottom:18px;">
      <el-table-column prop="time" label="时间" align="center" />
      <el-table-column prop="srcIP" label="源IP" align="center" />
      <el-table-column prop="dstIP" label="目的IP" align="center" />
      <el-table-column prop="size" label="流量大小" align="center" />
      <el-table-column prop="status" label="状态" align="center" />
    </el-table>
    <div v-if="pagedData.length === 0" style="text-align:center;color:#888;margin-bottom:18px;">暂无数据</div>
    <el-pagination
      background
      layout="prev, pager, next"
      :total="filteredData.length"
      :page-size="pageSize"
      v-model:current-page="page"
      style="text-align:right;"
    />
  </el-card>
</template>

<script>
// import axios from 'axios'; // 后端接口接入时再启用
const mockData = Array.from({ length: 37 }, (_, i) => ({
  id: i + 1,
  time: `2024-06-0${(i%9)+1} 12:0${i%6}:00`,
  srcIP: `192.168.1.${(i%10)+1}`,
  dstIP: `10.0.0.${(i%8)+1}`,
  size: `${(Math.random()*100).toFixed(2)} MB`,
  status: i%5===0 ? '异常' : '正常',
}));

export default {
  name: 'TrafficDetail',
  data() {
    return {
      search: '',
      filterStatus: '',
      page: 1,
      pageSize: 10,
      allData: mockData,
      uploadMsg: '',
      uploadSuccess: false,
    };
  },
  computed: {
    filteredData() {
      let data = this.allData;
      if (this.search) {
        const s = this.search.trim();
        data = data.filter(item =>
          item.srcIP.includes(s) ||
          item.dstIP.includes(s) ||
          item.status.includes(s)
        );
      }
      if (this.filterStatus) {
        data = data.filter(item => item.status === this.filterStatus);
      }
      return data;
    },
    pagedData() {
      const start = (this.page - 1) * this.pageSize;
      return this.filteredData.slice(start, start + this.pageSize);
    },
  },
  methods: {
    resetFilter() {
      this.search = '';
      this.filterStatus = '';
    },
    beforeUpload() {
      // 阻止自动上传，改为手动处理
      return false;
    },
    async uploadFile() {
      // 取消注释后端接入
      // const formData = new FormData();
      // formData.append('file', option.file);
      // const res = await axios.post('/api/upload', formData, {
      //   headers: { 'Content-Type': 'multipart/form-data' },
      //   onUploadProgress: progressEvent => {
      //     // 可选：显示进度
      //   }
      // });
      // this.uploadMsg = '上传成功，正在分析...';
      // this.uploadSuccess = true;
      // 可根据res.data处理后续逻辑
      // mock演示：
      this.uploadMsg = '';
      this.uploadSuccess = false;
      try {
        await new Promise(r=>setTimeout(r, 1200));
        this.uploadMsg = '上传成功，正在分析...';
        this.uploadSuccess = true;
      } catch (e) {
        this.uploadMsg = '上传失败';
        this.uploadSuccess = false;
      }
    },
  },
  watch: {
    filteredData() {
      this.page = 1;
    },
  },
};
</script>

<style scoped>
.traffic-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(53,120,229,0.08);
  padding: 32px 28px 24px 28px;
  max-width: 900px;
  margin: 32px auto;
}
.upload-area {
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.filter-area {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}
</style> 