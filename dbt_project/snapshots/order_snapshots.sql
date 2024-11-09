{% snapshot orders_snaphot %}

    {{
        config(

          target_schema='test_analytics',
          strategy='timestamp',
          unique_key='order_id',
          updated_at='updated_at_timestamp',
          tags=["shopify"],
        )
    }}

    select * from {{ ref('stg_orders') }}
        where updated_at_timestamp = (
            select max(updated_at_timestamp) 
            from {{ ref('stg_orders') }}
        )

{% endsnapshot %}