"""
Claude Code Skills 文章配图生成器
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 创建输出目录
output_dir = r"d:\code\ai\document\公众号写作\images\claude-skills"
os.makedirs(output_dir, exist_ok=True)

# 配色方案
COLORS = {
    'dark_blue': (26, 35, 126),
    'medium_blue': (74, 144, 226),
    'light_blue': (179, 229, 252),
    'purple': (156, 39, 176),
    'white': (255, 255, 255),
    'gray': (33, 33, 33),
    'light_gray': (245, 245, 245),
    'accent': (3, 169, 244),
    'green': (76, 175, 80),
    'orange': (255, 152, 0)
}

def create_main_image():
    """主图：Claude Code Skills概念图"""
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), COLORS['dark_blue'])
    draw = ImageDraw.Draw(img)

    # 背景网格
    for i in range(0, width, 50):
        draw.line([(i, 0), (i, height)], fill=(40, 50, 150), width=1)
    for i in range(0, height, 50):
        draw.line([(0, i), (width, i)], fill=(40, 50, 150), width=1)

    # 中心圆圈
    cx, cy = width // 2, height // 2
    for r in range(200, 50, -30):
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=COLORS['medium_blue'], width=3)

    # 中心文字
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 30)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    draw.text((cx, cy - 50), "SKILLS", fill=COLORS['white'], font=title_font, anchor="mm")
    draw.text((cx, cy + 30), "Claude Code", fill=COLORS['light_blue'], font=subtitle_font, anchor="mm")

    # 装饰性数据流线条
    for i in range(8):
        angle = i * 45
        import math
        x1 = cx + 150 * math.cos(math.radians(angle))
        y1 = cy + 150 * math.sin(math.radians(angle))
        x2 = cx + 220 * math.cos(math.radians(angle))
        y2 = cy + 220 * math.sin(math.radians(angle))
        draw.line([(x1, y1), (x2, y2)], fill=COLORS['accent'], width=4)
        draw.ellipse([x2-8, y2-8, x2+8, y2+8], fill=COLORS['white'])

    img.save(os.path.join(output_dir, "01-main.jpg"))
    print("[OK] Created main image")

def create_architecture_diagram():
    """渐进式披露架构示意图"""
    width, height = 1000, 800
    img = Image.new('RGB', (width, height), COLORS['light_gray'])
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
        title_font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    # 标题
    draw.text((50, 30), "Skills Progressive Disclosure Architecture", fill=COLORS['dark_blue'], font=title_font)

    # 第一层：元数据
    y1 = 100
    draw.rectangle([50, y1, 950, y1 + 150], fill=COLORS['green'], outline=COLORS['dark_blue'], width=3)
    draw.text((70, y1 + 20), "Layer 1: Metadata (Startup)", fill=COLORS['white'], font=font)
    draw.text((70, y1 + 60), "name: processing-pdfs", fill=COLORS['white'], font=font)
    draw.text((70, y1 + 95), "description: Extract text and tables from PDF files", fill=COLORS['white'], font=font)
    draw.text((70, y1 + 130), "Cost: ~100 tokens per skill", fill=COLORS['light_gray'], font=font)

    # 箭头
    draw.polygon([450, y1 + 160, 470, y1 + 180, 430, y1 + 180], fill=COLORS['gray'])

    # 第二层：SKILL.md
    y2 = y1 + 200
    draw.rectangle([50, y2, 950, y2 + 180], fill=COLORS['medium_blue'], outline=COLORS['dark_blue'], width=3)
    draw.text((70, y2 + 20), "Layer 2: SKILL.md (When triggered)", fill=COLORS['white'], font=font)
    draw.text((70, y2 + 60), "# PDF Processing Guide", fill=COLORS['white'], font=font)
    draw.text((70, y2 + 95), "- Use pdfplumber for text extraction", fill=COLORS['white'], font=font)
    draw.text((70, y2 + 130), "- Table recognition tips", fill=COLORS['white'], font=font)
    draw.text((70, y2 + 160), "Cost: <5000 tokens", fill=COLORS['light_gray'], font=font)

    # 箭头
    draw.polygon([450, y2 + 190, 470, y2 + 210, 430, y2 + 210], fill=COLORS['gray'])

    # 第三层：附加资源
    y3 = y2 + 230
    draw.rectangle([50, y3, 950, y3 + 220], fill=COLORS['purple'], outline=COLORS['dark_blue'], width=3)
    draw.text((70, y3 + 20), "Layer 3: Additional Resources (On-demand)", fill=COLORS['white'], font=font)
    draw.text((100, y3 + 60), "├── FORMS.md (Form filling guide)", fill=COLORS['white'], font=font)
    draw.text((100, y3 + 95), "├── REFERENCE.md (API reference)", fill=COLORS['white'], font=font)
    draw.text((100, y3 + 130), "├── EXAMPLES.md (Use cases)", fill=COLORS['white'], font=font)
    draw.text((100, y3 + 165), "└── scripts/ (Executable scripts)", fill=COLORS['white'], font=font)
    draw.text((70, y3 + 200), "Cost: Only when accessed", fill=COLORS['light_gray'], font=font)

    img.save(os.path.join(output_dir, "02-architecture.jpg"))
    print("[OK] Created architecture diagram")

def create_file_structure():
    """Skill文件结构图"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), COLORS['dark_blue'])
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("consolas.ttf", 20)
        title_font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    draw.text((50, 30), "Skill File Structure", fill=COLORS['white'], font=title_font)

    # 文件夹结构
    start_y = 100
    items = [
        ("my-skill/", True),
        ("  ├── SKILL.md", False, COLORS['green']),
        ("  ├── reference.md", False, COLORS['accent']),
        ("  ├── examples.md", False, COLORS['accent']),
        ("  └── scripts/", True),
        ("      ├── helper.py", False, COLORS['orange']),
        ("      └── validator.sh", False, COLORS['orange'])
    ]

    for item in items:
        color = COLORS['white'] if len(item) < 3 else item[2]
        draw.text((80, start_y), item[0], fill=color, font=font)
        start_y += 40

    img.save(os.path.join(output_dir, "03-file-structure.jpg"))
    print("[OK] Created file structure diagram")

