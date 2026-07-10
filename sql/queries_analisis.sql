SELECT 
    CASE 
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 7 THEN '0-7 días'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 14 THEN '8-14 días'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) <= 21 THEN '15-21 días'
        ELSE 'Más de 21 días'
    END AS rango_entrega,
    COUNT(*) AS total_ordenes,
    ROUND(AVG(r.review_score), 2) AS calificacion_promedio,
    ROUND(COUNT(CASE WHEN r.review_score >= 4 THEN 1 END) * 100.0 / COUNT(*), 1) AS pct_satisfechos
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY rango_entrega
ORDER BY calificacion_promedio DESC;