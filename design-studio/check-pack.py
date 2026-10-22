#!/usr/bin/env python3
"""Metadata validation of Liniya Sporta Design Studio (Python 3.11+ optional for TOML)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".agents" / "skills"
AGENTS = ROOT / ".codex" / "agents"
EXPECTED_SKILLS = {
    "ls-design-studio", "ls-typography", "ls-interior", "ls-signage",
    "ls-pictograms", "ls-print", "ls-brand", "ls-design-critic", "ls-digital-display"
}
EXPECTED_AGENTS = {
    "ls_creative_director", "ls_typographer", "ls_interior_designer",
    "ls_signage_designer", "ls_design_critic"
}
issues = []
for name in sorted(EXPECTED_SKILLS):
    path = SKILLS / name / "SKILL.md"
    if not path.is_file():
        issues.append(f"Missing skill: {path}")
        continue
    content = path.read_text(encoding="utf-8-sig")
    if not content.startswith("---\n") or len(content.split("---", 2)) < 3:
        issues.append(f"Missing frontmatter: {path}")
        continue
    frontmatter = content.split("---", 2)[1]
    if f"name: {name}" not in frontmatter or "description:" not in frontmatter:
        issues.append(f"Invalid skill metadata: {path}")
for name in sorted(EXPECTED_AGENTS):
    path = AGENTS / f"{name}.toml"
    if not path.is_file():
        issues.append(f"Missing agent: {path}")
        continue
    content = path.read_text(encoding="utf-8-sig")
    for field in (f'name = "{name}"', "description =", "developer_instructions ="):
        if field not in content:
            issues.append(f"Invalid agent metadata, {field}: {path}")
    try:
        import tomllib
    except ModuleNotFoundError:
        pass
    else:
        try:
            tomllib.loads(content)
        except Exception as error:
            issues.append(f"TOML parse error: {path}: {error}")
for path in (
    ROOT / "AGENTS.md",
    ROOT / "design-studio" / "README.md",
    ROOT / "design-studio" / "chatgpt-project-instructions.md",
    ROOT / "design-studio" / "qa-checklist.md",
):
    if not path.is_file():
        issues.append(f"Missing shared file: {path}")
if issues:
    for item in issues:
        print("FAIL:", item)
    sys.exit(1)
print(f"PASS: {len(EXPECTED_SKILLS)} skills, {len(EXPECTED_AGENTS)} agents, 4 shared files")
