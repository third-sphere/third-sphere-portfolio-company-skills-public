#!/usr/bin/env python3
"""Consistency checks for the plugin + marketplace manifests.

This repo is distributed two ways from one tree: as a Claude Code plugin
(`.claude-plugin/`) and as a folder of skills to copy by hand. Those two paths
drift silently — a skill added to `skills/` is picked up by the plugin
automatically but stays missing from the README table, and a version bumped in
`plugin.json` but not in `marketplace.json` means installed copies never see the
update. Neither failure is visible until someone tries to install.

These are cheap structural checks, not a schema validator. `claude plugin
validate .` is the real validator; it needs the Claude Code CLI, which CI here
doesn't have.
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MARKET = ROOT / ".claude-plugin" / "marketplace.json"
SKILLS = ROOT / "skills"
README = ROOT / "README.md"


def _plugin() -> dict:
    return json.loads(PLUGIN.read_text())


def _entry() -> dict:
    """The marketplace entry for this repo's own plugin."""
    market = json.loads(MARKET.read_text())
    name = _plugin()["name"]
    matches = [p for p in market["plugins"] if p.get("name") == name]
    assert matches, f"no marketplace entry named {name!r}"
    return matches[0]


def skill_dirs() -> list[pathlib.Path]:
    return sorted(d for d in SKILLS.iterdir() if d.is_dir())


# ----------------------------------------------------------------- manifests
def test_manifests_parse():
    assert _plugin()["name"], "plugin.json needs a name"
    market = json.loads(MARKET.read_text())
    assert market["name"], "marketplace.json needs a name"
    assert market["owner"]["name"], "marketplace.json needs owner.name"


def test_plugin_name_is_kebab_case():
    name = _plugin()["name"]
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name), (
        f"{name!r} must be kebab-case — it is the skill namespace users type"
    )


def test_marketplace_entry_points_at_repo_root():
    # Single-plugin repo: the plugin IS this repo, so source is the marketplace root.
    assert _entry()["source"] == ".", "source must be '.' for a single-plugin repo"


def test_versions_agree():
    """A version set in one file and not the other means users get no update."""
    pv, mv = _plugin().get("version"), _entry().get("version")
    assert pv == mv, (
        f"plugin.json version {pv!r} != marketplace.json version {mv!r}; "
        "bump both or omit both"
    )


def test_version_is_semver():
    v = _plugin().get("version")
    if v is not None:
        assert re.fullmatch(r"\d+\.\d+\.\d+", v), f"{v!r} is not semver"


# -------------------------------------------------------------------- skills
def test_every_skill_has_a_skill_md():
    missing = [d.name for d in skill_dirs() if not (d / "SKILL.md").is_file()]
    assert not missing, f"skill dirs without SKILL.md: {missing}"


def test_frontmatter_name_matches_directory():
    """The plugin namespaces skills by directory; a mismatched frontmatter name
    makes the skill answer to something other than what its folder implies."""
    bad = []
    for d in skill_dirs():
        text = (d / "SKILL.md").read_text()
        m = re.search(r"^name:\s*(\S+)\s*$", text, re.M)
        if m and m.group(1) != d.name:
            bad.append((d.name, m.group(1)))
    assert not bad, f"frontmatter name != directory name: {bad}"


def test_every_skill_has_a_description():
    """Skills are model-invoked off the description; without one it never fires."""
    missing = [
        d.name
        for d in skill_dirs()
        if not re.search(r"^description:", (d / "SKILL.md").read_text(), re.M)
    ]
    assert not missing, f"skills with no description frontmatter: {missing}"


# -------------------------------------------------------------------- README
def test_readme_table_lists_every_skill():
    """The README table is the human index; a skill missing from it is invisible."""
    table = README.read_text()
    missing = [d.name for d in skill_dirs() if f"**{d.name}**" not in table]
    assert not missing, f"skills missing from the README table: {missing}"


def test_readme_table_has_no_phantom_rows():
    rows = set(re.findall(r"^\|\s*\*\*([a-z0-9-]+)\*\*\s*\|", README.read_text(), re.M))
    phantom = rows - {d.name for d in skill_dirs()}
    assert not phantom, f"README rows with no matching skill dir: {sorted(phantom)}"


# ------------------------------------------------------------------- licensing
def test_license_file_exists_and_is_mpl2():
    lic = ROOT / "LICENSE"
    assert lic.is_file(), "no LICENSE file — other orgs have no right to use this"
    head = lic.read_text()[:200]
    assert "Mozilla Public License Version 2.0" in head, (
        "LICENSE is not the MPL-2.0 text the manifests declare"
    )


def test_declared_license_matches_across_manifests():
    """A mismatch here means the plugin manager shows terms the repo doesn't grant."""
    assert _plugin().get("license") == "MPL-2.0"
    assert _entry().get("license") == "MPL-2.0"


def test_notice_file_names_a_copyright_holder():
    notice = ROOT / "NOTICE"
    assert notice.is_file(), "NOTICE carries the copyright line MPL 3.4 protects"
    assert re.search(r"Copyright \(c\) \d{4}", notice.read_text())
