# AI Skills 集合 v2.0

基于 reference.md 重构的 Claude Code 技能集合，实现**两层判断机制**和**9步专业写作流程**。

---

## 🏗️ 目录结构

```
.claude/skills/
├── README.md                 # 本文件 - 总索引
│
├── _system/                  # 🎯 核心系统
│   ├── router.md            # 工作区路由器（两层判断入口）
│   ├── task_classifier.md   # 任务类型判断器
│   ├── core_principles.md   # 核心原则约束（不可妥协）
│   └── think_aloud.md       # Think Aloud 透明化规则
│
├── _workspaces/              # 📝 工作区配置
│   ├── 公众号/
│   │   ├── config.md        # 工作区配置和规范
│   │   ├── workflow.md      # 9步写作流程
│   │   └── 选题指南.md       # 选题技巧和模板
│   ├── 视频/
│   │   └── config.md        # 视频创作配置
│   └── Prompt/
│       └── config.md        # Prompt优化配置
│
├── _tools/                   # 🔧 工具集
│   ├── knowledge_base.md    # 个人素材库管理
│   ├── content_analyzer.md  # 内容分析器
│   ├── translator.md        # 智能翻译器
│   └── code_assistant.md    # 编程助手
│
├── _writers/                 # ✍️ 写作工具
│   ├── ai_writer.md         # AI写作（轻量版，无需后端）
│   ├── writer.md            # GLM写作助手
│   └── workflow_lite.md     # 轻量版工作流
│
├── _guides/                  # 📚 使用指南
│   ├── 使用指南.md           # 详细使用说明
│   └── 素材库管理.md         # 素材库搭建指南
│
└── _backend/                 # ⚙️ 后端服务
    ├── glm_backend.py       # Python后端服务
    └── writer_api.md        # API写作助手
```

---

## 🚀 快速开始

### 最简单的方式
直接描述你的需求，系统会自动识别工作区和任务类型：

```
写一篇关于AI工具的公众号文章
做个3分钟的产品介绍视频
优化这个prompt
```

### 手动指定工作区
```
[公众号] 写一篇关于AI的文章
[视频] 做个产品介绍视频
[Prompt] 优化这个提示词
```

---

## 🎯 核心架构：两层判断机制

### 第一层：工作区判断
| 工作区 | 触发关键词 | 特点 |
|--------|-----------|------|
| 公众号 | 公众号、文章、写作 | 需要配图、SEO、三遍审校 |
| 视频 | 视频、脚本、剪辑 | 分镜头、时长控制 |
| Prompt | prompt、提示词 | 结构化、可复用 |
| 通用 | 其他任务 | 灵活处理 |

### 第二层：任务类型判断
| 类型 | 识别特征 | 执行流程 |
|------|---------|---------|
| A | 有完整brief | 完整9步流程 |
| B | 无brief只有需求 | 先创建brief再执行 |
| C | 修改已有文章 | 读取→理解→修改 |
| D | 审校/降AI味 | 三遍审校流程 |
| E | 快速咨询 | 直接回答 |

---

## ⭐ 核心原则（不可妥协）

详见 [_system/core_principles.md](_system/core_principles.md)

1. **绝不编造数据** - 没有来源不要写
2. **绝不使用过时信息** - 新产品必须先搜索
3. **绝不省略 Think Aloud** - 说明思考过程
4. **绝不跳过用户确认** - 重要决策等待确认
5. **绝不混淆"我"的身份** - 素材必须来自真实经历

---

## 📝 公众号写作9步流程

详见 [_workspaces/公众号/workflow.md](_workspaces/公众号/workflow.md)

```
Step 1: 理解需求 & 保存Brief
Step 2: 信息搜索与知识管理 ⭐
Step 3: 选题讨论 ⭐⭐ (必做)
Step 4: 创建协作文档
Step 5: 学习个人风格
Step 5.5: 使用个人素材库 ⭐⭐
Step 6: 等待测试数据
Step 7: 创作初稿
Step 7.5: 风格转换实验（可选）
Step 8: 三遍审校 ⭐⭐⭐ (降AI味核心)
Step 9: 文章配图
```

---

## 🔧 工具使用

### 素材库管理
```
[KB] 添加素材
类型：产品评价
内容：今天测试了Claude Code...
标签：Claude Code, 测试
```

```
[KB] 搜索素材
关键词：AI工具, 评价
时间范围：最近30天
```

### AI写作
```
[AI] 写文章
主题：[文章主题]
风格：[专业/轻松]
字数：[字数]
```

### 完整工作流
```
[Workflow] 开始写作流程
主题：[文章主题]
类型：公众号
目标字数：3000
```

---

## 💡 使用建议

1. **日常写作** → 使用 `_writers/ai_writer.md`（轻量版）
2. **正式发布** → 使用 `_workspaces/公众号/workflow.md`（9步流程）
3. **积累素材** → 使用 `_tools/knowledge_base.md`
4. **降AI味** → 参考 `_system/core_principles.md` 和三遍审校

---

## 📊 新旧结构对比

| 改进项 | 旧版 | 新版 |
|--------|------|------|
| 目录结构 | 26个平铺文件 | 6个分类目录 |
| 工作区判断 | 分散在多个文件 | 统一在 `_system/router.md` |
| 任务分类 | 无 | 新增 `task_classifier.md` |
| 核心原则 | 隐含在流程中 | 独立为 `core_principles.md` |
| Think Aloud | 无显式规则 | 新增 `think_aloud.md` |
| Step 7.5 | 缺失 | 已补充在 workflow.md |

---

## 🗑️ 清理旧文件

重构完成后，可以删除根目录下的旧文件（已迁移到子目录）：

```bash
# 确认新结构正常工作后执行
# rm workspace_detector.md 智能工作区.md 分区识别.md ...
```

---

## 📚 相关文档

- 设计理念：参考项目根目录的 `reference.md`
- 详细使用：[_guides/使用指南.md](_guides/使用指南.md)
- 素材库搭建：[_guides/素材库管理.md](_guides/素材库管理.md)
