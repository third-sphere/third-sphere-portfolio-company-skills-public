"""Reusable checks for any trailer project. A project's tests/test_plan.py calls make_plan_tests().

Rules come from the project's script.json, not from this file:
  runtime_target_s, turn_beat, title_beat, versions, and
  rules.allowed_names  (anything in a beat's "demo"/"names" must be listed here)
  rules.banned_text    (words or phrases that must never appear on a card; matched on word boundaries)
Checks that need picks or rendered files skip themselves until those exist.
"""
import json
import re
import subprocess
import unittest

import project


def _load():
    return project.script(), project.candidates()


def make_plan_tests():
    import assemble
    import mix
    import sound_design
    from PIL import ImageFont

    class PlanTests(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.s, cls.c = _load()
            cls.beats = [b for b in cls.s["beats"] if not b.get("cut")]
            cls.picked = all(b.get("picks") for b in cls.beats)

        # ---------- structure (always) ----------
        def test_turn_and_title_beats_exist(self):
            ids = [b["id"] for b in self.beats]
            self.assertIn(project.turn_beat(self.s), ids)
            self.assertEqual(ids[-1], project.title_beat(self.s), "the title beat should close the trailer")

        def test_runtime_near_target(self):
            target = self.s.get("runtime_target_s", 60)
            total = sum(b["dur_s"] for b in self.beats)
            self.assertLessEqual(abs(total - target), 0.15 * target, f"{total}s vs target {target}s")

        def test_every_beat_has_queries(self):
            for b in self.beats:
                self.assertTrue(b.get("queries"), b["id"])

        def test_banned_text_absent_from_cards(self):
            banned = self.s.get("rules", {}).get("banned_text", [])
            for b in self.beats:
                text = " ".join([b.get("card") or "", *b.get("subcards", [])]).lower()
                for w in banned:
                    self.assertIsNone(re.search(rf"(?<!\w){re.escape(w.lower())}(?!\w)", text),
                                      f"{b['id']}: banned text {w!r} on a card")

        def test_named_things_are_allowed(self):
            allowed = set(self.s.get("rules", {}).get("allowed_names", []))
            for b in self.beats:
                for n in [b.get("demo"), *b.get("names", [])]:
                    if n:
                        self.assertIn(n, allowed, f"{b['id']}: {n!r} is not in rules.allowed_names")

        def test_cards_fit_the_frame(self):
            # Long cards wrap onto two lines; three or more lines means the card needs shortening.
            serif = str(project.FONTS / "DMSerifDisplay-Regular.ttf")
            sans = str(project.FONTS / "DMSans.ttf")
            title_id = project.title_beat(self.s)
            for b in self.beats:
                if not b.get("card"):
                    continue
                size = 110 if (b["id"] == title_id or b.get("title_style")) else 84
                for text, font, sz in [(b["card"], serif, size)] + [(x, sans, 40) for x in b.get("subcards", [])]:
                    lines = project.wrap(text, font, sz)
                    self.assertLessEqual(len(lines), 2, f"{b['id']}: {text!r} needs more than two lines")
                    for ln in lines:
                        w = ImageFont.truetype(font, sz).getlength(ln)
                        self.assertLess(w, 1920 * 0.9, f"{b['id']}: {ln!r} is {w:.0f}px wide")

        def test_cards_have_reading_time(self):
            # Every card stays up long enough for a slow reader, in every version.
            if not self.picked:
                self.skipTest("not every beat has picks yet")
            by_id = {b["id"]: b for b in self.beats}
            for v in [None, *self.s.get("versions", {})]:
                shown = {}
                for _, k, a in assemble.plan(v):
                    if k == "card":
                        shown[a["beat"]] = shown.get(a["beat"], 0) + a["dur"]
                    elif a.get("overlay"):
                        shown[a["beat"]] = shown.get(a["beat"], 0) + a["dur"]
                for bid, t in shown.items():
                    b = by_id[bid]
                    texts = [b["card"], *b.get("subcards", [])] if (b["id"] == project.title_beat(self.s)
                                                                    or b.get("title_style")) else [b["card"]]
                    need = project.reading_time(*texts, s=self.s)
                    self.assertGreaterEqual(t + 1e-6, need, f"{v or 'full'}: {bid} shows its text {t:.1f}s; "
                                            f"a slow reader needs {need:.1f}s ({project.words(*texts)} words)")

        def test_no_faces_lost_to_cropping(self):
            p = project.root() / "framing.json"
            if not p.exists():
                self.skipTest("no framing decisions yet (render first)")
            cache = json.loads(p.read_text())
            used = {}
            for b in self.beats:
                for ref in b.get("picks", []):
                    r, i = map(int, ref.split("."))
                    used[self.c[b["id"]][r]["clips"][i]["id"]] = b
            for key, d in cache.items():
                cid = key.split("|")[0]
                b = used.get(cid)
                if b is None or not d.get("faces_cut"):
                    continue
                ok = b.get("crop_ok")
                if isinstance(ok, str):
                    self.fail(f"{b['id']}: crop_ok must name the clips it covers ({{clip_id: reason}}), so a new "
                              f"pick can't inherit an acceptance meant for another clip")
                hand = {self.c[b["id"]][int(r.split(".")[0])]["clips"][int(r.split(".")[1])]["id"]
                        for r in b.get("frame_y", {})}           # clips framed by hand skip the auto verdict
                if cid not in (ok or {}) and cid not in hand:
                    self.fail(f"{b['id']}: shot {cid[:8]} crops a face; pick another, set frame_y by hand, "
                              f"or accept it in crop_ok {{clip_id: reason}} after looking")

        # ---------- picks (once chosen) ----------
        def test_picks_resolve_to_real_clips(self):
            if not self.picked:
                self.skipTest("not every beat has picks yet")
            for b in self.beats:
                for p in b["picks"]:
                    r, i = map(int, p.split("."))
                    clip = self.c[b["id"]][r]["clips"][i]
                    prov = clip.get("provenance")
                    if prov:
                        self.assertTrue(prov.get("source") and prov.get("identifier"), (b["id"], p))
                    else:
                        self.assertIn(".r2.dev/sources/", clip["videoUrl"], (b["id"], p))

        def test_picks_long_enough_to_fill_each_beat(self):
            # The assembler trims each pick to its share of the beat; a pick shorter than its share
            # silently shortens the beat (and the whole trailer). Name that failure directly.
            if not self.picked:
                self.skipTest("not every beat has picks yet")
            for v in [None, *self.s.get("versions", {})]:
                want = {b["id"]: b["dur_s"] for b in self.beats} if v is None else \
                       {k: o["dur_s"] for k, o in self.s["versions"][v]["beats"].items()}
                got = {}
                for _, _, a in assemble.plan(v):
                    got[a["beat"]] = got.get(a["beat"], 0) + a["dur"]
                for bid, d in want.items():
                    self.assertAlmostEqual(got.get(bid, 0), d, delta=0.05,
                                           msg=f"{v or 'full'}: {bid} plays {got.get(bid, 0):.2f}s of {d}s; "
                                               f"its picks are too short. Add a pick or shorten the beat.")

        def test_timeline_matches_script(self):
            if not self.picked:
                self.skipTest("not every beat has picks yet")
            total = sum(a["dur"] for _, _, a in assemble.plan())
            self.assertAlmostEqual(total, sum(b["dur_s"] for b in self.beats), delta=0.05)

        def test_no_shot_too_short_to_read(self):
            if not self.picked:
                self.skipTest("not every beat has picks yet")
            for v in [None, *self.s.get("versions", {})]:
                for name, kind, a in assemble.plan(v):
                    if kind == "shot":
                        floor = 1.2 if a.get("overlay") else 0.8
                        self.assertGreaterEqual(a["dur"], floor, f"{v or 'full'}: {name}")
                        self.assertLessEqual(a["dur"], a["clip"]["durationSeconds"] + 1e-6, name)

        def test_one_hit_per_beat_and_one_riser(self):
            if not self.picked:
                self.skipTest("not every beat has picks yet")
            for v in [None, *self.s.get("versions", {})]:
                _, cues = sound_design.cue_times(v)
                n = len(self.beats) if v is None else len(self.s["versions"][v]["beats"])
                self.assertEqual(sum(k in ("hit", "big") for _, k in cues), n, v)
                self.assertEqual(sum(k == "riser" for _, k in cues), 1, v)

        def test_versions_hit_length_and_keep_turn_and_title(self):
            if not self.picked:
                self.skipTest("not every beat has picks yet")
            for v, spec in self.s.get("versions", {}).items():
                self.assertIn(project.turn_beat(self.s), spec["beats"], v)
                self.assertIn(project.title_beat(self.s), spec["beats"], v)
                self.assertAlmostEqual(sum(a["dur"] for _, _, a in assemble.plan(v)), float(v), delta=0.05, msg=v)

        # ---------- rendered output (once built) ----------
        def test_rendered_cuts(self):
            outs = [(None, mix.out_path(None))] + [(v, mix.out_path(v)) for v in self.s.get("versions", {})]
            built = [(v, p) for v, p in outs if p.exists()]
            if not built:
                self.skipTest("nothing rendered yet")
            for v, p in built:
                info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json",
                                                  "-show_streams", "-show_format", str(p)],
                                                 capture_output=True, text=True, check=True).stdout)
                vid = next(x for x in info["streams"] if x["codec_type"] == "video")
                self.assertEqual((vid["width"], vid["height"], vid["pix_fmt"]), (1920, 1080, "yuv420p"), p.name)
                want = float(v) if v else sum(b["dur_s"] for b in self.beats)
                self.assertAlmostEqual(float(info["format"]["duration"]), want, delta=0.3, msg=p.name)
                self.assertAlmostEqual(mix.integrated_lufs(p), mix.TARGET_LUFS, delta=1.0, msg=p.name)

    return PlanTests
