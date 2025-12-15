"""
聊天触发Skills系统
支持自然语言和命令式触发
"""

import re
import json
import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import jieba
from dataclasses import dataclass

@dataclass
class ChatMessage:
    """聊天消息数据类"""
    user_id: str
    message: str
    channel: str  # wechat, slack, web
    timestamp: datetime
    context: Optional[Dict] = None

@dataclass
class SkillIntent:
    """技能意图识别结果"""
    skill_name: str
    action: str
    parameters: Dict
    confidence: float

class ChatSkillTrigger:
    """聊天技能触发器"""

    def __init__(self):
        # 初始化技能映射
        self.skill_patterns = {
            # 选题分析
            'analyze_topic': {
                'patterns': [
                    r'分析.*?选题',
                    r'评估.*?话题',
                    r'.*?怎么样',
                    r'.*?值得写吗',
                    r'选题分析'
                ],
                'skill': 'wechat-topic-analyzer',
                'required_params': ['topic']
            },

            # 标题生成
            'generate_title': {
                'patterns': [
                    r'生成.*?标题',
                    r'帮我想.*?标题',
                    r'起个.*?标题',
                    r'标题.*?建议'
                ],
                'skill': 'wechat-title-generator',
                'required_params': ['content']
            },

            # 内容生成
            'generate_content': {
                'patterns': [
                    r'写.*?文章',
                    r'生成.*?内容',
                    r'帮我写.*?',
                    r'创作.*?'
                ],
                'skill': 'wechat-content-generator',
                'required_params': ['topic']
            },

            # SEO优化
            'optimize_seo': {
                'patterns': [
                    r'优化.*?SEO',
                    r'SEO.*?优化',
                    r'关键词.*?优化',
                    r'提高.*?搜索排名'
                ],
                'skill': 'wechat-seo-optimizer',
                'required_params': ['content', 'keywords']
            },

            # 内容润色
            'polish_content': {
                'patterns': [
                    r'润色.*?内容',
                    r'优化.*?文章',
                    r'改进.*?文案',
                    r'让.*?更好'
                ],
                'skill': 'wechat-content-polisher',
                'required_params': ['content']
            },

            # 批量操作
            'batch_operation': {
                'patterns': [
                    r'批量.*?',
                    r'一次性.*?',
                    r'多个.*?',
                    r'全部.*?'
                ],
                'skill': 'batch_processor',
                'required_params': ['operation', 'targets']
            }
        }

        # 初始化自然语言处理器
        self.nlp_processor = NLPProcessor()

        # 加载技能模块
        self.skill_modules = self._load_skill_modules()

    async def process_message(self, message: ChatMessage) -> Dict:
        """处理聊天消息并触发相应技能"""

        # 1. 解析用户意图
        intent = await self._parse_intent(message.message)

        if not intent or intent.confidence < 0.6:
            return {
                'type': 'clarification',
                'message': '抱歉，我没太明白您的意思。您可以试试：\n'
                         '• "分析AI写作工具这个选题"\n'
                         '• "帮我想个关于量化的标题"\n'
                         '• "写一篇关于高性能计算的文章"',
                'suggestions': ['选题分析', '标题生成', '内容创作']
            }

        # 2. 验证参数
        missing_params = self._check_required_params(intent)
        if missing_params:
            return await self._ask_for_missing_params(intent, missing_params)

        # 3. 执行技能
        try:
            result = await self._execute_skill(intent)
            return {
                'type': 'skill_result',
                'skill': intent.skill_name,
                'result': result,
                'suggestions': self._get_next_suggestions(intent, result)
            }
        except Exception as e:
            return {
                'type': 'error',
                'message': f'执行技能时出错：{str(e)}',
                'skill': intent.skill_name
            }

    async def _parse_intent(self, message: str) -> Optional[SkillIntent]:
        """解析用户意图"""

        # 预处理消息
        cleaned_message = self._preprocess_message(message)

        # 匹配模式
        matched_skills = []

        for skill_name, config in self.skill_patterns.items():
            for pattern in config['patterns']:
                match = re.search(pattern, cleaned_message, re.IGNORECASE)
                if match:
                    confidence = self._calculate_confidence(match, cleaned_message)
                    if confidence > 0.5:
                        matched_skills.append({
                            'skill_name': skill_name,
                            'confidence': confidence,
                            'match': match,
                            'config': config
                        })

        if not matched_skills:
            # 尝试NLP意图识别
            nlp_intent = await self.nlp_processor.classify_intent(cleaned_message)
            if nlp_intent:
                return nlp_intent
            return None

        # 选择置信度最高的
        best_match = max(matched_skills, key=lambda x: x['confidence'])

        # 提取参数
        parameters = await self._extract_parameters(
            cleaned_message,
            best_match['config'],
            best_match['match']
        )

        return SkillIntent(
            skill_name=best_match['skill_name'],
            action=best_match['config'].get('action', 'execute'),
            parameters=parameters,
            confidence=best_match['confidence']
        )

    def _preprocess_message(self, message: str) -> str:
        """预处理消息"""
        # 移除多余空格
        message = re.sub(r'\s+', ' ', message.strip())

        # 移除特殊字符
        message = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', message)

        return message

    def _calculate_confidence(self, match, message: str) -> float:
        """计算匹配置信度"""
        # 基础分数
        base_score = len(match.group()) / len(message)

        # 关键词权重
        keywords = ['分析', '生成', '写', '优化', '标题', '内容', '选题']
        keyword_count = sum(1 for kw in keywords if kw in message)
        keyword_score = min(keyword_count * 0.2, 0.4)

        return min(base_score + keyword_score, 1.0)

    async def _extract_parameters(self, message: str, config: Dict, match) -> Dict:
        """提取技能参数"""
        parameters = {}

        # 从匹配中提取
        if match.groups():
            parameters['matched_text'] = match.group(0)

        # 使用NLP提取实体
        entities = await self.nlp_processor.extract_entities(message)

        # 映射到所需参数
        required_params = config.get('required_params', [])
        for param in required_params:
            if param == 'topic':
                parameters['topic'] = entities.get('topic') or self._extract_topic(message)
            elif param == 'content':
                parameters['content'] = entities.get('content') or message
            elif param == 'keywords':
                parameters['keywords'] = entities.get('keywords', [])
            elif param == 'style':
                parameters['style'] = entities.get('style', 'professional')

        return parameters

    def _extract_topic(self, message: str) -> str:
        """从消息中提取主题"""
        # 简单实现：提取引号内内容或关键词
        quoted = re.search(r'["""](.*?)["""]', message)
        if quoted:
            return quoted.group(1)

        # 提取"关于"、"分析"等后的内容
        topic_patterns = [
            r'关于(.*?)(?:的|的文章|怎么样)',
            r'分析(.*?)(?:的|这个|那个)',
            r'写.*?关于(.*?)的'
        ]

        for pattern in topic_patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1).strip()

        return message  # 如果都失败，返回原消息

    async def _execute_skill(self, intent: SkillIntent) -> Dict:
        """执行技能"""
        skill_module = self.skill_modules.get(intent.skill_name)
        if not skill_module:
            raise ValueError(f"Skill {intent.skill_name} not found")

        # 调用技能
        if hasattr(skill_module, intent.action):
            method = getattr(skill_module, intent.action)
            if asyncio.iscoroutinefunction(method):
                return await method(**intent.parameters)
            else:
                return method(**intent.parameters)
        else:
            # 默认execute方法
            if asyncio.iscoroutinefunction(skill_module.execute):
                return await skill_module.execute(**intent.parameters)
            else:
                return skill_module.execute(**intent.parameters)

    def _load_skill_modules(self) -> Dict:
        """加载技能模块"""
        modules = {}

        # 这里应该动态加载所有技能模块
        try:
            from ..core_modules.topic_analyzer import TopicAnalyzer
            modules['wechat-topic-analyzer'] = TopicAnalyzer()
        except ImportError:
            pass

        try:
            from ..core_modules.content_generator import ContentGenerator
            modules['wechat-content-generator'] = ContentGenerator()
        except ImportError:
            pass

        return modules

    def _check_required_params(self, intent: SkillIntent) -> List[str]:
        """检查缺失的必需参数"""
        config = self.skill_patterns.get(intent.skill_name, {})
        required = config.get('required_params', [])

        missing = []
        for param in required:
            if param not in intent.parameters:
                missing.append(param)

        return missing

    async def _ask_for_missing_params(self, intent: SkillIntent, missing: List[str]) -> Dict:
        """询问缺失的参数"""
        questions = {
            'topic': '请告诉我您想分析或创作的主题是什么？',
            'content': '请提供需要优化或润色的内容',
            'keywords': '请提供相关的关键词（用逗号分隔）',
            'style': '您希望是什么风格？（如：专业、轻松、幽默等）'
        }

        if len(missing) == 1:
            question = questions.get(missing[0], f'请提供{missing[0]}')
        else:
            question = f'请提供以下信息：{", ".join(missing)}'

        return {
            'type': 'parameter_request',
            'message': question,
            'missing_params': missing,
            'skill_intent': intent
        }

    def _get_next_suggestions(self, intent: SkillIntent, result: Dict) -> List[str]:
        """获取下一步建议"""
        suggestions = []

        # 基于当前执行的技能提供建议
        if intent.skill_name == 'analyze_topic':
            if result.get('final_score', 0) > 70:
                suggestions = [
                    '生成文章大纲',
                    '创作完整内容',
                    '生成相关标题'
                ]
            else:
                suggestions = [
                    '尝试其他选题',
                    '查看相关话题',
                    '获取灵感建议'
                ]

        elif intent.skill_name == 'generate_content':
            suggestions = [
                '优化文章标题',
                '进行SEO优化',
                '润色文章内容',
                '生成文章摘要'
            ]

        elif intent.skill_name == 'generate_title':
            suggestions = [
                '优化文章内容',
                '生成不同风格标题',
                    '进行A/B测试'
            ]

        return suggestions


