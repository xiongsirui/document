# AI Skills 集合

这是一套Claude Code技能集合，提供多样化的AI辅助功能，包括直接调用API和模板化方案。

📖 **详细使用指南**：查看 [使用指南.md](使用指南.md) 了解如何实际使用这些技能。

## 🚀 快速开始

### 方式一：使用API版本（需要后端服务）
1. 启动后端服务
```bash
cd skills
python glm_backend.py
export API_KEY="your-api-key"
```

2. 在Claude Code中使用
```
[AI] 写一篇文章...
[AI] 分析这段话...
[AI] 写一个Python函数...
```

### 方式二：使用模板版本（无需API）
直接使用预定义模板：
```
使用模板：新闻稿
主题：[事件]
...
```

## 📚 技能列表

### 核心写作
- [writer_api.md](writer_api.md) - API写作助手（推荐）
- [article_writer.md](article_writer.md) - 文章模板
- [writer_template.md](writer_template.md) - 模拟风格写作

### 完整工作流
- [writing_workflow.md](writing_workflow.md) - 9步专业写作流程
- [knowledge_base.md](knowledge_base.md) - 个人素材库管理

### 内容工具
- [content_analyzer.md](content_analyzer.md) - 内容分析器
- [translator.md](translator.md) - 智能翻译器
- [code_assistant.md](code_assistant.md) - 编程助手
- [knowledge_manager.md](knowledge_manager.md) - 知识管理器

## 💰 成本优势

| 功能 | GLM成本 | Claude成本 | 节省比例 |
|------|---------|------------|----------|
| 文本生成 | ¥0.005/1K tokens | ¥20/1K tokens | **99.9%** |
| 代码生成 | ¥0.005/次 | ¥20/次 | **99.9%** |
| 内容分析 | ¥0.002/次 | ¥20/次 | **99.99%** |
| 翻译 | ¥0.001/1K字符 | ¥20/1K字符 | **99.99%** |

## 🎯 使用示例

### 写作场景
```
用户：我需要写一篇关于远程工作的文章

Claude：[使用glm_writer生成]
远程工作已成为新常态...

[生成的完整文章]
```

### 编程场景
```
用户：帮我写一个爬取网页的Python脚本

Claude：[使用glm_coder生成]
```python
import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    # [完整代码]
```

### 分析场景
```
用户：分析这段客户评论的情感

Claude：[使用glm_analyzer分析]
情感倾向：积极（85%置信度）
主要情感词汇：满意、推荐、优秀
...
```

## 🔧 配置说明

### API Key配置
```bash
# Linux/Mac
export GLM_API_KEY="your-api-key"

# Windows
set GLM_API_KEY=your-api-key
```

### Claude Code集成
Skills文件放在 `~/.claude/skills/` 目录下即可被Claude Code自动识别。

## 💡 使用技巧

1. **明确需求**：详细说明您想要什么
2. **提供上下文**：相关信息帮助获得更好的结果
3. **分步执行**：复杂任务可以分解成多个步骤
4. **迭代优化**：可以要求调整和改进结果
5. **成本控制**：简单任务可以指定使用更经济的模型

## ❓ 常见问题

**Q: 如何获取GLM API Key？**
A: 访问 https://open.bigmodel.cn/ 注册并获取

**Q: 技能不响应怎么办？**
A: 检查API Key是否正确设置，网络是否正常

**Q: 可以自定义技能吗？**
A: 可以，参考现有技能的格式创建新的.md文件

**Q: 如何控制使用成本？**
A: GLM已经非常便宜，但可以通过限制使用次数和长度进一步控制

## 🤝 贡献

欢迎提交新的技能创意和改进建议！

## 📄 许可证

MIT License - 可自由使用和修改