-- UNCOMMENT THE TWO LINES BELOW IF RUNNING FOR THE FIRST TIME:
---CREATE DATABASE OperationsAnalytics
---GO


USE OperationsAnalytics;

DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Warehouses;
DROP TABLE IF EXISTS Employees;

CREATE TABLE Warehouses(
    WarehouseID INT PRIMARY KEY,
    WarehouseName VARCHAR(100),
    City VARCHAR(100),
    State VARCHAR(10),
    Capacity INT,
    Manager VARCHAR(100)
);


CREATE TABLE Products(
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(100),
    UnitCost DECIMAL(10,2),
    UnitPrice DECIMAL(10,2)
);

CREATE TABLE Inventory(
    WarehouseID INT,
    ProductID INT,
    QuantityOnHand INT,
    ReOrderLevel INT,

    PRIMARY KEY(WarehouseID, ProductID),
    FOREIGN KEY(WarehouseID) REFERENCES Warehouses(WarehouseID),
    FOREIGN KEY(ProductID) REFERENCES Products(ProductID)
);


CREATE TABLE Orders(
     OrderID INT PRIMARY KEY,
    ProductID INT,
    WarehouseID INT,
    OrderDate DATE,
    DeliveryDate DATE,
    ActualDeliveryDate DATE,
    CustomerRegion VARCHAR(50),
    Revenue DECIMAL(10,2),

    FOREIGN KEY (ProductID)
        REFERENCES Products(ProductID),

    FOREIGN KEY (WarehouseID)
        REFERENCES Warehouses(WarehouseID)
);

DROP TABLE IF EXISTS Employees;
CREATE TABLE Employees(
    EmployeeID INT PRIMARY KEY,
    WarehouseID INT,
    EmployeeName VARCHAR(100),
    Role VARCHAR(50),

    FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID)
);