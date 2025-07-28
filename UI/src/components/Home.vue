<template>
  <div id="app" class="ai-chat-app app-root">
    <!-- 侧边栏 - 始终显示 -->
    <div class="sidebar-container" :class="{ 'sidebar-expanded': sidePanelExpanded || sessionPanelExpanded }">
      <div class="blue-bar">
        <!-- 顶部展开按钮（历史文件按钮） -->
        <div class="top-section">
          <!-- 历史文件按钮 -->
          <button 
            class="expand-btn" 
            :class="{ active: sidePanelExpanded }"
            @click="() => { sidePanelExpanded = !sidePanelExpanded; if(sidePanelExpanded) { sessionPanelExpanded = false; } }"
            :title="!sidePanelExpanded ? '展开历史文件' : '收起历史文件'"
          >
            <el-icon>
              <el-icon-arrow-right v-if="!sidePanelExpanded" />
              <el-icon-arrow-left v-if="sidePanelExpanded" />
            </el-icon>
          </button>
          <!-- 历史会话按钮 -->
          <button
            class="expand-btn"
            :class="{ active: sessionPanelExpanded }"
            @click="() => { sessionPanelExpanded = !sessionPanelExpanded; if(sessionPanelExpanded) { sidePanelExpanded = false; fetchUserSessions(); } }"
            :title="!sessionPanelExpanded ? '展开历史会话' : '收起历史会话'"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M12 3C7.03 3 3 7.03 3 12s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 16c-3.86 0-7-3.14-7-7s3.14-7 7-7 7 3.14 7 7-3.14 7-7 7zm-1-13h2v6l5.25 3.15-1 1.7L11 13V6z"/>
            </svg>
          </button>
        </div>
        
        <!-- 底部按钮组 -->
        <div class="bottom-section">
          <!-- 主题切换按钮 -->
          <button 
            class="theme-toggle-btn" 
            @click="toggleTheme"
            :title="isDarkMode ? '切换到亮色模式' : '切换到暗色模式'"
          >
            <svg v-if="isDarkMode" viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <!-- 太阳图标 -->
              <path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <!-- 月亮图标 -->
              <path d="M12.43 2.3c-2.38-.59-4.68-.27-6.63.64-.35.16-.41.64-.1.86C8.3 5.6 10 8.6 10 12c0 3.4-1.7 6.4-4.3 8.2-.31.22-.25.7.1.86 1.95.91 4.25 1.23 6.63.64 4.54-1.13 7.73-5.19 7.73-9.85 0-4.66-3.19-8.72-7.73-9.85zM12 18.5c-1.61 0-3.09-.59-4.23-1.57.27-.68.43-1.43.43-2.21 0-1.06-.25-2.07-.69-2.96-.44-.89-1.08-1.69-1.85-2.33-.07-.19-.11-.4-.11-.61 0-1.06.25-2.07.69-2.96.44-.89 1.08-1.69 1.85-2.33C9.95 6.41 11.9 7.5 12 7.5c3.31 0 6 2.69 6 6s-2.69 6-6 6z"/>
            </svg>
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
      </div>
      
      <!-- 展开的历史文件面板 -->
      <div 
        class="history-panel" 
        :class="{ expanded: sidePanelExpanded }"
        v-if="sidePanelExpanded"
      >
        <div class="history-header">
          <h3>历史文件</h3>
          <div class="batch-download-buttons">
            <el-button 
              v-if="!batchDownloadMode"
              size="small" 
              @click="toggleBatchDownload" 
              class="batch-download-btn"
              type="primary"
            >
              下载
            </el-button>
            <template v-else>
              <el-button 
                size="small" 
                @click="toggleBatchDownload" 
                class="batch-confirm-btn"
                type="success"
              >
                确认
              </el-button>
              <el-button 
                size="small" 
                @click="cancelBatchDownload" 
                class="batch-cancel-btn"
                type="info"
              >
                取消
              </el-button>
            </template>
          </div>
        </div>
        <div class="history-content">
          <div class="file-list">
            <div v-for="file in userFiles" :key="file.file_id" class="file-item" :class="{ 'batch-mode': batchDownloadMode }"
                 @click="batchDownloadMode ? handleFileItemClick(file) : null">
              <div class="file-checkbox" v-if="batchDownloadMode" @click.stop>
                <el-checkbox 
                  :model-value="selectedFiles.some(f => f.file_id === file.file_id)"
                  @change="(checked) => handleFileSelection(file, checked)"
                >
                </el-checkbox>
              </div>
              <el-link 
                :href="file.url" 
                target="_blank" 
                :class="{ 'selectable': batchDownloadMode }"
                @click="handleFileLinkClick($event, file.url)"
              >
                {{ file.filename }}
              </el-link>
              <div class="file-actions" v-if="!batchDownloadMode">
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
      <!-- 展开的历史会话面板（互斥显示） -->
      <div
        class="history-panel"
        :class="{ expanded: sessionPanelExpanded }"
        v-if="sessionPanelExpanded"
        style="left: 80px; top: 0; z-index: 999;"
      >
        <div class="history-header" style="display: flex; justify-content: space-between; align-items: center;">
          <h3>历史会话</h3>
          <div class="batch-download-buttons">
            <el-button size="small" type="primary" class="batch-download-btn" @click="createNewSession">新的对话</el-button>
          </div>
        </div>
        <div class="history-content">
          <div class="file-list">
            <div
              v-for="session in userSessions"
              :key="session.session_id"
              class="file-item"
              :class="{ selected: selectedSessionId === session.session_id }"
              @click="loadSession(session)"
              style="cursor:pointer;"
            >
              <template v-if="sessionRenameEditing === session.session_id">
                <el-input
                  v-model="sessionRenameInput"
                  size="small"
                  class="session-rename-input"
                  style="width:120px;"
                  @keyup.enter="confirmRenameSession(session)"
                  @blur="cancelRenameSession"
                />
                <el-button size="mini" type="info" class="batch-cancel-btn" circle @mousedown.prevent @click="onRenameConfirmClick(session)">✔</el-button>
              </template>
              <template v-else>
                <span class="session-name" style="flex:1 1 auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ session.name }}</span>
                <el-button size="mini" type="info" class="batch-cancel-btn" circle @click.stop="startRenameSession(session)" title="重命名">✎</el-button>
                <el-button size="mini" type="danger" class="delete-btn" circle @click.stop="deleteSession(session.session_id)" title="删除">×</el-button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域自适应居中 -->
    <div class="main-content" :class="{ 
      'sidebar-expanded': sidePanelExpanded || sessionPanelExpanded,
      'welcome-mode': isWelcomeMode,
      'chat-mode': !isWelcomeMode 
    }">
      <!-- 过渡动画容器 -->
      <transition 
        name="smooth-transform"
        mode="out-in"
        @before-leave="beforeLeave"
        @leave="leave"
        @before-enter="beforeEnter"
        @enter="enter"
        @after-enter="afterEnter"
      >
        <div v-if="isWelcomeMode" class="welcome-content-wrapper" key="welcome">
          <!-- 居中的欢迎内容 -->
          <div class="welcome-content">
            <!-- 标题 -->
            <h1 ref="welcomeTitle" class="welcome-title animate-target" data-target="chat-title">网络流量研判大模型对话助手</h1>
            
            <!-- AI欢迎消息 -->
            <div ref="welcomeMessage" class="welcome-ai-message animate-target" data-target="chat-message">
              <div class="welcome-ai-avatar">AI</div>
              <div class="welcome-ai-bubble">
                <div class="welcome-bubble-content">
                  <div class="welcome-message-text">你好，有什么可以帮你？</div>
                </div>
                <div class="welcome-bubble-tail"></div>
              </div>
            </div>

            <!-- 输入区域 -->
            <div class="welcome-input-section">
              <div v-if="!isLogin" class="welcome-login-notice">请先登录后使用对话和上传服务</div>
              
              <div class="welcome-pending-files-area" v-if="pendingFiles.length">
                <span v-for="file in pendingFiles" :key="file.file_id" class="welcome-pending-file-item">
                  <el-link @click="handleFileLinkClickGeneral($event, file.url)">{{ file.filename }}</el-link>
                  <el-button type="text" @click="removePendingFile(file.file_id)" class="welcome-pending-delete-btn" title="删除">×</el-button>
                </span>
              </div>
              
              <div v-if="mode==='pcap'||mode==='rules'" class="welcome-mode-indicator">
                <span>当前模式：<b>{{ mode==='pcap' ? '流量分析报告' : '流量规则' }}</b></span>
                <el-input v-model="customFileName" size="small" style="width:180px;margin-left:12px;" :placeholder="mode==='pcap'?'pcap.txt':'rules.txt'" />
                <el-button size="small" type="text" style="margin-left:12px;" @click="cancelMode">取消指令</el-button>
              </div>
              
              <!-- 统一的大输入框容器 -->
              <div ref="welcomeInput" class="welcome-unified-input-box animate-target" data-target="chat-input">
                <!-- 上部分：文本输入区域 -->
                <div class="welcome-text-input-area">
                  <textarea
                    v-model="inputMsg"
                    placeholder="和我聊聊天吧 (Enter发送，Shift+Enter换行)"
                    class="welcome-custom-textarea"
                    :disabled="!isLogin"
                    :maxlength="2000"
                    @keydown="handleKeyDown"
                  ></textarea>
                  <div class="welcome-char-count">{{ inputMsg.length }}/2000</div>
                </div>
                
                <!-- 下部分：按钮区域 -->
                <div class="welcome-button-area">
                  <!-- 左侧按钮组 -->
                  <div class="welcome-left-buttons">
                    <el-button size="small" :disabled="!isLogin" @click="openUploadDialog" class="welcome-box-button">上传文件</el-button>
                    <el-dropdown @command="handleModeCommand" trigger="click">
                      <el-button size="small" :disabled="!isLogin" class="welcome-box-button">
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
                  <div class="welcome-right-buttons">
                    <el-button type="primary" @click="sendMsg" :disabled="!isLogin" class="welcome-send-box-button">发送</el-button>
                  </div>
                </div>
              </div>
              
              <!-- AI 免责声明 -->
              <div class="welcome-ai-disclaimer">
                内容由 AI 生成，请仔细甄别
              </div>
            </div>
          </div>
        </div>

        <!-- 正常模式布局 -->
        <div v-else class="chat-content-wrapper" key="chat">
          <!-- 顶部标题栏 -->
          <div class="content-header">
            <span ref="chatTitle" class="app-title" id="chat-title">网络流量研判大模型对话助手</span>
          </div>

          <!-- 对话区域 -->
          <div class="chat-container">
            <div class="chat-messages-area" ref="chatMessagesArea">
              <div v-for="(msg, idx) in messages" :key="idx" :class="['chat-bubble-container', msg.role]">
                <!-- AI消息：头像 + 泡泡 -->
                <template v-if="msg.role === 'ai' && idx === 0">
                  <div class="ai-avatar">AI</div>
                  <div ref="chatMessage" class="chat-bubble ai-bubble" id="chat-message">
                    <div class="bubble-content">
                      <template v-if="msg.files && msg.files.length">
                        <div v-for="file in msg.files" :key="file.file_id" class="file-link">
                          <el-link @click="handleFileLinkClickGeneral($event, file.url)">{{ file.filename }}</el-link>
                        </div>
                        <div v-if="msg.content" class="message-text">{{ msg.content }}</div>
                      </template>
                      <template v-else-if="msg.file">
                        <div class="file-link">
                          <el-link @click="handleFileLinkClickGeneral($event, msg.file.url)">{{ msg.file.filename }}</el-link>
                        </div>
                      </template>
                      <template v-else>
                        <div class="message-text">{{ msg.content }}</div>
                      </template>
                    </div>
                    <div class="bubble-tail ai-tail"></div>
                  </div>
                </template>
                <template v-else-if="msg.role === 'ai'">
                  <div class="ai-avatar">AI</div>
                  <div class="chat-bubble ai-bubble">
                    <div class="bubble-content">
                      <template v-if="msg.files && msg.files.length">
                        <div v-for="file in msg.files" :key="file.file_id" class="file-link">
                          <el-link @click="handleFileLinkClickGeneral($event, file.url)">{{ file.filename }}</el-link>
                        </div>
                        <div v-if="msg.content" class="message-text">{{ msg.content }}</div>
                      </template>
                      <template v-else-if="msg.file">
                        <div class="file-link">
                          <el-link @click="handleFileLinkClickGeneral($event, msg.file.url)">{{ msg.file.filename }}</el-link>
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
                          <el-link @click="handleFileLinkClickGeneral($event, file.url)">{{ file.filename }}</el-link>
                        </div>
                        <div v-if="msg.content" class="message-text">{{ msg.content }}</div>
                      </template>
                      <template v-else-if="msg.file">
                        <div class="file-link">
                          <el-link @click="handleFileLinkClickGeneral($event, msg.file.url)">{{ msg.file.filename }}</el-link>
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
                <el-link @click="handleFileLinkClickGeneral($event, file.url)">{{ file.filename }}</el-link>
                <el-button type="text" @click="removePendingFile(file.file_id)" class="pending-delete-btn" title="删除">×</el-button>
              </span>
            </div>
            
            <div v-if="mode==='pcap'||mode==='rules'" class="mode-indicator">
              <span>当前模式：<b>{{ mode==='pcap' ? '流量分析报告' : '流量规则' }}</b></span>
              <el-input v-model="customFileName" size="small" style="width:180px;margin-left:12px;" :placeholder="mode==='pcap'?'pcap.txt':'rules.txt'" />
              <el-button size="small" type="text" style="margin-left:12px;" @click="cancelMode">取消指令</el-button>
            </div>
            
            <!-- 统一的大输入框容器 -->
            <div ref="chatInput" class="unified-input-box" id="chat-input">
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
      </transition>
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
    const isWelcomeMode = ref(true); // 新增：欢迎模式状态
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
    const chatMessagesArea = ref(null); // 对话消息区域的ref
    const pendingFiles = ref([]); // 待发送文件列表
    const mode = ref('chat'); // chat/pcap/rules
    const customFileName = ref(''); // 新增：自定义生成文件名
    const sidePanelExpanded = ref(false);
    const batchDownloadMode = ref(false); // 批量下载模式
    const selectedFiles = ref([]); // 选中的文件列表
    const sessionPanelExpanded = ref(false); // 历史会话栏展开状态
    
    // 主题切换功能
    const isDarkMode = ref(localStorage.getItem('theme') !== 'light');
    
    // 切换主题
    const toggleTheme = () => {
      isDarkMode.value = !isDarkMode.value;
      const theme = isDarkMode.value ? 'dark' : 'light';
      localStorage.setItem('theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
    };
    
    // 初始化主题
    const initTheme = () => {
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme) {
        isDarkMode.value = savedTheme === 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
      } else {
        // 默认为暗色主题
        isDarkMode.value = true;
        localStorage.setItem('theme', 'dark');
        document.documentElement.setAttribute('data-theme', 'dark');
      }
    };
    
    // 动画相关的refs
    const welcomeTitle = ref(null);
    const welcomeMessage = ref(null);
    const welcomeInput = ref(null);
    const chatTitle = ref(null);
    const chatMessage = ref(null);
    const chatInput = ref(null);
    
    // 动画状态
    const animationData = ref({});
    
    // 计算元素的位置和尺寸
    const getElementBounds = (element) => {
      if (!element) return null;
      const rect = element.getBoundingClientRect();
      return {
        x: rect.left,
        y: rect.top,
        width: rect.width,
        height: rect.height,
        centerX: rect.left + rect.width / 2,
        centerY: rect.top + rect.height / 2
      };
    };
    
    // 动画钩子函数
    const beforeLeave = (el) => {
      // 记录欢迎模式元素的位置
      if (welcomeTitle.value && welcomeMessage.value && welcomeInput.value) {
        animationData.value = {
          title: getElementBounds(welcomeTitle.value),
          message: getElementBounds(welcomeMessage.value),
          input: getElementBounds(welcomeInput.value)
        };
      }
    };
    
    const leave = (el, done) => {
      // 立即隐藏离开的元素
      el.style.opacity = '0';
      setTimeout(done, 50);
    };
    
    const beforeEnter = (el) => {
      // 准备进入的聊天模式元素
      el.style.opacity = '0';
    };
    
    const enter = async (el, done) => {
      // 添加动画状态标识
      document.body.classList.add('animating');
      
      // 等待DOM更新
      await nextTick();
      
      // 简化版本：添加一个淡入效果
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'all 0.5s ease';
      
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
        });
      });
      
      setTimeout(() => {
        document.body.classList.remove('animating');
        done();
      }, 500);
      return;
      
      // 暂时注释掉复杂动画逻辑，先确保基本功能正常
      /*
      // 获取目标位置
      const targetPositions = {};
      if (chatTitle.value) {
        targetPositions.title = getElementBounds(chatTitle.value);
      }
      if (chatMessage.value) {
        targetPositions.message = getElementBounds(chatMessage.value);
      }
      if (chatInput.value) {
        targetPositions.input = getElementBounds(chatInput.value);
      }
      
      if (!animationData.value.title || !targetPositions.title) {
        // 如果没有动画数据，直接显示
        el.style.opacity = '1';
        document.body.classList.remove('animating');
        done();
        return;
      }
      
      // 创建动画元素
      const createAnimationElement = (sourceData, targetData, originalEl, content, additionalStyles = {}) => {
        const animEl = document.createElement('div');
        animEl.className = 'animation-element';
        animEl.innerHTML = content;
        
        // 设置初始位置和样式
        Object.assign(animEl.style, {
          left: sourceData.x + 'px',
          top: sourceData.y + 'px',
          width: sourceData.width + 'px',
          height: sourceData.height + 'px',
          transition: 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)',
          transformOrigin: 'center center',
          opacity: '1',
          ...additionalStyles
        });
        
        // 复制部分原始样式
        const computedStyle = window.getComputedStyle(originalEl);
        animEl.style.backgroundColor = computedStyle.backgroundColor;
        animEl.style.border = computedStyle.border;
        animEl.style.borderRadius = computedStyle.borderRadius;
        animEl.style.boxShadow = computedStyle.boxShadow;
        
        document.body.appendChild(animEl);
        
        // 触发动画
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            const scaleX = targetData.width / sourceData.width;
            const scaleY = targetData.height / sourceData.height;
            const translateX = targetData.x - sourceData.x;
            const translateY = targetData.y - sourceData.y;
            
            animEl.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scaleX}, ${scaleY})`;
          });
        });
        
        return animEl;
      };
      
      const animationElements = [];
      
      // 创建标题动画
      if (animationData.value.title && targetPositions.title && chatTitle.value) {
        const titleEl = createAnimationElement(
          animationData.value.title,
          targetPositions.title,
          chatTitle.value,
          '<span style="display: flex; align-items: center; justify-content: center; height: 100%; font-size: 48px; color: var(--text-accent); font-weight: 700; letter-spacing: 2px; text-shadow: 0 4px 20px var(--accent-shadow-light);">网络流量研判大模型对话助手</span>'
        );
        animationElements.push(titleEl);
      }
      
      // 创建消息动画
      if (animationData.value.message && targetPositions.message && chatMessage.value) {
        const messageEl = createAnimationElement(
          animationData.value.message,
          targetPositions.message,
          chatMessage.value,
          '<div style="display: flex; align-items: flex-start; gap: 16px; padding: 20px 24px;"><div style="width: 60px; height: 60px; border-radius: 50%; background: var(--bg-tertiary); border: 3px solid var(--bg-quaternary); display: flex; align-items: center; justify-content: center; color: var(--text-accent); font-weight: bold; font-size: 18px; flex-shrink: 0; box-shadow: 0 6px 24px var(--shadow-color);">AI</div><div style="background: var(--bg-secondary); border: 2px solid var(--bg-tertiary); color: var(--text-primary); border-radius: 24px; border-bottom-left-radius: 8px; padding: 20px 24px; font-size: 20px; font-weight: 500; box-shadow: 0 8px 32px var(--shadow-color); position: relative;">你好，有什么可以帮你？<div style="position: absolute; bottom: 0; left: -12px; width: 0; height: 0; border-right: 16px solid var(--bg-secondary); border-bottom: 16px solid transparent;"></div></div></div>'
        );
        animationElements.push(messageEl);
      }
      
      // 创建输入框动画
      if (animationData.value.input && targetPositions.input && chatInput.value) {
        const inputEl = createAnimationElement(
          animationData.value.input,
          targetPositions.input,
          chatInput.value,
          '<div style="background: var(--bg-tertiary); border-radius: 48px; border: 4px solid var(--border-color); height: 100%; display: flex; align-items: center; justify-content: center; color: var(--text-secondary); font-size: 18px; box-shadow: 0 16px 64px var(--shadow-color);">和我聊聊天吧 (Enter发送，Shift+Enter换行)</div>'
        );
        animationElements.push(inputEl);
      }
      
      // 动画完成后清理
      setTimeout(() => {
        animationElements.forEach(animEl => {
          if (animEl && animEl.parentNode) {
            animEl.parentNode.removeChild(animEl);
          }
        });
        
        el.style.opacity = '1';
        document.body.classList.remove('animating');
        done();
      }, 800);
      */
    };
    
    const afterEnter = (el) => {
      // 动画完成后的清理工作
      animationData.value = {};
      
      // 确保页面可以正常滚动
      document.body.classList.remove('animating');
      
      // 清理可能残留的动画元素
      const remainingAnimElements = document.querySelectorAll('.animation-element');
      remainingAnimElements.forEach(animEl => {
        if (animEl && animEl.parentNode) {
          animEl.parentNode.removeChild(animEl);
        }
      });
    };
    
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
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
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

    // 滚动到对话底部
    const scrollToBottom = () => {
      nextTick(() => {
        if (chatMessagesArea.value) {
          chatMessagesArea.value.scrollTop = chatMessagesArea.value.scrollHeight;
        }
      });
    };

    // 发送消息
    const sendMsg = async () => {
      if (!isLogin.value) return;
      if (!inputMsg.value.trim() && pendingFiles.value.length === 0) return;
      
      // 第一次发送消息时切换到正常模式
      if (isWelcomeMode.value) {
        isWelcomeMode.value = false;
      }
      
      if (mode.value === 'chat') {
        // 普通对话
        messages.value.push({ role: 'user', content: inputMsg.value, files: [...pendingFiles.value] });
        scrollToBottom(); // 滚动到底部显示用户消息
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
          scrollToBottom(); // 滚动到底部显示AI回复
        } catch (e) {
          messages.value.push({ role: 'ai', content: '大模型接口异常' });
          scrollToBottom(); // 滚动到底部显示错误消息
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
          scrollToBottom(); // 滚动到底部显示用户消息
          messages.value.push({ role: 'ai', content: '', files: [res.data] });
          scrollToBottom(); // 滚动到底部显示AI生成的文件
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
      await saveCurrentSession(undefined, messages.value);
      fetchUserSessions();
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
    // 下载文件
    const downloadFile = async (fileUrl, filename) => {
      try {
        // 添加认证头请求文件
        const response = await axios.get(fileUrl, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') },
          responseType: 'blob'
        });
        
        // 创建下载链接
        const blob = new Blob([response.data]);
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        
        // 清理
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
        ElMessage.success('文件下载成功');
      } catch (e) {
        ElMessage.error('文件下载失败');
      }
    };
    
    // 切换批量下载模式
    const toggleBatchDownload = async () => {
      if (batchDownloadMode.value) {
        // 确认下载
        if (selectedFiles.value.length === 0) {
          ElMessage.warning('请选择要下载的文件');
          batchDownloadMode.value = false;
          selectedFiles.value = [];
          return;
        }
        
        try {
          // 直接使用浏览器下载功能
          ElMessage.info(`开始下载 ${selectedFiles.value.length} 个文件，请在浏览器弹窗中确认允许多个下载`);
          
          for (let i = 0; i < selectedFiles.value.length; i++) {
            const file = selectedFiles.value[i];
            
            // 创建带认证的下载链接
            const response = await axios.get(file.url, {
              headers: { Authorization: 'Bearer ' + localStorage.getItem('token') },
              responseType: 'blob'
            });
            
            // 创建临时下载链接
            const blob = new Blob([response.data]);
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = file.filename;
            link.style.display = 'none';
            
            // 添加到DOM并触发下载
            document.body.appendChild(link);
            link.click();
            
            // 延时清理，避免过快清理导致下载失败
            setTimeout(() => {
              document.body.removeChild(link);
              window.URL.revokeObjectURL(downloadUrl);
            }, 100);
            
            // 添加延时避免浏览器阻止多文件下载
            if (i < selectedFiles.value.length - 1) {
              await new Promise(resolve => setTimeout(resolve, 300));
            }
          }
          
          ElMessage.success(`已触发 ${selectedFiles.value.length} 个文件的下载`);
        } catch (e) {
          ElMessage.error('批量下载失败：' + (e.message || '未知错误'));
        }
        
        // 重置状态
        batchDownloadMode.value = false;
        selectedFiles.value = [];
      } else {
        // 进入批量下载模式
        batchDownloadMode.value = true;
        selectedFiles.value = [];
      }
    };
    
    // 处理文件选择
    const handleFileSelection = (file, checked) => {
      const index = selectedFiles.value.findIndex(f => f.file_id === file.file_id);
      if (checked && index === -1) {
        selectedFiles.value.push(file);
      } else if (!checked && index > -1) {
        selectedFiles.value.splice(index, 1);
      }
    };
    
    // 取消批量下载
    const cancelBatchDownload = () => {
      batchDownloadMode.value = false;
      selectedFiles.value = [];
      ElMessage.info('已取消批量下载');
    };
    
    // 处理文件项点击（批量模式下）
    const handleFileItemClick = (file) => {
      if (!batchDownloadMode.value) return;
      
      const isSelected = selectedFiles.value.some(f => f.file_id === file.file_id);
      handleFileSelection(file, !isSelected);
    };
    
    // 处理文件链接点击
    const handleFileLinkClick = (event, url) => {
      if (batchDownloadMode.value) {
        // 批量模式下，只有按住Shift键才打开链接
        if (!event.shiftKey) {
          event.preventDefault();
          // 不阻止冒泡，让事件传递到文件项进行选择
        } else {
          // 按住Shift键时阻止默认行为和冒泡，手动在新标签页打开
          event.preventDefault();
          event.stopPropagation();
          // 创建临时链接元素并模拟点击，确保在新标签页打开
          const link = document.createElement('a');
          link.href = url;
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }
      }
      // 非批量模式下，正常打开链接（默认行为）
    };
    
    // 处理一般文件链接点击（聊天消息、待发送文件等）
    const handleFileLinkClickGeneral = (event, url) => {
      event.preventDefault();
      // 创建临时链接元素并模拟点击，确保在新标签页打开
      const link = document.createElement('a');
      link.href = url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };
    window.addEventListener('storage', () => {
      isLogin.value = localStorage.getItem('isLogin') === '1';
      fetchUserFiles();
    });
    onMounted(() => {
      initTheme(); // 初始化主题
      fetchUserFiles();
      fetchUserSessions();
      scrollToBottom(); // 页面加载时滚动到最新消息
    });
    // 历史会话相关变量
    const userSessions = ref([]);
    const selectedSessionId = ref(null);
    const sessionRenameInput = ref('');
    const sessionRenameEditing = ref(null);
    // 历史会话相关方法
    const fetchUserSessions = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/modeltask/list_sessions/', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        userSessions.value = res.data.sessions || [];
      } catch (e) {
        userSessions.value = [];
      }
    };
    const loadSession = async (session) => {
      try {
        const res = await axios.get(`http://localhost:8000/api/modeltask/get_session/${session.session_id}/`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        messages.value = res.data.messages || [];
        selectedSessionId.value = session.session_id;
        isWelcomeMode.value = false;
      } catch (e) {}
    };
    const deleteSession = async (session_id) => {
      try {
        await axios.post('http://localhost:8000/api/modeltask/delete_session/', { session_id }, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        fetchUserSessions();
        if (selectedSessionId.value === session_id) {
          messages.value = [{ role: 'ai', content: '你好，有什么可以帮你？' }];
          selectedSessionId.value = null;
          isWelcomeMode.value = true;
        }
      } catch (e) {}
    };
    const startRenameSession = (session) => {
      sessionRenameEditing.value = session.session_id;
      sessionRenameInput.value = session.name;
    };
    const confirmRenameSession = async (session) => {
      try {
        await axios.post('http://localhost:8000/api/modeltask/rename_session/', {
          session_id: session.session_id,
          name: sessionRenameInput.value
        }, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        sessionRenameEditing.value = null;
        // 本地同步更新
        const s = userSessions.value.find(s => s.session_id === session.session_id);
        if (s) s.name = sessionRenameInput.value;
        fetchUserSessions();
      } catch (e) {}
    };
    const cancelRenameSession = () => {
      sessionRenameEditing.value = null;
      sessionRenameInput.value = '';
    };
    const isSessionEmpty = () => {
      // 仅有AI欢迎语，且无用户消息
      return messages.value.length === 1 && messages.value[0].role === 'ai' && (!messages.value[0].content || messages.value[0].content === '你好，有什么可以帮你？');
    };
    const createNewSession = async () => {
      // 如果当前会话非空才保存
      if (!isSessionEmpty()) {
        await saveCurrentSession(undefined, messages.value);
        fetchUserSessions();
      }
      // 切换到新空会话
      messages.value = [{ role: 'ai', content: '你好，有什么可以帮你？' }];
      selectedSessionId.value = null;
      isWelcomeMode.value = true;
    };
    const saveCurrentSession = async (name, msgs) => {
      try {
        // 优先用当前选中会话的名称
        let sessionName = name;
        if (!sessionName && selectedSessionId.value) {
          const session = userSessions.value.find(s => s.session_id === selectedSessionId.value);
          if (session) sessionName = session.name;
        }
        const res = await axios.post('http://localhost:8000/api/modeltask/save_session/', {
          name: sessionName || '新会话',
          messages: msgs || messages.value,
          session_id: selectedSessionId.value || undefined
        }, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        if (res.data.session_id) {
          selectedSessionId.value = res.data.session_id;
        }
      } catch (e) {}
    };
    const onRenameConfirmClick = async (session) => {
      await confirmRenameSession(session);
      cancelRenameSession();
    };
    return {
      isLogin,
      isWelcomeMode, // 新增：导出欢迎模式状态
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
      downloadFile,
      handleModeCommand,
      uploadComponent,
      pendingFiles,
      removePendingFile,
      mode,
      customFileName,
      cancelMode,
      sidePanelExpanded,
      sessionPanelExpanded,
      toggleSidePanel,
      batchDownloadMode,
      selectedFiles,
      toggleBatchDownload,
      handleFileSelection,
      cancelBatchDownload,
      handleFileItemClick,
      handleFileLinkClick,
      handleFileLinkClickGeneral,
      chatMessagesArea,
      scrollToBottom,
      // 主题切换相关
      isDarkMode,
      toggleTheme,
      // 动画相关
      welcomeTitle,
      welcomeMessage,
      welcomeInput,
      chatTitle,
      chatMessage,
      chatInput,
      beforeLeave,
      leave,
      beforeEnter,
      enter,
      afterEnter,
      userSessions,
      selectedSessionId,
      sessionRenameInput,
      sessionRenameEditing,
      fetchUserSessions,
      loadSession,
      deleteSession,
      startRenameSession,
      confirmRenameSession,
      cancelRenameSession,
      createNewSession,
      saveCurrentSession,
      onRenameConfirmClick,
      isSessionEmpty
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
  min-height: 300px !important;
  overflow: hidden !important;
  background: var(--bg-primary) !important;
  box-sizing: border-box;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  transition: background-color 0.3s ease, color 0.3s ease;
}

*, *::before, *::after {
  box-sizing: border-box;
}

#app {
  height: 100vh;
  width: 100vw;
  min-height: 300px;
  overflow: hidden;
  background: var(--bg-primary);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  transition: background-color var(--theme-transition), color var(--theme-transition);
}

.ai-chat-app.app-root {
  height: 100vh;
  width: 100vw;
  background: var(--bg-primary);
  display: flex;
  align-items: stretch;
  justify-content: flex-start;
  box-sizing: border-box;
  position: relative;
  overflow: hidden;
  margin: 0;
  padding: 0;
  transition: background-color var(--theme-transition), color var(--theme-transition);
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
  background: var(--bg-tertiary);
  padding: 20px 0;
  box-sizing: border-box;
  transition: background-color var(--theme-transition);
}

.top-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.bottom-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}
.expand-btn {
  background: var(--bg-secondary);
  border: none;
  border-radius: 10px;
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 8px var(--shadow-color);
  transition: all 0.25s ease-in-out;
  color: var(--text-primary);
  font-size: 20px;
}
.expand-btn:hover {
  transform: scale(1.05);
  background: var(--bg-quaternary);
}
.expand-btn.active {
  background: var(--bg-quaternary);
  color: var(--text-accent);
  box-shadow: 0 12px 40px var(--accent-shadow);
  border: 2px solid var(--text-accent);
}

/* 登录按钮样式 */
.login-btn {
  background: var(--bg-secondary);
  border: none;
  border-radius: 10px;
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 8px var(--shadow-color);
  transition: all 0.25s ease-in-out;
  color: var(--text-accent);
}

.login-btn:hover {
  transform: scale(1.05);
  background: var(--text-accent);
  color: var(--button-hover);
  box-shadow: 0 4px 12px var(--accent-shadow);
}

[data-theme="light"] .login-btn:hover {
  box-shadow: 0 4px 12px var(--accent-shadow);
}

/* 亮色主题下的登录按钮边框 */
[data-theme="light"] .login-btn {
  border: 3px solid var(--border-color) !important;
}

[data-theme="light"] .login-btn:hover {
  border-color: var(--text-accent) !important;
}

/* 退出登录按钮样式 */
.logout-btn {
  background: var(--bg-secondary);
  border: none;
  border-radius: 10px;
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 8px var(--shadow-color);
  transition: all 0.25s ease-in-out;
  color: var(--text-danger);
}

.logout-btn:hover {
  transform: scale(1.05);
  background: var(--text-danger);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.4);
}

/* 亮色主题下的退出登录按钮边框 */
[data-theme="light"] .logout-btn {
  border: 3px solid var(--border-color) !important;
}

[data-theme="light"] .logout-btn:hover {
  border-color: var(--text-danger) !important;
}

/* 主题切换按钮样式 */
.theme-toggle-btn {
  background: var(--bg-secondary);
  border: none;
  border-radius: 10px;
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 2px 8px var(--shadow-color);
  transition: all 0.25s ease-in-out;
  color: var(--text-accent);
}

.theme-toggle-btn:hover {
  transform: scale(1.05);
  background: var(--text-accent);
  color: var(--button-hover);
  box-shadow: 0 4px 12px var(--accent-shadow);
}

[data-theme="light"] .theme-toggle-btn:hover {
  box-shadow: 0 4px 12px var(--accent-shadow);
}

/* 亮色主题下的主题切换按钮边框 */
[data-theme="light"] .theme-toggle-btn {
  border: 3px solid var(--border-color) !important;
}

[data-theme="light"] .theme-toggle-btn:hover {
  border-color: var(--text-accent) !important;
}
.history-panel {
  width: 340px;
  background: var(--bg-secondary);
  border-radius: 0 14px 14px 0;
  box-shadow: 2px 0 12px var(--shadow-color);
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
  justify-content: flex-start;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 10px;
  position: relative;
}

.batch-download-buttons {
  position: absolute;
  right: 45px;
  top: 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
}

.batch-download-buttons .batch-download-btn {
  position: relative;
}

.batch-download-buttons .batch-cancel-btn,
.batch-download-buttons .batch-confirm-btn {
  position: static;
  left: unset;
  right: unset;
  top: unset;
  margin: 0;
}
.history-header h3 {
  font-size: 18px;
  color: var(--text-accent);
  font-weight: 600;
  margin: 0;
}

.batch-download-btn {
  background-color: var(--bg-secondary) !important;
  border-color: var(--bg-quaternary) !important;
  color: var(--text-accent) !important;
  border-radius: 8px !important;
  padding: 6px 12px !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 2px 8px var(--shadow-color) !important;
}

.batch-download-btn:hover {
  background-color: var(--text-accent) !important;
  border-color: var(--text-accent) !important;
  color: #ffffff !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px var(--accent-shadow) !important;
}

[data-theme="light"] .batch-download-btn:hover {
  box-shadow: 0 4px 12px var(--accent-shadow) !important;
}

/* 亮色主题下的批量下载按钮边框 */
[data-theme="light"] .batch-download-btn {
  border: 3px solid var(--border-color) !important;
}

[data-theme="light"] .batch-download-btn:hover {
  border-color: var(--text-accent) !important;
}

.batch-download-btn.el-button--success {
  background-color: var(--text-accent) !important;
  border-color: var(--text-accent) !important;
  color: #ffffff !important;
}

.batch-download-btn.el-button--success:hover {
  background-color: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
}

.batch-cancel-btn,
.batch-confirm-btn {
  padding: 6px 12px !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  border-radius: 8px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-shadow: 0 2px 8px var(--shadow-color) !important;
  transition: all 0.25s ease !important;
  border-width: 1.5px !important;
}

.batch-confirm-btn {
  background-color: var(--text-accent) !important;
  border-color: var(--text-accent) !important;
  color: #fff !important;
}

.batch-cancel-btn:hover {
  background-color: var(--bg-quaternary) !important;
  border-color: var(--text-accent) !important;
  color: var(--text-accent) !important;
}

.batch-confirm-btn:hover {
  background-color: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
  color: #fff !important;
}

[data-theme="light"] .batch-cancel-btn {
  border-width: 1.5px !important;
  border-color: var(--border-color) !important;
}

[data-theme="light"] .batch-cancel-btn:hover {
  border-color: var(--text-accent) !important;
  color: var(--text-accent) !important;
}

.history-content {
  flex: 1;
  overflow-y: auto;
  max-height: calc(100vh - 120px);
  scrollbar-width: thin;
  scrollbar-color: var(--bg-tertiary) transparent;
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
  background: var(--bg-tertiary);
  border-radius: 4px;
  border: 1px solid transparent;
  background-clip: content-box;
  transition: all 0.25s ease;
}

.history-content::-webkit-scrollbar-thumb:hover {
  background: var(--bg-quaternary);
  background-clip: content-box;
}

.history-content::-webkit-scrollbar-thumb:active {
  background: var(--text-accent);
  background-clip: content-box;
}

.file-list {
  flex: 1 1 auto;
  overflow-y: auto;
  max-height: calc(100vh - 120px);
  scrollbar-width: thin;
  scrollbar-color: var(--bg-tertiary) transparent;
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
  background: var(--bg-tertiary);
  border-radius: 4px;
  border: 1px solid transparent;
  background-clip: content-box;
  transition: all 0.25s ease;
}

.file-list::-webkit-scrollbar-thumb:hover {
  background: var(--bg-quaternary);
  background-clip: content-box;
}

.file-list::-webkit-scrollbar-thumb:active {
  background: var(--text-accent);
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
  width: 260px;
  min-width: 220px;
  max-width: 300px;
  min-height: 36px;
  box-sizing: border-box;
}

.file-item:hover {
  background: var(--hover-bg);
}

.file-item .el-link {
  flex: 1 1 auto;
  margin-right: 12px;
  color: var(--text-primary) !important;
  text-decoration: none !important;
  transition: color 0.25s ease;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: calc(100% - 40px);
  min-width: 180px;
  width: 220px;
  display: block;
  height: 20px;
  line-height: 20px;
}

.file-item .el-link:hover {
  color: var(--text-accent) !important;
}

.file-item.batch-mode {
  background: var(--hover-bg-light) !important;
  border: 1px solid var(--bg-tertiary) !important;
  padding: 4px 8px !important;
  cursor: pointer !important;
  user-select: none !important;
}

.file-item.batch-mode:hover {
  background: var(--accent-shadow-light) !important;
  border-color: var(--text-accent) !important;
}

[data-theme="light"] .file-item.batch-mode:hover {
  background: var(--accent-shadow-light) !important;
}

.file-item.batch-mode .el-link {
  width: 190px !important;
  max-width: calc(100% - 68px) !important;
}

.file-checkbox {
  margin-right: 8px;
  flex-shrink: 0;
  height: 20px;
  display: flex;
  align-items: center;
}

.file-checkbox .el-checkbox {
  color: var(--text-primary) !important;
}

.file-checkbox .el-checkbox__input.is-checked .el-checkbox__inner {
  background-color: var(--text-accent) !important;
  border-color: var(--text-accent) !important;
}

.file-checkbox .el-checkbox__input.is-checked .el-checkbox__inner::after {
  border-color: #ffffff !important;
}

.el-link.selectable {
  cursor: pointer !important;
  user-select: none !important;
}

.file-actions {
  display: flex;
  gap: 4px;
  align-items: center;
}


.main-content {
  position: fixed;
  left: 80px;
  top: 0;
  right: 0;
  bottom: 0;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  transition: left 0.25s cubic-bezier(.4,0,.2,1), background-color var(--theme-transition);
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
  background: var(--bg-primary);
  border-bottom: none;
  margin: 0;
  box-sizing: border-box;
  transition: background-color 0.3s ease;
}
.app-title {
  font-size: 18px;
  color: var(--text-accent);
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
  align-items: stretch;
  padding: 15px 20px;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
  min-height: 120px;
}

.chat-messages-area {
  width: 100%;
  max-width: 800px;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px 20px 20px 0;
  background: var(--bg-primary);
  border: none;
  border-radius: 0;
  box-shadow: none;
  margin: 0;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: var(--bg-tertiary) transparent;
  transition: background-color 0.3s ease;
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
  background: var(--bg-tertiary);
  border-radius: 6px;
  border: 2px solid transparent;
  background-clip: content-box;
  transition: all 0.25s ease;
}

.chat-messages-area::-webkit-scrollbar-thumb:hover {
  background: var(--bg-quaternary);
  background-clip: content-box;
}

.chat-messages-area::-webkit-scrollbar-thumb:active {
  background: var(--text-accent);
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
  background: var(--bg-tertiary);
  border: 2px solid var(--bg-quaternary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-accent);
  font-weight: bold;
  font-size: 14px;
  margin-right: 12px;
  flex-shrink: 0;
  box-shadow: 0 3px 12px var(--shadow-color);
  transition: all 0.25s ease;
}

/* 聊天泡泡基础样式 */
.chat-bubble {
  position: relative;
  border-radius: 20px;
  box-shadow: 0 3px 15px var(--shadow-color);
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
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  border-bottom-left-radius: 6px;
  transition: background-color var(--theme-transition), border-color var(--theme-transition);
}

/* 用户泡泡样式 */
.user-bubble {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  border-bottom-right-radius: 6px;
  transition: background-color var(--theme-transition), border-color var(--theme-transition);
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
  left: -9px;
  bottom: 0;
}

.ai-tail::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 0;
  border-right: 13px solid var(--border-color);
  border-bottom: 13px solid transparent;
}

