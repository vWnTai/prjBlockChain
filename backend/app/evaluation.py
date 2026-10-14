"""Evaluator only. Labels never enter the AML engine."""

from collections import defaultdict


def classification(actual: set, predicted: set, universe: set) -> dict:
    tp, fp, fn = len(actual & predicted), len(predicted - actual), len(actual - predicted)
    tn = len(universe - (actual | predicted))
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    return {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "precision": precision,
        "recall": recall,
        "FPR": fp / (fp + tn) if fp + tn else None,
        "F1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None,
    }


def evaluate(truth: dict[str, list[str]], assessments: list[tuple[str, dict]], alerts: list[dict]) -> dict:
    universe = {h for h, _ in assessments}
    actual = set().union(*(set(v) for v in truth.values())) if truth else set()
    online = {h for h, a in assessments if a["score"] >= 70}
    retrospective = set().union(*(set(a["evidence"]) for a in alerts)) if alerts else set()
    by_pattern = {}
    campaigns = []
    for pattern, hashes in truth.items():
        expected = set(hashes)
        predicted = {h for h, a in assessments if any(hit["code"] == pattern for hit in a["hits"])}
        relevant = [a for a in alerts if a["code"] == pattern]
        evidence = set().union(*(set(a["evidence"]) for a in relevant)) if relevant else set()
        match = max((len(expected & set(a["evidence"])) / len(expected) for a in relevant), default=0)
        by_pattern[pattern] = {
            "online": classification(expected, predicted, universe),
            "retrospective": classification(expected, evidence, universe),
            "campaign_detected": match >= 0.5,
            "core_overlap": match,
        }
        campaigns.append(match >= 0.5)
    counts = defaultdict(int)
    for a in alerts:
        counts[a["code"]] += 1
    return {
        "scope": "single synthetic run; not an independent held-out benchmark",
        "transaction_count": len(universe),
        "labelled_transaction_count": len(actual),
        "prevalence": len(actual) / len(universe) if universe else 0,
        "online": classification(actual, online, universe),
        "retrospective": classification(actual, retrospective, universe),
        "patterns": by_pattern,
        "campaigns_detected": sum(campaigns),
        "campaign_count": len(campaigns),
        "alerts_by_detector": dict(counts),
        "alerts_per_1000_tx": len(alerts) * 1000 / len(universe) if universe else 0,
    }
