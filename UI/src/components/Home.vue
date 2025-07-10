<template>
  <div id="app" class="ai-chat-app app-root">
    <!-- 蓝色棒状侧边框 -->
    <div class="sidebar-container" :class="{ 'sidebar-expanded': sidePanelExpanded }">
      <div class="blue-bar">
        <button 
          class="expand-btn" 
          @click="toggleSidePanel"
          :title="!sidePanelExpanded ? '展开历史文件' : '收起历史文件'"
        >
          <el-icon>
            <el-icon-arrow-right v-if="!sidePanelExpanded" />
            <el-icon-arrow-left v-if="sidePanelExpanded" />
          </el-icon>
        </button>
        
        <!-- 登录/退出登录按钮 -->
        <button 
          v-if="!isLogin"
          class="login-btn" 
          @click="goLogin"
          title="登录"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
          </svg>
        </button>
        
        <button 
          v-if="isLogin"
          class="logout-btn" 
          @click="logout"
          title="退出登录"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M16 17v-3H9v-4h7V7l5 5-5 5M14 2a2 2 0 0 1 2 2v2h-2V4H4v16h10v-2h2v2a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h10z"/>
          </svg>
        </button>
      </div>
      
      <!-- 展开的历史文件面板 -->
      <div 
        class="history-panel" 
        :class="{ expanded: sidePanelExpanded }"
        v-if="sidePanelExpanded"
      >
        <div class="history-header">
          <h3>历史文件</h3>
        </div>
        <div class="history-content">
          <div class="file-list">
            <div v-for="file in userFiles" :key="file.file_id" class="file-item">
              <el-link :href="file.url" target="_blank">
                {{ file.filename }}
              </el-link>
              <el-button 
                type="danger" 
                size="mini" 
                @click="deleteFile(file.file_id)" 
                title="删除" 
                circle 
                class="delete-btn"
              >×</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content" :class="{ 'sidebar-expanded': sidePanelExpanded }">
      <!-- 顶部标题栏 -->
      <div class="content-header">
        <span class="app-title">网络流量研判大模型对话助手</span>
      </div>

      <!-- 对话区域 -->
      <div class="chat-container">
        <div class="chat-messages-area">
          <div v-for="(msg, idx) in messages" :key="idx" :class="['chat-bubble-container', msg.role]">
            <!-- AI消息：头像 + 泡泡 -->
            <template v-if="msg.role === 'ai'">
              <div class="ai-avatar">AI</div>
              <div class="chat-bubble ai-bubble">
                <div class="bubble-content">
                  <template v-if="msg.files && msg.files.length">
                    <div v-for="file in msg.files" :key="file.file_id" class="file-link">
                      <el-link :href="file.url" target="_blank">{{ file.filename }}</el-link>
                    </div>
                    <div v-if="msg.content" class="message-text">{{ msg.content }}</div>
                  </template>
                  <template v-else-if="msg.file">
                    <div class="file-link">
                      <el-link :href="msg.file.url" target="_blank">{{ msg.file.filename }}</el-link>
                    </div>
                  </template>
                  <template v-else>
                    <div class="message-text">{{ msg.content }}</div>
                  </template>
                </div>
                <div class="bubble-tail ai-tail"></div>
              </div>
            </template>
            
            <!-- 用户消息：只有泡泡 -->
            <template v-else>
              <div class="chat-bubble user-bubble">
                <div class="bubble-content">
                  <template v-if="msg.files && msg.files.length">
                    <div v-for="file in msg.files" :key="file.file_id" class="file-link">
                      <el-link :href="file.url" target="_blank">{{ file.filename }}</el-link>
                    </div>
                    <div v-if="msg.content" class="message-text">{{ msg.content }}</div>
                  </template>
                  <template v-else-if="msg.file">
                    <div class="file-link">
                      <el-link :href="msg.file.url" target="_blank">{{ msg.file.filename }}</el-link>
                    </div>
                  </template>
                  <template v-else>
                    <div class="message-text">{{ msg.content }}</div>
                  </template>
                </div>
                <div class="bubble-tail user-tail"></div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- 底部输入区域 -->
      <div class="input-section">
        <div v-if="!isLogin" class="login-notice">请先登录后使用对话和上传服务</div>
        
        <div class="pending-files-area" v-if="pendingFiles.length">
          <span v-for="file in pendingFiles" :key="file.file_id" class="pending-file-item">
            <el-link :href="file.url" target="_blank">{{ file.filename }}</el-link>
            <el-button type="text" @click="removePendingFile(file.file_id)" class="pending-delete-btn" title="删除">×</el-button>
          </span>
        </div>
        
        <div v-if="mode==='pcap'||mode==='rules'" class="mode-indicator">
          <span>当前模式：<b>{{ mode==='pcap' ? '流量分析报告' : '流量规则' }}</b></span>
          <el-input v-model="customFileName" size="small" style="width:180px;margin-left:12px;" :placeholder="mode==='pcap'?'pcap.txt':'rules.txt'" />
          <el-button size="small" type="text" style="margin-left:12px;" @click="cancelMode">取消指令</el-button>
        </div>
        
        <!-- 统一的大输入框容器 -->
        <div class="unified-input-box">
          <!-- 上部分：文本输入区域 -->
          <div class="text-input-area">
            <textarea
              v-model="inputMsg"
              placeholder="和我聊聊天吧 (Enter发送，Shift+Enter换行)"
              class="custom-textarea"
              :disabled="!isLogin"
              :maxlength="2000"
              @keydown="handleKeyDown"
            ></textarea>
            <div class="char-count">{{ inputMsg.length }}/2000</div>
          </div>
          
          <!-- 下部分：按钮区域 -->
          <div class="button-area">
            <!-- 左侧按钮组 -->
            <div class="left-buttons">
              <el-button size="small" :disabled="!isLogin" @click="openUploadDialog" class="box-button">上传文件</el-button>
              <el-dropdown @command="handleModeCommand" trigger="click">
                <el-button size="small" :disabled="!isLogin" class="box-button">
                  指令选择<el-icon-arrow-down />
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="pcap">生成pcap.txt</el-dropdown-item>
                    <el-dropdown-item command="rules">生成rules.txt</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            
            <!-- 右侧发送按钮 -->
            <div class="right-buttons">
              <el-button type="primary" @click="sendMsg" :disabled="!isLogin" class="send-box-button">发送</el-button>
            </div>
          </div>
          
          <!-- 隐藏的上传组件 -->
          <el-upload
            class="upload-btn"
            :show-file-list="false"
            :http-request="uploadFile"
            :disabled="!isLogin"
            multiple
            style="display:none"
            ref="uploadComponent"
          >
            <el-button size="small" :disabled="!isLogin">上传文件</el-button>
          </el-upload>
        </div>
        
        <!-- AI 免责声明 -->
        <div class="ai-disclaimer">
          内容由 AI 生成，请仔细甄别
        </div>
      </div>
    </div>

    <!-- 对话框 -->
    <el-dialog v-model="createDialogVisible" title="生成文件" width="300px">
      <el-input v-model="createFileName" placeholder="文件名" />
      <template #footer>
        <el-button @click="createDialogVisible=false">取消</el-button>
        <el-button type="primary" @click="createTxtFile">生成</el-button>
      </template>
    </el-dialog>
    
    <!-- 隐藏的文件上传输入 -->
    <input ref="uploadInput" type="file" style="display:none" multiple @change="handleMultiUpload" />
  </div>