.ai-tail::after {
  content: '';
  position: absolute;
  bottom: 1px;
  left: 1px;
  width: 0;
  height: 0;
  border-right: 12px solid var(--bg-secondary);
  border-bottom: 12px solid transparent;
}

.user-tail {
  right: -9px;
  bottom: 0;
}

.user-tail::before {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 0;
  height: 0;
  border-left: 13px solid var(--border-color);
  border-bottom: 13px solid transparent;
}

.user-tail::after {
  content: '';
  position: absolute;
  bottom: 1px;
  right: 1px;
  width: 0;
  height: 0;
  border-left: 12px solid var(--bg-tertiary);
  border-bottom: 12px solid transparent;
}

/* 消息文本样式 */
.message-text {
  color: var(--text-primary);
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
  color: var(--text-accent) !important;
  text-decoration: underline;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  max-width: 100% !important;
  min-width: 200px !important;
  width: 280px !important;
  display: block !important;
}

.chat-bubble .el-link:hover {
  color: var(--accent-hover) !important;
}

.input-section {
  padding: 15px 20px 8px 20px;
  background: var(--bg-primary);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin: 0;
  box-sizing: border-box;
  transition: background-color 0.3s ease;
}

.login-notice {
  color: var(--text-warning);
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
  background: var(--bg-tertiary);
  border-radius: 6px;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--border-color);
  transition: all 0.25s ease;
  min-width: 180px;
  width: 220px;
  max-width: 280px;
}

