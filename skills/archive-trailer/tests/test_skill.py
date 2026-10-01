"""archive-trailer skill tests. Run: python3 -m unittest discover -s tests -v   (about a minute)
Builds a tiny synthetic project (generated clips and music) so nothing touches the network."""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
PROJ = Path(tempfile.mkdtemp(prefix="trailer-test-"))
os.environ["TRAILER_PROJECT"] = str(PROJ)
sys.path.insert(0, str(SCRIPTS))


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def make_fixture():
    subprocess.run([sys.executable, str(SCRIPTS / "new_project.py"), str(PROJ), "Test trailer"], check=True,
                   capture_output=True)
    (PROJ / "clips").mkdir()
    cands = {}
    beats = [("01_a", 1, "First card.", 4), ("02_b", 1, None, 3), ("03_turn", 3, "The turn.", 3),
             ("04_c", 3, "Payoff line.", 3), ("05_title", 3, "TITLE", 4)]
    for n, (bid, act, card, dur) in enumerate(beats):
        clips = []
        for k in range(2):
            cid = f"{bid}-clip{k}"
            ff("-f", "lavfi", "-i", f"testsrc=size=640x480:rate=24:duration=6", "-vf", f"hue=h={n * 60 + k * 30}",
               "-pix_fmt", "yuv420p", str(PROJ / "clips" / f"{cid}.mp4"))
            clips.append({"id": cid, "sourceTitle": f"Fixture {bid} {k}", "sourceYear": 1930, "startSeconds": 0,
                          "endSeconds": 6, "durationSeconds": 6.0, "colorMode": "color",
                          "videoUrl": f"https://example.r2.dev/sources/{cid}.mp4", "thumbnailUrl": None})
        cands[bid] = [{"query": "fixture", "clips": clips}]
    (PROJ / "candidates.json").write_text(json.dumps(cands))
    s = json.loads((PROJ / "script.json").read_text())
    s.update({"runtime_target_s": 17, "turn_beat": "03_turn", "title_beat": "05_title",
              "rules": {"allowed_names": ["Acme"], "banned_text": ["guaranteed"]},
              "decisions": {"card_treatment": {"decision": "overlay_act3"}, "color": {"decision": "bw_then_color"}},
              "versions": {"11": {"beats": {"01_a": {"dur_s": 3, "picks": ["0.0"]}, "03_turn": {"dur_s": 2.5},
                                             "04_c": {"dur_s": 2.0, "picks": ["0.0"]}, "05_title": {"dur_s": 3.5}}}},
              "music": {"file": "assets/music/fixture.wav", "opening_in": 1.0, "climax_end": 40.0,
                        "opening_gain_db": 8.0}})
    s["beats"] = [{"id": b, "act": a, "card": c, "dur_s": d, "queries": ["q1", "q2"], "picks": ["0.0", "0.1"]}
                  for b, a, c, d in beats]
    s["beats"][-1]["subcards"] = ["A subtitle", "Imprint · 2026"]
    s["beats"][3]["demo"] = "Acme"
    (PROJ / "script.json").write_text(json.dumps(s, indent=1))
    # Music: 1 s silence, 19 s quiet, 20 s loud, final chord cut at 40.0 s, then 3 s decay.
    sr = 48000
    t = np.arange(int(sr * 43)) / sr
    amp = np.where(t < 1, 0, np.where(t < 20, 0.02, np.where(t < 40, 0.5, 0.5 * np.exp(-(t - 40) * 6))))
    sig = amp * np.sin(2 * np.pi * 220 * t)
    (PROJ / "assets" / "music").mkdir(parents=True)
    import wave
    with wave.open(str(PROJ / "assets" / "music" / "fixture.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((sig * 32767).astype(np.int16).tobytes())


make_fixture()
import apply_review  # noqa: E402
import assemble  # noqa: E402
import mix  # noqa: E402
import music_map  # noqa: E402
import project  # noqa: E402
import sound_design  # noqa: E402
from checks import make_plan_tests  # noqa: E402

PlanChecksOnFixture = make_plan_tests()     # the same checks a real project runs, on the fixture


class TestScaffold(unittest.TestCase):
    def test_scaffold_files(self):
        for f in ("script.json", "CONTEXT.md", ".gitignore", "tests/test_plan.py"):
            self.assertTrue((PROJ / f).exists(), f)

    def test_scaffold_refuses_overwrite(self):
        r = subprocess.run([sys.executable, str(SCRIPTS / "new_project.py"), str(PROJ), "x"], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)


class TestPlan(unittest.TestCase):
    def test_overlay_and_color_decisions(self):
        plan = list(assemble.plan())
        black = [a["text"] for _, k, a in plan if k == "card"]
        self.assertEqual(black, ["First card."])                      # act 1 card is a black card
        over = {a["beat"]: a.get("style") for _, k, a in plan if k == "shot" and a.get("overlay")}
        self.assertEqual(over, {"03_turn": "card", "04_c": "card", "05_title": "title"})
        for _, k, a in plan:
            if k == "shot":
                self.assertEqual(a["bw"], a["beat"] in ("01_a", "02_b"))

    def test_title_found_by_setting_not_subcards(self):
        s = project.script()
        self.assertEqual(project.title_beat(s), "05_title")
        s.pop("title_beat")
        self.assertEqual(project.title_beat(s), "05_title")              # falls back to subcards

    def test_cues(self):
        _, cues = sound_design.cue_times()
        self.assertEqual([k for _, k in cues].count("riser"), 1)
        self.assertEqual([k for _, k in cues][-1], "big")


class TestApplyReview(unittest.TestCase):
    EXPORT = {"run": "r1", "items": [
        {"id": "01_a", "action": "pick", "picks": ["01_a-clip1"], "text": "First card.", "text_changed": False},
        {"id": "02_b", "action": "more", "picks": [], "request": "a night street", "text": "", "text_changed": False},
        {"id": "04_c", "action": "keep", "picks": [], "text": "New payoff.", "text_changed": True}],
        "decisions": [{"id": "music_direction", "decision": "orchestral"}, {"id": "color", "decision": ""}]}

    def test_apply_and_idempotent(self):
        s0, c = project.script(), project.candidates()
        once = apply_review.apply(copy.deepcopy(self.EXPORT), copy.deepcopy(s0), c)
        twice = apply_review.apply(copy.deepcopy(self.EXPORT), copy.deepcopy(once), c)
        self.assertEqual(once, twice)
        b = {x["id"]: x for x in once["beats"]}
        self.assertEqual(b["01_a"]["picks"], ["0.1"])
        self.assertEqual(b["02_b"]["requery_pending"], "a night street")
        self.assertEqual(b["04_c"]["card"], "New payoff.")
        self.assertEqual(once["decisions"]["color"], s0["decisions"]["color"])   # unanswered: kept
        self.assertEqual(once["decisions"]["music_direction"]["decision"], "orchestral")

    def test_unknown_clip_rejected(self):
        with self.assertRaises(KeyError):
            apply_review.apply({"items": [{"id": "01_a", "action": "pick", "picks": ["nope"]}]},
                               project.script(), project.candidates())


class TestMusicMap(unittest.TestCase):
    def test_finds_edit_points_on_known_track(self):
        db, hop = music_map.loudness(str(PROJ / "assets/music/fixture.wav"))
        s = music_map.suggest(db, hop, act3=8)
        self.assertAlmostEqual(s["opening_in"], 1.0, delta=0.6)
        self.assertAlmostEqual(s["final_chord_cutoff"], 40.0, delta=0.5)
        self.assertAlmostEqual(s["quiet_gap_db"], 28.0, delta=2.0)             # 20*log10(0.5/0.02)
        self.assertTrue(s["climax_window_ok"])


class TestRender(unittest.TestCase):
    """End to end: picture + hits + music bed + loudness, full cut and a cutdown."""
    @classmethod
    def setUpClass(cls):
        cls.full = mix.build()
        cls.short = mix.build("11")

    def probe(self, p):
        return json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams",
                                          "-show_format", str(p)], capture_output=True, text=True, check=True).stdout)

    def test_lengths(self):
        self.assertAlmostEqual(float(self.probe(self.full)["format"]["duration"]), 17.0, delta=0.3)
        self.assertAlmostEqual(float(self.probe(self.short)["format"]["duration"]), 11.0, delta=0.3)

    def test_loudness_on_target(self):
        for p in (self.full, self.short):
            self.assertAlmostEqual(mix.integrated_lufs(p), mix.TARGET_LUFS, delta=1.0, msg=p.name)

    def test_music_too_short_is_caught(self):
        s = project.script()
        s["music"]["climax_end"] = 2.0                 # a climax that can't cover Act 3
        (PROJ / "script.json").write_text(json.dumps(s))
        try:
            with self.assertRaises(ValueError):
                mix.build_bed()
        finally:
            s["music"]["climax_end"] = 40.0
            (PROJ / "script.json").write_text(json.dumps(s))


