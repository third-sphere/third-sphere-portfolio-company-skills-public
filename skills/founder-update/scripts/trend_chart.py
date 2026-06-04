#!/usr/bin/env python3
"""
trend_chart.py — Generate a clean trend chart (PNG) for a founder investor update.

Plots one or more metrics over the last several periods, with an optional target line.
Designed for the "at least one chart of progress over months" requirement: e.g. new
qualified leads, pipeline $, ARR, revenue, or runway across the trailing periods.

USAGE
-----
  python3 trend_chart.py --spec chart.json --out /mnt/user-data/outputs/acme_trend.png
  echo '{...}' | python3 trend_chart.py --out out.png        # spec on stdin

SPEC SCHEMA (JSON)
------------------
{
  "title":  "New qualified leads",        # chart title (required)
  "ylabel": "Leads",                       # y-axis label (optional)
  "periods": ["Feb","Mar","Apr","May","Jun"],   # x labels, oldest -> newest (required)
  "series": [                              # 1+ series; values align to periods (required)
    {"name": "Qualified leads", "values": [3, 5, 6, 8, 11]}
  ],
  "target": 15,                            # optional horizontal target line
  "kind":   "line",                        # "line" (default) or "bar"
  "money":  false                          # true -> format axis/labels as $ (k/M)
}

Notes:
- Use null in a values array for a missing period (the line will gap there).
- Single-point series are rejected — a trend needs >=2 points. Skip the chart and note
  that tracking starts next period instead of faking history.
"""
import argparse
import json
import sys


def _fmt_money(v):
    if v is None:
        return ""
    av = abs(v)
    if av >= 1_000_000:
        return f"${v/1_000_000:.1f}M"
    if av >= 1_000:
        return f"${v/1_000:.0f}K"
    return f"${v:.0f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", help="Path to JSON spec (omit to read stdin)")
    ap.add_argument("--out", required=True, help="Output PNG path")
    args = ap.parse_args()

    raw = open(args.spec).read() if args.spec else sys.stdin.read()
    spec = json.loads(raw)

    periods = spec["periods"]
    series = spec["series"]
    title = spec["title"]
    ylabel = spec.get("ylabel", "")
    target = spec.get("target")
    kind = spec.get("kind", "line")
    money = bool(spec.get("money", False))

    max_pts = max(len([v for v in s["values"] if v is not None]) for s in series)
    if max_pts < 2:
        sys.exit("ERROR: need >=2 data points for a trend chart. Skip the chart this "
                 "period and note that tracking starts next period.")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    # Clean, neutral, investor-friendly palette (color-blind safe).
    palette = ["#2563EB", "#059669", "#D97706", "#7C3AED", "#DC2626"]
    plt.rcParams.update({
        "font.size": 12,
        "font.family": "sans-serif",
        "axes.edgecolor": "#D1D5DB",
        "axes.linewidth": 0.8,
    })

    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=160)
    x = list(range(len(periods)))

    for i, s in enumerate(series):
        color = palette[i % len(palette)]
        vals = s["values"]
        if kind == "bar" and len(series) == 1:
            bars = ax.bar(x, [v if v is not None else 0 for v in vals],
                          color=color, width=0.6, zorder=3)
            for xi, v in zip(x, vals):
                if v is not None:
                    ax.annotate(_fmt_money(v) if money else f"{v:g}",
                                (xi, v), textcoords="offset points", xytext=(0, 5),
                                ha="center", fontsize=10, color="#374151")
        else:
            ax.plot(x, vals, marker="o", linewidth=2.4, markersize=6,
                    color=color, label=s["name"], zorder=3)
            for xi, v in zip(x, vals):
                if v is not None:
                    ax.annotate(_fmt_money(v) if money else f"{v:g}",
                                (xi, v), textcoords="offset points", xytext=(0, 8),
                                ha="center", fontsize=10, color="#374151")

    if target is not None:
        ax.axhline(target, ls="--", lw=1.4, color="#9CA3AF", zorder=2)
        ax.annotate(f"target {_fmt_money(target) if money else target:g}"
                    if not money else f"target {_fmt_money(target)}",
                    (x[-1], target), textcoords="offset points", xytext=(4, 4),
                    ha="right", va="bottom", fontsize=9, color="#6B7280")

    ax.set_xticks(x)
    ax.set_xticklabels(periods)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12, loc="left")
    ax.margins(y=0.18)
    ax.grid(axis="y", color="#F0F1F3", linewidth=1, zorder=0)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    if money:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _fmt_money(v)))
    if len(series) > 1:
        ax.legend(frameon=False, loc="upper left", fontsize=10)

    fig.tight_layout()
    fig.savefig(args.out, bbox_inches="tight", facecolor="white")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