.pending-file-item:hover {
  background: var(--bg-secondary);
  border-color: var(--text-accent);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px var(--shadow-color);
}

.pending-file-item .el-link {
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  max-width: calc(100% - 30px) !important;
  min-width: 120px !important;
  width: 180px !important;
  display: block !important;
  flex: 1 1 auto !important;
}

/* 上传文件按钮样式 */
.pending-delete-btn {
  background: transparent !important;
  border: none !important;
  color: var(--text-danger) !important;
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
  background: var(--text-danger) !important;
  color: #ffffff !important;
  transform: scale(1.1) !important;
}

.mode-indicator {
  display: flex;
  align-items: center;
  background: var(--bg-tertiary);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 15px;
  color: var(--text-accent);
  margin-bottom: 10px;
  transition: background-color 0.3s ease;
}

/* 统一的大输入框容器 */
.unified-input-box {
  position: relative;
  width: 100%;
  max-width: 1000px;
  height: 280px;
  min-height: 120px;
  max-height: 400px;
  background: var(--bg-tertiary);
  border-radius: 40px;
  padding: 0;
  box-shadow: 0 12px 48px var(--shadow-color);
  border: 3px solid var(--border-color);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.unified-input-box:focus-within {
  border-color: var(--text-accent);
  box-shadow: 0 16px 56px var(--accent-shadow);
}

/* 上部分：文本输入区域 */
.text-input-area {
  flex: 1;
  position: relative;
  padding: 30px 35px 20px 35px;
  background: var(--bg-tertiary);
}

/* 自定义textarea样式 */
.custom-textarea {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 16px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  resize: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--bg-quaternary) transparent;
}

