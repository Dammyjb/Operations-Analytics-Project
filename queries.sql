USE OperationsAnalytics;

---Inventory insights
    ---Which warehouses are running low on stock? 
SELECT w.WarehouseName, p.ProductName,
    (ReOrderLevel - QuantityOnHand) As UnitsShort
FROM Inventory i
JOIN Warehouses w
ON i.WarehouseID = w.WarehouseID
JOIN Products p
ON i.ProductID = P.ProductID
WHERE ReOrderLevel >= QuantityOnHand
ORDER BY UnitsShort DESC;

--What is the aggregate?
SELECT w.WarehouseName,
     SUM((ReOrderLevel - QuantityOnHand)) As CountUnitsShort
FROM Inventory i
JOIN Warehouses w
ON i.WarehouseID = w.WarehouseID
JOIN Products p
ON i.ProductID = P.ProductID
WHERE ReOrderLevel >= QuantityOnHand
GROUP BY w.WarehouseName
ORDER BY CountUnitsShort DESC;

---Which products are most overstocked?
SELECT w.WarehouseName, p.ProductName,
     (QuantityOnHand - ReOrderLevel) As ExcessUnits
FROM Inventory i
JOIN Warehouses w
ON i.WarehouseID = w.WarehouseID
JOIN Products p
ON i.ProductID = P.ProductID
WHERE ReOrderLevel <= QuantityOnHand
ORDER BY ExcessUnits DESC;

--Revenue insights
    --Revenue by warehouse
    --Revenue by product category



--Efficiency
    --Average delivery delay by region
    --On-time vs late delivery rate




--Operations
    --Top 10 fastest moving products
    --Employees per warehouse and workload distribution



--Employee Insights
    --Employees per warehouse
    --Manager-to-worker ratios
    --Warehouses with the largest workforce