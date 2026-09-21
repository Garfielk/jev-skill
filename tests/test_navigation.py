"""Reader and installed-skill navigation contracts."""
from pathlib import Path
import re
import json
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {'jev', 'jev-triage', 'jev-documents', 'jev-eval', 'jev-act'}


class NavigationTests(unittest.TestCase):
    def test_all_scenarios_have_a_primary_skill_and_reverse_link(self):
        mappings = []
        for filename in ('README.md', 'README.zh.md'):
            text = (ROOT / filename).read_text()
            parts = re.findall(r'<a id="(sc-[^"]+)"></a>(.*?)(?=<a id="|\Z)', text, re.S)
            self.assertEqual(len(parts), 108)
            mapping = []
            for anchor, part in parts:
                match = re.search(r'<!-- skill: (jev[\w-]*) -->', part)
                self.assertIsNotNone(match, anchor)
                skill = match[1]
                self.assertIn(skill, SKILLS)
                self.assertIn(f'skills/{skill}/SKILL.md', part)
                reverse = (ROOT / 'skills' / skill / 'references/scenarios.md').read_text()
                self.assertIn('#' + anchor + ')', reverse)
                mapping.append((anchor, skill))
            mappings.append(mapping)
        self.assertEqual(*mappings)

    def test_readme_has_three_main_sections_and_keeps_full_examples(self):
        for filename, headings in [('README.md', ['Projects', 'Skills', 'Examples']),
                                   ('README.zh.md', ['项目', '技能', '用法'])]:
            text = (ROOT / filename).read_text()
            self.assertEqual(re.findall(r'^## (.+)$', text, re.M), headings)
            self.assertEqual(len(re.findall(r'<!-- request:', text)), 14)
            self.assertEqual(len(re.findall(r'<!-- receipt:', text)), 14)
            self.assertEqual(len(re.findall(r'^#### \d+\.', text, re.M)), 108)

    def test_project_intake_is_visible_once_in_each_project_list(self):
        record = json.loads((ROOT / 'evals/results/project-intake-2026-09-22.json').read_text())
        for filename in ('README.md', 'README.zh.md'):
            section = (ROOT / filename).read_text().split('<a id="projects"></a>')[1].split('<a id="skills"></a>')[0]
            for project in record['projects']:
                self.assertEqual(section.count('](' + project['url'] + ')'), 1, project['id'])
                self.assertEqual(len(project['revision']), 40)
                self.assertTrue(project['decision'])

    def test_demo_previews_share_a_canvas_and_keep_animation(self):
        for filename in ('README.md', 'README.zh.md'):
            text = (ROOT / filename).read_text().split('<a id="showcase"></a>')[1].split('</table>')[0]
            paths = re.findall(r'<img src="([^"]+)"', text)
            self.assertEqual(len(paths), 6)
            self.assertTrue(paths[0].endswith('.gif'))
            for path in paths:
                data = (ROOT / path).read_bytes()
                if path.endswith('.gif'):
                    self.assertIn(data[:6], (b'GIF87a', b'GIF89a'))
                    size = struct.unpack('<HH', data[6:10])
                else:
                    self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
                    size = struct.unpack('>II', data[16:24])
                self.assertEqual(size, (800, 450), path)

    def test_short_entries_link_to_local_examples_without_loading_readme(self):
        for skill in SKILLS:
            entry = (ROOT / 'skills' / skill / 'SKILL.md').read_text()
            self.assertIn('references/scenarios.md', entry)
            paths = re.findall(r'\]\((assets/[^)]+)\)', entry)
            self.assertTrue(paths, skill)
            for path in paths:
                self.assertTrue((ROOT / 'skills' / skill / path).is_file())


if __name__ == '__main__':
    unittest.main()
