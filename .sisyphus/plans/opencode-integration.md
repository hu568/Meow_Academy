# OpenCode 接入喵学堂 - 工作计划

## TL;DR

> **目标**: 配置 OpenCode 通过 MCP 协议连接喵学堂项目目录，使 AI 能够读写全部文件并执行命令，实现完整的开发工作流。
>
> **交付物**:
> - MCP 配置文件（OpenCode 设置）
> - 项目上下文文件（AI 理解架构）
> - 验证测试（确保连接正常）
>
> **预计工作量**: 短（Short）
> **并行执行**: YES - 2 个 Wave
> **关键路径**: T1 → T2 → T3 → F1-F3

---

## Context

### 原始需求
用户希望 AI 编码工具（OpenCode）能够连接到喵学堂项目目录，直接操作文件和执行命令。

### 讨论结果
- **AI 工具**: OpenCode（支持 MCP 协议）
- **权限范围**: 全部目录（知识层 + 智能体层 + 用户层）
- **操作类型**: 完整开发工作流（文件读写 + 命令执行 + 代码分析）
- **技术方案**: MCP（Model Context Protocol）
- **项目根目录**: `E:\Meow_Academy`
- **架构文档**: `喵学堂架构.txt`

### 架构概览
喵学堂是一个三层学习系统：
1. **知识层**: 原始资料库 + 结构化知识库（学科模板）
2. **智能体层**: 中央调度 + 5 个领域专家 Agent + 工具箱
3. **用户层**: 学习者画像 + 会话状态 + 学习档案 + 配置文件

---

## Work Objectives

### 核心目标
配置 OpenCode 通过 MCP 协议连接喵学堂项目，实现 AI 对项目目录的完整访问和操作能力。

### 具体交付物
- `.opencode/mcp.json` - MCP 服务器配置文件
- `.opencode/project-context.md` - 项目上下文说明
- `.opencode/README.md` - 使用说明
- 验证脚本 - 测试连接和功能

### 完成标准
- [ ] OpenCode 能读取喵学堂目录下的文件
- [ ] OpenCode 能创建和修改文件
- [ ] OpenCode 能执行 shell 命令
- [ ] AI 理解喵学堂的架构和文件组织

### 必须包含
- MCP 配置文件（filesystem + command 工具）
- 项目架构说明（让 AI 理解目录结构）
- 使用示例和验证方法

### 明确排除（Guardrails）
- 不修改喵学堂的核心业务代码
- 不创建复杂的 Agent 实现（仅配置连接）
- 不部署到远程服务器（本地开发环境）
- 不处理身份验证（假设本地安全环境）

---

## Verification Strategy

### 测试决策
- **基础设施**: 不适用（配置任务，无传统测试框架）
- **自动化测试**: 无（使用 Agent 执行的 QA 场景验证）
- **验证方式**: Agent 直接操作验证

### QA 策略
每个任务包含 Agent 执行的 QA 场景：
- **文件操作**: Bash 命令验证文件读写
- **命令执行**: Bash 命令验证命令执行
- **AI 理解**: 验证 AI 能正确回答架构相关问题

---

## Execution Strategy

### 并行执行 Wave

```
Wave 1 (立即开始 - 配置和上下文):
├── Task 1: 创建 MCP 配置文件 [quick]
├── Task 2: 创建项目上下文文件 [quick]
└── Task 3: 创建使用说明文档 [quick]

Wave 2 (Wave 1 完成后 - 验证和优化):
├── Task 4: 验证文件系统访问 [quick]
├── Task 5: 验证命令执行 [quick]
└── Task 6: 验证 AI 架构理解 [quick]

Wave FINAL (所有任务后 - 审查):
├── Task F1: 配置完整性检查 [quick]
├── Task F2: 功能验证 [quick]
└── Task F3: 文档审查 [quick]
-> 向用户展示结果 -> 获得明确确认

关键路径: T1 → T2 → T3 → T4 → T5 → T6 → F1-F3 → 用户确认
并行加速: Wave 1 内 3 个任务可并行
```

### 依赖矩阵

- **T1**: - - T4, T5
- **T2**: - - T6
- **T3**: - - F3
- **T4**: T1 - F1, F2
- **T5**: T1 - F1, F2
- **T6**: T2 - F1, F3
- **F1**: T4, T5, T6 - 完成
- **F2**: T4, T5 - 完成
- **F3**: T3, T6 - 完成

### Agent 分配

- **Wave 1**: **3** - T1 → `quick`, T2 → `quick`, T3 → `quick`
- **Wave 2**: **3** - T4 → `quick`, T5 → `quick`, T6 → `quick`
- **FINAL**: **3** - F1 → `quick`, F2 → `quick`, F3 → `quick`

