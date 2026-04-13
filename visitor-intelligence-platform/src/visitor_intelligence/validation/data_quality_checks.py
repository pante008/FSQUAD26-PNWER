"""
Data Quality Validation Module
Validates synthetic visitor data for completeness, accuracy, and consistency
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

import numpy as np
import pandas as pd


EXPECTED_COLUMNS = [
    "visitor_id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "age",
    "gender",
    "country",
    "origin_region",
    "group_size",
    "arrival_date",
    "departure_date",
    "stay_nights",
    "accommodation_type",
    "spend_total_usd",
    "favorite_team",
    "returning_visitor",
]

GENDERS = ["Female", "Male", "Non-binary", "Prefer not to say"]
ACCOMMODATION = ["Hotel", "Airbnb", "Hostel", "Short-term rental", "Friends/Family"]


class DataQualityChecker:
    def __init__(self, data_path: str, output_dir: str = "reports", processed_dir: str = "data/processed"):
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.processed_dir = Path(processed_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        print(f"📊 Loading data from: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Loaded {len(self.df):,} records with {len(self.df.columns)} columns")

        self.quality_report: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "file": str(self.data_path),
            "total_records": len(self.df),
            "total_columns": len(self.df.columns),
            "checks": {},
        }

    def check_schema(self) -> Dict[str, Any]:
        print("\n🔍 Checking schema...")
        missing = [c for c in EXPECTED_COLUMNS if c not in self.df.columns]
        extra = [c for c in self.df.columns if c not in EXPECTED_COLUMNS]

        result = {
            "missing_columns": missing,
            "extra_columns": extra,
            "status": "✅ PASS" if not missing else "❌ FAIL",
        }

        if missing:
            print(f"   ❌ Missing columns: {missing}")
        if extra:
            print(f"   ⚠️ Extra columns: {extra}")
        print(f"   {result['status']}")
        return result

    def check_duplicates(self) -> Dict[str, Any]:
        print("\n🔍 Checking for duplicates...")
        duplicate_rows = int(self.df.duplicated().sum())
        duplicate_ids = int(self.df["visitor_id"].duplicated().sum()) if "visitor_id" in self.df.columns else 0

        result = {
            "total_duplicates": duplicate_rows,
            "duplicate_ids": duplicate_ids,
            "status": "✅ PASS" if duplicate_rows == 0 else "❌ FAIL",
        }

        print(f"   Total duplicates: {duplicate_rows}")
        print(f"   Duplicate IDs: {duplicate_ids}")
        print(f"   {result['status']}")
        return result

    def check_missing_values(self) -> Dict[str, Any]:
        print("\n🔍 Checking for missing values...")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)

        missing_summary = {}
        total_missing = 0

        for col in self.df.columns:
            if missing[col] > 0:
                missing_summary[col] = {
                    "count": int(missing[col]),
                    "percentage": float(missing_pct[col]),
                }
                total_missing += int(missing[col])

        result = {
            "total_missing_cells": int(total_missing),
            "columns_with_missing": missing_summary,
            "status": "✅ PASS" if total_missing == 0 else "⚠️ WARNING",
        }

        if total_missing == 0:
            print("   No missing values found!")
        else:
            print(f"   Total missing cells: {total_missing}")
            for col, info in missing_summary.items():
                print(f"   - {col}: {info['count']} ({info['percentage']}%)")

        print(f"   {result['status']}")
        return result

    def check_data_types(self) -> Dict[str, Any]:
        print("\n🔍 Checking data types...")
        type_mapping = {
            "visitor_id": "object",
            "first_name": "object",
            "last_name": "object",
            "email": "object",
            "phone": "object",
            "age": ("int64", "float64"),
            "gender": "object",
            "country": "object",
            "origin_region": "object",
            "group_size": ("int64", "float64"),
            "arrival_date": "object",
            "departure_date": "object",
            "stay_nights": ("int64", "float64"),
            "accommodation_type": "object",
            "spend_total_usd": ("float64", "int64"),
            "favorite_team": "object",
            "returning_visitor": ("bool", "int64"),
        }

        type_issues = {}
        all_pass = True

        for col, expected_type in type_mapping.items():
            if col in self.df.columns:
                actual_type = str(self.df[col].dtype)
                if isinstance(expected_type, tuple):
                    type_match = actual_type in expected_type
                else:
                    type_match = actual_type == expected_type

                if not type_match:
                    type_issues[col] = {"expected": str(expected_type), "actual": actual_type}
                    all_pass = False
                    print(f"   ❌ {col}: Expected {expected_type}, got {actual_type}")
                else:
                    print(f"   ✅ {col}: {actual_type}")

        result = {
            "type_issues": type_issues,
            "status": "✅ PASS" if all_pass else "⚠️ WARNING",
        }
        print(f"   {result['status']}")
        return result

    def check_value_ranges(self) -> Dict[str, Any]:
        print("\n🔍 Checking value ranges...")
        range_issues = {}
        all_pass = True

        if "age" in self.df.columns:
            out = ((self.df["age"] < 18) | (self.df["age"] > 80)).sum()
            if out > 0:
                range_issues["age"] = {"issue": "Out of range (18-80)", "count": int(out)}
                all_pass = False
                print(f"   ⚠️ Age: {out} out of range")
            else:
                print("   ✅ Age: All values in range 18-80")

        if "group_size" in self.df.columns:
            out = ((self.df["group_size"] < 1) | (self.df["group_size"] > 6)).sum()
            if out > 0:
                range_issues["group_size"] = {"issue": "Out of range (1-6)", "count": int(out)}
                all_pass = False
                print(f"   ⚠️ Group size: {out} out of range")
            else:
                print("   ✅ Group size: All values in range 1-6")

        if "stay_nights" in self.df.columns:
            out = ((self.df["stay_nights"] < 2) | (self.df["stay_nights"] > 18)).sum()
            if out > 0:
                range_issues["stay_nights"] = {"issue": "Out of range (2-18)", "count": int(out)}
                all_pass = False
                print(f"   ⚠️ Stay nights: {out} out of range")
            else:
                print("   ✅ Stay nights: All values in range 2-18")

        if "spend_total_usd" in self.df.columns:
            out = (self.df["spend_total_usd"] < 100).sum()
            if out > 0:
                range_issues["spend_total_usd"] = {"issue": "Below minimum 100", "count": int(out)}
                all_pass = False
                print(f"   ⚠️ Spend total: {out} below minimum")
            else:
                print("   ✅ Spend total: All values >= 100")

        result = {
            "range_issues": range_issues,
            "status": "✅ PASS" if all_pass else "⚠️ WARNING",
        }
        print(f"   {result['status']}")
        return result

    def check_categorical_values(self) -> Dict[str, Any]:
        print("\n🔍 Checking categorical values...")
        expected = {
            "gender": GENDERS,
            "accommodation_type": ACCOMMODATION,
        }

        issues = {}
        all_pass = True

        for col, allowed in expected.items():
            if col in self.df.columns:
                invalid_mask = ~self.df[col].isin(allowed)
                invalid_count = int(invalid_mask.sum())
                if invalid_count > 0:
                    issues[col] = {
                        "expected": allowed,
                        "invalid_count": invalid_count,
                        "invalid_values": self.df.loc[invalid_mask, col].unique().tolist(),
                    }
                    all_pass = False
                    print(f"   ⚠️ {col}: {invalid_count} invalid values")
                else:
                    print(f"   ✅ {col}: All values valid")

        result = {"categorical_issues": issues, "status": "✅ PASS" if all_pass else "⚠️ WARNING"}
        print(f"   {result['status']}")
        return result

    def check_date_consistency(self) -> Dict[str, Any]:
        print("\n🔍 Checking date consistency...")
        issues = {}
        all_pass = True

        if all(c in self.df.columns for c in ["arrival_date", "departure_date", "stay_nights"]):
            arrival = pd.to_datetime(self.df["arrival_date"], errors="coerce")
            departure = pd.to_datetime(self.df["departure_date"], errors="coerce")
            stay = self.df["stay_nights"].astype("float", errors="ignore")

            invalid_dates = arrival.isna().sum() + departure.isna().sum()
            mismatch = ((departure - arrival).dt.days != stay).sum()

            if invalid_dates > 0:
                issues["invalid_dates"] = int(invalid_dates)
                all_pass = False
                print(f"   ⚠️ Invalid dates: {invalid_dates}")
            if mismatch > 0:
                issues["stay_nights_mismatch"] = int(mismatch)
                all_pass = False
                print(f"   ⚠️ stay_nights mismatches: {mismatch}")

            if all_pass:
                print("   ✅ Dates consistent with stay_nights")

        result = {"date_issues": issues, "status": "✅ PASS" if all_pass else "⚠️ WARNING"}
        print(f"   {result['status']}")
        return result

    def run_all_checks(self) -> Dict[str, Any]:
        print("\n" + "=" * 80)
        print("🔍 STARTING DATA QUALITY VALIDATION")
        print("=" * 80)

        self.quality_report["checks"]["schema"] = self.check_schema()
        self.quality_report["checks"]["duplicates"] = self.check_duplicates()
        self.quality_report["checks"]["missing_values"] = self.check_missing_values()
        self.quality_report["checks"]["data_types"] = self.check_data_types()
        self.quality_report["checks"]["value_ranges"] = self.check_value_ranges()
        self.quality_report["checks"]["categorical_values"] = self.check_categorical_values()
        self.quality_report["checks"]["date_consistency"] = self.check_date_consistency()

        all_pass = all(
            check.get("status", "❌ FAIL").startswith("✅") for check in self.quality_report["checks"].values()
        )
        self.quality_report["overall_status"] = "✅ ALL CHECKS PASSED" if all_pass else "⚠️ SOME WARNINGS"
        return self.quality_report

    def save_report(self) -> Path:
        report_path = self.output_dir / "data_quality_validation.json"
        with open(report_path, "w") as f:
            json.dump(self.quality_report, f, indent=2)
        print(f"\n📄 Report saved: {report_path}")
        return report_path

    def save_clean_data(self) -> Dict[str, Path]:
        cleaned = self.df.drop_duplicates().copy()

        csv_path = self.processed_dir / "synthetic_visitors_clean.csv"
        parquet_path = self.processed_dir / "synthetic_visitors_validated.parquet"

        cleaned.to_csv(csv_path, index=False)
        cleaned.to_parquet(parquet_path, index=False)

        print(f"\n✅ Cleaned CSV: {csv_path}")
        print(f"✅ Validated Parquet: {parquet_path}")

        return {"csv": csv_path, "parquet": parquet_path}

    def print_summary(self) -> None:
        print("\n" + "=" * 80)
        print("📊 DATA QUALITY SUMMARY")
        print("=" * 80)

        print(f"\nTotal Records: {self.quality_report['total_records']:,}")
        print(f"Total Columns: {self.quality_report['total_columns']}")
        print(f"\nOverall Status: {self.quality_report['overall_status']}")

        print("\nCheck Results:")
        for check_name, result in self.quality_report["checks"].items():
            status = result.get("status", "UNKNOWN")
            print(f"  {check_name:30s}: {status}")

        print("\n" + "=" * 80)


def main() -> Dict[str, Any]:
    checker = DataQualityChecker(
        data_path="data/raw/synthetic_visitors.csv",
        output_dir="reports",
        processed_dir="data/processed",
    )

    checker.run_all_checks()
    checker.save_report()
    checker.save_clean_data()
    checker.print_summary()
    return checker.quality_report


if __name__ == "__main__":
    report = main()