"""
选题分析器模块
分析选题的热度、竞争度、受众匹配度等指标
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import jieba
import jieba.analyse

class TopicAnalyzer:
    """选题分析器"""

    def __init__(self, config: Dict):
        """
        初始化选题分析器

        Args:
            config: 配置信息，包含API密钥等
        """
        self.config = config
        self.wechat_index_api = config.get('wechat_index_api')
        self.hot_search_api = config.get('hot_search_api')
        self.competitor_db = CompetitorDatabase(config.get('db_config'))

        # 初始化jieba分词
        jieba.initialize()

    def analyze_topic(self, topic: str, account_info: Dict) -> Dict:
        """
        全面分析一个选题

        Args:
            topic: 选题关键词
            account_info: 公众号信息

        Returns:
            分析结果
        """
        # 1. 热度分析
        heat_analysis = self._analyze_heat(topic)

        # 2. 竞争度分析
        competition_analysis = self._analyze_competition(topic)

        # 3. 受众匹配度分析
        audience_match = self._analyze_audience_match(topic, account_info)

        # 4. 历史表现分析
        history_analysis = self._analyze_history_performance(topic)

        # 5. 综合评分
        final_score = self._calculate_final_score(
            heat_analysis,
            competition_analysis,
            audience_match,
            history_analysis
        )

        # 6. 生成建议
        suggestions = self._generate_suggestions(
            topic,
            heat_analysis,
            competition_analysis,
            audience_match,
            final_score
        )

        return {
            'topic': topic,
            'heat_analysis': heat_analysis,
            'competition_analysis': competition_analysis,
            'audience_match': audience_match,
            'history_analysis': history_analysis,
            'final_score': final_score,
            'suggestions': suggestions,
            'keywords': self._extract_keywords(topic),
            'related_topics': self._find_related_topics(topic),
            'best_publish_time': self._recommend_publish_time(account_info),
            'analysis_time': datetime.now().isoformat()
        }

    def _analyze_heat(self, topic: str) -> Dict:
        """分析话题热度"""
        try:
            # 获取微信指数
            wechat_index = self._get_wechat_index(topic)

            # 获取百度指数
            baidu_index = self._get_baidu_index(topic)

            # 获取微博热度
            weibo_heat = self._get_weibo_heat(topic)

            # 计算热度趋势（近7天）
            heat_trend = self._calculate_heat_trend(topic, days=7)

            # 判断是否为热点
            is_hotspot = self._is_hotspot(wechat_index, heat_trend)

            return {
                'wechat_index': wechat_index,
                'baidu_index': baidu_index,
                'weibo_heat': weibo_heat,
                'heat_trend': heat_trend,
                'is_hotspot': is_hotspot,
                'heat_level': self._get_heat_level(wechat_index)
            }
        except Exception as e:
            return {
                'error': str(e),
                'wechat_index': 0,
                'baidu_index': 0,
                'weibo_heat': 0,
                'heat_trend': 'stable',
                'is_hotspot': False,
                'heat_level': 'low'
            }

    def _analyze_competition(self, topic: str) -> Dict:
        """分析竞争度"""
        try:
            # 搜索相关文章数量
            article_count = self._search_article_count(topic)

            # 获取头部账号表现
            top_accounts = self._get_top_performers(topic)

            # 分析竞争激烈程度
            competition_level = self._evaluate_competition_level(
                article_count,
                top_accounts
            )

            # 查找差异化机会
            opportunities = self._find_opportunities(topic, top_accounts)

            return {
                'article_count': article_count,
                'top_accounts': top_accounts[:5],  # 返回前5个
                'competition_level': competition_level,
                'opportunities': opportunities,
                'difficulty_score': self._calculate_difficulty(
                    article_count, competition_level
                )
            }
        except Exception as e:
            return {
                'error': str(e),
                'article_count': 0,
                'top_accounts': [],
                'competition_level': 'unknown',
                'opportunities': [],
                'difficulty_score': 0
            }

    def _analyze_audience_match(self, topic: str, account_info: Dict) -> Dict:
        """分析受众匹配度"""
        # 提取话题关键词
        topic_keywords = self._extract_keywords(topic)

        # 获取账号粉丝画像
        audience_profile = account_info.get('audience_profile', {})

        # 计算匹配度
        match_score = self._calculate_audience_match(
            topic_keywords,
            audience_profile
        )

        # 分析潜在受众规模
        potential_audience = self._estimate_potential_audience(
            topic,
            audience_profile
        )

        return {
            'match_score': match_score,
            'potential_audience': potential_audience,
            'audience_interests': self._analyze_audience_interests(
                topic, audience_profile
            ),
            'recommendation': self._get_audience_recommendation(match_score)
        }

    def _generate_suggestions(self, topic: str, *analyses) -> List[str]:
        """生成选题建议"""
        suggestions = []

        # 基于热度给出建议
        heat = analyses[0]
        if heat.get('is_hotspot'):
            suggestions.append(
                f"🔥 {topic}是当前热点，建议快速发布抢占流量"
            )
        elif heat.get('heat_level') == 'high':
            suggestions.append(
                f"📈 {topic}热度较高，适合深度内容创作"
            )
        else:
            suggestions.append(
                f"💡 {topic}热度一般，需要通过独特角度提升吸引力"
            )

        # 基于竞争度给出建议
        competition = analyses[1]
        if competition.get('competition_level') == 'high':
            suggestions.append(
                "⚠️ 该话题竞争激烈，建议寻找差异化切入点"
            )
        elif competition.get('opportunities'):
            suggestions.append(
                f"💎 发现机会：{', '.join(competition['opportunities'][:2])}"
            )

        # 基于受众匹配度给出建议
        audience = analyses[2]
        if audience.get('match_score', 0) > 80:
            suggestions.append(
                "✅ 话题与受众高度匹配，预计将有良好互动"
            )
        elif audience.get('match_score', 0) < 50:
            suggestions.append(
                "⚠️ 话题与受众匹配度较低，建议调整或寻找相关话题"
            )

        # 基于最终评分给出建议
        final_score = analyses[4] if len(analyses) > 4 else 0
        if final_score >= 85:
            suggestions.append(
                "🌟 综合评分优秀，强烈推荐创作"
            )
        elif final_score >= 70:
            suggestions.append(
                "👍 综合评分良好，可以创作"
            )
        else:
            suggestions.append(
                "💪 综合评分一般，建议优化角度或选择其他话题"
            )

        return suggestions

    def _extract_keywords(self, text: str, topK: int = 10) -> List[str]:
        """提取关键词"""
        keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)
        return [kw[0] for kw in keywords]

    def _find_related_topics(self, topic: str) -> List[str]:
        """查找相关话题"""
        # 这里可以调用API或使用词向量模型找到相似话题
        # 简单实现：基于关键词扩展
        keywords = self._extract_keywords(topic, 5)
        related = []

        for keyword in keywords:
            # 添加相关组合
            related.append(f"{keyword}技巧")
            related.append(f"{keyword}方法")
            related.append(f"如何{keyword}")

        # 去重并返回
        return list(set(related))[:10]

    def _recommend_publish_time(self, account_info: Dict) -> Dict:
        """推荐发布时间"""
        # 获取账号历史最佳发布时间
        best_times = account_info.get('best_publish_times', ['12:00', '18:00'])

        # 获取粉丝活跃时间
        active_hours = account_info.get('audience_active_hours',
                                      ['08:00-10:00', '12:00-14:00', '18:00-21:00'])

        return {
            'recommended_times': best_times,
            'active_periods': active_hours,
            'reason': '基于历史数据和粉丝活跃分析'
        }

    def _get_wechat_index(self, keyword: str) -> int:
        """获取微信指数（模拟）"""
        # 实际应该调用微信指数API
        # 这里返回模拟数据
        import random
        return random.randint(1000, 100000)

    def _get_baidu_index(self, keyword: str) -> int:
        """获取百度指数（模拟）"""
        import random
        return random.randint(500, 50000)

    def _get_weibo_heat(self, keyword: str) -> int:
        """获取微博热度（模拟）"""
        import random
        return random.randint(0, 10000)

    def _calculate_heat_trend(self, topic: str, days: int) -> str:
        """计算热度趋势"""
        # 模拟趋势分析
        import random
        trend = random.choice(['rising', 'stable', 'declining'])
        return trend

    def _is_hotspot(self, index: int, trend: str) -> bool:
        """判断是否为热点"""
        return index > 10000 or trend == 'rising'

    def _get_heat_level(self, index: int) -> str:
        """获取热度等级"""
        if index > 50000:
            return 'very_high'
        elif index > 20000:
            return 'high'
        elif index > 5000:
            return 'medium'
        else:
            return 'low'

    def _search_article_count(self, topic: str) -> int:
        """搜索相关文章数量（模拟）"""
        import random
        return random.randint(100, 10000)

    def _get_top_performers(self, topic: str) -> List[Dict]:
        """获取头部账号（模拟）"""
        return [
            {'name': '示例账号A', 'read_count': 100000, 'likes': 5000},
            {'name': '示例账号B', 'read_count': 80000, 'likes': 4000},
        ]

    def _evaluate_competition_level(self, count: int, top_accounts: List) -> str:
        """评估竞争激烈程度"""
        if count > 5000:
            return 'high'
        elif count > 1000:
            return 'medium'
        else:
            return 'low'

    def _find_opportunities(self, topic: str, competitors: List) -> List[str]:
        """寻找差异化机会"""
        opportunities = [
            f"从{topic}的细分领域入手",
            f"结合个人经历分享{topic}",
            f"提供{topic}的实用工具或资源",
        ]
        return opportunities

    def _calculate_difficulty(self, count: int, level: str) -> int:
        """计算难度评分"""
        if level == 'high':
            return min(90, 50 + count // 100)
        elif level == 'medium':
            return min(70, 30 + count // 200)
        else:
            return min(50, 10 + count // 500)

    def _calculate_audience_match(self, keywords: List, profile: Dict) -> int:
        """计算受众匹配度"""
        # 简化实现
        interests = profile.get('interests', [])
        match_count = len(set(keywords) & set(interests))
        return min(100, match_count * 20)

    def _estimate_potential_audience(self, topic: str, profile: Dict) -> int:
        """估算潜在受众规模"""
        # 简化实现
        base_audience = profile.get('followers', 10000)
        interest_factor = 0.3  # 30%的粉丝可能感兴趣
        return int(base_audience * interest_factor)

    def _analyze_audience_interests(self, topic: str, profile: Dict) -> List[str]:
        """分析受众兴趣点"""
        # 基于话题和受众画像分析
        return [
            "实用技巧",
            "案例分析",
            "经验分享",
            "工具推荐"
        ]

    def _get_audience_recommendation(self, score: int) -> str:
        """获取受众建议"""
        if score > 80:
            return "高度匹配，强烈推荐"
        elif score > 60:
            return "比较匹配，可以尝试"
        else:
            return "匹配度较低，建议调整方向"

    def _analyze_history_performance(self, topic: str) -> Dict:
        """分析历史表现"""
        # 从数据库查询历史相关话题的表现
        return {
            'avg_read_count': 5000,
            'avg_like_rate': 0.05,
            'avg_share_rate': 0.02,
            'best_performing': {
                'title': '相关标题示例',
                'read_count': 10000
            }
        }

    def _calculate_final_score(self, *analyses) -> int:
        """计算最终评分"""
        # 热度权重30%
        heat_score = min(100, analyses[0].get('wechat_index', 0) / 1000)

        # 竞争度权重20%（竞争越低分数越高）
        competition_level = analyses[1].get('competition_level', 'medium')
        competition_score = {
            'low': 90,
            'medium': 60,
            'high': 30
        }.get(competition_level, 50)

        # 受众匹配度权重30%
        audience_score = analyses[2].get('match_score', 50)

        # 历史表现权重20%
        history_score = min(100, analyses[3].get('avg_read_count', 0) / 100)

        final_score = (
            heat_score * 0.3 +
            competition_score * 0.2 +
            audience_score * 0.3 +
            history_score * 0.2
        )

        return int(final_score)


class CompetitorDatabase:
    """竞品数据库操作类"""

    def __init__(self, config: Dict):
        self.config = config
        # 初始化数据库连接
        pass

    def get_competitors(self, topic: str) -> List[Dict]:
        """获取竞品信息"""
        # 实现数据库查询逻辑
        pass

    def update_competitor_data(self, competitor: Dict):
        """更新竞品数据"""
        # 实现数据更新逻辑
        pass


if __name__ == "__main__":
    # 测试代码
    config = {
        'wechat_index_api': 'your_api_key',
        'hot_search_api': 'your_api_key',
        'db_config': {
            'host': 'localhost',
            'database': 'wechat_writer'
        }
    }

    analyzer = TopicAnalyzer(config)

    # 分析示例
    result = analyzer.analyze_topic(
        topic="AI写作工具",
        account_info={
            'name': "科技前沿",
            'audience_profile': {
                'interests': ['AI', '写作', '效率工具'],
                'followers': 50000
            },
            'best_publish_times': ['12:00', '18:00'],
            'audience_active_hours': ['08:00-10:00', '12:00-14:00', '18:00-21:00']
        }
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))