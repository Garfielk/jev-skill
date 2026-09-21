import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import shutil
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/jev/scripts'))
import jev
spec = importlib.util.spec_from_file_location('triage_smoke', ROOT / 'skills/jev-triage/scripts/smoke_test.py')
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)
FIXTURE = ROOT / 'skills/jev-triage/assets/smoke-job.json'


class SmokeTests(unittest.TestCase):
    def setUp(self):
        self.job = json.loads(FIXTURE.read_text())

    def test_sampling_reproducible_bounded_and_metadata_excluded(self):
        plan = smoke.prepare(self.job, 8, 19)
        self.assertEqual(plan, smoke.prepare(self.job, 8, 19))
        self.assertEqual(len(plan['records']), 8)
        self.assertEqual(len({r['stratum'] for r in plan['records']}), 4)
        for row in plan['records']:
            left, right = smoke.requests(plan, row, 'openrouter', smoke.REFERENCE_MODEL)
            reference = json.loads(right['messages'][1]['content'])
            self.assertEqual(reference['state'], left['state'])
            self.assertEqual(reference['question'], left['questions']['category'])
            self.assertNotIn('gold', json.dumps(left))
            self.assertNotIn('stratum', json.dumps(left))
            self.assertNotIn('gold', json.dumps(right))
        self.assertEqual(smoke.prepare(self.job, 50)['sample_size'], 20)

    def test_cli_parameters_work_from_copied_skill_collection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('jev', 'jev-triage'):
                shutil.copytree(ROOT / 'skills' / name, root / name)
            command = [sys.executable, str(root/'jev-triage/scripts/smoke_test.py'),
                       str(root/'jev-triage/assets/smoke-job.json'), '--smoke-test', 'true',
                       '--sample-size', '7', '--seed', '12', '--timeout', '60']
            result = subprocess.run(command, capture_output=True, text=True, check=True, cwd=tmp)
            plan = json.loads(result.stdout)
            self.assertEqual(plan['plan']['sample_size'], 7)
            self.assertEqual(plan['plan']['seed'], 12)
            self.assertEqual(plan['mode'], 'dry_run')
            result = subprocess.run(command + ['--sample-size', '101'], capture_output=True, text=True, cwd=tmp)
            self.assertEqual(result.returncode, 1)

    def test_bad_records_and_parameters(self):
        for value in (0, 101, True, 1.1):
            with self.assertRaises(jev.JevError):
                smoke.prepare(self.job, value)
        for key, value in [('id', self.job['records'][1]['id']), ('gold', 'not-a-label'),
                           ('text', ''), ('stratum', [])]:
            bad = copy.deepcopy(self.job)
            bad['records'][0][key] = value
            with self.assertRaises(jev.JevError):
                smoke.prepare(bad)

    def test_dry_run_and_skip_do_not_call_models(self):
        with patch('jev.http_json', side_effect=AssertionError('network')), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(smoke.main([str(FIXTURE), '--sample-size', '3']), 0)
            self.assertFalse(json.loads(out.getvalue())['jev_called'])
        with patch('jev.http_json', side_effect=AssertionError('network')), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(smoke.main(['missing.json', '--smoke-test', 'false', '--live']), 2)
            self.assertEqual(json.loads(out.getvalue())['gate'], 'skipped')
            self.assertFalse(json.loads(out.getvalue())['bulk_authorized'])

    def test_gate_rejects_agreement_without_gold_or_errors(self):
        plan = smoke.prepare(self.job, 2)
        rows = [{'id': str(i), 'jev_label': 'bug', 'reference_label': 'bug', 'jev_review': False} for i in range(2)]
        self.assertEqual(smoke.summarize(plan, rows, .9, .05)['gate'], 'needs_review')
        self.assertIsNone(smoke.summarize(plan, rows, .9, .05)['metrics']['jev_accuracy'])
        for r in rows:
            r['gold'] = 'bug'
        report = smoke.summarize(plan, rows, .9, .05)
        self.assertEqual(report['gate'], 'sample_check_passed')
        self.assertFalse(report['bulk_authorized'])
        rows[0]['gold'] = 'billing'
        self.assertEqual(smoke.summarize(plan, rows, .9, .05)['gate'], 'needs_review')
        rows[0]['gold'] = 'bug'
        rows[0]['jev_review'] = True
        self.assertEqual(smoke.summarize(plan, rows, .9, .05)['gate'], 'needs_review')
        self.assertEqual(smoke.summarize(plan, rows[:1], .9, .05)['gate'], 'needs_review')

    def fake_call(self, url, payload, timeout):
        if url == jev.DECISIONS_URL or url == jev.TYPESAFE_URL:
            return {'model':payload['model'],'answers':{'category':{'type':'choice','choice':'bug','confidence':1,
                'probabilities':{k: int(k == 'bug') for k in self.job['criteria']}}},'usage':{'cost': .0001}}
        return {'model':payload['model'],'choices':[{'finish_reason':'stop','message':{'content':'{"label":"bug"}'}}],
                'usage':{'cost':.0002}}

    def test_live_mock_records_both_raw_arms_and_does_not_overwrite(self):
        plan = smoke.prepare(self.job, 2)
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'OPENROUTER_API_KEY':'test-secret'}, clear=True), \
                patch('jev.http_json', side_effect=self.fake_call) as network:
            output = Path(tmp) / 'run'
            report = smoke.run(plan, output)
            self.assertEqual(network.call_count, 4)
            self.assertEqual(report['metrics']['valid_pairs'], 2)
            self.assertEqual(report['usage']['reference']['reported_cost_usd'], .0004)
            self.assertEqual(len((output/'receipts.jsonl').read_text().splitlines()), 4)
            self.assertNotIn('test-secret', ''.join(p.read_text() for p in output.iterdir()))
            with self.assertRaises(FileExistsError):
                smoke.run(plan, output)
            self.assertEqual(network.call_count, 4)

    def test_missing_usage_is_unknown_not_zero(self):
        def call(url, payload, timeout):
            result = self.fake_call(url, payload, timeout)
            result['usage'] = None
            return result
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'OPENROUTER_API_KEY':'secret'}, clear=True), \
                patch('jev.http_json', side_effect=call):
            report = smoke.run(smoke.prepare(self.job, 1), Path(tmp)/'run')
            for usage in report['usage'].values():
                self.assertIsNone(usage['reported_cost_usd'])
                self.assertEqual(usage['cost_unknown_calls'], 1)

    def test_missing_native_key_fails_before_any_call(self):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY':'secret'}, clear=True), patch('jev.http_json') as network:
            with self.assertRaises(jev.JevError):
                smoke.run(smoke.prepare(self.job, 2), 'unused', provider='typesafe')
            network.assert_not_called()

    def test_error_stops_and_preserves_receipt_without_retry_or_secret(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'OPENROUTER_API_KEY':'secret'}, clear=True), \
                patch('jev.http_json', side_effect=jev.JevError('secret', http_status=403)) as network:
            output = Path(tmp)/'run'
            result = smoke.run(smoke.prepare(self.job, 5), output)
            self.assertEqual(network.call_count, 1)
            self.assertEqual(result['gate'], 'needs_review')
            self.assertEqual(result['metrics']['valid_pairs'], 0)
            self.assertIsNone(result['metrics']['jev_accuracy'])
            self.assertEqual(result['metrics']['jev_scored_gold_records'], 0)
            self.assertNotIn('secret', (output/'receipts.jsonl').read_text())
            self.assertIsNone(result['usage']['jev']['reported_cost_usd'])

    def test_invalid_reference_label_or_truncation_stops(self):
        for content, reason in [('{"label":"made-up"}', 'stop'), ('{"label":"bug"}', 'length'), ('not json', 'stop')]:
            def call(url, payload, timeout):
                result = self.fake_call(url, payload, timeout)
                if url == smoke.CHAT_URL:
                    result['choices'][0] = {'finish_reason':reason,'message':{'content':content}}
                return result
            with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'OPENROUTER_API_KEY':'secret'}, clear=True), \
                    patch('jev.http_json', side_effect=call) as network:
                report = smoke.run(smoke.prepare(self.job, 4), Path(tmp)/'run')
                self.assertEqual(network.call_count, 2)
                self.assertEqual(report['gate'], 'needs_review')
                self.assertEqual(report['metrics']['valid_pairs'], 0)

if __name__ == '__main__':
    unittest.main()
