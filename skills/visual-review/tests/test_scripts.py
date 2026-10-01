"""Tests for the visual-review scripts. Run: python3 -m unittest discover -s tests -v
Uses generated images and a generated video, so no network or fixtures are needed."""
import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import build_page  # noqa: E402
import merge_export  # noqa: E402


class Fixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        for name, color in (("red", (200, 40, 30)), ("blue", (30, 60, 200)), ("green", (30, 160, 60))):
            Image.new("RGB", (1200, 800), color).save(cls.tmp / f"{name}.jpg")
        Image.new("RGBA", (300, 900), (250, 200, 0, 255)).save(cls.tmp / "tall.png")
        cls.video = cls.tmp / "clip.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=640x360:rate=24:duration=3",
                        "-pix_fmt", "yuv420p", str(cls.video)], check=True)

    def spec(self):
        t = self.tmp
        return {"title": "Test review", "storage_key": "test-r1", "run": "r1", "items": [
            {"id": "a", "label": "Item A", "current": ["red"], "text_field": {"label": "Caption", "value": "Hello"},
             "options": [{"id": "red", "source": str(t / "red.jpg")}, {"id": "blue", "source": str(t / "blue.jpg")},
                         {"id": "vid", "source": str(self.video), "label": "A video"},
                         {"id": "bad", "source": str(t / "green.jpg"), "exclude": "watermark"}]},
            {"id": "b", "label": "Item B", "max_picks": 1,
             "options": [{"id": "tall", "source": str(t / "tall.png"), "flag": "third-party logo"}]}],
            "decisions": [{"id": "music", "question": "Music?", "options": [["a", "A"], ["b", "B"]]}]}


class TestBuild(Fixtures):
    def build(self, spec):
        return build_page.build(spec, self.tmp / "out.html")

    def test_builds_and_inlines_every_image(self):
        out, _ = self.build(self.spec())
        html = out.read_text()
        spec = json.loads(re.search(r"const SPEC = (\{.*?\});\n", html, re.S).group(1).replace("<\\/", "</"))
        for it in spec["items"]:
            for o in it["options"]:
                self.assertTrue(o["image"].startswith("data:image/"), o["id"])
                self.assertNotIn("source", o)
        self.assertNotRegex(html, r"url\('https?:")

    def test_exclusions_dropped_and_reported(self):
        out, report = self.build(self.spec())
        self.assertIn('"bad"', self.spec().__repr__().replace("'", '"'))
        self.assertNotIn('"id": "bad"', out.read_text())
        self.assertEqual(report, ["a: excluded bad: watermark"])

    def test_video_becomes_flipbook_and_still_fits_box(self):
        spec = self.spec()
        build_page.validate(spec)
        vid = next(o for o in spec["items"][0]["options"] if o["id"] == "vid")
        build_page.resolve_image(vid)
        self.assertEqual((vid["frames"], vid["w"], vid["h"]), (4, 184, 138))
        tall = spec["items"][1]["options"][0]
        build_page.resolve_image(tall)
        self.assertEqual((tall["w"], tall["h"]), (240, 180))       # padded, so mixed shapes line up
        red = spec["items"][0]["options"][0]
        build_page.resolve_image(red)
        self.assertEqual((red["w"], red["h"]), (240, 180))

    def test_keep_label_when_nothing_is_current(self):
        html = (SKILL / "assets" / "page.html").read_text()
        self.assertIn('"No choice yet"', html)

    def test_validation_errors(self):
        s = self.spec(); s["items"][0]["current"] = ["nope"]
        with self.assertRaises(build_page.SpecError):
            self.build(s)
        s = self.spec(); del s["storage_key"]
        with self.assertRaises(build_page.SpecError):
            self.build(s)
        s = self.spec(); s["items"][1]["options"][0]["exclude"] = "cut"
        with self.assertRaises(build_page.SpecError):   # an item with nothing left to show
            self.build(s)

    def test_size_limit_enforced(self):
        old = build_page.MAX_BYTES
        try:
            build_page.MAX_BYTES = 1000
            with self.assertRaises(build_page.SpecError):
                self.build(self.spec())
        finally:
            build_page.MAX_BYTES = old

    def test_input_spec_not_mutated(self):
        s = self.spec(); before = copy.deepcopy(s)
        self.build(s)
        self.assertEqual(s, before)

    def test_storage_calls_guarded(self):
        html = (SKILL / "assets" / "page.html").read_text()
        for m in re.finditer(r"localStorage\.\w+\(", html):
            line = html[html.rfind("\n", 0, m.start()) + 1:m.start()]
            self.assertIn("try{", line, line.strip()[:60])


