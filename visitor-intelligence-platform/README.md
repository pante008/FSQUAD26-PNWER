# Visitor Intelligence Platform (Stage 1)

Synthetic data generation for FIFA 2026 visitor analytics. Stage 1 produces 100,000 realistic visitor records with consistent distributions and business-friendly fields.

## What this stage does
- Generates 100,000 visitor records
- Saves CSV + JSON to outputs/
- Includes realistic distributions (countries, teams, dates, spend)

## Project layout
- src/visitor_intelligence/data/generate_synthetic_data.py
- src/visitor_intelligence/data/generate_synthetic_data_standalone.py
- config/config.py
- outputs/

## Run
1. Install deps
   - pip install -r requirements.txt
2. Generate data
   - python -m visitor_intelligence.data.generate_synthetic_data

Standalone (no deps):
- python -m visitor_intelligence.data.generate_synthetic_data_standalone

## Output columns
visitor_id, first_name, last_name, email, phone, age, gender, country, origin_region, group_size, arrival_date, departure_date, stay_nights, accommodation_type, spend_total_usd, favorite_team, returning_visitor
