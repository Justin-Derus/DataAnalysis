-- Big Query for top 10 products per year per month per branch, ranked by sales amount
WITH SalesRecords AS (
	SELECT 
    p.ProductID,
    b.BranchID,
    b.City,
    EXTRACT(YEAR FROM t.Date) as year_,
    EXTRACT(MONTH FROM t.Date) as month_,
    SUM(ti.SaleTotal) as ProductSales,
    COUNT(p.ProductID) as TotalTransactions,
    SUM(ti.UnitTotal) as UnitsSold,
  FROM `retail_database.transactionitems` as ti
  JOIN `retail_database.transactions` as t on ti.TransactionID = t.TransactionID
  JOIN `retail_database.branch` as b on b.BranchID = t.BranchID
  JOIN `retail_database.product` as p on ti.ProductID = p.ProductID
  WHERE b.BranchID <> 21
  GROUP BY b.BranchID, b.City, year_, month_, p.ProductID
  ORDER BY b.BranchID, year_, month_, SUM(ti.SaleTotal) DESC, p.ProductID
), Top10ProductPerMonthPerBranch AS (
  SELECT 
  ProductID, 
  BranchID,
  City, 
  year_, 
  month_, 
  ProductSales,
  TotalTransactions,
  UnitsSold, 
  ROW_NUMBER() OVER(PARTITION BY BranchID, year_, month_ ORDER BY ProductSales DESC) as RankedProduct
  FROM SalesRecords as sr
)
SELECT 
  ProductID,
  BranchID,
  City,
  year_ as Year,
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
  CONCAT("$ ", FORMAT("%'.2F",ProductSales)) as ProductSalesAmount,
  TotalTransactions,
  UnitsSold,
  RankedProduct
FROM Top10ProductPerMonthPerBranch
WHERE RankedProduct <= 10 -- top 10 products chosen per month per branch CRUCIAL (should only have 14440 records, 6 years * 12 months * 20 branches * 10 products = 14,440)
ORDER BY BranchID, year_, month_, RankedProduct