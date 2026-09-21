import json
import os
import random
import sys
import time
import hashlib
from pathlib import Path
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import jev helpers (installed module or repo path)
try:
    import jev
    from jev import request_decisions, build_report, http_json
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'skills' / 'jev' / 'scripts'))
    import jev
    from jev import request_decisions, build_report, http_json


def _validate_job(job):
    if not isinstance(job, dict):
        raise ValueError('job must be a dict')
    if 'criteria' not in job or not isinstance(job['criteria'], dict):
        raise ValueError('job.criteria required as dict')
    if 'records' not in job or not isinstance(job['records'], list) or len(job['records']) == 0:
        raise ValueError('job.records required nonempty list')
    seen = set()
    for r in job['records']:
        if not isinstance(r, dict):
            raise ValueError('each record must be a dict')
        if 'id' not in r or not isinstance(r['id'], str) or r['id'] == '':
            raise ValueError('record.id required nonempty string')
        if r['id'] in seen:
            raise ValueError(f'duplicate record id: {r["id"]}')
        seen.add(r['id'])
        if 'text' not in r or not isinstance(r['text'], str) or r['text'] == '':
            raise ValueError('record.text required nonempty string')
        if 'gold' in r and (not isinstance(r['gold'], str) or r['gold'] == ''):
            raise ValueError('record.gold must be nonempty string if present')
    if 'context' in job and not isinstance(job['context'], dict):
        raise ValueError('job.context must be dict if present')
    return True


def _validate_params(sample_size, concurrency, timeout, seed):
    if not isinstance(sample_size, int) or sample_size < 1 or sample_size > 100:
        raise ValueError('sample_size must be int 1..100')
    if not isinstance(concurrency, int) or concurrency < 1 or concurrency > 8:
        raise ValueError('concurrency must be int 1..8')
    if not isinstance(timeout, (int, float)) or timeout <= 0 or not (timeout < float('inf')):
        raise ValueError('timeout must be finite positive number')
    if not isinstance(seed, int):
        raise ValueError('seed must be int')
    return True


def _sample_records(job, sample_size, seed):
    records = list(job['records'])
    rng = random.Random(seed)
    if len(records) <= sample_size:
        sampled = records[:]
        rng.shuffle(sampled)
    else:
        sampled = rng.sample(records, sample_size)
    return sampled


def _build_manifest(sampled, job, sample_size, concurrency, timeout, seed, reference_model):
    manifest = {
        'sample_size': sample_size,
        'concurrency': concurrency,
        'timeout': timeout,
        'seed': seed,
        'reference_model': reference_model,
        'sampled_ids': [r['id'] for r in sampled],
        'gold_labels': {r['id']: r.get('gold') for r in sampled},
        'criteria_keys': list(job['criteria'].keys()),
        'input_hash': hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()
    }
    return manifest


def _build_jev_state(record, job):
    state = {
        'context': job.get('context', {}),
        'record': {
            'id': record['id'],
            'text': record['text']
        }
    }
    if 'context' in record:
        state['record']['context'] = record['context']
    return state


def _build_jev_questions(job):
    return {
        'category': {
            'type': 'choice',
            'choices': list(job['criteria'].keys()),
            'instructions': 'Select the single best category for this support ticket.',
            'criteria': job['criteria']
        }
    }


def _call_jev(record, job, timeout):
    state = _build_jev_state(record, job)
    questions = _build_jev_questions(job)
    try:
        result = request_decisions(state, questions, timeout=timeout)
        return result, None
    except Exception as e:
        return None, {'type': type(e).__name__, 'kind': 'exception', 'phase': 'jev_request', 'status': 'error'}


def _call_reference(record, job, reference_model, timeout):
    state = _build_jev_state(record, job)
    questions = _build_jev_questions(job)
    prompt_content = json.dumps({'state': state, 'question': questions['category']})
    messages = [
        {'role': 'system', 'content': 'You are a support ticket classifier. Respond with JSON {"label": "<category>"}.'},
        {'role': 'user', 'content': prompt_content}
    ]
    payload = {
        'model': reference_model,
        'messages': messages,
        'max_tokens': 512,
        'response_format': {'type': 'json_object'},
        'reasoning': {'enabled': False}
    }
    try:
        response = http_json('https://openrouter.ai/api/v1/chat/completions', payload, timeout=timeout)
        return response, None
    except Exception as e:
        return None, {'type': type(e).__name__, 'kind': 'exception', 'phase': 'reference_request', 'status': 'error'}


