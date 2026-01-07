# 拆解 Claude Code 的"记忆系统"：Anthropic 官方的 Context Engineering 方法论

---

### 一、Prompt Engineering 不够用了

上周我用 Claude Code 重构一个项目，连续对话了两个小时。

前半小时它表现完美，理解架构、遵守约定、代码风格统一。但到后面，它开始"忘事"了——明明前面讨论过的命名规范，它又用回了旧的；之前决定好的目录结构，它写着写着就变了。

我一度以为是自己 prompt 写得不好，反复调整措辞。后来才意识到：问题不在 prompt，在上下文管理。

这不是个例。

微软和 Salesforce 的一项研究发现：**仅仅一轮对话之后，模型准确率就可能下降近 40%**。

问题出在哪？不是模型不行，是上下文管理不行。

2025 年 6 月，Shopify CEO Tobi Lütke 发了一条推文，直接点破了这件事：

> "我更喜欢 Context Engineering 这个词，而不是 Prompt Engineering。它更准确地描述了核心技能：**提供足够的上下文，让任务对 LLM 来说是可解的**。"

三个月后，Anthropic 在官方博客正式定义了这个概念，并发布了一系列工程实践指南。

今天这篇文章，我想把 Anthropic 工程师的这套方法论拆解清楚。

---

### 二、什么是 Context Engineering？

先给个一句话定义：

**Context Engineering = 在 LLM 推理过程中，策划和维护最优 token 集合的策略**

听起来有点抽象，打个比方：

- **Prompt Engineering** 是"如何和 AI 说话"
- **Context Engineering** 是"如何教 AI 思考"

两者的关系是：Prompt Engineering 是 Context Engineering 的一个子集。

Andrej Karpathy（OpenAI 创始成员、Tesla AI 负责人）有个很精辟的类比：

> "LLM 就像一个新型操作系统。模型本身是 CPU，上下文窗口就是 RAM。就像操作系统要管理什么数据放进 RAM，我们也需要'上下文工程'来管理什么信息放进上下文窗口。"

这个类比一下子说清楚了为什么 Prompt Engineering 不够用——你不能只优化一条指令，得管理整个"内存系统"。

说白了，Prompt Engineering 是在优化单个 SQL 语句，Context Engineering 是在设计整个数据库架构。

---

### 三、为什么 2025 年突然火了？

Context Engineering 其实不是什么新概念，但 2025 年突然成了热词。我觉得有三个原因：

**1. Agent 时代来了**

LangChain 2025 年报告显示：**57% 的组织已经有 AI Agent 在生产环境运行**。

但同时，**32% 的组织认为"质量"是最大障碍**——而且大多数失败不是模型问题，是上下文管理问题。

**2. 对话变长了**

早期的 ChatGPT 使用场景是单轮问答。现在 Claude Code 一个任务可能跑几十上百轮对话，涉及读文件、写代码、调工具、debug……

单轮优化的 Prompt Engineering 思维，应付不了这种复杂度。

**3. 终于有人把方法论整理清楚了**

Anthropic 在 2025 年 9 月发布了《Effective Context Engineering for AI Agents》，把零散的实践经验系统化了。

这感觉就像从"凭感觉写 SQL"进化到"有了数据库范式理论"——行业终于有了可复用的方法论，而不是各家各玩各的。

---

### 四、四大核心策略

LangChain 把 Context Engineering 归纳为四个核心策略，Anthropic 的实践也基本围绕这四个方向。我按实用程度排个序：

#### 1. Write（写入）：别什么都往脑子里塞

LLM 生成的内容是"瞬时"的，不存下来就丢了。所以要把重要信息写到外部存储（文件、数据库、scratchpad）。

**Claude Code 怎么做的**：
- 长文本分析时，先把完整文章存到磁盘
- 上下文里只保留引用或摘要
- 需要时再读取相关部分

有个叫 **Scratchpad** 的技巧很实用：给模型一个"草稿区"，专门存放中间结果。这些中间值不会污染主对话，也不会因为上下文裁剪而丢失。

#### 2. Select（选择）：信息不是越多越好

上下文窗口有限，什么都塞进去会"信息过载"。所以要建立检索机制，按需拉取。

**怎么判断该拉什么？三个维度**：
- **相关性**：这条信息和当前任务有多相关？
- **时效性**：新信息通常比旧信息重要
- **重要性**：过滤掉低价值噪音

举个例子：Claude Code 在做研究任务时，不会把所有搜索结果都塞进上下文。它会先存储，需要综合分析时再选择性拉取最相关的内容。

#### 3. Compress（压缩）：该扔就扔

对话越长，上下文越臃肿，很多是重复或过时的信息。解决方案是智能压缩，用摘要替代原文。

**Claude Code 的 Compaction 机制**

这是 Anthropic 最有技术含量的实现之一。当 token 使用量超过阈值时，它会：

1. SDK 计算总 token 数
2. 注入一个摘要 prompt，让 Claude 生成结构化摘要
3. 用摘要替换整个消息历史

**压缩时保留什么？** 架构决策、未解决的 bug、关键实现细节。

**丢弃什么？** 冗余的工具输出、重复的消息、已完成任务的中间过程。

Anthropic 给了个很实用的建议：**先保证 recall（不遗漏），再优化 precision（去冗余）**。宁可多保留一点，也别过度压缩导致关键上下文丢失。

还有个轻量技巧：清理历史工具调用的结果。工具调用完之后，原始返回值通常不再需要，清掉它们是最安全的压缩方式。Claude 开发者平台最近也上线了这个功能。

#### 4. Isolate（隔离）：复杂任务就拆开

