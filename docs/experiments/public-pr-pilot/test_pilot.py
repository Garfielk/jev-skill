"""Offline checks of the public PR sample and actual Jev receipts."""
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent


class PublicPRPilot(unittest.TestCase):
    def test_sample_and_label_balance(self):
        cases = json.loads((HERE / 'manifest.json').read_text())['cases']
        self.assertEqual(len(cases), 20)
        self.assertEqual(len({c['url'] for c in cases}), 20)
        self.assertEqual(sum(c['expected'] == 'substantive' for c in cases), 10)
        self.assertEqual(sum(c['expected'] == 'routine_maintenance' for c in cases), 10)

    def test_hashes_and_evidence_boundary(self):
        for case in json.loads((HERE / 'manifest.json').read_text())['cases']:
            raw = (HERE / 'requests' / f"{case['id']}.json").read_bytes()
            request = json.loads(raw)
            receipt = json.loads((HERE / 'receipts' / f"{case['id']}.json").read_text())
            self.assertEqual(hashlib.sha256(raw).hexdigest(), case['request_sha256'])
            self.assertEqual(receipt['request_sha256'], case['request_sha256'])
            self.assertEqual(hashlib.sha256(request['state']['diff'].encode()).hexdigest(), case['diff_sha256'])
            self.assertEqual(set(request['state']), {'task', 'project', 'title', 'description', 'technical_discussion', 'diff', 'scope'})
            self.assertTrue(receipt['result']['jev_called'])

    def test_scores_and_review_case(self):
        cases = {c['id']: c for c in json.loads((HERE / 'manifest.json').read_text())['cases']}
        rows = json.loads((HERE / 'scores.json').read_text())
        self.assertEqual(len(rows), 20)
        for row in rows:
            receipt = json.loads((HERE / 'receipts' / f"{row['id']}.json").read_text())
            self.assertEqual(row['expected'], cases[row['id']]['expected'])
            self.assertEqual(row['actual'], receipt['result']['decisions']['value']['value'])
            self.assertEqual(row['agreement'], row['expected'] == row['actual'])
        self.assertEqual(sum(r['agreement'] for r in rows), 20)
        self.assertEqual([r['id'] for r in rows if r['status'] == 'needs_review'], ['pallets-flask-5945'])


if __name__ == '__main__':
    unittest.main()
