# 公众号写作集成指南

## 概述

这个目录是你的公众号写作工作区，与 AIWriteX 深度集成，支持**一键润色配图**和**一键发布**。

## 完整工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                   1. 内容生成 (document)                      │
│                                                             │
│  你说: "帮我写一篇关于xxx的文章"                               │
│        ↓                                                    │
│  我生成 Markdown 草稿（符合熊哥风格）                          │
│        ↓                                                    │
│  保存到: _协作文档/                                           │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                2. 润色配图 (AIWriteX)                         │
│                                                             │
│  python polish_and_publish.py article.md                    │
│        ↓                                                    │
│  - HTML 排版美化                                            │
│  - AI 配图生成                                               │
│  - 格式优化                                                  │
│        ↓                                                    │
│  输出: AIWriteX/output/article/xxx.html                      │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                   3. 一键发布 (API)                           │
│                                                             │
│  python polish_and_publish.py article.md --publish          │
│        ↓                                                    │
│  调用 AIWriteX 发布 API                                       │
│        ↓                                                    │
│  自动发布到公众号草稿箱                                        │
└─────────────────────────────────────────────────────────────┘
```

## 目录结构

```
公众号写作/
├── _briefs/              # 商单 brief 存放
├── _协作文档/              # 正在创作的文章 (Markdown)
├── _knowledge_base/       # 知识库
├── polish_and_publish.py  # 润色发布脚本 ⭐
├── README.md              # 本文档
└── CLAUDE.md              # 写作规范
```

## 使用方式

### 方式1: 命令行工具

```bash
# 1. 润色文章（生成精美HTML+配图）
python polish_and_publish.py _协作文档/xxx.md

# 2. 润色 + 一键发布
python polish_and_publish.py _协作文档/xxx.md --publish

# 3. 直接发布已有HTML
python polish_and_publish.py /path/to/xxx.html --publish-only

# 4. 指定公众号账号
python polish_and_publish.py xxx.md --publish --account 0

# 5. 查看可用账号
python polish_and_publish.py --list-accounts
```

### 方式2: 直接对话 (推荐)

直接告诉我你要写什么，我会：
1. 生成 Markdown 草稿
2. 询问是否润色配图
3. 询问是否一键发布

```
你: 帮我写一篇关于"AI 编程的未来趋势"的文章

我: [生成文章] → 保存到 _协作文档/
   是否需要润色配图并发布？

你: 润色并发布

我: [调用 AIWriteX] → [发布到公众号] → 完成！
```

## 命令参数

| 参数 | 说明 |
|------|------|
| `input` | 输入文件路径 (Markdown 或 HTML) |
| `--publish` | 润色后自动发布 |
| `--publish-only` | 跳过润色，直接发布 |
| `--account N` | 指定公众号账号索引 |
| `--title "xxx"` | 指定文章标题 |
| `--list-accounts` | 列出已配置的公众号账号 |

## 前置条件

1. **AIWriteX 已启动**
   ```bash
   cd I:/ai/AIWrite
   python main.py
   ```

2. **微信公众号已配置**
   - 在 AIWriteX 配置页面填写 AppID 和 AppSecret

3. **Python 依赖**
   ```bash
   pip install requests
   ```

## 文章状态流转

```
[新想法] → [Markdown草稿] → [润色HTML] → [已发布]
   │            │              │            │
   └── 对话生成 ─┘── polish ───┘── publish ─┘
```

## 常见问题

### Q: AIWriteX 服务未启动？

```bash
# 启动 AIWriteX
cd I:/ai/AIWrite
python main.py

# 或者使用 Web UI
python -m src.ai_write_x.web.app
```

### Q: 如何查看已发布的文章？

- **本地文章**: `AIWriteX/output/article/`
- **发布记录**: `AIWriteX/output/article/publish_records.json`
- **公众号后台**: 登录微信公众平台查看草稿箱

### Q: 如何修改文章风格？

编辑 `CLAUDE.md` 中的写作规范，或者在对话中告诉我具体的风格要求。

### Q: 支持多账号发布吗？

支持！使用 `--account` 参数指定账号索引：

```bash
# 发布到第一个账号
python polish_and_publish.py xxx.md --publish --account 0

# 发布到第二个账号
python polish_and_publish.py xxx.md --publish --account 1
```

## 技术架构

```
document (Claude Code)
    │
    ├── 生成内容 (Markdown)
    │
    └── 调用 polish_and_publish.py
            │
            ├── 调用 AIWriteX CLI (润色配图)
            │
            └── 调用 AIWriteX API (发布)
                    │
                    └── 微信公众号 API
```
