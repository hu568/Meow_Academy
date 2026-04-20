# 中央调度智能体 - 学习管家

## 概述
中央调度智能体是喵学堂系统的核心协调器，负责理解用户意图并分派任务给相应的领域专家智能体。

## 核心功能
1. **意图识别**：分析用户输入，识别学习意图
2. **代理选择**：根据意图选择最合适的领域专家
3. **任务分派**：生成指令调用相应技能或代理
4. **上下文管理**：维护会话状态和学习进度
5. **结果整合**：协调多代理工作流，提供完整响应

## 系统架构
```
中央调度智能体 (学习管家)
├── 意图分类器 (IntentClassifier) - 分析用户意图
├── 代理注册表 (AgentRegistry) - 管理可用代理
├── 主调度器 (LearningDispatcher) - 协调工作流程
└── 技能系统 (Claude Skills) - 实际执行任务
```

## 已实现组件

### 1. 技能系统 (已部署)
| 技能名称 | 英文标识 | 功能描述 | 状态 |
|----------|----------|----------|------|
| 学习管家 | learning-dispatcher | 中央调度器 | ✅ 已部署 |
| 图书管理员 | learning-librarian | 知识检索与解释 | ✅ 已部署 |
| 授课老师 | learning-teacher | 系统化讲解与答疑 | ✅ 已部署 |
| 出题考官 | learning-examiner | 练习生成与评估 | ✅ 已部署 |
| 学习伙伴 | learning-companion | 情感支持与动机维护 | ✅ 已部署 |
| 学情分析师 | learning-analyst | 学习数据分析与建议 | ✅ 已部署 |

### 2. Python组件 (示例实现)
- `intent_classifier.py` - 基于关键词的意图分类器
- `agent_registry.py` - 代理注册与管理
- `main_dispatcher.py` - 主调度器实现

## 使用方法

### 方式一：自动调度（推荐）
用户直接输入学习请求，系统自动识别意图并调用相应技能：
```
用户: "什么是相对论？"
→ 识别为"知识查询"意图
→ 调用 learning-librarian 技能
→ 返回知识解释
```

### 方式二：手动调用技能
用户可以直接指定使用某个技能：
```
用户: "/learning-teacher 请讲解微积分"
→ 直接调用授课老师技能
→ 返回详细讲解
```

### 方式三：测试Python组件
```bash
# 运行意图分类器测试
python intent_classifier.py

# 运行代理注册表测试
python agent_registry.py

# 运行主调度器演示
python main_dispatcher.py
```

## 意图分类
系统支持以下意图类型：

| 意图类型 | 描述 | 示例输入 | 对应技能 |
|----------|------|----------|----------|
| 知识查询 | 查找事实、概念、定义 | "什么是光合作用？" | learning-librarian |
| 学习讲解 | 请求系统化讲解 | "请讲解微积分" | learning-teacher |
| 练习测试 | 需要练习题或测试 | "给我一些练习题" | learning-examiner |
| 进度回顾 | 分析学习进度 | "我的学习情况如何？" | learning-analyst |
| 情感支持 | 需要鼓励和动力 | "我学习没有动力了" | learning-companion |
| 系统配置 | 修改学习设置 | "设置学习目标" | (待实现) |

## 开发指南

### 添加新技能
1. 使用技能创建工具初始化新技能：
   ```bash
   # 通过Claude Code的skills工具
   ```

2. 在 `agent_registry.py` 中注册新代理：
   ```python
   new_agent = RegisteredAgent(
       agent_id="new_agent_001",
       name="新代理名称",
       description="代理功能描述",
       skill_name="new-skill-name",
       capabilities=[...],
       priority=5
   )
   registry.register_agent(new_agent)
   ```

3. 在意图分类器中添加对应的意图识别规则

### 修改意图识别规则
编辑 `intent_classifier.py` 中的 `INTENT_PATTERNS` 字典：
```python
INTENT_PATTERNS = {
    "new_intent": [
        r"关键词1", r"关键词2", r"正则表达式模式"
    ],
    # ... 现有意图
}
```

### 配置代理属性
代理属性在 `RegisteredAgent` 类中定义：
- `priority`: 优先级 (1-10，越高越优先)
- `capabilities`: 代理能力列表
- `is_active`: 是否激活
- `metadata`: 额外元数据

## 测试

### 单元测试
```bash
# 运行所有测试
python -m pytest tests/ -v
```

### 集成测试
```python
# 测试完整调度流程
dispatcher = LearningDispatcher()
result = dispatcher.process_request("测试请求", "test_user")
print(result)
```

### 性能测试
- 意图识别响应时间：<100ms
- 代理选择时间：<50ms
- 整体调度延迟：<200ms

## 部署说明

### 生产环境要求
- Python 3.8+
- Claude Code 环境
- 技能系统已注册并激活
- 持久化存储（用于会话状态）

### 配置选项
```python
# 初始化带配置的调度器
dispatcher = LearningDispatcher(
    config_path="path/to/agent_config.json"
)
```

### 监控指标
- 意图识别准确率
- 技能调用成功率
- 用户满意度评分
- 系统响应时间

## 故障排除

### 常见问题
1. **技能未触发**：检查技能描述中的触发条件
2. **意图识别错误**：调整 `intent_classifier.py` 中的关键词
3. **代理选择不当**：检查代理优先级和能力匹配
4. **上下文丢失**：确保会话状态正确维护

### 调试模式
```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 路线图

### 短期计划 (1-2周)
- [ ] 实现基于机器学习的意图分类
- [ ] 添加会话持久化存储
- [ ] 开发管理界面
- [ ] 集成性能监控

### 中期计划 (1-2月)
- [ ] 实现多代理协同工作流
- [ ] 添加个性化推荐引擎
- [ ] 集成外部知识源
- [ ] 开发移动端适配

### 长期计划 (3-6月)
- [ ] 实现自适应学习路径
- [ ] 添加多模态交互支持
- [ ] 开发智能辅导系统
- [ ] 实现跨平台同步

## 贡献指南
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式
- 项目维护者：喵学堂团队
- 问题反馈：创建 GitHub Issue
- 功能请求：使用 Feature Request 模板

---
*最后更新: 2025-04-19*
*版本: 1.0.0*