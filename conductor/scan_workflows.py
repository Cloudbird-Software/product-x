#!/usr/bin/env python3
"""conductor/scan_workflows.py — Extract pr-ci.yml's scanners as callable functions.

Per R10-1 acceptance #3: the negative tests MUST call the scan logic body,
not a copy-pasted parallel implementation. This module hosts exactly that body.

Two scanners are exposed:
  scan_fake_green(root, file_pattern='.github/workflows/*.yml') → int exit
  scan_actions_pinned(root, file_pattern='.github/workflows/*.yml') → int exit

Each returns 0 on clean, non-zero on violations, and prints diagnostic lines.

They are intentionally 1:1 with the Python heredoc blocks in pr-ci.yml's
`no-fake-green` and `actions-pinned` jobs.
"""
from __future__ import annotations

import glob as _glob
import pathlib
import re
import sys
from typing import Sequence


# ======================================================================
# no-fake-green scanner (matches pr-ci.yml no-fake-green job)
# ======================================================================

_ALLOW_MARK = "fake-green-ok:"
_FAKE_GREEN_PATTERNS: list[tuple[str, str]] = [
    (r"\|\|\s*true\b", "`|| true` 吞掉失败"),
    (r"^\s*set\s+\+e\b", "`set +e` 关闭错误传播"),
    (r"continue-on-error:\s*true", "continue-on-error"),
]


def scan_fake_green(root: str | pathlib.Path = ".",
                    file_pattern: str = ".github/workflows/*.yml",
                    out=sys.stdout) -> int:
    """Scan workflow YAML for swallowed-error patterns.

    Returns 0 if clean, 1 if any violations found.
    """
    root = pathlib.Path(root)
    violations: list[str] = []
    files = sorted(_glob.glob(str(root / file_pattern)))
    for f in files:
        try:
            lines = pathlib.Path(f).read_text(encoding="utf-8").splitlines()
        except OSError as e:
            print(f"ERROR cannot read {f}: {e}", file=out)
            return 2
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            ctx = line + (lines[i - 1] if i else "")
            if _ALLOW_MARK in ctx:
                continue
            for pat, desc in _FAKE_GREEN_PATTERNS:
                if re.search(pat, line):
                    violations.append(f"{f}:{i+1}: {desc} → {stripped}")
    if violations:
        print("检出假绿模式（CHARTER N5 禁止）。若确有正当理由，"
              "在该行或上一行加注释 `fake-green-ok: <理由>`：", file=out)
        for v in violations:
            print("  ✗", v, file=out)
        return 1
    print("no-fake-green OK", file=out)
    return 0


# ======================================================================
# actions-pinned scanner (matches pr-ci.yml actions-pinned job)
# ======================================================================

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def scan_actions_pinned(root: str | pathlib.Path = ".",
                        file_pattern: str = ".github/workflows/*.yml",
                        out=sys.stdout) -> int:
    """Scan workflow YAML for uses: refs that are NOT pinned to 40-hex SHA.

    Returns 0 if clean, 1 if any violations found.
    """
    root = pathlib.Path(root)
    bad: list[str] = []
    files = sorted(_glob.glob(str(root / file_pattern)))
    for f in files:
        try:
            lines = pathlib.Path(f).read_text(encoding="utf-8").splitlines()
        except OSError as e:
            print(f"ERROR cannot read {f}: {e}", file=out)
            return 2
        for i, line in enumerate(lines):
            s = line.strip()
            if not (s.startswith("uses:") or s.startswith("- uses:")):
                continue
            ref = s.split("uses:", 1)[1].strip().strip("'\"").split()[0]
            if ref.startswith("./") or ref.startswith("docker://"):
                continue
            if "@" not in ref:
                bad.append(f"{f}:{i+1}: 无 ref → {ref}")
                continue
            sha = ref.rsplit("@", 1)[1]
            if not _SHA_RE.fullmatch(sha):
                bad.append(f"{f}:{i+1}: 未钉 SHA → {ref}")
    if bad:
        for b in bad:
            print("  ✗", b, file=out)
        return 1
    print("actions-pinned OK", file=out)
    return 0


# ======================================================================
# CLI entry
# ======================================================================

def main_pr_ci(root: str | pathlib.Path = ".") -> int:
    """Entry point for loop's pr-ci.yml: runs both scanners, returns combined exit code.

    0 if both clean, else 1 (any violation) or 2 (cli error).
    Prints diagnostics to stdout for each scanner separately.
    """
    e1 = scan_fake_green(root)
    e2 = scan_actions_pinned(root)
    if e1 == 2 or e2 == 2:
        return 2
    return 0 if (e1 == 0 and e2 == 0) else 1


def main_products_ci(root: str | pathlib.Path = ".") -> int:
    """Entry point for product-x ci.yml gates.profile=productx_ci post-step.

    Runs the no-fake-green and actions-pinned scanners against the local
    .github/workflows/*.yml as part of N-12 CI traceability. Returns 0 on
    clean, 1 on any violation, 2 on cli error.
    """
    print("=== scan_workflows.main_products_ci (gates.profile=productx_ci) ===")
    print("Running no-fake-green...")
    e1 = scan_fake_green(root)
    print("Running actions-pinned...")
    e2 = scan_actions_pinned(root)
    if e1 == 0 and e2 == 0:
        print("Both scanners clean: no fake-green swallowing, all uses are SHA-pinned.")
        return 0
    if e1 == 2 or e2 == 2:
        return 2
    return 1


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])
    if not argv:
        print("usage: scan_workflows.py [fake-green|actions-pinned|all] [root_dir]", file=sys.stderr)
        return 2
    cmd = argv[0]
    root = argv[1] if len(argv) > 1 else "."
    if cmd == "fake-green":
        return scan_fake_green(root)
    if cmd == "actions-pinned":
        return scan_actions_pinned(root)
    if cmd == "all":
        return main_pr_ci(root)
    print(f"unknown scanner: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
