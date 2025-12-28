# Sleepless Agent 深度解析：让 AI 在你睡觉时写代码

> 【配图1：主图 - Sleepless Agent 概念图】

## 开篇：$200/月的 Claude Max，你只用了 30%

前几天刷到一个有意思的开源项目：**Sleepless Agent**。

说实话，第一眼看到这名字我就乐了——"不眠代理"，这是要让 AI 007 吗？

它解决的问题很直接：如果你订阅了 Claude Max（$200/月），白天工作可能只用掉 20-30% 的额度，剩下 70% 在夜间完全闲置。这钱花得有点冤。

Sleepless Agent 的思路是：**让 AI 在你睡觉的时候继续干活**。

你睡前在 Slack 里发几条任务，第二天早上起来，代码写好了，测试跑过了，PR 也创建了，你直接 Review 就行。

听起来很科幻对吧？

我花了几天时间研究这个项目的架构，顺便分析了一个很多人关心的问题：**能不能用 GLM-4.7 等其他大模型替换 Claude Code，降低成本？**

结论先放这里：技术上可行，但需要较大改造。下面详细说。

---

## Sleepless Agent 是什么

**一句话解释**：Sleepless Agent 是一个 Python 后台服务，它把 Claude Code CLI 包装成 24/7 持续运行的 Agent 系统。

**GitHub 地址**：https://github.com/context-machine-lab/sleepless-agent

### 它能做什么

- **任务队列**：通过 Slack 或命令行提交任务，自动排队执行
- **工作区隔离**：每个任务在独立目录执行，互不干扰
- **多代理工作流**：Planner → Worker → Evaluator 三阶段协作
- **Git 集成**：自动 commit、push、创建分支
- **智能调度**：白天/夜间不同的使用量阈值

### 工作流程

整个系统的核心执行链路是这样的：

```
1. 你通过 Slack 或命令行提交任务
   ↓
2. SmartScheduler 根据优先级决定执行顺序
   ↓
3. ClaudeCodeExecutor 调用 Claude Code CLI
   走 Planner → Worker → Evaluator 流程
   ↓
4. 自动 Git commit，存储执行日志
```

### 两种任务模式

**随机想法模式（Random Thoughts）**
- 不带 `-p` 参数
- 用于记录灵感、临时任务
- 自动提交到 `thought-ideas` 分支
- 不创建 PR

**正式任务模式（Serious Tasks）**
- 带 `-p` 参数指定项目名
- 创建独立的 feature 分支
- 完成后可以手动创建 PR

### Slack 集成的便利

这个功能我觉得挺实用：你可以躺在床上，用手机在 Slack 里发几条命令：

```
/think -p my-project 实现功能 A
/think -p my-project 实现功能 B
/think -p my-project 写单元测试
```

然后睡觉。第二天早上打开手机，就能看到执行结果和 PR 链接。

比起每次都要打开电脑、切终端、敲命令，这种方式舒服多了。

---

## 三个 Agent 协作，这才是核心

> 【配图2：三 Agent 协作流程图】

说到 Sleepless Agent 最核心的设计，就是这个**三 Agent 协作模式**。

### Planner（规划者）

负责分析任务，制定详细执行计划。

比如你提交：「创建一个 Python CLI 工具」

Planner 会输出：
1. 创建 main.py 主脚本
2. 使用 argparse 处理命令行参数
3. 添加 --name 和 --verbose 参数
4. 编写 README.md
5. 创建 requirements.txt

### Worker（执行者）

按照 Planner 的计划，逐步执行任务。

它会：
- 创建文件
- 编写代码
- 运行测试
- 修复错误

### Evaluator（评估者）

验证 Worker 的执行结果是否符合要求。

检查点包括：
- 代码是否能运行
- 功能是否完整
- 测试是否通过

### 为什么需要三个 Agent？

我一开始也觉得：搞这么复杂干嘛，一个 Agent 不就完了？

后来测试发现差距真挺大：

**只开 Worker 的情况**：任务执行得很敷衍，可能只生成一个 README 就结束了。

**三个都开的情况**：执行质量明显提升，因为有规划、有执行、有验收。

这其实就是软件工程里经典的分工：产品（Planner）、开发（Worker）、测试（Evaluator）。三个角色互相制约，质量才有保障。

---

## 踩过的坑，替你踩了