---

## TODOs

- [ ] 1. **创建 MCP 配置文件**

  **What to do**:
  - 在 `.opencode/` 目录下创建 `mcp.json` 配置文件
  - 配置 filesystem 工具：允许访问 `E:\Meow_Academy` 目录及其所有子目录
  - 配置 command 工具：允许执行 shell 命令（用于构建、测试等）
  - 确保配置使用正斜杠路径（跨平台兼容）
  - 设置合理的权限范围（只读 vs 读写）

  **Must NOT do**:
  - 不要包含敏感信息（密码、API 密钥等）
  - 不要限制特定文件类型（让 AI 能访问所有文件）
  - 不要配置远程服务器（仅本地目录）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 纯配置文件创建，无需复杂逻辑
  - **Skills**: []
    - 无需特殊技能

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1（与 T2、T3 并行）
  - **Blocks**: T4, T5
  - **Blocked By**: 无（可立即开始）

  **References**:
  - `喵学堂架构.txt` - 了解目录结构，确定需要访问的路径
  - MCP 协议文档: `https://modelcontextprotocol.io` - filesystem 和 command 工具配置格式
  - OpenCode 文档: 查看 MCP 配置的具体要求

  **Acceptance Criteria**:
  - [ ] 文件 `.opencode/mcp.json` 存在
  - [ ] JSON 格式有效（可通过解析器验证）
  - [ ] 包含 filesystem 工具配置，指向项目根目录
  - [ ] 包含 command 工具配置
  - [ ] 路径使用正斜杠（如 `E:/Meow_Academy`）

  **QA Scenarios**:

  ```
  Scenario: MCP 配置文件格式正确
    Tool: Bash
    Preconditions: 无
    Steps:
      1. 读取 .opencode/mcp.json 文件内容
      2. 使用 python -m json.tool 验证 JSON 格式
      3. 检查是否包含 "filesystem" 和 "command" 工具
    Expected Result: JSON 解析成功，包含所需工具配置
    Failure Indicators: JSON 解析错误、缺少必要字段
    Evidence: .sisyphus/evidence/task-1-config-validation.txt

  Scenario: 路径配置正确
    Tool: Bash
    Preconditions: MCP 配置文件已创建
    Steps:
      1. 检查 filesystem 工具中的目录路径
      2. 验证路径指向 E:/Meow_Academy
      3. 确认路径使用正斜杠
    Expected Result: 路径正确，使用正斜杠格式
    Failure Indicators: 路径错误、使用反斜杠
    Evidence: .sisyphus/evidence/task-1-path-check.txt
  ```

  **Evidence to Capture**:
  - [ ] task-1-config-validation.txt - JSON 验证输出
  - [ ] task-1-path-check.txt - 路径检查结果

  **Commit**: YES（与 T2、T3 一起提交）
  - Message: `chore(opencode): add MCP configuration for AI tool integration`
  - Files: `.opencode/mcp.json`

- [ ] 2. **创建项目上下文文件**

  **What to do**:
  - 在 `.opencode/` 目录下创建 `project-context.md`
  - 总结喵学堂的三层架构（知识层、智能体层、用户层）
  - 说明目录结构和文件组织方式
  - 列出关键文件和它们的作用
  - 提供架构图的文字描述
  - 说明项目的技术栈和依赖

  **Must NOT do**:
  - 不要复制整个架构文档（应精简总结）
  - 不要包含实现细节（保持高层描述）
  - 不要假设 AI 知道特定技术（提供足够上下文）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 文档编写任务，基于现有架构文档
  - **Skills**: []
    - 无需特殊技能

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1（与 T1、T3 并行）
  - **Blocks**: T6
  - **Blocked By**: 无（可立即开始）

  **References**:
  - `喵学堂架构.txt` - 完整的架构描述，用于提炼关键信息
  - 项目根目录结构 - 了解实际文件组织

  **Acceptance Criteria**:
  - [ ] 文件 `.opencode/project-context.md` 存在
  - [ ] 包含三层架构的说明
  - [ ] 包含目录结构说明
  - [ ] 包含关键文件列表
  - [ ] 内容简洁（不超过 2 页）

  **QA Scenarios**:

  ```
  Scenario: 项目上下文文件完整
    Tool: Bash
    Preconditions: 无
    Steps:
      1. 读取 .opencode/project-context.md
      2. 检查是否包含 "知识层"、"智能体层"、"用户层"
      3. 检查是否有目录结构说明
    Expected Result: 文件存在且包含所有必要章节
    Failure Indicators: 缺少章节、内容不完整
    Evidence: .sisyphus/evidence/task-2-context-check.txt

  Scenario: AI 能理解项目架构
    Tool: Bash
    Preconditions: project-context.md 已创建
    Steps:
      1. 读取上下文文件内容
      2. 验证内容是否足够让 AI 理解项目结构
      3. 检查是否提到关键概念（Agent、知识库、学习者画像等）
    Expected Result: 内容充分，AI 能基于此理解项目
    Failure Indicators: 过于简略、缺少关键概念
    Evidence: .sisyphus/evidence/task-2-ai-understanding.txt
  ```

  **Evidence to Capture**:
  - [ ] task-2-context-check.txt - 文件内容检查
  - [ ] task-2-ai-understanding.txt - AI 理解度评估

  **Commit**: YES（与 T1、T3 一起提交）
  - Message: `chore(opencode): add MCP configuration for AI tool integration`
  - Files: `.opencode/project-context.md`