.custom-textarea::placeholder {
  color: var(--text-secondary);
  font-size: 16px;
}

.custom-textarea::-webkit-scrollbar {
  width: 8px;
}

.custom-textarea::-webkit-scrollbar-track {
  background: transparent;
}

.custom-textarea::-webkit-scrollbar-thumb {
  background: var(--bg-quaternary);
  border-radius: 10px;
}

.custom-textarea::-webkit-scrollbar-thumb:hover {
  background: var(--text-accent);
}

/* 字数统计 */
.char-count {
  position: absolute;
  bottom: 8px;
  right: 20px;
  color: var(--text-secondary);
  font-size: 14px;
  pointer-events: none;
}

/* 下部分：按钮区域 */
.button-area {
  height: 70px;
  background: var(--bg-tertiary);
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
  background-color: var(--bg-secondary) !important;
  border-color: var(--bg-secondary) !important;
  color: var(--text-primary) !important;
  box-shadow: 0 3px 12px var(--shadow-color) !important;
  transition: all 0.25s ease !important;
  height: 44px !important;
}

.box-button:hover {
  background-color: var(--button-hover) !important;
  border-color: var(--text-accent) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px var(--accent-shadow-light) !important;
}

[data-theme="light"] .box-button:hover {
  box-shadow: 0 6px 20px var(--accent-shadow-light) !important;
}

