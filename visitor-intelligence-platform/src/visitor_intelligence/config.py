from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GenerationConfig:
    """Configuration for synthetic visitor generation."""

    records: int = 100_000
    seed: int = 42
    output_dir: Path = Path("data/raw")
    csv_name: str = "visitors_2026.csv"
    json_name: str = "visitors_2026.json"


DEFAULT_CONFIG = GenerationConfig()