def _parse_reference_response(response, criteria_keys):
    if response is None:
        return None, {'type': 'NoneResponse', 'kind': 'missing', 'phase': 'reference_parse', 'status': 'error'}
    if not isinstance(response, dict):
        return None, {'type': 'TypeError', 'kind': 'invalid_type', 'phase': 'reference_parse', 'status': 'error'}
    choices = response.get('choices')
    if not choices or not isinstance(choices, list) or len(choices) == 0:
        return None, {'type': 'MissingChoices', 'kind': 'missing', 'phase': 'reference_parse', 'status': 'error'}
    choice = choices[0]
    if choice.get('finish_reason') != 'stop':
        return None, {'type': 'FinishReason', 'kind': f'not_stop:{choice.get("finish_reason")}', 'phase': 'reference_parse', 'status': 'error'}
    content = choice.get('message', {}).get('content')
    if not content:
        return None, {'type': 'MissingContent', 'kind': 'missing', 'phase': 'reference_parse', 'status': 'error'}
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return None, {'type': 'JSONDecodeError', 'kind': 'malformed_json', 'phase': 'reference_parse', 'status': 'error'}
    if not isinstance(parsed, dict) or 'label' not in parsed:
        return None, {'type': 'SchemaError', 'kind': 'missing_label_key', 'phase': 'reference_parse', 'status': 'error'}
    label = parsed['label']
    if label not in criteria_keys:
        return None, {'type': 'InvalidLabel', 'kind': f'unknown_label:{label}', 'phase': 'reference_parse', 'status': 'error'}
    return label, None


def _parse_jev_response(result, criteria_keys):
    if result is None:
        return None, {'type': 'NoneResult', 'kind': 'missing', 'phase': 'jev_parse', 'status': 'error'}
    if not isinstance(result, dict):
        return None, {'type': 'TypeError', 'kind': 'invalid_type', 'phase': 'jev_parse', 'status': 'error'}
    answers = result.get('answers', {})
    category = answers.get('category', {})
    if not isinstance(category, dict):
        return None, {'type': 'TypeError', 'kind': 'category_not_dict', 'phase': 'jev_parse', 'status': 'error'}
    if category.get('type') != 'choice':
        return None, {'type': 'TypeError', 'kind': 'not_choice_type', 'phase': 'jev_parse', 'status': 'error'}
    label = category.get('choice')
    if label not in criteria_keys:
        return None, {'type': 'InvalidLabel', 'kind': f'unknown_label:{label}', 'phase': 'jev_parse', 'status': 'error'}
    return label, None


def _write_receipt(writer, receipt):
    writer.write(json.dumps(receipt) + '\n')
    writer.flush()


def _build_receipt(record_id, arm, request_data, response_data, error_info, elapsed, requested_model, resolved_model):
    receipt = {
        'id': record_id,
        'arm': arm,
        'request': request_data,
        'elapsed_seconds': elapsed
    }
    if error_info:
        receipt['error'] = error_info
    else:
        receipt['response'] = response_data
    receipt['requested_model'] = requested_model
    receipt['resolved_model'] = resolved_model
    return receipt


