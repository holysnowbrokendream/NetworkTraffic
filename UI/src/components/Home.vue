<template>
  <div class="chat-app-root">
    <!-- 侧边栏：只保留icon按钮 -->
    <aside class="sidebar sidebar-icons">
      <button class="sidebar-icon-btn" @click="drawerVisible = true" title="历史会话">🕑</button>
      <button class="sidebar-icon-btn" @click="toggleTheme" :title="isDarkMode ? '切换到亮色模式' : '切换到暗色模式'">
        <span v-if="isDarkMode">🌙</span>
        <span v-else>☀️</span>
      </button>
      <button v-if="!isLogin" class="sidebar-icon-btn" @click="goLogin" title="登录">👤</button>
      <button v-else class="sidebar-icon-btn" @click="logout" title="退出登录">⎋</button>
    </aside>
    <!-- 历史会话抽屉 -->
    <el-drawer v-model="drawerVisible" direction="ltr" size="260px" :with-header="false" class="history-drawer">
      <div class="sidebar-history">
        <div class="sidebar-header">
          <span class="sidebar-title">历史会话</span>
          <el-button size="small" class="new-session-btn" @click="handleNewSession">+ 新建对话</el-button>
        </div>
        <div class="session-list">
          <div v-for="session in sessions" :key="session.id" :class="['session-item', {active: session.id===currentSessionId}]" @click="selectSession(session.id); drawerVisible=false">
            <div class="session-title">{{ session.title || '未命名会话' }}</div>
            <div class="session-time">{{ formatDate(session.updated_at) }}</div>
          </div>
        </div>
      </div>
    </el-drawer>
    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 欢迎页 -->
      <section v-if="!sessions.length" class="welcome-wrapper welcome-full">
        <div class="welcome-logo-title">
          <div class="welcome-logo">
            <svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#409eff"/><text x="50%" y="54%" text-anchor="middle" fill="#fff" font-size="32" font-family="Arial" dy=".3em">D</text></svg>
          </div>
          <div class="welcome-title">网络流量研判大模型对话助手</div>
          <div class="welcome-subtitle">我可以帮你分析流量、提取规则、生成pcap文件，请输入你的问题或需求~</div>
        </div>
        <div class="welcome-input-box">
          <input v-model="welcomeInput" :maxlength="2000" @keydown.enter="handleWelcomeSend" placeholder="请输入你的问题..." />
          <button class="welcome-send-btn" :disabled="!welcomeInput.trim()" @click="handleWelcomeSend">发送</button>
        </div>
      </section>
      <!-- 聊天界面 -->
      <template v-else>
        <header class="main-header">
          <h1>网络流量研判大模型对话助手</h1>
        </header>
        <div class="chat-container">
          <section class="chat-section" ref="chatSection">
            <div class="chat-messages" ref="chatMessages">
              <div v-for="(msg, idx) in messages" :key="msg.id || idx" :class="['msg-row', msg.role]">
                <template v-if="msg.role==='ai'">
                  <div class="msg-bubble ai-bubble">
                  <span class="avatar">AI</span>
                  <div class="bubble-content">
                    <div class="bubble-text" v-html="msg.content"></div>
                    <div v-if="msg.file" class="file-attachment">
                      <span class="file-icon">📄</span>
                      <div class="file-info">
                        <span class="file-name">{{ msg.file.filename }}</span>
                        <el-button type="primary" size="small" class="download-btn" @click="downloadFile(msg.file.url, msg.file.filename)">
                          下载文件
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
                </template>
                <template v-else>
                  <div class="msg-bubble user-bubble">
                  <div class="bubble-content">
                    <div v-if="msg.content" class="bubble-text">{{ msg.content }}</div>
                    <div v-if="msg.file" class="file-attachment">
                      <span class="file-icon">📄</span>
                      <div class="file-info">
                        <span class="file-name">{{ msg.file.filename }}</span>
                        <el-button type="primary" size="small" class="download-btn" @click="downloadFile(msg.file.url, msg.file.filename)">
                          下载文件
                        </el-button>
                      </div>
                    </div>
                  </div>
                    <span class="avatar">🧑‍💻</span>
                </div>
                </template>
              </div>
            </div>
          </section>
          <section class="input-section">
            <div v-if="!isLogin" class="login-notice">请先登录后使用对话和推理服务</div>
            <div class="input-box">
              <div class="input-left">
                <textarea 
                  v-model="inputMsg" 
                  :disabled="!isLogin" 
                  :maxlength="2000" 
                  @keydown="handleKeyDown" 
                  placeholder="和我聊聊天吧 (Enter发送，Shift+Enter换行)" 
                />
                <div class="input-tools">
                  <label v-if="selectedType==='bert'||selectedType==='rule'" class="file-upload-btn">
                    <input type="file" @change="handleFileChange" accept=".pcap" />
                    <span>{{ file ? file.name : '选择文件' }}</span>
                  </label>
                  <el-select v-model="selectedType" placeholder="请选择功能" class="type-select custom-select">
                    <el-option label="研判（BERT）" value="bert"></el-option>
                    <el-option label="规则提取" value="rule"></el-option>
                    <el-option label="生成pcap" value="gen"></el-option>
                  </el-select>
                </div>
              </div>
              <div class="input-right">
                <el-button type="primary" class="send-btn" :disabled="!isLogin || !currentSessionId" @click="handleSubmit">发送</el-button>
                <div class="char-count">{{ inputMsg.length }}/2000</div>
              </div>
            </div>
            <div class="ai-disclaimer">内容由 AI 生成，请仔细甄别</div>
          </section>
        </div>
      </template>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import axios from 'axios';

