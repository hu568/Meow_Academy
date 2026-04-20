#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
喵学堂中央调度智能体 - 主调度器
整合意图分类器和代理注册表，实现完整的调度功能
"""

import sys
import os
from typing import Dict, Any, Optional

# 添加当前目录到Python路径，以便导入本地模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from intent_classifier import IntentClassifier
from agent_registry import AgentRegistry, RegisteredAgent


class LearningDispatcher:
    """学习调度器 - 中央协调组件"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化调度器

        Args:
            config_path: 代理配置文件的路径
        """
        print("初始化学习调度器...")

        # 初始化组件
        self.intent_classifier = IntentClassifier()
        self.agent_registry = AgentRegistry(config_path)

        # 会话状态
        self.session_context: Dict[str, Any] = {
            "user_id": None,
            "current_topic": None,
            "learning_level": "beginner",
            "preferred_style": "balanced",
            "recent_intents": [],
            "skill_usage_count": {}
        }

        print("学习调度器初始化完成")
        print(f"已注册代理: {len(self.agent_registry.agents)} 个")

    def process_request(self, user_input: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        处理用户请求的主入口

        Args:
            user_input: 用户输入的文本
            user_id: 用户标识符

        Returns:
            包含处理结果的字典
        """
        print(f"\n处理用户请求: {user_input}")

        # 更新会话上下文
        self.session_context["user_id"] = user_id

        # 步骤1: 意图识别
        intent_result = self.intent_classifier.analyze_with_details(user_input)
        primary_intent = intent_result["primary_intent"]
        confidence = intent_result["confidence"]

        print(f"识别意图: {primary_intent} (置信度: {confidence:.2f})")

        # 记录意图历史
        self.session_context["recent_intents"].append({
            "intent": primary_intent,
            "input": user_input,
            "confidence": confidence,
            "timestamp": self._get_current_timestamp()
        })

        # 只保留最近10个意图
        self.session_context["recent_intents"] = self.session_context["recent_intents"][-10:]

        # 步骤2: 选择代理
        selected_agent = self.agent_registry.select_agent_for_intent(primary_intent)
        if not selected_agent:
            return self._create_error_response(
                "未找到适合处理此意图的代理",
                intent_result=intent_result
            )

        print(f"选择代理: {selected_agent.name}")

        # 步骤3: 准备执行上下文
        execution_context = self._prepare_execution_context(
            user_input, primary_intent, selected_agent, intent_result
        )

        # 步骤4: 生成代理调用指令
        dispatch_instruction = self._generate_dispatch_instruction(
            selected_agent, user_input, execution_context
        )

        # 步骤5: 更新使用统计
        self._update_skill_usage(selected_agent.skill_name)

        # 步骤6: 构建响应
        response = self._build_response(
            user_input=user_input,
            intent_result=intent_result,
            selected_agent=selected_agent,
            dispatch_instruction=dispatch_instruction,
            execution_context=execution_context
        )

        return response

    def _prepare_execution_context(self, user_input: str, intent: str,
                                   agent: RegisteredAgent,
                                   intent_result: Dict) -> Dict[str, Any]:
        """准备执行上下文"""
        context = {
            "user_input": user_input,
            "detected_intent": intent,
            "intent_confidence": intent_result["confidence"],
            "intent_scores": intent_result["intent_scores"],
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "agent_capabilities": [cap.name for cap in agent.capabilities],
            "user_context": self.session_context.copy(),
            "recommended_approach": self._get_recommended_approach(intent, agent)
        }

        # 添加上下文增强信息
        if self.session_context["current_topic"]:
            context["current_learning_topic"] = self.session_context["current_topic"]

        if self.session_context["recent_intents"]:
            context["recent_interaction_pattern"] = self._analyze_interaction_pattern()

        return context

    def _generate_dispatch_instruction(self, agent: RegisteredAgent,
                                       user_input: str,
                                       context: Dict) -> Dict[str, Any]:
        """生成代理调度指令"""
        if agent.skill_name:
            # 使用Claude技能
            instruction = {
                "type": "skill_invocation",
                "skill_name": agent.skill_name,
                "invocation_method": "direct",
                "suggested_prompt": user_input,
                "additional_context": {
                    "intent": context["detected_intent"],
                    "user_level": context["user_context"]["learning_level"],
                    "preferred_style": context["user_context"]["preferred_style"]
                }
            }
        else:
            # 使用Agent工具（如果可用）
            instruction = {
                "type": "agent_tool",
                "agent_type": "general-purpose",
                "description": f"Execute {agent.name} task",
                "prompt": self._create_agent_prompt(agent, user_input, context),
                "expected_output": "Detailed response from specialized agent"
            }

        return instruction

    def _create_agent_prompt(self, agent: RegisteredAgent, user_input: str,
                             context: Dict) -> str:
        """创建Agent工具的提示"""
        capabilities = ", ".join([cap.name for cap in agent.capabilities[:3]])

        prompt = f"""作为{agent.name}，请处理以下用户请求：

用户输入: {user_input}

上下文信息:
- 检测到的意图: {context['detected_intent']}
- 用户水平: {context['user_context']['learning_level']}
- 最近话题: {context.get('current_learning_topic', '无')}

你的能力包括: {capabilities}

请以{agent.name}的身份专业地回应用户请求，提供详细、准确的帮助。"""

        return prompt

    def _build_response(self, user_input: str, intent_result: Dict,
                        selected_agent: RegisteredAgent,
                        dispatch_instruction: Dict,
                        execution_context: Dict) -> Dict[str, Any]:
        """构建完整响应"""
        response = {
            "status": "success",
            "user_input": user_input,
            "intent_analysis": {
                "primary_intent": intent_result["primary_intent"],
                "confidence": intent_result["confidence"],
                "all_scores": intent_result["intent_scores"],
                "recommended_skill": intent_result["recommended_skill"]
            },
            "agent_selection": {
                "agent_id": selected_agent.agent_id,
                "agent_name": selected_agent.name,
                "agent_description": selected_agent.description,
                "skill_name": selected_agent.skill_name,
                "capabilities": [cap.name for cap in selected_agent.capabilities]
            },
            "dispatch_instruction": dispatch_instruction,
            "execution_context": execution_context,
            "user_message": self._create_user_friendly_message(
                selected_agent, intent_result["primary_intent"], user_input
            ),
            "suggested_next_steps": self._suggest_next_steps(
                intent_result["primary_intent"], selected_agent
            ),
            "timestamp": self._get_current_timestamp()
        }

        return response

    def _create_user_friendly_message(self, agent: RegisteredAgent,
                                      intent: str, user_input: str) -> str:
        """创建用户友好的消息"""
        messages = {
            "knowledge_query": f"我将作为{agent.name}为您查找相关信息。",
            "learning_explanation": f"我将作为{agent.name}为您详细讲解。",
            "practice_testing": f"我将作为{agent.name}为您准备练习题目。",
            "progress_review": f"我将作为{agent.name}为您分析学习进度。",
            "emotional_support": f"我将作为{agent.name}为您提供支持。",
        }

        default_message = f"我将作为{agent.name}为您提供帮助。"

        return messages.get(intent, default_message)

    def _suggest_next_steps(self, intent: str, agent: RegisteredAgent) -> List[str]:
        """建议下一步操作"""
        suggestions = {
            "knowledge_query": [
                "您可以进一步询问相关概念",
                "请求更多示例来加深理解",
                "探索相关知识点的联系"
            ],
            "learning_explanation": [
                "尝试用自己的话复述概念",
                "请求一些练习题来巩固理解",
                "询问实际应用场景"
            ],
            "practice_testing": [
                "完成练习后请求答案解析",
                "根据表现调整题目难度",
                "针对错题请求额外讲解"
            ],
            "progress_review": [
                "根据分析结果调整学习计划",
                "针对薄弱点进行专项练习",
                "设定下一阶段的学习目标"
            ],
            "emotional_support": [
                "设定小而可行的学习目标",
                "安排规律的休息时间",
                "庆祝每一个小进步"
            ]
        }

        return suggestions.get(intent, [
            "继续学习当前话题",
            "探索相关知识点",
            "休息一下，保持学习动力"
        ])

    def _get_recommended_approach(self, intent: str, agent: RegisteredAgent) -> str:
        """获取推荐的处理方法"""
        approaches = {
            "knowledge_query": "先提供简明定义，再补充详细解释和示例",
            "learning_explanation": "从基础概念开始，逐步深入，使用多种教学方式",
            "practice_testing": "根据用户水平生成适当难度的题目，提供详细解答",
            "progress_review": "客观分析数据，提供具体改进建议，保持积极鼓励",
            "emotional_support": "共情理解，提供实用建议，持续鼓励支持"
        }

        return approaches.get(intent, "根据具体情境提供个性化帮助")

    def _analyze_interaction_pattern(self) -> Dict[str, Any]:
        """分析交互模式"""
        if not self.session_context["recent_intents"]:
            return {"pattern": "no_data", "frequency": {}}

        # 统计意图频率
        intent_counts = {}
        for entry in self.session_context["recent_intents"]:
            intent = entry["intent"]
            intent_counts[intent] = intent_counts.get(intent, 0) + 1

        # 识别主要模式
        total = len(self.session_context["recent_intents"])
        pattern = "balanced"
        if intent_counts.get("emotional_support", 0) / total > 0.4:
            pattern = "support_seeking"
        elif intent_counts.get("practice_testing", 0) / total > 0.5:
            pattern = "practice_focused"
        elif intent_counts.get("knowledge_query", 0) / total > 0.6:
            pattern = "information_seeking"

        return {
            "pattern": pattern,
            "frequency": intent_counts,
            "total_interactions": total
        }

    def _update_skill_usage(self, skill_name: Optional[str]):
        """更新技能使用统计"""
        if skill_name:
            self.session_context["skill_usage_count"][skill_name] = \
                self.session_context["skill_usage_count"].get(skill_name, 0) + 1

    def _create_error_response(self, error_message: str, **kwargs) -> Dict[str, Any]:
        """创建错误响应"""
        response = {
            "status": "error",
            "error_message": error_message,
            "timestamp": self._get_current_timestamp()
        }
        response.update(kwargs)
        return response

    def _get_current_timestamp(self) -> str:
        """获取当前时间戳（简化版）"""
        import datetime
        return datetime.datetime.now().isoformat()

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "total_agents": len(self.agent_registry.agents),
            "active_agents": len([a for a in self.agent_registry.agents.values()
                                  if a.is_active]),
            "session_context": self.session_context,
            "agent_summary": self.agent_registry.list_all_agents()
        }


