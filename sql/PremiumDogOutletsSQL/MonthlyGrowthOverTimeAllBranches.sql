-- MySQL Version
WITH SalesReport AS (                                               -- Find the raw data and do all joins in first CTE
    SELECT SUM(ti.SaleTotal) as SalesAmount, 
    	   t.BranchID as branch,
    	   b.City as Location, 
    	   EXTRACT(YEAR FROM t.Date) as year_, 
    	   EXTRACT(MONTH FROM t.Date) AS month_
    FROM transactionitems as ti 
    JOIN transactions as t on t.TransactionID = ti.TransactionID
    JOIN branch as b on b.BranchID = t.BranchID
    WHERE t.BranchID <> 21
    GROUP BY t.BranchID, year_, month_
    ORDER BY t.BranchID, year_, month_
), Previous_Month_Col AS (                                          -- Using LAG window function, keep track of all previous months
    SELECT SalesAmount, 
    	   Location, 
    	   year_, 
   		   month_, 
    	   LAG(SalesAmount, 1) OVER(PARTITION BY branch ORDER BY branch, year_, month_) AS PreviousSalesAmount
    FROM SalesReport
), MoM_Growth AS (                                                  -- Calculate MoM % and Actual Amount 
    SELECT SalesAmount, 
    	   Location, 
    	   year_, 
           month_, 
    	   PreviousSalesAmount, 
    	   ((SalesAmount - PreviousSalesAmount) / PreviousSalesAmount) * 100 AS MoM_Perc,
    	   (SalesAmount - PreviousSalesAmount) AS MoM_Diff
    FROM Previous_Month_Col
)
SELECT                                                              -- Format the data to look nice
    CONCAT("$ ",FORMAT(SalesAmount,2)) as SalesAmount, 
    Location AS Branch, 
    year_ AS Sales_Year, 
    CASE 
    	WHEN month_ = 1 THEN "January"
        WHEN month_ = 2 THEN "Febuary"
        WHEN month_ = 3 THEN "March"
        WHEN month_ = 4 THEN "April"
        WHEN month_ = 5 THEN "May"
        WHEN month_ = 6 THEN "June"
        WHEN month_ = 7 THEN "July"
        WHEN month_ = 8 THEN "August"
        WHEN month_ = 9 THEN "September"
        WHEN month_ = 10 THEN "October"
        WHEN month_ = 11 THEN "November"
        WHEN month_ = 12 THEN "December"
        END AS Month,
    CONCAT("$ ",FORMAT(PreviousSalesAmount,2)) AS PreviousSalesAmount, 
    CONCAT(FORMAT(MoM_Perc,2),"%") AS MoM_Perc, 
    CONCAT("$ ",FORMAT(MoM_Diff,2)) AS MoM_Diff
FROM MoM_Growth;

-- -------------------------------------------------------------------------------------------------------------------------------------------------------------

-- BigQuery Version 
WITH SalesReport AS (
    SELECT SUM(ti.SaleTotal) as SalesAmount, 
    	   t.BranchID as branch,
    	   b.City as Location, 
    	   EXTRACT(YEAR FROM t.Date) as year_, 
    	   EXTRACT(MONTH FROM t.Date) AS month_
    FROM `retail_database.transactionitems` as ti 
    JOIN `retail_database.transactions` as t on t.TransactionID = ti.TransactionID
    JOIN `retail_database.branch` as b on b.BranchID = t.BranchID
    WHERE t.BranchID <> 21
    GROUP BY t.BranchID, b.City, year_, month_ -- Must add city in bigquery, all non aggregated cols must be grouped by in big query
    ORDER BY t.BranchID, year_, month_
), Previous_Month_Col AS (
    SELECT SalesAmount, 
    	   Location, 
    	   year_, 
   		   month_, 
    	   LAG(SalesAmount, 1) OVER(PARTITION BY branch ORDER BY branch, year_, month_) AS PreviousSalesAmount
    FROM SalesReport
), MoM_Growth AS (
    SELECT SalesAmount, 
    	   Location, 
    	   year_, 
           month_, 
    	   PreviousSalesAmount, 
    	   ((SalesAmount - PreviousSalesAmount) / PreviousSalesAmount) * 100 AS MoM_Perc,
    	   (SalesAmount - PreviousSalesAmount) AS MoM_Diff
    FROM Previous_Month_Col
)
SELECT 
    CONCAT("$ ",FORMAT("%'.2F",SalesAmount)) as SalesAmount, -- Format has diff syntax in BigQuery
    year_ AS Sales_Year, 
    CASE 
    	WHEN month_ = 1 THEN "January"
        WHEN month_ = 2 THEN "Febuary"
        WHEN month_ = 3 THEN "March"
        WHEN month_ = 4 THEN "April"
        WHEN month_ = 5 THEN "May"
        WHEN month_ = 6 THEN "June"
        WHEN month_ = 7 THEN "July"
        WHEN month_ = 8 THEN "August"
        WHEN month_ = 9 THEN "September"
        WHEN month_ = 10 THEN "October"
        WHEN month_ = 11 THEN "November"
        WHEN month_ = 12 THEN "December"
        END AS Month,
    CONCAT("$ ",FORMAT("%'.2F",PreviousSalesAmount)) AS PreviousSalesAmount, 
    CONCAT(ROUND(MoM_Perc,2),"%") AS MoM_Perc, 
    CONCAT("$ ",FORMAT("%'.2F",MoM_Diff)) AS MoM_Diff
FROM MoM_Growth;