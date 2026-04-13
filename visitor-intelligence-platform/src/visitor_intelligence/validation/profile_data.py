"""
Data Profiling Module
Generate detailed statistical profiles of visitor data
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd


class DataProfiler:
    def __init__(self, data_path: str, output_dir: str = "reports"):
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"📊 Loading data for profiling: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"✓ Loaded {len(self.df):,} records")

        self.profile = {
            "timestamp": datetime.now().isoformat(),
            "total_records": len(self.df),
            "total_columns": len(self.df.columns),
            "columns": {},
        }

    def profile_column(self, col_name: str) -> dict:
        col = self.df[col_name]
        col_type = str(col.dtype)

        profile = {
            "name": col_name,
            "type": col_type,
            "missing": int(col.isnull().sum()),
            "missing_pct": float((col.isnull().sum() / len(col) * 100).round(2)),
        }

        if col_type in ["int64", "float64"]:
            profile.update(
                {
                    "min": float(col.min()) if not col.isnull().all() else None,
                    "max": float(col.max()) if not col.isnull().all() else None,
                    "mean": float(col.mean()) if not col.isnull().all() else None,
                    "median": float(col.median()) if not col.isnull().all() else None,
                    "std": float(col.std()) if not col.isnull().all() else None,
                    "quantiles": {
                        "25%": float(col.quantile(0.25)) if not col.isnull().all() else None,
                        "50%": float(col.quantile(0.50)) if not col.isnull().all() else None,
                        "75%": float(col.quantile(0.75)) if not col.isnull().all() else None,
                    },
                }
            )
        else:
            profile.update(
                {
                    "unique_values": int(col.nunique()),
                    "most_common": str(col.mode()[0]) if len(col.mode()) > 0 else None,
                    "value_counts": col.value_counts().to_dict(),
                }
            )

        return profile

    def profile_all_columns(self) -> None:
        print("\n📈 Profiling all columns...")
        for col in self.df.columns:
            print(f"   Profiling {col}...")
            self.profile["columns"][col] = self.profile_column(col)

    def save_profile(self) -> Path:
        profile_path = self.output_dir / "data_profile.json"
        with open(profile_path, "w") as f:
            json.dump(self.profile, f, indent=2)
        print(f"\n📄 Profile saved: {profile_path}")
        return profile_path

    def print_summary(self) -> None:
        print("\n" + "=" * 80)
        print("📊 DATA PROFILE SUMMARY")
        print("=" * 80)
        print(f"\nTotal Records: {self.profile['total_records']:,}")
        print(f"Total Columns: {self.profile['total_columns']}")

        for col_name, col_profile in self.profile["columns"].items():
            print(f"\n  {col_name}:")
            print(f"    Type: {col_profile['type']}")
            print(f"    Missing: {col_profile['missing']} ({col_profile['missing_pct']}%)")
            if "min" in col_profile:
                print(f"    Range: {col_profile['min']} to {col_profile['max']}")
                print(f"    Mean: {col_profile['mean']:.2f}, Std: {col_profile['std']:.2f}")
            else:
                print(f"    Unique: {col_profile['unique_values']}")


def main() -> dict:
    profiler = DataProfiler(
        data_path="data/raw/synthetic_visitors.csv",
        output_dir="reports",
    )

    profiler.profile_all_columns()
    profiler.save_profile()
    profiler.print_summary()
    return profiler.profile


if __name__ == "__main__":
    profile = main()