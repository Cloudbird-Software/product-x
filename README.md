# product-x

![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-template-green)

**product-x 是 LOOP 体系的参考实现样板仓库。**
真实产品由本仓库「Use this template」生成；生成后请替换 CHARTER.md 的 G/Q/U 段，并保留 N 段全部红线。

## 仓库结构（产品仓应该长什么样）

```
.
├── CHARTER.md                  # 人类唯一可编辑真源（AI 代拟，人类审定）
├── LOOP.yml                    # 钉住 loop 控制面的 tag + 40 位 SHA
├── UPSTREAM.yaml               # 外部依赖登记（含 loop 自身作为控制面）
├── AGENTS.md                   # AI 工作单元快速入口与红线
├── README.md                   # 本文件
├── LICENSE
├── .editorconfig
├── .gitignore
├── .github/
│   ├── CODEOWNERS              # 关键文件的人类审批面
│   └── workflows/
│       ├── loop-ci.yml         # CI 薄壳 → loop reusable-product-ci.yml
│       ├── loop-gates.yml      # 门禁薄壳 → loop reusable-gates.yml
│       └── loop-review.yml     # 强模型验收薄壳 → loop reusable-review.yml
├── scripts/
│   ├── purge-mechanism-copies.sh   # 清理 loop 机制副本工具
│   └── r13-4-pr-description.md     # R13-4 PR 描述模板
├── src/                        # 产品自己的源码
├── tests/                      # 产品自己的测试
├── contracts/                  # 产品契约（示例）
└── migrations/                 # 产品迁移脚本（示例）
```

**不留**：gates / lenses / conductor / loopd / prompts / settings 的任何 loop 机制副本。
这些全部由 loop 侧 reusable workflow 提供（CHARTER N9）。

## CI

- `loop-ci`：lint / test / build（由 loop `reusable-product-ci.yml` 实现）
- `loop-gates`：全部门禁（由 loop `reusable-gates.yml` 实现，profile=strict）
- `loop-review`：强模型验收（由 loop `reusable-review.yml` 实现，非阻塞）

## 升级 loop pin

loop 发新 tag 后，第 8 环会在冷静期届满时自动开 bump PR：
同步更新 `LOOP.yml.loop.sha`、`UPSTREAM.yaml` 与全部薄壳 workflow 的 `@<sha>`。
该 PR 走与普通 PR 完全相同的门禁，无任何豁免。
