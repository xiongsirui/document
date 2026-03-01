# OpenClaw + Claude Code：在 Telegram 里远程操控终端，实时确认每一步

![OpenClaw 架构](../images/openclaw/01-architecture.jpg)

## 开篇：手机发消息，电脑在干活

前几天我在外面吃饭，突然收到群里报错的消息。

手头没有电脑，但问题又比较紧急。怎么办？

我想起最近在用的 OpenClaw，掏出手机，在 Telegram 里发了一条消息：「帮我查一下 logs/error.log 最后 20 行」。

几秒后，手机收到回复：

```
AI：正在查看日志...

[2025-02-26 10:15:23] ERROR: Connection timeout
[2025-02-26 10:15:27] FATAL: Database connection lost

分析：数据库连接超时，可能是连接池满了。

需要我检查数据库状态吗？
```

我回复：「检查一下」

```
AI：执行 db status...

Connections: 95/100 (警告：接近上限）

问题定位：连接池快满了。建议重启连接池。

需要我重启吗？
```

我回复：「重启」

```
AI：⚠️ 重启连接池会影响正在进行的请求，确认吗？

你：确认

AI：已重启连接池，当前连接数：12/100
问题已解决。
```

**整个过程，我没开电脑，没开终端，只在手机上发了几条消息。**

这就是 OpenClaw + Claude Code 的核心价值：**把终端交互搬到 IM 里，随时随地操控，实时确认每一步**。

今天这篇文章，我会讲清楚：
- OpenClaw 是什么，和 Claude Code 的关系
- Skills 系统如何连接 IM 和终端
- 完整的配置和操作指南
- 实际场景演示
- 踩过的坑

---

## Part 1：核心原理

### OpenClaw 是什么？

**OpenClaw 是一个开源的个人 AI 助手网关**，它把 Claude Code（或其他 AI 模型）包装成多渠道可访问的服务。

**GitHub 地址**：https://github.com/openclaw/openclaw

### 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                        你的手机                              │
│                   Telegram / WhatsApp                        │
│                         │                                    │
│                    发消息/收结果                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      OpenClaw Gateway                        │
│                    (运行在你的电脑上)                         │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Channel    │    │    Skill     │    │    Agent     │  │
│   │   Handler    │───▶│   Executor   │───▶│   (Claude)   │  │
│   │ (Telegram)   │    │  (terminal)  │    │              │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│                              │                    │          │
│                              ▼                    ▼          │
│                         ┌─────────────────────────────┐     │
│                         │       Claude Code CLI        │     │
│                         │      (终端执行 + 输出)        │     │
│                         └─────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 数据流

1. 用户在 Telegram 发送消息
2. OpenClaw Gateway 接收消息，调用对应 Skill
3. Skill 执行终端命令或调用 Claude Code CLI
4. 输出被捕获，格式化后返回 Telegram
5. 如需确认，暂停等待用户回复

### 和 Claude Code 的关系

| 工具 | 定位 | 职责 |
|------|------|------|
| **Claude Code** | AI 编程代理 | 执行代码任务、读写文件、运行命令 |
| **OpenClaw** | 多渠道网关 | 接收 IM 消息、调度执行、返回结果、处理确认 |

---

## Part 2：Skills 系统

### 什么是 Skill？

Skill 是 OpenClaw 的插件系统，用于扩展 AI 的能力。**ClawHub 上目前有 3000+ Skill 可用**。

核心 Skill：

| Skill | 作用 |
|-------|------|
| `terminal-pro` | 执行 bash 命令，返回终端输出 |
| `code-interpreter` | 运行 Python/JS 代码 |
| `github` | GitHub 仓库操作 |
| `browser` | 浏览器自动化 |

### terminal-pro：最核心的 Skill

这个 Skill 让 AI 能执行终端命令，并支持**交互式确认**：

```yaml
# ~/.openclaw/workspace/skills/terminal-pro/SKILL.md
skills:
  - name: terminal-pro
    description: |
      Execute bash commands and return terminal output.
      Supports interactive confirmation for dangerous operations.
    tools:
      - bash
      - read
      - write
      - edit
```

**交互式确认机制**：

```
AI：准备执行：rm -rf ./dist
这是一个危险操作，是否继续？

你：继续

AI：已执行，删除了 23 个文件
```

### 安装 Skills

