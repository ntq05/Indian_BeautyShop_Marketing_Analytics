USE marketing_analytics;

SELECT 
    COUNT(*) AS num_camp,
    COUNT(DISTINCT Brand) AS num_brand,
    COUNT(DISTINCT Campaign_Type) AS num_camp_type,
    AVG(DURATION) AS avg_duration,
    SUM(Impressions) AS sum_impression,
    AVG(Impressions) as avg_impression,
    SUM(Clicks) AS sum_click,
    AVG(Clicks) as avg_click,
    SUM(Leads) AS sum_lead,
    AVG(Leads) as avg_lead,
    SUM(Revenue) AS sum_revenue,
    AVG(Revenue) as avg_revenue,
    SUM(CPA) AS sum_cpa,
    AVG(CPA) as avg_cpa,
    SUM(calc_roi) AS sum_roi,
    AVG(calc_roi) as avg_roit
FROM fct_campaign_kpis;

SELECT 
	Brand,
    COUNT(*) AS num_camp,
    COUNT(DISTINCT Brand) AS num_brand,
    COUNT(DISTINCT Campaign_Type) AS num_camp_type,
    AVG(DURATION) AS avg_duration,
    SUM(Impressions) AS sum_impression,
    AVG(Impressions) as avg_impression,
    SUM(Clicks) AS sum_click,
    AVG(Clicks) as avg_click,
    SUM(Leads) AS sum_lead,
    AVG(Leads) as avg_lead,
    SUM(Revenue) AS sum_revenue,
    AVG(Revenue) as avg_revenue,
    SUM(CPA) AS sum_cpa,
    AVG(CPA) as avg_cpa,
    SUM(calc_roi) AS sum_roi,
    AVG(calc_roi) as avg_roit
FROM fct_campaign_kpis
GROUP BY Brand;

SELECT 
	Campaign_Type,
    COUNT(*) AS num_camp,
    COUNT(DISTINCT Brand) AS num_brand,
    COUNT(DISTINCT Campaign_Type) AS num_camp_type,
    AVG(DURATION) AS avg_duration,
    SUM(Impressions) AS sum_impression,
    AVG(Impressions) as avg_impression,
    SUM(Clicks) AS sum_click,
    AVG(Clicks) as avg_click,
    SUM(Leads) AS sum_lead,
    AVG(Leads) as avg_lead,
    SUM(Revenue) AS sum_revenue,
    AVG(Revenue) as avg_revenue,
    SUM(CPA) AS sum_cpa,
    AVG(CPA) as avg_cpa,
    SUM(calc_roi) AS sum_roi,
    AVG(calc_roi) as avg_roit
FROM fct_campaign_kpis
GROUP BY Campaign_Type;

SELECT 
	Customer_Segment,,
    COUNT(*) AS num_camp,
    COUNT(DISTINCT Brand) AS num_brand,
    COUNT(DISTINCT Campaign_Type) AS num_camp_type,
    AVG(DURATION) AS avg_duration,
    SUM(Impressions) AS sum_impression,
    AVG(Impressions) as avg_impression,
    SUM(Clicks) AS sum_click,
    AVG(Clicks) as avg_click,
    SUM(Leads) AS sum_lead,
    AVG(Leads) as avg_lead,
    SUM(Revenue) AS sum_revenue,
    AVG(Revenue) as avg_revenue,
    SUM(CPA) AS sum_cpa,
    AVG(CPA) as avg_cpa,
    SUM(calc_roi) AS sum_roi,
    AVG(calc_roi) as avg_roit
FROM fct_campaign_kpis
GROUP BY Customer_Segment;

SELECT 
	Language,
    COUNT(*) AS num_camp,
    COUNT(DISTINCT Brand) AS num_brand,
    COUNT(DISTINCT Campaign_Type) AS num_camp_type,
    AVG(DURATION) AS avg_duration,
    SUM(Impressions) AS sum_impression,
    AVG(Impressions) as avg_impression,
    SUM(Clicks) AS sum_click,
    AVG(Clicks) as avg_click,
    SUM(Leads) AS sum_lead,
    AVG(Leads) as avg_lead,
    SUM(Revenue) AS sum_revenue,
    AVG(Revenue) as avg_revenue,
    SUM(CPA) AS sum_cpa,
    AVG(CPA) as avg_cpa,
    SUM(calc_roi) AS sum_roi,
    AVG(calc_roi) as avg_roit
FROM fct_campaign_kpis
GROUP BY Language;