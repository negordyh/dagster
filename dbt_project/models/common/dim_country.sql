{{
  config(
    tags = ['shopify']
  )
}}

with country as (

    select distinct 
    
        country_name
        ,country_code

    from {{ ref('country_codes') }}

)
select 
    * 
    ,{{ dbt_utils.generate_surrogate_key(['country_code']) }} as dim_country_sk
from country
where country_code is not null