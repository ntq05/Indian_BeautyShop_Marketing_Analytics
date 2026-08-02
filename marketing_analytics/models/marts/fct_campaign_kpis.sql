{{config(materialized='table')}}

-- Reference the staging model to get cleaned and deduplicated campaign data
WITH stg_data AS (
    SELECT * FROM {{ref('stg_campaigns')}}
),

calculated_kpis AS(
    SELECT
        Campaign_ID,
        Brand,
        Campaign_Type,
        Language,
        Customer_Segment,
        Target_Audience,
        Duration,
        Campaign_Date,
        DATE_FORMAT(Campaign_Date, '%Y-%m') AS campaign_month,
        Impressions,
        Clicks,
        Leads,
        Conversions,
        Revenue,
        Acquisition_Cost AS CPA,

        -- Calculate KPIs
        ROUND(Acquisition_Cost * Conversions, 2) AS calc_total_spend,
        ROUND(Revenue - (Acquisition_Cost * Conversions), 2) AS calc_profit,

        ROUND(Clicks/ NULLIF(impressions, 0), 4) AS calc_ctr,
        ROUND(leads / NULLIF(clicks, 0), 4) AS calc_lead_rate,
        ROUND(conversions / NULLIF(leads, 0), 4) AS calc_lead_conversion_rate, -- LCR
        ROUND(conversions / NULLIF(clicks, 0), 4) AS calc_cvr,
        ROUND(revenue / NULLIF(conversions, 0), 2) AS calc_aov,

        ROUND(
            (revenue - (Acquisition_Cost * Conversions)) / NULLIF((Acquisition_Cost * Conversions), 0), 4
        ) AS calc_roi

    FROM stg_data
)

SELECT
    *,
    CASE
        WHEN calc_roi >= 0.5 AND calc_profit > 0 AND calc_cvr >= 0.05 THEN 'SCALE'
        WHEN calc_roi < 0 OR calc_profit < 0 THEN 'STOP'
        ELSE 'WATCH'
    END AS campaign_status
FROM calculated_kpis