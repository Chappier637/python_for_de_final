DROP TABLE IF EXISTS sales_analysis;

CREATE TABLE sales_analysis AS
SELECT
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) AS full_name,
    u.email,
    u.phone,
    u.loyalty_status,
    o.order_id,
    o.order_date,
    o.total_amount AS order_total,
    p.product_id,
    p.name AS product_name,
    pc.name AS category_name,
    od.quantity,
    od.price_per_unit,
    od.quantity * od.price_per_unit AS total_price_per_product,
    o.status AS order_status
FROM
    orders o
JOIN
    users u ON o.user_id = u.user_id
JOIN
    orderDetails od ON o.order_id = od.order_id
JOIN
    products p ON od.product_id = p.product_id
JOIN
    productCategories pc ON p.category_id = pc.category_id;