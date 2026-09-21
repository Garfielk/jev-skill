from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SmokeGuidanceTests(unittest.TestCase):
    def test_bulk_entry_exposes_agent_authored_pilot_without_new_skill(self):
        entry = (ROOT/'skills/jev-triage/SKILL.md').read_text()
        guide = (ROOT/'skills/jev-triage/references/smoke-test.md').read_text()
        self.assertIn('smoke_test=true', entry)
        self.assertIn('smoke_test=false', entry)
        self.assertIn('references/smoke-test.md', entry)
        self.assertIn('host agent to write task-specific code', entry)
        self.assertIn('not flags accepted by `jev-decide`', guide)
        self.assertFalse((ROOT/'skills/jev-triage/scripts/smoke_test.py').exists())
        for name in ('jev', 'jev-triage', 'jev-documents', 'jev-eval', 'jev-act'):
            self.assertIn(f'`{name}`', guide)
            self.assertTrue((ROOT/'skills'/name/'SKILL.md').is_file())