- [ ] 3. **创建使用说明文档**

  **What to do**:
  - 在 `.opencode/` 目录下创建 `README.md`
  - 说明如何配置 OpenCode 使用 MCP
  - 提供使用示例（读取文件、执行命令）
  - 包含故障排除指南
  - 说明安全注意事项

  **Must NOT do**:
  - 不要假设用户已安装 OpenCode（提供安装链接）
  - 不要包含过时的信息（使用当前版本说明）
  - 不要忽略安全警告（明确说明权限风险）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 文档编写任务
  - **Skills**: []
    - 无需特殊技能

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1（与 T1、T2 并行）
  - **Blocks**: F3
  - **Blocked By**: 无（可立即开始）

  **References**:
  - OpenCode 官方文档 - MCP 配置说明
  - MCP 协议文档 - 工具使用示例

  **Acceptance Criteria**:
  - [ ] 文件 `.opencode/README.md` 存在
  - [ ] 包含配置步骤
  - [ ] 包含使用示例
  - [ ] 包含故障排除
  - [ ] 包含安全说明

  **QA Scenarios**:

  ```
  Scenario: 使用说明文档完整
    Tool: Bash
    Preconditions: 无
    Steps:
      1. 读取 .opencode/README.md
      2. 检查是否包含配置步骤
      3. 检查是否包含示例和故障排除
    Expected Result: 文档完整，用户能按步骤配置
    Failure Indicators: 缺少步骤、没有示例
    Evidence: .sisyphus/evidence/task-3-docs-check.txt
  ```

  **Evidence to Capture**:
  - [ ] task-3-docs-check.txt - 文档完整性检查

  **Commit**: YES（与 T1、T2 一起提交）
  - Message: `chore(opencode): add MCP configuration for AI tool integration`
  - Files: `.opencode/README.md`

- [ ] 4. **验证文件系统访问**

  **What to do**:
  - 使用 Bash 验证 MCP 配置中的目录路径可访问
  - 测试读取项目根目录下的文件
  - 测试读取子目录（知识层、智能体层、用户层）
  - 验证文件权限（读取、写入）

  **Must NOT do**:
  - 不要修改实际文件（仅读取测试）
  - 不要测试系统目录（仅项目目录）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 简单的验证任务
  - **Skills**: []
    - 无需特殊技能

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2（与 T5、T6 并行）
  - **Blocks**: F1, F2
  - **Blocked By**: T1（需要 MCP 配置）

  **References**:
  - `.opencode/mcp.json` - 检查配置的目录路径
  - `喵学堂架构.txt` - 了解应访问的目录

  **Acceptance Criteria**:
  - [ ] 能读取项目根目录文件列表
  - [ ] 能读取各层子目录
  - [ ] 路径配置正确

  **QA Scenarios**:

  ```
  Scenario: 目录可访问
    Tool: Bash
    Preconditions: MCP 配置已创建
    Steps:
      1. 列出项目根目录文件
      2. 列出知识层目录
      3. 列出智能体层目录
    Expected Result: 所有目录可正常列出
    Failure Indicators: 权限错误、路径不存在
    Evidence: .sisyphus/evidence/task-4-dir-access.txt
  ```

  **Evidence to Capture**:
  - [ ] task-4-dir-access.txt - 目录访问测试结果

  **Commit**: NO（验证任务，不修改代码）

