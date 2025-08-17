USE ecommerce;

-- Users
INSERT INTO users (username, email, password, role) VALUES
('alice', 'alice@mail.com', 'pass123', 'customer'),
('bob', 'bob@mail.com', 'pass123', 'vendor'),
('charlie', 'charlie@mail.com', 'pass123', 'vendor');

-- Vendors
INSERT INTO vendors (user_id, vendor_name) VALUES
(2, 'Bob Store'),
(3, 'Charlie Shop');

-- Products
INSERT INTO products (vendor_id, name, description, price, stock) VALUES
(1, 'Laptop', 'Gaming laptop', 800.00, 10),
(1, 'Mouse', 'Wireless mouse', 20.00, 50),
(2, 'Headphones', 'Noise cancelling', 100.00, 25);

-- Cart
INSERT INTO cart (user_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 2, 2);

-- Orders
INSERT INTO orders (user_id, total) VALUES
(1, 840.00);

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 800.00),
(1, 2, 2, 20.00);
