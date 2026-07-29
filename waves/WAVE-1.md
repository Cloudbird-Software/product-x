# WAVE-1：项目骨架补齐

> spec-kit spec+plan+tasks 融合格式（见 OPC-v4 第 2.1 节）。
> 目标：为 product-x 补齐 5 个项目骨架文件，让仓库达到可被力工池正常工作的最小完备态。
> 全部 tier=trivial；charter 占位映射 `["G0"]`（CHARTER 未立前，见 DECISIONS.md ADR-002）。

---

## Spec（规格）

product-x 当前只有 `.github/CODEOWNERS`、`UPSTREAM.yaml`、`canary/` 三个顶层项，缺 5 个项目骨架文件。本波各补一个，互不交叉：

| 卡 ID | 补什么 | paths | 备注 |
|---|---|---|---|
| w1-license | LICENSE | `["LICENSE"]` | MIT |
| w1-gitignore | .gitignore | `[".gitignore"]` | Python/Node/IDE 通用 |
| w1-readme-badge | README 徽章 | `["README.md"]` | 含 CI/license 等徽章 |
| w1-editorconfig | .editorconfig | `[".editorconfig"]` | 跨编辑器风格 |
| w1-agents | AGENTS.md | `["AGENTS.md"]` | ⚠ CODEOWNERS 锁 @randypanding，PR 需 code-owner 批 |

paths 两两不交叉（5 个不同文件，无 glob 重叠）。

---

## Plan（计划）

- 触发：本 PR 合入 product-x main → materializer workflow（`.github/workflows/materializer.yml`，paths `waves/**`）物化出 5 张 Card issue（label `card`，含 ` ```json loop ` block）。
- 力工池（impl-1 起）按 P0 自主领卡：`loop next` → save → verify → done → merge queue。
- AGENTS.md 卡（w1-agents）因 CODEOWNERS 锁定，PR 会触发 code-owner review；**人（@randypanding）需手动批准该卡 PR**。其余 4 张无此限制，可自动合。
- 验收（W1 退出标准第一条）：连续 5 张 trivial 卡合入 main，`confirm_taps=0`。

---

## Tasks（5 张卡）

### Card w1-license

```json loop
{
  "id": "w1-license",
  "state": "ready",
  "tier": "trivial",
  "role": "impl",
  "paths": ["LICENSE"],
  "forbid_paths": [".github/**", "settings/**", "**/*.lock"],
  "charter": ["G0"],
  "attempt": 0,
  "acceptance": [
    "LICENSE 文件存在",
    "许可证类型为 MIT（首行含 'MIT License'）",
    "版权行含年份与 Cloudbird-Software"
  ]
}
```

**Charter:** G0（占位，见 DECISIONS.md ADR-002）
**Tier:** trivial
**Paths:** LICENSE

#### Acceptance Criteria
1. `LICENSE` 文件存在
2. 许可证类型为 MIT（首行含 `MIT License`）
3. 版权行含年份与 `Cloudbird-Software`

#### 任务
创建 `LICENSE`，MIT 许可证，版权 `Copyright (c) 2026 Cloudbird-Software`。完成后走 P0 的 `loop verify` → `loop done`。

---

### Card w1-gitignore

```json loop
{
  "id": "w1-gitignore",
  "state": "ready",
  "tier": "trivial",
  "role": "impl",
  "paths": [".gitignore"],
  "forbid_paths": [".github/**", "settings/**", "**/*.lock"],
  "charter": ["G0"],
  "attempt": 0,
  "acceptance": [
    ".gitignore 文件存在",
    "至少含 Python (__pycache__/, *.pyc)、Node (node_modules/)、IDE (.vscode/, .idea/) 三类条目"
  ]
}
```

**Charter:** G0（占位）
**Tier:** trivial
**Paths:** .gitignore

#### Acceptance Criteria
1. `.gitignore` 文件存在
2. 至少含 Python（`__pycache__/`、`*.pyc`）、Node（`node_modules/`）、IDE（`.vscode/`、`.idea/`）三类条目

#### 任务
创建 `.gitignore`，覆盖 Python / Node / IDE / OS（`.DS_Store`）通用忽略项。完成后走 P0 的 `loop verify` → `loop done`。

---

### Card w1-readme-badge

```json loop
{
  "id": "w1-readme-badge",
  "state": "ready",
  "tier": "trivial",
  "role": "impl",
  "paths": ["README.md"],
  "forbid_paths": [".github/**", "settings/**", "**/*.lock"],
  "charter": ["G0"],
  "attempt": 0,
  "acceptance": [
    "README.md 文件存在",
    "含项目名 product-x 的一级标题",
    "含至少一个 Markdown 徽章（img.shields.io 或类似）"
  ]
}
```

**Charter:** G0（占位）
**Tier:** trivial
**Paths:** README.md

#### Acceptance Criteria
1. `README.md` 文件存在
2. 含项目名 `product-x` 的一级标题（`# product-x`）
3. 含至少一个 Markdown 徽章（`img.shields.io` 或类似）

#### 任务
创建 `README.md`：一级标题 `# product-x`，一段简介，再加 license / CI 状态徽章行。完成后走 P0 的 `loop verify` → `loop done`。

---

### Card w1-editorconfig

```json loop
{
  "id": "w1-editorconfig",
  "state": "ready",
  "tier": "trivial",
  "role": "impl",
  "paths": [".editorconfig"],
  "forbid_paths": [".github/**", "settings/**", "**/*.lock"],
  "charter": ["G0"],
  "attempt": 0,
  "acceptance": [
    ".editorconfig 文件存在",
    "首行为 root = true",
    "含 [*] 段且设了 indent_style 与 indent_size"
  ]
}
```

**Charter:** G0（占位）
**Tier:** trivial
**Paths:** .editorconfig

#### Acceptance Criteria
1. `.editorconfig` 文件存在
2. 首行为 `root = true`
3. 含 `[*]` 段且设了 `indent_style` 与 `indent_size`

#### 任务
创建 `.editorconfig`：`root = true`，`[*]` 段设 `indent_style = space`、`indent_size = 2`、`end_of_line = lf`、`charset = utf-8`；可加 `[*.{py,java}]` 段设 `indent_size = 4`。完成后走 P0 的 `loop verify` → `loop done`。

---

### Card w1-agents

```json loop
{
  "id": "w1-agents",
  "state": "ready",
  "tier": "trivial",
  "role": "impl",
  "paths": ["AGENTS.md"],
  "forbid_paths": [".github/**", "settings/**", "**/*.lock"],
  "charter": ["G0"],
  "attempt": 0,
  "acceptance": [
    "AGENTS.md 文件存在",
    "含一段说明本仓库由 loop 力工池自治维护",
    "含禁止人工直接 push main 的说明"
  ]
}
```

**Charter:** G0（占位）
**Tier:** trivial
**Paths:** AGENTS.md

> ⚠ **本卡受 CODEOWNERS 锁定**（`/AGENTS.md` → @randypanding）。生成的 PR 会触发 code-owner review，需 @randypanding 手动批准才能合入。其余 4 张卡无此限制。

#### Acceptance Criteria
1. `AGENTS.md` 文件存在
2. 含一段说明本仓库由 loop 力工池自治维护
3. 含禁止人工直接 push main 的说明

#### 任务
创建 `AGENTS.md`：说明本仓库由 loop 力工池（impl/verify/audit 沙盒）按 Card 自治维护，所有变更经 PR + merge queue；人工不得直接 push main（ruleset 强制）。完成后走 P0 的 `loop verify` → `loop done`（PR 合并需等 code owner 批）。
