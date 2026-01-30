With BAT AS (
  SELECT SUM(ti.SaleTotal) as BranchSalesAllTime, b.City AS Location
  FROM `retail_database.transactionitems` as ti
  JOIN `retail_database.transactions` as t on ti.TransactionID = t.TransactionID
  JOIN `retail_database.branch` as b on t.BranchID = b.BranchID
  GROUP BY b.City
  ORDER BY BranchSalesAllTime DESC, b.City
), BAT_W_AVG AS (
  SELECT BranchSalesAllTime,
  AVG(BranchSalesAllTime) OVER() as average,
  Location
  FROM BAT
)
SELECT CONCAT("$",FORMAT("%'.2f", BranchSalesAllTime)) as BranchSales, CONCAT("$", FORMAT("%'.2f", average)) AS CompanyAverage, Location,
CASE WHEN BranchSalesAllTime > average THEN "Yes"
     WHEN BranchSalesAllTime < average THEN "No"
     ELSE "Equal"
     END AS AverageMet
FROM BAT_W_AVG;