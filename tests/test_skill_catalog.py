import contextlib
import io
import json
import re
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
    def test_agent_first_installation_entrypoint(self):
        guide_url = "https://raw.githubusercontent.com/wuyoscar/jev-skill/main/docs/install.md"
        for filename in ("README.md", "README.zh.md"):
            text = (ROOT / filename).read_text()
            first_block = re.search(r"```(\w*)\n(.*?)\n```", text, re.S)
            self.assertEqual(first_block.group(1), "text")
            self.assertIn(guide_url, first_block.group(2))
            self.assertLess(text.index(guide_url), text.index('id="agent"'))
        guide = (ROOT / "docs/install.md").read_text()
        for name in ("jev", *SCENARIOS):
            self.assertIn(f"`{name}`", guide)
        for requirement in ("OPENROUTER_API_KEY", "--dry-run", "v0.1.0"):
            self.assertIn(requirement, guide)

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

    def test_readmes_cover_the_full_researched_catalog(self):
        references = ROOT / "skills/jev/references"
        recipe_ids = set()
        for filename in ("agent-recipes.md", "human-recipes.md"):
            recipe_ids.update(re.findall(r"\*\*([AH]\d{2}) ·", (references / filename).read_text()))
        pattern_ids = {
            f"M{int(number):02d}" for number in re.findall(
                r"^## (\d+)\.", (references / "implementation-patterns.md").read_text(), re.M
            )
        }
        social_ids = {f"X{number:02d}" for number in range(1, 8)}
        readmes = [(ROOT / name).read_text() for name in ("README.md", "README.zh.md")]
        for text in readmes:
            coverage = re.findall(r"<!-- covers: (.*?) -->", text)
            covered = set(" ".join(coverage).split())
            self.assertTrue(recipe_ids | pattern_ids | social_ids <= covered)
            anchors = re.findall(r'<a id="(sc-[^"]+)"', text)
            self.assertEqual(len(anchors), len(set(anchors)))
            self.assertEqual(len(anchors), len(coverage))
            self.assertEqual(len(anchors), len(re.findall(r"^### \d+\.", text, re.M)))
        self.assertEqual(
            re.findall(r"<!-- covers: (.*?) -->", readmes[0]),
            re.findall(r"<!-- covers: (.*?) -->", readmes[1]),
        )

    def test_readme_outputs_match_all_saved_example_receipts(self):
        expected = {}
        for filename in ("examples-2026-09-20.json", "scenario-smoke-2026-09-20.json"):
            receipt = json.loads((ROOT / "evals/results" / filename).read_text())
            for result in receipt["results"]:
                expected[f"{filename}#{result['example']}"] = {
                    question: {key: value for key, value in decision.items() if key != "levels"}
                    for question, decision in result["decisions"].items()
                }
        for filename in ("README.md", "README.zh.md"):
            text = (ROOT / filename).read_text()
            shown = re.findall(
                r"<!-- receipt: (.*?) -->\s*```json\n(.*?)\n```", text, re.S
            )
            self.assertEqual(len(shown), len(expected))
            self.assertEqual({key for key, _ in shown}, set(expected))
            for key, output in shown:
                with self.subTest(readme=filename, receipt=key):
                    self.assertEqual(json.loads(output), expected[key])


if __name__ == "__main__":
    unittest.main()
