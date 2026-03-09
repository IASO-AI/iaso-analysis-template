# IASO Clinic AI File Processor Project

## 项目概述

IASO Clinic 医疗诊所管理系统 - AI 文件智能处理扩展模块

## 变更历史

| Change ID | 标题 | 状态 | 创建时间 |
|-----------|------|------|----------|
| implement-ai-file-processor | 实现 AI 文件智能处理平台 | 提案中 | 2025-02-09 |

## 活跃变更

### implement-ai-file-processor

- **proposal.md**: 需求提案文档
- **design.md**: 架构设计文档
- **tasks.md**: 任务拆分文档

**任务列表**:
- T-001: 后端基础设施搭建
- T-002: Kimi AI 服务封装 (deps: T-001)
- T-003: 文件重命名异步任务实现 (deps: T-001, T-002)
- T-004: 完整性检测异步任务实现 (deps: T-001, T-002)
- T-005: 前端基础布局实现
- T-006: 文件重命名页面实现 (deps: T-005)
- T-007: 完整性检测页面实现 (deps: T-005)
- T-008: 任务列表页面实现 (deps: T-005)
- T-009: 集成测试与优化 (deps: T-003, T-004, T-006, T-007, T-008)

## 技术栈

- **前端**: React + TypeScript + Vite + TanStack Router + Tailwind CSS v4 + shadcn/ui
- **后端**: Django REST Framework + MySQL + Redis + Celery
- **AI 服务**: Kimi K2.5 API (Moonshot AI)
