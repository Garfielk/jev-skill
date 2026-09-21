"""Conversion examples at the installed-script and CLI request seams."""
import importlib.util
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/jev/scripts'))
import jev


class PromptConversionTests(unittest.TestCase):
    def test_example_dry_run_needs_no_key_and_keeps_rules_out_of_state(self):
        spec = importlib.util.spec_from_file_location(
            'prompt_example', ROOT / 'skills/jev/assets/prompt_to_jev.py')
        example = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(example)
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), \
                patch('urllib.request.build_opener', side_effect=AssertionError('network')), \
                contextlib.redirect_stdout(output):
            self.assertEqual(example.main(['--dry-run']), 0)
        request = json.loads(output.getvalue())
        self.assertEqual(set(request['questions']), {'team', 'refund', 'impact'})
        self.assertEqual({q['type'] for q in request['questions'].values()},
                         {'choice', 'noul', 'score'})
        self.assertEqual(set(request['state']), {'ticket'})
        self.assertEqual(set(request['state']['ticket']), {'text'})
        self.assertEqual(request['questions']['team']['criteria']['other'],
                         'None fits, or the message is unclear.')
        jev.validate_request(request)

    def test_calling_example_handles_false_and_uncertain_refund(self):
        spec = importlib.util.spec_from_file_location(
            'prompt_example', ROOT / 'skills/jev/assets/prompt_to_jev.py')
        example = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(example)
        for probability, queue, status in [(0.97, 'refund_review', 0),
                                           (0.02, 'normal', 0),
                                           (0.5, 'human_review', 2)]:
            response = {'answers': {
                'team': {'type': 'choice', 'choice': 'billing',
                         'probabilities': {'billing': 1, 'access': 0, 'other': 0}, 'confidence': 1},
                'refund': {'type': 'noul', 'noul': probability},
                'impact': {'type': 'score', 'score': 0,
                           'legend': {'0': 'Can still use the service; no work is blocked.',
                                      '1': 'Some work is disrupted, but a workaround exists.',
                                      '2': 'Cannot use the service to do their work.'},
                           'probabilities': {'0': 1, '1': 0, '2': 0}, 'confidence': 1}}}
            output = io.StringIO()
            with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-secret'}, clear=True), \
                    patch('urllib.request.build_opener') as opener, \
                    contextlib.redirect_stdout(output):
                opener.return_value.open.return_value.__enter__.return_value.read.return_value = json.dumps(response).encode()
                self.assertEqual(example.main([]), status)
            self.assertEqual(json.loads(output.getvalue())['proposed_queue'], queue)
            self.assertNotIn('test-secret', output.getvalue())

    def test_typesafe_example_uses_native_model_for_dry_run_and_transport(self):
        spec = importlib.util.spec_from_file_location(
            'prompt_example', ROOT / 'skills/jev/assets/prompt_to_jev.py')
        example = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(example)
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), \
                patch('urllib.request.build_opener', side_effect=AssertionError('network')), \
                contextlib.redirect_stdout(output):
            self.assertEqual(example.main(['--provider', 'typesafe', '--dry-run']), 0)
        self.assertEqual(json.loads(output.getvalue())['model'], 'jev-1.13.0')
        with patch.dict(os.environ, {'TYPESAFE_API_KEY': 'native-test-secret'}, clear=True), \
                patch('urllib.request.build_opener') as opener:
            # Stop at the external transport; do not mock the request-building code.
            opener.return_value.open.side_effect = RuntimeError('transport reached')
            with self.assertRaisesRegex(RuntimeError, 'transport reached'):
                example.main(['--provider', 'typesafe'])
            sent = opener.return_value.open.call_args.args[0]
            self.assertEqual(sent.full_url, 'https://api.typesafe.ai/v1/systemone')
            self.assertEqual(sent.get_header('Authorization'), 'Bearer native-test-secret')
            self.assertEqual(json.loads(sent.data)['model'], 'jev-1.13.0')

    def test_worked_conversions_validate_without_inventing_missing_evidence(self):
        assets = ROOT / 'skills/jev/assets'
        cases = {c['id']: c for c in json.loads(
            (assets / 'prompt-conversion-cases.json').read_text())}
        missing = cases['missing']['after']
        self.assertIsNone(missing['request'])
        self.assertEqual(missing['next_step'], 'collect-or-review')
        self.assertEqual(missing['missing_fields'], ['ticket', 'amount'])
        dependent = cases['dependent']['after']
        first, second = dependent['requests']
        self.assertNotIn('document_text', first['state'])
        self.assertEqual(second['state']['document_text'], dependent['new_observation']['text'])
        self.assertEqual(second['state']['document_id'], dependent['new_observation']['document_id'])
        self.assertIn('unknown', second['questions']['support']['criteria'])
        requests = [first, second]
        for name in ('labels', 'rubric', 'rules', 'generation'):
            requests.append(json.loads((assets / cases[name]['after']['request_file']).read_text()))
        for request in requests:
            output = io.StringIO()
            with patch.dict(os.environ, {}, clear=True), \
                    patch('urllib.request.build_opener', side_effect=AssertionError('network')), \
                    patch('sys.stdin', io.StringIO(json.dumps(request))), \
                    contextlib.redirect_stdout(output):
                self.assertEqual(jev.main(['decide', '-', '--dry-run']), 0)
            self.assertEqual(json.loads(output.getvalue()), request)

    def test_conversion_fixtures_have_expected_roles(self):
        cases = json.loads((ROOT / 'skills/jev/assets/prompt-conversion-cases.json').read_text())
        self.assertEqual({c['id'] for c in cases},
                         {'labels', 'rubric', 'rules', 'generation', 'missing', 'dependent'})
        for case in cases:
            self.assertTrue(case['prompt'])
            self.assertTrue(case['expected'])
        by_id = {c['id']: c for c in cases}
        self.assertEqual(by_id['rules']['expected']['amount_and_age'], 'code')
        self.assertEqual(by_id['generation']['expected']['reply'], 'keep-llm')
        self.assertEqual(by_id['dependent']['expected']['read_selected_document'], 'next-step')


if __name__ == '__main__':
    unittest.main()
