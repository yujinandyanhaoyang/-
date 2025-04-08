# 研友集 - 学习协作平台
+ [![Test Coverage](https://img.shields.io/codecov/c/github/yujinandyanhaoyang/研友集)](https://codecov.io/gh/yujinandyanhaoyang/研友集)
+ [![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

一个基于Django构建的在线学习协作平台，帮助用户组建学习小组、共享资源并管理学习任务。
## 主要功能

- 🧑💼 用户认证系统（注册/登录/权限管理）
- 👥 学习小组创建与管理
- 📁 学习资源上传与共享（PDF/文档/课件）
- ✅ 任务管理系统（任务创建/状态跟踪）
- 💬 学习交流讨论区

## 技术栈

- 后端框架: Django 4.2
- 数据库: SQLite（默认）/ 支持MySQL/PostgreSQL
- 前端: HTML5 + Bootstrap
- 部署: WSGI (兼容Apache/Nginx)
- 文件存储: 本地文件系统（可扩展至云存储）

## 安装指南
```
### 环境要求
- Python 3.8+
- pip 20+

### 快速启动

# 克隆仓库
git clone https://github.com/yujinandyanhaoyang/study-buddy-platform.git

# 进入项目目录
cd study-buddy-platform

# 安装依赖
pip install -r requirements.txt

# 应用数据库迁移
python manage.py migrate

# 创建管理员用户（按提示输入信息）
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```



## 配置说明

在settings.py中，你可以配置以下关键参数：
数据库配置：
```bash
DATABASES = {
    'default': {
        # 使用SQLite（默认）
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 如需使用MySQL：
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'mydatabase',
        # 'USER': 'root',
        # 'PASSWORD': 'mypassword',
        # 'HOST': 'localhost',
        # 'PORT': '3306',
    }
}
```

## 贡献指南
```
Fork 本仓库
创建特性分支 (git checkout -b feature/新功能)
提交修改 (git commit -am '添加新功能')
推送分支 (git push origin feature/新功能)
创建Pull Request
```
