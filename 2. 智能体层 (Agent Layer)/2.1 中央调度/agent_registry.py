#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
喵学堂中央调度智能体 - 代理注册表
管理所有可用技能和代理的注册信息
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json
import os

@dataclass
class AgentCapability:
    """代理能力描述"""
    name: str
    description: str
    input_types: List[str]  # 支持的输入类型
    output_types: List[str]  # 支持的输出类型
    limitations: List[str] = field(default_factory=list)
    version: str = "1.0.0"

@dataclass
class RegisteredAgent:
    """注册代理信息"""
    agent_id: str
    name: str
    description: str
    skill_name: Optional[str] = None  # 对应的Claude技能名称
    capabilities: List[AgentCapability] = field(default_factory=list)
    is_active: bool = True
    priority: int = 5  # 优先级，1-10，越高越优先
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentRegistry:
    """代理注册表管理所有可用代理"""

    def __init__(self, config_file: Optional[str] = None):
        """
        初始化代理注册表

        Args:
            config_file: 配置文件路径，如果提供则从文件加载配置
        """
        self.agents: Dict[str, RegisteredAgent] = {}
        self.skill_to_agent: Dict[str, str] = {}  # 技能名称到代理ID的映射

        # 预定义代理配置
        self._initialize_default_agents()

        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)

    def _initialize_default_agents(self):
        """初始化默认代理配置"""
        # 图书管理员代理
        librarian_caps = [
            AgentCapability(
                name="knowledge_retrieval",
                description="从结构化知识库检索信息",
                input_types=["text_query", "concept_name", "topic"],
                output_types=["explanation", "definition", "reference"]
            ),
            AgentCapability(
                name="concept_explanation",
                description="解释学术概念",
                input_types=["concept_name", "question"],
                output_types=["detailed_explanation", "examples"]
            ),
            AgentCapability(
                name="material_recommendation",
                description="推荐学习材料",
                input_types=["topic", "skill_level", "learning_goal"],
                output_types=["resource_list", "study_path"]
            )
        ]

        librarian = RegisteredAgent(
            agent_id="librarian_001",
            name="图书管理员",
            description="管理知识库，提供知识检索和概念解释服务",
            skill_name="learning-librarian",
            capabilities=librarian_caps,
            priority=7
        )
        self.register_agent(librarian)

        # 授课老师代理
        teacher_caps = [
            AgentCapability(
                name="systematic_explanation",
                description="系统化讲解复杂主题",
                input_types=["topic", "concept", "question"],
                output_types=["step_by_step_tutorial", "examples", "analogies"]
            ),
            AgentCapability(
                name="question_answering",
                description="回答学习问题",
                input_types=["question", "problem_statement"],
                output_types=["answer", "explanation", "solution_steps"]
            ),
            AgentCapability(
                name="example_generation",
                description="生成说明性示例",
                input_types=["concept", "difficulty_level"],
                output_types=["examples", "practice_cases"]
            )
        ]

        teacher = RegisteredAgent(
            agent_id="teacher_001",
            name="授课老师",
            description="提供系统化讲解、答疑和示例生成",
            skill_name="learning-teacher",
            capabilities=teacher_caps,
            priority=8
        )
        self.register_agent(teacher)

        # 出题考官代理
        examiner_caps = [
            AgentCapability(
                name="exercise_generation",
                description="生成练习题",
                input_types=["topic", "difficulty", "question_type", "count"],
                output_types=["exercise_set", "answer_key"]
            ),
            AgentCapability(
                name="assessment_grading",
                description="评估和评分答案",
                input_types=["answer", "exercise", "rubric"],
                output_types=["grade", "feedback", "corrections"]
            ),
            AgentCapability(
                name="skill_gap_analysis",
                description="分析技能差距",
                input_types=["performance_data", "test_results"],
                output_types=["gap_analysis", "recommendations"]
            )
        ]

        examiner = RegisteredAgent(
            agent_id="examiner_001",
            name="出题考官",
            description="生成练习题、进行评估和提供反馈",
            skill_name="learning-examiner",
            capabilities=examiner_caps,
            priority=6
        )
        self.register_agent(examiner)

        # 学习伙伴代理
        companion_caps = [
            AgentCapability(
                name="emotional_support",
                description="提供情感支持和鼓励",
                input_types=["emotional_state", "challenge_description"],
                output_types=["encouragement", "motivation", "coping_strategies"]
            ),
            AgentCapability(
                name="progress_tracking",
                description="跟踪学习进度",
                input_types=["study_data", "goals"],
                output_types=["progress_report", "reminders", "celebrations"]
            ),
            AgentCapability(
                name="habit_building",
                description="帮助建立学习习惯",
                input_types=["current_habits", "goals"],
                output_types=["habit_plan", "schedule", "accountability_check"]
            )
        ]

        companion = RegisteredAgent(
            agent_id="companion_001",
            name="学习伙伴",
            description="提供情感支持、动机维护和学习陪伴",
            skill_name="learning-companion",
            capabilities=companion_caps,
            priority=5
        )
        self.register_agent(companion)

        # 学情分析师代理
        analyst_caps = [
            AgentCapability(
                name="performance_analysis",
                description="分析学习表现数据",
                input_types=["performance_data", "historical_records"],
                output_types=["analysis_report", "trends", "insights"]
            ),
            AgentCapability(
                name="gap_diagnosis",
                description="诊断知识差距",
                input_types=["test_results", "learning_history"],
                output_types=["gap_report", "priority_areas"]
            ),
            AgentCapability(
                name="recommendation_generation",
                description="生成个性化学习建议",
                input_types=["analysis_results", "learning_goals"],
                output_types=["recommendations", "study_plan"]
            )
        ]

        analyst = RegisteredAgent(
            agent_id="analyst_001",
            name="学情分析师",
            description="分析学习数据、诊断差距、提供优化建议",
            skill_name="learning-analyst",
            capabilities=analyst_caps,
            priority=7
        )
        self.register_agent(analyst)

    def register_agent(self, agent: RegisteredAgent):
        """注册一个新代理"""
        self.agents[agent.agent_id] = agent

        if agent.skill_name:
            self.skill_to_agent[agent.skill_name] = agent.agent_id

        print(f"注册代理: {agent.name} ({agent.agent_id})")

    def get_agent_by_id(self, agent_id: str) -> Optional[RegisteredAgent]:
        """根据ID获取代理"""
        return self.agents.get(agent_id)

    def get_agent_by_skill(self, skill_name: str) -> Optional[RegisteredAgent]:
        """根据技能名称获取代理"""
        agent_id = self.skill_to_agent.get(skill_name)
        if agent_id:
            return self.agents.get(agent_id)
        return None

    def find_agents_by_capability(self, capability_name: str) -> List[RegisteredAgent]:
        """根据能力名称查找代理"""
        matching_agents = []
        for agent in self.agents.values():
            for cap in agent.capabilities:
                if cap.name == capability_name:
                    matching_agents.append(agent)
                    break
        return matching_agents

    def select_agent_for_intent(self, intent: str, context: Dict = None) -> Optional[RegisteredAgent]:
        """
        根据意图选择最合适的代理

        Args:
            intent: 意图类型（knowledge_query, learning_explanation等）
            context: 可选上下文信息

        Returns:
            选择的代理或None
        """
        # 意图到代理ID的映射
        intent_to_agent = {
            "knowledge_query": "librarian_001",
            "learning_explanation": "teacher_001",
            "practice_testing": "examiner_001",
            "progress_review": "analyst_001",
            "emotional_support": "companion_001",
            "system_configuration": None  # 待实现
        }

        agent_id = intent_to_agent.get(intent)
        if agent_id:
            return self.get_agent_by_id(agent_id)

        # 如果映射中没有，尝试根据能力查找
        intent_capability_map = {
            "knowledge_query": "knowledge_retrieval",
            "learning_explanation": "systematic_explanation",
            "practice_testing": "exercise_generation",
            "progress_review": "performance_analysis",
            "emotional_support": "emotional_support",
        }

        capability = intent_capability_map.get(intent)
        if capability:
            agents = self.find_agents_by_capability(capability)
            if agents:
                # 返回优先级最高的代理
                return max(agents, key=lambda a: a.priority)

        return None

    def list_all_agents(self) -> List[Dict]:
        """列出所有代理的摘要信息"""
        result = []
        for agent in self.agents.values():
            result.append({
                "id": agent.agent_id,
                "name": agent.name,
                "description": agent.description,
                "skill": agent.skill_name,
                "active": agent.is_active,
                "capabilities": [cap.name for cap in agent.capabilities]
            })
        return result

    def save_to_file(self, filepath: str):
        """将代理配置保存到文件"""
        data = {
            "agents": {},
            "skill_mapping": self.skill_to_agent
        }

        for agent_id, agent in self.agents.items():
            # 将代理对象转换为可序列化的字典
            agent_dict = {
                "agent_id": agent.agent_id,
                "name": agent.name,
                "description": agent.description,
                "skill_name": agent.skill_name,
                "is_active": agent.is_active,
                "priority": agent.priority,
                "metadata": agent.metadata,
                "capabilities": []
            }

            for cap in agent.capabilities:
                cap_dict = {
                    "name": cap.name,
                    "description": cap.description,
                    "input_types": cap.input_types,
                    "output_types": cap.output_types,
                    "limitations": cap.limitations,
                    "version": cap.version
                }
                agent_dict["capabilities"].append(cap_dict)

            data["agents"][agent_id] = agent_dict

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"代理配置已保存到: {filepath}")

    def load_from_file(self, filepath: str):
        """从文件加载代理配置"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 清空当前注册表
            self.agents.clear()
            self.skill_to_agent.clear()

            # 加载代理
            for agent_id, agent_data in data.get("agents", {}).items():
                capabilities = []
                for cap_data in agent_data.get("capabilities", []):
                    cap = AgentCapability(
                        name=cap_data["name"],
                        description=cap_data["description"],
                        input_types=cap_data["input_types"],
                        output_types=cap_data["output_types"],
                        limitations=cap_data.get("limitations", []),
                        version=cap_data.get("version", "1.0.0")
                    )
                    capabilities.append(cap)

                agent = RegisteredAgent(
                    agent_id=agent_data["agent_id"],
                    name=agent_data["name"],
                    description=agent_data["description"],
                    skill_name=agent_data.get("skill_name"),
                    capabilities=capabilities,
                    is_active=agent_data.get("is_active", True),
                    priority=agent_data.get("priority", 5),
                    metadata=agent_data.get("metadata", {})
                )

                self.register_agent(agent)

            # 加载技能映射
            self.skill_to_agent = data.get("skill_mapping", {})

            print(f"从 {filepath} 加载了 {len(self.agents)} 个代理")

        except Exception as e:
            print(f"加载配置文件失败: {e}")


# 示例使用
if __name__ == "__main__":
    # 创建注册表实例
    registry = AgentRegistry()

    # 列出所有代理
    print("喵学堂代理注册表")
    print("=" * 60)

    agents_summary = registry.list_all_agents()
    for agent in agents_summary:
        print(f"ID: {agent['id']}")
        print(f"名称: {agent['name']}")
        print(f"描述: {agent['description']}")
        print(f"技能: {agent['skill']}")
        print(f"能力: {', '.join(agent['capabilities'])}")
        print(f"状态: {'活跃' if agent['active'] else '停用'}")
        print("-" * 60)

    # 测试意图到代理的选择
    print("\n意图到代理选择测试:")
    test_intents = [
        "knowledge_query",
        "learning_explanation",
        "practice_testing",
        "progress_review",
        "emotional_support",
        "unknown_intent"
    ]

    for intent in test_intents:
        agent = registry.select_agent_for_intent(intent)
        if agent:
            print(f"意图 '{intent}' → 选择代理: {agent.name} ({agent.agent_id})")
        else:
            print(f"意图 '{intent}' → 没有找到合适的代理")

    # 保存配置到文件
    registry.save_to_file("agent_registry_backup.json")
    print("\n配置已保存到 agent_registry_backup.json")