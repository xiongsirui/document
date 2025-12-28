#!/usr/bin/env python3
"""
生成 Sleepless Agent 文章配图
使用 PIL 创建风格化的示意图
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_gradient(width, height, color1, color2):
    """创建渐变背景"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))

    return img

def create_main_cover():
    """生成封面图 - Sleepless Agent 概念"""
    width, height = 1920, 1080

    # 深色渐变背景
    img = create_gradient(width, height, (10, 15, 30), (5, 10, 25))
    draw = ImageDraw.Draw(img)

    # 添加网格线
    for i in range(0, width, 100):
        draw.line([(i, 0), (i, height)], fill=(30, 40, 60, 50), width=1)
    for i in range(0, height, 100):
        draw.line([(0, i), (width, i)], fill=(30, 40, 60, 50), width=1)

    # 左侧：睡眠的人形轮廓 (简化)
    # 月亮图标
    draw.ellipse([(150, 150), (350, 350)], fill=(40, 50, 80), outline=(100, 150, 255, 200), width=3)

    # 右侧：工作中的 AI (发光效果)
    # AI 核心圆
    center_x, center_y = 1400, 300
    for r in range(150, 50, -10):
        alpha = int(255 * (1 - r / 150))
        draw.ellipse([(center_x - r, center_y - r), (center_x + r, center_y + r)],
                     fill=(0, 100, 255, 20), outline=(0, 150, 255, 100))

    # 代码流效果
    for i in range(10):
        x = 1200 + i * 60
        y_start = 350
        for j in range(20):
            y = y_start + j * 30
            length = 30 + (j % 3) * 20
            alpha = 255 - j * 10
            if alpha > 0:
                draw.rectangle([(x, y), (x + length, y + 15)],
                              fill=(0, 200, 255, alpha))

    # 底部文字区域
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    draw.text((960, 700), "Sleepless Agent", fill=(255, 255, 255), anchor="mm", font=title_font)
    draw.text((960, 800), "24/7 AI Development Team", fill=(100, 200, 255), anchor="mm", font=subtitle_font)

    return img

def create_multi_agent_workflow():
    """生成多代理工作流图"""
    width, height = 1920, 1080

    img = create_gradient(width, height, (15, 20, 35), (8, 12, 28))
    draw = ImageDraw.Draw(img)

    # 标题
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        label_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    draw.text((960, 80), "Three-Agent Workflow", fill=(255, 255, 255), anchor="mm", font=title_font)

    # 三个 Agent 节点
    agents = [
        {"name": "PLANNER", "x": 320, "y": 350, "color": (255, 150, 50), "desc": "分析任务\n制定计划"},
        {"name": "WORKER", "x": 960, "y": 350, "color": (50, 200, 150), "desc": "执行任务\n编写代码"},
        {"name": "EVALUATOR", "x": 1600, "y": 350, "color": (100, 150, 255), "desc": "验证结果\n质量检查"}
    ]

    # 绘制连接箭头
    draw.line([(480, 350), (780, 350)], fill=(100, 150, 200), width=4)
    draw.line([(1140, 350), (1440, 350)], fill=(100, 150, 200), width=4)

    # 箭头头部
    draw.polygon([(780, 350), (760, 340), (760, 360)], fill=(100, 150, 200))
    draw.polygon([(1440, 350), (1420, 340), (1420, 360)], fill=(100, 150, 200))

    # 绘制 Agent 框
    for agent in agents:
        x, y = agent["x"], agent["y"]
        color = agent["color"]

        # 外框发光效果
        for offset in range(20, 0, -5):
            alpha = int(50 * (1 - offset / 20))
            draw.rectangle([(x - 160 - offset, y - 100 - offset),
                          (x + 160 + offset, y + 100 + offset)],
                         outline=(*color, alpha), width=2)

        # 主框
        draw.rectangle([(x - 160, y - 100), (x + 160, y + 100)],
                      fill=(*color, 30), outline=color, width=4)

        # 文字
        draw.text((x, y - 20), agent["name"], fill=color, anchor="mm", font=label_font)
        draw.text((x, y + 30), agent["desc"], fill=(200, 200, 200), anchor="mm", font=label_font)

    # 底部说明
    draw.text((960, 550), "协作流程：规划 → 执行 → 验证",
             fill=(150, 180, 220), anchor="mm", font=label_font)
    draw.text((960, 620), "确保代码质量和任务完整性",
             fill=(120, 150, 180), anchor="mm", font=label_font)

    return img

def create_quickstart_guide():
    """生成快速上手指南图"""
    width, height = 1920, 1080

    img = create_gradient(width, height, (12, 18, 32), (6, 10, 24))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        step_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except:
        title_font = ImageFont.load_default()
        step_font = ImageFont.load_default()

    draw.text((960, 80), "Quick Start Guide", fill=(255, 255, 255), anchor="mm", font=title_font)

    # 8 个步骤
    steps = [
        "1. Install Claude Code CLI",
        "2. Clone Sleepless Agent",
        "3. Install Python Dependencies",
        "4. Create GitHub Token",
        "5. Configure config.yaml",
        "6. Setup GitHub CLI",
        "7. Run First Task",
        "8. Start Daemon (Optional)"
    ]

    y_start = 200
    for i, step in enumerate(steps):
        y = y_start + i * 100

        # 步骤编号圆圈
        draw.ellipse([(150, y - 35), (210, y + 35)],
                    fill=(0, 150, 255), outline=(100, 200, 255), width=3)
        draw.text((180, y), str(i + 1), fill=(255, 255, 255), anchor="mm", font=step_font)

        # 步骤文字
        draw.text((280, y), step, fill=(200, 220, 255), anchor="lm", font=step_font)

        # 连接线
        if i < len(steps) - 1:
            draw.line([(180, y + 40), (180, y + 60)], fill=(80, 120, 180), width=2)

    # 右侧提示框
    draw.rectangle([(1100, 200), (1800, 900)],
                  fill=(0, 100, 200, 20), outline=(0, 150, 255), width=3)

    tips = [
        "⚠️ Prerequisites:",
        "",
        "• Claude Max Subscription",
        "• Python 3.10+",
        "• Git & GitHub Account",
        "",
        "✨ Time to complete:",
        "",
        "Approximately 10-15 minutes",
        "",
        "📖 Full guide in article"
    ]

    y_tip = 250
    for tip in tips:
        draw.text((1200, y_tip), tip, fill=(180, 200, 230), anchor="lm", font=step_font)
        y_tip += 50

    return img