用了几天，踩了不少坑。这里总结一下，帮你少走弯路。

### 坑 1：SSH vs HTTPS

**问题**：配置 SSH 地址后，push 报权限错误。

**原因**：如果用 `gh auth login` 认证过 GitHub，它用的是 HTTPS Token。SSH 需要单独配置密钥。

**解决**：直接用 HTTPS 地址，省事。

### 坑 2：文件创建位置错误

**问题**：Worker 把文件创建到 `/private/tmp/` 而不是项目目录。

**原因**：Claude Code CLI 的工作目录配置问题。

**临时解决**：在任务描述里明确指定文件路径，比如「创建 workspace/projects/my-project/main.py」

### 坑 3：PR 无法创建

**问题**：用 `git push --all` 推送后，所有分支内容一样，无法创建 PR。

**原因**：`--all` 把所有提交推到了所有分支。

**解决**：确保 feature 分支和 main 分支有差异，手动创建测试提交。

### 坑 4：多代理工作流未启用

**问题**：任务执行质量差，只生成了 README。

**原因**：只开启了 Worker，没开 Planner 和 Evaluator。

**解决**：在 config.yaml 里把三个都设为 enabled: true。

---

## 5 分钟快速上手

> 【配图3：快速上手流程图】

上面说了这么多原理和坑，可能有人已经想动手试了。这部分给你一个完整的上手指南。

### 前置条件

**必需项：**
- Claude Max 订阅（$200/月）
- Python 3.10+
- Git 和 GitHub 账号
- 一个 GitHub Personal Access Token

**可选项：**
- Slack Workspace（方便远程提交任务）

### 安装步骤

**Step 1：安装 Claude Code CLI**

这是基础，先把官方 CLI 装上：

```bash
npm install -g @anthropic-ai/claude-code
```

装完后测试一下：`claude --version`，能输出版本号就说明装好了。

**Step 2：克隆 Sleepless Agent**

```bash
git clone https://github.com/context-machine-lab/sleepless-agent.git
cd sleepless-agent
```

**Step 3：安装 Python 依赖**

```bash
pip install -r requirements.txt
```

如果遇到权限问题，用 `pip install --user -r requirements.txt`

**Step 4：创建 GitHub Token**

Sleepless Agent 需要权限帮你自动 commit 和 push。

去 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)，生成新 token，勾选 `repo` 权限。

**Step 5：配置 config.yaml**

这是核心配置文件，需要设置：
- 工作区路径
- GitHub 仓库地址
- GitHub Token
- 多代理开关（建议全开）
- 任务超时和重试次数

**Step 6：第一次运行**

先跑个简单任务测试：

```bash
python main.py --task "创建一个 README.md" --project test-project
```

如果一切正常，你会看到 Agent 开始分析任务 → Planner 制定计划 → Worker 执行 → Evaluator 验证 → 自动 commit。

**Step 7：启动守护进程（可选）**

如果你想让 Agent 24/7 运行，可以启动守护进程。macOS 和 Linux 都有对应命令。

### 常见启动问题

**问题 1**：`ModuleNotFoundError` → 用 `pip install xxx` 安装缺失模块

**问题 2**：Git push 失败 → 检查 GitHub Token 或用 `gh auth login` 重新认证

**问题 3**：Claude API 调用失败 → 用 `claude auth login` 重新登录

---

## 能不能用 GLM 替换 Claude Code？

这是很多人问的问题。$200/月确实不便宜，能不能换个便宜的模型？

我研究了一下，结论是：**能，但费劲**。

### 先看架构依赖

Sleepless Agent 的核心是 `ClaudeCodeExecutor`，它调用的是 Claude Code CLI。

这个 CLI 不只是 API 调用，它是一个完整的开发环境：
- 文件读写
- Shell 命令执行
- Git 操作
- 多代理调度
- 工具权限管理

### GLM-4.7 能力怎么样？

看了下官方数据：
- SWE-bench：73.8%（不错的成绩）
- 支持 Tool Calling（OpenAI 格式）
- 支持思维链推理
- 原生支持代码生成

而且 GLM-4.7 官方已经宣布可以在 Claude Code、Kilo Code、Roo Code 等编码代理中使用。

**但问题来了**：GLM 只有 API，没有官方 CLI 工具。

### 替换可行性分析

