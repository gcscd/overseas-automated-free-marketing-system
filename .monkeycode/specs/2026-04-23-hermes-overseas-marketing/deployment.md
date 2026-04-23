# Hermes 海外全自动免费营销系统 - 部署与配置

**需求名称**: hermes-overseas-marketing  
**更新日期**: 2026-04-23  
**版本**: 1.0

本文档包含完整的部署配置、API 接口设计、前端页面设计等内容。

---

## 五、 API 接口设计

### 5.1 项目接口

| 接口 | 方法 | 描述 |
|------|------|------|
| /api/projects | GET | 获取项目列表 |
| /api/projects | POST | 创建新项目 |
| /api/projects/{id} | GET | 获取项目详情 |
| /api/projects/{id} | PUT | 更新项目 |
| /api/projects/{id}/status | PATCH | 更新项目状态 |
| /api/projects/{id} | DELETE | 删除项目 |
| /api/projects/{id}/tasks | GET | 获取项目任务列表 |
| /api/projects/{id}/stats | GET | 获取项目统计数据 |

### 5.2 AI 角色接口

| 接口 | 方法 | 描述 |
|------|------|------|
| /api/roles | GET | 获取角色列表 |
| /api/roles/{id} | GET | 获取角色详情 |
| /api/roles/{id}/current-task | GET | 获取当前任务 |
| /api/roles/{id}/history | GET | 获取历史任务 |

### 5.3 任务接口

| 接口 | 方法 | 描述 |
|------|------|------|
| /api/tasks | GET | 获取任务列表（支持过滤） |
| /api/tasks/{id} | GET | 获取任务详情 |
| /api/tasks/{id}/retry | POST | 重试任务 |
| /api/tasks/{id}/cancel | POST | 取消任务 |

### 5.4 数据接口

| 接口 | 方法 | 描述 |
|------|------|------|
| /api/stats/overview | GET | 获取总览数据 |
| /api/stats/trend | GET | 获取趋势数据 |
| /api/stats/channel | GET | 获取渠道数据 |
| /api/keywords/ranking | GET | 获取关键词排名 |
| /api/keywords/trend | GET | 获取关键词趋势 |

### 5.5 系统接口

| 接口 | 方法 | 描述 |
|------|------|------|
| /api/auth/login | POST | 用户登录 |
| /api/auth/logout | POST | 用户登出 |
| /api/system/config | GET | 获取系统配置 |
| /api/system/config | PUT | 更新系统配置 |
| /api/system/logs | GET | 获取系统日志 |

---

## 六、前端页面设计

### 6.1 页面结构

```
/                    # 首页/数据看板
/projects            # 项目管理列表
/projects/:id        # 项目详情页
/projects/create     # 创建项目
/roles               # AI 角色管理
/tasks               # 任务监控
/channels            # 渠道管理
/settings            # 系统设置
```

### 6.2 路由设计

```typescript
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { 
    path: '/', 
    name: 'Dashboard', 
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '数据看板' }
  },
  { 
    path: '/projects', 
    name: 'Projects', 
    component: () => import('@/views/ProjectList.vue'),
    meta: { title: '项目管理' }
  },
  { 
    path: '/projects/create', 
    name: 'CreateProject', 
    component: () => import('@/views/ProjectCreate.vue'),
    meta: { title: '创建项目' }
  },
  { 
    path: '/projects/:id', 
    name: 'ProjectDetail', 
    component: () => import('@/views/ProjectDetail.vue'),
    meta: { title: '项目详情' }
  },
  { 
    path: '/roles', 
    name: 'Roles', 
    component: () => import('@/views/RoleList.vue'),
    meta: { title: 'AI 角色' }
  },
  { 
    path: '/tasks', 
    name: 'Tasks', 
    component: () => import('@/views/TaskList.vue'),
    meta: { title: '任务监控' }
  },
  { 
    path: '/channels', 
    name: 'Channels', 
    component: () => import('@/views/ChannelList.vue'),
    meta: { title: '渠道管理' }
  },
  { 
    path: '/settings', 
    name: 'Settings', 
    component: () => import('@/views/Settings.vue'),
    meta: { title: '系统设置' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
```

### 6.3 组件结构

```
src/
├── components/
│   ├── common/
│   │   ├── PageHeader.vue
│   │   ├── DataTable.vue
│   │   └── StatusTag.vue
│   ├── project/
│   │   ├── ProjectCard.vue
│   │   ├── ProjectForm.vue
│   │   └── ProjectStats.vue
│   ├── role/
│   │   ├── RoleCard.vue
│   │   └── RoleStatus.vue
│   ├── task/
│   │   ├── TaskList.vue
│   │   ├── TaskItem.vue
│   │   └── TaskProgress.vue
│   └── chart/
│       ├── TrendChart.vue
│       ├── PieChart.vue
│       └── BarChart.vue
├── views/
│   ├── Dashboard.vue
│   ├── ProjectList.vue
│   ├── ProjectCreate.vue
│   ├── ProjectDetail.vue
│   ├── RoleList.vue
│   ├── TaskList.vue
│   ├── ChannelList.vue
│   └── Settings.vue
├── stores/
│   ├── project.ts
│   ├── role.ts
│   ├── task.ts
│   └── system.ts
└── api/
    ├── project.ts
    ├── role.ts
    ├── task.ts
    └── system.ts
```

