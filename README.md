# AI Recruitment System

基于 AI 的智能招聘管理系统。

## 技术栈

- **前端**: React 19 + TypeScript + Vite + Tailwind CSS v4 + shadcn/ui
- **后端**: Python FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy + Alembic

## 项目结构

```
ai-recruitment-system/
├── frontend/          # React 前端
│   ├── src/
│   │   ├── api/          # API 调用层
│   │   ├── components/   # UI 组件
│   │   ├── hooks/        # 自定义 Hooks
│   │   ├── layouts/      # 布局组件
│   │   ├── lib/          # 工具函数
│   │   ├── pages/        # 页面组件
│   │   └── types/        # TypeScript 类型
│   └── ...
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 配置与核心模块
│   │   ├── models/       # 数据库模型
│   │   ├── schemas/      # Pydantic 数据模型
│   │   └── services/     # 业务逻辑层
│   ├── alembic/          # 数据库迁移
│   └── tests/            # 测试
└── ...
```

## 快速开始

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 启动服务
uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## API 文档

启动后端后访问: http://localhost:8000/docs