/* 发送按钮样式 */
.send-box-button {
  border-radius: 22px !important;
  padding: 10px 30px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  background-color: var(--text-accent) !important;
  border-color: var(--text-accent) !important;
  color: var(--button-hover) !important;
  box-shadow: 0 4px 16px var(--accent-shadow) !important;
  transition: all 0.25s ease !important;
  height: 44px !important;
  min-width: 100px !important;
}

.send-box-button:hover {
  background-color: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px var(--accent-shadow-strong) !important;
}

[data-theme="light"] .send-box-button {
  box-shadow: 0 4px 16px var(--accent-shadow) !important;
}

[data-theme="light"] .send-box-button:hover {
  box-shadow: 0 8px 24px var(--accent-shadow-strong) !important;
}

/* 下拉菜单优化 */
.unified-input-box .el-dropdown-menu {
  z-index: 2000 !important;
}

/* AI 免责声明样式 */
.ai-disclaimer {
  text-align: center;
  color: var(--text-secondary);
  font-size: 12px;
  margin-top: 2px;
  margin-bottom: 0;
  opacity: 0.8;
  font-weight: 400;
  letter-spacing: 0.5px;
}
/* 旧样式已被新布局替代 */
/* 旧样式已被新布局替代 */

/* 主题Element Plus组件样式覆盖 */
.main-content .el-input__wrapper {
  background-color: var(--bg-tertiary) !important;
  border-color: var(--border-color) !important;
  box-shadow: 0 0 0 1px var(--border-color) inset !important;
}
.main-content .el-input__inner {
  color: var(--text-primary) !important;
}
.main-content .el-input__inner::placeholder {
  color: var(--text-secondary) !important;
}

