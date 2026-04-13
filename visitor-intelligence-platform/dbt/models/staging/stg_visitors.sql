-- Staging layer: Clean and deduplicate raw data

select distinct
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
    returning_visitor
from {{ source('raw', 'raw_visitors') }}
where visitor_id is not null