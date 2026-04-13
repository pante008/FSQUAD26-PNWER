"""
Anomaly Detection Module
Detect outliers and unusual patterns in visitor data
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd


class AnomalyDetector:
    def __init__(self, data_path: str, output_dir: str = "reports"):
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"🔎 Loading data for anomaly detection: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Loaded {len(self.df):,} records")

        self.anomalies = {
            "timestamp": datetime.now().isoformat(),
            "total_records": len(self.df),
            "anomaly_types": {},
        }

    def detect_outliers_iqr(self, col_name: str, threshold: float = 1.5) -> list:
        if col_name not in self.df.columns:
            return []

        col = self.df[col_name]
        Q1 = col.quantile(0.25)
        Q3 = col.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - threshold * IQR
        upper = Q3 + threshold * IQR
        return col[(col < lower) | (col > upper)].index.tolist()

    def detect_high_spenders(self) -> dict:
        print("\n🔍 Detecting high spenders...")
        if "spend_total_usd" not in self.df.columns:
            return {}
        threshold = self.df["spend_total_usd"].quantile(0.99)
        high = self.df[self.df["spend_total_usd"] > threshold]
        result = {
            "count": len(high),
            "threshold": float(threshold),
            "percentage": float(len(high) / len(self.df) * 100),
            "avg_spend_total_usd": float(high["spend_total_usd"].mean()),
        }
        print(f"   Found {result['count']} high spenders (>{threshold:.2f})")
        return result

    def detect_long_stays(self) -> dict:
        print("\n🔍 Detecting long stays...")
        if "stay_nights" not in self.df.columns:
            return {}
        threshold = self.df["stay_nights"].quantile(0.99)
        long_stays = self.df[self.df["stay_nights"] > threshold]
        result = {
            "count": len(long_stays),
            "threshold": float(threshold),
            "percentage": float(len(long_stays) / len(self.df) * 100),
        }
        print(f"   Found {result['count']} long stays (>{threshold:.0f})")
        return result

    def detect_data_quality_issues(self) -> dict:
        print("\n🔍 Detecting data quality issues...")
        issues = {}
        issue_count = 0

        if "email" in self.df.columns:
            invalid_emails = self.df[~self.df["email"].str.contains("@", na=False)]
            if len(invalid_emails) > 0:
                issues["invalid_emails"] = len(invalid_emails)
                issue_count += len(invalid_emails)

        if "phone" in self.df.columns:
            invalid_phones = self.df[self.df["phone"].str.len() < 5]
            if len(invalid_phones) > 0:
                issues["invalid_phones"] = len(invalid_phones)
                issue_count += len(invalid_phones)

        print(f"   Found {issue_count} quality issues")
        return {"issues": issues, "total": issue_count}

    def run_all_detections(self) -> None:
        print("\n" + "=" * 80)
        print("🔎 STARTING ANOMALY DETECTION")
        print("=" * 80)

        self.anomalies["anomaly_types"]["high_spenders"] = self.detect_high_spenders()
        self.anomalies["anomaly_types"]["long_stays"] = self.detect_long_stays()
        self.anomalies["anomaly_types"]["data_quality"] = self.detect_data_quality_issues()

    def save_report(self) -> Path:
        report_path = self.output_dir / "anomaly_detection.json"
        with open(report_path, "w") as f:
            json.dump(self.anomalies, f, indent=2)
        print(f"\n📄 Report saved: {report_path}")
        return report_path

    def print_summary(self) -> None:
        print("\n" + "=" * 80)
        print("🔎 ANOMALY DETECTION SUMMARY")
        print("=" * 80)

        for anomaly_type, data in self.anomalies["anomaly_types"].items():
            print(f"\n{anomaly_type}:")
            for key, value in data.items():
                print(f"  {key}: {value}")


def main() -> dict:
    detector = AnomalyDetector(
        data_path="data/raw/synthetic_visitors.csv",
        output_dir="reports",
    )

    detector.run_all_detections()
    detector.save_report()
    detector.print_summary()
    return detector.anomalies


if __name__ == "__main__":
    anomalies = main()