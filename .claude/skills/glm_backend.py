"""
GLM API Backend Server
为Claude Code Skills提供GLM-4.6模型调用服务
"""

from flask import Flask, request, jsonify
from zhipuai import ZhipuAI
import os
import logging
from datetime import datetime

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化GLM客户端
API_KEY = os.getenv("GLM_API_KEY")
if not API_KEY:
    print("❌ 错误：未设置 GLM_API_KEY 环境变量")
    print("\n请设置您的GLM API Key:")
    print("export GLM_API_KEY='your-api-key'")
    print("\n获取API Key: https://open.bigmodel.cn/")

client = ZhipuAI(api_key=API_KEY) if API_KEY else None

# 统计信息
stats = {
    "total_requests": 0,
    "total_tokens": 0,
    "total_cost": 0.0,
    "start_time": datetime.now()
}

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "model": "glm-4.6",
        "api_key_set": bool(API_KEY),
        "stats": stats
    })

@app.route('/api/generate', methods=['POST'])
def generate_text():
    """调用GLM-4.6生成文本"""
    if not client:
        return jsonify({
            "success": False,
            "error": "GLM API Key未配置"
        }), 400

    try:
        data = request.json
        prompt = data.get("prompt", "")
        system_prompt = data.get("system", "你是一个专业的写作助手")
        max_tokens = data.get("max_tokens", 2000)
        model = data.get("model", "glm-4.6")
        temperature = data.get("temperature", 0.7)

        if not prompt:
            return jsonify({
                "success": False,
                "error": "缺少prompt参数"
            }), 400

        logger.info(f"收到请求：{prompt[:50]}...")

        # 调用GLM API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        content = response.choices[0].message.content
        usage = response.usage

        # 更新统计
        stats["total_requests"] += 1
        stats["total_tokens"] += usage.total_tokens

        # 计算成本（GLM-4.6价格）
        cost_per_1k = {
            "glm-4.6": 0.005,
            "glm-4.5": 0.0014,
            "glm-3-turbo": 0.0005
        }
        cost = (usage.total_tokens / 1000) * cost_per_1k.get(model, 0.005)
        stats["total_cost"] += cost

        logger.info(f"生成成功，使用 {usage.total_tokens} tokens")

        return jsonify({
            "success": True,
            "content": content,
            "model": model,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            },
            "cost": cost,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"生成失败：{e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """文本分析"""
    if not client:
        return jsonify({
            "success": False,
            "error": "GLM API Key未配置"
        }), 400

    try:
        data = request.json
        text = data.get("text", "")
        analysis_type = data.get("type", "summary")

        prompts = {
            "summary": "请总结以下文本的主要内容：",
            "keywords": "请提取以下文本的关键词：",
            "sentiment": "请分析以下文本的情感倾向：",
            "style": "请分析以下文本的写作风格："
        }

        prompt = prompts.get(analysis_type, prompts["summary"]) + f"\n\n{text}"

        response = client.chat.completions.create(
            model="glm-4.5",  # 分析使用较便宜的模型
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return jsonify({
            "success": True,
            "analysis": response.choices[0].message.content,
            "type": analysis_type
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """获取使用统计"""
    runtime = datetime.now() - stats["start_time"]
    return jsonify({
        "total_requests": stats["total_requests"],
        "total_tokens": stats["total_tokens"],
        "total_cost": stats["total_cost"],
        "runtime_hours": runtime.total_seconds() / 3600,
        "avg_cost_per_request": stats["total_cost"] / max(1, stats["total_requests"])
    })

if __name__ == '__main__':
    if not API_KEY:
        print("\n⚠️  警告：未检测到GLM_API_KEY")
        print("服务将启动但无法调用GLM API\n")

    print("🚀 GLM API Backend Server 启动中...")
    print("📍 服务地址：http://localhost:5000")
    print("📊 健康检查：http://localhost:5000/health")
    print("📈 统计信息：http://localhost:5000/stats")
    print("\n按 Ctrl+C 停止服务\n")

    app.run(host='0.0.0.0', port=5000, debug=True)