/* 这些旧的textarea样式已被新的统一输入框设计替代 */
.main-content .el-button {
  background-color: var(--bg-tertiary) !important;
  border-color: var(--border-color) !important;
  color: var(--text-primary) !important;
}
.main-content .el-button:hover {
  background-color: var(--bg-quaternary) !important;
  border-color: var(--text-accent) !important;
}
.main-content .el-button--primary {
  background-color: var(--text-accent) !important;
  border-color: var(--text-accent) !important;
  color: var(--button-hover) !important;
}
.main-content .el-button--primary:hover {
  background-color: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
}
.main-content .el-button--danger {
  background-color: var(--text-danger) !important;
  border-color: var(--text-danger) !important;
}
.main-content .el-button--danger:hover {
  background-color: var(--text-danger-hover) !important;
  border-color: var(--text-danger-hover) !important;
}
.main-content .el-link {
  color: var(--text-accent) !important;
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
  min-height: 300px !important;
  overflow: hidden !important;
  background: var(--bg-primary) !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

/* 小窗口自适应 */
@media (max-height: 700px) {
  .unified-input-box {
    height: 200px !important;
    min-height: 100px !important;
    max-width: 1000px !important;
  }
  
  .content-header {
    padding: 8px 20px !important;
  }
  
  .app-title {
    font-size: 16px !important;
  }
  
  .chat-container {
    padding: 10px 20px !important;
    min-height: 120px !important;
  }
  
  .input-section {
    padding: 10px 20px 6px 20px !important;
  }
}

@media (max-height: 600px) {
  .unified-input-box {
    height: 160px !important;
    min-height: 80px !important;
    max-width: 1000px !important;
  }
  
  .text-input-area {
    padding: 20px 25px 15px 25px !important;
  }
  
  .button-area {
    height: 60px !important;
    padding: 10px 25px !important;
  }
  
  .content-header {
    padding: 6px 20px !important;
  }
  
  .app-title {
    font-size: 14px !important;
  }
  
  .chat-container {
    padding: 8px 20px !important;
    min-height: 120px !important;
  }
  
  .input-section {
    padding: 8px 20px 4px 20px !important;
  }
}
.main-content .el-link:hover {
  color: var(--accent-hover) !important;
}
.history-panel .el-link {
  color: var(--text-primary) !important;
}
.history-panel .el-link:hover {
  color: var(--text-accent) !important;
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
  background-color: var(--bg-tertiary) !important;
  border-color: var(--border-color) !important;
  color: var(--text-danger) !important;
  border-radius: 8px !important;
  width: 28px !important;
  height: 28px !important;
  padding: 0 !important;
  box-shadow: 0 2px 8px var(--shadow-color) !important;
  transition: all 0.25s ease !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 16px !important;
  font-weight: bold !important;
  line-height: 1 !important;
}

.history-panel .el-button--danger.delete-btn:hover {
  background-color: var(--text-danger) !important;
  border-color: var(--text-danger) !important;
  color: #ffffff !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px var(--shadow-color) !important;
}

/* 亮色主题下的删除按钮边框 */
[data-theme="light"] .history-panel .el-button--danger.delete-btn {
  border: 2px solid var(--border-color) !important;
}

[data-theme="light"] .history-panel .el-button--danger.delete-btn:hover {
  border-color: var(--text-danger) !important;
}

/* 全局下拉菜单暗色主题 - 修复白色背景问题 */
.el-popper {
  background: var(--accent-shadow-light) !important;
  border-radius: 14px !important;
  padding: 2px !important;
}

[data-theme="light"] .el-popper {
  background: var(--accent-shadow-light) !important;
}

.el-popper .el-popper__arrow {
  display: none !important;
}

.el-dropdown-menu {
  background-color: var(--bg-secondary) !important;
  border: 2px solid var(--border-color) !important;
  border-radius: 12px !important;
  box-shadow: 0 12px 48px var(--shadow-color) !important;
  padding: 8px 0 !important;
  margin: 0 !important;
  outline: none !important;
}

.el-dropdown-menu .el-dropdown-menu__item {
  color: var(--text-primary) !important;
  background-color: transparent !important;
  padding: 12px 20px !important;
  font-size: 15px !important;
  transition: all 0.25s ease !important;
  border-radius: 0 !important;
}

.el-dropdown-menu .el-dropdown-menu__item:hover {
  background-color: var(--bg-tertiary) !important;
  color: var(--text-accent) !important;
  border-left: 3px solid var(--text-accent) !important;
}

.el-dropdown-menu .el-dropdown-menu__item:focus {
  background-color: var(--bg-tertiary) !important;
  color: var(--text-accent) !important;
  border-left: 3px solid var(--text-accent) !important;
}

.el-dropdown-menu .el-dropdown-menu__item--divided {
  border-top: 1px solid var(--border-color) !important;
}

/* 特别针对指令选择下拉菜单 */
.el-dropdown__popper {
  background: var(--accent-shadow-light) !important;
  border: none !important;
  box-shadow: none !important;
  padding: 2px !important;
  border-radius: 14px !important;
}

[data-theme="light"] .el-dropdown__popper {
  background: var(--accent-shadow-light) !important;
}

.el-dropdown__popper .el-dropdown-menu {
  background-color: var(--bg-secondary) !important;
  border: 2px solid var(--border-color) !important;
  border-radius: 12px !important;
  box-shadow: 0 12px 48px var(--shadow-color), inset 0 0 0 1px var(--border-color) !important;
  margin: 0 !important;
  position: relative !important;
  z-index: 9999 !important;
}

/* 强制边框显示 */
.el-dropdown-menu,
.el-dropdown__popper .el-dropdown-menu {
  box-sizing: border-box !important;
  border-style: solid !important;
  border-width: 2px !important;
  border-color: var(--border-color) !important;
}

/* 主内容区域模式样式 */
.main-content.welcome-mode {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.main-content.chat-mode {
  display: flex;
  flex-direction: column;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 平滑变换动画 */
.smooth-transform-enter-active {
  transition: opacity 0.1s ease;
}

.smooth-transform-leave-active {
  transition: opacity 0.1s ease;
}

.smooth-transform-enter-from,
.smooth-transform-leave-to {
  opacity: 0;
}

.smooth-transform-enter-to,
.smooth-transform-leave-from {
  opacity: 1;
}

/* 动画目标元素样式 */
.animate-target {
  transition: all 0.3s ease;
}

/* 确保动画期间元素正确显示 */
.main-content {
  overflow: visible !important;
}

.welcome-content-wrapper,
.chat-content-wrapper {
  overflow: visible !important;
}

/* 动画期间防止页面滚动 */
body.animating {
  overflow: hidden !important;
}

/* 动画元素基础样式 */
.animation-element {
  position: fixed !important;
  z-index: 10000 !important;
  pointer-events: none !important;
  will-change: transform, opacity !important;
  backface-visibility: hidden !important;
  transform-style: preserve-3d !important;
  contain: layout style paint !important;
}

/* 动画期间优化渲染性能 */
.main-content.welcome-mode .animate-target,
.main-content.chat-mode .animate-target {
  will-change: transform, opacity;
  backface-visibility: hidden;
}

/* 动画完成后恢复正常 */
.main-content:not(.welcome-mode):not(.chat-mode) .animate-target {
  will-change: auto;
}

/* 欢迎内容包装器 */
.welcome-content-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  box-sizing: border-box;
  min-height: 100vh;
  position: relative;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  overflow-y: auto;
}

/* 欢迎模式下的主内容区域适配 */
.main-content.welcome-mode {
  overflow: hidden;
}

/* 欢迎模式特殊背景效果 */
.welcome-content-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(ellipse at center, var(--accent-shadow-light) 0%, transparent 70%);
}

[data-theme="light"] .welcome-content-wrapper::before {
  background: radial-gradient(ellipse at center, var(--accent-shadow-light) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* 聊天内容包装器 */
.chat-content-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.welcome-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  max-width: 1000px;
  width: 100%;
  position: relative;
  z-index: 1;
}

.welcome-title {
  font-size: 48px;
  font-weight: 700;
  color: var(--text-accent);
  text-align: center;
  margin: 0;
  letter-spacing: 2px;
  text-shadow: 0 4px 20px var(--accent-shadow-light);
  animation: welcomeTitleGlow 3s ease-in-out infinite alternate;
}

@keyframes welcomeTitleGlow {
  from {
    text-shadow: 0 4px 20px var(--accent-shadow-light);
  }
  to {
    text-shadow: 0 8px 32px var(--accent-shadow-strong);
  }
}

.welcome-ai-message {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin: 20px 0;
}

.welcome-ai-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  border: 3px solid var(--bg-quaternary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-accent);
  font-weight: bold;
  font-size: 18px;
  box-shadow: 0 6px 24px var(--shadow-color);
  animation: welcomeAvatarPulse 2s ease-in-out infinite alternate;
}

@keyframes welcomeAvatarPulse {
  from {
    box-shadow: 0 6px 24px var(--shadow-color);
  }
  to {
    box-shadow: 0 8px 32px var(--accent-shadow);
  }
}

.welcome-ai-bubble {
  position: relative;
  background: var(--bg-secondary);
  border: 2px solid var(--bg-tertiary);
  color: var(--text-primary);
  border-radius: 24px;
  border-bottom-left-radius: 8px;
  box-shadow: 0 8px 32px var(--shadow-color);
  max-width: 400px;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.welcome-bubble-content {
  padding: 20px 24px;
  line-height: 1.6;
}

.welcome-message-text {
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 500;
  margin: 0;
}

.welcome-bubble-tail {
  position: absolute;
  bottom: 0;
  left: -14px;
  width: 0;
  height: 0;
}

.welcome-bubble-tail::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 0;
  border-right: 18px solid var(--bg-tertiary);
  border-bottom: 18px solid transparent;
}

.welcome-bubble-tail::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 2px;
  width: 0;
  height: 0;
  border-right: 16px solid var(--bg-secondary);
  border-bottom: 16px solid transparent;
}

