#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建更有视觉冲击力的配图
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random
import math

def create_gradient_image(size, start_color, end_color, direction='vertical'):
    """创建渐变背景"""
    width, height = size
    image = Image.new('RGB', size)
    draw = ImageDraw.Draw(image)

    if direction == 'vertical':
        for y in range(height):
            ratio = y / height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:
        for x in range(width):
            ratio = x / width
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))

    return image

def add_tech_pattern(image, pattern_type='grid'):
    """添加科技感图案"""
    width, height = image.size
    draw = ImageDraw.Draw(image)

    if pattern_type == 'grid':
        # 网格线
        for x in range(0, width, 30):
            draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 30))
        for y in range(0, height, 30):
            draw.line([(0, y), (width, y)], fill=(255, 255, 255, 30))

    elif pattern_type == 'dots':
        # 点阵
        for x in range(20, width, 40):
            for y in range(20, height, 40):
                draw.ellipse([(x-2, y-2), (x+2, y+2)], fill=(255, 255, 255, 50))

    elif pattern_type == 'circles':
        # 同心圆
        center_x, center_y = width // 2, height // 2
        for radius in range(50, max(width, height), 50):
            draw.ellipse(
                [(center_x - radius, center_y - radius),
                 (center_x + radius, center_y + radius)],
                outline=(255, 255, 255, 20)
            )

def create_tech_image(filename, title, subtitle="", colors=None):
    """创建科技感图片"""
    if colors is None:
        colors = {
            'primary': (0, 116, 217),    # 蓝色
            'secondary': (255, 65, 54),   # 红色
            'accent': (46, 204, 113),     # 绿色
            'dark': (44, 62, 80),         # 深蓝灰
            'light': (236, 240, 241)      # 浅灰
        }

    # 创建画布
    img = Image.new('RGB', (1200, 600), colors['dark'])
    draw = ImageDraw.Draw(img)

    # 添加渐变背景
    gradient = create_gradient_image(
        (1200, 600),
        (30, 40, 50),
        (60, 80, 100),
        'vertical'
    )
    img.paste(gradient, (0, 0))

    # 添加科技图案
    add_tech_pattern(img, 'grid')

    # 尝试加载字体
    try:
        font_title = ImageFont.truetype('arial.ttf', 60)
        font_subtitle = ImageFont.truetype('arial.ttf', 30)
        font_small = ImageFont.truetype('arial.ttf', 20)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 绘制标题背景
    title_height = 120
    title_bg = Image.new('RGBA', (1200, title_height), (0, 0, 0, 100))
    img.paste(title_bg, (0, 240), title_bg)

    # 绘制主标题
    if '\n' in title:
        lines = title.split('\n')
        y_pos = 260
        for line in lines:
            text_bbox = draw.textbbox((0, 0), line, font=font_title)
            text_width = text_bbox[2] - text_bbox[0]
            x = (1200 - text_width) // 2
            draw.text((x, y_pos), line, fill=colors['light'], font=font_title)
            y_pos += 70
    else:
        text_bbox = draw.textbbox((0, 0), title, font=font_title)
        text_width = text_bbox[2] - text_bbox[0]
        x = (1200 - text_width) // 2
        draw.text((x, 280), title, fill=colors['light'], font=font_title)

    # 绘制副标题
    if subtitle:
        text_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        text_width = text_bbox[2] - text_bbox[0]
        x = (1200 - text_width) // 2
        draw.text((x, 400), subtitle, fill=colors['primary'], font=font_subtitle)

    # 添加装饰元素
    draw.rectangle([(50, 50), (150, 150)], outline=colors['primary'], width=3)
    draw.rectangle([(1050, 450), (1150, 550)], outline=colors['accent'], width=3)

    # 添加代码装饰
    code_lines = [
        "def oauth_service():",
        "    user = authenticate()",
        "    token = generate_jwt(user)",
        "    return {'token': token}"
    ]
    y_pos = 50
    for line in code_lines:
        draw.text((50, y_pos), line, fill=(255, 255, 255, 80), font=font_small)
        y_pos += 25

    # 保存图片
    filepath = os.path.join(os.path.dirname(__file__), filename)
    img.save(filepath, 'JPEG', quality=95)
    print(f"创建科技感图片: {filepath}")
    return filepath

