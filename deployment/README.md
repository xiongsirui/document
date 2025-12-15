# 微信公众号AI自动化写作系统 - 部署指南

## 目录
1. [系统要求](#系统要求)
2. [快速部署](#快速部署)
3. [详细配置](#详细配置)
4. [Docker部署](#docker部署)
5. [监控和维护](#监控和维护)
6. [常见问题](#常见问题)

## 系统要求

### 最低配置
- **CPU**: 4核心
- **内存**: 8GB RAM
- **存储**: 50GB 可用空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **CPU**: 8核心或更多
- **内存**: 16GB RAM或更多
- **存储**: 100GB SSD
- **网络**: 高速互联网连接

### 软件依赖
- **操作系统**: Ubuntu 20.04+ / CentOS 8+ / Windows 10+ / macOS 10.15+
- **Python**: 3.9或更高版本
- **Node.js**: 16.x或更高版本
- **MySQL**: 8.0或更高版本
- **Redis**: 6.0或更高版本
- **Docker**: 20.10或更高版本（可选）

## 快速部署

### 1. 克隆项目
```bash
git clone https://github.com/your-org/wechat-auto-writer.git
cd wechat-auto-writer
```

### 2. 环境配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

### 3. 使用Docker Compose一键部署
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 初始化数据库
```bash
# 进入Python容器
docker-compose exec python bash

# 运行数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 初始化基础数据
python scripts/init_data.py
```

### 5. 访问系统
- **API文档**: http://localhost:8000/docs
- **管理后台**: http://localhost:8000/admin
- **Web界面**: http://localhost:3000

## 详细配置

### 1. 环境变量配置 (.env)
```bash
# 应用配置
APP_NAME=WeChat AI Writer
APP_VERSION=1.0.0
DEBUG=False
SECRET_KEY=your-super-secret-key-here

# 数据库配置
DB_HOST=mysql
DB_PORT=3306
DB_NAME=wechat_writer
DB_USER=root
DB_PASSWORD=your-database-password

# Redis配置
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# API密钥
OPENAI_API_KEY=sk-your-openai-api-key
CLAUDE_API_KEY=your-claude-api-key
BAIDU_AI_API_KEY=your-baidu-api-key
BAIDU_AI_SECRET_KEY=your-baidu-secret-key

# 微信公众号配置
WECHAT_APP_ID=your-wechat-app-id
WECHAT_APP_SECRET=your-wechat-app-secret
WECHAT_TOKEN=your-wechat-token
WECHAT_AES_KEY=your-wechat-aes-key

# 外部API配置
WECHAT_INDEX_API_KEY=your-wechat-index-key
HOT_SEARCH_API_KEY=your-hot-search-key

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/var/log/wechat-writer/app.log

# 文件存储
UPLOAD_PATH=/app/uploads
MAX_UPLOAD_SIZE=10485760  # 10MB
```

### 2. 数据库初始化脚本 (scripts/init_db.sql)
```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS wechat_writer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE wechat_writer;

-- 公众号账号表
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    app_id VARCHAR(100) NOT NULL,
    app_secret VARCHAR(255) NOT NULL,
    token VARCHAR(100),
    aes_key VARCHAR(255),
    followers INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY (app_id)
);

-- 文章表
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT,
    summary TEXT,
    keywords JSON,
    status ENUM('draft', 'published', 'scheduled') DEFAULT 'draft',
    publish_time TIMESTAMP NULL,
    read_count INT DEFAULT 0,
    like_count INT DEFAULT 0,
    share_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- 选题表
CREATE TABLE IF NOT EXISTS topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    keywords JSON,
    heat_score INT DEFAULT 0,
    competition_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    audience_match INT DEFAULT 0,
    final_score INT DEFAULT 0,
    status ENUM('pending', 'selected', 'used') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_score (final_score DESC)
);

-- 任务表
CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    status ENUM('pending', 'running', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    parameters JSON,
    result JSON,
    error TEXT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL
);

-- 性能统计表
CREATE TABLE IF NOT EXISTS analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    date DATE NOT NULL,
    articles_published INT DEFAULT 0,
    total_reads INT DEFAULT 0,
    total_likes INT DEFAULT 0,
    total_shares INT DEFAULT 0,
    avg_read_time INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (account_id, date),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- 素材库表
CREATE TABLE IF NOT EXISTS materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('image', 'video', 'text', 'link') NOT NULL,
    title VARCHAR(255),
    content TEXT,
    file_path VARCHAR(500),
    tags JSON,
    usage_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Docker Compose配置 (docker-compose.yml)
```yaml
version: '3.8'

services:
  # Python后端服务
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=mysql
      - REDIS_HOST=redis
    depends_on:
      - mysql
      - redis
    volumes:
      - ./logs:/var/log/wechat-writer
      - ./uploads:/app/uploads
    restart: unless-stopped

  # Node.js前端服务
  web:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "3000:3000"
    depends_on:
      - api
    restart: unless-stopped

  # MySQL数据库
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./scripts/init_db.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  # Redis缓存
  redis:
    image: redis:6.2-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - api
      - web
    restart: unless-stopped

volumes:
  mysql_data:
  redis_data:
```

### 4. Nginx配置 (nginx/nginx.conf)
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    upstream web {
        server web:3000;
    }

    # HTTP重定向到HTTPS
    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS配置
    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL证书配置
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # 前端
        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API接口
        location /api/ {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 文件上传大小限制
        client_max_body_size 50M;
    }
}
```

## Docker部署

### 1. API服务Dockerfile (Dockerfile.api)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建日志目录
RUN mkdir -p /var/log/wechat-writer

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "integration.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Web服务Dockerfile (Dockerfile.web)
```dockerfile
FROM node:16-alpine

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 构建应用
RUN npm run build

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["npm", "start"]
```

### 3. Python依赖文件 (requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pymysql==1.1.0
redis==5.0.1
celery==5.3.4
jieba==0.42.1
openai==1.3.7
anthropic==0.7.8
requests==2.31.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
Pillow==10.1.0
schedule==1.2.0
sqlalchemy==2.0.23
alembic==1.12.1
```

## 监控和维护

### 1. 日志管理
```bash
# 查看API日志
docker-compose logs -f api

# 查看错误日志
tail -f logs/error.log

# 日志轮转配置
sudo nano /etc/logrotate.d/wechat-writer
```

### 2. 性能监控
```bash
# 安装监控工具
docker run -d \
  --name=grafana \
  -p 3001:3000 \
  grafana/grafana

docker run -d \
  --name=prometheus \
  -p 9090:9090 \
  prom/prometheus
```

### 3. 数据备份
```bash
#!/bin/bash
# 备份脚本 backup.sh

# 备份数据库
docker-compose exec mysql mysqldump \
  -u root -p$DB_PASSWORD \
  wechat_writer > backup/db_$(date +%Y%m%d).sql

# 备份文件
tar -czf backup/files_$(date +%Y%m%d).tar.gz uploads/

# 清理旧备份（保留30天）
find backup/ -type f -mtime +30 -delete
```

### 4. 定时任务
```bash
# 添加到crontab
crontab -e

# 每天凌晨2点备份
0 2 * * * /path/to/backup.sh

# 每小时检查服务状态
0 * * * * docker-compose ps | grep -q "Up" || docker-compose restart
```

## 常见问题

### 1. 服务无法启动
```bash
# 检查端口占用
netstat -tulpn | grep :8000

# 检查Docker服务
systemctl status docker

# 重建容器
docker-compose down
docker-compose up --force-recreate
```

### 2. 数据库连接失败
```bash
# 检查数据库服务
docker-compose logs mysql

# 测试连接
docker-compose exec mysql mysql -u root -p

# 重置密码
docker-compose exec mysql mysql \
  -u root -p \
  -e "ALTER USER 'root'@'%' IDENTIFIED BY 'newpassword';"
```

### 3. API请求失败
```bash
# 检查API服务日志
docker-compose logs api

# 测试API连通性
curl http://localhost:8000/

# 检查环境变量
docker-compose exec api env | grep API_KEY
```

### 4. 内存不足
```bash
# 监控内存使用
docker stats

# 增加swap空间
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 5. 磁盘空间不足
```bash
# 清理Docker镜像
docker system prune -a

# 清理日志
sudo journalctl --vacuum-time=7d

# 监控磁盘使用
df -h
```

## 性能优化建议

### 1. 数据库优化
```sql
-- 添加索引
CREATE INDEX idx_articles_status ON articles(status);
CREATE INDEX idx_articles_publish_time ON articles(publish_time);
CREATE INDEX idx_tasks_status ON tasks(status);

-- 优化查询
EXPLAIN SELECT * FROM articles WHERE status = 'published';
```

### 2. 缓存策略
```python
# Redis缓存热点数据
import redis

r = redis.Redis(host='redis', port=6379)

# 缓存选题分析结果
def cache_topic_analysis(topic, result):
    r.setex(f"topic:{topic}", 3600, json.dumps(result))
```

### 3. 异步任务
```python
# 使用Celery处理耗时任务
from celery import Celery

celery_app = Celery('writer')

@celery_app.task
def generate_article_async(topic):
    # 异步生成文章
    pass
```

## 安全配置

### 1. 防火墙设置
```bash
# 只开放必要端口
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 2. SSL证书配置
```bash
# 使用Let's Encrypt
sudo apt install certbot
sudo certbot --nginx -d your-domain.com
```

### 3. 访问控制
```python
# IP白名单
ALLOWED_IPS = ['192.168.1.0/24', '10.0.0.0/8']

# 速率限制
from slowapi import Limiter
limiter = Limiter(key_func=lambda: request.client.host)

@app.post("/api/v1/content/generate")
@limiter.limit("10/minute")
async def generate_content():
    pass
```

---

## 获取帮助

- **文档**: https://docs.your-domain.com
- **问题反馈**: https://github.com/your-org/wechat-auto-writer/issues
- **技术支持**: support@your-domain.com
- **社区讨论**: https://discord.gg/your-channel

## 更新日志

### v1.0.0 (2024-01-15)
- 初始版本发布
- 完整的自动化写作功能
- Docker部署支持
- API文档完成

### v1.1.0 (计划中)
- 视频号内容生成
- 多平台支持
- 移动端App
- 更多AI模型集成