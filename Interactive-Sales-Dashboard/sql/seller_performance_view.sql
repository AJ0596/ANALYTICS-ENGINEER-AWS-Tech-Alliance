CREATE OR REPLACE VIEW seller_performance_view AS
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    p.product_id,
    p.product_cat_name,
    COUNT(DISTINCT o.order_cust_id) AS total_orders,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers,
    SUM(oi.order_price) AS total_revenue,
    AVG(oi.order_price) AS average_order_value,
    SUM(oi.order_freight_value) AS total_freight_value,
    COUNT(DISTINCT p.product_id) AS unique_products_sold,
    DATE_TRUNC('month', o.purchase_date_time) AS sale_month,
    
    -- Delivery KPIs
    SUM(CASE WHEN o.order_status = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN o.order_status != 'delivered' THEN 1 ELSE 0 END) AS non_delivered_orders,
    ROUND(AVG(CASE 
        WHEN o.order_status = 'delivered' 
        THEN DATE_PART('day', o.delivery_end - o.estimated_delivery) 
        ELSE NULL 
    END), 2) AS avg_delivery_delay,
    SUM(CASE 
        WHEN o.order_status = 'delivered' AND o.delivery_end <= o.estimated_delivery 
        THEN 1 ELSE 0 
    END) AS on_time_deliveries,
    SUM(CASE 
        WHEN o.order_status = 'delivered' AND o.delivery_end > o.estimated_delivery 
        THEN 1 ELSE 0 
    END) AS late_deliveries,

    -- Success & Cancel Metrics
    COUNT(*) FILTER (WHERE o.order_status = 'delivered') * 1.0 / NULLIF(COUNT(*), 0) AS successful_delivery_rate,
    COUNT(*) FILTER (WHERE o.order_status = 'canceled') * 1.0 / NULLIF(COUNT(*), 0) AS canceled_rate,

    -- Heavy/Bulky Products Delivery Performance
    COUNT(*) FILTER (WHERE p.product_weight > 10000 OR p.product_length > 50) AS large_heavy_product_orders,
    ROUND(AVG(CASE 
        WHEN (p.product_weight > 10000 OR p.product_length > 50) AND o.order_status = 'delivered' 
        THEN DATE_PART('day', o.delivery_end - o.estimated_delivery) 
        ELSE NULL 
    END), 2) AS avg_delivery_delay_large_heavy_product,

    -- Freight to Order Value % (for cost efficiency)
    ROUND(AVG(oi.order_freight_value / NULLIF(oi.order_price, 0)), 2) AS avg_freight_cost_percentage

FROM
    seller_analysis_fct saf
    JOIN seller s ON saf.seller_id = s.seller_id
    JOIN order_items oi ON saf.order_id = oi.order_id AND saf.seller_id = oi.seller_id
    JOIN orders o ON saf.order_cust_id = o.order_cust_id
    JOIN products p ON saf.product_id = p.product_id
    JOIN customers c ON saf.customer_id = c.customer_id
GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state,
    p.product_id,
    p.product_cat_name,
    DATE_TRUNC('month', o.purchase_date_time);
