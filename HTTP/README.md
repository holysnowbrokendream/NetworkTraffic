## 初次运行
1. 复制conda环境`conda env create -f environment.yml`
2. 激活新建的conda环境
3. 配置数据库（如下）
4. 运行 `python manage.py migrate` 进行迁移
5. 运行 `python manage.py runserver` 即可启动后端

## 初次运行时数据库问题
1. 首先，安装MySQL数据库
2. 登录用户 `mysql -u your_username -p`
tips: 若创建新用户，需给予权限
`GRANT ALL PRIVILEGES ON all_users.* TO 'your_username'@'localhost';`
`FLUSH PRIVILEGES;`
3. 按照如下命令创建表
`CREATE DATABASE all_users`
`  CHARACTER SET utf8mb4`
`  COLLATE utf8mb4_unicode_ci;`
4. 查看 MySQL 中 Django 使用的用户认证插件
`SELECT user, host, plugin, FROM mysql.user WHERE user='your_username';`
如果是 `caching_sha2_password` 但 Django 报错，可切换为兼容的：
`ALTER USER 'your_username'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';`
`FLUSH PRIVILEGES;`
5. 修改 backend/setting.py 内第83-84行的用户名以及密码
6. 运行 `python manage.py migrate` 进行迁移

## 运行
运行 `python manage.py runserver` 即可启动后端

