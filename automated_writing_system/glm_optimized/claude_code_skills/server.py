"""
GLM自动化写作系统 - MCP Server (独立版本)
基于Model Context Protocol实现Claude Code原生Skills
"""

import asyncio
import json
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP imports
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource, Tool, TextContent, ImageContent, EmbeddedResource,
        LoggingLevel
    )
    MCP_AVAILABLE = True
except ImportError:
    logger.error("MCP library not found. Please install: pip install mcp")
    MCP_AVAILABLE = False

# GLM imports
try:
    from zhipuai import ZhipuAI
    GLM_AVAILABLE = True
except ImportError:
    logger.error("GLM library not found. Please install: pip install zhipuai")
    GLM_AVAILABLE = False

class GLMMCPServer:
    """GLM MCP服务器"""

    def __init__(self):
        if not MCP_AVAILABLE or not GLM_AVAILABLE:
            raise ImportError("Required libraries not installed")

        self.server = Server("glm-writing-system")
        self.client = None
        self._setup_client()
        self._register_tools()

    def _setup_client(self):
        """设置GLM客户端"""
        api_key = os.getenv("GLM_API_KEY")
        if not api_key:
            raise ValueError("GLM_API_KEY environment variable is required")
        self.client = ZhipuAI(api_key=api_key)

    def _register_tools(self):
        """注册所有工具"""

        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """列出所有可用工具"""
            return [
                Tool(
                    name="glm_generate",
                    description="使用GLM生成内容（文章、代码、文本等）",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "生成内容的提示词"
                            },
                            "model": {
                                "type": "string",
                                "enum": ["glm-4.6", "glm-4.5", "glm-3-turbo"],
                                "description": "使用的模型",
                                "default": "glm-4.5"
                            },
                            "max_tokens": {
                                "type": "integer",
                                "description": "最大token数",
                                "default": 2000
                            }
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="glm_analyze",
                    description="分析文本（风格、情感、关键词等）",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "要分析的文本"
                            },
                            "analysis_type": {
                                "type": "string",
                                "enum": ["style", "sentiment", "keywords", "summary"],
                                "description": "分析类型",
                                "default": "summary"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                Tool(
                    name="glm_optimize",
                    description="优化文本或prompt",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "要优化的内容"
                            },
                            "goal": {
                                "type": "string",
                                "enum": ["clarity", "conciseness", "engagement", "seo"],
                                "description": "优化目标",
                                "default": "clarity"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                Tool(
                    name="glm_translate",
                    description="翻译文本",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "要翻译的文本"
                            },
                            "target_language": {
                                "type": "string",
                                "description": "目标语言",
                                "default": "English"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                Tool(
                    name="glm_code",
                    description="生成或解释代码",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "request": {
                                "type": "string",
                                "description": "代码生成或解释请求"
                            },
                            "language": {
                                "type": "string",
                                "description": "编程语言",
                                "default": "Python"
                            }
                        },
                        "required": ["request"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """处理工具调用"""
            try:
                if name == "glm_generate":
                    return await self._handle_generate(arguments)
                elif name == "glm_analyze":
                    return await self._handle_analyze(arguments)
                elif name == "glm_optimize":
                    return await self._handle_optimize(arguments)
                elif name == "glm_translate":
                    return await self._handle_translate(arguments)
                elif name == "glm_code":
                    return await self._handle_code(arguments)
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
            except Exception as e:
                logger.error(f"Error in {name}: {e}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

    async def _handle_generate(self, args: Dict[str, Any]) -> List[TextContent]:
        """处理生成请求"""
        prompt = args["prompt"]
        model = args.get("model", "glm-4.5")
        max_tokens = args.get("max_tokens", 2000)

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的写作助手"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )

        content = response.choices[0].message.content

        return [TextContent(
            type="text",
            text=f"✅ 生成成功（模型：{model}）\n\n{content}"
        )]

    async def _handle_analyze(self, args: Dict[str, Any]) -> List[TextContent]:
        """处理分析请求"""
        text = args["text"]
        analysis_type = args.get("analysis_type", "summary")

        prompts = {
            "style": "请分析以下文本的写作风格和特点",
            "sentiment": "请分析以下文本的情感倾向",
            "keywords": "请提取以下文本的主要关键词",
            "summary": "请总结以下文本的主要内容"
        }

        prompt = f"{prompts.get(analysis_type, prompts['summary'])}:\n\n{text}"

        response = self.client.chat.completions.create(
            model="glm-4.5",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return [TextContent(
            type="text",
            text=f"📊 {analysis_type}分析结果：\n\n{response.choices[0].message.content}"
        )]

    async def _handle_optimize(self, args: Dict[str, Any]) -> List[TextContent]:
        """处理优化请求"""
        content = args["content"]
        goal = args.get("goal", "clarity")

        goal_descriptions = {
            "clarity": "让内容更清晰易懂",
            "conciseness": "让内容更简洁精炼",
            "engagement": "让内容更吸引人",
            "seo": "让内容更适合SEO"
        }

        prompt = f"请优化以下内容，目标：{goal_descriptions.get(goal, goal)}\n\n原内容：\n{content}"

        response = self.client.chat.completions.create(
            model="glm-4.5",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return [TextContent(
            type="text",
            text=f"✨ 优化结果（目标：{goal}）：\n\n{response.choices[0].message.content}"
        )]

    async def _handle_translate(self, args: Dict[str, Any]) -> List[TextContent]:
        """处理翻译请求"""
        text = args["text"]
        target_language = args.get("target_language", "English")

        prompt = f"请将以下文本翻译成{target_language}：\n\n{text}"

        response = self.client.chat.completions.create(
            model="glm-4.5",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return [TextContent(
            type="text",
            text=f"🌍 翻译结果（{target_language}）：\n\n{response.choices[0].message.content}"
        )]

    async def _handle_code(self, args: Dict[str, Any]) -> List[TextContent]:
        """处理代码请求"""
        request = args["request"]
        language = args.get("language", "Python")

        prompt = f"请用{language}处理以下请求：\n\n{request}\n\n请提供代码和必要的解释。"

        response = self.client.chat.completions.create(
            model="glm-4.6",  # 代码生成使用最强模型
            messages=[
                {"role": "system", "content": "你是一个专业的编程助手"},
                {"role": "user", "content": prompt}
            ]
        )

        return [TextContent(
            type="text",
            text=f"💻 代码生成（{language}）：\n\n{response.choices[0].message.content}"
        )]

    async def run(self):
        """运行服务器"""
        if not self.client:
            raise ValueError("GLM client not initialized")

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="glm-writing-system",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities={}
                    )
                )
            )

async def main():
    """主函数"""
    try:
        # 检查环境变量
        if not os.getenv("GLM_API_KEY"):
            print("❌ 错误：未设置 GLM_API_KEY 环境变量")
            print("\n请设置您的GLM API Key:")
            print("export GLM_API_KEY='your-api-key'")
            print("\n获取API Key: https://open.bigmodel.cn/")
            return

        # 创建并运行服务器
        server = GLMMCPServer()
        logger.info("GLM MCP Server启动成功")
        await server.run()

    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("\n请安装必要的依赖:")
        print("pip install mcp zhipuai")
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"❌ 服务器错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())