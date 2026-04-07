#!/usr/bin/env python3
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

DATASET_ROOT = Path("test_samples")
CATEGORIES = {
    "paper_pocs": "attack",
    "synthetic": "attack",
    "clean": "clean"
}

def run_on_email(eml_path: Path) -> Tuple[str, float, bool]:
    cmd = [sys.executable, "main.py", "--input", str(eml_path), "--summary"]
    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=False)
        elapsed = time.time() - start
        if result.returncode != 0:
            combined_output = (result.stdout + result.stderr).lower()
            if "no html part" in combined_output:
                return "Safe", elapsed, True
            else:
                return f"ERROR: {result.returncode}", elapsed, False
        output = result.stdout.strip()
        if "(" in output and ")" in output:
            label = output.split("(")[0].strip()
        else:
            label = output.strip()
        return label, elapsed, True
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 10.0, False
    except Exception as e:
        return f"EXCEPTION: {e}", time.time() - start, False

def evaluate_category(category: str, expected_type: str) -> Dict:
    folder = DATASET_ROOT / category
    if not folder.exists():
        return {"files": [], "detected": 0, "total": 0, "times": [], "errors": 0}
    eml_files = list(folder.glob("*.eml"))
    if not eml_files:
        return {"files": [], "detected": 0, "total": 0, "times": [], "errors": 0}
    results = []
    detected = 0
    times = []
    errors = 0
    for eml in eml_files:
        label, elapsed, success = run_on_email(eml)
        if not success:
            errors += 1
            results.append((eml.name, label, elapsed, "FAIL"))
        else:
            times.append(elapsed)
            if expected_type == "attack":
                if label != "Safe":
                    detected += 1
            else:
                if label != "Safe":
                    detected += 1
            results.append((eml.name, label, elapsed, "OK"))
    total = len(eml_files)
    return {
        "files": results,
        "detected": detected,
        "total": total,
        "times": times,
        "errors": errors
    }

def main():
    print("=" * 70)
    print("EMailGuard Evaluation on Full Dataset")
    print("=" * 70)
    all_times = []
    summary = {}
    for category, expected_type in CATEGORIES.items():
        print(f"\n--- Category: {category} (expected: {expected_type}) ---")
        stats = evaluate_category(category, expected_type)
        summary[category] = stats
        all_times.extend(stats["times"])
        if stats["total"] == 0:
            print("  No .eml files found.")
            continue
        print(f"  Total emails: {stats['total']}")
        print(f"  Errors: {stats['errors']}")
        if stats["times"]:
            avg_time = sum(stats["times"]) / len(stats["times"])
            print(f"  Avg time: {avg_time:.3f} sec")
        if expected_type == "attack":
            detection_rate = (stats["detected"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            print(f"  Detection rate: {stats['detected']}/{stats['total']} = {detection_rate:.1f}%")
        else:
            fp_rate = (stats["detected"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            print(f"  False positive rate: {stats['detected']}/{stats['total']} = {fp_rate:.1f}%")
        if stats["files"]:
            print("  Sample results (first 3):")
            for name, label, elapsed, status in stats["files"][:3]:
                print(f"    {name}: {label} ({elapsed:.2f}s) [{status}]")
    if all_times:
        overall_avg = sum(all_times) / len(all_times)
        print("\n" + "=" * 70)
        print(f"Overall average processing time per email: {overall_avg:.3f} seconds")
        print("=" * 70)
    print("\n" + "-" * 70)
    print("SUMMARY METRICS")
    print("-" * 70)
    for category, stats in summary.items():
        if stats["total"] == 0:
            continue
        if CATEGORIES[category] == "attack":
            rate = (stats["detected"] / stats["total"]) * 100
            print(f"{category:12} : Detection = {rate:.1f}% ({stats['detected']}/{stats['total']})")
        else:
            rate = (stats["detected"] / stats["total"]) * 100
            print(f"{category:12} : False Pos = {rate:.1f}% ({stats['detected']}/{stats['total']})")

if __name__ == "__main__":
    main()