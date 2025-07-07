<template>
  <div id="app" class="ai-chat-app">
    <div class="chat-panel">
      <div class="chat-header">
        <span>AI对话助手</span>
        <div>
          <el-button v-if="!isLogin" type="primary" size="small" @click="goLogin">登录</el-button>
          <el-button v-if="isLogin" type="danger" size="small" @click="logout">退出登录</el-button>
        </div>
      </div>
      <div class="chat-messages" ref="msgList">
        <div v-for="(msg, idx) in messages" :key="idx" :class="['chat-msg', msg.role]">
          <span class="msg-role">{{ msg.role === 'user' ? '我' : 'AI' }}：</span>
          <span class="msg-content">{{ msg.content }}</span>
        </div>
      </div>
      <div v-if="!isLogin" class="login-tip">请先登录后使用对话和上传服务</div>
      <div class="chat-input-area">
        <el-upload
          class="upload-btn"
          :show-file-list="false"
          :http-request="uploadFile"
          :disabled="!isLogin"
        >
          <el-button size="small" :disabled="!isLogin">上传文件</el-button>
        </el-upload>
        <el-input
          v-model="inputMsg"
          placeholder="和我聊聊天吧"
          class="chat-input"
          :disabled="!isLogin"
          @keyup.enter.native="sendMsg"
        />
        <el-button type="primary" @click="sendMsg" :disabled="!isLogin">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import axios from 'axios';
export default {
  name: 'Home',
  setup() {
    const router = useRouter();
    const isLogin = ref(localStorage.getItem('isLogin') === '1');
    // 聊天相关
    const messages = ref([
      { role: 'ai', content: '你好，有什么可以帮你？' }
    ]);
    const inputMsg = ref('');
    const msgList = ref(null);
    const uploadedFileIds = ref([]); // 存储已上传文件id
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
    // 发送消息
    const sendMsg = async () => {
      console.log('sendMsg called', isLogin.value, inputMsg.value);
      if (!isLogin.value) return;
      if (!inputMsg.value.trim()) return;
      messages.value.push({ role: 'user', content: inputMsg.value });
      const userMsg = inputMsg.value;
      inputMsg.value = '';
      scrollToBottom();
      try {
        const res = await axios.post('http://localhost:8000/api/llm/chat/', {
          messages: messages.value,
          file_ids: uploadedFileIds.value
        });
        messages.value.push({ role: 'ai', content: res.data.reply });
        scrollToBottom();
      } catch (e) {
        messages.value.push({ role: 'ai', content: '大模型接口异常' });
        scrollToBottom();
      }
    };
    // 滚动到底部
    const scrollToBottom = () => {
      nextTick(() => {
        if (msgList.value) {
          msgList.value.scrollTop = msgList.value.scrollHeight;
        }
      });
    };
    // 文件上传
    const uploadFile = async (option) => {
      if (!isLogin.value) return;
      const formData = new FormData();
      formData.append('file', option.file);
      try {
        const res = await axios.post('http://localhost:8000/api/llm/upload/', formData);
        uploadedFileIds.value.push(res.data.file_id);
        ElMessage.success('文件上传成功: ' + option.file.name);
        option.onSuccess && option.onSuccess({ file_id: res.data.file_id }, option.file);
      } catch (e) {
        ElMessage.error('文件上传失败');
        option.onError && option.onError(e, option.file);
      }
    };
    // 监听登录状态变化（如登录页登录后返回首页）
    window.addEventListener('storage', () => {
      isLogin.value = localStorage.getItem('isLogin') === '1';
    });
    return {
      isLogin,
      goLogin,
      logout,
      messages,
      inputMsg,
      sendMsg,
      msgList,
      uploadFile
    };
  }
};
</script>

<style scoped>
.ai-chat-app {
  min-height: 100vh;
  background: #f6f8fa;
  display: flex;
  align-items: center;
  justify-content: center;
}
.chat-panel {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(53,120,229,0.08);
  max-width: 700px;
  width: 96vw;
  min-width: 320px;
  min-height: 600px;
  margin: 60px auto;
  display: flex;
  flex-direction: column;
  padding: 0 0 20px 0;
  box-sizing: border-box;
}
@media (max-width: 600px) {
  .chat-panel {
    padding: 0 2px 8px 2px;
    margin: 12px auto;
    min-width: unset;
    min-height: 70vh;
  }
  .chat-header, .chat-messages, .chat-input-area {
    padding-left: 8px;
    padding-right: 8px;
  }
}
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px 12px 32px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 22px;
  color: #3578e5;
  font-weight: 600;
}
.chat-messages {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: 20px 32px 0 32px;
  background: #f8fafc;
  font-size: 18px;
}
.chat-msg {
  margin-bottom: 14px;
  display: flex;
  align-items: flex-start;
}
.chat-msg.user .msg-role {
  color: #3578e5;
  font-weight: bold;
}
.chat-msg.ai .msg-role {
  color: #e67e22;
  font-weight: bold;
}
.msg-content {
  margin-left: 6px;
  word-break: break-all;
}
.chat-input-area {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 32px 0 32px;
}
.chat-input {
  flex: 1 1 auto;
}
.upload-btn {
  margin-right: 8px;
}
.login-tip {
  color: #e67e22;
  text-align: center;
  margin: 8px 0 0 0;
  font-size: 15px;
}
</style> 