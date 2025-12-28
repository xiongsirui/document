# CC Switch：一站式管理 Claude Code / Codex / Gemini 的神器

> 【配图1：主图 - CC Switch 界面截图】

## 开篇：三个 CLI 工具，三套配置，烦死了

最近 AI 编程工具越来越多了：Claude Code、Codex、Gemini CLI...

每个都要单独配置：
- Claude Code 要配 `~/.claude/settings.json`
- Codex 要配 `~/.codex/settings.json`
- Gemini 要配 `~/.gemini/settings.json`

想换个 API Provider？手动改 JSON。
想加个 MCP Server？三个地方都要配。
想用个 Skill？每个工具操作方式还不一样。

更崩溃的是：每次换个国产模型试试（比如 Kimi、Deepseek），又要改一堆配置。改错了还可能把原来的配置搞丢。

有没有一个工具，能**统一管理这些乱七八糟的东西**？

有。今天介绍的 **CC Switch** 就是干这个的。

---

## CC Switch 是什么

**GitHub**: https://github.com/farion1231/cc-switch

CC Switch 是一个跨平台桌面应用，用来统一管理 Claude Code、Codex、Gemini CLI 的：

- ✅ **Provider 配置**：一键切换官方/第三方 API
- ✅ **MCP Server**：跨应用统一管理
- ✅ **Skills**：一键安装/卸载
- ✅ **System Prompt**：多预设管理，快速切换

**支持平台**：Windows、macOS、Linux

**技术栈**：Tauri 2.0 + React 18 + TypeScript（后面会详细分析）

---

## 核心功能详解

### 功能 1：Provider 一键切换

这是最刚需的功能。

**场景**：你平时用官方 Claude API，但想试试 Kimi 或者 Deepseek 的效果。

**以前怎么做**：
1. 打开 `~/.claude/settings.json`
2. 手动改 `apiUrl` 和 `apiKey`
3. 保存，重启 Claude Code
4. 想换回来？再改一遍

**用 CC Switch**：
1. 打开 CC Switch
2. 点击预设的 Provider（比如「Kimi」）
3. 一键应用
4. 重启 Claude Code

内置的预设包括：
- 官方登录（Claude/Codex/Gemini 各自的 OAuth）
- PackyCode
- 自定义（填你自己的 API 地址和 Key）

还有个贴心功能：**切换前自动备份当前配置**，不怕改错。

### 功能 2：MCP Server 统一管理

MCP（Model Context Protocol）是现在 AI 编程工具的扩展协议。但问题是：

Claude Code、Codex、Gemini 的 MCP 配置格式不一样，分散在不同的文件里。

CC Switch 把它们统一了：

```
┌─────────────────────────────────────┐
│         CC Switch MCP 管理           │
├─────────────────────────────────────┤
│  ┌─────────┐                        │
│  │ MCP-1   │ → Claude Code ✓       │
│  │         │ → Codex ✓             │
│  │         │ → Gemini ✗            │
│  └─────────┘                        │
│  ┌─────────┐                        │
│  │ MCP-2   │ → Claude Code ✓       │
│  │         │ → Codex ✗             │
│  │         │ → Gemini ✓            │
│  └─────────┘                        │
└─────────────────────────────────────┘
```

你可以：
- 在一个界面管理所有 MCP Server
- 选择哪个 MCP 对哪个应用生效
- 一键同步到各个应用的配置文件

### 功能 3：Skills 市场

Claude Code 的 Skills 是个好东西，但发现和安装有点麻烦。

CC Switch 内置了 Skills 浏览器：
- 自动扫描 GitHub 上的 Skills 仓库（包括 Anthropic 官方、ComposioHQ、社区仓库等）
- 一键安装到 `~/.claude/skills/`
- 一键卸载，清理干净

不用手动 clone、不用手动复制文件。

### 功能 4：System Prompt 多预设