def create_chart_image(filename, title, data):
    """创建图表图片"""
    width, height = 1200, 600
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 背景
    gradient = create_gradient_image((width, height), (240, 240, 240), (255, 255, 255), 'vertical')
    img.paste(gradient, (0, 0))

    try:
        font_title = ImageFont.truetype('arial.ttf', 48)
        font_label = ImageFont.truetype('arial.ttf', 24)
        font_data = ImageFont.truetype('arial.ttf', 32)
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_data = ImageFont.load_default()

    # 标题
    text_bbox = draw.textbbox((0, 0), title, font=font_title)
    text_width = text_bbox[2] - text_bbox[0]
    x = (width - text_width) // 2
    draw.text((x, 40), title, fill=(0, 116, 217), font=font_title)

    # 绘制柱状图
    bar_width = 150
    spacing = 200
    start_x = (width - (len(data) * bar_width + (len(data) - 1) * spacing)) // 2
    start_y = 450

    max_value = max(item['value'] for item in data)
    scale = 300 / max_value

    colors = [(0, 116, 217), (255, 65, 54), (46, 204, 113), (255, 193, 7)]

    for i, item in enumerate(data):
        x = start_x + i * (bar_width + spacing)
        bar_height = int(item['value'] * scale)
        y = start_y - bar_height

        # 柱子
        draw.rectangle(
            [(x, y), (x + bar_width, start_y)],
            fill=colors[i % len(colors)]
        )

        # 数值
        value_text = f"{item['value']}x"
        text_bbox = draw.textbbox((0, 0), value_text, font=font_data)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (bar_width - text_width) // 2
        draw.text((text_x, y - 40), value_text, fill=(0, 0, 0), font=font_data)

        # 标签
        text_bbox = draw.textbbox((0, 0), item['label'], font=font_label)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (bar_width - text_width) // 2
        draw.text((text_x, start_y + 20), item['label'], fill=(0, 0, 0), font=font_label)

    # 保存
    filepath = os.path.join(os.path.dirname(__file__), filename)
    img.save(filepath, 'JPEG', quality=95)
    print(f"创建图表图片: {filepath}")
    return filepath

# 创建图片配置
images = [
    {
        'filename': 'claude-code-agents-main.jpg',
        'title': 'Claude Code Agents',
        'subtitle': 'AI编程助手，重新定义开发效率',
        'type': 'tech'
    },
    {
        'filename': 'claude-code-architecture.jpg',
        'title': 'Agent架构',
        'subtitle': '上下文持久化 + 多代理协作 + MCP协议',
        'type': 'tech'
    },
    {
        'filename': 'oauth-project-structure.jpg',
        'title': 'OAuth项目结构',
        'subtitle': 'FastAPI + PostgreSQL + Redis',
        'type': 'tech'
    },
    {
        'filename': 'agent-workflow.jpg',
        'title': '多Agent协作',
        'subtitle': '架构师 + 后端 + 前端 + 测试 + 安全',
        'type': 'tech'
    },
    {
        'filename': 'code-comparison.jpg',
        'title': '开发效率对比',
        'subtitle': '432倍效率提升',
        'type': 'chart',
        'data': [
            {'label': '传统开发', 'value': 432},
            {'label': 'Claude Code', 'value': 1}
        ]
    },
    {
        'filename': 'claude-code-collaboration.jpg',
        'title': '人机协作',
        'subtitle': '人类负责创意，AI负责实现',
        'type': 'tech'
    }
]

def main():
    print("开始创建有视觉冲击力的配图...\n")

    for img_config in images:
        if img_config['type'] == 'tech':
            create_tech_image(
                img_config['filename'],
                img_config['title'],
                img_config['subtitle']
            )
        elif img_config['type'] == 'chart':
            create_chart_image(
                img_config['filename'],
                img_config['title'],
                img_config['data']
            )

    print("\n所有图片创建完成！")
    print("\n新图片特点：")
    print("1. 渐变背景，更有层次感")
    print("2. 科技感网格图案")
    print("3. 鲜明的色彩对比")
    print("4. 清晰的信息层级")
    print("5. 装饰性代码元素")

if __name__ == "__main__":
    main()