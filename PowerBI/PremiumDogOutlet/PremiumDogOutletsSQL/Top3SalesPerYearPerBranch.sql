WITH Yearly_Sales AS (
  SELECT t.BranchID as branch, 
  t.EmployeeID as emp, 
  SUM(ti.SaleTotal) as SalesAmount,
  EXTRACT(YEAR FROM t.Date) as SaleYear
  FROM transactions as t
  JOIN transactionitems as ti ON t.TransactionID = ti.TransactionID
  WHERE t.EmployeeID <> "NULL" AND t.BranchID <> 21
  GROUP BY SaleYear, branch, emp
), Ranked_Sales AS (
  SELECT *, DENSE_RANK() OVER(PARTITION BY SaleYear, branch ORDER BY SalesAmount DESC) as YearlyRank
  FROM Yearly_Sales
)
SELECT rs.SaleYear, rs.branch, rs.emp, e.EmployeeName, CONCAT('$ ', FORMAT("%'.2F", rs.SalesAmount)) as YearlySalesAmount, --if mysql use FORMAT(NUM, 2)
CASE WHEN YearlyRank = 1 THEN "First"
     WHEN YearlyRank = 2 THEN "Second"
     WHEN YearlyRank = 3 THEN "Third"
END AS EmployeeRankInBranch
FROM Ranked_Sales as rs
JOIN employee AS e ON CAST(e.EmployeeID AS STRING) = rs.emp
WHERE YearlyRank <= 3
ORDER BY rs.SaleYear, rs.branch, YearlySalesAmount;