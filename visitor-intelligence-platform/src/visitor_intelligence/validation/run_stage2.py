"""
Stage 2 Main Orchestrator
Run all validation checks and generate comprehensive report
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from visitor_intelligence.validation.data_quality_checks import DataQualityChecker
from visitor_intelligence.validation.profile_data import DataProfiler
from visitor_intelligence.validation.anomaly_detection import AnomalyDetector


def main() -> dict:
    print("\n" + "=" * 80)
    print("🚀 STAGE 2: DATA VALIDATION & QUALITY CHECKS")
    print("=" * 80)

    data_path = "data/raw/visitors_2026.csv"
    output_dir = "reports"

    print("\n📊 Initializing validators...")
    quality_checker = DataQualityChecker(data_path, output_dir, processed_dir="data/processed")
    profiler = DataProfiler(data_path, output_dir)
    anomaly_detector = AnomalyDetector(data_path, output_dir)

    print("\n" + "-" * 80)
    quality_report = quality_checker.run_all_checks()
    quality_checker.save_report()
    quality_checker.save_clean_data()
    quality_checker.print_summary()

    print("\n" + "-" * 80)
    profiler.profile_all_columns()
    profiler.save_profile()
    profiler.print_summary()

    print("\n" + "-" * 80)
    anomaly_detector.run_all_detections()
    anomaly_detector.save_report()
    anomaly_detector.print_summary()

    print("\n" + "-" * 80)
    print("📋 Generating consolidated validation report...")

    consolidated_report = {
        "timestamp": datetime.now().isoformat(),
        "stage": "Stage 2: Data Validation",
        "data_file": str(data_path),
        "quality_checks": quality_report,
        "data_profile": profiler.profile,
        "anomalies": anomaly_detector.anomalies,
        "summary": {
            "total_records": len(quality_checker.df),
            "quality_status": quality_report["overall_status"],
            "anomalies_found": sum(
                v.get("count", v.get("total", 0))
                for v in anomaly_detector.anomalies["anomaly_types"].values()
            ),
        },
    }

    report_path = Path(output_dir) / "stage2_validation_report.json"
    with open(report_path, "w") as f:
        json.dump(consolidated_report, f, indent=2)

    print(f"\n✅ Consolidated report saved: {report_path}")
    
    print("\n" + "=" * 80)
    print("✅ STAGE 2 COMPLETE!")
    print("=" * 80)
    print("\nGenerated Reports:")
    print(f"  ✓ {output_dir}/data_quality_validation.json")
    print(f"  ✓ {output_dir}/data_profile.json")
    print(f"  ✓ {output_dir}/anomaly_detection.json")
    print(f"  ✓ {output_dir}/stage2_validation_report.json")
    print("\nCleaned Data:")
    print(f"  ✓ data/processed/synthetic_visitors_clean.csv")
    print(f"  ✓ data/processed/synthetic_visitors_validated.parquet")
    print("\nNext Steps:")
    print("  1. Review validation reports in 'reports/' directory")
    print("  2. Fix any data quality issues if needed")
    print("  3. Proceed to Stage 3: Data Transformation (dbt)")
    
    return consolidated_report


if __name__ == "__main__":
    report = main()