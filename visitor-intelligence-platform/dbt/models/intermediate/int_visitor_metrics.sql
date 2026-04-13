-- Intermediate layer: Calculate metrics

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

    case
        when total_spending < 500 then 'Budget'
        when total_spending < 1500 then 'Standard'
        when total_spending < 3000 then 'Premium'
        else 'VIP'
    end as spending_tier,

    case
        when stay_nights <= 3 then 'Short Stay'
        when stay_nights <= 7 then 'Medium Stay'
        else 'Long Stay'
    end as stay_duration

from {{ ref('stg_visitors') }}