if __name__ == "__main__":
    unittest.main()


class TestSearchCache(unittest.TestCase):
    """search.py must keep cached results when a beat's queries are unchanged (picks point into them),
    and re-search when they change. Network calls are stubbed."""
    def test_cache_rules(self):
        import search
        calls = []
        search.search = lambda q, retries=3: calls.append(q) or [
            {"id": f"new-{q}", "sourceTitle": "t", "durationSeconds": 3.0, "videoUrl": "https://x.r2.dev/sources/a.mp4",
             "thumbnailUrl": None}]
        search.sheet = lambda beat_id, rows: None
        search.time.sleep = lambda s: None
        before = json.loads((PROJ / "candidates.json").read_text())
        s = json.loads((PROJ / "script.json").read_text())
        s["beats"][0]["queries"] = ["fixture", "fixture"]        # matches the cached rows -> no call
        s["beats"][1]["queries"] = ["a brand new query"]         # changed -> re-searched
        (PROJ / "script.json").write_text(json.dumps(s))
        # cached rows for beat 0 need the same queries list to count as unchanged
        c = copy.deepcopy(before); c["01_a"] = [c["01_a"][0], c["01_a"][0]]
        (PROJ / "candidates.json").write_text(json.dumps(c))
        try:
            search.main()
            after = json.loads((PROJ / "candidates.json").read_text())
            self.assertEqual(after["01_a"], c["01_a"])                    # untouched
            self.assertIn("a brand new query", calls)
            self.assertNotIn("fixture", calls)
            self.assertEqual(after["02_b"][0]["query"], "a brand new query")
        finally:
            (PROJ / "candidates.json").write_text(json.dumps(before))
            s["beats"][0]["queries"] = ["q1", "q2"]; s["beats"][1]["queries"] = ["q1", "q2"]
            (PROJ / "script.json").write_text(json.dumps(s))


