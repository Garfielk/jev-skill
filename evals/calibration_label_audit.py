"""Post-hoc bracket-only label diagnostic; never changes strict results or receipts."""

import argparse
from copy import deepcopy
import json
from pathlib import Path

from . import calibration


def _one_choice(pairs):
    if len(pairs) != 1 or pairs[0][0] != "choice":
        raise ValueError("Expected exactly one choice key")
    return dict(pairs)


def recover_letter(record, criteria):
    """Use option membership only, never gold, to recover C -> (C)."""
    error = record.get("error")
    if (record.get("kind") != "base" or not isinstance(error, dict)
            or error.get("type") != "ValueError" or error.get("http_status") is not None
            or "response" not in record):
        return None
    try:
        content = record["response"]["choices"][0]["message"]["content"]
        answer = json.loads(content, object_pairs_hook=_one_choice)
    except (ValueError, TypeError, KeyError, IndexError):
        return None
    if not isinstance(answer, dict):
        return None
    letter = answer["choice"]
    if not isinstance(letter, str) or len(letter) != 1 or not "A" <= letter <= "Z":
        return None
    label = f"({letter})"
    return label if label in criteria else None


def _accuracy(records):
    attempted = len(records)
    valid = [record for record in records if "error" not in record]
    correct = sum(record.get("prediction") == record["target"] for record in valid)
    return {"attempted": attempted, "valid": len(valid), "invalid": attempted - len(valid),
            "correct": correct, "accuracy": correct / attempted if attempted else None,
            "accuracy_valid": correct / len(valid) if valid else None}


def audit(directory):
    directory = Path(directory)
    # Retain every completeness/hash/request/raw-response check from the strict runner.
    strict = calibration.summarize_run(directory, write=False)
    samples = json.loads((directory / "samples.json").read_text())
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text().splitlines()]
    normalized = deepcopy(events)
    options = {sample["id"]: sample["criteria"] for sample in samples}
    recovered_ids = []
    for record in normalized:
        label = recover_letter(record, options[record["id"]])
        if label is not None:
            record["prediction"] = label
            del record["error"]
            recovered_ids.append(record["id"])
    base = [record for record in normalized if record["kind"] == "base"]
    tasks = sorted({sample["task"] for sample in samples})
    snapshots = {name: (calibration.ROOT / name).read_text() for name in
                 ("evals/calibration_label_audit.py", "evals/calibration.py")}
    return {
        "source_snapshots": snapshots,
        "source_sha256": {name: calibration.digest(code.encode()) for name, code in snapshots.items()},
        "disclaimer": "POST-HOC bracket-only diagnostic, NOT preregistered. No new API calls. "
            "Strict summary and raw receipts remain unchanged. This is label-format sensitivity analysis, "
            "not a replacement for the strict benchmark or evidence from a deployed cascade.",
        "normalization": "Only base ValueError records without HTTP status, with response JSON containing "
            "exactly one choice key whose value is one uppercase letter, are recovered when the parenthesized "
            "letter is an original option. Gold labels are not consulted during recovery. All other errors remain.",
        "new_api_calls": 0, "strict_summary_changed": False,
        "recovered_count": len(recovered_ids), "recovered_ids": recovered_ids,
        "strict_base": strict["base"],
        "normalized_base": {"overall": _accuracy(base), "by_task": {
            task: _accuracy([record for record in base if record["task"] == task]) for task in tasks}},
        "normalized_cascade": {score: calibration.cascade(normalized, samples, score)
                               for score in ("top_probability", "confidence")},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args(argv)
    result = audit(args.directory)
    output = args.directory / "label-audit.json"
    with output.open("x") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(output), "recovered_count": result["recovered_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
