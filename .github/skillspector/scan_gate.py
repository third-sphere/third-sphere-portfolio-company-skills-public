#!/usr/bin/env python3
"""SkillSpector CI gate for the Third Sphere public portco skills repo.

Runs NVIDIA SkillSpector (static, --no-llm) over one or more skill directories, drops
allowlisted findings, optionally writes a merged SARIF for upload, prints a human summary,
and EXITS 1 if any remaining finding is HIGH or CRITICAL (unless --report-only).

Two ways to feed it findings:
  * default: it invokes `skillspector scan <dir> --no-llm --format json` itself (CI).
  * --json FILE: parse an already-produced SkillSpector JSON instead of invoking it
    (handy for the local pre-push scan and for the test suite, which has no scanner).

Design note: the decision logic (parse_findings / evaluate) is kept free of subprocess and
filesystem side effects so it can be unit-tested anywhere, including environments without
SkillSpector or Python 3.12 installed. Only `scan_dir` shells out.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from typing import Iterable

try:  # PyYAML is present in CI (installed alongside pytest); allowlist is optional locally.
    import yaml
except ImportError:  # pragma: no cover - environment dependent
    yaml = None

BLOCKING = {"HIGH", "CRITICAL"}


# --------------------------------------------------------------------------- pure logic
def load_allowlist(path: str | None) -> set[tuple[str, str]]:
    """Return the set of (skill, rule_id) pairs a reviewer has consciously suppressed."""
    if not path:
        return set()
    p = pathlib.Path(path)
    if not p.exists() or yaml is None:
        return set()
    data = yaml.safe_load(p.read_text()) or {}
    return {
        (str(e.get("skill", "")), str(e.get("rule_id", "")))
        for e in data.get("suppress", [])
    }


def _message_of(f: dict) -> str:
    """Best human-readable line for a finding across the shapes above.

    The v2.9.x CLI carries no `message`; the useful text is `pattern` (what matched)
    plus `category`, with the file/line in a nested `location`. Without this, every
    finding printed as a bare rule id and the summary was unreadable.
    """
    msg = f.get("message") or f.get("pattern") or f.get("explanation") or ""
    cat = f.get("category")
    loc = f.get("location") or {}
    where = loc.get("file") or f.get("file") or ""
    line = loc.get("start_line") or f.get("line")
    parts = [str(msg)]
    if cat and str(cat) not in str(msg):
        parts.append(f"[{cat}]")
    if where:
        parts.append(f"({where}:{line})" if line else f"({where})")
    return " ".join(p for p in parts if p).strip()


def parse_findings(data: dict) -> list[dict]:
    """Normalize SkillSpector output into a flat list of {severity, rule_id, message}.

    The CLI JSON shape isn't contractually documented, so accept the variants we've seen:
    a top-level `issues` list (the v2.9.x CLI shape, verified against v2.9.6), a
    `filtered_findings`/`findings` list (the Python-API shape), or SARIF
    (`runs[].results[]`). Validate against real output when bumping the pinned version.
    """
    findings = data.get("filtered_findings")
    if findings is None:
        findings = data.get("findings")
    if findings is None:
        findings = data.get("issues")
    if findings is None and "runs" in data:  # SARIF fallback
        findings = []
        level_to_sev = {"error": "HIGH", "warning": "MEDIUM", "note": "LOW"}
        for run in data.get("runs", []):
            for r in run.get("results", []):
                sev = (r.get("properties", {}) or {}).get("severity")
                if not sev:
                    sev = level_to_sev.get(r.get("level", ""), "MEDIUM")
                msg = (r.get("message", {}) or {}).get("text", "")
                findings.append(
                    {"severity": sev, "rule_id": r.get("ruleId", ""), "message": msg}
                )
    if findings is None:
        raise ValueError("could not locate findings in SkillSpector output")
    out = []
    for f in findings:
        out.append(
            {
                "severity": str(f.get("severity", "")).upper(),
                "rule_id": str(f.get("rule_id") or f.get("id") or f.get("ruleId") or ""),
                "message": _message_of(f),
            }
        )
    return out


def evaluate(
    findings_by_skill: dict[str, list[dict]],
    allow: set[tuple[str, str]],
    report_only: bool = False,
) -> tuple[list[str], list[str], int]:
    """Return (summary_lines, blocking_lines, exit_code). exit_code is 1 when blocked."""
    summary: list[str] = []
    blocking: list[str] = []
    for skill, findings in findings_by_skill.items():
        if not findings:
            summary.append(f"  ok       {skill}: no findings")
            continue
        for f in findings:
            sev, rule = f["severity"], f["rule_id"]
            line = f"  {sev:<8} {skill}: {rule} — {f['message']}"
            if (skill, rule) in allow:
                summary.append(f"  allow    {skill}: {rule} ({sev}) — suppressed by allowlist")
                continue
            summary.append(line)
            if sev in BLOCKING:
                blocking.append(line)
    exit_code = 1 if (blocking and not report_only) else 0
    return summary, blocking, exit_code


# ------------------------------------------------------------------------- side effects
def scan_dir(skill_dir: str) -> list[dict]:
    """Invoke SkillSpector on one dir and parse its JSON. Fails closed on bad output."""
    proc = subprocess.run(
        ["skillspector", "scan", skill_dir, "--no-llm", "--format", "json"],
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(
            f"::error::could not parse SkillSpector JSON for {skill_dir}\n{proc.stderr}",
            file=sys.stderr,
        )
        sys.exit(2)  # fail closed: a scanner we can't read must not silently pass
    return parse_findings(data)


def write_merged_sarif(dirs: Iterable[str], out_path: str) -> None:
    """Best-effort: run SkillSpector per dir in SARIF mode and merge the runs for upload."""
    merged = {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": []}
    for d in dirs:
        proc = subprocess.run(
            ["skillspector", "scan", d, "--no-llm", "--format", "sarif"],
            capture_output=True,
            text=True,
        )
        try:
            merged["runs"].extend(json.loads(proc.stdout).get("runs", []))
        except json.JSONDecodeError:
            print(f"::warning::no SARIF produced for {d}", file=sys.stderr)
    pathlib.Path(out_path).write_text(json.dumps(merged, indent=2))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="SkillSpector CI gate (block on HIGH/CRITICAL).")
    ap.add_argument("dirs", nargs="+", help="skill directories to scan, e.g. skills/foo")
    ap.add_argument("--allowlist", help="path to allowlist.yml of reviewed suppressions")
    ap.add_argument("--sarif", help="write a merged SARIF here (for code-scanning upload)")
    ap.add_argument("--report-only", action="store_true", help="never exit non-zero")
    ap.add_argument(
        "--json",
        dest="json_file",
        help="use this pre-produced SkillSpector JSON instead of invoking the scanner "
        "(single-dir/local mode)",
    )
    args = ap.parse_args(argv)

    allow = load_allowlist(args.allowlist)

    findings_by_skill: dict[str, list[dict]] = {}
    if args.json_file:
        data = json.loads(pathlib.Path(args.json_file).read_text())
        # local mode scans one skill at a time; attribute findings to the first dir
        findings_by_skill[pathlib.Path(args.dirs[0]).name] = parse_findings(data)
    else:
        for d in args.dirs:
            findings_by_skill[pathlib.Path(d).name] = scan_dir(d)
        if args.sarif:
            write_merged_sarif(args.dirs, args.sarif)

    summary, blocking, code = evaluate(findings_by_skill, allow, args.report_only)
    print("SkillSpector gate:")
    print("\n".join(summary) if summary else "  (nothing scanned)")
    if blocking and not args.report_only:
        print(f"\n{len(blocking)} HIGH/CRITICAL finding(s) — failing the check.")
    elif blocking:
        print(f"\nreport-only: {len(blocking)} HIGH/CRITICAL finding(s), not failing.")
    else:
        print("\nNo blocking findings.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
