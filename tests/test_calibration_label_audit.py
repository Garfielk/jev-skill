from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from evals import calibration as c
from evals import calibration_label_audit as a


def failed(content='{"choice":"B"}', **error):
    return {"kind": "base", "error": {"type": "ValueError", "http_status": None, **error},
            "response": {"choices": [{"message": {"content": content}}]}}


class LabelAuditTests(unittest.TestCase):
    def fixture(self, directory):
        samples = [{"id": f"{task}:0", "task": task, "input": "Question\nOptions:\n(A) First\n(B) Second",
                    "target": "(B)", "criteria": {"(A)": "First", "(B)": "Second"}} for task in c.TASKS]
        c.dump(directory / "samples.json", samples)
        plan = {"jev_model": "fake-jev", "base_model": "fake-base", "instructions": c.INSTRUCTIONS,
                "base_system": c.BASE_SYSTEM, "base_options": c.BASE_OPTIONS,
                "samples_sha256": c.digest((directory / "samples.json").read_bytes())}
        c.dump(directory / "manifest.json", plan)
        events = []
        for sample in samples:
            for kind in ("jev", "base"):
                payload = c.payload_for(sample, kind, plan)
                record = {key: sample[key] for key in ("id", "task", "target")}
                record.update(kind=kind, request=payload, latency_seconds=0.1)
                if kind == "base":
                    record.update(failed())
                else:
                    response = {"answers": {"answer": {"type": "choice", "choice": "(B)",
                        "confidence": 0.8, "probabilities": {"(A)": 0.2, "(B)": 0.8}}}}
                    record.update(response=response, **c.parse_prediction(sample, kind, payload, response))
                events.append(record)
        (directory / "events.jsonl").write_text("".join(json.dumps(event) + "\n" for event in events))
        c.summarize_run(directory)
        return samples, events

    def test_recovers_only_original_parenthesized_label(self):
        item = failed()
        before = deepcopy(item)
        self.assertEqual(a.recover_letter(item, {"(A)": "First", "(B)": "Second"}), "(B)")
        self.assertIsNone(a.recover_letter(item, {"(A)": "First", "(C)": "Third"}))
        self.assertEqual(item, before)

    def test_rejects_other_formats_and_extra_or_duplicate_keys(self):
        for content in ['{"choice":"Z"}', '{"choice":"b"}', '{"choice":" B "}',
                        '{"choice":"(B)"}', '{"choice":"BB"}', '{"choice":null}',
                        '{"choice":["B"]}', '{"choice":"B","reason":"why"}',
                        '{"choice":"B","choice":"B"}', '[{"choice":"B"}]',
                        '```json\n{"choice":"B"}\n```', 'B', None]:
            with self.subTest(content=content):
                self.assertIsNone(a.recover_letter(failed(content), {"(A)": "First", "(B)": "Second"}))
        self.assertIsNone(a.recover_letter(failed('{"choice":"Y"}'), {"Yes": "Yes", "No": "No"}))

    def test_preserves_transport_and_other_error_types(self):
        for item in [failed(type="JevError"), failed(type="TypeError"), failed(http_status=500),
                     {**failed(), "kind": "jev"}, {"kind": "base", "error": {"type": "ValueError"}},
                     {"kind": "base", "response": failed()["response"]}]:
            with self.subTest(item=item):
                self.assertIsNone(a.recover_letter(item, {"(B)": "Second"}))

    def test_recovery_has_no_gold_dependency(self):
        class NoGold(dict):
            def __getitem__(self, key):
                if key == "target":
                    raise AssertionError("Gold read during normalization")
                return super().__getitem__(key)

            def get(self, key, default=None):
                if key == "target":
                    raise AssertionError("Gold read during normalization")
                return super().get(key, default)

        for target in ("(A)", "(B)", "not-an-option"):
            item = NoGold({**failed(), "target": target})
            self.assertEqual(a.recover_letter(item, {"(A)": "First", "(B)": "Second"}), "(B)")

    def test_completed_audit_no_calls_or_original_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            samples, _ = self.fixture(directory)
            originals = {path.name: (path.read_bytes(), path.stat().st_mtime_ns) for path in directory.iterdir()}
            with patch.object(c.jev, "request_decisions") as helper, patch.object(c.jev, "http_json") as base:
                result = a.audit(directory)
                helper.assert_not_called()
                base.assert_not_called()
            self.assertEqual(result["recovered_count"], 4)
            self.assertEqual(result["recovered_ids"], [sample["id"] for sample in samples])
            self.assertEqual(result["strict_base"]["overall"]["accuracy"], 0)
            self.assertEqual(result["normalized_base"]["overall"]["accuracy"], 1)
            self.assertEqual(result["normalized_cascade"]["top_probability"]["automatic_accuracy"], 1)
            self.assertEqual(result["normalized_cascade"]["confidence"]["automatic_errors_unresolved"], 0)
            self.assertIn("NOT preregistered", result["disclaimer"])
            self.assertEqual(result["new_api_calls"], 0)
            self.assertEqual({path.name: (path.read_bytes(), path.stat().st_mtime_ns)
                              for path in directory.iterdir()}, originals)

    def test_cli_output_exclusive(self):
        with tempfile.TemporaryDirectory() as tmp, patch("builtins.print"):
            directory = Path(tmp)
            self.fixture(directory)
            self.assertEqual(a.main([str(directory)]), 0)
            first = (directory / "label-audit.json").read_bytes()
            with self.assertRaises(FileExistsError):
                a.main([str(directory)])
            self.assertEqual((directory / "label-audit.json").read_bytes(), first)

    def test_incomplete_or_aborted_run_cannot_create_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            _, events = self.fixture(directory)
            (directory / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events[:-1]))
            with self.assertRaisesRegex(ValueError, "Incomplete"):
                a.main([str(directory)])
            self.assertFalse((directory / "label-audit.json").exists())
            c.dump(directory / "aborted.json", {"reason": "transport failure"})
            with self.assertRaisesRegex(ValueError, "Aborted"):
                a.main([str(directory)])


if __name__ == "__main__":
    unittest.main()