```bash
# 从 ClawHub 安装
openclaw hub install terminal-pro

# 查看已安装
openclaw skills list

# 搜索 skill
openclaw hub search <关键词>
```

Skills 安装位置：`~/.openclaw/workspace/skills/`

---

## Part 3：完整配置指南

### 前置条件

| 条件 | 说明 |
|------|------|
| Node.js ≥22 | 运行环境 |
| Claude Max 订阅 | 或 Claude API Key |
| Telegram 账号 | 用于 Bot 通信 |

### Step 1：安装 OpenClaw

```bash
npm install -g openclaw@latest

# 运行初始化向导
openclaw onboard --install-daemon
```

向导会引导完成：
1. Gateway 配置
2. Workspace 设置
3. 渠道连接
4. Skills 安装

### Step 2：配置 Claude 作为后端

```json
// ~/.openclaw/openclaw.json
{
  "agent": {
    "model": "anthropic/claude-opus-4-6"
  }
}
```

### Step 3：配置 Telegram 渠道

1. 在 Telegram 找 `@BotFather`，发送 `/newbot`
2. 按提示创建 Bot，获取 Token（格式：`123456:ABCDEF...`）
3. 配置：

```json
// ~/.openclaw/openclaw.json
{
  "channels": {
    "telegram": {
      "botToken": "123456:ABCDEF..."
    }
  }
}
```

4. 启动 Gateway：

```bash
openclaw gateway --port 18789 --verbose
```

5. 在 Telegram 给 Bot 发消息，获取配对码
6. 批准配对：

```bash
openclaw pairing approve telegram ABC123
```

### Step 4：安装并配置 terminal-pro Skill

```bash
openclaw hub install terminal-pro
```

```json
// ~/.openclaw/openclaw.json
{
  "skills": {
    "terminal-pro": {
      "enabled": true,
      "confirmDangerousOps": true,
      "timeout": 60000
    }
  }
}
```

### Step 5：测试

在 Telegram 发送：

```
你：列出当前目录的文件
```

应收到：

```
AI：执行 ls -la...

total 48
drwxr-xr-x  12 user  staff   384 Feb 26 10:30 .
-rw-r--r--   1 user  staff  1024 Feb 26 10:30 README.md
drwxr-xr-x   6 user  staff   192 Feb 26 10:30 src
```

---

## Part 4：实际场景演示

### 场景 1：远程调试

```
你（Telegram）：
生产环境报错了，帮我查一下 logs/error.log 最后 20 行

AI：
执行 tail -n 20 logs/error.log...

[2025-02-26 10:15:23] ERROR: Connection timeout
[2025-02-26 10:15:27] FATAL: Database connection lost

分析：数据库连接超时，可能是连接池满了。

需要我检查数据库状态吗？

你：检查一下

AI：
执行 db status...

Connections: 95/100 (警告：接近上限）

问题定位：连接池快满了。建议重启连接池。

需要我重启吗？

你：重启

AI：
⚠️ 重启连接池会影响正在进行的请求，确认吗？

你：确认

AI：
已重启，当前连接数：12/100
问题已解决。
```

### 场景 2：代码重构

```
你（Telegram）：
帮我把 src/utils/helpers.ts 里的函数改成 arrow function

AI：
读取 src/utils/helpers.ts...
找到 8 个函数声明

准备修改：
1. formatDate → const formatDate = ...
2. parseJSON → const parseJSON = ...
...

这是一个较大的改动，是否继续？

你：继续

AI：
已完成 8 处修改

需要我运行测试验证吗？

你：跑一下

AI：
执行 npm test...
✓ 45 tests passed

所有测试通过！
```

### 场景 3：部署确认

```
你（Telegram）：
帮我部署到 staging

AI：
准备执行 deploy/staging.sh

⚠️ 此操作会：
1. 构建 5 分钟
2. 重启 staging 服务器

确认部署？

你：yes

AI：
开始部署...
[1/5] 拉取代码... ✓
[2/5] 安装依赖... ✓
[3/5] 构建... ✓
[4/5] 测试... ✓
[5/5] 部署... ✓

完成！
Staging URL: https://staging.example.com
```

---

## Part 5：交互式确认机制

### 为什么需要确认？

Claude Code 执行某些操作时需要用户确认：
- 删除文件（`rm`）
- 修改关键配置
- 部署到生产环境
- 执行不可逆操作

### 确认流程

