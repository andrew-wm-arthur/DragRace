# this script takes the resulting table and outputs the .csv file we need to write Python code on
# if you want to run it on only the testing data, change the “FinalTable” FROM statement to the name of the table that is the subset 3-way j
# oin you did

#!/bin/bash
cd ~/ML_project/db
sqlite3 so-dump.db <<!
.headers off
.mode list
.separator '##C##'
.output data.csv
SELECT 	PostViewCount,
		Reputation,
		UserLifeDays,
		PostLifeDays,
		CodeSnippet,
		PostLength,
		URLCount,
		MAX(CASE WHEN PostHistoryTypeId = 1 THEN Text END) AS Title,
	    MAX(CASE WHEN PostHistoryTypeId = 2 THEN Text END) AS Body,
	    MAX(CASE WHEN PostHistoryTypeId = 3 THEN Text END) AS Tags,
		Delimiter 
	FROM sub_Final WHERE PostTypeId = 1 AND PostHistoryTypeId BETWEEN 1 AND 3 
	GROUP BY PostId;
!

SELECT 	PostViewCount, Reputation, UserLifeDays, PostLifeDays, CodeSnippet, PostLength, URLCount, MAX(CASE WHEN PostHistoryTypeId = 1 THEN Text END) AS Title,    MAX(CASE WHEN PostHistoryTypeId = 2 THEN Text END) AS Body,    MAX(CASE WHEN PostHistoryTypeId = 3 THEN Text END) AS Tags, Delimiter FROM sub_Final WHERE PostTypeId = 1 AND PostHistoryTypeId BETWEEN 1 AND 3 GROUP BY PostId;