.welcome-input-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
  max-width: 1000px;
}

.welcome-login-notice {
  color: var(--text-warning);
  text-align: center;
  font-size: 16px;
  font-weight: 500;
}

.welcome-pending-files-area {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  max-width: 100%;
}

.welcome-pending-file-item {
  background: var(--bg-tertiary);
  border-radius: 8px;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 2px solid var(--border-color);
  transition: all 0.3s ease;
  min-width: 200px;
  max-width: 300px;
}

.welcome-pending-file-item:hover {
  background: var(--bg-secondary);
  border-color: var(--text-accent);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--shadow-color);
}

.welcome-pending-delete-btn {
  background: transparent !important;
  border: none !important;
  color: var(--text-danger) !important;
  font-size: 18px !important;
  font-weight: bold !important;
  width: 24px !important;
  height: 24px !important;
  padding: 0 !important;
  border-radius: 50% !important;
  transition: all 0.3s ease !important;
}

.welcome-pending-delete-btn:hover {
  background: var(--text-danger) !important;
  color: #ffffff !important;
  transform: scale(1.2) !important;
}

.welcome-mode-indicator {
  display: flex;
  align-items: center;
  background: var(--bg-tertiary);
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 16px;
  color: var(--text-accent);
  border: 2px solid var(--border-color);
}

