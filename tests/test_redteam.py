import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/jev-eval/scripts/prepare.py"
spec = importlib.util.spec_from_file_location("redteam_prepare", SCRIPT)
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)
sys.path.insert(0, str(ROOT / "skills/jev/scripts"))
import jev


class RedTeamTests(unittest.TestCase):
    def fixtures(self):
        return [json.loads(line) for line in (ROOT / "skills/jev-eval/assets/transcripts.jsonl").read_text().splitlines()]

    def test_requests_are_valid_preserve_order_and_exclude_labels(self):
        records = self.fixtures()
        requests = prepare.prepare(records)
        self.assertEqual(len(requests), len(records))
        for record in records:
            payload = requests[record["case_id"]]
            jev.validate_request(payload)
            self.assertEqual(payload["state"]["messages"], record["messages"])
            self.assertNotIn("expected", payload["state"])
            self.assertEqual(set(payload["questions"]), {"outcome", "evidence"})

    def test_rejects_duplicate_ids_and_path_traversal(self):
        record = self.fixtures()[0]
        for records in [[record, record], [{**record, "case_id": "../../escape"}], [], [None], ["text"]]:
            with self.assertRaises(ValueError):
                prepare.prepare(records)

    def test_bad_transcript_rejected(self):
        for messages in [[], "not a list", [{"role": "attacker", "content": "fixture"}], [{}]]:
            record = copy.deepcopy(self.fixtures()[0])
            record["messages"] = messages
            with self.assertRaises(ValueError):
                prepare.prepare([record])

    def test_cli_offline_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = [sys.executable, str(SCRIPT), str(ROOT / "skills/jev-eval/assets/transcripts.jsonl"), "--out-dir", tmp]
            first = subprocess.run(command, capture_output=True, text=True, check=True)
            result = json.loads(first.stdout)
            self.assertFalse(result["jev_called"])
            self.assertFalse(result["target_called"])
            original = {p.name: p.read_bytes() for p in Path(tmp).glob("*.json")}
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(original, {p.name: p.read_bytes() for p in Path(tmp).glob("*.json")})
