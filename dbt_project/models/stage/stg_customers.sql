{{
  config(
    tags = ['shopify']
  )
}}

with base_customers as ( 

    select * from {{ ref('base_customers') }}

), final as (

    select

        customer_id
        ,email
        ,first_name
        ,last_name
        ,phone
        ,created_at_timestamp
        ,state
        
    from base_customers

) select * from final
