import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from evals import agent_pilot as pilot

JOB = {'criteria': {'billing':'Payment issue', 'bug':'Product failure', 'unknown':'Insufficient evidence'},
       'context': {'policy':'Use current unresolved request'}, 'records':[
           {'id':'B','text':'Duplicate charge','context':{'thread':'Login already fixed'},'gold':'billing'},
           {'id':'A','text':'App crashes','gold':'bug'}]}

def reply(url, payload, timeout=30):
    if 'questions' in payload:
        label = 'billing' if payload['state']['record']['id'] == 'B' else 'bug'
        return {'model':'resolved-jev','answers':{'category':{'type':'choice','choice':label,
                'confidence':1,'probabilities':{k:int(k==label) for k in JOB['criteria']}}},'usage':{'cost':0.01}}
    data = json.loads(payload['messages'][-1]['content'])
    label = 'billing' if data['state']['record']['id'] == 'B' else 'bug'
    return {'model':'resolved-reference','choices':[{'finish_reason':'stop','message':{'content':json.dumps({'label':label})}}],
            'usage':{'cost':0.02}}

class AgentPilotTests(unittest.TestCase):
    def test_dry_run_never_calls_or_authorizes_bulk(self):
        with tempfile.TemporaryDirectory() as tmp, patch('jev.urllib.request.build_opener') as http:
            result=pilot.run(JOB, Path(tmp)/'run', sample_size=2, live=False)
            self.assertFalse(result['bulk_authorized'])
            self.assertEqual(result['mode'],'dry_run')
            http.assert_not_called()

    def test_paired_outputs_ids_evidence_gold_and_costs(self):
        received=[]
        def transport(url,payload,timeout=30):
            received.append(payload)
            if 'questions' in payload:
                time.sleep(0.01)
            return reply(url,payload,timeout)
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ,{'OPENROUTER_API_KEY':'dummy'}), \
                patch('jev.http_json',side_effect=transport):
            out=Path(tmp)/'run'
            report=pilot.run(JOB,out,sample_size=2,live=True,concurrency=2)
            self.assertEqual(report['metrics']['valid_pairs'],2)
            self.assertEqual(report['metrics']['agreement'],1)
            self.assertEqual(report['metrics']['jev_accuracy'],1)
            self.assertFalse(report['bulk_authorized'])
            receipts=[json.loads(l) for l in (out/'receipts.jsonl').read_text().splitlines()]
            self.assertEqual({(r['id'],r['arm']) for r in receipts},{('A','jev'),('A','reference'),('B','jev'),('B','reference')})
            for id in ('A','B'):
                j=next(r['request'] for r in receipts if r['id']==id and r['arm']=='jev')
                c=next(r['request'] for r in receipts if r['id']==id and r['arm']=='reference')
                content=json.loads(c['messages'][-1]['content'])
                self.assertEqual(content,{'state':j['state'],'question':j['questions']['category']})
                self.assertNotIn('gold',j['state']['record'])
                self.assertNotIn('stratum',j['state']['record'])
            self.assertEqual(report['usage']['jev']['known_cost_subtotal_usd'],0.02)
            self.assertEqual(report['usage']['reference']['known_cost_subtotal_usd'],0.04)

    def test_bad_output_stops_new_work_retains_inflight_receipts(self):
        job={**JOB,'records':JOB['records']+[{'id':'C','text':'Third','gold':'bug'}]}
        def broken(url,payload,timeout=30):
            if 'questions' not in payload:
                return {'choices':[{'finish_reason':'length','message':{'content':'{"label":"billing"}'}}]}
            return reply(url,payload,timeout)
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ,{'OPENROUTER_API_KEY':'dummy'}), \
                patch('jev.http_json',side_effect=broken):
            out=Path(tmp)/'run'
            report=pilot.run(job,out,sample_size=3,concurrency=2,live=True)
            self.assertEqual(report['gate'],'needs_review')
            self.assertFalse(report['bulk_authorized'])
            receipts=[json.loads(l) for l in (out/'receipts.jsonl').read_text().splitlines()]
            self.assertEqual(len(receipts),2)
            self.assertTrue(any('error' in r for r in receipts))
            self.assertEqual(report['metrics']['valid_pairs'],0)

    def test_no_gold_means_no_accuracy_or_quality_pass(self):
        job={**JOB,'records':[{k:v for k,v in r.items() if k!='gold'} for r in JOB['records']]}
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ,{'OPENROUTER_API_KEY':'dummy'}), \
                patch('jev.http_json',side_effect=reply):
            report=pilot.run(job,Path(tmp)/'run',sample_size=2,live=True)
            self.assertIsNone(report['metrics']['jev_accuracy'])
            self.assertEqual(report['gate'],'needs_review')

    def test_missing_key_duplicates_and_existing_output_make_no_calls(self):
        with tempfile.TemporaryDirectory() as tmp, patch('jev.http_json') as http:
            with patch.dict(os.environ,{},clear=True), self.assertRaises(ValueError):
                pilot.run(JOB,Path(tmp)/'missing',sample_size=2,live=True)
            with patch.dict(os.environ,{'OPENROUTER_API_KEY':'dummy'}):
                with self.assertRaises(ValueError):
                    pilot.run({**JOB,'records':[JOB['records'][0]]*2},Path(tmp)/'dupe',live=True)
                with self.assertRaises((ValueError,FileExistsError)):
                    pilot.run(JOB,Path(tmp),sample_size=2,live=True)
            http.assert_not_called()

    def test_global_concurrency_and_one_worker_limit(self):
        for limit in (1,2,3):
            active=0
            peak=0
            lock=threading.Lock()
            def slow(url,payload,timeout=30):
                nonlocal active,peak
                with lock:
                    active+=1
                    peak=max(peak,active)
                time.sleep(0.02)
                result=reply(url,payload,timeout)
                with lock:
                    active-=1
                return result
            with self.subTest(limit=limit), tempfile.TemporaryDirectory() as tmp, \
                    patch.dict(os.environ,{'OPENROUTER_API_KEY':'dummy'}),patch('jev.http_json',side_effect=slow):
                report=pilot.run(JOB,Path(tmp)/'run',sample_size=2,concurrency=limit,live=True)
                self.assertEqual(report['metrics']['valid_pairs'],2)
                self.assertLessEqual(peak,limit)
                if limit>1:
                    self.assertGreater(peak,1)

    def test_safe_timeout_and_unknown_costs_remain_visible(self):
        def fail(url,payload,timeout=30):
            if 'questions' in payload:
                raise pilot.jev.JevError('private detail',error_kind='timeout',phase='response_body',http_status=200)
            return reply(url,payload,timeout)
        with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'OPENROUTER_API_KEY':'dummy'}), \
                patch('jev.http_json',side_effect=fail):
            out=Path(tmp)/'run'
            report=pilot.run(JOB,out,sample_size=2,concurrency=2,live=True)
            self.assertEqual(report['metrics']['attempted_records'],1)
            self.assertEqual(report['metrics']['valid_pairs'],0)
            self.assertEqual(report['metrics']['reference_scored_gold_records'],1)
            self.assertEqual(report['usage']['jev']['calls'],1)
            self.assertIsNone(report['usage']['jev']['reported_cost_usd'])
            self.assertEqual(report['usage']['jev']['cost_unknown_calls'],1)
            text=(out/'receipts.jsonl').read_text()
            self.assertNotIn('private detail',text)
            self.assertNotIn('dummy',text)
            r=next(json.loads(l) for l in text.splitlines() if json.loads(l)['arm']=='jev')
            self.assertEqual(r['error']['phase'],'response_body')
            self.assertEqual(r['error']['http_status'],200)
            self.assertIn('request',r)

    def test_invalid_reference_fields_keep_raw_response_and_cannot_pass(self):
        for content,reason in [('[]','stop'),('{"label":[]}','stop'),('{"label":"other"}','stop'),
                               ('{"label":"bug","extra":1}','stop'),('{"label":"bug"}','length'),
                               ('{"label":"bug","label":"billing"}','stop')]:
            def bad(url,payload,timeout=30):
                if 'questions' in payload:
                    return reply(url,payload,timeout)
                return {'choices':[{'finish_reason':reason,'message':{'content':content}}]}
            with self.subTest(content=content,reason=reason),tempfile.TemporaryDirectory() as tmp, \
                    patch.dict(os.environ,{'OPENROUTER_API_KEY':'dummy'}),patch('jev.http_json',side_effect=bad):
                out=Path(tmp)/'run'
                report=pilot.run(JOB,out,sample_size=2,concurrency=2,live=True)
                self.assertEqual(report['gate'],'needs_review')
                self.assertEqual(report['metrics']['valid_pairs'],0)
                r=next(json.loads(l) for l in (out/'receipts.jsonl').read_text().splitlines() if json.loads(l)['arm']=='reference')
                self.assertIn('response',r)
                self.assertIn('error',r)

    def test_invalid_parameters_stop_before_spending(self):
        with tempfile.TemporaryDirectory() as tmp,patch('jev.http_json') as http:
            for kwargs in ({'concurrency':True},{'sample_size':True},{'timeout':float('nan')},
                           {'live':'false'},{'reference_model':''},{'sample_size':0}):
                with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                    pilot.run(JOB,Path(tmp)/'invalid',**kwargs)
            http.assert_not_called()
