import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:MySQL_2026!@localhost:5434/olist_db')

# Consulta simplificada sin subconsulta
query_simple = """
SELECT 
    EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400 as delivery_days,
    AVG(r.review_score) as avg_rating,
    COUNT(*) as total_orders
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY delivery_days
ORDER BY delivery_days
LIMIT 10;
"""

df = pd.read_sql(query_simple, engine)
print(f"Filas devueltas: {len(df)}")
print(df.head())
print(f"\nTipos de datos:\n{df.dtypes}")