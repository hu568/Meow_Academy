# AGENTS.md — 喵学堂 (Meow Academy)

> 本仓库是一个**AI 驱动的个人学习系统**，不是传统软件项目。没有构建脚本、测试套件或 CI/CD。所有“代码”都是 Markdown 形式的知识资产和 Agent 角色定义。

---

## 仓库本质

- **项目类型**：知识库 + 多 Agent 协作系统（Markdown + SQLite 双存储驱动）
- **技术栈**：Node.js + SQLite（LibSQL），用于数据库操作和 Markdown 同步
- **外部依赖**：
  - `.opencode/package.json` 中的 `@opencode-ai/plugin`（OpenCode 工具集成）
  - `@libsql/client`（SQLite 数据库客户端）
- **入口点**：用户与 **西西喵斯**（主智能体）对话，由她调度子 Agent
- **数据存储**：SQLite 数据库（`喵学堂.db`）为数据源，Markdown 文件为只读视图

---

## 三层架构（目录即架构）

```
喵学堂/
├── 📥 1. 知识层/              ← 核心资产，按学科模板管理
│   └── 结构化知识库/
│       ├── _学科模板_/         ← 学科模板：格式化书页、知识点卡片、专业词典
│       └── {学科}/             ← 按模板实例化（如 英语/数学/物理）
│
├── 🧠 2. 智能体层/            ← 多 Agent 协作系统
│   └── .opencode/agents/       ← Agent 角色定义（YAML Frontmatter + Markdown）
│
├── 👤 3. 用户层/              ← 学习者画像、会话状态、学习档案
│   └── （当前以 Markdown 形式分散在各处，尚未集中）
│
└── 🗄️ 4. 数据层/              ← SQLite 数据库 + Markdown 双存储
    ├── 喵学堂.db               ← SQLite 数据源（AI 直接操作）
    ├── 索引/图书总录.md         ← Markdown 只读视图（人类可读）
    └── .opencode/tools/        ← 数据库工具和同步脚本
```

> 详细架构见 `喵学堂架构.txt`（72 行，中文）。

---

## Agent 体系（4 个角色）

所有 Agent 定义位于 `.opencode/agents/*.md`，采用 YAML Frontmatter + Markdown 正文格式：

| Agent | 文件 | 模式 | 职责 | 可调度子 Agent |
|-------|------|------|------|----------------|
| **西西喵斯** (Sisyphus) | `西西喵斯.md` | `primary` | 中央调度、意图识别、工作流编排 | 全部 |
| **帕秋莉** (Patchouli) | `帕秋莉.md` | `subagent` | 资料解析、知识归档、OCR/结构化 | — |
| **月咏小萌** (Komoe) | `月咏小萌.md` | `subagent` | 知识讲解、答疑解惑、教学引导 | — |
| **茅场晶彦** (Kayaba) | `茅场晶彦.md` | `subagent` | 出题、测试设计、错题分析 | — |

### 关键约定

- **西西喵斯是唯一入口**：任何学习需求都应先由她理解意图，再分派给子 Agent
- **子 Agent 不越权**：帕秋莉不教学、小萌不出题、晶彦不管理知识库
- **调度决策树**：资料整理→帕秋莉 / 知识讲解→小萌 / 练习测试→晶彦 / 多步骤→编排协作

---

## 知识库目录规范

### 学科模板 (`知识层/结构化知识库/_学科模板_/`)

每个学科必须包含：

```
{学科}/
├── 📄 格式化书页/
│   └── {书名}_{页码}.md          ← 保留完整章节结构的整书 Markdown
├── 🧩 知识点卡片/
│   └── {知识点ID}_{名称}.md       ← 原子化，可复用，Frontmatter 包含 ID、难度、前置知识
└── 📖 专业词典/
    └── {词条}.md                  ← 提取的专业术语
```

### 索引文件

- **`索引/图书总录.md`**：所有入库书籍的元数据总表（ID、书名、作者、学科、难度、ISBN、OCR 质量等）
- 新增书籍后必须更新此表

---

## 文件操作规范

- **所有内容均为 Markdown**：知识点、Agent 定义、配置文件全部是 `.md`
- **使用 YAML Frontmatter**：Agent 定义和知识点卡片需要标准化的 Frontmatter
- **中文为主**：界面、文档、知识内容均为中文；英语学科内容保留英文原文
- **路径使用正斜杠**：即使 Windows 环境，配置文件中也使用 `E:/Meow_Academy` 格式

