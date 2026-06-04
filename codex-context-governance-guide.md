# Codex Context Ops 使用指南

这份文档说明如何使用 `codex-context-ops` 插件，在不同项目中建立 Codex 上下文治理、Bug 记忆、技能路由、并行分析和隔离实现流程。

核心目标：

- 减少上下文污染和上下文压缩后的信息丢失
- 避免重复 Bug 反复出现
- 降低大项目中的无效 Token 消耗
- 让结构问题优先走 CodeGraph，而不是全量读文件
- 把长期规则、Bug 记录和架构事实沉淀到项目文件中

---

## 1. 插件安装

推荐使用 GitHub 远程 marketplace 安装，这样不依赖本地目录，换项目时也更稳定。

```powershell
codex plugin marketplace add ac674-life/codex-context-ops
codex plugin add codex-context-ops@context-tools
```

安装后重启 Codex app，或至少在目标项目中新开一个线程。

验证：

```powershell
codex plugin list
```

应该看到：

```text
codex-context-ops@context-tools  installed, enabled
```

如果 WindowsApps 里的 `codex.exe` 权限异常，可以使用 Codex app 实际配置里的 CLI 路径，例如：

```powershell
C:\Users\admin\AppData\Local\OpenAI\Codex\bin\<版本>\codex.exe plugin list
```

---

## 2. 为什么有的项目可用，有的项目不可用

同一个账号下，如果有的项目找不到插件，通常不是账号问题，而是以下原因。

### 2.1 旧线程没有加载新插件

插件是在新线程启动时加载的。安装插件前已经打开的线程，可能看不到新技能。

解决：

```text
重启 Codex app，并在目标项目中新开线程。
```

### 2.2 项目还没有初始化

插件是全局安装的，但每个项目自己的治理文件需要单独初始化。

第一次进入某个项目时使用：

```text
使用 $codex-context-ops:context-init，以简体中文初始化这个项目。
```

初始化后会生成：

```text
AGENTS.md
docs/bugs.md
docs/architecture.md
.agents/skills/context-governance
.agents/skills/context-safe-bugfix
.agents/skills/context-safe-review
.agents/skills/context-safe-refactor
.agents/skills/context-subagents
.agents/skills/context-worktree
.agents/skills/context-release-check
.agents/skills/context-bug-memory
```

### 2.3 技能名冲突或没有被自动联想

推荐使用完整命名：

```text
$codex-context-ops:context-init
$codex-context-ops:context-safe-bugfix
$codex-context-ops:context-safe-review
```

如果短名可用，也可以写：

```text
$context-init
$context-safe-bugfix
```

### 2.4 项目没有刷新或没有信任

如果目标项目是新目录，请确认 Codex app 中该项目已被信任，并新开线程。

---

## 3. 中英文初始化

中文初始化：

```text
使用 $codex-context-ops:context-init，以简体中文初始化这个项目。
```

英文初始化：

```text
Use $codex-context-ops:context-init to initialize this project in English.
```

脚本层面支持：

```powershell
python scripts/init_context_ops.py --target . --lang zh-CN
python scripts/init_context_ops.py --target . --lang en
python scripts/init_context_ops.py --target . --lang auto
```

除非明确要求 `--force`，否则不会覆盖已有文件。

---

## 4. 项目一开始应该有什么

每个项目建议至少有：

```text
AGENTS.md
docs/bugs.md
docs/architecture.md
.agents/skills/context-governance
.agents/skills/context-safe-bugfix
```

完整初始化会额外加入：

```text
.agents/skills/context-safe-review
.agents/skills/context-safe-refactor
.agents/skills/context-subagents
.agents/skills/context-worktree
.agents/skills/context-release-check
.agents/skills/context-bug-memory
```

这些文件的分工：

| 文件或技能 | 作用 |
|---|---|
| `AGENTS.md` | 项目级持久规则，Codex 每次进入项目都应读取 |
| `docs/bugs.md` | 重复、隐蔽、高风险 Bug 的长期记忆 |
| `docs/architecture.md` | 架构边界、重要决策、高风险区域 |
| `$context-governance` | 非简单任务的默认路由和上下文治理 |
| `$context-safe-bugfix` | 修 Bug、测试失败、回归问题 |
| `$context-safe-review` | Review、PR 风险分析、测试缺口分析 |
| `$context-safe-refactor` | 重构、迁移、大范围结构调整 |
| `$context-subagents` | 多模块复杂问题的并行隔离分析 |
| `$context-worktree` | 隔离实现、实验性修复 |
| `$context-release-check` | 发布前或合并前检查 |
| `$context-bug-memory` | 更新历史 Bug 记录 |

