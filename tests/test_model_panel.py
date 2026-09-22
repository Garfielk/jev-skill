import json
from pathlib import Path
import tempfile
import unittest

from evals import model_panel as panel


class ModelPanelTests(unittest.TestCase):
    def test_offline_prepare_keeps_gold_out_of_both_transports(self):
        samples = [{'id': 'one', 'task': 'demo', 'input': 'Pick a label',
                    'criteria': {'A': 'one', 'B': 'two'}, 'target': 'A'}]
        models = [{'id': 'test/jev', 'kind': 'jev', 'options': {}},
                  {'id': 'test/chat', 'kind': 'chat', 'options': {'max_tokens': 512}}]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            plan = panel.prepare(root, samples, models, {'dataset': 'unit fixture'})
            for model in models:
                before = panel.payload_for(samples[0], model, plan)
                samples[0]['target'] = 'SECRET_GOLD'
                self.assertEqual(before, panel.payload_for(samples[0], model, plan))
                self.assertNotIn('SECRET_GOLD', json.dumps(before))
            self.assertFalse((root / 'events.jsonl').exists())

    def test_live_run_retains_errors_and_offline_replay_rejects_tampering(self):
        class Client:
            def helper(self, payload):
                return {'answers': {'answer': {'type': 'choice', 'choice': 'A',
                        'probabilities': {'A': .9, 'B': .1}, 'confidence': .8}}, 'usage': {'cost': .001}}

            def base(self, payload):
                return {'choices': [{'finish_reason': 'stop', 'message': {'content': '{"choice":"Z"}'}}], 'usage': {'cost': .002}}
        samples = [{'id': 'one', 'task': 'demo', 'input': 'Pick a label',
                    'criteria': {'A': 'one', 'B': 'two'}, 'target': 'A'}]
        models = [{'id': 'test/jev', 'kind': 'jev', 'options': {}},
                  {'id': 'test/chat', 'kind': 'chat', 'options': {}}]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            panel.prepare(root, samples, models, {})
            result = panel.run(root, client=Client())
            self.assertEqual(result['models']['test/jev']['correct'], 1)
            self.assertEqual(result['models']['test/jev']['by_task']['demo']['correct'], 1)
            self.assertEqual(result['models']['test/chat']['by_task']['demo']['correct'], 0)
            self.assertEqual(result['models']['test/chat']['errors'], 1)
            self.assertEqual(result['models']['test/chat']['usage']['reported_cost_usd'], .002)
            self.assertEqual(panel.summarize_run(root), result)
            with self.assertRaises(FileExistsError):
                panel.run(root, client=Client())
            events = (root / 'events.jsonl').read_text().splitlines()
            row = json.loads(events[0]);row['request']['model'] = 'tampered'
            events[0] = json.dumps(row)
            (root / 'events.jsonl').write_text('\n'.join(events)+'\n')
            with self.assertRaisesRegex(ValueError, 'request'):
                panel.summarize_run(root)

    def test_changed_manifest_is_rejected_before_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'run'
            panel.prepare(root, [{'id':'one','task':'demo','input':'Choose','criteria':{'A':'one'},'target':'A'}],
                          [{'id':'test/chat','kind':'chat','options':{}}], {})
            path = root / 'manifest.json'
            plan = json.loads(path.read_text());plan['models'][0]['id'] = 'changed'
            path.write_text(json.dumps(plan))
            with self.assertRaisesRegex(ValueError, 'Manifest'):
                panel.run(root, client=object())
            self.assertFalse((root / 'events.jsonl').exists())

    def test_chat_schema_constrains_choice_to_supplied_labels(self):
        sample = {'id':'one','task':'demo','input':'Pick','criteria':{'A':'blue','B':'seven'},'target':'A'}
        request = panel.payload_for(sample, {'id':'test/chat','kind':'chat','options':{}}, {'instructions':'Select'})
        schema = request['response_format']['json_schema']['schema']
        self.assertEqual(schema['properties']['choice']['enum'], ['A', 'B'])
        self.assertEqual(schema['required'], ['choice'])
        self.assertFalse(schema['additionalProperties'])
