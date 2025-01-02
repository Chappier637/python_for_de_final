-- Connect to the database

BEGIN;

-- Create the Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) UNIQUE,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    loyalty_status VARCHAR(20) CHECK (loyalty_status IN ('Gold', 'Silver', 'Bronze'))
);

-- Create the ProductCategories table
CREATE TABLE productCategories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_category_id INT REFERENCES ProductCategories(category_id)
);

-- Create the Products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category_id INT REFERENCES ProductCategories(category_id),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Pending', 'Completed', 'Canceled')),
    delivery_date TIMESTAMP
);

-- Create the OrderDetails table
CREATE TABLE orderDetails (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id),
    product_id INT REFERENCES Products(product_id),
    quantity INT NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * price_per_unit) STORED
);

-- Insert sample data into Users
INSERT INTO users (first_name, last_name, email, phone, loyalty_status) VALUES
('John', 'Doe', 'john.doe@example.com', '1234567890', 'Gold'),
('Jane', 'Smith', 'jane.smith@example.com', '0987654321', 'Silver'),
('Alice', 'Johnson', 'alice.johnson@example.com', '1122334455', 'Bronze'),
('Bob', 'Brown', 'bob.brown@example.com', '6677889900', 'Gold'),
('Carol', 'Davis', 'carol.davis@example.com', '4433221100', 'Silver');

-- Insert sample data into ProductCategories
INSERT INTO productCategories (name, parent_category_id) VALUES
('Electronics', NULL),
('Mobile Phones', 1),
('Laptops', 1),
('Home Appliances', NULL),
('Kitchen Appliances', 4);

-- Insert sample data into Products
INSERT INTO products (name, description, category_id, price, stock_quantity) VALUES
('iPhone 14', 'Latest Apple smartphone', 2, 999.99, 50),
('MacBook Pro', 'Apple laptop with M2 chip', 3, 1999.99, 20),
('Samsung Galaxy S23', 'High-end Samsung smartphone', 2, 899.99, 30),
('Dell XPS 13', 'Compact and powerful laptop', 3, 1499.99, 15),
('KitchenAid Mixer', 'Stand mixer for baking', 5, 299.99, 25),
('Dyson Vacuum', 'High-power vacuum cleaner', 4, 499.99, 10);

-- Insert sample data into Orders
INSERT INTO orders (user_id, total_amount, status, delivery_date) VALUES
(1, 2999.97, 'Completed', '2023-12-25'),
(2, 999.99, 'Pending', NULL),
(3, 1499.99, 'Completed', '2023-12-20'),
(4, 1799.98, 'Pending', NULL),
(5, 299.99, 'Completed', '2023-12-18');

-- Insert sample data into OrderDetails
INSERT INTO orderDetails (order_id, product_id, quantity, price_per_unit) VALUES
(1, 2, 1, 1999.99),
(1, 1, 1, 999.99),
(2, 1, 1, 999.99),
(3, 4, 1, 1499.99),
(4, 3, 1, 899.99),
(4, 6, 2, 449.99),
(5, 5, 1, 299.99);

COMMIT;