class TestMerge(unittest.TestCase):
    EXPORT = {"run": "r1", "items": [
        {"id": "a", "action": "pick", "picks": ["blue"], "current": ["red"], "text": "Hi", "text_changed": True,
         "request": "", "notes": "brighter"},
        {"id": "b", "action": "more", "picks": [], "current": [], "text": None, "text_changed": False,
         "request": "something at night", "notes": ""},
        {"id": "c", "action": "keep", "picks": [], "current": ["x"], "text": None, "text_changed": False,
         "request": "", "notes": ""}],
        "decisions": [{"id": "music", "decision": "a", "notes": ""}, {"id": "tone", "decision": "", "notes": ""}],
        "freetext": {"overall": "good"}}

    def test_merge_applies_choices(self):
        s = merge_export.merge({}, copy.deepcopy(self.EXPORT))
        self.assertEqual(s["items"]["a"]["picks"], ["blue"])
        self.assertEqual(s["items"]["a"]["history"][0]["picks"], ["red"])
        self.assertEqual(s["items"]["a"]["text"], "Hi")
        self.assertEqual(s["items"]["b"]["status"], "wants_other_options")
        self.assertEqual(s["items"]["b"]["request"], "something at night")
        self.assertEqual(s["items"]["c"], {"picks": ["x"], "history": [], "status": "kept"})
        self.assertEqual(s["decisions"], {"music": {"decision": "a", "notes": ""}})   # unanswered not stored

    def test_idempotent(self):
        once = merge_export.merge({}, copy.deepcopy(self.EXPORT))
        twice = merge_export.merge(copy.deepcopy(once), copy.deepcopy(self.EXPORT))
        self.assertEqual(once, twice)

    def test_partial_round_keeps_earlier_answers(self):
        s = merge_export.merge({}, copy.deepcopy(self.EXPORT))
        partial = {"run": "r2", "items": [{"id": "a", "action": "keep", "picks": [], "current": ["blue"],
                                           "text": "Hello again", "text_changed": True, "request": "", "notes": ""}],
                   "decisions": [{"id": "music", "decision": "", "notes": ""}]}
        s2 = merge_export.merge(copy.deepcopy(s), partial)
        self.assertEqual(s2["decisions"]["music"]["decision"], "a")
        self.assertEqual(s2["items"]["a"]["picks"], ["blue"])
        self.assertEqual(s2["items"]["a"]["text"], "Hello again")
        self.assertEqual(s2["items"]["b"], s["items"]["b"])
        self.assertEqual(s2["runs"], ["r1", "r2"])

    def test_cli_saves_export_verbatim(self):
        d = Path(tempfile.mkdtemp())
        (d / "export.json").write_text(json.dumps({**self.EXPORT, "exported_at": "2026-09-29T04:37:35.129Z"}))
        subprocess.run([sys.executable, str(SKILL / "scripts" / "merge_export.py"), str(d / "state.json"),
                        str(d / "export.json")], check=True, capture_output=True)
        saved = list((d / "rounds").glob("*.json"))
        self.assertEqual(len(saved), 1)
        self.assertEqual(json.loads(saved[0].read_text())["items"], self.EXPORT["items"])


if __name__ == "__main__":
    unittest.main()
