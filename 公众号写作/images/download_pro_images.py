#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载专业编程相关图片
使用 Placeholder 服务和专门的图片 API
"""

import requests
import os
from urllib.parse import quote

def download_from_placeholder(filename, query, size=(1200, 600)):
    """
    从 Placeholder 图片服务下载图片
    使用 https://placeholder.com/ 或类似服务
    """
    width, height = size

    # 生成带文字的占位图
    url = f"https://via.placeholder.com/{width}x{height}/1e3a8a/ffffff?text={quote(query)}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filepath = os.path.join(os.path.dirname(__file__), filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"下载成功: {filename}")
            return filepath
        else:
            print(f"下载失败: {filename} - HTTP {response.status_code}")
    except Exception as e:
        print(f"下载错误: {filename} - {str(e)}")
    return None

def download_from_lorem_picsum(filename, query, size=(1200, 600)):
    """
    从 Lorem Picsum 下载高质量随机图片
    """
    width, height = size
    # 使用固定的种子确保图片一致性
    seed = hash(query) % 1000
    url = f"https://picsum.photos/{width}/{height}?random={seed}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filepath = os.path.join(os.path.dirname(__file__), filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✅ 下载成功: {filename}")
            return filepath
    except Exception as e:
        print(f"❌ 下载错误: {filename} - {str(e)}")
    return None

# 专业图片搜索关键词映射
image_keywords = {
    'claude-code-agents-main.jpg': {
        'keywords': ['AI programming assistant', 'developer coding with AI', 'software development AI'],
        'description': 'AI编程助手界面'
    },
    'claude-code-architecture.jpg': {
        'keywords': ['software architecture diagram', 'system architecture', 'tech infrastructure'],
        'description': '系统架构图'
    },
    'oauth-project-structure.jpg': {
        'keywords': ['code structure', 'project files', 'development workspace'],
        'description': '项目代码结构'
    },
    'agent-workflow.jpg': {
        'keywords': ['workflow diagram', 'team collaboration', 'development process'],
        'description': '工作流程图'
    },
    'code-comparison.jpg': {
        'keywords': ['performance comparison', 'efficiency chart', 'productivity graph'],
        'description': '效率对比图表'
    },
    'claude-code-collaboration.jpg': {
        'keywords': ['human AI collaboration', 'pair programming', 'developer and AI'],
        'description': '人机协作场景'
    }
}

def create_custom_image(filename, title, subtitle=""):
    """
    创建自定义的编程主题图片
    """
    from PIL import Image, ImageDraw, ImageFont
    import random

    width, height = 1200, 600

    # 创建渐变背景
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # 深色渐变背景
    colors = [
        (26, 32, 44),   # 深蓝
        (45, 55, 72),   # 中蓝
        (74, 85, 104),  # 浅蓝
    ]

    for y in range(height):
        ratio = y / height
        if ratio < 0.5:
            # 深到中
            r = int(colors[0][0] * (1 - ratio*2) + colors[1][0] * ratio*2)
            g = int(colors[0][1] * (1 - ratio*2) + colors[1][1] * ratio*2)
            b = int(colors[0][2] * (1 - ratio*2) + colors[1][2] * ratio*2)
        else:
            # 中到浅
            ratio2 = (ratio - 0.5) * 2
            r = int(colors[1][0] * (1 - ratio2) + colors[2][0] * ratio2)
            g = int(colors[1][1] * (1 - ratio2) + colors[2][1] * ratio2)
            b = int(colors[1][2] * (1 - ratio2) + colors[2][2] * ratio2)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 添加网格线
    grid_color = (100, 116, 139, 50)
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=grid_color)
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=grid_color)

    # 添加代码装饰
    code_snippets = [
        "function createAgent() {",
        "  const ai = new ClaudeCode();",
        "  return ai.optimize();",
        "}",
        "",
        "class OAuthService {",
        "  authenticate(token) {",
        "    return jwt.verify(token);",
        "  }",
        "}"
    ]

    try:
        font_code = ImageFont.truetype('consola.ttf', 16)
        font_title = ImageFont.truetype('arial.ttf', 56)
        font_subtitle = ImageFont.truetype('arial.ttf', 28)
    except:
        font_code = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()

    # 绘制代码
    y = 100
    for line in code_snippets[:10]:
        draw.text((50, y), line, fill=(100, 255, 218, 100), font=font_code)
        y += 20

    # 绘制主标题
    if '\n' in title:
        lines = title.split('\n')
        y_pos = 300
        for line in lines:
            text_bbox = draw.textbbox((0, 0), line, font=font_title)
            text_width = text_bbox[2] - text_bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y_pos), line, fill=(255, 255, 255), font=font_title)
            y_pos += 65
    else:
        text_bbox = draw.textbbox((0, 0), title, font=font_title)
        text_width = text_bbox[2] - text_bbox[0]
        x = (width - text_width) // 2
        draw.text((x, 320), title, fill=(255, 255, 255), font=font_title)

    # 绘制副标题
    if subtitle:
        text_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        text_width = text_bbox[2] - text_bbox[0]
        x = (width - text_width) // 2
        draw.text((x, 450), subtitle, fill=(100, 255, 218), font=font_subtitle)

    # 添加装饰元素
    draw.rectangle([30, 30, 70, 70], fill=(100, 255, 218), outline=(255, 255, 255))
    draw.rectangle([width-70, height-70, width-30, height-30], fill=(255, 100, 100), outline=(255, 255, 255))

    # 保存图片
    filepath = os.path.join(os.path.dirname(__file__), filename)
    img.save(filepath, 'JPEG', quality=95)
    print(f"创建自定义图片: {filename}")
    return filepath

def main():
    print("开始下载/创建专业编程图片...\n")

    # 创建自定义编程主题图片
    custom_images = [
        ('claude-code-agents-main.jpg', 'Claude Code Agents', 'AI驱动的编程革命'),
        ('claude-code-architecture.jpg', 'Agent Architecture', '多代理协作系统'),
        ('oauth-project-structure.jpg', 'OAuth Project', '认证系统架构'),
        ('agent-workflow.jpg', 'Agent Workflow', '并行开发流程'),
        ('claude-code-collaboration.jpg', 'Human-AI Team', '未来开发模式'),
    ]

    for filename, title, subtitle in custom_images:
        create_custom_image(filename, title, subtitle)

    # 下载对比图
    download_from_placeholder(
        'code-comparison.jpg',
        '432x Faster Development',
        (1200, 600)
    )

    print("\n所有图片准备完成！")
    print("\n使用建议：")
    print("1. 这些图片专为编程文章设计")
    print("2. 包含代码元素和科技感")
    print("3. 自定义图片质量更高")
    print("\n如需真实图片，建议访问：")
    print("- Unsplash: https://unsplash.com (搜索: 'coding', 'programming')")
    print("- Pexels: https://www.pexels.com (支持中文搜索)")
    print("- Devicon: https://devicon.dev/ (编程语言图标)")

if __name__ == "__main__":
    main()