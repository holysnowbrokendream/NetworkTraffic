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
      <header v-if="sessions.length" class="main-header">
        <h1>网络流量研判大模型对话助手</h1>
      </header>
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
                      <template v-else>
        <section class="chat-section">
          <div class="chat-messages">
            <div v-for="(msg, idx) in messages" :key="msg.id || idx" :class="['msg-row', msg.role]">
              <div v-if="msg.role==='ai'" class="msg-bubble ai-bubble">
                <span class="avatar">AI</span>
                <span class="bubble-text" v-html="msg.content"></span>
                    </div>
              <div v-else class="msg-bubble user-bubble">
                <span class="avatar">🧑‍💻</span>
                <span class="bubble-text">{{ msg.content }}</span>
                  </div>
                    </div>
                    </div>
        </section>
        <section class="input-section">
          <div v-if="!isLogin" class="login-notice">请先登录后使用对话和推理服务</div>
          <div class="input-box">
            <textarea v-model="inputMsg" :disabled="!isLogin" :maxlength="2000" @keydown="handleKeyDown" placeholder="和我聊聊天吧 (Enter发送，Shift+Enter换行)" />
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
              <el-button type="primary" class="send-btn" :disabled="!isLogin || !currentSessionId" @click="handleSubmit">发送</el-button>
                </div>
            <div class="char-count">{{ inputMsg.length }}/2000</div>
          </div>
          <div class="ai-disclaimer">内容由 AI 生成，请仔细甄别</div>
        </section>
      </template>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
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
        // 新建会话，title取首条消息前20字
        const title = welcomeInput.value.slice(0, 20);
        const res = await axios.post('/api/modeltask/sessions/', { title }, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        const sessionId = res.data.id;
        // 保存首条消息
        const userMsg = { role: 'user', content: welcomeInput.value };
        await axios.post(`/api/modeltask/sessions/${sessionId}/messages/`, userMsg, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        await fetchSessions();
        selectSession(sessionId);
        welcomeInput.value = '';
        await fetchSessionDetail(sessionId);
      } catch (e) {
        console.error('新建会话失败', e?.response?.data || e.message || e);
        ElMessage.error('新建会话失败: ' + (e?.response?.data?.detail || e.message || ''));
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
      // 追加用户消息
      const userMsg = { role: 'user', content: inputMsg.value };
      try {
        await axios.post(`/api/modeltask/sessions/${currentSessionId.value}/messages/`, userMsg, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        // 如果当前会话title为空，自动用首条消息前20字更新title
        const session = sessions.value.find(s => s.id === currentSessionId.value);
        if (session && (!session.title || session.title === '')) {
          const newTitle = inputMsg.value.slice(0, 20);
          await axios.patch(`/api/modeltask/sessions/${currentSessionId.value}/`, { title: newTitle }, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        }
        let res;
        if (selectedType.value === 'bert' || selectedType.value === 'rule') {
          const formData = new FormData();
          formData.append('file', file.value);
          formData.append('type', selectedType.value);
          res = await axios.post('/api/modeltask/analyze/', formData, {
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token'), 'Content-Type': 'multipart/form-data' }
          });
          const aiMsg = { role: 'ai', content: JSON.stringify(res.data) };
          await axios.post(`/api/modeltask/sessions/${currentSessionId.value}/messages/`, aiMsg, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        } else if (selectedType.value === 'gen') {
          res = await axios.post('/api/modeltask/analyze/', { type: 'gen', text: inputMsg.value }, {
            headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') },
            responseType: 'blob'
          });
          const url = window.URL.createObjectURL(new Blob([res.data]));
          const aiMsg = { role: 'ai', content: `生成的pcap文件：<a href=\"${url}\" download=\"result.pcap\">点击下载</a>` };
          await axios.post(`/api/modeltask/sessions/${currentSessionId.value}/messages/`, aiMsg, { headers: { Authorization: 'Bearer ' + localStorage.getItem('token') } });
        }
      } catch (e) {
        ElMessage.error('推理失败');
      }
      inputMsg.value = '';
      file.value = null;
      fetchSessions();
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
      handleWelcomeSend
    };
  }
};
</script>

<style scoped>
.welcome-wrapper {
  height: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f7f8fa;
  box-sizing: border-box;
}
.welcome-full {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f7f8fa;
  z-index: 1;
}
.welcome-logo-title {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 48px;
  max-width: 600px;
}
.welcome-logo {
  margin-bottom: 18px;
}
.welcome-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #409eff;
  margin-bottom: 10px;
  text-align: center;
}
.welcome-subtitle {
  font-size: 1.1rem;
  color: #888;
  margin-bottom: 0;
  text-align: center;
}
.welcome-input-box {
  display: flex;
  align-items: center;
  background: #f3f6fa;
  border-radius: 32px;
  box-shadow: 0 2px 12px #e0e6ed;
  padding: 18px 32px;
  min-width: 320px;
  max-width: 90vw;
  width: 100%;
}
.welcome-input-box input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 1.1rem;
  color: #222;
  padding: 0 8px;
}
.welcome-send-btn {
  margin-left: 18px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 18px;
  font-size: 1rem;
  font-weight: 600;
  padding: 8px 28px;
  cursor: pointer;
  box-shadow: 0 2px 8px #e0e6ed;
  transition: background 0.2s;
}
.welcome-send-btn:disabled {
  background: #d0d7de;
  color: #aaa;
  cursor: not-allowed;
}
.chat-app-root {
  display: flex;
  min-height: 100vh;
  background: var(--bg-primary, #f7f8fa);
}
.sidebar {
  width: 260px;
  background: #eaf0fa;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: stretch;
  padding: 0;
  box-shadow: 2px 0 12px #e0e6ed;
}
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
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 0 0 0;
  min-height: 100vh;
  background: var(--bg-primary, #f7f8fa);
}
.main-header {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 0 12px 0;
  text-align: center;
}
.main-header h1 {
  font-size: 2rem;
  color: #409eff;
  font-weight: 700;
  margin: 0;
  letter-spacing: 1px;
}
.chat-section {
  width: 100%;
  max-width: 900px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto;
  padding-bottom: 16px;
}
.chat-messages {
  width: 100%;
  flex: 1;
  overflow-y: auto;
  padding: 0 0 24px 0;
  min-height: 320px;
}
.msg-row {
  display: flex;
  margin-bottom: 18px;
}
.msg-row.ai {
  justify-content: flex-start;
}
.msg-row.user {
  justify-content: flex-end;
}
.msg-bubble {
  display: flex;
  align-items: flex-end;
  max-width: 70%;
  border-radius: 18px;
  box-shadow: 0 2px 8px #e0e6ed;
  padding: 12px 18px;
  font-size: 16px;
  line-height: 1.6;
  background: #fff;
  color: #222;
  position: relative;
}
.ai-bubble {
  background: #f3f6fa;
  color: #409eff;
  margin-left: 12px;
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
.input-section {
  width: 100%;
  max-width: 900px;
  margin: 0 auto 24px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.input-box {
  width: 100%;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 2px 12px #e0e6ed;
  padding: 18px 24px 12px 24px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin-bottom: 8px;
}
.input-box textarea {
  width: 100%;
  min-height: 60px;
  border: none;
  outline: none;
  font-size: 16px;
  color: #222;
  background: transparent;
  resize: none;
  margin-bottom: 8px;
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