{% macro trim_email(email) -%}
    {%- if email is none -%}
        NULL
    {%- else -%}
        {{ email | trim }}
    {%- endif -%}
{%- endmacro %}
