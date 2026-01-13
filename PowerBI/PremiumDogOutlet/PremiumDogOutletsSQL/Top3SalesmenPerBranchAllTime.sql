-- Find The Top 3 Salesmen From Each Branch Uses Window Fxn, Join, Case When
WITH RankedSales AS ( -- Use a CTE to get all of the information pertaining to the sales and employee number
    SELECT 
    	SUM(ti.SaleTotal) as SalesAmount, t.EmployeeID AS EmpID, t.BranchID as Branch,
    	ROW_NUMBER() OVER(PARTITION BY t.BranchID ORDER BY SUM(ti.SaleTotal) DESC) AS SaleRank -- window fxn for getting top 3 per branch
    FROM TRANSACTIONS AS t
    JOIN transactionitems as ti on ti.TransactionID = t.TransactionID WHERE t.BranchID <> 0 AND t.EmployeeID IS NOT NULL -- branch 0 means all combined, null emp is anon transaction
    GROUP BY t.BranchID, t.EmployeeID
)
SELECT CONCAT('$', FORMAT(rs.SalesAmount,2)) as TotalSales, rs.Branch, rs.EmpID, e.EmployeeName,
CASE
    WHEN rs.SaleRank = 1 THEN "First"
    WHEN rs.SaleRank = 2 THEN "Second"
    WHEN rs.SaleRank = 3 THEn "Third"
END AS SalesRanking
FROM RankedSales as rs
JOIN employee as e on e.EmployeeID = rs.EmpID
WHERE SaleRank <= 3
ORDER BY Branch, SaleRank ASC;