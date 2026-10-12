
import pandas as pd
import mysql.connector
from getpass import getpass

# Read the CSV
df = pd.read_csv("data/raw/01_fund_master.csv")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass("Enter your MySQL root password: "),
    database="mutual_fund_analytics"
)

cursor = conn.cursor()

# Convert pandas missing values to SQL NULL
df = df.astype(object).where(pd.notna(df), None)

columns = list(df.columns)
column_sql = ", ".join(f"`{col}`" for col in columns)
placeholders = ", ".join(["%s"] * len(columns))

query = f"""
INSERT INTO fund_master ({column_sql})
VALUES ({placeholders})
"""

rows = [tuple(row) for row in df.itertuples(index=False, name=None)]

try:
    cursor.executemany(query, rows)
    conn.commit()
    print(f"Successfully imported {cursor.rowcount} records.")

    cursor.execute("SELECT COUNT(*) FROM fund_master")
    print("Total rows in fund_master:", cursor.fetchone()[0])

except Exception:
    conn.rollback()
    raise

finally:
    cursor.close()
    conn.close()
