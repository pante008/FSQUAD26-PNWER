# Stage 1 Summary

## Scope
Synthetic data generation for FIFA 2026 visitor records.

## Deliverables
- CSV and JSON outputs in outputs/
- Generator script with Faker
- Standalone generator without dependencies
- Config-driven settings

## Record schema
- Visitor identity and contact
- Demographics and origin
- Trip details and spend
- Preferences and return flag

## Next steps
- Stage 2: Load to Snowflake via orchestration
- Stage 3: Data quality checks with Great Expectations
