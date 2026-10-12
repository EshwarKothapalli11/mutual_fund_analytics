
import pandas as pd
import mysql.connector
from getpass import getpass

# Load the transaction CSV
df = pd.read_csv("data/raw/08_investor_transactions.csv")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass("Enter MySQL root password: "),
    database="mutual_fund_analytics"
)

cursor = conn.cursor()

columns = [
    "investor_id", "transaction_date", "amfi_code",
    "transaction_type", "amount_inr", "state", "city",
    "city_tier", "age_group", "gender", "annual_income_lakh",
    "payment_mode", "kyc_status"
]

# Convert missing values to SQL NULL
df = df[columns].astype(object).where(pd.notna(df[columns]), None)

query = """
INSERT INTO investor_transactions (
    investor_id, transaction_date, amfi_code,
    transaction_type, amount_inr, state, city,
    city_tier, age_group, gender, annual_income_lakh,
    payment_mode, kyc_status
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

rows = list(df.itertuples(index=False, name=None))

try:
    cursor.executemany(query, rows)
    conn.commit()

    print("CSV records:", len(df))
    print("Rows inserted:", cursor.rowcount)

    cursor.execute("SELECT COUNT(*) FROM investor_transactions")
    print("Total rows in table:", cursor.fetchone()[0])

except Exception:
    conn.rollback()
    raise

finally:
    cursor.close()
    conn.close()
