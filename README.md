# Visitor Intelligence Platform

This project builds a visitor analytics pipeline that:

1. generates realistic visitor data,
2. validates the data for quality issues,
3. detects anomalies,
4. transforms the data with dbt,
5. and produces reports for analysis.

## What happens in this project step by step

1. **Data generation**  
   Synthetic visitor data is created in `src/visitor_intelligence/data/generate_realistic_visitor_data.py`.

2. **Raw data storage**  
   The generated data is saved in the project data directory for downstream processing.

3. **Data profiling**  
   The dataset is profiled to understand structure, distributions, and missing values.

4. **Data quality checks**  
   Validation rules are run to detect invalid, missing, or inconsistent records.

5. **Anomaly detection**  
   Unusual visitor behavior is identified and saved into reports.

6. **dbt transformations**  
   dbt models transform the staged data into intermediate and mart tables.

7. **Report generation**  
   Final validation and summary reports are written to the `reports/` folder.

## Project structure

- `src/visitor_intelligence/` — Python package for generation and validation
- `dbt/` — dbt project with models and build artifacts
- `data/raw/` — raw generated data
- `reports/` — validation and analysis outputs

## How to run the project

### 1. Clone the repository
```bash
git clone https://github.com/pante008/FSQUAD26-PNWER.git
cd FSQUAD26-PNWER
```

### 2. Go to the project folder
```bash
cd visitor-intelligence-platform
```

### 3. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

### 5. Generate the visitor data
```bash
python -m visitor_intelligence.data.generate_realistic_visitor_data
```

### 6. Run validation and analysis
```bash
python -m visitor_intelligence.validation.run_stage2
```

### 7. Run dbt
```bash
cd dbt
dbt deps
dbt debug
dbt run
dbt test
```

## Outputs

After running the project, check these folders:

- `data/raw/` — generated raw data
- `reports/` — quality, anomaly, and summary reports
- `dbt/target/` — dbt build artifacts and compiled output

## Notes

- Make sure Python 3.11+ is installed.
- Run dbt commands only after configuring your dbt profile.
- Some generated files may be large and should not usually be committed.
