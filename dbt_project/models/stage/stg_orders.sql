{{
  config(
    tags = ['shopify']
  )
}}

with base_orders as ( 

    select * from {{ ref('base_orders') }}

), final as (

    select

        order_id
        ,customer_id
        ,financial_status
        ,fulfillment_status
        ,tags
        ,payment_gateway_names
        ,presentment_currency
        ,total_line_items_price_presentment_amount
        ,total_discounts_presentment_amount
        ,subtotal_price_presentment_amount
        ,total_tax_presentment_amount
        ,total_shipping_price_presentment_amount
        ,total_price_presentment_amount
        ,created_at_timestamp
        ,updated_at_timestamp
        ,cancelled_at_timestamp
        ,order_status_url

    from base_orders

) select * from final
