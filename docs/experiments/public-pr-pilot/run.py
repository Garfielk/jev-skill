"""Score frozen public-PR receipts offline; --live makes 20 paid calls, no retries."""
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


def call(case):
    request = HERE / 'requests' / f"{case['id']}.json"
    digest = hashlib.sha256(request.read_bytes()).hexdigest()
    if digest != case['request_sha256']:
        raise ValueError('Request changed after annotation')
    start = time.perf_counter()
    try:
        proc = subprocess.run([sys.executable, str(ROOT / 'skills/jev/scripts/jev.py'), 'decide', str(request), '--provider', 'openrouter'], capture_output=True, text=True, timeout=90)
        receipt = dict(exit_code=proc.returncode, stderr=proc.stderr)
        try:
            receipt['result'] = json.loads(proc.stdout)
        except json.JSONDecodeError:
            receipt['stdout'] = proc.stdout
    except subprocess.TimeoutExpired:
        receipt = dict(exit_code=124, stderr='Timed out after 90 seconds; no retry.')
    receipt.update(request_sha256=digest, wall_seconds=time.perf_counter()-start)
    (HERE / 'receipts' / f"{case['id']}.json").write_text(json.dumps(receipt, indent=2) + '\n')
    return case['id'], receipt['exit_code']


def score(cases):
    rows = []
    for case in cases:
        path = HERE / 'receipts' / f"{case['id']}.json"
        if not path.exists():
            continue
        receipt = json.loads(path.read_text())
        decision = receipt.get('result', {}).get('decisions', {}).get('value', {})
        rows.append(dict(id=case['id'], expected=case['expected'], actual=decision.get('value'),
                         agreement=decision.get('value') == case['expected'], status=decision.get('status'),
                         probability=decision.get('probability'), exit_code=receipt['exit_code']))
    (HERE / 'scores.json').write_text(json.dumps(rows, indent=2) + '\n')
    print('Scored:', len(rows), 'Agreement:', sum(r['agreement'] for r in rows))
    for row in rows:
        print(row['id'], row['expected'], row['actual'], row['status'], row['probability'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    cases = json.loads((HERE / 'manifest.json').read_text())['cases']
    if args.live:
        (HERE / 'receipts').mkdir(exist_ok=True)
        if list((HERE / 'receipts').glob('*.json')):
            raise SystemExit('Existing receipts: refusing to overwrite or repeat calls.')
        with ThreadPoolExecutor(max_workers=4) as pool:
            for result in pool.map(call, cases):
                print(*result, flush=True)
    score(cases)