.welcome-unified-input-box {
  position: relative;
  width: 100%;
  max-width: 1000px;
  height: 320px;
  background: var(--bg-tertiary);
  border-radius: 48px;
  padding: 0;
  box-shadow: 0 16px 64px var(--shadow-color);
  border: 4px solid var(--border-color);
  transition: all 0.4s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.welcome-unified-input-box:focus-within {
  border-color: var(--text-accent);
  box-shadow: 0 20px 80px var(--accent-shadow);
  transform: translateY(-4px);
}

[data-theme="light"] .welcome-unified-input-box:focus-within {
  box-shadow: 0 20px 80px var(--accent-shadow);
}

.welcome-text-input-area {
  flex: 1;
  position: relative;
  padding: 40px 45px 25px 45px;
  background: var(--bg-tertiary);
}

.welcome-custom-textarea {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 18px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  resize: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--bg-quaternary) transparent;
}

.welcome-custom-textarea::placeholder {
  color: var(--text-secondary);
  font-size: 18px;
}

.welcome-char-count {
  position: absolute;
  bottom: 12px;
  right: 25px;
  color: var(--text-secondary);
  font-size: 14px;
  pointer-events: none;
}

.welcome-button-area {
  height: 80px;
  background: var(--bg-tertiary);
  padding: 18px 45px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: none;
}

.welcome-left-buttons {
  display: flex;
  align-items: center;
  gap: 18px;
}

.welcome-right-buttons {
  display: flex;
  align-items: center;
}

.welcome-box-button {
  border-radius: 28px !important;
  padding: 12px 24px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  background-color: var(--bg-secondary) !important;
  border-color: var(--bg-secondary) !important;
  color: var(--text-primary) !important;
  box-shadow: 0 4px 16px var(--shadow-color) !important;
  transition: all 0.3s ease !important;
  height: 48px !important;
}

.welcome-box-button:hover {
  background-color: var(--button-hover) !important;
  border-color: var(--text-accent) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 8px 24px var(--accent-shadow-light) !important;
}

[data-theme="light"] .welcome-box-button:hover {
  box-shadow: 0 8px 24px var(--accent-shadow-light) !important;
}

.welcome-send-box-button {
  border-radius: 28px !important;
  padding: 12px 36px !important;
  font-size: 18px !important;
  font-weight: 700 !important;
  background-color: var(--text-accent) !important;
  border-color: var(--text-accent) !important;
  color: var(--button-hover) !important;
  box-shadow: 0 6px 20px var(--accent-shadow-strong) !important;
  transition: all 0.3s ease !important;
  height: 48px !important;
  min-width: 120px !important;
}

.welcome-send-box-button:hover {
  background-color: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 10px 32px var(--accent-shadow-strong) !important;
}

[data-theme="light"] .welcome-send-box-button {
  box-shadow: 0 6px 20px var(--accent-shadow-strong) !important;
}

[data-theme="light"] .welcome-send-box-button:hover {
  box-shadow: 0 10px 32px var(--accent-shadow-strong) !important;
}

.welcome-ai-disclaimer {
  text-align: center;
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 8px;
  opacity: 0.8;
  font-weight: 400;
  letter-spacing: 0.5px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-title {
    font-size: 32px;
  }
  
  .welcome-content {
    gap: 30px;
    padding: 0 15px;
  }
  
  .welcome-unified-input-box {
    height: 280px;
  }
  
  .welcome-text-input-area {
    padding: 30px 25px 20px 25px;
  }
  
  .welcome-button-area {
    padding: 15px 25px;
    height: 70px;
  }
  
  .welcome-custom-textarea {
    font-size: 16px;
  }
  
  .welcome-content-wrapper {
    padding: 20px 15px;
  }
}

@media (max-height: 700px) {
  .welcome-content-wrapper {
    padding: 20px 15px;
    min-height: auto;
    justify-content: flex-start;
    padding-top: 60px;
  }
  
  .welcome-content {
    gap: 25px;
  }
  
  .welcome-title {
    font-size: 36px;
  }
  
  .welcome-unified-input-box {
    height: 240px;
  }
}

@media (max-height: 600px) {
  .welcome-content-wrapper {
    padding: 15px 10px;
    padding-top: 40px;
  }
  
  .welcome-content {
    gap: 20px;
  }
  
  .welcome-title {
    font-size: 28px;
  }
  
  .welcome-unified-input-box {
    height: 200px;
  }
  
  .welcome-text-input-area {
    padding: 20px 20px 15px 20px;
  }
  
  .welcome-button-area {
    padding: 10px 20px;
    height: 60px;
  }
}

.session-name {
  color: var(--text-primary) !important;
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.5px;
  transition: color 0.3s;
}

.session-rename-input .el-input__wrapper {
  background: var(--bg-tertiary) !important;
  border-color: var(--border-color) !important;
  color: var(--text-primary) !important;
  box-shadow: 0 0 0 1px var(--border-color) inset !important;
  border-radius: 8px !important;
  transition: all 0.3s ease !important;
}
.session-rename-input .el-input__inner {
  color: var(--text-primary) !important;
  background: transparent !important;
  font-size: 15px !important;
}
.session-rename-input .el-input__inner::placeholder {
  color: var(--text-secondary) !important;
}
.session-rename-input .el-input__wrapper:hover,
.session-rename-input .el-input__wrapper.is-focus {
  border-color: var(--text-accent) !important;
  box-shadow: 0 0 0 1px var(--text-accent) inset !important;
}
</style> 