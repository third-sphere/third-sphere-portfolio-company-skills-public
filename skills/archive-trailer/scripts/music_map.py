#!/usr/bin/env python3
"""Map a track's loudness and suggest trailer edit points.

Usage: python3 music_map.py <audio file> [--act3 SECONDS]
Prints loudness every 5 seconds, then suggests:
  opening_in   first moment the music is clearly audible (for the quiet opening under Acts 1-2)
  climax_end   just after the final loud chord cuts off, leaving a little hall decay
  quiet_gap_db how much quieter the opening is than the climax; the suggested opening gain keeps
               it ~12 dB under the climax, the balance that was approved on an earlier trailer
With --act3, also checks that the climax window before climax_end is long enough and loud
throughout. Listen before trusting it: the numbers find candidates, your ears decide.
"""
import subprocess
import sys

import numpy as np

SR = 8000
OPENING_HEADROOM_DB = 12.0   # calibrated on one approved mix (2026-09); revisit with more


def loudness(path: str, hop: float = 0.1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(float)
    w = int(SR * hop)
    frames = a[: len(a) // w * w].reshape(-1, w)
    return 20 * np.log10(np.sqrt((frames ** 2).mean(1)) / 32768 + 1e-9), hop


def suggest(db, hop, act3=None):
    smooth = np.convolve(db, np.ones(10) / 10, mode="same")          # 1 s moving average, for finding regions
    peak = np.percentile(smooth, 98)
    audible = np.where(smooth > peak - 35)[0]
    opening_in = round(audible[0] * hop, 1) if len(audible) else 0.0
    loud = np.where(smooth > peak - 8)[0]
    last_loud = loud[-1] if len(loud) else len(db) - 1
    # The drop itself is found on the unsmoothed signal: smoothing delays it by up to a second.
    start = max(0, last_loud - int(2 / hop))
    raw_after = db[start:]
    drop = np.where(raw_after < peak - 15)[0]
    cutoff = (start + (drop[0] if len(drop) else len(raw_after))) * hop
    climax_end = round(min(cutoff + 1.8, len(db) * hop), 1)          # keep ~2 s of hall decay
    # Compare the opening with the climax's typical level, not its loudest moment.
    head = db[int(opening_in / hop): int(opening_in / hop) + int(25 / hop)]
    tail = db[max(0, int((cutoff - 30) / hop)): int(cutoff / hop)]
    gap = round(float(np.median(tail) - np.median(head)), 1) if len(head) and len(tail) else 0.0
    out = {"opening_in": opening_in, "climax_end": climax_end, "final_chord_cutoff": round(cutoff, 1),
           "quiet_gap_db": gap,
           # Keep the opening well under the climax, not level with it: an approved mix sat ~12 dB below.
           "suggested_opening_gain_db": max(0.0, round(gap - OPENING_HEADROOM_DB, 0))}
    if act3:
        win = smooth[int((climax_end - act3) / hop): int(cutoff / hop)]
        out["climax_window_ok"] = bool(len(win) and np.percentile(win, 10) > peak - 12)
        out["climax_window_min_db_below_peak"] = round(float(peak - win.min()), 1) if len(win) else None
    return out


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    act3 = float(argv[argv.index("--act3") + 1]) if "--act3" in argv else None
    db, hop = loudness(argv[1])
    step = int(5 / hop)
    for i in range(0, len(db), step * 12):
        row = db[i: i + step * 12: step]
        t = i * hop
        print(f"{int(t // 60):2d}:{int(t % 60):02d} " + " ".join(f"{x:4.0f}" for x in row))
    for k, v in suggest(db, hop, act3).items():
        print(f"{k:34} {v}")


if __name__ == "__main__":
    main(sys.argv)