复杂任务塞在一个上下文里，容易混乱。不如拆分成多个 Agent，各管各的上下文。

**三种隔离方式**：

- **按环境隔离**：不同 Agent 有不同上下文，完成不同子任务
- **按存储隔离**：建立上下文检索 API，不同信息存在不同地方，按需获取
- **按状态隔离**：设计不同状态来区分不同上下文（有点像有限状态机）

Claude Code 的做法是：用 subagent 来验证细节或调查特定问题，特别是在对话早期。这样既能保护主上下文的空间，又不损失效率。

---

### 五、深入：Claude Code 的系统 Prompt 架构

这部分比较硬核，聊聊 Claude Code 内部的系统 prompt 是怎么组织的。

**一个关键发现**：Claude Code 不是用一个单一的 system prompt 字符串。

根据社区分析（截至 v2.0.75），它的系统 prompt 由 **40+ 个字符串组件** 动态组合而成，在一个大型压缩 JS 文件里不断变化。

这种设计的好处是**模块化**——不同场景激活不同的 prompt 组件，而不是用一个巨大的 prompt 覆盖所有情况。

#### CLAUDE.md 的作用

CLAUDE.md 是一个特殊文件，Claude Code 启动时会自动拉入上下文。

**适合放什么**：
- 仓库规范（分支命名、merge vs rebase）
- 开发环境配置（pyenv、编译器版本）
- 项目特有的 quirks 和注意事项

**Anthropic 的建议**：保持简洁、人类可读，没有固定格式要求。

#### Tool 设计：少即是多

Anthropic 在博客里强调了一个常见失败模式：

> "如果人类工程师都说不清该用哪个工具，AI Agent 也做不到。"

问题往往出在：工具集太臃肿、功能覆盖有重叠、决策点模糊。

解决方案很简单：每个工具职责单一、边界清晰。工具描述要写清楚"什么时候用"和"什么时候不用"。

#### Claude 4.x 的行为变化

如果你之前用 Claude 3.x，升级到 4.x 会发现一些明显变化：

**更"听话"了**：Claude 4.x 被训练得更精确遵循指令。以前可能需要强调 "CRITICAL: You MUST..."，现在正常语气就行。反过来说，如果你的 prompt 之前为了防止模型"偷懒"加了很多强调语气，现在可能会过度触发。

**对 "think" 这个词敏感**：当 extended thinking 关闭时，Claude Opus 4.5 对 "think" 这个词特别敏感。建议用 "consider"、"evaluate"、"believe" 替代。

**并行工具调用更激进**：Sonnet 4.5 特别擅长并行执行多个工具调用。如果工具之间没有依赖关系，它会同时发起。这是好事，但也意味着你要更注意工具之间的依赖关系。

---

### 六、五条核心原则

最后总结一下 Anthropic 工程师反复强调的几条原则。这些是我读完所有材料后提炼出来的，算是"元方法论"：

#### 1. 追求信息密度，不是信息数量

> "找到最小的高信号 token 集合，最大化期望结果的概率。"

不是越多信息越好，是**相关信息密度**越高越好。

#### 2. 压缩的艺术

过度压缩会丢失"当时不起眼但后来很关键"的上下文。

实操建议：先保证 recall，再优化 precision。

#### 3. 工具设计要克制

工具不是越多越好。每加一个工具，就增加了 Agent 的决策负担。

#### 4. 示例比规则有效

Few-shot prompting 仍然是最有效的技巧之一，但要注意：
- 选择多样化、典型的例子
- 不要塞一堆边缘案例
- 示例要能代表期望行为

#### 5. System Prompt 的"金发姑娘区间"

避免两个极端：
- **太具体**：硬编码复杂逻辑，脆弱易崩
- **太模糊**：高层指导缺乏具体信号

---

### 七、实操清单

如果你在开发 AI Agent 或者重度使用 Claude Code，这几条可以直接用：

1. **建立外部记忆系统**：重要信息别只存在对话里，写到文件或数据库
2. **主动压缩长对话**：别等上下文爆了再处理，定期整理
3. **用 subagent 处理子任务**：保护主上下文的空间
4. **工具描述要精确**：说清楚什么时候用、什么时候不用
5. **监控 token 使用**：Claude 4.5 有原生的上下文感知能力，善用它

---

### 写在最后

从 Prompt Engineering 到 Context Engineering，本质上是从"单次对话优化"到"系统性信息管理"的转变。

这不是 buzzword。当 AI 从"回答问题的工具"变成"持续工作的 Agent"，管理它的"工作记忆"就成了核心能力。

回到开头我遇到的问题：Claude Code 用久了会"失忆"。现在我知道了——这不是 prompt 的问题，是我没有主动管理上下文。该写入外部存储的信息没存，该压缩的历史没压缩，所有信息都堆在一个越来越臃肿的上下文里，能不失忆吗？

Anthropic 把这套方法论公开出来，某种程度上也在定义下一代 AI 应用的开发范式。如果你在做 AI Agent 相关的事，这是必修课。

如果你想深入了解，推荐直接读 Anthropic 的原文：
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Claude Code: Best Practices for Agentic Coding](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## 参考资料

1. [Anthropic - Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
2. [Anthropic - Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
3. [LangChain - Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/)
4. [Tobi Lütke on X - Context Engineering Tweet](https://x.com/tobi/status/1935533422589399127)
5. [Claude Docs - Prompting Best Practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
6. [FlowHunt - Context Engineering Guide](https://www.flowhunt.io/blog/context-engineering/)
7. [Simon Willison - Context Engineering](https://simonwillison.net/2025/jun/27/context-engineering/)

