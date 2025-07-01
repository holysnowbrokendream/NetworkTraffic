<template>
  <div>
    <h2>流量明细</h2>
    <div style="margin-bottom: 16px;">
      <!-- 上传区域 -->
      <form @submit.prevent="uploadFile" style="display:inline-block;margin-right:16px;">
        <input type="file" @change="onFileChange" accept=".csv,.pcap,.psap,.txt" />
        <button type="submit" :disabled="!selectedFile || uploading">上传</button>
      </form>
      <span style="font-size:12px;color:#888;">支持 .csv, .pcap, .psap, .txt 文件</span>
      <span v-if="uploading">上传中...</span>
      <span v-if="uploadMsg" :style="{color: uploadSuccess ? 'green' : 'red'}">{{ uploadMsg }}</span>
    </div>
    <div style="margin-bottom: 16px;">
      <input v-model="search" placeholder="搜索IP/状态" style="margin-right:8px;" />
      <select v-model="filterStatus" style="margin-right:8px;">
        <option value="">全部状态</option>
        <option value="正常">正常</option>
        <option value="异常">异常</option>
      </select>
      <button @click="resetFilter">重置</button>
    </div>
    <table border="1" cellpadding="8" style="width: 100%;">
      <thead>
        <tr>
          <th>时间</th>
          <th>源IP</th>
          <th>目的IP</th>
          <th>流量大小</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in pagedData" :key="item.id">
          <td>{{ item.time }}</td>
          <td>{{ item.srcIP }}</td>
          <td>{{ item.dstIP }}</td>
          <td>{{ item.size }}</td>
          <td>{{ item.status }}</td>
        </tr>
        <tr v-if="pagedData.length === 0">
          <td colspan="5" style="text-align:center;">暂无数据</td>
        </tr>
      </tbody>
    </table>
    <div style="margin-top: 16px; text-align:right;">
      <button :disabled="page===1" @click="page--">上一页</button>
      <span style="margin:0 8px;">{{ page }}/{{ totalPages }}</span>
      <button :disabled="page===totalPages" @click="page++">下一页</button>
    </div>
  </div>
</template>

<script>
const mockData = Array.from({ length: 37 }, (_, i) => ({
  id: i + 1,
  time: `2024-06-0${(i%9)+1} 12:0${i%6}:00`,
  srcIP: `192.168.1.${(i%10)+1}`,
  dstIP: `10.0.0.${(i%8)+1}`,
  size: `${(Math.random()*100).toFixed(2)} MB`,
  status: i%5===0 ? '异常' : '正常',
}));

// import axios from 'axios'; // 后端接口接入时再启用

export default {
  name: 'TrafficDetail',
  data() {
    return {
      search: '',
      filterStatus: '',
      page: 1,
      pageSize: 10,
      allData: mockData,
      // 上传相关
      selectedFile: null,
      uploading: false,
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
    totalPages() {
      return Math.max(1, Math.ceil(this.filteredData.length / this.pageSize));
    },
    pagedData() {
      const start = (this.page - 1) * this.pageSize;
      return this.filteredData.slice(start, start + this.pageSize);
    },
  },
  watch: {
    filteredData() {
      this.page = 1;
    },
  },
  methods: {
    resetFilter() {
      this.search = '';
      this.filterStatus = '';
    },
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
      this.uploadMsg = '';
    },
    async uploadFile() {
      if (!this.selectedFile) return;
      this.uploading = true;
      this.uploadMsg = '';
      this.uploadSuccess = false;
      try {
        // 取消注释后端接入
        // const formData = new FormData();
        // formData.append('file', this.selectedFile);
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
        await new Promise(r=>setTimeout(r, 1200));
        this.uploadMsg = '上传成功，正在分析...';
        this.uploadSuccess = true;
      } catch (e) {
        this.uploadMsg = '上传失败';
        this.uploadSuccess = false;
      } finally {
        this.uploading = false;
        this.selectedFile = null;
      }
    },
  },
};
</script> 