| 维度 | Claude Code | GLM-4.7 | 可替换性 |
|------|-------------|---------|----------|
| API 调用 | Anthropic API | Z.ai API | 可以 |
| Tool Calling | 原生支持 | 原生支持 | 可以 |
| Coding 能力 | 很强 | 不错 | 可以 |
| CLI 工具 | 官方提供 | 没有 | 需自建 |
| 多代理调度 | 内置 | 需自己实现 | 需改造 |

### 两种替换方案

**方案 A：最小改动（推荐）**

利用 Claude Code 支持自定义 API 端点的特性，搭一个代理服务，把 GLM API 转成 Anthropic 格式。有一定技术门槛。

**方案 B：重写执行层**

用 GLM API + LangChain/AutoGen 重新实现所有功能。工作量较大，相当于重写整个执行层。

### 我的建议

说实话，如果你已经有 Claude Max 订阅，直接用原生方案最省心。

如果真想省钱，可以考虑：
1. **短期**：等社区出 GLM 适配方案（已经有人在做了）
2. **中期**：用方案 A 搭代理，技术门槛不算太高
3. **长期**：等 GLM 官方出 CLI 工具（不知道要等多久）

---

## 什么场景适合用？

> 【配图4：适用场景对比图】

用了一段时间，我总结了下适合和不适合的场景。

### 适合的场景

**个人 Side Project**

你有很多想法，但白天时间有限。睡前提交任务，第二天起来 Review。这种场景太合适了。

**技术债务清理**

加测试、重构代码、更新文档、依赖升级。这些事情重要但枯燥，让 AI 做最合适。

**批量迁移任务**

比如给项目里 50 个文件加 license 头，或者把某个 API 调用统一替换成新版本。

**工具和脚本开发**

自动化脚本、CLI 工具、数据处理。需求明确，逻辑清晰的任务。

### 不适合的场景

**企业级项目**

复杂流程、多团队协作、严格合规要求。不适合完全自动化。

**需要频繁交互的任务**

如果任务方向可能随时调整，异步执行反而低效。

**高度定制化需求**

复杂的业务逻辑，AI 可能理解不了。

---

## 效率提升到底有多少？

这个问题大家最关心。我结合社区反馈算了下，实际效率提升在 60-80% 左右。

### 时间对比

| 阶段 | 传统开发 | Sleepless Agent | 节省 |
|------|---------|-----------------|------|
| 需求分析 | 4h | 4h | 0% |
| 架构设计 | 2h | 2h | 0% |
| 任务分解 | 1h | 1h | 0% |
| 代码实现 | 40h | 2h (Review) | 95% |
| 测试调试 | 20h | 3h (Review) | 85% |
| 文档编写 | 8h | 1h (Review) | 87% |
| **总计** | **75h** | **13h** | **83%** |

### 关键认知

有几点要说清楚：

前期工作（需求、架构、任务分解）**无法省略**。这些还是得你自己做。

Review 时间也**不能压缩**，这是质量把关的关键。AI 写的代码不能盲目信任。

人类从「码农」变成「PM + 架构师 + Reviewer」，时间花在更有价值的事情上。你不是被替代了，是升级了。

---

## 总结：AI Agent 的正确打开方式

> 【配图5：结尾总结图】

Sleepless Agent 给我的最大启发是：

**AI 不是替代你，而是成为你的开发团队。**

你负责：
- 定义需求
- 技术选型
- 任务分解
- 代码 Review

AI 负责：
- 编写代码
- 运行测试
- 生成文档
- 处理重复性工作

这才是人机协作的正确姿势。

至于 GLM 替换的问题，技术上可行，但现阶段还需要较大改造。如果你已经有 Claude Max 订阅，直接用原生方案是最优解。

---

## 相关资源

- Sleepless Agent GitHub：https://github.com/context-machine-lab/sleepless-agent
- Sleepless Agent 文档：https://context-machine-lab.github.io/sleepless-agent/
- GLM-4.7 API 文档：https://docs.z.ai/guides/llm/glm-4.7
- Claude Code 官方文档：https://code.claude.com/docs

---

*这是 Claude Code 系列的第六篇。之前写过《Agents 实战指南》《Skills 完全指南》《Background Agents 完全指南》《LSP 完全指南》《CC Switch 产品介绍》，感兴趣可以翻翻历史文章。*

*有问题欢迎评论区讨论。*

---

**全文约 4200 字，阅读时间约 13 分钟**
