# 我用 Claude Code 写代码，效率提升了 3 倍

---

## 问题的开始

用 Claude Code 写代码有一段时间了，但总觉得哪里不对劲。

**问题一**：让 AI 开发一个功能，他总是跑偏。你说"加个评论功能"，他可能直接开写，写到一半发现需求不清，又来问你，来回折腾。

**问题二**：你得守着它，担心它乱来。要么盯着屏幕看它每一步操作，要么就随便它写，结果全看运气。

**问题三**：每次新开对话，Claude 都忘了之前聊过什么。项目架构、技术选型、已完成功能……得重新解释一遍，Token 烧得心疼。

直到最近，我发现了两个插件：**Superpower 工作流** + **Claude mem 记忆系统**。

用了一周后，真实感受是：

- ✅ 一周交付了 1 个完整应用和 1 个 MVP（之前要 3-4 周）
- ✅ 需求确认好后，基本可以放心离开，让 Claude 自己执行
- ✅ Token 消耗明显降了 30-50%

今天重点讲讲这两套插件怎么安装、怎么用。

---

## 一、Superpower 工作流

### 什么是 Superpower？

简单说，它给 Claude Code 加了一套"正规军的开发流程"。

原本你让 Claude 写代码，它可能直接开干，写到一半发现需求不对，又来问你。

Superpower 的做法是：**先聊透需求 → 再写详细计划 → 最后按计划执行**。

这样就不会跑偏，你也可以放心离开。

### 三个核心命令

| 命令 | 用途 | 什么时候用 |
| --- | --- | --- |
| `/superpowers:brainstorming` | 头脑风暴，确认需求细节 | 功能刚开始时 |
| `/superpowers:writing-plans` | 编写详细任务清单 | 需求确认后 |
| `/superpowers:executing-plans` | 按任务逐个执行 | 计划确认后 |

### 怎么用？一个完整例子

假设你要给博客加个评论功能。

**第一步：头脑风暴**

在 Claude Code 里输入：

```
/superpowers:brainstorming 我想给博客添加评论功能
```

Claude 会开始问你问题：

- 评论是否需要登录？
  - 你回答：需要
- 是否支持回复和嵌套？
  - 你回答：支持，最多 2 层
- 是否需要审核机制？
  - 你回答：不需要
- 用什么存储方案？
  - 你回答：PostgreSQL

聊完后，Claude 会自动生成一份 PRD 文档，保存在 `./docs/plan/` 文件夹下。

**第二步：编写计划**

正常流程下，头脑风暴结束后会自动进入计划阶段。

如果中断了，可以手动输入：

```
/superpowers:writing-plans
```

Claude 会基于 PRD 生成详细任务清单，类似这样：

```
- [ ] Task 1: 创建 Comment 数据模型
- [ ] Task 2: 实现评论 CRUD API
- [ ] Task 3: 前端评论组件开发
- [ ] Task 4: 添加嵌套回复支持
- [ ] Task 5: 编写测试用例
```

每个任务都包含具体的实现代码和步骤说明。

**这一步你要仔细看，确认没问题再继续。**

**第三步：执行计划**

正常流程会问你是直接在当前会话执行，还是开多个 Subagent 并行执行。

确认后，Claude 会按顺序执行每个任务。每个任务都遵循：写测试 → 写实现 → 运行测试 → 代码审查 → 提交代码。

**这个时候你就可以离开去买杯咖啡了。**

如果中断了，可以输入：

```
/superpowers:executing-plans
```

继续执行。

### 为什么这套流程这么有效？

传统方式的问题：需求不清就开干，写到一半发现不对，来回折腾。

Superpower 的解法：**先把需求聊透，详细编排任务，再动手写代码**。

PRD 和计划文档就是"契约"，Claude 严格按照契约执行，不会跑偏。

你需要在头脑风暴和计划 Review 投入精力，确保方向正确。后续的执行阶段，给它足够权限，然后挂机就行。

### 安装 Superpower

在 Claude Code 里依次输入：

```bash
# 1. 添加插件市场
/plugin marketplace add obra/superpowers-marketplace

# 2. 安装 Superpower
/plugin install superpowers@superpowers-marketplace

# 3. 验证安装（看看有没有在列表里）
/plugin list
```

