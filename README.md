# Hermes 海外全自动免费营销系统

## 项目简介

Hermes 是一个基于 AI Agent 的海外全自动免费营销系统，通过组建 AI 虚拟团队，自动完成市场调研、内容创作、多渠道分发、数据监控与优化复盘，实现从 0 到 1 的全托管式营销。

## 技术栈

### 前端
- Vue 3.x + TypeScript
- Vite 5.x
- Element Plus 2.x
- ECharts 5.x
- Pinia 2.x
- Vue Router 4.x

### 后端
- Hermes Agent (核心 Agent 引擎)
- Python 3.11+
- FastAPI
- SQLite
- SQLAlchemy + Alembic
- APScheduler

## 快速开始

### 方式一：Docker Compose 部署

```bash
docker compose up -d --build
```

访问 http://localhost

### 方式二：本地开发

#### 前端
```bash
cd frontend
npm install
npm run dev
```

#### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 默认账号

- 用户名：admin
- 密码：admin123

## 项目结构

```
/
├── frontend/          # 前端项目
│   ├── src/
│   │   ├── api/      # API 接口
│   │   ├── views/    # 页面组件
│   │   ├── stores/   # 状态管理
│   │   └── utils/    # 工具函数
│   └── ...
├── backend/           # 后端项目
│   ├── app/
│   │   ├── api/      # API 路由
│   │   ├── models/   # 数据模型
│   │   ├── schemas/  # Pydantic Schemas
│   │   └── core/     # 核心配置
│   └── ...
└── docker-compose.yml
```

## 文档

- [设计文档](.monkeycode/specs/2026-04-23-hermes-overseas-marketing/design.md)
- [AI 角色设计](.monkeycode/specs/2026-04-23-hermes-overseas-marketing/ai-roles.md)
- [部署文档](.monkeycode/specs/2026-04-23-hermes-overseas-marketing/deployment.md)

## License

MIT
