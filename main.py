# 1. Imports
# 2. Faker setup
# 3. Generate Warehouses
# 4. Generate Products
# 5. Generate Inventory
# 6. Generate Orders
# 7. Generate Employees
# 8. Export all CSVs

from faker import Faker
import pandas as pd
import numpy as np

fake = Faker()
np.random.seed(42)
Faker.seed(42)

#WAREHOUSES
n_warehouses = 10

warehouses = pd.DataFrame({
    "WarehouseID": range(1, n_warehouses +1),
    "WarehouseName": [f"Warehouse_{i}" for i in range(1, n_warehouses +1)],
    "City": [fake.city() for _ in range(n_warehouses)],
    "State": [fake.state_abbr() for _ in range(n_warehouses)],
    "Capacity": np.random.randint(5000, 20000, n_warehouses),
    "Manager": [fake.name() for _ in range(n_warehouses)]
})

#PRODUCTS

n_products = 100

product_catalog = {
    "Electronics": [
        "Laptop", "Monitor", "Keyboard",
        "Mouse", "Webcam", "Headphones"
    ],
    "Office": [
        "Desk", "Office Chair", "Notebook",
        "Stapler", "Printer", "Whiteboard"
    ],
    "Home": [
        "Lamp", "Bookshelf", "Coffee Table",
        "Storage Bin", "Curtains"
    ],
    "Clothing": [
        "T-Shirt", "Hoodie", "Jeans",
        "Jacket", "Sweatpants"
    ]
}

products_data = []

for i in range(1, n_products + 1):
    category = np.random.choice(list(product_catalog.keys()))
    product_name = np.random.choice(product_catalog[category])
    products_data.append({
        "ProductID": i,
        "ProductName": product_name,
        "Category": category,
        "UnitCost": round(np.random.uniform(5, 200), 2),
        "UnitPrice": round(np.random.uniform(10, 400), 2)
    })

products = pd.DataFrame(products_data)


#INVENTORY
inventory_rows = []

for w in warehouses["WarehouseID"]:
    for p in products["ProductID"]:
        inventory_rows.append({
            "WarehouseID": w,
            "ProductID": p,
            "QuantityOnHand": np.random.randint(0, 500),
            "ReOrderLevel": np.random.randint(20, 100),
            "LastUpdated": fake.date_between(start_date = "-1y", end_date = "today")
        })
inventory = pd.DataFrame(inventory_rows)


#ORDERS

n_orders = 10000

orders = pd.DataFrame({
    "OrderID": range(1, n_orders+1),
    "ProductID": np.random.choice(products["ProductID"], n_orders),
    "OrderDate": pd.to_datetime(
        np.random.choice(pd.date_range("2024-01-01", "2025-06-01"), n_orders)
    ),
    "WarehouseID": np.random.choice(warehouses["WarehouseID"], n_orders),
    "CustomerRegion": np.random.choice(
        ["West", "South", "Midwest", "Northeast"], n_orders
    ),
    "Revenue": np.round(np.random.uniform(20, 2000, n_orders), 2),
})

orders["DeliveryDelay"] = np.random.normal(2, 3, n_orders).round().astype(int)
orders["DeliveryDelay"] = orders["DeliveryDelay"].clip(-2, 10)

orders["DeliveryDate"] = orders["OrderDate"] + pd.to_timedelta(3, unit="D")
orders["ActualDeliveryDate"] = orders["DeliveryDate"] + pd.to_timedelta(
    orders["DeliveryDelay"], unit="D"
)

orders.drop(columns=["DeliveryDelay"], inplace=True)


#EMPLOYEES

n_employees = 50
employees = pd.DataFrame({
    "EmployeeID": range(1, n_employees +1),
    "WarehouseID": np.random.choice(warehouses["WarehouseID"], n_employees),
    "EmployeeName": [fake.name() for _ in range(n_employees)],
    "Role": np.random.choice(["Picker", "Manager", "Supervisor", "Clerk"], n_employees)
})

#EXPORTING

warehouses.to_csv("warehouse.csv", index = False)
products.to_csv("products.csv", index = False)
inventory.to_csv("inventory.csv", index = False)
orders.to_csv("orders.csv", index = False)
employees.to_csv("employees.csv", index = False)