export default {
  name: 'Home',
  setup() {
    const router = useRouter();
    const isLogin = ref(localStorage.getItem('isLogin') === '1');
    const isDarkMode = ref(localStorage.getItem('theme') === 'dark');
    const selectedType = ref('bert');
    const inputMsg = ref('');
    const file = ref(null);
    const sessions = ref([]); // 历史会话列表
    const currentSessionId = ref(null);
    const messages = ref([]); // 当前会话消息
    const drawerVisible = ref(false);
    const welcomeInput = ref('');
    const chatMessages = ref(null);
    const chatSection = ref(null);

    // 滚动到底部
    const scrollToBottom = async () => {
      await nextTick();
      if (chatMessages.value) {
        chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
      }
    };

    // 监听消息变化，自动滚动
    watch(() => messages.value, () => {
      scrollToBottom();
    }, { deep: true });

    // 监听会话切换，自动滚动
    watch(currentSessionId, () => {
      scrollToBottom();
    });

    // 获取历史会话列表
    const fetchSessions = async () => {
      try {
        const res = await axios.get('/api/modeltask/sessions/', { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        sessions.value = res.data;
        if (!currentSessionId.value && sessions.value.length > 0) {
          selectSession(sessions.value[0].id);
        }
        } catch (e) {
        sessions.value = [];
      }
    };
    // 获取会话详情
    const fetchSessionDetail = async (sessionId) => {
      try {
        const res = await axios.get(`/api/modeltask/sessions/${sessionId}/`, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        messages.value = res.data.messages || [];
      } catch (e) {
        messages.value = [];
      }
    };
    // 选择会话
    const selectSession = (sessionId) => {
      currentSessionId.value = sessionId;
      fetchSessionDetail(sessionId);
    };
    // 新建会话（仅主动点击新建时调用）
    const handleNewSession = async () => {
      try {
        const res = await axios.post('/api/modeltask/sessions/', { title: '' }, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        await fetchSessions();
        selectSession(res.data.id);
      } catch (e) {
        ElMessage.error('新建会话失败');
      }
    };
    // 欢迎页发送
    const handleWelcomeSend = async () => {
      if (!welcomeInput.value.trim()) return;
      if (!isLogin.value) {
        ElMessage.warning('请先登录');
        return;
      }
      try {
        // 1. 新建会话，title取首条消息前20字
        const title = welcomeInput.value.slice(0, 20);
        const sessionRes = await axios.post('/api/modeltask/sessions/', { title }, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        const sessionId = sessionRes.data.id;
        
        try {
          // 2. 保存首条消息
          const userMsg = { role: 'user', content: welcomeInput.value };
          await axios.post(`/api/modeltask/sessions/${sessionId}/messages/`, userMsg, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
          
          // 3. 成功后再刷新会话列表和详情
          await fetchSessions();
          selectSession(sessionId);
          welcomeInput.value = '';
        } catch (msgError) {
          // 如果保存消息失败，删除刚创建的空会话
          await axios.delete(`/api/modeltask/sessions/${sessionId}/`, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
          throw msgError;
        }
      } catch (e) {
        console.error('新建会话失败', e?.response?.data || e.message || e);
        ElMessage.error('新建会话失败: ' + (e?.response?.data?.detail || e.message || '未知错误'));
      }
    };
    // 发送消息（仅复用当前会话）
    const handleSubmit = async () => {
      if (!isLogin.value) {
        ElMessage.warning('请先登录');
        return;
      }
      if (!inputMsg.value.trim() && !(selectedType.value === 'gen' ? inputMsg.value.trim() : file.value)) {
        ElMessage.warning('请输入内容或上传文件');
          return;
        }
      if (!currentSessionId.value) {
        ElMessage.error('请先新建会话');
        return;
      }
      const userMsgContent = inputMsg.value;
      // 1. 先保存文本消息
      if (userMsgContent.trim()) {
        await axios.post(`/api/modeltask/sessions/${currentSessionId.value}/messages/`, { role: 'user', content: userMsgContent }, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
      }

      if (file.value && (selectedType.value === 'bert' || selectedType.value === 'rule')) {
        // 2. 为上传的文件本身创建一条持久化消息
        const fileFormData = new FormData();
        fileFormData.append('role', 'user');
        fileFormData.append('file', file.value);
        fileFormData.append('filename', file.value.name);
        await axios.post(`/api/modeltask/sessions/${currentSessionId.value}/messages/`, fileFormData, {
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token'), 'Content-Type': 'multipart/form-data' }
        });

        // 3. 调用模型分析，并根据结果创建AI消息
        const analyzeFormData = new FormData();
        analyzeFormData.append('file', file.value);
        analyzeFormData.append('type', selectedType.value);

        let aiContent = '';
        try {
            const res = await axios.post('/api/modeltask/analyze/', analyzeFormData, {
                headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
            });
            aiContent = JSON.stringify(res.data);
        } catch (e) {
            aiContent = '模型服务未连接，无法进行分析。';
            ElMessage.error('模型分析失败，请检查服务是否可用。');
        }

        // 4. 持久化AI的回复或错误提示
        await axios.post(`/api/modeltask/sessions/${currentSessionId.value}/messages/`, {
            role: 'ai',
            content: aiContent
        }, {
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
        });

      } else if (selectedType.value === 'gen') {
        const res = await axios.post('/api/modeltask/analyze/', { type: 'gen', text: userMsgContent }, {
          headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') },
          responseType: 'blob'
        });
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const aiMsg = { role: 'ai', content: '', file: { url: url, filename: 'result.pcap' } };
        await axios.post(`/api/modeltask/sessions/${currentSessionId.value}/messages/`, { role: 'ai', content: `[Generated file: result.pcap]` }, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        messages.value.push(aiMsg);
      }

      // 5. 所有操作完成后，清空输入框并从后端刷新UI
      inputMsg.value = '';
      file.value = null;
      await fetchSessions();
      await fetchSessionDetail(currentSessionId.value);
    };
    const handleFileChange = (e) => {
      file.value = e.target.files[0];
    };
    const handleKeyDown = (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
          event.preventDefault();
        handleSubmit();
      }
    };
    const toggleTheme = () => {
      isDarkMode.value = !isDarkMode.value;
      const theme = isDarkMode.value ? 'dark' : 'light';
      localStorage.setItem('theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
    };
    const goLogin = () => {
      router.push('/login');
    };
    const logout = () => {
      localStorage.removeItem('isLogin');
      localStorage.removeItem('token');
      isLogin.value = false;
      ElMessage.success('已退出登录');
    };
    const formatDate = (dt) => {
      if (!dt) return '';
      const d = new Date(dt);
      return d.toLocaleDateString() + ' ' + d.toLocaleTimeString().slice(0,5);
    };
    const downloadFile = (url, filename) => {
      // 如果是Blob URL（本地临时文件）
      if (url.startsWith('blob:')) {
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        // 如果是服务器文件，先获取文件内容再下载
        axios.get(url, {
          responseType: 'blob',
          headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
        }).then(response => {
          const blob = new Blob([response.data]);
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = downloadUrl;
          link.download = filename;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(downloadUrl);
        }).catch(error => {
          ElMessage.error('下载文件失败');
          console.error('Download error:', error);
        });
      }
    };
    // 监听登录状态变化，重新登录后进入欢迎页
    watch(isLogin, (val) => {
      if (val) {
        // 清空历史会话和当前会话，进入欢迎页
        sessions.value = [];
        currentSessionId.value = null;
        messages.value = [];
      }
    });
    // 页面初次加载时如果未登录也进入欢迎页
    onMounted(() => {
      if (isLogin.value) fetchSessions();
      else {
        sessions.value = [];
        currentSessionId.value = null;
        messages.value = [];
      }
    });
    return {
      isLogin,
      isDarkMode,
      selectedType,
      inputMsg,
      file,
      sessions,
      currentSessionId,
      messages,
      fetchSessions,
      selectSession,
      handleNewSession,
      handleSubmit,
      handleFileChange,
      handleKeyDown,
      toggleTheme,
      goLogin,
      logout,
      formatDate,
      drawerVisible,
      welcomeInput,
      handleWelcomeSend,
      downloadFile,
      chatMessages,
      chatSection
    };
  }
};
</script>

<style scoped>
.chat-app-root {
  display: flex;
  width: 100%;
  height: 100vh;
  background: var(--bg-primary, #f7f8fa);
}

.sidebar {
  width: 64px;
  flex-shrink: 0;
  background: #eaf0fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 0;
  gap: 18px;
  box-shadow: 2px 0 12px #e0e6ed;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止内容溢出 */
}

.main-header {
  flex-shrink: 0;
  padding: 20px 0;
  text-align: center;
  background: var(--bg-primary, #f7f8fa);
  z-index: 2;
}

.main-header h1 {
  font-size: 2rem;
  color: #409eff;
  font-weight: 700;
  margin: 0;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.chat-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0 20px;
  position: relative;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
  margin-right: -8px; /* 为滚动条预留空间 */
  padding-right: 8px;
}

.input-section {
  flex-shrink: 0;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px 16px;
  position: relative;
  z-index: 1;
}

.input-box {
  width: 100%;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  padding: 12px 16px;
  transition: box-shadow 0.3s ease;
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.input-box:focus-within {
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.12);
}

.input-left {
  flex: 1;
  min-width: 0; /* 防止flex子元素溢出 */
}

.input-right {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-end;
}

.input-box textarea {
  width: 100%;
  min-height: 44px;
  max-height: 120px;
  border: none;
  outline: none;
  font-size: 15px;
  line-height: 1.5;
  color: #333;
  background: transparent;
  resize: none;
  padding: 0;
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
}

.input-box textarea::placeholder {
  color: #999;
}

.input-tools {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.file-upload-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 32px;
  min-width: 100px;
  padding: 0 12px;
  background: #f3f6fa;
  border-radius: 16px;
  border: 1px solid #e0e6ed;
  color: #409eff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-upload-btn:hover {
  background: #eaf4ff;
  border-color: #409eff;
}

.file-upload-btn input[type="file"] {
  display: none;
}

.file-upload-btn span {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.type-select {
  min-width: 100px !important; /* 减小最小宽度 */
  max-width: 120px !important; /* 限制最大宽度 */
}

.custom-select :deep(.el-input__wrapper) {
  border-radius: 16px !important;
  height: 32px !important;
  background: #f3f6fa !important;
  border: 1px solid #e0e6ed !important;
  box-shadow: none !important;
}

.custom-select :deep(.el-input__wrapper):hover {
  border-color: #409eff !important;
  background: #eaf4ff !important;
}

.custom-select :deep(.el-input__wrapper.is-focus) {
  border-color: #409eff !important;
  background: #fff !important;
  box-shadow: 0 0 0 1px #409eff !important;
}

.custom-select :deep(.el-input__inner) {
  font-size: 12px !important; /* 减小字号 */
  color: #333 !important;
  font-weight: 500 !important;
  height: 32px !important;
  line-height: 32px !important;
  padding: 0 8px !important; /* 减小内边距 */
}

.custom-select :deep(.el-select__caret) {
  font-size: 12px !important; /* 减小下拉箭头大小 */
}

.send-btn {
  height: 32px !important;
  border-radius: 16px !important;
  padding: 0 20px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  margin-left: auto !important; /* 推到最右边 */
}

.send-btn:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3) !important;
}

.send-btn:disabled {
  background: #e0e6ed !important;
  border-color: #e0e6ed !important;
  color: #999 !important;
  cursor: not-allowed !important;
}

.char-count {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.ai-disclaimer {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 4px;
}

/* 深色模式适配 */
[data-theme='dark'] .input-box {
  background: #2d323c;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

[data-theme='dark'] .input-box:focus-within {
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.15);
}

[data-theme='dark'] .input-box textarea {
  color: #fff;
}

[data-theme='dark'] .input-box textarea::placeholder {
  color: #666;
}

[data-theme='dark'] .file-upload-btn,
[data-theme='dark'] .custom-select :deep(.el-input__wrapper) {
  background: #1e2227 !important;
  border-color: #3e4451 !important;
}

[data-theme='dark'] .file-upload-btn:hover,
[data-theme='dark'] .custom-select :deep(.el-input__wrapper):hover {
  background: #2d323c !important;
  border-color: #409eff !important;
}

[data-theme='dark'] .custom-select :deep(.el-input__wrapper.is-focus) {
  background: #2d323c !important;
}

[data-theme='dark'] .custom-select :deep(.el-input__inner) {
  color: #fff !important;
}

[data-theme='dark'] .send-btn:disabled {
  background: #1e2227 !important;
  border-color: #3e4451 !important;
}

/* 消息气泡样式 */
.msg-row {
  display: flex;
  align-items: flex-end;
  margin-bottom: 16px;
}
.msg-row.user {
  flex-direction: row-reverse;
}
.msg-bubble {
  max-width: 60%;
  padding: 12px 18px;
  border-radius: 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  font-size: 16px;
  word-break: break-all;
  display: flex;
  align-items: flex-end;
}
.user-bubble {
  background: #4f8cff;
  color: #fff;
  border-bottom-right-radius: 4px;
  margin-left: 12px;
  margin-right: 0;
  display: flex;
  flex-direction: row;
  align-items: flex-end;
}
.user-bubble .bubble-content {
  flex: 1;
}
.user-bubble .avatar {
  margin-left: 8px;
  margin-right: 0;
}
.ai-bubble {
  background: #f1f1f1;
  color: #222;
  border-bottom-left-radius: 4px;
  margin-right: 12px;
  margin-left: 0;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  margin: 0 8px;
}
.msg-row.user .avatar {
  margin-left: 8px;
  margin-right: 0;
}
.msg-row.ai .avatar {
  margin-right: 8px;
  margin-left: 0;
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.2);
}

/* 深色模式滚动条 */
[data-theme='dark'] .chat-messages::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.1);
}

[data-theme='dark'] .chat-messages::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

/* 欢迎页样式 */
.welcome-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.welcome-full {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-primary, #f7f8fa);
  z-index: 1;
}

/* 输入框样式 */
.input-box {
  width: 100%;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 2px 12px #e0e6ed;
  padding: 18px 24px 12px;
}

/* 其他已有的样式保持不变... */
.sidebar-history {
  flex: 1;
  padding: 24px 0 0 0;
  overflow-y: auto;
}
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18px 12px 18px;
}
.sidebar-title {
  font-size: 18px;
  font-weight: 600;
  color: #409eff;
}
.new-session-btn {
  border-radius: 16px !important;
  font-size: 14px !important;
  padding: 4px 16px !important;
  background: #fff !important;
  color: #409eff !important;
  border: 1.5px solid #e0e6ed !important;
  box-shadow: 0 2px 8px #e0e6ed !important;
  transition: background 0.2s, color 0.2s;
}
.new-session-btn:hover {
  background: #409eff !important;
  color: #fff !important;
}
.session-list {
  padding: 0 8px 0 8px;
}
.session-item {
  border-radius: 12px;
  padding: 10px 14px 8px 14px;
  margin-bottom: 8px;
  background: #fff;
  cursor: pointer;
  box-shadow: 0 2px 8px #e0e6ed;
  transition: background 0.2s, box-shadow 0.2s;
}
.session-item.active, .session-item:hover {
  background: #409eff;
  color: #fff;
  box-shadow: 0 4px 16px #b3e5fc;
}
.session-title {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.session-time {
  font-size: 12px;
  color: #888;
}
.sidebar-bottom {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: center;
  padding: 24px 0;
}
.bubble-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.file-attachment {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.6);
  padding: 8px 12px;
  border-radius: 12px;
  border: 1px solid #e0e6ed;
}
.user-bubble .file-attachment {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}
.file-icon {
  font-size: 20px;
}
.file-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}
.file-name {
  font-size: 14px;
  font-weight: 500;
  word-break: break-all;
}
.download-btn {
  align-self: flex-start;
  border-radius: 12px !important;
  padding: 6px 16px !important;
}
.user-bubble .download-btn {
  background: rgba(255, 255, 255, 0.2) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
}
.user-bubble .download-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
}
.user-bubble .file-name {
  color: #fff;
}
.ai-bubble .file-link {
  color: #409eff;
  text-decoration: none;
}
.ai-bubble .file-link:hover {
  text-decoration: underline;
}
.upload-progress {
  margin-top: 4px;
}
.upload-progress :deep(.el-progress-bar__inner) {
  background-color: #fff !important;
}
.upload-progress :deep(.el-progress-bar__outer) {
  background-color: rgba(0, 0, 0, 0.2) !important;
}
.user-bubble {
  background: #409eff;
  color: #fff;
  margin-right: 12px;
}
.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #eaf0fa;
  color: #409eff;
  font-weight: bold;
  font-size: 15px;
  margin-right: 10px;
  margin-left: 0;
}
.user-bubble .avatar {
  background: #fff;
  color: #409eff;
  margin-right: 0;
  margin-left: 10px;
}
.bubble-text a {
  color: #409eff;
  text-decoration: underline;
}
.input-tools {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}
.type-select {
  min-width: 140px;
}
.send-btn {
  border-radius: 18px !important;
  padding: 8px 28px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
}
.char-count {
  text-align: right;
  color: #aaa;
  font-size: 13px;
  margin-top: 2px;
}
.login-notice {
  color: #e67e22;
  font-size: 15px;
  margin-bottom: 8px;
  text-align: center;
}
.ai-disclaimer {
  color: #888;
  font-size: 13px;
  text-align: center;
  margin-top: 2px;
}
/* 美化文件选择按钮 */
.file-upload-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  min-width: 120px;
  padding: 0 18px;
  background: #f3f6fa;
  border-radius: 18px;
  border: 1.5px solid #e0e6ed;
  color: #409eff;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  margin-right: 10px;
  box-shadow: 0 2px 8px #e0e6ed;
  transition: background 0.2s, border 0.2s;
  position: relative;
}
.file-upload-btn:hover {
  background: #eaf4ff;
  border-color: #409eff;
}
.file-upload-btn input[type="file"] {
  display: none;
}
/* 美化下拉框 */
.custom-select .el-input__wrapper {
  border-radius: 18px !important;
  height: 44px !important;
  min-height: 44px !important;
  box-shadow: 0 2px 8px #e0e6ed !important;
  background: #f3f6fa !important;
  border: none !important;
  font-size: 15px !important;
  padding: 0 18px !important;
  display: flex;
  align-items: center;
}
.custom-select .el-input__inner {
  font-size: 15px !important;
  color: #409eff !important;
  height: 44px !important;
  line-height: 44px !important;
  padding: 0 !important;
}
.custom-select .el-input__suffix {
  right: 12px !important;
}
.custom-select .el-input__wrapper.is-focus {
  box-shadow: 0 4px 12px #b3e5fc !important;
  border: 2px solid #409eff !important;
  background: #fff !important;
}
:root[data-theme='dark'] {
  --bg-primary: #23272f;
}
[data-theme='dark'] .main-content,
[data-theme='dark'] .chat-app-root {
  background: #23272f !important;
}
[data-theme='dark'] .sidebar {
  background: #23272f !important;
  box-shadow: 2px 0 12px #181a1f;
}
[data-theme='dark'] .main-header h1 {
  color: #90c4ff;
}
[data-theme='dark'] .msg-bubble {
  background: #23272f;
  color: #fff;
  box-shadow: 0 2px 8px #181a1f;
}
[data-theme='dark'] .ai-bubble {
  background: #2d323c;
  color: #90c4ff;
}
[data-theme='dark'] .user-bubble {
  background: #409eff;
  color: #fff;
}
[data-theme='dark'] .input-box {
  background: #2d323c;
  color: #fff;
  box-shadow: 0 2px 12px #181a1f;
}
[data-theme='dark'] .input-box textarea {
  color: #fff;
}
[data-theme='dark'] .char-count {
  color: #aaa;
}
.sidebar.sidebar-icons {
  width: 64px;
  background: #eaf0fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 24px 0;
  box-shadow: 2px 0 12px #e0e6ed;
  gap: 18px;
}
.sidebar-icon-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: none;
  background: #fff;
  color: #409eff;
  font-size: 22px;
  box-shadow: 0 2px 8px #e0e6ed;
  cursor: pointer;
  margin-bottom: 12px;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sidebar-icon-btn:hover {
  background: #409eff;
  color: #fff;
}
.history-drawer {
  z-index: 2000;
}
</style> 