</template>

<script>
import { ref, nextTick, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { ArrowDown, ArrowRight, ArrowLeft } from '@element-plus/icons-vue';
export default {
  name: 'Home',
  components: { 
    'el-icon-arrow-down': ArrowDown,
    'el-icon-arrow-right': ArrowRight,
    'el-icon-arrow-left': ArrowLeft
  },
  setup() {
    const router = useRouter();
    const isLogin = ref(localStorage.getItem('isLogin') === '1');
    const messages = ref([
      { role: 'ai', content: '你好，有什么可以帮你？' }
    ]);
    const inputMsg = ref('');
    const uploadedFileIds = ref([]); // 存储已上传文件id
    const userFiles = ref([]);
    const createDialogVisible = ref(false);
    const createFileName = ref('');
    let createFileType = 'pcap';
    const uploadInput = ref(null);
    const uploadComponent = ref(null);
    const pendingFiles = ref([]); // 待发送文件列表
    const mode = ref('chat'); // chat/pcap/rules
    const customFileName = ref(''); // 新增：自定义生成文件名
    const sidePanelExpanded = ref(false);
    // 切换侧边面板
    const toggleSidePanel = () => {
      sidePanelExpanded.value = !sidePanelExpanded.value;
    };
    // 跳转登录页
    const goLogin = () => {
      router.push('/login');
    };
    // 退出登录
    const logout = () => {
      localStorage.removeItem('isLogin');
      isLogin.value = false;
      ElMessage.success('已退出登录');
    };
    // 处理键盘事件
    const handleKeyDown = (event) => {
      if (event.key === 'Enter') {
        if (event.shiftKey) {
          // Shift+Enter：换行，不阻止默认行为
          return;
        } else {
          // Enter：发送消息
          event.preventDefault();
          sendMsg();
        }
      }
    };

    // 发送消息
    const sendMsg = async () => {
      if (!isLogin.value) return;
      if (!inputMsg.value.trim() && pendingFiles.value.length === 0) return;
      if (mode.value === 'chat') {
        // 普通对话
        messages.value.push({ role: 'user', content: inputMsg.value, files: [...pendingFiles.value] });
        const file_ids = pendingFiles.value.map(f => f.file_id);
        inputMsg.value = '';
        pendingFiles.value = [];
        uploadedFileIds.value = [];
        try {
          const res = await axios.post('http://localhost:8000/api/llm/chat/', {
            messages: messages.value,
            file_ids: file_ids
          });
          messages.value.push({ role: 'ai', content: res.data.reply });
        } catch (e) {
          messages.value.push({ role: 'ai', content: '大模型接口异常' });
        }
      } else if (mode.value === 'pcap' || mode.value === 'rules') {
        // 生成txt文件，内容为：上传文件名+对话内容
        const filenames = pendingFiles.value.map(f => f.filename).join(', ');
        const content = filenames + (inputMsg.value ? (filenames ? ' ' : '') + inputMsg.value : '');
        const filename = customFileName.value.trim() || (mode.value === 'pcap' ? 'pcap.txt' : 'rules.txt');
        try {
          const res = await axios.post('http://localhost:8000/api/modeltask/create_txt_file/', {
            filename: filename,
            filetype: mode.value,
            content: content
          }, {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
          });
          // 由AI发送生成的文件
          messages.value.push({ role: 'user', content: (pendingFiles.value.length ? '\n' : '') + inputMsg.value, files: [...pendingFiles.value] });
          messages.value.push({ role: 'ai', content: '', files: [res.data] });
          ElMessage.success('文件生成成功');
          fetchUserFiles();
        } catch (e) {
          ElMessage.error('文件生成失败');
        }
        inputMsg.value = '';
        pendingFiles.value = [];
        uploadedFileIds.value = [];
        customFileName.value = '';
        mode.value = 'chat';
      }
    };
    // 文件上传（多文件），上传后暂存到 pendingFiles
    const uploadFile = async (option) => {
      if (!isLogin.value) return;
      const formData = new FormData();
      formData.append('file', option.file);
      try {
        const res = await axios.post('http://localhost:8000/api/modeltask/multi_upload/', formData, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        if (res.data.files && res.data.files.length > 0) {
          res.data.files.forEach(f => {
            pendingFiles.value.push(f);
            uploadedFileIds.value.push(f.file_id);
          });
          ElMessage.success('文件上传成功');
          fetchUserFiles();
        }
        option.onSuccess && option.onSuccess({}, option.file);
      } catch (e) {
        ElMessage.error('文件上传失败');
        option.onError && option.onError(e, option.file);
      }
    };
    // 多文件上传弹窗
    const openUploadDialog = () => {
      uploadInput.value && uploadInput.value.click();
    };
    const handleMultiUpload = async (e) => {
      if (!isLogin.value) return;
      const files = e.target.files;
      if (!files.length) return;
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
      }
      try {
        const res = await axios.post('http://localhost:8000/api/modeltask/multi_upload/', formData, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        if (res.data.files && res.data.files.length > 0) {
          res.data.files.forEach(f => {
            pendingFiles.value.push(f);
            uploadedFileIds.value.push(f.file_id);
          });
          ElMessage.success('文件上传成功');
          fetchUserFiles();
        }
      } catch (e) {
        ElMessage.error('文件上传失败');
      }
    };
    // 移除待发送文件
    const removePendingFile = (file_id) => {
      pendingFiles.value = pendingFiles.value.filter(f => f.file_id !== file_id);
      uploadedFileIds.value = uploadedFileIds.value.filter(id => id !== file_id);
    };
    // 指令选择处理
    const handleModeCommand = (command) => {
      mode.value = command;
      customFileName.value = command === 'pcap' ? 'pcap.txt' : 'rules.txt';
    };
    // 取消指令
    const cancelMode = () => {
      mode.value = 'chat';
      customFileName.value = '';
    };
    // 生成txt文件弹窗（不再直接用，保留）
    const openCreateDialog = (type) => {
      createFileType = type;
      createFileName.value = type === 'pcap' ? 'pcap.txt' : 'rules.txt';
      createDialogVisible.value = true;
    };
    const createTxtFile = async () => {
      if (!isLogin.value) return;
      const filename = createFileName.value.trim();
      if (!filename) {
        ElMessage.warning('请输入文件名');
        return;
      }
      try {
        const res = await axios.post('http://localhost:8000/api/modeltask/create_txt_file/', {
          filename,
          filetype: createFileType
        }, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        pendingFiles.value.push(res.data);
        uploadedFileIds.value.push(res.data.file_id);
        ElMessage.success('文件生成成功');
        fetchUserFiles();
        createDialogVisible.value = false;
      } catch (e) {
        ElMessage.error('文件生成失败');
      }
    };
    // 获取用户文件历史
    const fetchUserFiles = async () => {
      if (!isLogin.value) return;
      try {
        const res = await axios.get('http://localhost:8000/api/modeltask/list_user_files/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        userFiles.value = res.data.files || [];
      } catch (e) {
        userFiles.value = [];
      }
    };
    // 删除文件
    const deleteFile = async (file_id) => {
      try {
        await axios.post('http://localhost:8000/api/modeltask/delete_user_file/', { file_id }, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        ElMessage.success('删除成功');
        fetchUserFiles();
      } catch (e) {
        ElMessage.error('删除失败');
      }
    };
    window.addEventListener('storage', () => {
      isLogin.value = localStorage.getItem('isLogin') === '1';
      fetchUserFiles();
    });
    onMounted(() => {
      fetchUserFiles();
    });
    return {
      isLogin,
      goLogin,
      logout,
      messages,
      inputMsg,
      sendMsg,
      handleKeyDown,
      uploadFile,
      userFiles,
      openCreateDialog,
      createDialogVisible,
      createFileName,
      createTxtFile,
      uploadInput,
      openUploadDialog,
      handleMultiUpload,
      deleteFile,
      handleModeCommand,
      uploadComponent,
      pendingFiles,
      removePendingFile,
      mode,
      customFileName,
      cancelMode,
      sidePanelExpanded,
      toggleSidePanel
    };
  }
};
</script>

<style>
/* 全局样式重置 */
html, body {
  margin: 0 !important;
  padding: 0 !important;
  height: 100vh !important;
  width: 100vw !important;
  overflow: hidden !important;
  background: #1a1a1a !important;
  box-sizing: border-box;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

*, *::before, *::after {
  box-sizing: border-box;
}

#app {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #1a1a1a;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.ai-chat-app.app-root {
  height: 100vh;
  width: 100vw;
  background: #1a1a1a;
  display: flex;
  align-items: stretch;
  justify-content: flex-start;
  box-sizing: border-box;
  position: relative;
  overflow: hidden;
  margin: 0;
  padding: 0;
}
.sidebar-container {
  width: 80px;
  background: transparent;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: flex-start;
  box-sizing: border-box;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 1000;
  transition: width 0.25s cubic-bezier(.4,0,.2,1);
}
.sidebar-container.sidebar-expanded {
  width: 420px;
}
.blue-bar {
  width: 80px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  background: #2d3748;
  padding: 20px 0;
  box-sizing: border-box;
}
.expand-btn {
  background: #4a5568;
  border: none;
  border-radius: 10px;
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  transition: all 0.25s ease-in-out;
  color: #e2e8f0;
  font-size: 20px;
}
.expand-btn:hover {
  transform: scale(1.05);
  background: #718096;
}
.sidebar-container.sidebar-expanded .expand-btn {
  background: #2d3748;
  border: 1px solid #4a5568;
  color: #81c784;
  box-shadow: 0 12px 40px rgba(129, 199, 132, 0.4);
}

/* 登录按钮样式 */
.login-btn {
  background: #4a5568;
  border: none;
  border-radius: 10px;
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  transition: all 0.25s ease-in-out;
  color: #81c784;
}

.login-btn:hover {
  transform: scale(1.05);
  background: #81c784;
  color: #1a202c;
  box-shadow: 0 4px 12px rgba(129, 199, 132, 0.4);
}

/* 退出登录按钮样式 */
.logout-btn {
  background: #4a5568;
  border: none;
  border-radius: 10px;
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  transition: all 0.25s ease-in-out;
  color: #e53e3e;
}

.logout-btn:hover {
  transform: scale(1.05);
  background: #e53e3e;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.4);
}
.history-panel {
  width: 340px;
  background: #2d3748;
  border-radius: 0 14px 14px 0;
  box-shadow: 2px 0 12px rgba(0,0,0,0.3);
  padding: 20px 18px 15px 18px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  transition: all 0.25s cubic-bezier(.4,0,.2,1);
  overflow: hidden;
  height: 100vh;
  position: absolute;
  left: 80px;
  top: 0;
  z-index: 998;
}
.history-panel.expanded {
  opacity: 1;
  visibility: visible;
}
.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid #4a5568;
  margin-bottom: 10px;
}
.history-header h3 {
  font-size: 18px;
  color: #81c784;
  font-weight: 600;
  margin: 0;
}
.history-content {
  flex: 1;
  overflow-y: auto;
  max-height: calc(100vh - 120px);
  scrollbar-width: thin;
  scrollbar-color: #4a5568 transparent;
}

/* 历史文件栏滚动条样式 */
.history-content::-webkit-scrollbar {
  width: 8px;
}

.history-content::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 4px;
}

.history-content::-webkit-scrollbar-thumb {
  background: #4a5568;
  border-radius: 4px;
  border: 1px solid transparent;
  background-clip: content-box;
  transition: all 0.25s ease;
}

.history-content::-webkit-scrollbar-thumb:hover {
  background: #718096;
  background-clip: content-box;
}

.history-content::-webkit-scrollbar-thumb:active {
  background: #81c784;
  background-clip: content-box;
}

.file-list {
  flex: 1 1 auto;
  overflow-y: auto;
  max-height: calc(100vh - 120px);
  scrollbar-width: thin;
  scrollbar-color: #4a5568 transparent;
}

/* 文件列表滚动条样式 */
.file-list::-webkit-scrollbar {
  width: 8px;
}

.file-list::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 4px;
}

.file-list::-webkit-scrollbar-thumb {
  background: #4a5568;
  border-radius: 4px;
  border: 1px solid transparent;
  background-clip: content-box;
  transition: all 0.25s ease;
}

.file-list::-webkit-scrollbar-thumb:hover {
  background: #718096;
  background-clip: content-box;
}

.file-list::-webkit-scrollbar-thumb:active {
  background: #81c784;
  background-clip: content-box;
}
.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  padding: 4px 8px;
  border-radius: 6px;
  background: transparent;
  transition: all 0.25s ease;
  width: 100%;
  max-width: 320px;
}

.file-item:hover {
  background: rgba(74, 85, 104, 0.3);
}

.file-item .el-link {
  flex: 1 1 auto;
  margin-right: 12px;
  color: #e2e8f0 !important;
  text-decoration: none !important;
  transition: color 0.25s ease;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: calc(100% - 40px);
  display: block;
}

.file-item .el-link:hover {
  color: #81c784 !important;
}
.main-content {
  position: fixed;
  left: 80px;
  top: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  background: #1a1a1a;
  transition: left 0.25s cubic-bezier(.4,0,.2,1);
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  overflow: hidden;
}
.main-content.sidebar-expanded {
  left: 420px;
}
@media (max-width: 600px) {
  .sidebar-container {
    width: 60px;
  }
  .sidebar-container.sidebar-expanded {
    width: 360px;
  }
  .blue-bar {
    width: 60px;
  }
  .history-panel {
    width: 300px;
    left: 60px;
    padding: 18px 15px 12px 15px;
  }
  .main-content {
    left: 60px;
  }
  .main-content.sidebar-expanded {
    left: 360px;
  }
  .content-header {
    padding: 12px 15px;
  }
  .app-title {
    font-size: 20px;
  }
  .chat-container {
    padding: 12px 15px;
  }
  .chat-messages-area {
    height: 50vh;
    padding: 12px;
  }
  .input-section {
    padding: 12px 15px 6px 15px;
  }
  .input-controls {
    max-width: 100%;
    flex-wrap: wrap;
    gap: 8px;
  }
  .message-input {
    max-width: 100%;
    min-width: 200px;
  }
}
/* 新的布局样式 */
.content-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 12px 20px;
  background: #1a1a1a;
  border-bottom: none;
  margin: 0;
  box-sizing: border-box;
}
.app-title {
  font-size: 18px;
  color: #81c784;
  font-weight: 600;
  text-align: center;
  letter-spacing: 0.5px;
}
.header-actions {
  display: flex;
  gap: 12px;
}

