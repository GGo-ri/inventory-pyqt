CREATE DATABASE IF NOT EXISTS jerseydb DEFAULT CHARACTER SET utf8mb4;

USE jerseydb;

CREATE TABLE IF NOT EXISTS users (
	id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'GUEST'
);

INSERT INTO users (username, password, role)
VALUES ('GGori', 'GGori0516', 'ADMIN')
ON DUPLICATE KEY UPDATE password = VALUES(password), role = VALUES(role);

CREATE TABLE IF NOT EXISTS jerseys (
	id INT PRIMARY KEY AUTO_INCREMENT,
    serial_number VARCHAR(10) UNIQUE NOT NULL,
    back_number INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    jersey_type VARCHAR(10) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    price INT NOT NULL DEFAULT 0
);

INSERT INTO jerseys (serial_number, back_number, product_name, jersey_type, stock, price)
VALUES
	('10090', 9, '엘링 홀란(MCI)', 'HOME', 20, 195000)
ON DUPLICATE KEY UPDATE
	stock = VALUES(stock),
    price = VALUES(price);