class TestFraming(unittest.TestCase):
    """The framing decision, on synthetic frames with a known 'face' position (detector stubbed)."""
    def setUp(self):
        import framing
        self.f = framing
        self.orig = framing._faces

    def tearDown(self):
        self.f._faces = self.orig

    def frames(self):
        return [np.zeros((1440, 1920), np.uint8)]          # a 4:3 source scaled to cover 1920x1080

    def test_no_faces_biases_upward(self):
        self.f._faces = lambda img: []
        self.assertEqual(self.f.decide(self.frames())["fy"], self.f.NO_FACE_FY)

    def test_face_near_top_keeps_its_head(self):
        self.f._faces = lambda img: [(120, 320)]            # a face high in the frame
        d = self.f.decide(self.frames())
        y = d["fy"] * (1440 - 804)
        self.assertLessEqual(y, 120 - 0.35 * 200 + 1)       # window starts above the headroom line
        self.assertFalse(d["faces_cut"])

    def test_faces_too_spread_to_fit_are_reported(self):
        self.f._faces = lambda img: [(60, 200), (1200, 1400)]
        d = self.f.decide(self.frames())
        self.assertTrue(d["faces_cut"])
        self.assertLessEqual(d["fy"] * (1440 - 804), 60)     # keeps the tops of heads

    def test_reading_time_and_wrap(self):
        self.assertAlmostEqual(project.reading_time("one two three four", s={"style": {}}), 0.8 + 2.0)
        serif = str(project.FONTS / "DMSerifDisplay-Regular.ttf")
        self.assertEqual(len(project.wrap("Short card.", serif, 84)), 1)
        self.assertEqual(len(project.wrap("It’s amongst the most important and valuable companies of our time.", serif, 84)), 2)
