# 🌐 NetworkTraffic 项目说明文档

---

## 项目结构概览

| 目录       | 说明 |
|------------|------|
| `Model/`   | 大模型微调相关代码 |
| `UI/`      | 前端页面（Vue 项目） |
| `HTTP/`    | 后端服务代码（Django / Python） |

---

## Model 模块

- **用途**：用于大语言模型的微调与训练  
- **技术栈**：Python, Transformers, HuggingFace, PyTorch 等  
- **备注**：请根据具体任务配置训练环境

---

## UI 模块（前端）

- **技术栈**：Vue.js + Vite（无须安装 Vue CLI）  
- **依赖管理**：npm（nodejs v22）

### ✅ 快速启动

```bash
cd UI
npm install     # 安装依赖
npm run dev     # 启动开发服务器
```

> 📝 详细说明请参考：`UI/README.md`

---

## HTTP 模块（后端）

- **技术栈**：Python + Django + DRF（Django REST Framework）  
- **数据库支持**：SQLite（Django内置数据库）

### ▶️ 启动服务
```bash
python manage.py runserver
```

> 📝 Django 具体配置详见：`HTTP/README.md`

---

如有任何问题，欢迎联系项目维护者 👨‍💻👩‍💻

