#!/usr/bin/env python3
"""Cut the music bed, mix it with the sound-design hits, and mux onto the picture.

The track and its edit points live in script.json["music"] (see references/music.md):
the opening section plays from `opening_in` until the turn beat, then a hard cut on the turn
into the climax, back-timed so the track reaches `climax_end` exactly as the trailer ends.
Output: build/trailer.mp4 (full cut) or build/trailer_<version>s.mp4
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import assemble  # noqa: E402
import sound_design  # noqa: E402

import project  # noqa: E402

ROOT = project.root()
BED = ROOT / "build" / "music_bed.wav"
OUT = ROOT / "build" / "trailer.mp4"
MUSIC_DB, HITS_DB = -2.0, -7.0


def out_path(version=None) -> Path:
    return OUT if version is None else ROOT / "build" / f"trailer_{version}s.mp4"


def turn_time(version=None) -> tuple[float, float]:
    t = 0.0
    for _, _, a in assemble.plan(version):
        if a.get("beat") == project.turn_beat():
            return t, sum(x["dur"] for _, _, x in assemble.plan(version))
        t += a["dur"]
    raise ValueError("turn beat not in timeline")


def build_bed(version=None) -> Path:
    turn, total = turn_time(version)
    bed = BED if version is None else BED.with_name(f"music_bed_{version}.wav")
    act3 = total - turn
    m = project.music()
    src = ROOT / m["file"]
    opening_in, climax_end, gain = float(m["opening_in"]), float(m["climax_end"]), float(m.get("opening_gain_db", 0))
    climax_in = climax_end - act3
    if climax_in < 0:
        raise ValueError(f"the climax section needs {act3:.1f}s but the track only has {climax_end:.1f}s before climax_end")
    fc = (f"[0:a]atrim={opening_in}:{opening_in + turn},asetpts=N/SR/TB,"
          f"volume={gain}dB,afade=t=in:d=1.0,afade=t=out:st={turn - 0.4:.2f}:d=0.4[a];"
          f"[0:a]atrim={climax_in:.3f}:{climax_end},asetpts=N/SR/TB,"
          f"afade=t=out:st={act3 - 1.2:.2f}:d=1.2[b];"
          f"[a][b]concat=n=2:v=0:a=1,aresample=48000,aformat=channel_layouts=stereo[out]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-filter_complex", fc,
                    "-map", "[out]", str(bed)], check=True)
    return bed


TARGET_LUFS = -14.0


def integrated_lufs(path: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    line = [l for l in err.splitlines() if l.strip().startswith("I:")][-1]
    return float(line.split()[1])


def build(version=None) -> Path:
    picture = assemble.build(version)
    hits = sound_design.build(version)
    bed = build_bed(version)
    out = out_path(version)
    fc = (f"[1:a]volume={MUSIC_DB}dB[m];[2:a]volume={HITS_DB}dB[h];"
          f"[m][h]amix=inputs=2:normalize=0:duration=first,"
          f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]")    # -14 LUFS: social-platform target
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(picture), "-i", str(bed), "-i", str(hits),
                    "-filter_complex", fc, "-map", "0:v:0", "-map", "[mix]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    # Single-pass loudnorm lands ~2 dB hot on this material; measure and trim to target.
    delta = TARGET_LUFS - integrated_lufs(out)
    if abs(delta) > 0.3:
        tmp = out.with_suffix(".tmp.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-c:v", "copy", "-af",
                        f"volume={delta:.2f}dB,alimiter=limit=0.84:level=false", "-c:a", "aac", "-b:a", "256k",
                        "-movflags", "+faststart", str(tmp)], check=True)
        tmp.replace(out)
    return out


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else None))
