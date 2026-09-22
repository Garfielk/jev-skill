"""Reconstruct frozen panel inputs locally. --download fetches public data, never models."""
import argparse
import csv
import io
import json
from pathlib import Path
import random
import urllib.request
from . import panel_datasets as adapters
from .model_panel import prepare
from .calibration import digest
from .run import ROOT

FIXTURES = ROOT/'evals/fixtures'


def load_samples(dataset, cache):
    cache = Path(cache)
    sources = json.loads((FIXTURES/'panel-sources.json').read_text())[dataset]
    for source in sources:
        if digest((cache/source['file']).read_bytes()) != source['sha256']:
            raise ValueError(f"Source hash mismatch: {source['file']}")
    def lines(name):
        return [json.loads(line) for line in (cache/name).read_text().splitlines()]
    if dataset == 'logiqa':
        samples = adapters.logiqa(lines('logiqa2-test-zh.jsonl'))
    elif dataset == 'ocnli':
        samples = adapters.ocnli(lines('ocnli-dev.jsonl'))
    elif dataset == 'banking':
        samples = adapters.banking(list(csv.DictReader(io.StringIO((cache/'banking-test.csv').read_text()))),
                                   json.loads((cache/'banking-categories.json').read_text()))
    elif dataset in ('boolq','injection'):
        import pyarrow.parquet as pq  # Optional preparation-only dependency; never installed automatically.
        rows = pq.read_table(cache/(dataset+'.parquet')).to_pylist()
        samples = getattr(adapters,dataset)(rows)
    elif dataset == 'bfcl':
        samples = adapters.bfcl(lines('bfcl-multiple.jsonl'), lines('bfcl-answers.jsonl'))
    elif dataset == 'ruozhiba':
        return adapters.ruozhiba(lines('ruozhiba.jsonl'), json.loads((FIXTURES/'ruozhiba-mc-options.json').read_text()))
    else:
        raise ValueError('Unknown dataset')
    return sorted(random.Random('20260922:'+dataset).sample(samples,20),key=lambda s:s['id'])


def download(dataset, cache):
    cache = Path(cache); cache.mkdir(parents=True,exist_ok=True)
    for source in json.loads((FIXTURES/'panel-sources.json').read_text())[dataset]:
        path = cache/source['file']
        if path.exists():
            raw=path.read_bytes()
        else:
            with urllib.request.urlopen(source['url'],timeout=60) as response:
                raw=response.read()
        if digest(raw)!=source['sha256']:
            raise ValueError('Source hash mismatch; refusing to use changed data')
        if not path.exists():
            path.write_bytes(raw)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset',required=True,choices=['logiqa','ocnli','banking','boolq','bfcl','ruozhiba','injection'])
    parser.add_argument('--cache',required=True,type=Path)
    parser.add_argument('--download',action='store_true',help='Fetch source after reviewing its license in the report')
    parser.add_argument('--publication',required=True,type=Path,help='Published source-free run directory')
    parser.add_argument('--output',required=True,type=Path,help='New local campaign directory')
    args=parser.parse_args()
    if args.download: download(args.dataset,args.cache)
    index=json.loads((args.publication/'index.json').read_text());plan=index['manifest']
    samples=load_samples(args.dataset,args.cache)
    # Reconstructed bytes must match the original frozen inputs before any model call.
    raw=(json.dumps(samples,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    if digest(raw)!=plan['samples_sha256']:
        raise ValueError('Reconstructed samples differ from the original campaign')
    models=json.loads(json.dumps(plan['models']))
    for model in models:
        model['options'].pop('response_format',None)  # v1 always replaced this with enum schema.
    prepare(args.output,samples,models,{**plan['provenance'],'reconstructed_from':str(args.publication)})