def run(job, output, *, sample_size=20, reference_model='deepseek/deepseek-v4-flash', concurrency=4, timeout=30, live=False, seed=0):
    _validate_job(job)
    _validate_params(sample_size, concurrency, timeout, seed)

    if not live:
        sampled = _sample_records(job, sample_size, seed)
        manifest = _build_manifest(sampled, job, sample_size, concurrency, timeout, seed, reference_model)
        output.mkdir(exist_ok=False)
        with open(output / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        report = {
            'bulk_authorized': False,
            'mode': 'dry_run',
            'metrics': {
                'sample_size': sample_size,
                'attempted_records': 0,
                'valid_pairs': 0,
                'agreement': None,
                'jev_accuracy': None,
                'reference_accuracy': None
            },
            'gate': 'needs_review',
            'usage': {
                'jev': {'calls': 0, 'known_cost_subtotal_usd': 0.0, 'cost_unknown_calls': 0},
                'reference': {'calls': 0, 'known_cost_subtotal_usd': 0.0, 'cost_unknown_calls': 0},
                'reported_cost_usd': None
            },
            'sample_check_passed': False,
            'disagreements': [],
            'input_hash': manifest['input_hash']
        }
        return report

    # Live mode
    if 'OPENROUTER_API_KEY' not in os.environ:
        raise ValueError('OPENROUTER_API_KEY environment variable required for live mode')

    sampled = _sample_records(job, sample_size, seed)
    manifest = _build_manifest(sampled, job, sample_size, concurrency, timeout, seed, reference_model)
    output.mkdir(exist_ok=False)
    with open(output / 'manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    criteria_keys = list(job['criteria'].keys())
    receipts_path = output / 'receipts.jsonl'
    writer = open(receipts_path, 'w')

    # Build pairs: each record has two arms
    pairs = []
    for rec in sampled:
        pairs.append((rec, 'jev'))
        pairs.append((rec, 'reference'))

    # Sort pairs by record id for stable pairing
    pairs.sort(key=lambda x: (x[0]['id'], x[1]))

    # Group into waves: each wave contains one pair per record (jev+reference for same id)
    # For concurrency=2, first wave = first record's two arms
    # We'll process in waves: each wave picks up to concurrency arms, but we must ensure
    # that we don't split a record's arms across waves if possible.
    # Actually spec: "For concurrency=2, first wave MUST be first record's two arms."
    # So we group by record and process record by record, but limit concurrency.
    # Simpler: process pairs in order, but ensure that for each record, both arms are
    # submitted together if concurrency allows.

    # Build ordered list of (record, arm) but grouped by record
    record_order = []
    seen_ids = set()
    for rec in sampled:
        if rec['id'] not in seen_ids:
            seen_ids.add(rec['id'])
            record_order.append(rec)

    # Build wave plan: each wave takes up to concurrency arms, but we try to keep
    # both arms of a record together.
    waves = []
    current_wave = []
    for rec in record_order:
        # Add both arms
        if len(current_wave) + 2 <= concurrency:
            current_wave.append((rec, 'jev'))
            current_wave.append((rec, 'reference'))
        else:
            if current_wave:
                waves.append(current_wave)
            current_wave = [(rec, 'jev'), (rec, 'reference')]
    if current_wave:
        waves.append(current_wave)

    # If waves are empty (shouldn't happen), fallback
    if not waves:
        waves = [pairs[:concurrency]]
        remaining = pairs[concurrency:]
        while remaining:
            waves.append(remaining[:concurrency])
            remaining = remaining[concurrency:]

    # Track results
    results = {}  # {record_id: {'jev': ..., 'reference': ...}}
    errors = []
    all_receipts = []
    stop_new_waves = False

    for wave_idx, wave_pairs in enumerate(waves):
        if stop_new_waves:
            break

        futures = {}
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            for rec, arm in wave_pairs:
                if stop_new_waves:
                    break
                if arm == 'jev':
                    future = executor.submit(_call_jev, rec, job, timeout)
                else:
                    future = executor.submit(_call_reference, rec, job, reference_model, timeout)
                futures[future] = (rec, arm)

            for future in as_completed(futures):
                rec, arm = futures[future]
                start_time = time.time()
                try:
                    if arm == 'jev':
                        result, error = future.result()
                    else:
                        response, error = future.result()
                except Exception as e:
                    result = None
                    response = None
                    error = {'type': type(e).__name__, 'kind': 'exception', 'phase': f'{arm}_execution', 'status': 'error'}
                elapsed = time.time() - start_time

                if error:
                    receipt = _build_receipt(rec['id'], arm, None, None, error, elapsed, reference_model if arm == 'reference' else 'jev', None)
                    _write_receipt(writer, receipt)
                    all_receipts.append(receipt)
                    errors.append(receipt)
                    stop_new_waves = True
                    break
                else:
                    if arm == 'jev':
                        label, parse_error = _parse_jev_response(result, criteria_keys)
                        if parse_error:
                            receipt = _build_receipt(rec['id'], arm, result, None, parse_error, elapsed, 'jev', result.get('model', 'unknown') if isinstance(result, dict) else None)
                            _write_receipt(writer, receipt)
                            all_receipts.append(receipt)
                            errors.append(receipt)
                            stop_new_waves = True
                            break
                        else:
                            resolved_model = result.get('model', 'unknown') if isinstance(result, dict) else None
                            receipt = _build_receipt(rec['id'], arm, result, {'label': label}, None, elapsed, 'jev', resolved_model)
                            _write_receipt(writer, receipt)
                            all_receipts.append(receipt)
                            if rec['id'] not in results:
                                results[rec['id']] = {}
                            results[rec['id']]['jev'] = {'label': label, 'cost': result.get('usage', {}).get('cost', None) if isinstance(result, dict) else None}
                    else:
                        label, parse_error = _parse_reference_response(response, criteria_keys)
                        if parse_error:
                            receipt = _build_receipt(rec['id'], arm, response, None, parse_error, elapsed, reference_model, response.get('model', 'unknown') if isinstance(response, dict) else None)
                            _write_receipt(writer, receipt)
                            all_receipts.append(receipt)
                            errors.append(receipt)
                            stop_new_waves = True
                            break
                        else:
                            resolved_model = response.get('model', 'unknown') if isinstance(response, dict) else None
                            receipt = _build_receipt(rec['id'], arm, response, {'label': label}, None, elapsed, reference_model, resolved_model)
                            _write_receipt(writer, receipt)
                            all_receipts.append(receipt)
                            if rec['id'] not in results:
                                results[rec['id']] = {}
                            results[rec['id']]['reference'] = {'label': label, 'cost': response.get('usage', {}).get('cost', None) if isinstance(response, dict) else None}

            if stop_new_waves:
                break

    writer.close()

    # Compute metrics
    attempted_records = len(sampled)
    valid_pairs = 0
    agreement = 0
    jev_correct = 0
    ref_correct = 0
    gold_count = 0
    disagreements = []
    jev_calls = 0
    ref_calls = 0
    jev_known_cost = 0.0
    ref_known_cost = 0.0
    jev_unknown_calls = 0
    ref_unknown_calls = 0

    for rec in sampled:
        rid = rec['id']
        if rid in results and 'jev' in results[rid] and 'reference' in results[rid]:
            valid_pairs += 1
            j_label = results[rid]['jev']['label']
            r_label = results[rid]['reference']['label']
            if j_label == r_label:
                agreement += 1
            else:
                disagreements.append({'id': rid, 'jev_label': j_label, 'reference_label': r_label})
            if 'gold' in rec:
                gold_count += 1
                if j_label == rec['gold']:
                    jev_correct += 1
                if r_label == rec['gold']:
                    ref_correct += 1
            # Costs
            j_cost = results[rid]['jev'].get('cost')
            r_cost = results[rid]['reference'].get('cost')
            jev_calls += 1
            ref_calls += 1
            if j_cost is not None and isinstance(j_cost, (int, float)) and j_cost >= 0:
                jev_known_cost += j_cost
            else:
                jev_unknown_calls += 1
            if r_cost is not None and isinstance(r_cost, (int, float)) and r_cost >= 0:
                ref_known_cost += r_cost
            else:
                ref_unknown_calls += 1

    # Also count calls from error receipts that had successful calls before error
    for rec in sampled:
        rid = rec['id']
        if rid in results:
            if 'jev' in results[rid]:
                pass  # already counted
            if 'reference' in results[rid]:
                pass

    # Count all receipts for call counts
    for r in all_receipts:
        if 'error' not in r:
            if r['arm'] == 'jev':
                jev_calls += 1
            else:
                ref_calls += 1

    # Deduplicate call counts (since we already counted from results)
    # Actually we counted from results, but also from all_receipts which includes those.
    # Let's just count from all_receipts
    jev_calls = sum(1 for r in all_receipts if r['arm'] == 'jev' and 'error' not in r)
    ref_calls = sum(1 for r in all_receipts if r['arm'] == 'reference' and 'error' not in r)

    # Recompute costs from receipts
    jev_known_cost = 0.0
    ref_known_cost = 0.0
    jev_unknown_calls = 0
    ref_unknown_calls = 0
    for r in all_receipts:
        if 'error' not in r:
            resp = r.get('response', {})
            cost = None
            if r['arm'] == 'jev':
                req = r.get('request', {})
                if isinstance(req, dict):
                    cost = req.get('usage', {}).get('cost')
            else:
                resp_data = r.get('response', {})
                if isinstance(resp_data, dict):
                    cost = resp_data.get('usage', {}).get('cost')
            if cost is not None and isinstance(cost, (int, float)) and cost >= 0:
                if r['arm'] == 'jev':
                    jev_known_cost += cost
                else:
                    ref_known_cost += cost
            else:
                if r['arm'] == 'jev':
                    jev_unknown_calls += 1
                else:
                    ref_unknown_calls += 1

    reported_cost = None
    if jev_unknown_calls == 0 and ref_unknown_calls == 0:
        reported_cost = jev_known_cost + ref_known_cost

    jev_accuracy = jev_correct / gold_count if gold_count > 0 else None
    ref_accuracy = ref_correct / gold_count if gold_count > 0 else None
    agreement_rate = agreement / valid_pairs if valid_pairs > 0 else None

    # Gate logic
    sample_check_passed = False
    if gold_count > 0 and valid_pairs > 0:
        if jev_accuracy is not None and ref_accuracy is not None:
            if jev_accuracy >= 0.9 and ref_accuracy >= 0.9:
                if jev_accuracy - ref_accuracy <= 0.05:
                    if len(disagreements) == 0:
                        sample_check_passed = True

    gate = 'needs_review'
    if sample_check_passed:
        gate = 'pass'

    report = {
        'bulk_authorized': False,
        'mode': 'live_paired_smoke_test',
        'metrics': {
            'sample_size': sample_size,
            'attempted_records': attempted_records,
            'valid_pairs': valid_pairs,
            'agreement': agreement_rate,
            'jev_accuracy': jev_accuracy,
            'reference_accuracy': ref_accuracy
        },
        'gate': gate,
        'sample_check_passed': sample_check_passed,
        'usage': {
            'jev': {
                'calls': jev_calls,
                'known_cost_subtotal_usd': jev_known_cost,
                'cost_unknown_calls': jev_unknown_calls
            },
            'reference': {
                'calls': ref_calls,
                'known_cost_subtotal_usd': ref_known_cost,
                'cost_unknown_calls': ref_unknown_calls
            },
            'reported_cost_usd': reported_cost
        },
        'disagreements': disagreements,
        'input_hash': manifest['input_hash']
    }

    with open(output / 'report.json', 'w') as f:
        json.dump(report, f, indent=2)

    return report


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true', help='Enable live API calls')
    parser.add_argument('--output', required=True, type=Path, help='Output directory')
    parser.add_argument('--sample-size', type=int, default=20)
    parser.add_argument('--reference-model', default='deepseek/deepseek-v4-flash')
    parser.add_argument('--concurrency', type=int, default=4)
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('job_file', type=Path, help='Path to job JSON file')
    args = parser.parse_args()

    with open(args.job_file) as f:
        job = json.load(f)

    try:
        report = run(
            job,
            args.output,
            sample_size=args.sample_size,
            reference_model=args.reference_model,
            concurrency=args.concurrency,
            timeout=args.timeout,
            live=args.live,
            seed=args.seed
        )
        if report['gate'] == 'needs_review':
            sys.exit(2)
        elif report['mode'] == 'dry_run':
            sys.exit(0)
        else:
            sys.exit(0)
    except (ValueError, FileExistsError) as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
