-- This will create a physical table in mysql
{{config(materialized='table')}}

-- Reference the fact model to get calculated KPIs
WITH base AS (
    SELECT * FROM {{ref('fct_campaign_kpis')}}
)

SELECT 
    Brand,
    COUNT(*) AS total_campaigns,
    SUM(REVENUE) AS total_revenue,
    SUM(calc_total_spend) AS total_spend,
    SUM(calc_profit) AS total_profit,

    ROUND(SUM(Clicks) / NULLIF(SUM(Impressions), 0), 4) AS overall_ctr,
    ROUND(SUM(Leads) / NULLIF(SUM(Clicks), 0), 4) AS overall_lead_rate,
    ROUND(SUM(conversions) / NULLIF(SUM(Leads), 0), 4) AS overall_conv_rate,
    ROUND(SUM(conversions) / NULLIF(SUM(Clicks), 0), 4) AS overall_cvr,
    ROUND(SUM(calc_total_spend) / NULLIF(SUM(Conversions), 0), 2) AS overall_cpa,
    ROUND(
        (SUM(Revenue) - SUM(calc_total_spend)) / NULLIF(SUM(calc_total_spend), 0), 
        4
    ) AS overall_roi,

    SUM(CASE WHEN campaign_status = 'SCALE' THEN 1 ELSE 0 END) AS scale_count,
    SUM(CASE WHEN campaign_status = 'WATCH' THEN 1 ELSE 0 END) AS watch_count,
    SUM(CASE WHEN campaign_status = 'STOP' THEN 1 ELSE 0 END) AS stop_count

FROM base
GROUP BY Brand