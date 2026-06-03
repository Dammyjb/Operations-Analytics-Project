import os
import pandas as pd
from sqlalchemy import create_engine, text

conn_str = (
    "mssql+pyodbc://sa:NewSecurePass123!@localhost:1433/OperationsAnalytics"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(conn_str)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())

script_dir = os.path.dirname(os.path.abspath(__file__))

tables_to_load = [
    ('Warehouses', 'warehouse.csv'),
    ('Products', 'products.csv'),
    ('Employees', 'employees.csv'),
    ('Inventory', 'inventory.csv'),
    ('Orders', 'orders.csv')
]

for table_name, csv_filename in tables_to_load:
    csv_path = os.path.join(script_dir, csv_filename)

    if not os.path.exists(csv_path):
        print(f"Missing file: {csv_filename}")
        continue

    print(f"Loading {csv_filename} → {table_name}")

    try:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Loaded {len(df)} rows into {table_name}")

    except Exception as e:
        print(f"Error in {table_name}: {e}")
        break

print("Done!")