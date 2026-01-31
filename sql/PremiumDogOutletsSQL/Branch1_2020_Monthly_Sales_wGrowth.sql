-- MySQL Version
-- Branch 1 Sales for 2020, Including Month Over Month % and Dollar Amount
WITH Sales2020 AS ( -- Find the total sales for each month
    SELECT SUM(ti.SaleTotal) as Sales, EXTRACT(MONTH FROM t.Date) AS month_, b.BranchID
    FROM transactionitems AS ti
    JOIN transactions AS t on ti.TransactionID = t.TransactionID
    JOIN branch as b on b.BranchID = t.BranchID
    WHERE b.BranchID = 1 AND t.Date BETWEEN '2020-01-01 00:00:00' and '2020-12-31 00:00:00'
    GROUP BY EXTRACT(MONTH from t.Date)
), RevComparisons AS ( -- With the totals now calculated, create a window fxn to find the previous month
    SELECT Sales,
    ELT(month_, -- Extract Load Transform, turn month_ i.e. a digit into the corresponding month
        'January','Febuary','March','April',
        'May','June','July','August',
        'September','October','November','December') AS Month,
    LAG(Sales,1) OVER(ORDER BY month_) AS PreviousMonth -- Lag to create a column of previous months sales for calculations later
    FROM Sales2020
)
SELECT CONCAT("$",FORMAT(Sales,2)) AS Sales, 
       Month, 
       CONCAT("$",FORMAT(PreviousMonth,2)) PreviousMonthSales, 
       CONCAT(FORMAT(((Sales - PreviousMonth) / PreviousMonth) * 100,2),"%") AS MoM_Growth_Perc, -- Percentage change of month over month
       CONCAT("$",FORMAT(Sales - PreviousMonth,2)) AS MoM_Dollar_Amount -- Dollar amount of month over month change
FROM RevComparisons;



-- BigQuery Version
WITH Sales2020 AS ( -- Find the total sales for each month
    SELECT SUM(ti.SaleTotal) as Sales, EXTRACT(MONTH FROM t.Date) AS month_
    FROM `retail_database.transactionitems` AS ti
    JOIN `retail_database.transactions` AS t on ti.TransactionID = t.TransactionID
    JOIN `retail_database.branch` as b on b.BranchID = t.BranchID
    WHERE b.BranchID = 1 AND t.Date BETWEEN '2020-01-01 00:00:00' and '2020-12-31 00:00:00'
    GROUP BY EXTRACT(MONTH from t.Date)
), RevComparisons AS ( -- With the totals now calculated, create a window fxn to find the previous month
    SELECT Sales,
    CASE WHEN month_ = 1 THEN "January"
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
    LAG(Sales,1) OVER(ORDER BY month_) AS PreviousMonth -- Lag to create a column of previous months sales for calculations later
    FROM Sales2020
)
SELECT CONCAT("$",FORMAT("%'.2F",Sales)) AS Sales, 
       Month, 
       CONCAT("$",FORMAT("%'.2F",PreviousMonth)) PreviousMonthSales, 
       CONCAT(FORMAT("%'.2F",((Sales - PreviousMonth) / PreviousMonth) * 100),"%") AS MoM_Growth_Perc, -- Percentage change of month over month
       CONCAT("$",FORMAT("%'.2F",Sales - PreviousMonth)) AS MoM_Dollar_Amount -- Dollar amount of month over month change
FROM RevComparisons;