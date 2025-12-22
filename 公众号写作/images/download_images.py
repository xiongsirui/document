#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片下载脚本
使用Placeholder图片服务生成临时图片
"""

import requests
import os
from PIL import Image, ImageDraw, ImageFont
import io

def create_placeholder_image(filename, title, size=(800, 400)):
    """创建占位图片"""
    # 创建图片
    img = Image.new('RGB', size, color='#f0f0f0')
    draw = ImageDraw.Draw(img)

    # 绘制边框
    draw.rectangle([(10, 10), (size[0]-10, size[1]-10)], outline='#333333', width=2)

    # 尝试加载字体
    try:
        # Windows系统
        font_large = ImageFont.truetype('arial.ttf', 36)
        font_small = ImageFont.truetype('arial.ttf', 20)
    except:
        # 使用默认字体
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 绘制标题
    text_bbox = draw.textbbox((0, 0), title, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2

    draw.text((x, y), title, fill='#333333', font=font_large)

    # 添加副标题
    subtitle = f"图片文件名: {filename}"
    draw.text((20, size[1]-40), subtitle, fill='#666666', font=font_small)

    # 保存图片
    filepath = os.path.join(os.path.dirname(__file__), filename)
    img.save(filepath, 'JPEG', quality=90)
    print(f"生成图片: {filepath}")
    return filepath

# 图片配置
images_config = [
    {
        'filename': 'claude-code-agents-main.jpg',
        'title': 'Claude Code Agents\nAI编程助手界面',
        'size': (1200, 600)
    },
    {
        'filename': 'claude-code-architecture.jpg',
        'title': 'Claude Code Agents\n技术架构图',
        'size': (1000, 600)
    },
    {
        'filename': 'oauth-project-structure.jpg',
        'title': 'OAuth项目\n目录结构',
        'size': (800, 600)
    },
    {
        'filename': 'agent-workflow.jpg',
        'title': '多Agent协作\n工作流程',
        'size': (1000, 600)
    },
    {
        'filename': 'code-comparison.jpg',
        'title': '开发效率对比\n432倍提升',
        'size': (1000, 600)
    },
    {
        'filename': 'claude-code-collaboration.jpg',
        'title': '程序员与AI协作\n创造未来',
        'size': (1200, 600)
    }
]

def main():
    print("开始生成文章配图...\n")

    # 创建images目录（如果不存在）
    os.makedirs(os.path.dirname(__file__), exist_ok=True)

    # 生成所有图片
    for config in images_config:
        create_placeholder_image(
            config['filename'],
            config['title'],
            config.get('size', (800, 400))
        )

    print("\n所有配图生成完成！")
    print("\n使用说明：")
    print("1. 这些是占位图片，用于文章排版预览")
    print("2. 实际发布时建议从以下来源下载高清图片：")
    print("   - Unsplash (https://unsplash.com)")
    print("   - Pexels (https://www.pexels.com)")
    print("   - Pixabay (https://pixabay.com)")
    print("3. 搜索关键词建议：")
    for config in images_config:
        print(f"   - {config['filename']}: AI programming, architecture diagram, code structure")

if __name__ == "__main__":
    main()