#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code Skills 演示脚本
展示如何通过编程方式调用 Skills 来解决公众号选题问题
"""

import json
import requests
from typing import Dict, List, Any
from datetime import datetime

class SkillDemo:
    def __init__(self):
        self.base_url = "http://localhost:5000"  # Skills 后端服务地址
        self.session = requests.Session()

    def call_knowledge_base(self, keywords: List[str], material_types: List[str] = None, time_range: str = "最近30天") -> Dict[str, Any]:
        """
        调用知识库 Skill 搜索相关素材

        Args:
            keywords: 搜索关键词列表
            material_types: 素材类型筛选 [经历, 评价, 案例, 洞察, 数据]
            time_range: 时间范围

        Returns:
            搜索到的素材列表
        """
        # 模拟调用知识库 API
        mock_materials = [
            {
                "id": "kb001",
                "type": "经历",
                "content": "团队试用Slack一个月后，发现异步沟通效率提升了40%，但紧急事项响应变慢了",
                "tags": ["Slack", "异步沟通", "团队协作"],
                "date": "2024-11-20",
                "source": "个人实践",
                "credibility": 8
            },
            {
                "id": "kb002",
                "type": "洞察",
                "content": "远程办公的关键不是工具，而是建立清晰的沟通协议和预期管理",
                "tags": ["远程办公", "沟通协议", "管理"],
                "date": "2024-11-15",
                "source": "观察总结",
                "credibility": 9
            },
            {
                "id": "kb003",
                "type": "数据",
                "content": "公司200名员工调研显示：73%的人认为远程办公效率更高，但89%感到孤独",
                "tags": ["调研", "员工满意度", "效率"],
                "date": "2024-10-28",
                "source": "内部调研",
                "credibility": 9
            },
            {
                "id": "kb004",
                "type": "案例",
                "content": "通过优化会议流程，将周会从60分钟缩短到30分钟，决策效率提升",
                "tags": ["会议优化", "效率提升", "流程改进"],
                "date": "2024-11-10",
                "source": "团队实践",
                "credibility": 8
            }
        ]

        # 过滤相关素材
        filtered_materials = []
        for material in mock_materials:
            # 检查关键词匹配
            content_lower = material['content'].lower()
            if any(keyword.lower() in content_lower for keyword in keywords):
                filtered_materials.append(material)

        return {
            "status": "success",
            "count": len(filtered_materials),
            "materials": filtered_materials,
            "time_range": time_range
        }

    def call_writer_skill(self, materials: List[Dict], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用写作 Skill 基于素材生成选题

        Args:
            materials: 素材列表
            requirements: 写作要求

        Returns:
            生成的选题方案
        """
        # 基于素材智能生成选题
        topics = []

        # 分析素材类型
        has_experience = any(m["type"] == "经历" for m in materials)
        has_data = any(m["type"] == "数据" for m in materials)
        has_insight = any(m["type"] == "洞察" for m in materials)
        has_case = any(m["type"] == "案例" for m in materials)

        # 生成选题1：工具对比类
        if has_experience:
            topics.append({
                "title": "《我用过10款协作工具，这3款真正提升了团队效率》",
                "angle": "基于实际使用体验的工具对比",
                "unique_value": "真实测评数据，不谈功能谈体验",
                "supporting_materials": [m["id"] for m in materials if m["type"] == "经历"],
                "workload": "中等(3星)",
                "estimated_words": 2500,
                "type": "工具对比"
            })

        # 生成选题2：方法论类
        if has_insight and has_case:
            topics.append({
                "title": "《异步办公：让远程团队效率提升50%的秘密》",
                "angle": "介绍异步工作方法论",
                "unique_value": "结合具体案例和原则",
                "supporting_materials": [m["id"] for m in materials if m["type"] in ["洞察", "案例"]],
                "workload": "简单(2星)",
                "estimated_words": 2000,
                "type": "方法论"
            })

        # 生成选题3：数据洞察类
        if has_data:
            topics.append({
                "title": "《200人远程办公调查：最影响效率的不是工具》",
                "angle": "基于调研数据的深度分析",
                "unique_value": "第一手数据，反常识洞察",
                "supporting_materials": [m["id"] for m in materials if m["type"] == "数据"],
                "workload": "复杂(4星)",
                "estimated_words": 3000,
                "type": "数据洞察"
            })

        # 生成选题4：问题解决类
        if has_case:
            topics.append({
                "title": "《远程团队周会，如何从1小时压缩到30分钟》",
                "angle": "解决具体问题",
                "unique_value": "可立即执行的优化方案",
                "supporting_materials": [m["id"] for m in materials if m["type"] == "案例"],
                "workload": "非常简单(1星)",
                "estimated_words": 1500,
                "type": "问题解决"
            })

        return {
            "status": "success",
            "topic_count": len(topics),
            "topics": topics,
            "generation_time": datetime.now().isoformat()
        }

    def call_workflow_skill(self, brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用写作工作流 Skill 进行完整选题流程

        Args:
            brief: 项目简报

        Returns:
            完整的工作流程输出
        """
        # Step 1: 理解需求
        step1_output = {
            "brief": brief,
            "understanding": f"理解需求：为{brief['platform']}创作关于{brief['topic']}的内容，目标字数{brief['word_count']}字"
        }

        # Step 2: 信息搜索（模拟）
        step2_output = {
            "search_results": {
                "官方信息": 5,
                "媒体报道": 12,
                "社区讨论": 28,
                "竞品分析": 3
            },
            "key_points": [
                "远程办公已成为新常态",
                "效率提升是核心痛点",
                "工具选择至关重要",
                "管理方式需要转变"
            ]
        }

        # Step 3: 选题讨论
        step3_output = {
            "selected_topic": brief.get('selected_topic', '工具对比类'),
            "alternatives": [
                {
                    "title": "《远程办公工具实测：Slack、Teams、钉钉深度对比》",
                    "angle": "三款主流工具的深度使用体验",
                    "workload": "复杂(4星)",
                    "advantages": ["真实测试数据", "对比维度全面"],
                    "disadvantages": ["测试周期需要2周"],
                    "needs_test": True,
                    "outline": {
                        "opening": "远程办公工具市场现状（200字）",
                        "main": [
                            "界面与易用性对比（500字）",
                            "协作功能深度测试（500字）",
                            "集成能力评估（400字）",
                            "成本分析（400字）"
                        ],
                        "experience": "测试体验：团队成员反馈（300字）",
                        "conclusion": "选择建议（200字）"
                    }
                },
                {
                    "title": "《我们的远程办公实践：效率提升80%的5个方法》",
                    "angle": "总结可复制的实践经验",
                    "workload": "简单(2星)",
                    "advantages": ["基于真实经验", "可直接应用"],
                    "disadvantages": ["需要整理和提炼"],
                    "needs_test": False,
                    "outline": {
                        "opening": "从混乱到有序的转变（200字）",
                        "main": [
                            "方法1：异步沟通规则（350字）",
                            "方法2：结果导向管理（350字）",
                            "方法3：工具组合策略（300字）",
                            "方法4：定期反馈机制（300字）",
                            "方法5：文化建设技巧（300字）"
                        ],
                        "case": "案例展示：具体实施过程（500字）",
                        "conclusion": "注意事项（200字）"
                    }
                }
            ]
        }

        return {
            "status": "success",
            "workflow_step": 3,
            "step_outputs": {
                "step1": step1_output,
                "step2": step2_output,
                "step3": step3_output
            },
            "next_steps": [
                "Step 4: 创建协作文档",
                "Step 5: 学习个人风格",
                "Step 6: 使用个人素材库",
                "Step 7: 创作初稿",
                "Step 8: 三遍审校",
                "Step 9: 文章配图"
            ]
        }

def demo_topic_selection():
    """演示完整的选题流程"""
    print("=" * 60)
    print("Claude Code Skills 公众号选题演示")
    print("=" * 60)
    print()

    # 初始化
    demo = SkillDemo()

    # 演示场景
    topic = "远程办公效率"
    print(f"【场景】用户想写一篇关于'{topic}'的公众号文章")
    print("-" * 60)

    # 步骤1：使用知识库搜索素材
    print("\n[步骤1] 使用 [KB] 知识库 Skill 搜索相关素材")
    print("-" * 60)

    kb_results = demo.call_knowledge_base(
        keywords=["远程办公", "效率", "协作"],
        material_types=["经历", "评价", "案例", "洞察", "数据"],
        time_range="最近30天"
    )

    print(f"找到 {kb_results['count']} 条相关素材：\n")
    for i, material in enumerate(kb_results['materials'], 1):
        print(f"{i}. [{material['type']}] {material['content']}")
        print(f"   标签：{', '.join(material['tags'])} | 可信度：{material['credibility']}/10\n")

    # 步骤2：使用写作 Skill 生成选题
    print("\n[步骤2] 使用 [AI] 写作 Skill 基于素材生成选题")
    print("-" * 60)

    writer_results = demo.call_writer_skill(
        materials=kb_results['materials'],
        requirements={
            "topic": topic,
            "platform": "公众号",
            "style": "实用",
            "target_audience": "职场人士"
        }
    )

    print(f"基于素材生成了 {writer_results['topic_count']} 个选题：\n")
    for i, t in enumerate(writer_results['topics'], 1):
        print(f"选题{i}：{t['title']}")
        print(f"角度：{t['angle']}")
        print(f"独特价值：{t['unique_value']}")
        print(f"工作量：{t['workload']} | 预计字数：{t['estimated_words']}字\n")

    # 步骤3：使用写作工作流进行完整选题
    print("\n[步骤3] 使用 [Workflow] writing_workflow Skill 进行完整选题")
    print("-" * 60)

    # 创建简报
    brief = {
        "project_name": "远程办公效率文章",
        "platform": "公众号",
        "publish_date": "2024-12-20",
        "topic": topic,
        "word_count": 2500,
        "special_requirements": "需要有真实案例和数据支撑",
        "selected_topic": "工具对比类"
    }

    workflow_results = demo.call_workflow_skill(brief=brief)

    print("【Step 3】选题讨论结果：\n")
    topics = workflow_results['step_outputs']['step3']['alternatives']
    for i, t in enumerate(topics, 1):
        print(f"方案{i}：{t['title']}")
        print(f"核心角度：{t['angle']}")
        print(f"工作量评估：{t['workload']}")
        print(f"优势：{', '.join(t['advantages'])}")
        print(f"劣势：{', '.join(t['disadvantages'])}")
        print(f"是否需要测试：{'是' if t['needs_test'] else '否'}")

        print("\n大纲结构：")
        outline = t['outline']
        if isinstance(outline, dict):
            for section, content in outline.items():
                if isinstance(content, list):
                    print(f"  {section}：")
                    for item in content:
                        print(f"    - {item}")
                else:
                    print(f"  {section}：{content}")
        print()

    print("下一步流程：")
    for step in workflow_results['next_steps']:
        print(f"  - {step}")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\n总结：")
    print("1. 知识库 Skill 帮助快速找到相关素材，确保内容真实可信")
    print("2. 写作 Skill 基于素材智能生成多个选题方案")
    print("3. 写作工作流 Skill 提供系统化的创作流程")
    print("\n通过 Skills 的组合使用，将选题过程系统化，提高创作效率和质量！")

if __name__ == "__main__":
    demo_topic_selection()