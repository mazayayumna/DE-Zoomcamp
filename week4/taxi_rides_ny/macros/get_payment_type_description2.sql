{#
    this macro returns the desc of payment type for yellow, payment type is int
#}

{% macro get_payment_type_description2(payment_type) -%}

    case cast( {{payment_type}} as string)
        when '1' then 'Credit card'
        when '2' then 'Cash'
        when '3' then 'No charge'
        when '4' then 'Dispute'
        when '5' then 'Unknown'
        when '6' then 'Voided trip'
        else 'EMPTY'
    end

{%- endmacro %}