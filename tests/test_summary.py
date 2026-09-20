import json
from pathlib import Path
import tempfile
import unittest

from evals.summarize import summarize


class SummaryTests(unittest.TestCase):
    def test_rejects_aborted_run(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "aborted.json").write_text("{}")
            with self.assertRaises(ValueError):
                summarize(directory)

    def test_rejects_missing_episode(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "manifest.json").write_text(json.dumps({"repeats": 1, "cases": ["a"]}))
            Path(directory, "results.json").write_text("[]")
            with self.assertRaises(ValueError):
                summarize(directory)
