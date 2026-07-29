# TEMPLATE.md — product-x 自描述模板说明

本仓库（`Cloudbird-Software/product-x`）是一个 GitHub **template repository**。
用 `Use this template` 复制出一个新 `product-*` 仓库后，力工池（loop）即可自治运转。

本文件把仓库里的所有文件分成三层，说清哪些**复制后必须重写**、哪些**复制即用**、
哪些**根本不复制只引用**。最后一节给出从零拉起一个新 `product-*` 的 **复制 SOP**。

> 参考架构：ADR-002（waves/ 与 materializer 归 product-x；见 loop 仓 `DECISIONS.md`）。
> 共享本体（gates / lenses / prompts）始终只活在 `Cloudbird-Software/loop` 仓。

---

## 三层模型

| 层 | 复制策略 | 复制后要不要改 | 谁是真源 |
|---|---|---|---|
| ① 灵魂层 | 复制结构，重写内容 | **必须重写** | 各 product 仓自己 |
| ② 生成层 | 复制即用 | **不改**（仅 3 处产品名例外，见 SOP） | 本模板（product-x） |
| ③ 共享层 | 不复制，只引用 | **不复制** | loop 仓 |

### ① 灵魂层 —— 复制后必须重写

这一层是**产品自己的灵魂**：每个 `product-*` 的目标、契约、验收、波次都不一样。
模板只给目录占位和格式约定，复制后必须按新产品重写正文。

| 路径 | 说明 | 复制后动作 |
|---|---|---|
| `CHARTER.md` | 产品宪章正文（G0/G1/… 目标） | 新建并写本产品的目标映射 |
| `contracts/**` | 契约（API/数据/接口） | 新建，写本产品契约 |
| `tests/acceptance/**` | 验收测试（红→绿驱动） | 新建，写本产品验收 |
| `waves/**` | 波次声明（`WAVE-N.md`，含 ```json loop``` 卡） | **清空模板的 WAVE-1**，写本产品自己的波次 |
| `README.md` 产品正文 | 简介、目标、状态 | 改产品名与正文（见 SOP 3 文件） |

> `waves/WAVE-1.md` 是模板自举波（为 product-x 自己补骨架），**不是**新产品的波次。
> 复制后应删掉它，换成新产品的 `WAVE-1.md`。

> 灵魂层文件不受「生成层禁止手改」约束，新产品作者可自由编辑。
> 注意 `CODEOWNERS` 把 `CHARTER.md` / `contracts/**` / `tests/acceptance/**`
> 锁给了 `@randypanding`，相关 PR 需 code-owner 批（见生成层）。

### ② 生成层 —— 复制即用，本地禁止手改

这一层是**力工池运转的壳**：调用链、守护脚本、保护规则。复制过去就能跑，
正文一律不动。每个文件头部都带一行注释：

> `由模板生成，本地禁止手改。变更请改模板（product-x）并走 loop 流程。`

需要升级时，改**模板**（product-x）走 loop 流程合入，再由各 `product-*` 按模板同步；
**不要在 product-* 本地直接手改**，否则会和模板漂移、被 drift 检查（loop 仓
`conductor/drift_check.py`）告警。

