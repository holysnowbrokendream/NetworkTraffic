# 🚀 后端运行指南

---

## 初次运行步骤

请按顺序执行以下操作以完成项目初始化与启动：

1. **创建并激活 Python 环境**
    使用 Conda：
    ```bash
    conda env create -f environment.yml
    conda activate NWT
    ```

    使用 pip：
    ```bash
    cd HTTP
    python -m venv venv
    source venv/bin/activate    # Linux/macOS
    # 或
    venv\Scripts\activate       # Windows

    pip install -r requirements.txt
    ```

2. **配置数据库（见下文详细说明）**

3. **执行数据库迁移**
    ```bash
    python manage.py migrate
    ```

3. **启动 Django 开发服务器**
    ```bash
    python manage.py runserver
    ```

> tip: 成功后访问 `http://localhost:8000` 查看 API 接口或前端对接结果。

---

## 数据库配置说明

本项目使用 **SQLite** 作为默认数据库，这是Django内置的轻量级数据库，无需额外配置。

### 优势：
- ✅ 无需安装额外数据库服务
- ✅ 零配置，开箱即用
- ✅ 数据存储在 `db.sqlite3` 文件中
- ✅ 适合开发和测试环境

### 数据库文件位置：
```
HTTP/db.sqlite3
```

---

## 启动后端服务

一切准备就绪后，运行开发服务器：

```bash
python manage.py runserver
```

---

## 📌 常见问题参考

| 问题 | 解决方案 |
|------|----------|
| `no such table` | 执行 `python manage.py migrate` 创建数据库表 |
| `database is locked` | 确保没有其他进程正在使用数据库文件 |
| `permission denied` | 检查数据库文件权限，确保可读写 |

---

## 📦 项目依赖一览

如需查看或重建环境，请参考以下文件：

- `requirements.txt`：标准 Python 依赖文件（适用于 `venv`）
- `environment.yml`：Conda 环境配置文件（跨平台通用优化版）
