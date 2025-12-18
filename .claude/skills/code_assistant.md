---
name: glm_coder
description: GLM驱动的编程助手，支持多种编程语言
author: GLM AI
version: 1.0.0
---

# GLM编程助手

专业的AI编程助手，使用GLM-4.6模型提供代码生成和解释服务。

## 主要功能

### 代码生成
根据需求生成完整代码。

**使用示例：**
```
请用glm_coder写一个Python函数实现快速排序算法
```

```
请用glm_coder用JavaScript创建一个待办事项应用
```

### 代码解释
解释复杂代码的工作原理。

**使用示例：**
```
请用glm_coder解释这段代码的作用：
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 代码优化
改进现有代码的性能和可读性。

**使用示例：**
```
请用glm_coder优化这段代码的性能：
for i in range(len(list)):
    for j in range(len(list)):
        if list[i] < list[j]:
            # swap
```

### 调试助手
帮助找出和修复代码中的错误。

**使用示例：**
```
请用glm_coder帮我找出这段代码的错误：
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # 当列表为空时会出错
```

### 单元测试生成
为代码生成测试用例。

**使用示例：**
```
请用glm_coder为这个函数生成单元测试：
def add(a, b):
    return a + b
```

## 支持的语言

- **Python** - 数据科学、Web开发、自动化
- **JavaScript** - 前端开发、Node.js
- **Java** - 企业级应用、Android
- **C++** - 系统编程、游戏开发
- **Go** - 云原生、微服务
- **Rust** - 系统编程、安全应用
- **SQL** - 数据库查询
- **HTML/CSS** - Web页面
- **Shell** - 系统管理脚本

## 特色功能

### 代码注释
自动生成详细的中文注释。

**使用示例：**
```
请用glm_coder为这段代码添加详细的中文注释
```

### 代码转换
在不同编程语言间转换代码。

**使用示例：**
```
请用glm_coder把这段Python代码转换成JavaScript：
def greet(name):
    return f"Hello, {name}!"
```

### 最佳实践
提供编程最佳实践建议。

**使用示例：**
```
请用glm_coder告诉我处理用户输入的最佳实践
```

## 使用技巧

1. **明确需求**：详细说明要实现的功能
2. **指定语言**：明确使用哪种编程语言
3. **提供上下文**：说明代码的用途和场景
4. **要求注释**：需要时可要求添加注释
5. **渐进式开发**：复杂功能可以分步实现

## 成本优势

- **代码生成**：¥0.005/次（Claude的1/4000）
- **代码解释**：¥0.002/次（Claude的1/10000）
- **批量处理**：支持多个文件同时处理

## 示例输出

生成代码时会包含：
- 完整的代码实现
- 详细的注释说明
- 使用示例
- 可能的错误处理
- 性能考虑

## 限制说明

- 生成的代码需要人工审查和测试
- 复杂算法可能需要多轮对话优化
- 建议在测试环境先运行验证