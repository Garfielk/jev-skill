import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/jev/scripts"))
import jev


SCENARIOS = (
    "jev-triage", "jev-documents", "jev-ui", "jev-route",
    "jev-context", "jev-code-review", "jev-find-code", "jev-simulation",
)


class SkillCatalogTests(unittest.TestCase):
    def test_scenario_entrypoints_and_examples(self):
        for name in SCENARIOS:
            with self.subTest(skill=name):
                folder = ROOT / "skills" / name
                text = (folder / "SKILL.md").read_text()
                self.assertIn(f"name: {name}\n", text)
                self.assertIn("description:", text)
                self.assertIn("jev-decide", text)
                self.assertIn("OPENROUTER_API_KEY", text)
                self.assertIn("assets/example.json", text)
                payload = json.loads((folder / "assets/example.json").read_text())
                jev.validate_request(payload)

    def test_installed_scenarios_dry_run_without_sibling_skill(self):
        for name in SCENARIOS:
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp) / name
                shutil.copytree(ROOT / "skills" / name, folder)
                output = io.StringIO()
                with patch.dict("os.environ", {}, clear=True), \
                        patch("urllib.request.urlopen", side_effect=AssertionError("network")), \
                        contextlib.redirect_stdout(output):
                    status = jev.main(["decide", str(folder / "assets/example.json"), "--dry-run"])
                self.assertEqual(status, 0)
                self.assertIn("questions", output.getvalue())

    def test_readmes_expose_each_scenario(self):
        for filename in ("README.md", "README.zh.md"):
            text = (ROOT / filename).read_text()
            for name in SCENARIOS:
                with self.subTest(readme=filename, skill=name):
                    self.assertIn(f"skills/{name}/SKILL.md", text)
                    self.assertIn(f"skills/{name}/assets/example.json", text)


if __name__ == "__main__":
    unittest.main()
