{{
  config(
    tags = ['shopify']
  )
}}

with stg_customers as ( 

    select * from {{ ref('stg_customers') }}

), final as (

    select
        customer_id
        ,first_name
        ,last_name
        ,email

    from stg_customers
    
) select * from final