---

## 5. 默认常驻 vs 主动调用

### 默认常驻

这些应该在项目初始化后长期存在：

- `AGENTS.md`
- `docs/bugs.md`
- `docs/architecture.md`
- `$context-governance`
- CodeGraph 使用规则
- 完成前验证规则

### 需要主动调用

这些不建议每次自动启用，因为会增加成本或协调复杂度：

- `$context-safe-bugfix`
- `$context-safe-review`
- `$context-safe-refactor`
- `$context-subagents`
- `$context-worktree`
- `$context-release-check`
- `$context-bug-memory`

---

## 6. 技能使用速查

| 场景 | 推荐调用 |
|---|---|
| 不确定任务类型 | `$codex-context-ops:context-governance` |
| 初始化项目 | `$codex-context-ops:context-init` |
| 修 Bug | `$codex-context-ops:context-safe-bugfix` |
| 测试失败 | `$codex-context-ops:context-safe-bugfix` |
| 重复 Bug | `$codex-context-ops:context-safe-bugfix` + `$codex-context-ops:context-bug-memory` |
| 代码审查 | `$codex-context-ops:context-safe-review` |
| PR 风险分析 | `$codex-context-ops:context-safe-review` |
| 重构 | `$codex-context-ops:context-safe-refactor` |
| 迁移 | `$codex-context-ops:context-safe-refactor` |
| 多模块复杂问题 | `$codex-context-ops:context-subagents` |
| 隔离实现 | `$codex-context-ops:context-worktree` |
| 发布前检查 | `$codex-context-ops:context-release-check` |
| 更新 Bug 记录 | `$codex-context-ops:context-bug-memory` |

---

## 7. 常用提示词

### 7.1 初始化新项目

```text
使用 $codex-context-ops:context-init，以简体中文初始化这个项目。

要求：
1. 创建或更新 AGENTS.md。
2. 创建 docs/bugs.md 和 docs/architecture.md。
3. 创建上下文治理相关 .agents/skills。
4. 不修改业务代码。
5. 已有文件不要覆盖，除非我明确要求 force。
```

### 7.2 修 Bug

```text
使用 $codex-context-ops:context-safe-bugfix 修复这个 Bug：

[描述 Bug、错误日志或复现步骤]

要求：
1. 先复现或定位失败测试。
2. 用 CodeGraph 分析相关调用链。
3. 只读取相关文件。
4. 做最小修复。
5. 添加或更新回归测试。
6. 如果是重复或隐蔽问题，更新 docs/bugs.md。
7. 完成前运行相关测试并报告结果。
```

### 7.3 测试失败

```text
使用 $codex-context-ops:context-safe-bugfix 调查这个测试失败。

先解释失败现象和可能根因，不要直接改代码。
然后定位最小相关路径，修复后优先跑相关测试。
```

### 7.4 重复 Bug 记录

```text
使用 $codex-context-ops:context-bug-memory 更新 docs/bugs.md。

请记录：
- 现象
- 根因
- 影响文件
- 回归测试
- 修复状态
- 后续风险
```

### 7.5 代码 Review

```text
使用 $codex-context-ops:context-safe-review review 当前改动。

重点检查：
1. 正确性问题
2. 回归风险
3. 安全风险
4. 数据丢失风险
5. 测试缺口
6. 是否违反 AGENTS.md 项目规则

请按严重程度排序输出，并给出文件路径和证据。
```

### 7.6 大范围重构

```text
使用 $codex-context-ops:context-safe-refactor 准备这个重构。

先不要改代码。
请先：
1. 用 CodeGraph 分析相关模块、调用方和被调用方。
2. 列出影响范围。
3. 给出分阶段迁移计划。
4. 标出兼容性风险和测试策略。

等我确认计划后再开始实现。
```

### 7.7 多模块复杂问题

```text
使用 $codex-context-ops:context-subagents 隔离分析这个复杂问题。

请拆成三个方向：
1. 调用链和架构边界，优先使用 CodeGraph。
2. 测试、复现路径和历史 Bug。
3. 实现风险和兼容性风险。

每个方向只返回摘要、证据、文件路径和风险，不要返回长日志。
```

### 7.8 隔离实现

```text
使用 $codex-context-ops:context-worktree 在隔离环境实现这个修复。

完成后请给我：
1. 改动摘要
2. 关键 diff
3. 测试结果
4. 风险和回滚建议
```

### 7.9 发布前检查

```text
使用 $codex-context-ops:context-release-check 做发布前检查。

要求：
1. 检查当前改动风险。
2. 检查 docs/bugs.md 是否有未关闭高风险问题。
3. 运行完整测试或说明无法运行原因。
4. 输出发布阻塞项和非阻塞风险。
```

