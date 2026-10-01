#!/usr/bin/env python3
"""Synthesize the trailer's sound-design layer: a low hit on every card cut, a riser into the
turn, and a bigger boom on the title. Generated from scratch, so there are no rights to clear.
Music (public-domain orchestral, per review v1) gets mixed under this later.
Output: build/hits.wav (48 kHz stereo, same length as the cut).
"""
import sys
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import assemble  # noqa: E402
import project  # noqa: E402

SR = 48000
OUT = assemble.ROOT / "build" / "hits.wav"


def hit(big: bool = False) -> np.ndarray:
    n = int(SR * (2.4 if big else 1.4))
    t = np.arange(n) / SR
    f0 = 42 if big else 55
    sweep = 2 * np.pi * (f0 * t + 30 * (1 - np.exp(-t * 18)) / 18)      # pitch drops into the boom
    body = np.sin(sweep) * np.exp(-t * (1.6 if big else 3.2))
    rng = np.random.default_rng(7)
    click = rng.standard_normal(n) * np.exp(-t * 60)                    # transient attack
    click = np.convolve(click, np.ones(24) / 24, mode="same")           # soften the click
    return 0.9 * body + 0.35 * click


def riser(seconds: float = 2.2) -> np.ndarray:
    n = int(SR * seconds)
    t = np.arange(n) / SR
    rng = np.random.default_rng(11)
    noise = rng.standard_normal(n)
    out, y = np.empty(n), 0.0
    for k in range(n):                                                  # one-pole lowpass opening up
        a = 0.02 + 0.5 * (t[k] / seconds) ** 2
        y += a * (noise[k] - y)
        out[k] = y
    return out * (t / seconds) ** 2 * 0.6


def out_path(version=None) -> Path:
    return OUT if version is None else OUT.with_name(f"hits_{version}.wav")


def cue_times(version=None):
    """(time, kind) for every sound cue, derived from the same timeline as the picture."""
    t, cues = 0.0, []
    s = project.script()
    turn_id, title_id = project.turn_beat(s), project.title_beat(s)
    for name, kind, a in assemble.plan(version):
        if a.get("hit"):
            beat = a["beat"]
            titled = beat == title_id or any(x["id"] == beat and x.get("title_style") for x in s["beats"])
            cues.append((t, "big" if titled else "hit"))
            if beat == turn_id:
                cues.append((max(0.0, t - 2.2), "riser"))   # short cuts may turn early
        t += a["dur"]
    return t, cues


def build(version=None) -> Path:
    total, cues = cue_times(version)
    mix = np.zeros(int(SR * total) + SR)
    for when, kind in cues:
        s = {"hit": hit, "big": lambda: hit(True), "riser": riser}[kind]()
        i = max(0, int(when * SR))
        mix[i:i + len(s)] += s[: len(mix) - i]
    mix = mix[: int(SR * total)]
    mix = mix / max(1e-9, np.abs(mix).max()) * 0.7                       # headroom for music later
    pcm = (np.stack([mix, mix], axis=1) * 32767).astype(np.int16)
    out = out_path(version)
    out.parent.mkdir(exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return out


if __name__ == "__main__":
    print(build(), len(cue_times()[1]), "cues")
