"""Fetch the fixed manifest's public sources with gh; never execute their code."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='New directory for raw public snapshots')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    cases = json.loads((HERE / 'manifest.json').read_text())['cases']

    def fetch(case):
        parts = case['url'].split('/')
        repo, number = '/'.join(parts[3:5]), parts[-1]
        data = subprocess.check_output(['gh', 'pr', 'view', number, '-R', repo, '--json',
                                        'number,title,body,url,baseRefOid,headRefOid,mergedAt,comments,reviews,files'], text=True)
        diff = subprocess.check_output(['gh', 'pr', 'diff', number, '-R', repo], text=True)
        (args.output / f"{case['id']}.json").write_text(data)
        (args.output / f"{case['id']}.diff").write_text(diff)
        return case['id']

    with ThreadPoolExecutor(max_workers=4) as pool:
        for identifier in pool.map(fetch, cases):
            print(identifier)


if __name__ == '__main__':
    main()
