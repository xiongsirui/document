"""
微信聊天机器人
集成Skills触发功能
"""

from flask import Flask, request, jsonify
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime
import asyncio
from chat_trigger import ChatSkillTrigger, ChatMessage

app = Flask(__name__)

class WeChatBot:
    """微信机器人"""

    def __init__(self, config):
        self.config = config
        self.trigger = ChatSkillTrigger()
        self.user_contexts = {}  # 存储用户对话上下文

    def verify_signature(self, signature, timestamp, nonce):
        """验证微信签名"""
        token = self.config['token']
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        tmp_str = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
        return tmp_str == signature

    async def handle_message(self, user_id, message):
        """处理用户消息"""
        # 创建聊天消息对象
        chat_msg = ChatMessage(
            user_id=user_id,
            message=message,
            channel='wechat',
            timestamp=datetime.now(),
            context=self.user_contexts.get(user_id, {})
        )

        # 处理消息
        response = await self.trigger.process_message(chat_msg)

        # 保存上下文
        self.user_contexts[user_id] = {
            'last_message': message,
            'last_response': response,
            'timestamp': datetime.now()
        }

        return response

    def format_response(self, response, to_user):
        """格式化微信响应"""
        msg_type = response.get('type', 'text')

        if msg_type == 'skill_result':
            # 技能执行结果
            result = response.get('result', {})

            if 'analysis' in result:
                # 选题分析结果
                content = self._format_topic_analysis(result)
            elif 'content' in result:
                # 内容生成结果
                content = self._format_content_result(result)
            elif 'titles' in result:
                # 标题生成结果
                content = self._format_titles_result(result)
            else:
                content = "操作完成：" + str(result)

        elif msg_type == 'parameter_request':
            # 询问参数
            content = response.get('message', '请提供更多信息')

        elif msg_type == 'clarification':
            # 澄清意图
            content = response.get('message', '没太明白您的意思')
            suggestions = response.get('suggestions', [])
            if suggestions:
                content += "\n\n您可以试试：\n" + "\n".join(f"• {s}" for s in suggestions)

        elif msg_type == 'error':
            content = f"出错了：{response.get('message', '未知错误')}"

        else:
            content = str(response)

        # 生成XML响应
        return self._create_text_response(to_user, content)

    def _format_topic_analysis(self, analysis):
        """格式化选题分析结果"""
        content = f"📊 选题：{analysis.get('topic', 'Unknown')}\n\n"
        content += f"🔥 热度评分：{analysis.get('heat_analysis', {}).get('heat_level', 'N/A')}\n"
        content += f"⚔️ 竞争程度：{analysis.get('competition_analysis', {}).get('competition_level', 'N/A')}\n"
        content += f"👥 受众匹配：{analysis.get('audience_match', {}).get('match_score', 0)}%\n"
        content += f"⭐ 综合评分：{analysis.get('final_score', 0)}/100\n\n"

        # 添加建议
        suggestions = analysis.get('suggestions', [])
        if suggestions:
            content += "💡 建议：\n" + "\n".join(f"• {s}" for s in suggestions)

        return content

    def _format_titles_result(self, result):
        """格式化标题结果"""
        titles = result.get('titles', [])
        content = "📝 为您生成了以下标题：\n\n"

        for i, title in enumerate(titles, 1):
            content += f"{i}. {title}\n"

        return content

    def _format_content_result(self, result):
        """格式化内容结果"""
        content = result.get('content', '')
        # 限制长度，避免微信消息过长
        if len(content) > 1000:
            content = content[:1000] + "\n\n[内容已截断，完整内容请在后台查看]"

        return content

    def _create_text_response(self, to_user, content):
        """创建文本响应"""
        timestamp = int(datetime.now().timestamp())

        response = f"""
        <xml>
            <ToUserName><![CDATA[{to_user}]]></ToUserName>
            <FromUserName><![CDATA[{self.config['app_id']}]]></FromUserName>
            <CreateTime>{timestamp}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{content}]]></Content>
        </xml>
        """
        return response

# 初始化机器人
bot = WeChatBot({
    'token': 'your_wechat_token',
    'app_id': 'your_app_id'
})

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    """微信消息处理"""
    if request.method == 'GET':
        # 验证服务器
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        if bot.verify_signature(signature, timestamp, nonce):
            return echostr
        else:
            return 'Verification failed', 403

    else:
        # 处理消息
        xml_data = request.data
        xml_tree = ET.fromstring(xml_data)

        # 解析消息
        msg_type = xml_tree.find('MsgType').text
        from_user = xml_tree.find('FromUserName').text

        if msg_type == 'text':
            # 文本消息
            content = xml_tree.find('Content').text

            # 异步处理
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                bot.handle_message(from_user, content)
            )
            loop.close()

            return response

        elif msg_type == 'event':
            # 事件处理
            event = xml_tree.find('Event').text

            if event == 'subscribe':
                # 用户关注
                welcome_msg = """
👋 欢迎来到AI写作助手！

我是您的智能内容创作伙伴，可以帮您：

📊 选题分析：评估话题热度和可行性
✍️ 内容创作：生成高质量文章内容
🏷️ 标题优化：创作吸引眼球的标题
🔍 SEO优化：提升文章搜索排名
✨ 内容润色：优化文章可读性

试试说：
• "分析AI写作工具这个选题"
• "写一篇关于量化的文章"
• "帮我想个标题"

更多功能请输入"帮助"
                """
                return bot._create_text_response(from_user, welcome_msg)

        return 'success'


# 测试接口
@app.route('/test/chat', methods=['POST'])
def test_chat():
    """测试聊天接口"""
    data = request.json
    user_id = data.get('user_id', 'test')
    message = data.get('message', '')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(
        bot.handle_message(user_id, message)
    )
    loop.close()

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)