---

## 七、部署配置

### 7.1 Docker Compose 配置

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: hermes-frontend
    ports:
      - "3000:80"
    volumes:
      - ./frontend/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend
    restart: always
    networks:
      - hermes-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: hermes-backend
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
    environment:
      - DATABASE_URL=sqlite+aiosqlite:////app/data/hermes.db
      - HERMES_AGENT_CONFIG=/app/config/agent.yaml
    restart: always
    networks:
      - hermes-network

  nginx:
    image: nginx:1.24-alpine
    container_name: hermes-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - backend
    restart: always
    networks:
      - hermes-network

volumes:
  data:
  logs:

networks:
  hermes-network:
    driver: bridge
```

### 7.2 前端 Dockerfile

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 7.3 后端 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 7.4 Nginx 配置

```nginx
server {
    listen 80;
    server_name _;

    # 前端静态资源
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 反向代理
    location /api/ {
        proxy_pass http://backend:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Hermes Agent
    location /agent/ {
        proxy_pass http://backend:8080/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 八、错误处理设计

### 8.1 统一错误响应格式

```typescript
interface ErrorResponse {
  code: string;
  message: string;
  detail?: any;
  timestamp: string;
  path: string;
}
```

### 8.2 错误码定义

| 错误码 | 说明 |
|-------|------|
| SUCCESS | 成功 |
| VALIDATION_ERROR | 参数校验失败 |
| NOT_FOUND | 资源不存在 |
| UNAUTHORIZED | 未授权 |
| FORBIDDEN | 禁止访问 |
| INTERNAL_ERROR | 服务器内部错误 |
| TASK_FAILED | 任务执行失败 |
| API_ERROR | 第三方 API 错误 |

### 8.3 重试机制

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    reraise=True
)
async def call_ai_api(prompt: str):
    # AI 调用逻辑
    pass
```

---

## 九、安全性设计

### 9.1 认证授权

- 使用 JWT 进行用户认证
- Token 有效期 24 小时
- 支持 Refresh Token 续期
- 所有 API 接口需要 Authentication Header

### 9.2 数据加密

- 用户密码使用 bcrypt 加密存储
- API Key、Secret等敏感信息加密存储
- 数据库文件加密（可选）

### 9.3 输入校验

- 所有用户输入使用 Pydantic 进行校验
- 防止 SQL 注入
- 防止 XSS 攻击
- 文件大小和类型限制

### 9.4 日志审计

- 记录所有用户操作日志
- 记录系统异常日志
- 记录 API 调用日志
- 日志保留 90 天

---

## 十、测试策略

### 10.1 单元测试

- 后端 API 接口测试（pytest）
- 前端组件测试（Vitest）
- 工具函数测试
- 覆盖率目标：80%+

### 10.2 集成测试

- 数据库集成测试
- AI 调用集成测试
- 第三方 API 集成测试

### 10.3 E2E 测试

- 核心业务流程测试（Playwright）
- 关键页面交互测试

### 10.4 性能测试

- API 响应时间测试
- 并发请求测试
- 压力测试

---

## 十一、验收标准检查清单

### 11.1 功能验收

- [ ] 所有 P0/P1 级功能 100% 实现
- [ ] 核心自动化闭环完整
- [ ] 所有页面交互正常
- [ ] 第三方 API 对接正常
- [ ] AI 角色正常执行任务
- [ ] 关键词监控、代理管理正常

### 11.2 性能验收

- [ ] 前端首屏加载≤2s
- [ ] API 响应≤500ms
- [ ] 连续运行 72 小时无崩溃
- [ ] 同时运行 5 个项目、10 个并行任务稳定
- [ ] AI 内容生成成功率≥95%

### 11.3 部署验收

- [ ] Shell 脚本在全新 Ubuntu 22.04 正常执行
- [ ] Docker Compose 部署正常，数据持久化
- [ ] 服务器重启后服务自动恢复
- [ ] 部署文档清晰完整
- [ ] HTTPS 证书可正常配置

---

## 十二、交付物清单

1. [x] 系统完整前端源码
2. [x] Hermes Agent 后端定制化代码
3. [ ] 一键部署 Shell 脚本 install.sh
4. [ ] Docker Compose 配置文件
5. [ ] Nginx 配置模板
6. [x] 数据库设计文档
7. [ ] 系统部署与使用说明书
8. [ ] 系统运维与常见问题排查手册

---

**文档结束**

本文档与以下文档配合使用：
- `design.md` - 主设计文档
- `ai-roles.md` - AI 角色设计分册
- `deployment.md` - 部署与配置（本文档）