def create_scenarios():
    """生成适用场景图"""
    width, height = 1920, 1080

    img = create_gradient(width, height, (10, 16, 30), (5, 10, 25))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        item_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        item_font = ImageFont.load_default()

    draw.text((960, 60), "When to Use Sleepless Agent", fill=(255, 255, 255), anchor="mm", font=title_font)

    # 左侧：适合的场景
    draw.text((480, 180), "✅ Great For", fill=(100, 255, 150), anchor="mm", font=header_font)

    suitable = [
        "Side Projects",
        "• Ideas while sleeping",
        "• Nightly code generation",
        "",
        "Technical Debt",
        "• Add tests",
        "• Refactor code",
        "• Update docs",
        "",
        "Batch Tasks",
        "• License headers",
        "• API migrations",
        "",
        "Tools & Scripts",
        "• CLI tools",
        "• Automation"
    ]

    y = 260
    for item in suitable:
        draw.text((200, y), item, fill=(180, 230, 200), anchor="lm", font=item_font)
        y += 50

    # 右侧：不适合的场景
    draw.text((1440, 180), "❌ Not For", fill=(255, 100, 100), anchor="mm", font=header_font)

    not_suitable = [
        "Enterprise Projects",
        "• Complex workflows",
        "• Multi-team collab",
        "",
        "High Interaction",
        "• Frequent changes",
        "• Real-time feedback",
        "",
        "Custom Logic",
        "• Business-specific",
        "• Domain knowledge"
    ]

    y = 260
    for item in not_suitable:
        draw.text((1100, y), item, fill=(230, 180, 180), anchor="lm", font=item_font)
        y += 50

    # 底部总结
    draw.rectangle([(200, 850), (1720, 1000)],
                  fill=(0, 80, 150, 30), outline=(0, 120, 200), width=2)
    draw.text((960, 925), "Best for: Well-defined tasks that can run independently",
             fill=(150, 200, 255), anchor="mm", font=item_font)

    return img

def create_conclusion():
    """生成结尾图"""
    width, height = 1920, 1080

    img = create_gradient(width, height, (8, 14, 28), (3, 8, 22))
    draw = ImageDraw.Draw(img)

    # 添加一些装饰性光点
    import random
    random.seed(42)
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(2, 6)
        alpha = random.randint(20, 80)
        draw.ellipse([(x, y), (x + size, y + size)], fill=(100, 180, 255, alpha))

    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # 主标题
    draw.text((960, 300), "The Future of Development", fill=(255, 255, 255), anchor="mm", font=title_font)

    # 副标题
    draw.text((960, 420), "AI isn't replacing you.",
             fill=(150, 200, 255), anchor="mm", font=text_font)
    draw.text((960, 480), "It's becoming your team.",
             fill=(150, 200, 255), anchor="mm", font=text_font)

    # 分隔线
    draw.line([(560, 560), (1360, 560)], fill=(80, 150, 220), width=2)

    # 底部信息
    draw.text((960, 680), "You define requirements → AI builds → You review",
             fill=(180, 200, 230), anchor="mm", font=text_font)

    draw.text((960, 780), "This is human-AI collaboration, done right.",
             fill=(120, 170, 220), anchor="mm", font=small_font)

    # GitHub 链接提示
    draw.text((960, 900), "github.com/context-machine-lab/sleepless-agent",
             fill=(100, 180, 255), anchor="mm", font=small_font)

    return img

# 生成所有图片
if __name__ == "__main__":
    output_dir = "/Users/victoryx/code/document/公众号写作/images/sleepless-agent"

    print("Generating images...")

    print("1. Creating main cover...")
    img1 = create_main_cover()
    img1.save(f"{output_dir}/01-main.jpg", quality=95)
    print("   ✓ Saved 01-main.jpg")

    print("2. Creating multi-agent workflow...")
    img2 = create_multi_agent_workflow()
    img2.save(f"{output_dir}/02-multi-agent.jpg", quality=95)
    print("   ✓ Saved 02-multi-agent.jpg")

    print("3. Creating quickstart guide...")
    img3 = create_quickstart_guide()
    img3.save(f"{output_dir}/03.5-quickstart.jpg", quality=95)
    print("   ✓ Saved 03.5-quickstart.jpg")

    print("4. Creating scenarios...")
    img4 = create_scenarios()
    img4.save(f"{output_dir}/03-scenarios.jpg", quality=95)
    print("   ✓ Saved 03-scenarios.jpg")

    print("5. Creating conclusion...")
    img5 = create_conclusion()
    img5.save(f"{output_dir}/04-conclusion.jpg", quality=95)
    print("   ✓ Saved 04-conclusion.jpg")

    print("\n✅ All images generated successfully!")
