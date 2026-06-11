import sqlalchemy as db
import matplotlib.pyplot as plt
import pandas as pd

#plot revenue by warehouse
#plot total Units Short by Warehouse
#plot revenue by product category
#plot on-time Delivery Ratest By Region


# Creating the connection engine to SQL database
engine = db.create_engine('mssql+pyodbc://sa:NewSecurePass123!@localhost:1433/OperationsAnalytics?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes')
#in create_engine = (dialect +driver://user:pass@host:port/db)

with open("queries.sql", "r") as file:
    sql_content = file.read()

queries = {
    "inventory_short": """
        SELECT w.WarehouseName, p.ProductName,
               (ReOrderLevel - QuantityOnHand) AS UnitsShort
        FROM Inventory i
        JOIN Warehouses w ON i.WarehouseID = w.WarehouseID
        JOIN Products p ON i.ProductID = p.ProductID
        WHERE ReOrderLevel >= QuantityOnHand
    """,

    "revenue_warehouse": """
        SELECT w.WarehouseName,
               ROUND(SUM(Revenue),2) AS WarehouseRevenue
        FROM Orders o
        JOIN Warehouses w ON o.WarehouseID = w.WarehouseID
        GROUP BY w.WarehouseName
    """,

    "revenue_category": """
        SELECT p.Category,
               ROUND(SUM(Revenue),3) AS TotalRev
        FROM Orders o
        JOIN Products p ON o.ProductID = p.ProductID
        GROUP BY p.Category
    """,
    "delivery_delay": """
        SELECT CustomerRegion, AVG(DATEDIFF(day, DeliveryDate,ActualDeliveryDate)) AS AvgDelay
        FROM Orders
        WHERE ActualDeliveryDate > DeliveryDate
        GROUP BY CustomerRegion;
    """,

    "delivery_rates":"""
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
    """
}
#Creating figure
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
# CHART 1: Revenue by Warehouse (Horizontal Bar)
#----------------------------------------------
df1 = pd.read_sql(queries["revenue_warehouse"], con=engine)
# Use barh for horizontal bar chart
axs[0,0].barh(df1["WarehouseName"], df1["WarehouseRevenue"], color="darkred")
axs[0,0].set_title("Revenue by Warehouse")
axs[0,0].set_xlabel("Revenue ($)")
axs[0,0].invert_yaxis()


# CHART 2: Units Short by Warehouse (Horizontal Bar)

df2 = pd.read_sql(queries["inventory_short"], con=engine)

axs[0,1].barh(df2["WarehouseName"], df2["UnitsShort"], color="teal")
axs[0,1].set_title("Total Units Short by Warehouse")
axs[0,1].set_xlabel("Units Short")
axs[0,1].invert_yaxis()

# CHART 3: Revenue by Product Category (Horizontal Bar)
df3 = pd.read_sql(queries["revenue_category"], con=engine)

axs[1,0].barh(df3["Category"], df3["TotalRev"], color = "orange")
axs[1,0].set_title("Total Revenue by Category")
axs[1,0].set_xlabel("Total Revenue")
axs[1,0].invert_yaxis()

#CHART 4: On-time Delivery Ratest By Region
df4 = pd.read_sql(queries["delivery_rates"], con=engine)
x = range(len(df4))
width = 0.4

axs[1,1].barh([i - width/2 for i in x],
              df4["EarlyRatePercent"],
              height=width,
              label="Early",
              color="green")

axs[1,1].barh([i + width/2 for i in x],
              df4["LateRatePercent"],
              height=width,
              label="Late",
              color="red")

axs[1,1].set_yticks(list(x))
axs[1,1].set_yticklabels(df4["Category"])

axs[1,1].set_title("Delivery Performance by Category")
axs[1,1].legend()

plt.tight_layout()
plt.show()