#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
喵学堂中央调度智能体 - 意图分类器
简单基于关键词的意图识别实现
"""

import re
from typing import Dict, List, Tuple, Optional

class IntentClassifier:
    """基于关键词和规则的模式匹配意图分类器"""

    # 意图关键词映射
    INTENT_PATTERNS = {
        "knowledge_query": [
            r"什么是", r"什么叫", r"定义", r"含义", r"解释一下",
            r"什么意思", r"指的是什么", r"如何理解", r"概念",
            r"查找", r"搜索", r"查询", r"了解", r"什么是.*?", r"定义.*?",
        ],
        "learning_explanation": [
            r"讲解", r"教教", r"教学", r"授课", r"说明",
            r"详细介绍", r"系统讲解", r"从头讲", r"基础讲解",
            r"如何学习", r"怎么学", r"学习方法", r"学习.*?的步骤",
            r"分步讲解", r"逐步说明", r"详细解释",
        ],
        "practice_testing": [
            r"练习题", r"习题", r"题目", r"试题", r"考试",
            r"测试", r"测验", r"作业", r"练习", r"刷题",
            r"出题", r"生成.*?题", r"做.*?题", r"考题",
            r"模拟考试", r"真题", r"试卷",
        ],
        "progress_review": [
            r"进度", r"进展", r"学习情况", r"学习状态",
            r"掌握程度", r"学习效果", r"评估", r"评价",
            r"分析.*?学习", r"学习报告", r"学习总结",
            r"薄弱点", r"强项", r"需要改进", r"提升空间",
        ],
        "emotional_support": [
            r"鼓励", r"激励", r"动力", r"没劲", r"不想学",
            r"坚持不下去", r"放弃", r"沮丧", r"灰心",
            r"陪伴", r"支持", r"帮助", r"安慰", r"加油",
            r"陪伴学习", r"一起学习", r"监督", r"提醒",
        ],
        "system_configuration": [
            r"设置", r"配置", r"设定", r"调整", r"修改",
            r"偏好", r"个性化", r"自定义", r"目标",
            r"计划", r"安排", r"时间表", r"学习计划",
        ]
    }

    # 意图到技能的映射
    INTENT_TO_SKILL = {
        "knowledge_query": "learning-librarian",
        "learning_explanation": "learning-teacher",
        "practice_testing": "learning-examiner",
        "progress_review": "learning-analyst",
        "emotional_support": "learning-companion",
        "system_configuration": "config-manager",  # 待实现
    }

    def __init__(self):
        """初始化分类器，编译正则表达式"""
        self.compiled_patterns = {}
        for intent, patterns in self.INTENT_PATTERNS.items():
            compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
            self.compiled_patterns[intent] = compiled

    def classify(self, text: str) -> Tuple[str, float, Dict]:
        """
        对输入文本进行意图分类

        Args:
            text: 用户输入的文本

        Returns:
            tuple: (主要意图, 置信度, 所有意图得分)
        """
        text = text.strip().lower()

        # 计算每个意图的匹配分数
        intent_scores = {}
        for intent, patterns in self.compiled_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern.search(text):
                    score += 1
            intent_scores[intent] = score

        # 找到得分最高的意图
        if not intent_scores:
            return "unknown", 0.0, intent_scores

        max_score = max(intent_scores.values())
        if max_score == 0:
            return "unknown", 0.0, intent_scores

        # 找出所有得分最高的意图（处理平局）
        top_intents = [intent for intent, score in intent_scores.items()
                      if score == max_score]

        # 如果有多个意图得分相同，使用优先级规则
        primary_intent = self._resolve_tie(top_intents, text)

        # 计算置信度（归一化到0-1）
        total_score = sum(intent_scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.0

        return primary_intent, confidence, intent_scores

    def _resolve_tie(self, intents: List[str], text: str) -> str:
        """解决多个意图得分相同的情况"""
        # 优先级顺序
        priority_order = [
            "knowledge_query",
            "learning_explanation",
            "practice_testing",
            "progress_review",
            "emotional_support",
            "system_configuration"
        ]

        for intent in priority_order:
            if intent in intents:
                return intent

        # 如果都不在优先级列表中，返回第一个
        return intents[0]

    def get_skill_for_intent(self, intent: str) -> Optional[str]:
        """获取意图对应的技能名称"""
        return self.INTENT_TO_SKILL.get(intent)

    def analyze_with_details(self, text: str) -> Dict:
        """
        详细分析文本，返回完整的分类结果

        Returns:
            dict: 包含意图、置信度、推荐技能等详细信息
        """
        intent, confidence, scores = self.classify(text)

        return {
            "text": text,
            "primary_intent": intent,
            "confidence": confidence,
            "intent_scores": scores,
            "recommended_skill": self.get_skill_for_intent(intent),
            "skill_mapping": self.INTENT_TO_SKILL
        }


# 示例使用
if __name__ == "__main__":
    classifier = IntentClassifier()

    # 测试用例
    test_cases = [
        "什么是相对论？",
        "请讲解微积分的基本定理",
        "给我一些线性代数练习题",
        "我的学习进度怎么样？",
        "我学习没有动力了",
        "设置我的学习目标",
        "我想学习量子力学",
    ]

    print("意图分类器测试：")
    print("=" * 50)

    for test in test_cases:
        result = classifier.analyze_with_details(test)
        print(f"输入: {test}")
        print(f"主要意图: {result['primary_intent']}")
        print(f"置信度: {result['confidence']:.2f}")
        print(f"推荐技能: {result['recommended_skill']}")
        print(f"得分: {result['intent_scores']}")
        print("-" * 50)