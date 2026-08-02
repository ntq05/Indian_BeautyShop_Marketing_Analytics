-- This will just create a view in mysql, it does not create a physical table
{{config(materialized='view')}}

WITH source_data AS (
    SELECT * FROM {{source('marketing_analytics', 'campaigns')}}
),

parsed_and_cleanded AS (
    -- Trim whitespace
    SELECT 
        TRIM(Campaign_ID) AS Campaign_ID,
        CASE
            WHEN Brand IS NOT NULL AND TRIM(Brand) != '' THEN TRIM(Brand)
            WHEN TRIM(Campaign_ID) LIKE 'NY-%' THEN 'Nykaa'
            WHEN TRIM(Campaign_ID) LIKE 'PU-%' THEN 'Purplle'
            WHEN TRIM(Campaign_ID) LIKE 'TI-%' THEN 'Tira Beauty'
            ELSE 'Unknown'

        END AS Brand,

        TRIM(Campaign_Type) AS Campaign_Type,
        TRIM(Language) AS Language,
        TRIM(Customer_Segment) AS Customer_Segment,
        TRIM(Target_Audience) AS Target_Audience,

        CAST(Duration AS SIGNED) AS Duration,
        Impressions,
        Clicks,
        Leads,
        Conversions,
        Revenue,
        Acquisition_Cost,
        Engagement_Score,
        Channel_Used,
        
        -- Only dates in the format of DD-MM-YYYY are considered valid. Any other formats will be treated as NULL.
        CASE
            WHEN Campaign_Date REGEXP '^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-[0-9]{4}$'
                AND CAST(SUBSTRING(Campaign_Date,1,2) AS UNSIGNED) <=
                    DAY(
                        LAST_DAY(
                            CONCAT(
                                SUBSTRING(Campaign_Date,7,4), '-',
                                SUBSTRING(Campaign_Date,4,2), '-01'
                            )
                        )
                    )
            THEN STR_TO_DATE(Campaign_Date, '%d-%m-%Y')
            ELSE NULL
        END AS parsed_date
    FROM source_data
),

-- Remove Deduplicated records
deduplicated AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Campaign_ID
            ORDER BY
                Duration ASC,
                Revenue ASC,
                parsed_date DESC
        ) AS row_num
    FROM parsed_and_cleanded
)

SELECT
    Campaign_ID,
    Brand,
    Campaign_Type,
    Language,
    Customer_Segment,
    Target_Audience,
    Channel_Used,
    Duration,
    Impressions,
    Clicks,
    Leads,
    Conversions,
    Revenue,
    Acquisition_Cost,
    Engagement_Score,
    parsed_date AS Campaign_Date
FROM deduplicated
WHERE row_num = 1

-- Remove null
AND Impressions IS NOT NULL
AND Clicks IS NOT NULL
AND Leads IS NOT NULL
AND Conversions IS NOT NULL
AND Revenue IS NOT NULL

-- Remove unfollowed-logic records
AND Impressions >= Clicks
AND Clicks >= Leads
AND Leads >= Conversions

-- Remove negative values
AND Impressions >= 0
AND Clicks >= 0
AND Leads >= 0
AND Conversions >= 0
AND Revenue >= 0
AND Acquisition_Cost >= 0

-- Remove unparsable dates and out of range dates
AND parsed_date IS NOT NULL
AND parsed_date BETWEEN '2024-01-01' AND '2025-12-31'