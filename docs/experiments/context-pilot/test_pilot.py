"""Offline checks of the frozen pilot artifacts, not additional model calls."""
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent


class PilotArtifacts(unittest.TestCase):
    def test_twenty_paired_cases(self):
        cases = json.loads((HERE / 'cases.json').read_text())
        self.assertEqual(len(cases), 20)
        self.assertEqual(len({c['id'] for c in cases}), 20)
        self.assertEqual(len(list((HERE / 'receipts').glob('*.json'))), 40)

    def test_receipts_match_requests_without_gold(self):
        for path in (HERE / 'receipts').glob('*.json'):
            receipt = json.loads(path.read_text())
            data = (HERE / 'requests' / path.name).read_bytes()
            self.assertEqual(receipt['request_sha256'], hashlib.sha256(data).hexdigest())
            self.assertEqual(set(json.loads(data)['state']), {'task', 'claim', 'policy', 'evidence'})
            self.assertTrue(receipt['result']['jev_called'])
            self.assertIn(receipt['exit_code'], (0, 2))

    def test_scores_come_from_receipts_and_gold(self):
        cases = {c['id']: c for c in json.loads((HERE / 'cases.json').read_text())}
        scores = json.loads((HERE / 'scores.json').read_text())
        self.assertEqual(len(scores), 40)
        for row in scores:
            receipt = json.loads((HERE / 'receipts' / f"{row['id']}-{row['condition']}.json").read_text())
            self.assertEqual(row['value'], receipt['result']['decisions']['verdict']['value'])
            self.assertEqual(row['gold'], cases[row['id']][f"gold_{row['condition']}"])
            self.assertEqual(row['correct'], row['value'] == row['gold'])

    def test_report_totals(self):
        rows = json.loads((HERE / 'scores.json').read_text())
        for condition, correct, unknown, selected in [('short', 20, 15, 5), ('full', 19, 4, 15)]:
            group = [r for r in rows if r['condition'] == condition]
            self.assertEqual(sum(r['correct'] for r in group), correct)
            self.assertEqual(sum(r['value'] == 'unknown' for r in group), unknown)
            self.assertEqual(sum(r['status'] == 'selected' for r in group), selected)


if __name__ == '__main__':
    unittest.main()
