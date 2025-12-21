#!/bin/bash
# Claude Prompt进化史 - 图片下载脚本
# 使用 curl 下载所需配图

# 设置目标目录
TARGET_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "开始下载 Claude Prompt 进化史配图..."
echo "目标目录: $TARGET_DIR"
echo "=================================================="

# 图片列表
declare -A IMAGES=(
    ["01-main-image.jpg"]="https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=1200&h=630&fit=crop"
    ["02-talking-to-air.jpg"]="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&h=630&fit=crop"
    ["03-information-overload.jpg"]="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop"
    ["04-aha-moment.jpg"]="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&h=630&fit=crop"
    ["05-house-framework.jpg"]="https://images.unsplash.com/photo-1541888946145-d3c458132c8c?w=1200&h=630&fit=crop"
    ["06-perfect-understanding.jpg"]="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1200&h=630&fit=crop"
)

# 下载函数
download_image() {
    local filename="$1"
    local url="$2"
    local filepath="$TARGET_DIR/$filename"

    if [ -f "$filepath" ]; then
        echo "✓ $filename 已存在，跳过下载"
        return
    fi

    echo "正在下载 $filename..."
    if curl -L -s -o "$filepath" "$url"; then
        echo "✓ $filename 下载成功"
    else
        echo "✗ $filename 下载失败"
    fi
}

# 下载所有图片
for filename in "${!IMAGES[@]}"; do
    download_image "$filename" "${IMAGES[$filename]}"
    sleep 0.5  # 添加延迟
done

echo "=================================================="
echo "所有图片下载完成！"
echo ""
echo "图片说明:"
echo "1. 01-main-image.jpg - 两个人对话场景（主图）"
echo "2. 02-talking-to-air.jpg - 沟通障碍/对着空气说话"
echo "3. 03-information-overload.jpg - 信息过载/困惑"
echo "4. 04-aha-moment.jpg - 灵感瞬间/顿悟时刻"
echo "5. 05-house-framework.jpg - 建筑框架/结构思维"
echo "6. 06-perfect-understanding.jpg - 完美配合/心有灵犀"