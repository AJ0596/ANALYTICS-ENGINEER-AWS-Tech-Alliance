-- ------------------------------
-- Create Dimension Tables
-- ------------------------------

CREATE TABLE customers (
    customer_id VARCHAR(255) PRIMARY KEY,
    customer_unique_id VARCHAR(255),
    customer_city VARCHAR(50),
    customer_state VARCHAR(20)
);

CREATE TABLE products (
    product_id VARCHAR(255) PRIMARY KEY,
    product_cat_name VARCHAR(100),
    product_weight INT,
    product_length INT,
    product_height INT,
    product_width INT
);

CREATE TABLE seller (
    seller_id VARCHAR(255) PRIMARY KEY,
    seller_city VARCHAR(50),
    seller_zip_code INT,
    seller_state VARCHAR(20)
);

CREATE TABLE orders (
    order_cust_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    order_status VARCHAR(50),
    purchase_date_time TIMESTAMP,
    approved_date_time TIMESTAMP,
    delivery_start TIMESTAMP,
    delivery_end TIMESTAMP,
    estimated_delivery TIMESTAMP
);

CREATE TABLE order_items (
    order_id VARCHAR(255),
    order_item_id INT,
    product_id VARCHAR(255),
    seller_id VARCHAR(255),
    order_price DECIMAL(10,2),
    order_freight_value DECIMAL(10,2),
    PRIMARY KEY (order_id, order_item_id)
);

-- ------------------------------
-- Create Fact Table
-- ------------------------------

CREATE TABLE seller_analysis_fct (
    customer_id VARCHAR(255),
    product_id VARCHAR(255),
    seller_id VARCHAR(255),
    order_id VARCHAR(255),
    order_cust_id VARCHAR(255),
    PRIMARY KEY (customer_id, product_id, seller_id, order_id, order_cust_id)
);
