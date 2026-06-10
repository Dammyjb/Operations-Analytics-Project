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
SELECT w.WarehouseName, ROUND(SUM(Revenue),2) AS WarehouseRevenue
FROM Orders o
JOIN Warehouses w
ON o.WarehouseID = w.WarehouseID
GROUP BY w.WarehouseName
ORDER BY WarehouseRevenue DESC;

    --Revenue by product category
SELECT p.Category, ROUND(SUM(Revenue),3) as TotalRev
FROM Orders o
JOIN Products p
ON p.ProductID = o.ProductID
GROUP BY p.Category
ORDER BY TotalRev DESC;


--Efficiency
    --Average delivery delay by region
SELECT CustomerRegion, AVG(DATEDIFF(day, DeliveryDate,ActualDeliveryDate)) AS AvgDelay
FROM Orders
WHERE ActualDeliveryDate > DeliveryDate
GROUP BY CustomerRegion;

    --On-time vs late delivery rate

SELECT p.Category,CAST(ROUND(SUM(
        CASE 
            WHEN ActualDeliveryDate <= DeliveryDate THEN 1
            ELSE 0
            END) * 100.0 / COUNT(CASE 
            WHEN ActualDeliveryDate <= DeliveryDate THEN 1
            ELSE 0
            END),2) AS decimal(5,2)) AS EarlyRatePercent, 
        CAST(ROUND((Count(p.Category) - SUM(
            CASE 
            WHEN ActualDeliveryDate <= DeliveryDate THEN 1
            ELSE 0
            END))* 100.0/ COUNT(CASE 
            WHEN ActualDeliveryDate <= DeliveryDate THEN 1
            ELSE 0
            END), 2) AS decimal (5,2)) AS LateRatePercent
FROM Orders o
JOIN Products p
ON o.ProductID = p.ProductID
GROUP BY p.Category;