| 路径 | 角色 | 备注 |
|---|---|---|
| `AGENTS.md` | 力工池自治说明（禁止人工 push main） | 复制即用 |
| `conductor/materialize.py` | `.loop` 脚本：把 `waves/**` 物化成 Card issue | 复制即用（产品名见 SOP） |
| `.github/workflows/materializer.yml` | `.github/gates` 调用壳：push waves/** 触发物化 | 复制即用（产品名见 SOP） |
| `.github/CODEOWNERS` | `.github/gates` 保护壳：锁灵魂层路径给 code-owner | 复制即用 |
| `.editorconfig` / `.gitignore` / `UPSTREAM.yaml` | 生成层配套配置 | 复制即用 |

> 「`.loop` 脚本」指 loop 守护体系在 product 仓本地落地的那一份可执行脚本
> （本模板即 `conductor/materialize.py`）。loop 守护本体（`loopd/`、`.loop/scripts/`）
> 属共享层，见下。
>
> 「`.github/gates` 调用壳」指 `.github/` 下调用 gate / 物化逻辑的 workflow 与保护文件。
> gate 本体（`gates/gate_*.py`）属共享层，见下。

### ③ 共享层 —— 在 loop 仓，只引用不复制

这一层是**所有 `product-*` 共用的本体**：gate、lens、prompt、守护进程。
它们只活在 `Cloudbird-Software/loop` 仓，product 仓**不复制**，运行时由 loop 守护
（`loopd`，按 `LOOP_BOOTSTRAP_REF` 拉）按需引用 / 拉取。

| 路径（loop 仓） | 说明 | product 仓怎么办 |
|---|---|---|
| `gates/gate_*.py` | gate 本体（paths/charter/diffsize/license/minage/testown/upstream/verdict） | 不复制；由 loop 守护在 verify 阶段引用 |
| `lenses/*.md` + `*.sh` | lens 本体（ci-security / contract-drift / …） | 不复制；审计工按需引用 |
| `prompts/P0.md` … `P10.md` | 角色提示词本体 | 不复制；沙盒 bootstrap 按 `LOOP_PROMPTS_SHA` pin 拉取 |
| `loopd/**`、`.loop/scripts/**` | loop 守护进程与脚本本体 | 不复制；沙盒 bootstrap 安装 |
| `conductor/drift_check.py` 等 | 跨仓 conductor（drift / scribe / tick / upgrade） | 不复制；loop 仓侧运行 |
| `settings/main-protection.json` | org ruleset 定义（main 保护 + merge queue） | 不复制；由 loop 仓 `policy.yml` 下发（见 SOP 第 5 步） |

> 判据：**改它会影响所有 `product-*`** → 它在共享层（loop 仓）。
> **改它只影响本产品灵魂** → 它在灵魂层（本仓，重写）。
> **它是壳、改它只是升级运转机制** → 它在生成层（本仓，禁手改，走模板）。

---

## 复制 SOP —— 拉起一个新 `product-*`

目标：从 `Use this template` 到「骨架可用、力工池可领卡」，控制在 15 分钟内。

### 第 0 步：用模板建仓

在 `Cloudbird-Software/product-x` 仓库页点 **Use this template → Create a new repository**，
新仓名按 `product-*` 模式取（如 `product-y`），归属 `Cloudbird-Software` org。
建好后新仓自带生成层全套壳 + 灵魂层目录占位。

### 第 1 步：改 3 个文件（产品名落地）

全仓只有 3 处硬编码了模板名 `product-x`，必须改成新产品名（`LOOP_ORG` 由
`github.repository_owner` 自动派生，不用改）：

| # | 文件 | 改什么 |
|---|---|---|
| 1 | `README.md` | 一级标题 `# product-x` → `# <新产品名>` |
| 2 | `.github/workflows/materializer.yml` | `LOOP_REPO: product-x` → `LOOP_REPO: <新产品名>` |
| 3 | `conductor/materialize.py` | 默认值 `E.get("LOOP_REPO","product-x")` → `"<新产品名>"`（本地/兜底用，CI 由上一步 env 覆盖） |

> 验证：`grep -rn "product-x" --exclude-dir=waves .` 在改完后应**无输出**
> （`waves/**` 是灵魂层，模板自举波应删/重写，不算残留）。

### 第 2 步：补 4 个自定义 label（模板不复制 label）

GitHub「Use this template」**不复制 label**。`materializer` 用 `--label card` 造卡，
缺 `card` label 会**静默失败**（卡过了校验、issue 却没建成，workflow 仍报绿）。
复制后立即补这 4 个自定义 label（颜色对齐 product-x；GitHub 默认 9 个 label 已自带）：

| label | color | 用途 |
|---|---|---|
| `card` | `1d76db` | materializer 物化的卡（**必需**，否则造卡失败） |
| `claimed` | `fbca04` | 卡被沙盒领取 |
| `done` | `0e8a16` | 卡完成 |
| `gripe` | `aaaaaa` | 吐槽箱 issue |

一键创建（`gh` 已登录即可，`<新产品名>` 替换为实际仓名）：

```bash
for l in "card 1d76db" "claimed fbca04" "done 0e8a16" "gripe aaaaaa"; do
  set -- $l
  gh api -X POST repos/Cloudbird-Software/<新产品名>/labels -f name="$1" -f color="$2" >/dev/null
done
```

> `materialize.py` 校验失败时还会 `--label incident` 开 Incident；`incident` label 不在
> product-x 默认集里，需要时一并建（`-f name=incident -f color=b60205`）。

### 第 3 步：清灵魂层占位

- 删 `waves/WAVE-1.md`（模板自举波，不是新产品的）。
- 按新产品写自己的 `CHARTER.md`、`contracts/**`、`tests/acceptance/**`、`waves/WAVE-1.md`。
- （可后补）先建一个最小 `WAVE-1.md` 让力工池能领卡即可。

### 第 4 步：发新 worker PAT

为新产品发一枚 **fine-grained PAT**（沙盒语境记 `GH_TOKEN`，探针语境记 `WK_PAT`，同一枚）：
- 作用域：仅本新 `product-*` 仓；
- 权限：`Contents` / `Issues` / `Pull requests` / `Metadata`（**read+write**）；
- **绝不给 `Workflows`**（避免沙盒改 workflow）。
- 命名建议：`LOOP_WK_<PRODUCT>`，灌进每个 impl/verify/audit 沙盒的 `GH_TOKEN`。

> 见 loop 仓 `Trae沙盒填写卡.md` ③ 敏感变量：每个沙盒的 `GH_TOKEN` 就是这枚 PAT。

### 第 5 步：org ruleset 自动护住（第 8 波后）

`main` 保护（deletion / non-fast-forward / merge queue / 线性历史 / 必审）由 loop 仓
`settings/main-protection.json` 定义，经 loop 仓 `policy.yml` 下发为 **org ruleset**。
第 8 波后该 ruleset 按 **`product-*` 名字模式**匹配，新建的 `product-*` 仓**自动**被护住，
无需逐仓配保护。第 8 波前，新产品可临时用 repo 级保护兜底。

> 第 8 波前：手动对新产品仓套 repo 级 `main-protection`（参考 loop 仓同名 json）。
> 第 8 波后：org ruleset 按模式自动覆盖，这一步消失。

### 退出标准（骨架可用）

- [ ] `grep -rn "product-x" --exclude-dir=waves .` 无输出；
- [ ] 4 个自定义 label（`card`/`claimed`/`done`/`gripe`）已建；
- [ ] `waves/WAVE-1.md` 是新产品自己的波次（含至少 1 张合法 ```json loop``` 卡）；
- [ ] 推一次 `waves/**` 变更到 `main` → `materializer` workflow 跑绿、物化出 Card issue；
- [ ] worker PAT 已发、沙盒 `loop next` 能领到卡。

走到这里，力工池即可在新 `product-*` 自治运转。灵魂层（CHARTER/contracts/acceptance/waves）
随后按波次逐步补齐即可。
