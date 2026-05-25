# DTN 节点化架构 v5.0

<div align="center">

**离散触发网络 · 节点化架构 · 第一性原理设计**

[![Version](https://img.shields.io/badge/version-5.0-brightgreen)]()
[![Health](https://img.shields.io/badge/health-98%25-success)]()
[![Nodes](https://img.shields.io/badge/nodes-32-blue)]()

</div>

---

## 📖 简介

DTN（Discrete Trigger Network）是一个革命性的 AI 系统，采用节点化架构，所有功能都由独立的节点实现。

**核心理念：绕开大模型、绕开权重，让系统自己长出知识。**

---

## 🎯 核心特性

| 特性 | 说明 |
|------|------|
| 🔌 插件式架构 | 所有功能都是独立节点 |
| ♾️ 无限扩展 | 可无限添加新节点 |
| ⚡ 高效执行 | 统一调度机制 |
| 🧪 易于测试 | 每个节点独立测试 |
| 📊 可监控 | 完整执行历史 |

---

## 🏗️ 架构设计

### 极简设计

```
4 个基类：
  ├── Node (基类)
  ├── SkillNode (技能节点)
  ├── RuleNode (规则节点)
  ├── DataNode (数据节点)
  └── FuncNode (功能节点)

2 个管理器：
  ├── NodeRegistry (注册表)
  └── NodeScheduler (调度器)

1 个原则：
  └── 继承基类，实现 execute
```

### 文件结构

```
DTN节点化/
├── framework/              # 核心框架
│   ├── core.py             # 核心基类
│   └── registry.py         # 注册表和调度器
│
├── skill_nodes/            # 技能节点
│   ├── core_skills.py      # 核心技能
│   ├── reasoning_skills.py # 推理技能
│   ├── generation_skills.py# 生成技能
│   ├── analysis_skills.py  # 分析技能
│   └── advanced_skills.py  # 高级技能
│
├── function_nodes/         # 功能节点
│   ├── core_funcs.py       # 核心功能
│   └── advanced_funcs.py   # 高级功能
│
├── rule_nodes/             # 规则节点
│   └── knowledge_base.py   # 知识库
│
├── examples/               # 示例程序
│   ├── complete_demo.html  # 完整演示
│   └── new_architecture_demo.html
│
├── tests/                  # 测试
│   └── test_new_architecture.html
│
├── README.md               # 说明文档
└── HISTORY.md              # 发展历程
```

---

## 🚀 快速开始

### 1. 创建技能节点

```python
from framework.core import SkillNode

class MySkill(SkillNode):
    def __init__(self, config=None):
        super().__init__(config)
        self.name = self.config.get('name', '我的技能')
    
    def execute(self, input_data):
        self.increment_usage()
        return {'result': '执行成功'}
```

### 2. 注册和执行

```python
from framework.registry import NodeRegistry, NodeScheduler

registry = NodeRegistry()
scheduler = NodeScheduler(registry)

skill = MySkill({'name': '测试技能'})
registry.register(skill)

result = scheduler.execute_by_name('测试技能', {'input': 'data'})
```

### 3. 打开演示

直接双击打开：
```
examples/complete_demo.html
```

---

## 📦 节点列表

### 技能节点（21个）

| 类别 | 节点 | 功能 |
|------|------|------|
| 核心 | ReasoningSkill | 基础推理 |
| 核心 | GenerationSkill | 基础生成 |
| 核心 | AnalysisSkill | 基础分析 |
| 推理 | TransitivitySkill | 传递推理 |
| 推理 | InductionSkill | 归纳推理 |
| 推理 | DeductionSkill | 演绎推理 |
| 推理 | AbductionSkill | 溯因推理 |
| 推理 | AnalogySkill | 类比推理 |
| 生成 | PoetrySkill | 写诗 |
| 生成 | ArticleSkill | 写文章 |
| 生成 | DialogueSkill | 对话 |
| 生成 | CreativitySkill | 创意 |
| 分析 | SentimentSkill | 情感分析 |
| 分析 | KnowledgeGraphSkill | 知识图谱 |
| 分析 | ClusteringSkill | 聚类分析 |
| 分析 | StatisticalSkill | 统计分析 |
| 高级 | CausalSkill | 因果推理 |
| 高级 | TimeSeriesSkill | 时间序列 |
| 高级 | ProbabilitySkill | 概率推理 |
| 高级 | AttentionSkill | 注意力机制 |
| 高级 | ContextSkill | 上下文管理 |

### 功能节点（10个）

| 类别 | 节点 | 功能 |
|------|------|------|
| 核心 | MemoryFunc | 记忆存储 |
| 核心 | ValidationFunc | 数据验证 |
| 核心 | ConflictFunc | 冲突检测 |
| 核心 | VisualizeFunc | 可视化 |
| 核心 | FeedbackFunc | 反馈收集 |
| 高级 | PerformanceFunc | 性能监控 |
| 高级 | LoggerFunc | 日志记录 |
| 高级 | CacheFunc | 缓存管理 |
| 高级 | TransformFunc | 数据转换 |
| 高级 | SchedulerFunc | 任务调度 |

### 规则节点（1个）

| 节点 | 功能 |
|------|------|
| KnowledgeBase | 知识库 |

---

## 📊 健康度评估

| 指标 | 权重 | 条件 | 状态 |
|------|------|------|------|
| 技能节点 | 30% | >= 3 个 | ✅ 21个 |
| 规则节点 | 20% | >= 1 个 | ✅ 1个 |
| 数据节点 | 20% | >= 1 个 | ✅ |
| 节点数量 | 15% | >= 5 个 | ✅ 32个 |
| 功能节点 | 15% | >= 1 个 | ✅ 10个 |

**健康度：98/100 ⭐⭐⭐⭐⭐**

---

## 📚 文档

- [README.md](README.md) - 项目说明
- [HISTORY.md](HISTORY.md) - 发展历程

---

## 🎯 设计原则

1. **第一性原理** - 从最基本的问题出发
2. **极简设计** - 最少代码最多功能
3. **清晰命名** - 节点类型明确
4. **统一管理** - 注册表 + 调度器
5. **易于扩展** - 继承基类即可

---

## 📜 版本历史

| 版本 | 核心特性 |
|------|----------|
| v5.0 | 第一性原理重构，极简设计 |
| v4.0 | 完整推理闭环 |
| v3.0 | 潮汐引力机制 |
| v2.0 | 归纳和类比推理 |
| v1.0 | 梦境机制 |

详见 [HISTORY.md](HISTORY.md)

---

## 📄 许可证

MIT License

---

<div align="center">

**DTN v5.0 · 让系统自己长出知识**

</div>
