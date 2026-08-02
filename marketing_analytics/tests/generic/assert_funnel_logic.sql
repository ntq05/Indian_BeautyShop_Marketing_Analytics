{% test assert_funnel_logic(model, upper_column, lower_column)%}

SELECT *
FROM {{ model }}
WHERE {{ upper_column }} < {{ lower_column }}

{% endtest %}