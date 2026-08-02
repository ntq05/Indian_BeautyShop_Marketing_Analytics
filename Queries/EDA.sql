USE marketing_analytics;

SELECT COUNT(*) FROM campaigns;

SELECT DISTINCT Campaign_Type from campaigns;
SELECT DISTINCT Target_Audience from campaigns;
SELECT DISTINCT Language from campaigns;
SELECT DISTINCT Customer_Segment from campaigns;

-- null detections
SELECT SUM(CASE WHEN Impressions IS NULL THEN 1 ELSE 0 END) AS null_impressions,
	   SUM(CASE WHEN Clicks IS NULL THEN 1 ELSE 0 END) AS null_clicks,
       SUM(CASE WHEN Revenue IS NULL THEN 1 ELSE 0 END) AS null_revenue,
       SUM(CASE WHEN Campaign_ID IS NULL THEN 1 ELSE 0 END) As null_campaign_ID,
       SUM(CASE WHEN Campaign_Type IS NULL THEN 1 ELSE 0 END) AS null_campaign_type,
       SUM(CASE WHEN Target_Audience IS NULL THEN 1 ELSE 0 END) AS null_target_audience,
       SUM(CASE WHEN DURATION IS NULL THEN 1 ELSE 0 END) AS null_duration,
       SUM(CASE WHEN Channel_Used IS NULL THEN 1 ELSE 0 END) AS null_channel_used,
       SUM(CASE WHEN Leads IS NULL THEN 1 ELSE 0 END) AS null_leads,
       SUM(CASE WHEN Conversions IS NULL THEN 1 ELSE 0 END) AS null_conversions,
       SUM(CASE WHEN Acquisition_Cost IS NULL THEN 1 ELSE 0 END) AS null_acquisition_cost,
       SUM(CASE WHEN ROI IS NULL THEN 1 ELSE 0 END) AS null_ROI,
       SUM(CASE WHEN Language IS NULL THEN 1 ELSE 0 END) AS null_language,
       SUM(CASE WHEN Engagement_Score IS NULL THEN 1 ELSE 0 END) AS null_engagement_score,
       SUM(CASE WHEN Customer_Segment IS NULL THEN 1 ELSE 0 END) AS null_customer_segment,
       SUM(CASE WHEN Campaign_Date is NULL THEN 1 ELSE 0 END) AS null_campaign_date
FROM campaigns;

-- Duplication
SELECT Campaign_ID, COUNT(*) AS duplication
FROM campaigns
GROUP BY Campaign_ID
HAVING COUNT(*) > 1
ORDER BY duplication DESC;

-- Funnel logic evaluation
SELECT 
	SUM(CASE WHEN Clicks > Impressions THEN 1 ELSE 0 END) AS click_gt_impression,
    SUM(CASE WHEN Leads > Clicks THEN 1 ELSE 0 END) AS lead_gt_click,
    SUM(CASE WHEN Conversions > Leads THEN 1 ELSE 0 END) AS conversion_gt_lead
FROM campaigns;

-- Negative values detection
SELECT SUM(CASE WHEN Duration < 0 THEN 1 ELSE 0 END) AS neg_duration,
	   SUM(CASE WHEN Impressions < 0 THEN 1 ELSE 0 END) AS neg_impression,
       SUM(CASE WHEN Clicks < 0 THEN 1 ELSE 0 END) AS neg_click,
       SUM(CASE WHEN Leads < 0 THEN 1 ELSE 0 END) AS neg_lead,
       SUM(CASE WHEN Conversions < 0 THEN 1 ELSE 0 END) AS neg_conversion,
       SUM(CASE WHEN Revenue < 0 THEN 1 ELSE 0 END) AS neg_revenue,
       SUM(CASE WHEN Acquisition_Cost < 0 THEN 1 ELSE 0 END) AS neg_acquisition_cost,
       SUM(CASE WHEN Engagement_Score < 0 THEN 1 ELSE 0 END) AS neg_engagement_score
FROM campaigns;

-- Date format evaluation
SELECT Campaign_Date, Count(*)
FROM campaigns
WHERE Campaign_Date IS NOT NULL
AND STR_TO_DATE(Campaign_Date, '%d-%m-%Y') IS NULL
GROUP BY Campaign_Date;

SELECT 
    YEAR(STR_TO_DATE(Campaign_Date, '%d-%m-%Y')) AS campaign_year,
    COUNT(*) AS total_records
FROM campaigns
WHERE STR_TO_DATE(Campaign_Date, '%d-%m-%Y') IS NOT NULL
GROUP BY campaign_year
ORDER BY campaign_year ASC;

SELECT * FROM campaigns;