"""
多轮对话和上下文管理
支持复杂的对话流程
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json

@dataclass
class ConversationState:
    """对话状态"""
    user_id: str
    current_skill: Optional[str] = None
    step: int = 0
    parameters: Dict = field(default_factory=dict)
    history: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)

class ConversationManager:
    """对话管理器"""

    def __init__(self):
        self.states: Dict[str, ConversationState] = {}
        self.skill_flows = self._init_skill_flows()

    def _init_skill_flows(self) -> Dict:
        """初始化技能流程"""
        return {
            'create_article': [
                {
                    'step': 0,
                    'prompt': '请告诉我您想写什么主题的文章？',
                    'param': 'topic',
                    'validation': lambda x: len(x) > 2
                },
                {
                    'step': 1,
                    'prompt': '您希望文章是什么类型？\n1. 教程指南\n2. 深度分析\n3. 实战案例\n4. 观点评论',
                    'param': 'article_type',
                    'options': ['教程', '分析', '案例', '观点'],
                    'validation': lambda x: x in ['教程', '分析', '案例', '观点']
                },
                {
                    'step': 2,
                    'prompt': '目标字数大概多少？\n1. 短文 (1000字以内)\n2. 中篇 (1000-3000字)\n3. 长文 (3000字以上)',
                    'param': 'word_count',
                    'options': [1000, 2000, 3000],
                    'validation': lambda x: isinstance(x, int) and x > 0
                },
                {
                    'step': 3,
                    'prompt': '需要我帮您生成标题吗？(是/否)',
                    'param': 'need_title',
                    'validation': lambda x: x in ['是', '否']
                }
            ],
            'analyze_and_optimize': [
                {
                    'step': 0,
                    'prompt': '请提供您想分析的选题或文章主题',
                    'param': 'topic',
                    'validation': lambda x: len(x) > 2
                },
                {
                    'step': 1,
                    'prompt': '您已经有初稿了吗？(有/无)',
                    'param': 'has_draft',
                    'validation': lambda x: x in ['有', '无']
                },
                {
                    'step': 2,
                    'condition': lambda params: params.get('has_draft') == '有',
                    'prompt': '请粘贴您的内容（限制2000字）',
                    'param': 'content',
                    'validation': lambda x: len(x) > 100
                },
                {
                    'step': 3,
                    'prompt': '您最想优化哪个方面？\n1. 标题吸引力\n2. 内容可读性\n3. SEO表现\n4. 全面优化',
                    'param': 'optimize_target',
                    'options': ['标题', '可读性', 'SEO', '全面'],
                    'validation': lambda x: x in ['标题', '可读性', 'SEO', '全面']
                }
            ]
        }

    async def process_message(self, user_id: str, message: str) -> Dict:
        """处理消息并管理对话流程"""
        state = self.get_or_create_state(user_id)

        # 更新活动时间
        state.last_activity = datetime.now()
        state.history.append({
            'message': message,
            'timestamp': datetime.now(),
            'role': 'user'
        })

        # 检查是否在流程中
        if state.current_skill and state.step < len(self.skill_flows.get(state.current_skill, [])):
            return await self._continue_flow(state, message)
        else:
            # 新的对话，识别意图
            return await self._start_new_flow(state, message)

    async def _continue_flow(self, state: ConversationState, message: str) -> Dict:
        """继续当前的对话流程"""
        flow = self.skill_flows[state.current_skill]
        current_step_config = flow[state.step]

        # 验证输入
        if not self._validate_input(message, current_step_config):
            return {
                'type': 'validation_error',
                'message': f"输入格式不正确，请{current_step_config['prompt']}",
                'retry': True
            }

        # 提取并保存参数
        value = self._extract_value(message, current_step_config)
        state.parameters[current_step_config['param']] = value

        # 记录历史
        state.history.append({
            'step': state.step,
            'param': current_step_config['param'],
            'value': value,
            'timestamp': datetime.now()
        })

        # 检查是否需要条件判断
        if 'condition' in current_step_config:
            if not current_step_config['condition'](state.parameters):
                # 跳过这个步骤
                state.step += 1
                if state.step >= len(flow):
                    return await self._execute_flow(state)

        # 进入下一步
        state.step += 1

        if state.step >= len(flow):
            # 流程结束，执行技能
            return await self._execute_flow(state)
        else:
            # 继续下一步
            next_step = flow[state.step]
            return {
                'type': 'flow_continue',
                'message': next_step['prompt'],
                'step': state.step,
                'total_steps': len(flow),
                'options': next_step.get('options')
            }

    async def _start_new_flow(self, state: ConversationState, message: str) -> Dict:
        """开始新的对话流程"""
        # 识别用户意图
        intent = await self._identify_intent(message)

        if not intent:
            return {
                'type': 'clarification',
                'message': '请选择您要进行的操作：\n\n'
                         '1. 📝 创建文章\n'
                         '2. 🔍 分析优化\n'
                         '3. 💬 自由对话',
                'options': ['创建文章', '分析优化', '自由对话']
            }

        # 根据意图选择流程
        if intent == 'create_article':
            state.current_skill = 'create_article'
            state.step = 0
            state.parameters = {}
            return await self._continue_flow(state, "开始创建文章")
        elif intent == 'analyze_optimize':
            state.current_skill = 'analyze_and_optimize'
            state.step = 0
            state.parameters = {}
            return await self._continue_flow(state, "开始分析优化")
        else:
            # 自由对话，直接触发技能
            return {
                'type': 'direct_trigger',
                'message': message,
                'skill': intent
            }

    async def _execute_flow(self, state: ConversationState) -> Dict:
        """执行完成的流程"""
        # 执行相应的技能
        if state.current_skill == 'create_article':
            result = await self._create_article(state.parameters)
        elif state.current_skill == 'analyze_and_optimize':
            result = await self._analyze_and_optimize(state.parameters)
        else:
            result = {'message': '未知流程'}

        # 清理状态
        self.clear_state(state.user_id)

        return {
            'type': 'flow_complete',
            'result': result,
            'message': '✅ 操作完成！'
        }

    async def _identify_intent(self, message: str) -> Optional[str]:
        """识别用户意图"""
        message = message.lower()

        if any(kw in message for kw in ['写', '创作', '生成', '写一篇']):
            return 'create_article'
        elif any(kw in message for kw in ['分析', '优化', '改进', '提升']):
            return 'analyze_and_optimize'
        elif '帮助' in message:
            return 'help'
        elif '退出' in message:
            return 'exit'

        return None

    def _validate_input(self, message: str, step_config: Dict) -> bool:
        """验证用户输入"""
        validation = step_config.get('validation')
        if not validation:
            return True

        # 简单的数字识别
        if step_config.get('options') and isinstance(step_config['options'][0], int):
            try:
                value = int(message)
                return validation(value)
            except:
                return False

        # 选项验证
        if 'options' in step_config:
            return message in step_config['options']

        # 自定义验证
        return validation(message)

    def _extract_value(self, message: str, step_config: Dict) -> Any:
        """提取参数值"""
        # 选项映射
        if 'options' in step_config:
            options = step_config['options']
            if message in options:
                if isinstance(options[0], int):
                    # 数字选项，返回索引对应的值
                    index = options.index(message)
                    if 'values' in step_config:
                        return step_config['values'][index]
                return message

        # 默认返回原始消息
        return message

    async def _create_article(self, parameters: Dict) -> Dict:
        """创建文章"""
        # 调用内容生成技能
        topic = parameters['topic']
        article_type = parameters.get('article_type', '教程')
        word_count = parameters.get('word_count', 2000)
        need_title = parameters.get('need_title', '是')

        # 这里应该调用实际的技能模块
        return {
            'topic': topic,
            'type': article_type,
            'word_count': word_count,
            'content': f'这是一篇关于{topic}的{article_type}文章...',
            'title': f'{topic}：{article_type}指南' if need_title == '是' else None
        }

    async def _analyze_and_optimize(self, parameters: Dict) -> Dict:
        """分析和优化"""
        topic = parameters.get('topic')
        content = parameters.get('content')
        target = parameters.get('optimize_target', '全面')

        # 这里应该调用实际的技能模块
        return {
            'topic': topic,
            'has_content': content is not None,
            'optimization_target': target,
            'suggestions': [
                '建议增加具体案例',
                '优化段落结构',
                '添加数据支撑'
            ]
        }

    def get_or_create_state(self, user_id: str) -> ConversationState:
        """获取或创建对话状态"""
        if user_id not in self.states:
            self.states[user_id] = ConversationState(user_id=user_id)
        return self.states[user_id]

    def clear_state(self, user_id: str):
        """清理对话状态"""
        if user_id in self.states:
            del self.states[user_id]

    def cleanup_inactive_states(self, max_inactive_hours: int = 24):
        """清理不活跃的对话状态"""
        cutoff_time = datetime.now() - timedelta(hours=max_inactive_hours)

        inactive_users = [
            user_id for user_id, state in self.states.items()
            if state.last_activity < cutoff_time
        ]

        for user_id in inactive_users:
            del self.states[user_id]

    def get_state_summary(self) -> Dict:
        """获取状态摘要"""
        active_conversations = len(self.states)
        total_steps = sum(state.step for state in self.states.values())

        return {
            'active_conversations': active_conversations,
            'total_steps': total_steps,
            'average_steps': total_steps / max(active_conversations, 1)
        }