.chat-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px 20px;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.chat-messages-area {
  width: 100%;
  max-width: 800px;
  height: 60vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px 20px 20px 0;
  background: #1a1a1a;
  border: none;
  border-radius: 0;
  box-shadow: none;
  margin: 0;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: #4a5568 transparent;
}

/* 聊天消息区域滚动条样式 */
.chat-messages-area::-webkit-scrollbar {
  width: 12px;
}

.chat-messages-area::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 6px;
}

.chat-messages-area::-webkit-scrollbar-thumb {
  background: #4a5568;
  border-radius: 6px;
  border: 2px solid transparent;
  background-clip: content-box;
  transition: all 0.25s ease;
}

.chat-messages-area::-webkit-scrollbar-thumb:hover {
  background: #718096;
  background-clip: content-box;
}

.chat-messages-area::-webkit-scrollbar-thumb:active {
  background: #81c784;
  background-clip: content-box;
}

/* 聊天泡泡容器样式 */
.chat-bubble-container {
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  position: relative;
  width: 100%;
  overflow: hidden;
}

.chat-bubble-container.ai {
  justify-content: flex-start;
}

.chat-bubble-container.user {
  justify-content: flex-end;
  padding-right: 2px;
}

/* AI头像样式 */
.ai-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #4a5568;
  border: 2px solid #718096;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #81c784;
  font-weight: bold;
  font-size: 14px;
  margin-right: 12px;
  flex-shrink: 0;
  box-shadow: 0 3px 12px rgba(0,0,0,0.4);
  transition: all 0.25s ease;
}

