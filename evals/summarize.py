"""Summarize a completed paired run without discarding errors or charging guesses."""

import argparse
import json
from pathlib import Path


def summarize(directory):
    directory = Path(directory)
    if (directory / "aborted.json").exists():
        raise ValueError("Aborted run is not a completed paired comparison")
    manifest = json.loads((directory / "manifest.json").read_text())
    results = json.loads((directory / "results.json").read_text())
    expected = {(repeat, case, arm) for repeat in range(1, manifest["repeats"] + 1)
                for case in manifest["cases"] for arm in ("baseline", "jev")}
    actual = [(row["repeat"], row["case"], row["arm"]) for row in results]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError("Missing, duplicate, or unexpected episodes")
    arms = {}
    for arm in ("baseline", "jev"):
        rows = [row for row in results if row["arm"] == arm]
        costs = [row["total"]["reported_cost_usd"] for row in rows]
        arms[arm] = {
            "episodes": len(rows), "successes": sum(row["success"] for row in rows),
            "mean_steps": sum(row["steps"] for row in rows) / len(rows),
            "unsafe_attempts": sum(row["unsafe_attempts"] for row in rows),
            "tool_errors": sum(row["tool_errors"] for row in rows),
            "invalid_actions": sum(row["invalid_actions"] for row in rows),
            "helper_invalid_answers": sum(row["helper_invalid_answers"] for row in rows),
            "api_calls": sum(row["total"]["calls"] for row in rows),
            "failed_api_calls": sum(row["total"]["failed_calls"] for row in rows),
            "reported_input_tokens": sum(row["total"]["reported_input_tokens"] for row in rows),
            "reported_output_tokens": sum(row["total"]["reported_output_tokens"] for row in rows),
            "usage_missing_calls": sum(row["total"]["usage_missing_calls"] for row in rows),
            "reported_cost_usd": sum(costs) if all(cost is not None for cost in costs) else None,
            "mean_api_seconds": sum(row["total"]["latency_seconds"] for row in rows) / len(rows),
        }
    by_key = {(row["repeat"], row["case"], row["arm"]): row for row in results}
    changes = [int(by_key[(repeat, case, "jev")]["success"]) -
               int(by_key[(repeat, case, "baseline")]["success"])
               for repeat in range(1, manifest["repeats"] + 1) for case in manifest["cases"]]
    return {"run": directory.name, "base_model": manifest["base_model"],
            "arms": arms, "paired": {"jev_wins": changes.count(1),
            "ties": changes.count(0), "jev_losses": changes.count(-1)},
            "scope": manifest["scope"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(summarize(args.directory), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