def create_comparison_table():
    """Skills对比表格图"""
    width, height = 1200, 700
    img = Image.new('RGB', (width, height), COLORS['white'])
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
        header_font = ImageFont.truetype("arial.ttf", 22)
    except:
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()

    # 标题
    draw.text((50, 20), "Skills vs Other Approaches", fill=COLORS['dark_blue'], font=header_font)

    # 表头
    headers = ["Feature", "Skills", "CLAUDE.md", "Slash Commands", "MCP"]
    x_positions = [50, 200, 380, 560, 760]

    y = 70
    for i, header in enumerate(headers):
        draw.text((x_positions[i], y), header, fill=COLORS['white'], font=header_font)
    draw.rectangle([40, y-10, 1160, y+40], fill=COLORS['dark_blue'])

    # 表格内容
    rows = [
        ("Trigger", "Auto", "Project", "Manual", "Tool Call"),
        ("Reusable", "Cross-project", "Single project", "Single project", "Cross-project"),
        ("Token Eff.", "High", "Medium", "Low", "Varies"),
        ("Executable", "Yes", "No", "No", "Yes"),
        ("Complexity", "Medium", "Simple", "Simple", "Complex"),
        ("Best For", "Expertise", "Context", "Shortcuts", "External API")
    ]

    y += 60
    for row_idx, row in enumerate(rows):
        bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else COLORS['white']
        draw.rectangle([40, y-5, 1160, y+45], fill=bg_color, outline=(200, 200, 200))

        for i, cell in enumerate(row):
            color = COLORS['dark_blue']
            draw.text((x_positions[i], y), cell, fill=color, font=font)
        y += 50

    img.save(os.path.join(output_dir, "04-comparison.jpg"))
    print("[OK] Created comparison table")

def create_ending_image():
    """结尾配图"""
    width, height = 1200, 400
    img = Image.new('RGB', (width, height), COLORS['dark_blue'])
    draw = ImageDraw.Draw(img)

    # 装饰性背景
    for i in range(5):
        y = 50 + i * 70
        draw.rectangle([0, y, width, y+20], fill=(40, 50, 150))

    try:
        font = ImageFont.truetype("arial.ttf", 40)
        sub_font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # 文字
    draw.text((600, 150), "Start Building Your Skills", fill=COLORS['white'], font=font, anchor="mm")
    draw.text((600, 210), "Today: Create your first skill", fill=COLORS['light_blue'], font=sub_font, anchor="mm")
    draw.text((600, 250), "This week: Explore GitHub skills", fill=COLORS['light_blue'], font=sub_font, anchor="mm")
    draw.text((600, 290), "This month: Build your skills library", fill=COLORS['light_blue'], font=sub_font, anchor="mm")

    img.save(os.path.join(output_dir, "05-ending.jpg"))
    print("[OK] Created ending image")

if __name__ == "__main__":
    print("Generating Claude Code Skills article images...")
    create_main_image()
    create_architecture_diagram()
    create_file_structure()
    create_comparison_table()
    create_ending_image()
    print(f"\nAll images saved to: {output_dir}")