不同项目可能需要不同的 System Prompt。

CC Switch 让你可以：
- 创建多个 Prompt 预设
- 每个预设有独立的 Markdown 内容
- 一键激活，自动同步到对应的配置文件

同步规则：
- Claude Code → `~/.claude/CLAUDE.md`
- Codex → `~/.codex/AGENTS.md`
- Gemini → `~/.gemini/GEMINI.md`

还有个 Markdown 编辑器，支持语法高亮和实时预览。

---

## 使用方式

### 安装

去 [Releases 页面](https://github.com/farion1231/cc-switch/releases) 下载：

| 平台 | 格式 |
|------|------|
| Windows | `.msi` 安装包 或 `.zip` 便携版 |
| macOS | `.dmg` 或 `.zip` |
| Linux | `.deb` 或 `.AppImage` |
| Arch Linux | `paru -S cc-switch-bin` |

### 快速上手

**1. 首次启动**

CC Switch 会自动检测并导入你现有的 Claude/Codex/Gemini 配置作为默认 Provider。

**2. 切换 Provider**

点击左侧的「Providers」，选择一个预设（比如「Kimi」），点击「Apply」。

**3. 管理 MCP Server**

点击右上角的「MCP」按钮，添加或编辑 MCP Server，勾选要同步的应用。

**4. 安装 Skills**

点击右上角的「Skills」按钮，浏览可用的 Skills，点击「Install」一键安装。

**5. 管理 Prompt**

点击右上角的「Prompts」按钮，创建新预设或编辑现有的，点击「Activate」激活。

---

## 源码架构分析

作为程序员，我对这个项目的架构很感兴趣。让我拆解一下。

### 技术选型

| 层 | 技术 |
|---|------|
| **桌面框架** | Tauri 2.8（Rust 后端 + Web 前端） |
| **前端** | React 18 + TypeScript + Vite |
| **UI** | TailwindCSS 4 + shadcn/ui |
| **状态管理** | TanStack Query v5 |
| **表单** | react-hook-form + zod |
| **国际化** | react-i18next（中英双语） |
| **后端** | Rust + serde + tokio |

**为什么选 Tauri？**

相比 Electron，Tauri 的优势是：
- 包体积小（几 MB vs 几十 MB）
- 内存占用低
- 原生性能（Rust 后端）

对于一个配置管理工具来说，轻量是第一优先级。

### 项目结构

```
cc-switch/
├── src/                    # 前端代码 (React)
│   ├── components/         # UI 组件
│   │   ├── providers/      # Provider 管理相关
│   │   ├── settings/       # 设置页面
│   │   ├── mcp/            # MCP 管理
│   │   └── ui/             # 通用 UI 组件 (shadcn)
│   ├── hooks/              # 自定义 Hooks（业务逻辑）
│   ├── lib/
│   │   ├── api/            # Tauri API 封装（类型安全）
│   │   └── query/          # TanStack Query 配置
│   ├── i18n/locales/       # 国际化文件 (zh/en)
│   ├── config/             # 预设配置
│   └── types/              # TypeScript 类型定义
│
├── src-tauri/              # 后端代码 (Rust)
│   ├── src/
│   │   ├── commands/       # Tauri 命令层（按领域划分）
│   │   ├── services/       # 业务逻辑层
│   │   ├── app_config.rs   # 配置数据模型
│   │   ├── provider.rs     # Provider 领域模型
│   │   ├── mcp.rs          # MCP 同步 & 验证
│   │   └── lib.rs          # 应用入口 & 托盘菜单
│   └── Cargo.toml
│
└── package.json
```

### 架构亮点

**1. 前后端分离 + 类型安全**

前端通过 Tauri IPC 调用后端 Rust 函数，封装在 `lib/api/` 中，保证类型安全。

```typescript
// 前端调用示例
import { invoke } from '@tauri-apps/api/core';

const providers = await invoke<Provider[]>('get_providers');
```

**2. 领域驱动设计**

后端按领域划分模块：
- `commands/` - API 层
- `services/` - 业务逻辑层
- `models/` - 数据模型层

比如 MCP 相关功能在 v3.8.0 重构时，把 1135 行的 `mcp.rs` 拆分成了：
- `validation.rs` - 验证逻辑
- `claude.rs` - Claude 相关
- `codex.rs` - Codex 相关
- `gemini.rs` - Gemini 相关

**3. 双层数据持久化**

v3.8.0 引入了 SQLite + JSON 双层架构：
- SQLite：存储 Provider、MCP、Skills 等结构化数据
- JSON：兼容各 CLI 工具的原生配置格式

这样既有数据库的查询效率，又保持了与原生配置的兼容性。

**4. 自动同步机制**

当你在 CC Switch 中修改配置后，会自动同步到对应的配置文件：

```
CC Switch 数据库
      ↓
   同步引擎
      ↓
┌─────────────────────────────┐
│ ~/.claude/settings.json    │
│ ~/.codex/settings.json     │
│ ~/.gemini/settings.json    │
└─────────────────────────────┘
```

---

## 适用场景

### 场景 1：多 Provider 切换党

你同时用官方 API、Kimi、Deepseek，经常要切换比较效果。

→ CC Switch 让你一键切换，不用手动改 JSON。

### 场景 2：MCP 重度用户

你装了很多 MCP Server，想在 Claude Code 和 Codex 之间共享，但又不想每个都配一遍。

→ CC Switch 统一管理，勾选同步。

### 场景 3：多项目不同配置

不同项目需要不同的 System Prompt。

→ CC Switch 的 Prompt 预设功能，一键切换。

### 场景 4：Skills 探索者

想试试 GitHub 上各种 Skills，但手动安装太麻烦。

→ CC Switch 内置 Skills 市场，一键安装卸载。

---

## 我的使用体验

用了一周，说说感受：

**优点**：
- 🎯 **痛点精准**：配置管理确实是个麻烦事，CC Switch 解决得很好
- 🚀 **轻量**：Tauri 架构，安装包才几 MB，启动秒开
- 🌍 **国际化**：中英双语，对国内用户友好
- 📦 **功能完整**：Provider、MCP、Skills、Prompt 全覆盖

**小建议**：
- UI 可以再精致一点（不过开源项目，能用就行）
- 希望能加个配置导出/导入功能（方便换电脑）

**总体评价**：如果你同时用多个 AI CLI 工具，或者经常切换 Provider，这个工具值得装一个。

---

## 总结

CC Switch 解决的是一个**「配置碎片化」**的问题。

当你只用 Claude Code 一个工具、只用官方 API 的时候，可能感觉不强烈。

但当你开始：
- 同时用 Claude Code + Codex + Gemini
- 想试试各种国产模型
- 装了一堆 MCP Server
- 不同项目有不同的 Prompt

这时候，统一管理的价值就体现出来了。

**推荐人群**：
- AI 工具重度用户
- 经常切换 Provider 的人
- MCP/Skills 探索者
- 讨厌手动改 JSON 的人

**不推荐人群**：
- 只用一个工具、只用官方 API 的人（原生配置就够了）

---

> 【配图2：结尾图 - 多工具统一管理概念图】

## 相关资源

- GitHub 仓库：https://github.com/farion1231/cc-switch
- Releases 下载：https://github.com/farion1231/cc-switch/releases
- CLI 版本（命令行爱好者）：https://github.com/SaladDay/cc-switch-cli

---

*这是 Claude Code 系列的第五篇。之前写过《Agents 实战指南》《Skills 完全指南》《Background Agents 完全指南》《LSP 完全指南》，感兴趣可以翻翻历史文章。*

*有问题欢迎评论区讨论。*

---

**全文约 2800 字，阅读时间约 8 分钟**
