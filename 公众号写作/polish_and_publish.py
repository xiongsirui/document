#!/usr/bin/env python3
"""
文章润色与一键发布工具 - 连接 document 与 AIWriteX

工作流程:
    1. 接收 document 生成的 Markdown 内容
    2. 调用 AIWriteX 进行润色和配图
    3. 输出精美的 HTML 文章
    4. 一键发布到公众号

使用方式:
    # 从文件润色
    python polish_and_publish.py input.md

    # 从文件润色并发布
    python polish_and_publish.py input.md --publish

    # 直接发布（跳过润色）
    python polish_and_publish.py input.html --publish-only

    # 指定公众号账号
    python polish_and_publish.py input.md --publish --account 0
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# 路径配置
DOCUMENT_ROOT = Path(__file__).parent
AIWRITEX_ROOT = Path("/Users/victoryx/code/AIWriteX")
OUTPUT_DIR = AIWRITEX_ROOT / "output" / "article"
TEMP_DIR = AIWRITEX_ROOT / "temp"

# API 配置
AIWRITEX_API = "http://127.0.0.1:8000"


def call_aiwritex_polish(title: str, content: str):
    """调用 AIWriteX 进行润色和配图"""
    print(f"🎨 正在调用 AIWriteX 润色文章...")
    print(f"   标题: {title}")

    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file = TEMP_DIR / f"input_{timestamp}.md"

    temp_file.write_text(content, encoding="utf-8")
    print(f"📝 临时文件: {temp_file}")

    cmd = [
        sys.executable,
        str(AIWRITEX_ROOT / "main.py"),
        "--input", str(temp_file),
        "--title", title,
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(AIWRITEX_ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            print("✅ AIWriteX 处理完成")
            temp_file.unlink()
            return find_output_file(title)
        else:
            print(f"❌ AIWriteX 处理失败: {result.stderr}")
            return None

    except Exception as e:
        print(f"❌ 调用 AIWriteX 出错: {e}")
        return None


def publish_to_wechat(article_path: str, account_index: int = 0):
    """一键发布到微信公众号"""
    print(f"\n📤 正在发布到公众号...")

    try:
        import requests

        url = f"{AIWRITEX_API}/api/articles/publish"
        payload = {
            "article_paths": [article_path],
            "account_indices": [account_index],
            "platform": "wechat"
        }

        response = requests.post(url, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()

            if result.get("success_count", 0) > 0:
                print(f"✅ 发布成功!")
                return True, "发布成功"
            else:
                errors = result.get("error_details", ["未知错误"])
                print(f"❌ 发布失败: {errors}")
                return False, errors
        else:
            error = response.json().get("detail", "API 调用失败")
            print(f"❌ 发布失败: {error}")
            return False, error

    except Exception as e:
        print(f"❌ 发布出错: {e}")
        return False, str(e)


def get_wechat_accounts():
    """获取已配置的微信公众号账号列表"""
    try:
        import requests

        url = f"{AIWRITEX_API}/api/articles/platforms"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            result = response.json()
            platforms = result.get("data", [])

            for platform in platforms:
                if platform["id"] == "wechat":
                    return platform.get("accounts", [])

        return []

    except Exception:
        return []


def find_output_file(title: str):
    """查找 AIWriteX 生成的输出文件"""
    if not OUTPUT_DIR.exists():
        return None

    html_files = list(OUTPUT_DIR.glob("*.html"))
    if not html_files:
        return None

    for f in html_files:
        if title in f.stem:
            return f

    html_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return html_files[0]


def parse_markdown_file(file_path: Path):
    """解析 Markdown 文件，提取标题和内容"""
    content = file_path.read_text(encoding="utf-8")

    lines = content.split("\n")
    title = "无标题"

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            break

    return title, content


def main():
    parser = argparse.ArgumentParser(
        description="文章润色与一键发布工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 润色文章
  python polish_and_publish.py article.md

  # 润色并发布
  python polish_and_publish.py article.md --publish

  # 直接发布已有文章
  python polish_and_publish.py article.html --publish-only

  # 查看可用账号
  python polish_and_publish.py --list-accounts
        """
    )

    parser.add_argument("input", nargs="?", help="输入文件路径")
    parser.add_argument("--publish", action="store_true", help="润色后自动发布")
    parser.add_argument("--publish-only", action="store_true", help="跳过润色，直接发布")
    parser.add_argument("--account", type=int, default=0, help="公众号账号索引 (默认: 0)")
    parser.add_argument("--title", help="指定标题")
    parser.add_argument("--list-accounts", action="store_true", help="列出可用账号")

    args = parser.parse_args()

    # 列出账号
    if args.list_accounts:
        accounts = get_wechat_accounts()
        if accounts:
            print("\n📱 已配置的公众号账号:")
            for acc in accounts:
                print(f"   [{acc['index']}] {acc['author']}")
        else:
            print("\n❌ 未找到已配置的公众号账号")
            print("   请在 AIWriteX 中配置微信公众号 credentials")
        return

    # 检查输入
    if not args.input:
        parser.print_help()
        sys.exit(1)

    file_path = Path(args.input)
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)

    # 获取标题
    if file_path.suffix.lower() == ".md":
        title, content = parse_markdown_file(file_path)
    else:
        title = file_path.stem.replace("_", "|")
        content = file_path.read_text(encoding="utf-8")

    if args.title:
        title = args.title

    print(f"\n📄 文章信息:")
    print(f"   标题: {title}")
    print(f"   文件: {file_path}")
    print(f"   字数: {len(content)}")

    # 流程选择
    if args.publish_only:
        article_path = str(file_path.absolute())
    else:
        output_path = call_aiwritex_polish(title, content)
        if not output_path:
            print(f"\n❌ 润色失败")
            sys.exit(1)
        article_path = str(output_path)
        print(f"   输出: {output_path}")

    # 发布
    if args.publish or args.publish_only:
        success, message = publish_to_wechat(article_path, args.account)

        if success:
            print(f"\n🎉 完成! 文章已发布到公众号")
        else:
            print(f"\n❌ 发布失败: {message}")
            sys.exit(1)
    else:
        print(f"\n✅ 润色完成!")
        print(f"💡 使用 --publish 参数一键发布到公众号")


if __name__ == "__main__":
    main()
