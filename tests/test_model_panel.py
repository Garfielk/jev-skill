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

    def test_response_error_conflict_is_rejected(self):
        class Client:
            def base(self, payload):
                return {'choices':[{'finish_reason':'stop','message':{'content':'{"choice":"A"}'}}]}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run'
            panel.prepare(root,[{'id':'1','task':'demo','input':'x','criteria':{'A':'a'},'target':'A'}],
                          [{'id':'test/chat','kind':'chat','options':{}}],{})
            panel.run(root,client=Client())
            p=root/'events.jsonl'; event=json.loads(p.read_text());event['error']={'type':'ValueError'}
            p.write_text(json.dumps(event)+'\n')
            with self.assertRaisesRegex(ValueError,'error'):
                panel.summarize_run(root)

    def test_provider_override_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                panel.prepare(Path(tmp)/'r',[{'id':'1','task':'demo','input':'x','criteria':{'A':'a'},'target':'A'}],
                              [{'id':'test/chat','kind':'chat','options':{'provider':{'only':['example']}}}],{})

    def test_fatal_stops_after_bounded_wave_and_retains_safe_diagnostics(self):
        class Client:
            def base(self,payload):
                raise panel.jev.JevError('must not log this',http_status=403,error_kind='http',phase='connect_or_headers')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run'
            panel.prepare(root,[{'id':str(i),'task':'demo','input':'x','criteria':{'A':'a'},'target':'A'} for i in range(9)],
                          [{'id':'test/chat','kind':'chat','options':{}}],{})
            with self.assertRaisesRegex(ValueError,'Fatal'): panel.run(root,client=Client())
            text=(root/'events.jsonl').read_text();rows=[json.loads(s) for s in text.splitlines()]
            self.assertEqual(len(rows),4)
            self.assertEqual(rows[0]['error']['error_kind'],'http')
            self.assertNotIn('must not log',text)
            with self.assertRaisesRegex(ValueError,'Aborted'): panel.summarize_run(root)

    def test_missing_key_stops_before_live_artifacts(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run'
            panel.prepare(root,[dict(id='1',task='t',input='x',criteria={'A':'a'},target='A')],
                          [dict(id='test/chat',kind='chat',options={})],{})
            with patch.dict('os.environ',{},clear=True):
                with self.assertRaisesRegex(ValueError,'OPENROUTER_API_KEY'): panel.run(root)
            self.assertFalse((root/'events.jsonl').exists())

    def test_timeout_is_retained_without_retry(self):
        class Client:
            calls=0
            def base(self,payload):
                self.calls+=1
                raise panel.jev.JevError('private details',error_kind='timeout',phase='response_body')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run';client=Client()
            panel.prepare(root,[dict(id='1',task='t',input='x',criteria={'A':'a'},target='A')],
                          [dict(id='test/chat',kind='chat',options={})],{})
            result=panel.run(root,client)
            self.assertEqual(client.calls,1)
            self.assertEqual(result['models']['test/chat']['errors'],1)
            self.assertEqual(json.loads((root/'events.jsonl').read_text())['error']['phase'],'response_body')