---

## 8. CodeGraph 使用规则

结构问题优先用 CodeGraph：

| 问题 | 推荐工具 |
|---|---|
| X 在哪里定义 | `codegraph_search` |
| 谁调用了 Y | `codegraph_callers` |
| Y 调用了什么 | `codegraph_callees` |
| 改 Z 会影响什么 | `codegraph_impact` |
| 解释系统/调用链 | `codegraph_explore` |
| 查看签名/源码 | `codegraph_node` |

只有这些情况优先用文本搜索：

- 日志片段
- 错误字符串
- 注释文本
- 精确字面量

---

## 9. 本地迁移与记忆

本项目自己的迁移记忆保存在：

```text
.local-migration/
```

该目录已加入 `.gitignore`，不会上传 GitHub。

包含：

- `MEMORY.md`：项目记忆、设计决策、部署状态
- `MIGRATION.md`：迁移说明
- `INDEX.md`：人类可读索引
- `file-index.json`：文件、大小和 SHA-256
- `snapshot/`：生成物快照

迁移前刷新快照：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-local-migration.ps1
```

恢复快照：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\restore-local-migration.ps1 -Destination "新的目录"
```

---

## 10. 故障排查

### 10.1 插件列表找不到

先运行：

```powershell
codex plugin list
```

确认是否存在：

```text
codex-context-ops@context-tools  installed, enabled
```

如果没有，重新安装：

```powershell
codex plugin marketplace add ac674-life/codex-context-ops
codex plugin add codex-context-ops@context-tools
```

### 10.2 CLI 权限异常

如果 `codex.exe` 来自 WindowsApps 且提示 `Access is denied`，使用 Codex 配置中的真实 CLI 路径：

```powershell
C:\Users\admin\AppData\Local\OpenAI\Codex\bin\<版本>\codex.exe plugin list
```

### 10.3 某个项目不能用

按顺序检查：

1. 是否安装并启用了插件。
2. 是否重启 Codex app。
3. 是否在目标项目新开线程。
4. 是否使用完整技能名 `$codex-context-ops:context-init`。
5. 该项目是否已执行过 `$context-init`。
6. 该项目是否 trusted。

### 10.4 更新插件后不生效

执行：

```powershell
codex plugin marketplace upgrade context-tools
codex plugin add codex-context-ops@context-tools
```

然后重启 Codex 或新开线程。

---

## 11. 一句话记忆

全局安装插件，项目内执行 `$context-init`。

小任务走 `$context-governance`，Bug 用 `$context-safe-bugfix`，Review 用 `$context-safe-review`，重构用 `$context-safe-refactor`，复杂问题用 `$context-subagents`，隔离实现用 `$context-worktree`，发布前检查用 `$context-release-check`，重复 Bug 记忆用 `$context-bug-memory`。

## 12. 功能索引与模块地图自动维护

当项目变大后，单靠 `docs/architecture.md` 和 `docs/bugs.md` 还不够。你需要一张“功能索引 / 模块地图”，让新的 Codex 线程可以先定位功能，再定点读取代码。

初始化后应包含：

```text
docs/feature-index.md
docs/modules/README.md
.agents/skills/context-feature-index
```

推荐首次建立索引时这样说：

```text
使用 $codex-context-ops:context-feature-index 为这个项目建立功能索引。
请按照用户可见功能或领域模块拆分，不要只按文件夹机械拆分。
为每个主要模块创建 docs/modules/<module>.md。
建立索引时不要修改业务代码。
```

后续更新项目时，Codex 应自动维护索引：

- 如果修改了用户可见行为，更新对应模块文档。
- 如果新增或移动入口点，更新 `docs/feature-index.md` 和相关模块文档。
- 如果依赖关系、数据流或测试位置变化，更新对应模块文档。
- 如果引入或修复重复 Bug，同步 `docs/bugs.md` 与相关模块文档。
- 完成回复中说明“功能索引是否已更新”，如果没有更新，需要说明原因。

使用方式：

| 场景 | 推荐指令 |
|---|---|
| 首次建立功能地图 | `$codex-context-ops:context-feature-index` |
| 怀疑索引过期 | `$codex-context-ops:context-feature-index` |
| 新线程快速定位功能 | 先让 Codex 读取 `docs/feature-index.md` |
| 普通 Bugfix / Refactor | 使用对应技能，完成后让 Codex 同步更新索引 |

一句话：`context-init` 负责创建索引框架，`context-feature-index` 负责主动建立或审计索引，其他安全工作流负责在日常改代码时顺手维护索引。
