#!/usr/bin/env python3
"""
Claude Prompt进化史 - 图片下载脚本
用于从免费图库批量下载所需的配图
"""

import os
import requests
import time
from urllib.parse import urlparse
from pathlib import Path

# 图片下载链接
IMAGE_URLS = {
    "01-main-image.jpg": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=1200&h=630&fit=crop",  # 沟通对话
    "02-talking-to-air.jpg": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&h=630&fit=crop",  # 沮丧沟通
    "03-information-overload.jpg": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop",  # 信息过载
    "04-aha-moment.jpg": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&h=630&fit=crop",  # 灯泡时刻
    "05-house-framework.jpg": "https://images.unsplash.com/photo-1541888946145-d3c458132c8c?w=1200&h=630&fit=crop",  # 建筑框架
    "06-perfect-understanding.jpg": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1200&h=630&fit=crop",  # 团队合作
}

def download_image(url: str, filename: str, target_dir: str):
    """下载单张图片"""
    try:
        # 创建目标目录
        Path(target_dir).mkdir(parents=True, exist_ok=True)

        # 完整文件路径
        file_path = os.path.join(target_dir, filename)

        # 检查文件是否已存在
        if os.path.exists(file_path):
            print(f"✓ {filename} 已存在，跳过下载")
            return

        print(f"正在下载 {filename}...")

        # 下载图片
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 保存文件
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✓ {filename} 下载成功")

    except Exception as e:
        print(f"✗ {filename} 下载失败: {str(e)}")

def main():
    """主函数"""
    target_dir = os.path.dirname(os.path.abspath(__file__))

    print("开始下载 Claude Prompt 进化史配图...")
    print(f"目标目录: {target_dir}")
    print("-" * 50)

    for filename, url in IMAGE_URLS.items():
        download_image(url, filename, target_dir)
        # 添加延迟，避免请求过于频繁
        time.sleep(0.5)

    print("-" * 50)
    print("所有图片下载完成！")
    print("\n图片说明:")
    print("1. 01-main-image.jpg - 两个人对话场景")
    print("2. 02-talking-to-air.jpg - 沟通障碍/沮丧")
    print("3. 03-information-overload.jpg - 信息过载")
    print("4. 04-aha-moment.jpg - 灵感瞬间")
    print("5. 05-house-framework.jpg - 建筑框架")
    print("6. 06-perfect-understanding.jpg - 完美配合")

if __name__ == "__main__":
    main()