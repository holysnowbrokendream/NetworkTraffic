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

4. **启动 Django 开发服务器**
    ```bash
    python manage.py runserver
    ```

> tip: 成功后访问 `http://localhost:8000` 查看 API 接口或前端对接结果。

---

## 数据库配置指南（MySQL）

本项目使用 MySQL 作为默认数据库，请按照以下步骤完成配置。

1. **安装 MySQL**

    确保你已安装并启动了 MySQL 服务。

2. **登录 MySQL**

    ```bash
    mysql -u your_username -p
    ```

    💡 提示：如果你需要创建新用户，请使用如下语句：

    ```sql
    CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
    ```

    并为其授予数据库权限：

    ```sql
    GRANT ALL PRIVILEGES ON your_database.* TO 'your_username'@'localhost';
    FLUSH PRIVILEGES;
    ```

3. **创建数据库**

    ```sql
    CREATE DATABASE your_database
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
    ```

4. **检查用户认证插件（错误排查）**

    运行以下 SQL 查询当前用户的认证方式：

    ```sql
    SELECT user, host, plugin FROM mysql.user WHERE user='your_username';
    ```

    如果返回的 `plugin` 是 `caching_sha2_password`，而 Django 报错连接失败，请改为兼容模式：

    ```sql
    ALTER USER 'your_username'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
    FLUSH PRIVILEGES;
    ```

5. **修改 Django 配置文件**

    打开 `backend/settings.py` 文件，找到如下内容，修改为你的 MySQL 用户名和密码：

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database',     # 修改为自己的数据库名称
            'USER': 'your_username',     # 修改为自己的用户名
            'PASSWORD': 'your_password', # 修改为自己的密码
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

6. **执行数据库迁移**

    ```bash
    python manage.py migrate
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
| `Access denied for user` | 检查用户名、密码是否正确，确认权限是否授予 |
| `Authentication plugin 'caching_sha2_password' cannot be loaded` | 使用 `ALTER USER ... IDENTIFIED WITH mysql_native_password` 更换认证方式 |
| `Database does not exist` | 确保已执行 `CREATE DATABASE` 并且名称一致 |

---

## 📦 项目依赖一览

如需查看或重建环境，请参考以下文件：

- `requirements.txt`：标准 Python 依赖文件（适用于 `venv`）
- `environment.yml`：Conda 环境配置文件（跨平台通用优化版）