# 示例使用
if __name__ == "__main__":
    print("喵学堂中央调度智能体 - 演示")
    print("=" * 60)

    # 创建调度器实例
    dispatcher = LearningDispatcher()

    # 显示系统状态
    status = dispatcher.get_system_status()
    print(f"系统状态: {status['total_agents']} 个代理已注册")
    print(f"活跃代理: {status['active_agents']} 个")
    print()

    # 测试处理请求
    test_requests = [
        "什么是相对论？",
        "请讲解微积分的基本定理",
        "给我一些线性代数练习题",
        "我的学习进度怎么样？",
        "我学习没有动力了",
        "如何设置学习目标？"
    ]

    for i, request in enumerate(test_requests, 1):
        print(f"\n测试 {i}: {request}")
        print("-" * 40)

        result = dispatcher.process_request(request, user_id="test_user")

        if result["status"] == "success":
            print(f"识别意图: {result['intent_analysis']['primary_intent']}")
            print(f"选择代理: {result['agent_selection']['agent_name']}")
            print(f"用户消息: {result['user_message']}")

            # 显示调度指令
            instr = result["dispatch_instruction"]
            print(f"调度类型: {instr['type']}")
            if instr['type'] == 'skill_invocation':
                print(f"调用技能: {instr['skill_name']}")
        else:
            print(f"错误: {result['error_message']}")

        print()

    # 显示最终系统状态
    print("\n最终系统状态:")
    final_status = dispatcher.get_system_status()
    print(f"会话上下文: {final_status['session_context']['user_id']}")
    print(f"技能使用统计: {final_status['session_context']['skill_usage_count']}")
    print(f"最近意图: {len(final_status['session_context']['recent_intents'])} 条记录")

    print("\n演示完成！")