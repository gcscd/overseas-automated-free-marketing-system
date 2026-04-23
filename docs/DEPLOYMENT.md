# Hermes 海外全自动免费营销系统 - 部署指南

**需求名称**: hermes-overseas-marketing  
**更新日期**: 2026-04-23  
**版本**: 1.0

---

## 一、快速部署

### 方式一：Docker Compose 部署（推荐）

适合生产环境，一键部署所有服务。

```bash
# 1. 克隆项目
git clone <repository-url>
cd hermes-marketing-system

# 2. 一键启动
docker compose up -d --build
```

启动后会自动运行以下服务：
- **前端**：http://localhost:80
- **后端 API**：http://localhost:8080

### 方式二：本地开发部署

适合开发调试。

#### 1. 部署后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

#### 2. 部署前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:3000

---

## 二、服务器环境要求

### 最低配置
| 配置项 | 要求 |
|--------|------|
| 系统 | Ubuntu 20.04 LTS |
| CPU | 2 核 |
| 内存 | 2GB |
| 硬盘 | 20GB SSD |
| 带宽 | 5Mbps |

### 推荐配置
| 配置项 | 要求 |
|--------|------|
| 系统 | Ubuntu 22.04 LTS |
| CPU | 4 核 |
| 内存 | 4GB |
| 硬盘 | 40GB SSD |
| 带宽 | 10Mbps |

---

## 三、系统配置

### 1. 后端配置

编辑 `.env` 文件：

```bash
# 数据库
DATABASE_URL=sqlite+aiosqlite:///./data/hermes.db

# JWT 密钥（生产环境必须修改）
JWT_SECRET_KEY=your-secret-key-change-in-production

# AI 模型配置
DEFAULT_AI_MODEL=claude-3-5-sonnet
AI_API_BASE_URL=https://api.anthropic.com
```

### 2. AI 角色配置

编辑 `config/agent.yaml` 配置 AI 角色和调度参数。

---

## 四、启动验证

### 1. 检查服务状态

```bash
# 后端健康检查
curl http://localhost:8080/api/health

# 前端访问
curl http://localhost:3000
```

### 2. 登录系统

访问前端，使用默认账号登录：
- 用户名：`admin`
- 密码：`admin123`

**首次登录建议立即修改密码！**

---

## 四、运维管理

### 服务管理

```bash
# Docker 部署
docker compose ps              # 查看服务状态
docker compose logs -f         # 查看日志
docker compose down            # 停止服务
docker compose restart         # 重启服务

# 本地部署
pm2 start ecosystem.config.js  # 使用 PM2 管理进程
pm2 logs                        # 查看日志
pm2 restart all                 # 重启服务
```

### 数据备份

```bash
# 备份数据库
cp backend/data/hermes.db ./backup/hermes_$(date +%Y%m%d).db

# 备份配置文件
tar -czf backup/config_$(date +%Y%m%d).tar.gz backend/config backend/logs
```

### 日志查看

```bash
# 后端日志
tail -f backend/logs/hermes.log

# 前端日志
docker compose logs frontend

# 后端日志
docker compose logs backend
```

---

## 五、HTTPS 配置（可选）

### Let's Encrypt 免费证书

```bash
# 安装 Certbot
apt-get install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com
```

Nginx 会自动配置 HTTPS，证书会自动续期。

---

## 六、常见问题

### 1. 后端启动失败

**检查端口占用**：
```bash
lsof -i :8080
```

**检查依赖**：
```bash
cd backend
pip install -r requirements.txt
```

### 2. 前端页面空白

**检查 API 连通性**：
```bash
curl http://localhost:8080/api/health
```

**清除缓存**：
```bash
rm -rf dist
npm run build
```

### 3. 数据库错误

**重置数据库**：
```bash
rm backend/data/hermes.db
# 重启服务会自动创建
```

### 4. Docker 权限问题

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 七、生产环境优化

### 1. 性能优化

- 使用 Redis 缓存热点数据
- 配置 CDN 加速静态资源
- 启用 Gzip 压缩
- 调整 Nginx worker 进程数

### 2. 安全加固

- 修改默认 JWT 密钥
- 配置防火墙规则
- 启用 Fail2ban 防止暴力破解
- 定期更新系统依赖

### 3. 监控告警

- 配置 Prometheus 监控
- 接入 Grafana 可视化
- 设置异常告警通知

---

## 八、技术支持

如遇到问题，请检查：

1. 系统日志
2. Docker 容器状态
3. API 健康检查接口

官方文档：参考项目根目录 `.monkeycode/specs/` 下的设计文档。
