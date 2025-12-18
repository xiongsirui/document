# GLM写作系统 - Claude Code Skills

基于MCP (Model Context Protocol) 的GLM自动化写作系统，集成到Claude Code中。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置API Key

```bash
export GLM_API_KEY='your-api-key-here'
```

获取API Key: https://open.bigmodel.cn/

### 3. 配置Claude Code

编辑Claude Code配置文件：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

添加：

```json
{
  "mcpServers": {
    "glm-writing-system": {
      "command": "python",
      "args": [
        "D:/code/ai/document/automated_writing_system/glm_optimized/claude_code_skills/server.py"
      ],
      "env": {
        "GLM_API_KEY": "${GLM_API_KEY}"
      }
    }
  }
}
```

### 4. 重启Claude Code

重启后，您可以直接在对话中使用GLM功能。

## 🛠️ 可用功能

### 1. 内容生成
```
请写一篇关于人工智能的文章
```
- 自动调用GLM生成文章
- 支持各种主题和风格

### 2. 文本分析
```
分析这段文字的风格和情感
```
- 写作风格分析
- 情感倾向分析
- 关键词提取
- 内容总结

### 3. 内容优化
```
让这段话更简洁一些
```
- 提高清晰度
- 增强吸引力
- SEO优化
- 精简内容

### 4. 翻译功能
```
把这段话翻译成英文
```
- 支持多语言翻译
- 保持原文含义

### 5. 代码生成
```
用Python写一个快速排序算法
```
- 支持多种编程语言
- 包含详细解释
- 提供完整代码

## 💰 成本优势

| 模型 | 价格/1K tokens | 相比Claude节省 |
|------|----------------|----------------|
| Claude 3.5 | ~¥20 | - |
| GLM-4.6 | ¥0.005 | **99.9%** |
| GLM-4.5 | ¥0.0014 | **93%** |
| GLM-3-Turbo | ¥0.0005 | **97.5%** |

## 📝 使用示例

### 写作示例
```
用户：帮我写一个产品发布会的邀请函

Claude：[自动调用GLM生成]

亲爱的朋友们：

我们诚挚地邀请您参加[产品名称]发布会...

[完整内容]
```

### 代码示例
```
用户：写一个Python函数计算斐波那契数列

Claude：[自动调用GLM生成]

def fibonacci(n):
    """计算斐波那契数列的第n项"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

[完整代码和解释]
```

## ❓ 故障排除

### 1. 连接失败
- 检查GLM_API_KEY是否正确设置
- 确认依赖已完整安装
- 查看Claude Code日志

### 2. 工具不响应
- 重启Claude Code
- 检查MCP服务器是否正常运行
- 验证配置文件路径

### 3. API调用失败
- 检查API Key是否有效
- 确认网络连接正常
- 查看API配额

## 📄 许可证

MIT License