select
    order_id,
    total_discounts_presentment_amount as discount
from {{ ref('stg_orders') }}
where discount > 0