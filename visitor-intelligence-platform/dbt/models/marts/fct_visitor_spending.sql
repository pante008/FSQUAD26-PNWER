-- Final fact table: Analytics-ready

select
    visitor_id,
    first_name,
    last_name,
    email,
    phone,
    age,
    gender,
    country,
    origin_region,
    group_size,
    arrival_date,
    departure_date,
    stay_nights,
    accommodation_type,
    daily_spending,
    total_spending,
    group_total_spending,
    primary_activity,
    ticket_type,
    booking_source,
    returning_visitor,
    spending_tier,
    stay_duration,
    row_number() over (order by total_spending desc) as spending_rank
from {{ ref('int_visitor_metrics') }}
order by total_spending desc