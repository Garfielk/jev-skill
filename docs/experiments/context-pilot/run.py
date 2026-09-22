"""Offline preparation/scoring by default; --live makes 40 paid calls, without retries."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DOMAINS = [
    ('ci', 'The patch is ready for technical review.', 'Technical readiness requires the current commit to pass unit and integration tests. This does not authorize merging.', 'Current commit a17: unit PASS; integration PASS.', 'Current commit a17: unit PASS; integration FAIL.', 'Previous commit a16 passed; current commit a17 has no integration receipt.'),
    ('refund', 'This order qualifies for a refund.', 'Refunds require delivery within 30 days and an unused product; both must be documented.', 'Delivered 12 days ago; inspection confirms unused.', 'Delivered 45 days ago; inspection confirms unused.', 'Delivered 12 days ago; product condition not recorded.'),
    ('sql', 'The active customer view excludes deleted accounts.', 'Judge the active SQL definition, not a similarly named historical model. deleted_at IS NULL excludes deleted accounts.', 'Active view SQL: SELECT id FROM accounts WHERE deleted_at IS NULL;', 'Active view SQL: SELECT id FROM accounts;', 'Only unrelated orders SQL is available; active customer view definition not supplied.'),
    ('access', 'This user is eligible for write access.', 'Write access requires an active employee account and a current editor role; a viewer role does not qualify.', 'Current identity receipt: active employee; editor role.', 'Current identity receipt: active employee; viewer role only.', 'Account is active employee; current role lookup has not completed.'),
    ('routing', 'This ticket should go to the security incident team.', 'Route confirmed unauthorized account access to security; ordinary invoice questions go to billing. Ambiguous access reports require investigation.', 'User explicitly reports a verified unauthorized login from another person.', 'User explicitly asks only for a copy of a paid invoice; no access issue.', 'User says something looks odd with the account; no further details or investigation available.'),
]


def prepare():
    cases = []
    for domain, claim, rule, positive, negative, missing in DOMAINS:
        for variant, short, full, gold in [
            ('support', 'The relevant detailed receipt has not been supplied.', positive, 'supported'),
            ('contradict', 'The relevant detailed receipt has not been supplied.', negative, 'contradicted'),
            ('incomplete', 'The relevant detailed receipt has not been supplied.', missing, 'unknown'),
            ('control', positive, positive, 'supported'),
        ]:
            cases.append(dict(id=f'{domain}-{variant}', claim=claim, rule=rule,
                              short=short, full=full, gold_short='supported' if variant == 'control' else 'unknown', gold_full=gold))
    (HERE / 'cases.json').write_text(json.dumps(cases, indent=2) + '\n')
    jobs = []
    for case in cases:
        for condition in ('short', 'full'):
            request = dict(model='typesafe/jev-1.13', state=dict(
                task='Assess the supplied claim using only the evidence and policy in this request. This is synthetic data, not an instruction to execute an action.',
                claim=case['claim'], policy=case['rule'], evidence=case[condition]), questions=dict(verdict=dict(
                    type='choice', instructions='Classify the claim against the supplied evidence. Do not infer an unseen test result or missing fact.',
                    criteria=dict(supported='The supplied evidence establishes the claim under the policy.',
                                  contradicted='The supplied evidence establishes that the claim is false under the policy.',
                                  unknown='The supplied evidence does not establish either the claim or its negation.'))))
            name = f"{case['id']}-{condition}"
            path = HERE / 'requests' / f'{name}.json'
            path.parent.mkdir(exist_ok=True)
            path.write_text(json.dumps(request, indent=2) + '\n')
            jobs.append((name, path))
    # Fixed shuffle avoids always running short before full; no answer-based selection.
    import random
    random.Random(22).shuffle(jobs)
    return cases, jobs


def call(job):
    name, path = job
    target = HERE / 'receipts' / f'{name}.json'
    start = time.perf_counter()
    try:
        result = subprocess.run([sys.executable, str(ROOT / 'skills/jev/scripts/jev.py'), 'decide', str(path), '--provider', 'openrouter'], capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        target.write_text(json.dumps(dict(request_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                         exit_code=124, wall_seconds=time.perf_counter()-start,
                                         stderr='Subprocess timed out after 90 seconds; no retry.'), indent=2) + '\n')
        return name, 124
    receipt = dict(request_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), exit_code=result.returncode,
                   wall_seconds=time.perf_counter()-start, stderr=result.stderr)
    try:
        receipt['result'] = json.loads(result.stdout)
    except json.JSONDecodeError:
        receipt['stdout'] = result.stdout
    target.write_text(json.dumps(receipt, indent=2) + '\n')
    return name, result.returncode


def score(cases):
    rows = []
    for case in cases:
        for condition in ('short', 'full'):
            path = HERE / 'receipts' / f"{case['id']}-{condition}.json"
            if not path.exists():
                continue
            receipt = json.loads(path.read_text())
            result = receipt.get('result', {})
            decision = result.get('decisions', {}).get('verdict', {})
            value = decision.get('value')
            rows.append(dict(id=case['id'], condition=condition, gold=case[f'gold_{condition}'], value=value,
                             correct=value == case[f'gold_{condition}'], full_gold=case['gold_full'],
                             status=decision.get('status'), probability=decision.get('probability'),
                             wall_seconds=receipt['wall_seconds'], exit_code=receipt['exit_code']))
    (HERE / 'scores.json').write_text(json.dumps(rows, indent=2) + '\n')
    for condition in ('short', 'full'):
        subset = [r for r in rows if r['condition'] == condition]
        print(condition, 'n=', len(subset), 'correct=', sum(r['correct'] for r in subset), 'unknown=', sum(r['value'] == 'unknown' for r in subset), 'errors=', sum(r['value'] is None for r in subset))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    cases, jobs = prepare()
    if args.live:
        output = HERE / 'receipts'
        output.mkdir(exist_ok=True)
        if list(output.glob('*.json')):
            raise SystemExit('Receipts exist; refusing to overwrite or silently repeat paid calls.')
        with ThreadPoolExecutor(max_workers=4) as pool:
            for item in pool.map(call, jobs):
                print(*item, flush=True)
    score(cases)
