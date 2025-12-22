#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载真实场景图片，类似claude-prompt-guide的风格
"""

import requests
import os
import json
from urllib.parse import quote

# Pexels API (免费，需要注册获取API key)
# 如果没有API key，可以使用下面的列表中的备用图片URL

# 真实场景图片URL列表（使用免费的图片服务）
REALISTIC_IMAGES = [
    {
        'filename': 'claude-code-agents-main.jpg',
        'urls': [
            'https://images.pexels.com/photos/57690/pexels-photo-57690.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # programmer working
            'https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # coding on laptop
            'https://images.pexels.com/photos/3184291/pexels-photo-3184291.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # developer workspace
        ],
        'description': 'AI编程助手工作场景'
    },
    {
        'filename': 'claude-code-architecture.jpg',
        'urls': [
            'https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # system architecture
            'https://images.pexels.com/photos/3861972/pexels-photo-3861972.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # network diagram
            'https://images.pexels.com/photos/714699/pexels-photo-714699.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # blueprint
        ],
        'description': '系统架构图'
    },
    {
        'filename': 'oauth-project-structure.jpg',
        'urls': [
            'https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # code on screen
            'https://images.pexels.com/photos/574071/pexels-photo-574071.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # programming
            'https://images.pexels.com/photos/5380642/pexels-photo-5380642.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # multiple screens
        ],
        'description': '项目代码结构'
    },
    {
        'filename': 'agent-workflow.jpg',
        'urls': [
            'https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # team collaboration
            'https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # meeting
            'https://images.pexels.com/photos/1181677/pexels-photo-1181677.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # workflow
        ],
        'description': '团队协作流程'
    },
    {
        'filename': 'code-comparison.jpg',
        'urls': [
            'https://images.pexels.com/photos/442150/pexels-photo-442150.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # data comparison
            'https://images.pexels.com/photos/3861968/pexels-photo-3861968.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # charts
            'https://images.pexels.com/photos/160107/pexels-photo-160107.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # statistics
        ],
        'description': '效率对比图表'
    },
    {
        'filename': 'claude-code-collaboration.jpg',
        'urls': [
            'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # AI and human
            'https://images.pexels.com/photos/3862130/pexels-photo-3862130.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # future technology
            'https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',  # innovation
        ],
        'description': '人机协作场景'
    }
]

def download_image(url, filename):
    """下载单个图片"""
    try:
        # 添加请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            filepath = os.path.join(os.path.dirname(__file__), filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)

            # 检查文件大小
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"下载成功: {filename} ({file_size:.1f}KB)")
            return True
        else:
            print(f"下载失败: {filename} - HTTP {response.status_code}")
    except Exception as e:
        print(f"下载错误: {filename} - {str(e)}")
    return False

def download_with_fallback(image_info):
    """使用备用URL下载图片"""
    print(f"\n正在下载: {image_info['description']}")
    print(f"文件名: {image_info['filename']}")

    for i, url in enumerate(image_info['urls'], 1):
        print(f"尝试 URL {i}/{len(image_info['urls'])}...")
        if download_image(url, image_info['filename']):
            return True
        print("失败，尝试下一个URL...")

    print(f"所有URL都失败了: {image_info['filename']}")
    return False

def create_placeholder_realistic(filename, title):
    """创建占位图（当所有URL都失败时）"""
    from PIL import Image, ImageDraw, ImageFont
    import random

    width, height = 1200, 600

    # 创建渐变背景
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # 使用更柔和的渐变
    for y in range(height):
        ratio = y / height
        r = int(30 + (60 - 30) * ratio)
        g = int(40 + (80 - 40) * ratio)
        b = int(60 + (120 - 60) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 添加噪点效果，模拟真实照片
    for _ in range(5000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        draw.point((x, y), fill=(255, 255, 255, random.randint(20, 60)))

    # 尝试加载字体
    try:
        font_title = ImageFont.truetype('arial.ttf', 48)
        font_subtitle = ImageFont.truetype('arial.ttf', 24)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()

    # 绘制标题
    text_bbox = draw.textbbox((0, 0), title, font=font_title)
    text_width = text_bbox[2] - text_bbox[0]
    x = (width - text_width) // 2
    y = height // 2 - 50

    # 添加阴影效果
    draw.text((x+2, y+2), title, fill=(0, 0, 0, 128), font=font_title)
    draw.text((x, y), title, fill=(255, 255, 255), font=font_title)

    # 添加副标题
    subtitle = "图片下载中，请稍后..."
    text_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    text_width = text_bbox[2] - text_bbox[0]
    x = (width - text_width) // 2
    y = height // 2 + 20

    draw.text((x, y), subtitle, fill=(200, 200, 200), font=font_subtitle)

    # 保存图片
    filepath = os.path.join(os.path.dirname(__file__), filename)
    img.save(filepath, 'JPEG', quality=85)
    print(f"创建占位图: {filename}")

def main():
    print("开始下载真实场景图片...\n")
    print("注：这些图片来自Pexels免费图库")
    print("如果下载失败，将创建占位图\n")

    success_count = 0
    total_count = len(REALISTIC_IMAGES)

    for image_info in REALISTIC_IMAGES:
        if download_with_fallback(image_info):
            success_count += 1
        else:
            # 如果所有URL都失败，创建占位图
            create_placeholder_realistic(
                image_info['filename'],
                image_info['description']
            )

    print(f"\n下载完成！")
    print(f"成功: {success_count}/{total_count}")

    print("\n图片说明：")
    print("1. 这些都是真实场景照片")
    print("2. 来自Pexels免费图库")
    print("3. 类似claude-prompt-guide的风格")
    print("4. 适合公众号文章使用")

    print("\n如果对图片不满意，可以手动访问以下网站搜索：")
    print("- Pexels: https://www.pexels.com")
    print("- Unsplash: https://unsplash.com")
    print("搜索关键词: 'coding', 'programming', 'developer', 'AI', 'technology'")

if __name__ == "__main__":
    main()