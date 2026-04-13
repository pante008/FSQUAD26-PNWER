-- Dimension table: Visitor characteristics

select
    country,
    spending_tier,
    stay_duration,
    accommodation_type,
    primary_activity,
    count(distinct visitor_id) as visitor_count,
    round(avg(total_spending), 2) as avg_total_spending,
    round(avg(daily_spending), 2) as avg_daily_spending,
    round(avg(stay_nights), 1) as avg_stay_nights,
    sum(case when returning_visitor = true then 1 else 0 end) as returning_visitor_count
from VISITORS_DB.STAGING_INTERMEDIATE.int_visitor_metrics
group by
    country,
    spending_tier,
    stay_duration,
    accommodation_type,
    primary_activity