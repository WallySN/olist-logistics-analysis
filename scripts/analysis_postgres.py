import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from db_config import get_engine

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 10

print("Conectando a PostgreSQL (Docker)...")
engine = get_engine()
print("Conectado!")

pass  # directorio ya existe

# ============================================
# ANALISIS 1: TIEMPOS DE ENTREGA POR ESTADO
# ============================================
print("\nAnalisis 1: Tiempos de entrega por estado...")
query1 = """
SELECT 
    c.customer_state,
    ROUND(AVG(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400)::numeric, 1) as avg_days,
    COUNT(*) as total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_days DESC;
"""
df1 = pd.read_sql(query1, engine)

fig, ax = plt.subplots(figsize=(12, 7))
sns.barplot(data=df1, x='avg_days', y='customer_state', palette='viridis', ax=ax)
ax.set_title('Tiempo Promedio de Entrega por Estado', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Dias promedio de entrega', fontsize=12)
ax.set_ylabel('Estado de Brasil', fontsize=12)

for i, v in enumerate(df1['avg_days']):
    ax.text(v + 0.3, i, f'{v} dias', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('/app/images/01_entrega_por_estado.png', dpi=300, bbox_inches='tight')
plt.close()
print("Grafico 1 guardado: 01_entrega_por_estado.png")

# ============================================
# ANALISIS 2: VELOCIDAD vs SATISFACCION
# ============================================
print("\nAnalisis 2: Velocidad vs Satisfaccion...")
query2 = """
SELECT 
    ROUND(delivery_days::numeric) as delivery_days,
    AVG(avg_rating) as avg_rating,
    SUM(total_orders) as total_orders
FROM (
    SELECT 
        EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400 as delivery_days,
        AVG(r.review_score) as avg_rating,
        COUNT(*) as total_orders
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL
    GROUP BY o.order_id, o.order_delivered_customer_date, o.order_purchase_timestamp
) subquery
GROUP BY ROUND(delivery_days::numeric)
HAVING SUM(total_orders) > 50
ORDER BY delivery_days;
"""
df2 = pd.read_sql(query2, engine)

print(f"Filas obtenidas: {len(df2)}")

if len(df2) == 0:
    query2_backup = """
    SELECT 
        ROUND(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400::numeric) as delivery_days,
        AVG(r.review_score) as avg_rating,
        COUNT(*) as total_orders
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL
    GROUP BY ROUND(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400::numeric)
    ORDER BY delivery_days;
    """
    df2 = pd.read_sql(query2_backup, engine)
    print(f"Filas con backup: {len(df2)}")

df2['total_orders'] = df2['total_orders'].astype(float)
df2['avg_rating'] = df2['avg_rating'].astype(float)
df2['delivery_days'] = df2['delivery_days'].astype(float)

df2 = df2[(df2['delivery_days'] >= 0) & (df2['delivery_days'] <= 60)]
df2 = df2.dropna()

print(f"Filas finales: {len(df2)}")

if len(df2) > 0:
    fig, ax = plt.subplots(figsize=(12, 7))
    scatter = ax.scatter(df2['delivery_days'], df2['avg_rating'], 
                        s=df2['total_orders']/5, 
                        c=df2['avg_rating'], 
                        cmap='RdYlGn', 
                        alpha=0.6, 
                        edgecolors='black')

    if len(df2) > 1:
        z = np.polyfit(df2['delivery_days'], df2['avg_rating'], 1)
        p = np.poly1d(z)
        ax.plot(df2['delivery_days'], p(df2['delivery_days']), "r--", alpha=0.8, linewidth=2)

    plt.colorbar(scatter, ax=ax, label='Calificacion promedio')
    ax.set_title('Velocidad de Entrega vs Satisfaccion del Cliente', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Dias de entrega', fontsize=12)
    ax.set_ylabel('Calificacion promedio (1-5 estrellas)', fontsize=12)
    ax.set_ylim(0, 5.5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/app/images/02_velocidad_vs_satisfaccion.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Grafico 2 guardado: 02_velocidad_vs_satisfaccion.png")
else:
    print("No hay datos suficientes para generar el grafico 2")

# ============================================
# ANALISIS 3: TOP 10 CATEGORIAS
# ============================================
print("\nAnalisis 3: Top 10 categorias mas rentables...")
query3 = """
SELECT 
    ct.product_category_name_english as category,
    SUM(oi.price) as total_revenue,
    COUNT(DISTINCT oi.order_id) as total_orders,
    ROUND(AVG(oi.price)::numeric, 2) as avg_price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN category_translation ct ON p.product_category_name = ct.product_category_name
GROUP BY ct.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;
"""
df3 = pd.read_sql(query3, engine)

df3['total_revenue'] = df3['total_revenue'].astype(float)
df3['total_orders'] = df3['total_orders'].astype(float)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

sns.barplot(data=df3, x='total_revenue', y='category', palette='Blues_r', ax=ax1)
ax1.set_title('Ingresos por Categoria', fontweight='bold', fontsize=13)
ax1.set_xlabel('Ingresos totales ($)')

sns.barplot(data=df3, x='total_orders', y='category', palette='Greens_r', ax=ax2)
ax2.set_title('Ordenes por Categoria', fontweight='bold', fontsize=13)
ax2.set_xlabel('Total de ordenes')

fig.suptitle('Top 10 Categorias - Olist E-Commerce', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/app/images/03_top_categorias.png', dpi=300, bbox_inches='tight')
plt.close()
print("Grafico 3 guardado: 03_top_categorias.png")

# ============================================
# ANALISIS 4: METODOS DE PAGO
# ============================================
print("\nAnalisis 4: Metodos de pago...")
query4 = """
SELECT 
    payment_type,
    COUNT(*) as total_payments,
    SUM(payment_value) as total_value,
    ROUND(AVG(payment_value)::numeric, 2) as avg_value
FROM order_payments
GROUP BY payment_type
ORDER BY total_payments DESC;
"""
df4 = pd.read_sql(query4, engine)

df4['total_payments'] = df4['total_payments'].astype(float)
df4['total_value'] = df4['total_value'].astype(float)
df4['avg_value'] = df4['avg_value'].astype(float)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
wedges, texts, autotexts = ax1.pie(df4['total_payments'], 
                                    labels=df4['payment_type'],
                                    autopct='%1.1f%%',
                                    colors=colors,
                                    startangle=90,
                                    explode=[0.05 if i == 0 else 0 for i in range(len(df4))])
ax1.set_title('Distribucion de Metodos de Pago', fontweight='bold', fontsize=13)

sns.barplot(data=df4, x='payment_type', y='total_value', palette='Set2', ax=ax2)
ax2.set_title('Valor Total por Metodo', fontweight='bold', fontsize=13)
ax2.set_xlabel('Metodo de pago')
ax2.set_ylabel('Valor total ($)')
ax2.tick_params(axis='x', rotation=45)

for i, v in enumerate(df4['total_value']):
    ax2.text(i, v + 10000, f'${v:,.0f}', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('/app/images/04_metodos_pago.png', dpi=300, bbox_inches='tight')
plt.close()
print("Grafico 4 guardado: 04_metodos_pago.png")

# ============================================
# RESUMEN FINAL
# ============================================
print("\n" + "="*50)
print("TODOS LOS ANALISIS COMPLETADOS!")
print("="*50)
print("Graficos guardados en: /app/images/")
print("\nArchivos generados:")
print("  1. 01_entrega_por_estado.png")
print("  2. 02_velocidad_vs_satisfaccion.png")
print("  3. 03_top_categorias.png")
print("  4. 04_metodos_pago.png")
print("\nProyecto listo para GitHub y portfolio!")