class NLPProcessor:
    """自然语言处理器"""

    async def classify_intent(self, message: str) -> Optional[SkillIntent]:
        """使用NLP模型分类意图"""
        # 这里可以集成真正的NLP模型
        # 暂时使用简单规则

        if '写作' in message or '创作' in message:
            return SkillIntent(
                skill_name='generate_content',
                action='execute',
                parameters={'topic': message},
                confidence=0.7
            )

        return None

    async def extract_entities(self, message: str) -> Dict:
        """提取实体"""
        entities = {}

        # 提取主题
        topic_match = re.search(r'["""](.*?)["""]', message)
        if topic_match:
            entities['topic'] = topic_match.group(1)

        # 提取关键词
        keywords = re.findall(r'[\w]{2,}', message)
        entities['keywords'] = keywords[:5]  # 取前5个

        return entities


# 使用示例
async def main():
    trigger = ChatSkillTrigger()

    # 测试消息
    messages = [
        "分析'AI写作工具'这个选题怎么样",
        "帮我想个关于量化交易的文章标题",
        "写一篇高性能计算的入门教程",
        "优化这篇关于机器学习的内容",
        "批量生成5个AI相关的选题"
    ]

    for msg in messages:
        chat_msg = ChatMessage(
            user_id="user123",
            message=msg,
            channel="web",
            timestamp=datetime.now()
        )

        result = await trigger.process_message(chat_msg)
        print(f"消息: {msg}")
        print(f"结果: {result}\n")


if __name__ == "__main__":
    asyncio.run(main())