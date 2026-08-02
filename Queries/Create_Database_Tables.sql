CREATE DATABASE IF NOT EXISTS marketing_analytics;
USE marketing_analytics;

CREATE TABLE IF NOT EXISTS campaigns (
		Campaign_ID         VARCHAR(20),
		Brand               VARCHAR(20),
		Campaign_Type       VARCHAR(50),
		Target_Audience     VARCHAR(100),
		Duration            INT,
		Channel_Used        VARCHAR(200),
		Impressions         INT,
		Clicks              INT,
		Leads               INT,
		Conversions         INT,
		Revenue             INT,
		Acquisition_Cost    DECIMAL(10, 2),
		ROI                 DECIMAL(10, 4),
		Language            VARCHAR(50),
		Engagement_Score    DECIMAL(5, 2),
		Customer_Segment    VARCHAR(100),
		Campaign_Date 		VARCHAR(20)
);