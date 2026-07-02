import pandas as pd
from sqlalchemy import create_engine, text
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CONFIGURACIÓN: Cambia TU_PASSWORD por tu contraseña root de MySQL
# ============================================
PASSWORD = "MySQL_2026!"  # <-- ESCRIBE TU CONTRASEÑA AQUÍ

# Crear conexión a MySQL
engine = create_engine(f'mysql+mysqlconnector://root:{PASSWORD}@localhost/olist_db')

# Ruta donde están los CSV
DATA_PATH = "C:/data/olist/archive/"

print("=" * 60)
print("IMPORTANDO DATASET OLIST A MYSQL")
print("=" * 60)

# ============================================
# TABLA 1: CUSTOMERS
# ============================================
print("\n[1/9] Importando customers...")
df = pd.read_csv(f"{DATA_PATH}olist_customers_dataset.csv")
df.to_sql('customers', engine, if_exists='append', index=False)
print(f"    ✓ {len(df)} registros insertados")

# ============================================
# TABLA 2: GEOLOCATION (en chunks pequeños)
# ============================================
print("\n[2/9] Importando geolocation (en chunks de 10000)...")
chunk_size = 10000
total = 0

with engine.begin() as connection:
    for chunk in pd.read_csv(f"{DATA_PATH}olist_geolocation_dataset.csv", chunksize=chunk_size):
        chunk.to_sql('geolocation', connection, if_exists='append', index=False, method='multi')
        total += len(chunk)
        print(f"    ... {total} registros insertados")

print(f"    ✓ {total} registros insertados en total")

# ============================================
# TABLA 3: ORDERS
# ============================================
print("\n[3/9] Importando orders...")
df = pd.read_csv(f"{DATA_PATH}olist_orders_dataset.csv")

# Convertir columnas de fecha
date_columns = ['order_purchase_timestamp', 'order_approved_at', 
                'order_delivered_carrier_date', 'order_delivered_customer_date',
                'order_estimated_delivery_date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

df.to_sql('orders', engine, if_exists='append', index=False)
print(f"    ✓ {len(df)} registros insertados")

# ============================================
# TABLA 4: ORDER_ITEMS
# ============================================
print("\n[4/9] Importando order_items...")
df = pd.read_csv(f"{DATA_PATH}olist_order_items_dataset.csv")
df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
df.to_sql('order_items', engine, if_exists='append', index=False)
print(f"    ✓ {len(df)} registros insertados")

# ============================================
# TABLA 5: ORDER_PAYMENTS
# ============================================
print("\n[5/9] Importando order_payments...")
df = pd.read_csv(f"{DATA_PATH}olist_order_payments_dataset.csv")
df.to_sql('order_payments', engine, if_exists='append', index=False)
print(f"    ✓ {len(df)} registros insertados")

# ============================================
# TABLA 6: ORDER_REVIEWS
# ============================================
print("\n[6/9] Importando order_reviews...")
df = pd.read_csv(f"{DATA_PATH}olist_order_reviews_dataset.csv")
df['review_creation_date'] = pd.to_datetime(df['review_creation_date'], errors='coerce')
df['review_answer_timestamp'] = pd.to_datetime(df['review_answer_timestamp'], errors='coerce')
df.to_sql('order_reviews', engine, if_exists='append', index=False)
print(f"    ✓ {len(df)} registros insertados")

# ============================================
# TABLA 7: PRODUCTS
# ============================================
print("\n[7/9] Importando products...")
df = pd.read_csv(f"{DATA_PATH}olist_products_dataset.csv")
df.to_sql('products', engine, if_exists='append', index=False)
print(f"    ✓ {len(df)} registros insertados")

# ============================================
# TABLA 8: SELLERS
# ============================================
print("\n[8/9] Importando sellers...")
df = pd.read_csv(f"{DATA_PATH}olist_sellers_dataset.csv")
df.to_sql('sellers', engine, if_exists='append', index=False)
print(f"    ✓ {len(df)} registros insertados")

# ============================================
# TABLA 9: CATEGORY_TRANSLATION
# ============================================
print("\n[9/9] Importando category_translation...")
df = pd.read_csv(f"{DATA_PATH}product_category_name_translation.csv")
df.to_sql('category_translation', engine, if_exists='append', index=False)
print(f"    ✓ {len(df)} registros insertados")

print("\n" + "=" * 60)
print("¡IMPORTACIÓN COMPLETADA!")
print("=" * 60)