- [ ] 5. **验证命令执行**

  **What to do**:
  - 测试执行简单的 shell 命令（如 `echo`、`ls`）
  - 测试执行项目相关命令（如 `python`、`node`）
  - 验证命令输出能正确返回

  **Must NOT do**:
  - 不要执行危险命令（rm、format 等）
  - 不要修改系统配置

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 简单的验证任务
  - **Skills**: []
    - 无需特殊技能

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2（与 T4、T6 并行）
  - **Blocks**: F1, F2
  - **Blocked By**: T1（需要 MCP 配置）

  **References**:
  - `.opencode/mcp.json` - 检查 command 工具配置

  **Acceptance Criteria**:
  - [ ] 能执行 echo 命令
  - [ ] 能执行 ls/dir 命令
  - [ ] 命令输出正确

  **QA Scenarios**:

  ```
  Scenario: 命令执行正常
    Tool: Bash
    Preconditions: MCP 配置已创建
    Steps:
      1. 执行 echo 测试命令
      2. 执行目录列出命令
      3. 检查输出是否正确
    Expected Result: 命令执行成功，输出正确
    Failure Indicators: 命令失败、无输出
    Evidence: .sisyphus/evidence/task-5-command-exec.txt
  ```

  **Evidence to Capture**:
  - [ ] task-5-command-exec.txt - 命令执行测试结果

  **Commit**: NO（验证任务，不修改代码）

- [ ] 6. **验证 AI 架构理解**

  **What to do**:
  - 验证项目上下文文件能被 AI 正确理解
  - 测试 AI 能否回答关于架构的问题
  - 检查 AI 能否定位关键文件

  **Must NOT do**:
  - 不要测试复杂的业务逻辑（仅验证理解能力）
  - 不要修改任何文件

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 验证任务
  - **Skills**: []
    - 无需特殊技能

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2（与 T4、T5 并行）
  - **Blocks**: F1, F3
  - **Blocked By**: T2（需要项目上下文）

  **References**:
  - `.opencode/project-context.md` - AI 的上下文来源
  - `喵学堂架构.txt` - 验证 AI 理解是否正确

  **Acceptance Criteria**:
  - [ ] AI 能描述三层架构
  - [ ] AI 能指出关键文件位置
  - [ ] AI 能理解项目目的

  **QA Scenarios**:

  ```
  Scenario: AI 理解项目架构
    Tool: Bash
    Preconditions: project-context.md 已创建
    Steps:
      1. 读取项目上下文文件
      2. 检查内容是否包含架构描述
      3. 验证关键概念是否清晰
    Expected Result: 内容足够 AI 理解项目
    Failure Indicators: 内容混乱、缺少关键信息
    Evidence: .sisyphus/evidence/task-6-ai-comprehension.txt
  ```

  **Evidence to Capture**:
  - [ ] task-6-ai-comprehension.txt - AI 理解度验证

  **Commit**: NO（验证任务，不修改代码）

---

## Final Verification Wave

> 3 个审查 Agent 并行运行。全部通过后才能完成。

- [ ] F1. **配置完整性检查** — `quick`
  检查所有配置文件是否完整：MCP 配置包含 filesystem 和 command 工具、项目上下文包含架构说明、使用说明包含示例。验证文件路径正确。
  输出: `Config [COMPLETE/INCOMPLETE] | Context [COMPLETE/INCOMPLETE] | Docs [COMPLETE/INCOMPLETE] | VERDICT`

- [ ] F2. **功能验证** — `quick`
  实际测试：用 Bash 验证 MCP 配置格式正确（JSON 有效）、验证项目上下文文件可被读取、模拟 AI 查询架构信息。
  输出: `MCP Config [VALID/INVALID] | Context [READABLE/ERROR] | Integration [PASS/FAIL] | VERDICT`

- [ ] F3. **文档审查** — `quick`
  检查文档质量：使用说明是否清晰、示例是否完整、是否包含故障排除。
  输出: `Clarity [GOOD/NEEDS_WORK] | Examples [COMPLETE/INCOMPLETE] | Troubleshooting [PRESENT/MISSING] | VERDICT`

---

## Commit Strategy

- **1**: `chore(opencode): add MCP configuration for AI tool integration`
  - 文件: `.opencode/mcp.json`, `.opencode/project-context.md`, `.opencode/README.md`

---

## Success Criteria

### 验证命令
```bash
# 验证 MCP 配置格式
cat .opencode/mcp.json | python -m json.tool

# 验证项目上下文存在
ls .opencode/project-context.md

# 验证目录结构
tree -L 2
```

### 最终检查清单
- [ ] MCP 配置文件包含 filesystem 和 command 工具
- [ ] 项目上下文文件描述了三层架构
- [ ] 使用说明包含配置步骤和示例
- [ ] 所有 JSON 格式正确
- [ ] 文件路径使用正斜杠（跨平台兼容）
