import copy
import json
import math
import unittest

from evals.calibration_metrics import summarize


def record(probabilities=None, *, target="a", prediction="a", confidence=0.8, task="task", id="item"):
    return {"id": id, "task": task, "target": target, "prediction": prediction,
            "probabilities": {"a": 0.8, "b": 0.2} if probabilities is None else probabilities,
            "confidence": confidence}


class CalibrationMetricsTests(unittest.TestCase):
    def test_known_sum_brier_and_natural_log_loss(self):
        result = summarize([record()])["overall"]
        self.assertAlmostEqual(result["brier"], 0.08)
        self.assertAlmostEqual(result["nll"], -math.log(0.8))
        self.assertEqual(result["accuracy"], 1)
        self.assertAlmostEqual(result["top_probability_calibration"]["ece"], 0.2)

    def test_multiclass_brier_is_sum_not_class_mean(self):
        result = summarize([record({"a": 0.6, "b": 0.3, "c": 0.1})])["overall"]
        self.assertAlmostEqual(result["brier"], 0.26)

    def test_zero_gold_and_clamped_nll(self):
        result = summarize([record({"a": 0, "b": 1}, prediction="b")])["overall"]
        self.assertEqual(result["zero_gold_count"], 1)
        self.assertEqual(result["brier"], 2)
        self.assertAlmostEqual(result["nll"], -math.log(1e-12))
        self.assertEqual(result["correct"], 0)

    def test_failed_attempt_denominators_and_task_splits(self):
        records = [record(task="one"), {"id": "failed", "task": "one", "target": "a", "error": "timeout"},
                   record(target="b", task="two")]
        result = summarize(records)
        group = result["overall"]
        self.assertEqual((group["attempted"], group["valid"], group["invalid"]), (3, 2, 1))
        self.assertEqual(group["accuracy"], 1 / 3)
        self.assertEqual(group["accuracy_valid"], 0.5)
        self.assertEqual(result["by_task"]["one"]["accuracy"], 0.5)
        self.assertEqual(result["by_task"]["two"]["accuracy"], 0)
        human = group["routes"]["top_probability"]["human_candidate"]
        self.assertEqual((human["n"], human["correct"], human["accuracy"], human["risk"]), (1, 0, 0, 1))
        self.assertEqual(human["coverage"], 1 / 3)
        self.assertIsNone(human["mean_score"])

    def test_rounded_sums_normalize_without_mutating_input(self):
        item = record({"a": 0.79, "b": 0.2})
        original = copy.deepcopy(item)
        result = summarize([item])["overall"]
        p = 0.79 / 0.99
        self.assertAlmostEqual(result["brier"], (p - 1) ** 2 + (1 - p) ** 2)
        self.assertAlmostEqual(result["nll"], -math.log(p))
        self.assertAlmostEqual(result["routes"]["top_probability"]["stronger_model_candidate"]["mean_score"], p)
        self.assertEqual(result["rounded_sum_count"], 1)
        self.assertEqual(item, original)

    def test_normalization_controls_route_threshold(self):
        result = summarize([record({"a": 0.9, "b": 0.11})])["overall"]
        routes = result["routes"]["top_probability"]
        self.assertEqual(routes["auto_candidate"]["n"], 0)
        self.assertEqual(routes["stronger_model_candidate"]["n"], 1)

    def test_confidence_is_separate_and_nullable(self):
        items = [record({"a": 0.95, "b": 0.05}, confidence=0.1),
                 record({"a": 0.6, "b": 0.4}, confidence=0.95),
                 record({"a": 0.9, "b": 0.1}, confidence=None)]
        result = summarize(items)
        group = result["overall"]
        self.assertEqual(group["valid"], 3)
        self.assertEqual(group["top_probability_calibration"]["n"], 3)
        self.assertEqual(group["confidence_shape_diagnostic"]["n"], 2)
        self.assertAlmostEqual(group["confidence_shape_diagnostic"]["ece"], 0.475)
        self.assertEqual(group["routes"]["top_probability"]["auto_candidate"]["n"], 2)
        human = group["routes"]["confidence"]["human_candidate"]
        self.assertEqual((human["n"], human["score_n"], human["correct"]), (2, 1, 2))
        self.assertEqual(human["mean_score"], 0.1)
        self.assertIn("NOT a claimed probability", result["metadata"]["confidence"])

    def test_ece_bin_endpoints_and_threshold_endpoints(self):
        group = summarize([record(confidence=c) for c in (0, 0.1, 0.7, 0.9, 1)])["overall"]
        bins = group["confidence_shape_diagnostic"]["bins"]
        self.assertEqual([b["n"] for b in bins], [1, 1, 0, 0, 0, 0, 0, 1, 0, 2])
        self.assertEqual(group["routes"]["confidence"]["auto_candidate"]["n"], 2)
        self.assertEqual(group["routes"]["confidence"]["stronger_model_candidate"]["n"], 1)
        self.assertTrue(bins[-1]["upper_inclusive"])
        self.assertFalse(bins[0]["upper_inclusive"])
        self.assertIsNone(bins[2]["mean_score"])
        group = summarize([record({"a": 0.5, "b": 0.5}), record({"a": 1, "b": 0})])["overall"]
        self.assertEqual(group["top_probability_calibration"]["bins"][5]["n"], 1)
        self.assertEqual(group["top_probability_calibration"]["bins"][9]["n"], 1)

    def test_wilson_boundaries_and_empty_bucket(self):
        for target, lower, upper in [("a", 0.20654931437723745, 1), ("b", 0, 0.7934506856227626)]:
            group = summarize([record({"a": 1, "b": 0}, target=target)])["overall"]
            routes = group["routes"]["top_probability"]
            interval = routes["auto_candidate"]["wilson95"]
            self.assertAlmostEqual(interval["lower"], lower)
            self.assertAlmostEqual(interval["upper"], upper)
            self.assertIsNone(routes["human_candidate"]["wilson95"])
            self.assertIsNone(routes["human_candidate"]["accuracy"])
            self.assertEqual(routes["human_candidate"]["coverage"], 0)

    def test_invalid_scores_labels_and_predictions_count_wrong(self):
        invalid = [record(p) for p in ({}, {"a": 0, "b": 0}, {"a": 0.7, "b": 0.7},
            {"a": True, "b": 0}, {"a": float("nan"), "b": 0}, {"a": float("inf"), "b": 0},
            {"a": -0.1, "b": 1}, {"a": 1.1, "b": 0}, {"": 0.8, "b": 0.2}, {1: 0.8, "b": 0.2})]
        invalid += [record(target="missing"), record(prediction="missing"), record(prediction="b"),
                    record(confidence=True), record(confidence=float("nan")), record(confidence=-0.1),
                    record(confidence=1.1), record(id=""), record(task="")]
        result = summarize(invalid)
        self.assertEqual(result["overall"]["attempted"], len(invalid))
        self.assertEqual(result["overall"]["invalid"], len(invalid))
        self.assertEqual(result["overall"]["accuracy"], 0)
        self.assertIsNone(result["overall"]["brier"])
        self.assertIn("__invalid_task__", result["by_task"])
        json.dumps(result, allow_nan=False)

    def test_high_cardinality_tolerance_is_capped(self):
        probabilities = {str(i): 0.001 for i in range(255)}
        probabilities["0"] = 1
        group = summarize([record(probabilities, target="0", prediction="0")])["overall"]
        self.assertEqual(group["invalid"], 1)

    def test_empty_input_and_missing_confidence_have_no_fake_metrics(self):
        result = summarize([])
        self.assertEqual(result["overall"]["attempted"], 0)
        self.assertIsNone(result["overall"]["accuracy"])
        self.assertIsNone(result["overall"]["top_probability_calibration"]["ece"])
        self.assertIsNone(result["overall"]["routes"]["confidence"]["human_candidate"]["coverage"])
        self.assertEqual(result["by_task"], {})
        group = summarize([record(confidence=None)])["overall"]
        self.assertIsNone(group["confidence_shape_diagnostic"]["ece"])
        self.assertEqual(group["confidence_shape_diagnostic"]["n"], 0)


if __name__ == "__main__":
    unittest.main()