```
1. AI 检测到危险操作
2. 暂停执行，发送确认请求到 IM
3. 用户在 IM 里回复 "yes" 或 "no"
4. OpenClaw 把回复传回
5. AI 继续或取消操作
```

### 配置确认规则

```json
// ~/.openclaw/openclaw.json
{
  "agents": {
    "defaults": {
      "confirmPolicy": {
        "alwaysConfirm": ["rm", "git push", "npm publish"],
        "neverConfirm": ["ls", "cat", "grep"]
      }
    }
  }
}
```

---

## Part 6：踩过的坑

### 坑 1：终端输出被截断

**问题**：长输出只显示一部分

**原因**：Telegram 消息长度限制

**解决**：

```json
{
  "skills": {
    "terminal-pro": {
      "maxOutputLength": 4000
    }
  }
}
```

### 坑 2：确认超时

**问题**：太久没回复，操作被取消

**解决**：

```json
{
  "agents": {
    "defaults": {
      "confirmationTimeout": 300000
    }
  }
}
```

### 坑 3：配对失败

**问题**：发消息没反应

**原因**：未完成配对

**解决**：

```bash
openclaw pairing list
openclaw pairing approve telegram <code>
```

### 坑 4：并发冲突

**问题**：多个任务同时执行，互相干扰

**解决**：

```json
{
  "agents": {
    "defaults": {
      "queueMode": "sequential"
    }
  }
}
```

---

## Part 7：安全建议

### 权限最小化

```json
{
  "skills": {
    "terminal-pro": {
      "allowCommands": ["ls", "cat", "grep", "npm", "git"],
      "denyCommands": ["rm -rf /", "sudo"]
    }
  }
}
```

### 敏感操作保护

```json
{
  "confirmPolicy": {
    "production": {
      "requireConfirmation": true,
      "confirmMessage": "请输入 CONFIRM PRODUCTION 继续"
    }
  }
}
```

### 网络安全

```json
{
  "gateway": {
    "bind": "loopback",
    "allowedIPs": ["192.168.1.0/24"]
  }
}
```

---

## 快速参考

### 核心配置

```json
// ~/.openclaw/openclaw.json
{
  "agent": {
    "model": "anthropic/claude-opus-4-6"
  },
  "channels": {
    "telegram": {
      "botToken": "YOUR_BOT_TOKEN"
    }
  },
  "skills": {
    "terminal-pro": {
      "enabled": true,
      "confirmDangerousOps": true
    }
  }
}
```

### 常用命令速查

| 场景 | 你说的话 |
|------|---------|
| 查看文件 | 「看一下 package.json」 |
| 执行命令 | 「运行 npm test」 |
| 重构代码 | 「把 XXX 改成 YYY」 |
| 部署 | 「部署到 staging」 |
| 确认操作 | 「继续」/「yes」 |
| 取消操作 | 「取消」/「no」 |

### CLI 命令

```bash
npm install -g openclaw@latest    # 安装
openclaw onboard --install-daemon # 初始化
openclaw gateway --port 18789     # 启动
openclaw pairing approve telegram <code>  # 配对
openclaw hub install terminal-pro # 安装 Skill
```

---

## 总结

OpenClaw + Claude Code 带来的最大改变是：

**终端不再是"黑盒子"，而是可以随时随地通过 IM 交互的"对话窗口"。**

你不需要打开电脑、切换到终端、记住复杂的命令。只需要在 IM 里发消息，看到输出后确认下一步，实时掌控整个过程。

**和 Sleepless Agent 的配合**：
- **白天**：OpenClaw 实时交互，随时确认
- **晚上**：Sleepless Agent 批量执行，利用闲置额度

两者配合，让 AI 真正成为你的 24/7 助手。

---

![结尾图](../images/openclaw/02-conclusion.jpg)

## 相关资源

- OpenClaw GitHub：https://github.com/openclaw/openclaw
- ClawHub Skills：https://clawhub.ai
- Claude Code 文档：https://docs.anthropic.com/claude-code
- Telegram Bot 教程：https://core.telegram.org/bots/tutorial

---

*这是 Claude Code 系列的第七篇。之前写过《Agents 实战指南》《Skills 完全指南》《Background Agents 完全指南》《LSP 完全指南》《Sleepless Agent 深度解析》《Context Engineering 深度解析》，感兴趣可以翻翻历史文章。*

*有问题欢迎评论区讨论。*

---

**全文约 3500 字，阅读时间约 10 分钟**
