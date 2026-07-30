#!/usr/bin/env python3
"""paths-lease gate — PR diff files must be within card.paths (and not in forbid_paths).

Behavior:
  - non-pull_request event (push/merge_group): SKIP exit 0 (no PR to check)
  - bare PR (no 'Card: #N' in body): SKIP exit 0 (lease waived)
  - card has empty paths: SKIP exit 0
  - any diff file not covered by card.paths (or in forbid_paths): FAIL exit 1
  - all diff files within card.paths: OK exit 0

Ported from loop repo gates/gate_paths.py with bare-PR crash fixed
(original did m.group(1) on None -> AttributeError for bare PR).
"""
import json, subprocess, sys, os, re, fnmatch


def gh_json(*a):
    env = dict(os.environ)
    p = subprocess.run(["gh", *a], capture_output=True, text=True, env=env)
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return None


# 1. determine PR number (PR_NUMBER injected by ci.yml from github.event.pull_request.number;
#    fallback to GITHUB_REF for local/non-workflow runs)
pr = os.environ.get("PR_NUMBER") or None
if not pr:
    ref = os.environ.get("GITHUB_REF", "")
    parts = ref.split("/")
    if len(parts) >= 3 and parts[1] == "pull":
        pr = parts[2]
if not pr:
    print("SKIP: non-pull_request event (no PR number) - lease check waived")
    sys.exit(0)

# 2. fetch PR body, find Card: #N
pr_data = gh_json("pr", "view", pr, "--json", "body")
if not pr_data:
    print(f"SKIP: cannot fetch PR #{pr} - lease check waived")
    sys.exit(0)
body = pr_data.get("body", "") or ""
m = re.search(r"Card:\s*#(\d+)", body)
if not m:
    print("SKIP: no 'Card: #N' in PR body - bare PR, lease waived")
    sys.exit(0)
card_num = m.group(1)

# 3. fetch card issue, parse ```json loop block
issue = gh_json("issue", "view", card_num, "--json", "body")
if not issue:
    print(f"FAIL: cannot fetch card issue #{card_num}")
    sys.exit(1)
ibody = issue.get("body", "") or ""
marker = "```json loop"
if marker not in ibody:
    print(f"FAIL: card #{card_num} has no ```json loop block")
    sys.exit(1)
seg = ibody.split(marker, 1)[1].split("```", 1)[0]
try:
    card = json.loads(seg)
except Exception as e:
    print(f"FAIL: card #{card_num} json parse error: {e}")
    sys.exit(1)

# 4. diff files vs card.paths
base = subprocess.run(["git", "merge-base", "origin/main", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
if not base:
    print("SKIP: cannot determine merge-base - lease check waived")
    sys.exit(0)
files = [f for f in subprocess.run(["git", "diff", "--name-only", base, "HEAD"],
                                   capture_output=True, text=True).stdout.split() if f]

card_paths = card.get("paths", []) or []
forbid = card.get("forbid_paths", []) or []

if not card_paths:
    print(f"SKIP: card #{card_num} has empty paths - lease check waived")
    sys.exit(0)

bad = [f for f in files if (
    any(fnmatch.fnmatch(f, p) for p in forbid)
    or not any(fnmatch.fnmatch(f, p) for p in card_paths)
)]
if bad:
    print(f"OUT_OF_LEASE - files not in card #{card_num} paths={card_paths}:")
    for f in bad:
        print(f"  {f}")
    sys.exit(1)
print(f"OK - card #{card_num} paths={card_paths} cover all {len(files)} diff file(s): {files}")
