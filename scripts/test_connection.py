import pandas as pd
from sqlalchemy import create_engine

print("🔌 Probando conexión a MySQL...")
try:
    mysql_engine = create_engine('mysql+mysqlconnector://root:MySQL_2026!@localhost:3306/olist_db')
    df = pd.read_sql("SELECT COUNT(*) as total FROM customers", mysql_engine)
    print(f"✅ MySQL OK - Clientes: {df['total'][0]}")
except Exception as e:
    print(f"❌ MySQL Error: {e}")

print("\n🔌 Probando conexión a PostgreSQL...")
try:
    postgres_engine = create_engine('postgresql://postgres:MySQL_2026!@localhost:5434/olist_db')
    df = pd.read_sql("SELECT COUNT(*) as total FROM customers", postgres_engine)
    print(f"✅ PostgreSQL OK - Clientes: {df['total'][0]}")
except Exception as e:
    print(f"❌ PostgreSQL Error: {e}")