安装完成后，重启 Claude Code 即可。

### 计划文件在哪里？

默认保存在项目根目录的 `./docs/plan/` 文件夹下，每次头脑风暴和编写计划都会生成一个 markdown 文件。

任务结束后，Claude 会问你要不要删除。你也可以手动删除，不影响项目。

---

## 二、Claude mem 记忆插件

### 什么是 Claude mem？

它解决的是"跨会话记忆"问题。

你今天和 Claude 聊了一个小时，把项目架构、技术选型、已完成功能都讲清楚了。

第二天新开对话，Claude 又失忆了，你得重新解释一遍。这个过程消耗大量 Token。

Claude mem 会把你的对话生成语义化摘要，新会话开始时自动加载相关上下文。

### 怎么用？

安装好后，它是自动运行的，你不需要手动操作。

新会话开始时，Claude 会自动加载之前对话的摘要。你需要的时候，它会去获取更详细的历史记录。

它采用的是**三层渐进式披露**：

| 层级 | 内容 | 何时加载 |
| --- | --- | --- |
| 第1层 | 高度压缩的摘要索引 | 会话开始时自动加载 |
| 第2层 | 详细的历史叙述 | Claude 需要时按需获取 |
| 第3层 | 源代码和原始记录 | 深入查看时获取 |

这样既保证了上下文连贯，又不会一次性塞入太多 Token。

### 安装 Claude mem

在 Claude Code 里依次输入：

```bash
# 1. 添加插件市场
/plugin marketplace add thedotmack/claude-mem

# 2. 安装 Claude mem
/plugin install claude-mem

# 3. 重启 Claude Code
```

安装完成后重启，mem 会自动运行。

---

## 三、完整使用流程

结合这两个插件，我现在的使用流程是这样的：

**1. 新功能开始**

```
/superpowers:brainstorming 我要做一个XXX功能
```

和 Claude 聊透需求，生成 PRD。

**2. 生成执行计划**

正常流程会自动进入，或者手动输入：

```
/superpowers:writing-plans
```

仔细 Review 计划，确保没问题。

**3. 执行计划**

正常流程会自动进入，或者手动输入：

```
/superpowers:executing-plans
```

选择执行方式，然后就可以离开了。

**4. 第二天继续**

新开对话，Claude 会自动通过 mem 加载之前的上下文。

你可以直接问：

```
昨天那个评论功能写到哪了？
```

它会记得之前聊过的内容。

---

## 四、常见问题

**Q: Superpower 的命令太长，有简写吗？**

A: 暂时没有。你可以考虑配置 shell alias，或者直接复制粘贴。

**Q: 执行计划时 Claude 做错了怎么办？**

A: 一般不会偏离，因为它是按计划执行的。如果是想修改需求，可以执行：

```
/superpowers:writing-plans 评论功能改成支持上传图片
```

重新生成计划。

**Q: mem 会占用很多空间吗？**

A: 不会，它存的是语义化摘要，非常压缩。而且它用的是渐进式加载，不会一次性把所有历史都塞进上下文。

**Q: 这两个插件只适用于特定项目吗？**

A: 不是，它们是全局的，安装后在所有项目里都能用。

**Q: 两个插件必须一起用吗？**

A: 不是，你可以单独用 Superpower 或单独用 mem。但组合起来效果最好。

---

## 五、总结

这套组合的核心价值：

- **Superpower**：让 Claude 按流程干活，不会跑偏，你可以放心离开
- **Claude mem**：让 Claude 记住项目上下文，新会话不用重新解释

前期在头脑风暴和计划 Review 投入精力，后期就可以放心让 Claude 自己执行。

这就是效率提升的秘密。

---

**相关链接：**

- Superpower GitHub：https://github.com/obra/superpowers
- Claude mem GitHub：https://github.com/thedotmack/claude-mem
- Claude Code 官方文档：https://code.claude.com/docs

**P.S.** 这套配置目前只适用于 Claude Code 终端版/桌面版，VS Code 版暂不支持插件系统。如果你也在用 Claude Code 写代码，强烈推荐试试。
