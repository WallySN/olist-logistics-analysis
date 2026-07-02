USE olist_db;

SELECT 
    c.customer_state AS estado,
    COUNT(*) AS total_ordenes,
    ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)), 1) AS dias_promedio_entrega,
    ROUND(AVG(DATEDIFF(o.order_estimated_delivery_date, o.order_delivered_customer_date)), 1) AS dias_promedio_retraso,
    ROUND(COUNT(CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 1 END) * 100.0 / COUNT(*), 1) AS pct_entregas_a_tiempo
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_delivered_customer_date IS NOT NULL
  AND o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY dias_promedio_entrega DESC;