---

## 开发工作流（针对本仓库的维护）

### 添加新 Agent

1. 在 `.opencode/agents/` 创建 `{角色名}.md`
2. 必须包含 YAML Frontmatter：`description`, `mode`（`primary` 或 `subagent`）, `tools`, `permission`
3. 更新 `西西喵斯.md` 的调度决策树和协作机制

### 添加新学科

1. 在 `知识层/结构化知识库/` 创建 `{学科}/` 目录
2. 按 `_学科模板_` 结构创建三个子目录
3. 通过 `SyncManager` 更新数据库，Markdown 会自动同步

### 导入新书

1. 由 **帕秋莉** 处理：解析 → 清洗 → 分类 → 原子化 → 归档
2. 产出物写入对应学科的 `格式化书页/`、`知识点卡片/`、`专业词典/`
3. 通过 `SyncManager` 更新数据库，Markdown 会自动同步

---

## OpenCode 配置

- **配置目录**：`.opencode/`
- **Agent 定义**：`.opencode/agents/*.md`
- **MCP 配置**：`.opencode/mcp.json`（如存在，定义 filesystem + command 工具权限）
- **项目上下文**：`.opencode/project-context.md`（如存在，供 AI 快速理解架构）
- **计划目录**：`.sisyphus/plans/` — 存放 OpenCode 集成相关的工作计划

---

## 记忆系统

- **全局记忆**：`persona`（猫娘角色设定）、`human`（用户偏好）、`project`（项目约定）
- **项目记忆**：通过 OpenCode 的 `memory_*` 工具读写
- **学习档案**：分散在 `用户层/`（规划中），当前以 Markdown 形式记录

---

## 数据存储规范（SQLite + Markdown 双写）

### 存储架构

- **SQLite 数据库（`喵学堂.db`）**：唯一数据源，AI 直接操作
  - 表结构：`subjects`（学科）、`materials`（资料）、`knowledge_cards`（知识点卡片）、`terms`（专业词典）、`archive_logs`（归档记录）
  - AI 通过 `SyncManager` 类进行增删改查
  - 支持复杂查询、统计、关联检索

- **Markdown 文件（`索引/图书总录.md`）**：只读视图，人类可读
  - 由数据库自动生成，**禁止手动编辑**
  - 每次数据库变更后自动同步更新
  - 保留原有表格格式，便于人类阅读

### 同步机制

```
AI/程序操作 → 写入 SQLite → 自动生成 Markdown
                    ↑
人类阅读 ←──── 查看 Markdown（只读）
```

### 使用方式

**AI 操作数据库**：
```javascript
const sync = new SyncManager('喵学堂.db');
await sync.addSubject('math', '数学', '高中数学');
await sync.addMaterial('math-001', 'math', '函数基础', '教材', '1.1', 5, 8);
await sync.syncMarkdown(); // 自动同步到 Markdown
```

**人类阅读**：
直接打开 `索引/图书总录.md` 查看，格式与原来一致。

## 常见陷阱

1. **不要尝试运行构建/测试命令**：本仓库没有 `package.json` 脚本、没有测试框架、没有 CI
2. **不要修改 `.opencode/.gitignore` 中的忽略规则**：它故意忽略 `node_modules` 和 lockfile，因为插件依赖由 OpenCode 管理
3. **不要跳过西西喵斯直接调用子 Agent**：会破坏工作流编排和上下文管理
4. **不要混淆 Agent 职责**：每个 Agent 的能力边界在各自的 `.md` 文件中有明确说明
5. **不要手动编辑 `索引/图书总录.md`**：此文件由数据库自动生成，手动编辑会被覆盖
6. **新增资料后更新数据库**：通过 `SyncManager` 操作数据库，Markdown 会自动同步

---

## 参考文件

| 文件 | 用途 |
|------|------|
| `喵学堂架构.txt` | 完整的三层架构说明（72 行） |
| `.opencode/agents/西西喵斯.md` | 主智能体定义，含调度决策树 |
| `索引/图书总录.md` | 书籍元数据总表 |
| `.sisyphus/plans/opencode-integration.md` | OpenCode 接入计划（详细工作计划模板） |