/* 聊天泡泡基础样式 */
.chat-bubble {
  position: relative;
  border-radius: 20px;
  box-shadow: 0 3px 15px rgba(0,0,0,0.3);
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  box-sizing: border-box;
}

/* AI泡泡最大宽度 */
.ai-bubble {
  max-width: calc(100% - 60px);
}

/* 用户泡泡最大宽度和最小左边距 */
.user-bubble {
  max-width: 80%;
  margin-left: 10px;
}

/* AI泡泡样式 */
.ai-bubble {
  background: #2d3748;
  border: 1px solid #4a5568;
  color: #e2e8f0;
  border-bottom-left-radius: 6px;
}

/* 用户泡泡样式 */
.user-bubble {
  background: #4a5568;
  border: 1px solid #718096;
  color: #e2e8f0;
  border-bottom-right-radius: 6px;
}

/* 泡泡内容区域 */
.bubble-content {
  padding: 15px 18px;
  line-height: 1.5;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

/* 泡泡小尾巴 */
.bubble-tail {
  position: absolute;
  bottom: 0;
  width: 0;
  height: 0;
}

.ai-tail {
  left: -8px;
  border-right: 12px solid #2d3748;
  border-bottom: 12px solid transparent;
}

.user-tail {
  right: -8px;
  border-left: 12px solid #4a5568;
  border-bottom: 12px solid transparent;
}

/* 消息文本样式 */
.message-text {
  color: #e2e8f0;
  font-size: 16px;
  word-break: break-word;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  margin: 0;
  width: 100%;
  overflow: hidden;
}

/* 文件链接样式 */
.file-link {
  margin-bottom: 8px;
}

.file-link:last-child {
  margin-bottom: 0;
}

.chat-bubble .el-link {
  color: #81c784 !important;
  text-decoration: underline;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  max-width: 100% !important;
  display: block !important;
}

.chat-bubble .el-link:hover {
  color: #68d391 !important;
}

.input-section {
  padding: 15px 20px 8px 20px;
  background: #1a1a1a;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin: 0;
  box-sizing: border-box;
}

.login-notice {
  color: #f687b3;
  text-align: center;
  font-size: 15px;
  margin-bottom: 10px;
}

.pending-files-area {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-bottom: 10px;
  max-width: 1000px;
  width: 100%;
}

.pending-file-item {
  background: #4a5568;
  border-radius: 6px;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid #718096;
  transition: all 0.25s ease;
  min-width: 120px;
  max-width: 250px;
}

.pending-file-item:hover {
  background: #2d3748;
  border-color: #81c784;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.pending-file-item .el-link {
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  max-width: calc(100% - 30px) !important;
  display: block !important;
  flex: 1 1 auto !important;
}

/* 上传文件删除按钮样式 */
.pending-delete-btn {
  background: transparent !important;
  border: none !important;
  color: #e53e3e !important;
  font-size: 16px !important;
  font-weight: bold !important;
  width: 20px !important;
  height: 20px !important;
  padding: 0 !important;
  margin: 0 !important;
  line-height: 1 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 50% !important;
  transition: all 0.25s ease !important;
  cursor: pointer !important;
}

.pending-delete-btn:hover {
  background: #e53e3e !important;
  color: #ffffff !important;
  transform: scale(1.1) !important;
}

.mode-indicator {
  display: flex;
  align-items: center;
  background: #4a5568;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 15px;
  color: #81c784;
  margin-bottom: 10px;
}

/* 统一的大输入框容器 */
.unified-input-box {
  position: relative;
  width: 100%;
  max-width: 1000px;
  height: 280px;
  background: #4a5568;
  border-radius: 40px;
  padding: 0;
  box-shadow: 0 12px 48px rgba(0,0,0,0.5);
  border: 3px solid #718096;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.unified-input-box:focus-within {
  border-color: #81c784;
  box-shadow: 0 16px 56px rgba(129, 199, 132, 0.4);
}

/* 上部分：文本输入区域 */
.text-input-area {
  flex: 1;
  position: relative;
  padding: 30px 35px 20px 35px;
  background: #4a5568;
}

/* 自定义textarea样式 */
.custom-textarea {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: #e2e8f0;
  font-size: 16px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  resize: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #718096 transparent;
}

.custom-textarea::placeholder {
  color: #a0aec0;
  font-size: 16px;
}

.custom-textarea::-webkit-scrollbar {
  width: 8px;
}

.custom-textarea::-webkit-scrollbar-track {
  background: transparent;
}

.custom-textarea::-webkit-scrollbar-thumb {
  background: #718096;
  border-radius: 10px;
}

.custom-textarea::-webkit-scrollbar-thumb:hover {
  background: #81c784;
}

/* 字数统计 */
.char-count {
  position: absolute;
  bottom: 8px;
  right: 20px;
  color: #a0aec0;
  font-size: 14px;
  pointer-events: none;
}

/* 下部分：按钮区域 */
.button-area {
  height: 70px;
  background: #4a5568;
  padding: 15px 35px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: none;
}

/* 左侧按钮组 */
.left-buttons {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* 右侧按钮组 */
.right-buttons {
  display: flex;
  align-items: center;
}

/* 框内按钮通用样式 */
.box-button {
  border-radius: 22px !important;
  padding: 10px 20px !important;
  font-size: 15px !important;
  background-color: #2d3748 !important;
  border-color: #2d3748 !important;
  color: #e2e8f0 !important;
  box-shadow: 0 3px 12px rgba(0,0,0,0.4) !important;
  transition: all 0.25s ease !important;
  height: 44px !important;
}

.box-button:hover {
  background-color: #1a202c !important;
  border-color: #81c784 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.5) !important;
}

/* 发送按钮样式 */
.send-box-button {
  border-radius: 22px !important;
  padding: 10px 30px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  background-color: #81c784 !important;
  border-color: #81c784 !important;
  color: #1a202c !important;
  box-shadow: 0 4px 16px rgba(129, 199, 132, 0.5) !important;
  transition: all 0.25s ease !important;
  height: 44px !important;
  min-width: 100px !important;
}

.send-box-button:hover {
  background-color: #68d391 !important;
  border-color: #68d391 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(129, 199, 132, 0.7) !important;
}

/* 下拉菜单优化 */
.unified-input-box .el-dropdown-menu {
  z-index: 2000 !important;
}

/* AI 免责声明样式 */
.ai-disclaimer {
  text-align: center;
  color: #a0aec0;
  font-size: 12px;
  margin-top: 2px;
  margin-bottom: 0;
  opacity: 0.8;
  font-weight: 400;
  letter-spacing: 0.5px;
}
/* 旧样式已被新布局替代 */
/* 旧样式已被新布局替代 */

/* 暗色主题Element Plus组件样式覆盖 */
.main-content .el-input__wrapper {
  background-color: #4a5568 !important;
  border-color: #718096 !important;
  box-shadow: 0 0 0 1px #718096 inset !important;
}
.main-content .el-input__inner {
  color: #e2e8f0 !important;
}
.main-content .el-input__inner::placeholder {
  color: #a0aec0 !important;
}

/* 这些旧的textarea样式已被新的统一输入框设计替代 */
.main-content .el-button {
  background-color: #4a5568 !important;
  border-color: #718096 !important;
  color: #e2e8f0 !important;
}
.main-content .el-button:hover {
  background-color: #718096 !important;
  border-color: #81c784 !important;
}
.main-content .el-button--primary {
  background-color: #81c784 !important;
  border-color: #81c784 !important;
  color: #1a202c !important;
}
.main-content .el-button--primary:hover {
  background-color: #68d391 !important;
  border-color: #68d391 !important;
}
.main-content .el-button--danger {
  background-color: #e53e3e !important;
  border-color: #e53e3e !important;
}
.main-content .el-button--danger:hover {
  background-color: #fc8181 !important;
  border-color: #fc8181 !important;
}
.main-content .el-link {
  color: #81c784 !important;
}

/* 额外的全局样式重置 */
.el-scrollbar {
  height: 100% !important;
}

.el-scrollbar__wrap {
  overflow-x: hidden !important;
}

/* 确保所有元素都不会导致页面滚动 */
* {
  box-sizing: border-box !important;
}

html, body, #app {
  margin: 0 !important;
  padding: 0 !important;
  height: 100vh !important;
  width: 100vw !important;
  overflow: hidden !important;
  background: #1a1a1a !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}
.main-content .el-link:hover {
  color: #68d391 !important;
}
.history-panel .el-link {
  color: #e2e8f0 !important;
}
.history-panel .el-link:hover {
  color: #81c784 !important;
}

/* Element Plus 链接组件文本省略 */
.el-link__inner {
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  max-width: 100% !important;
  display: block !important;
}
/* 历史文件栏删除按钮样式 */
.history-panel .el-button--danger.delete-btn {
  background-color: #4a5568 !important;
  border-color: #718096 !important;
  color: #e53e3e !important;
  border-radius: 8px !important;
  width: 28px !important;
  height: 28px !important;
  padding: 0 !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
  transition: all 0.25s ease !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 16px !important;
  font-weight: bold !important;
  line-height: 1 !important;
}

.history-panel .el-button--danger.delete-btn:hover {
  background-color: #e53e3e !important;
  border-color: #e53e3e !important;
  color: #ffffff !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.4) !important;
}
</style> 