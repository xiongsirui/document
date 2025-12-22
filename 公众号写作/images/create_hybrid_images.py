#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建混合风格图片：真实照片 + 科技感元素
结合claude-prompt-guide的真实照片感和编程主题
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO

# 真实照片URL（Pexels）
PHOTO_URLS = {
    'claude-code-agents-main.jpg': 'https://images.pexels.com/photos/57690/pexels-photo-57690.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'claude-code-architecture.jpg': 'https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'oauth-project-structure.jpg': 'https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'agent-workflow.jpg': 'https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'code-comparison.jpg': 'https://images.pexels.com/photos/442150/pexels-photo-442150.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
    'claude-code-collaboration.jpg': 'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'
}

# 对应的文字说明
TEXT_INFO = {
    'claude-code-agents-main.jpg': {
        'title': 'Claude Code Agents',
        'subtitle': 'AI驱动的编程革命',
        'code_snippets': [
            'const agent = new ClaudeCode();',
            'agent.mode = "development";',
            'agent.execute("build OAuth");'
        ]
    },
    'claude-code-architecture.jpg': {
        'title': 'Agent Architecture',
        'subtitle': '多代理协作系统',
        'code_snippets': [
            'Core → Context Memory',
            '→ Multiple Agents',
            '→ MCP Protocol'
        ]
    },
    'oauth-project-structure.jpg': {
        'title': 'OAuth Project',
        'subtitle': '认证系统架构',
        'code_snippets': [
            'POST /auth/login',
            'POST /auth/register',
            'POST /auth/refresh'
        ]
    },
    'agent-workflow.jpg': {
        'title': 'Agent Workflow',
        'subtitle': '并行开发流程',
        'code_snippets': [
            'Architect Agent → Design',
            'Backend Agent → Code',
            'Test Agent → Verify'
        ]
    },
    'code-comparison.jpg': {
        'title': '432x Efficiency',
        'subtitle': '开发效率对比',
        'code_snippets': [
            'Traditional: 9 days',
            'Claude Code: 30 mins',
            'Speedup: 432x'
        ]
    },
    'claude-code-collaboration.jpg': {
        'title': 'Human-AI Team',
        'subtitle': '未来开发模式',
        'code_snippets': [
            'Human: Ideas & Vision',
            'AI: Implementation',
            'Together: Innovation'
        ]
    }
}

def download_photo(url):
    """下载真实照片"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"下载照片失败: {e}")
    return None

def add_tech_overlay(image, filename):
    """在照片上添加科技感覆盖层"""
    # 创建覆盖层
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 添加半透明暗角效果
    width, height = image.size
    for i in range(10):
        alpha = 20 - i * 2
        draw.rectangle([i*20, i*20, width-i*20, height-i*20],
                      outline=(0, 0, 0, alpha), width=20)

    # 添加网格线
    grid_color = (100, 255, 218, 30)
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=grid_color)
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=grid_color)

    # 获取文字信息
    info = TEXT_INFO.get(filename, {})

    # 尝试加载字体
    try:
        font_title = ImageFont.truetype('arial.ttf', 56)
        font_subtitle = ImageFont.truetype('arial.ttf', 28)
        font_code = ImageFont.truetype('consola.ttf', 20)
    except:
        try:
            font_title = ImageFont.truetype('arial.ttf', 48)
            font_subtitle = ImageFont.truetype('arial.ttf', 24)
            font_code = ImageFont.load_default()
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_code = ImageFont.load_default()

    # 添加半透明背景条
    title_bg = Image.new('RGBA', (width, 200), (0, 0, 0, 150))
    overlay.paste(title_bg, (0, height - 300), title_bg)

    # 绘制标题
    if 'title' in info:
        title = info['title']
        # 添加发光效果
        for offset in [3, 2, 1]:
            color = (0, 0, 0, 100 - offset * 30)
            text_bbox = draw.textbbox((0, 0), title, font=font_title)
            text_width = text_bbox[2] - text_bbox[0]
            x = (width - text_width) // 2 + offset
            y = height - 250 + offset
            draw.text((x, y), title, fill=color, font=font_title)

        # 主标题
        text_bbox = draw.textbbox((0, 0), title, font=font_title)
        text_width = text_bbox[2] - text_bbox[0]
        x = (width - text_width) // 2
        y = height - 250
        draw.text((x, y), title, fill=(100, 255, 218), font=font_title)

    # 绘制副标题
    if 'subtitle' in info:
        subtitle = info['subtitle']
        text_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        text_width = text_bbox[2] - text_bbox[0]
        x = (width - text_width) // 2
        y = height - 180
        draw.text((x, y), subtitle, fill=(255, 255, 255), font=font_subtitle)

    # 添加代码片段
    if 'code_snippets' in info:
        y_pos = 50
        for code in info['code_snippets'][:3]:
            # 代码背景
            code_bg = Image.new('RGBA', (300, 30), (0, 0, 0, 120))
            overlay.paste(code_bg, (30, y_pos), code_bg)

            # 代码文字
            draw.text((40, y_pos + 5), code, fill=(100, 255, 218, 200), font=font_code)
            y_pos += 40

    # 添加装饰性元素
    draw.rectangle([20, 20, 60, 60], fill=(100, 255, 218, 200), outline=(255, 255, 255, 100))
    draw.rectangle([width-60, height-60, width-20, height-20],
                  fill=(255, 100, 100, 200), outline=(255, 255, 255, 100))

    # 合并图片
    image = image.convert('RGBA')
    result = Image.alpha_composite(image, overlay)

    return result.convert('RGB')

def create_hybrid_image(filename):
    """创建混合风格图片"""
    print(f"处理图片: {filename}")

    # 下载真实照片
    url = PHOTO_URLS.get(filename)
    if not url:
        print(f"没有找到 {filename} 的URL")
        return False

    photo = download_photo(url)
    if not photo:
        print(f"下载 {filename} 失败")
        return False

    # 调整图片大小
    photo = photo.resize((1200, 600), Image.Resampling.LANCZOS)

    # 添加科技感覆盖层
    result = add_tech_overlay(photo, filename)

    # 保存图片
    filepath = os.path.join(os.path.dirname(__file__), filename)
    result.save(filepath, 'JPEG', quality=90)

    # 检查文件大小
    file_size = os.path.getsize(filepath) / 1024  # KB
    print(f"创建成功: {filename} ({file_size:.1f}KB)")

    return True

def main():
    print("开始创建混合风格图片...\n")
    print("风格：真实照片 + 科技感元素\n")

    success_count = 0
    total_count = len(PHOTO_URLS)

    for filename in PHOTO_URLS.keys():
        if create_hybrid_image(filename):
            success_count += 1

    print(f"\n创建完成！")
    print(f"成功: {success_count}/{total_count}")

    print("\n图片特点：")
    print("1. 背景：真实的摄影作品")
    print("2. 覆盖：科技感代码元素")
    print("3. 效果：既有真实感又有技术感")
    print("4. 风格：类似claude-prompt-guide但更技术化")

    print("\n文件大小应该会在 60-100KB 之间")

if __name__ == "__main__":
    main()