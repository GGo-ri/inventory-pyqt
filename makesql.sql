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
    ('10090', 9, '맨체스터 시티 엘링 홀란', 'HOME', 20, 195000),
    ('20041', 4, '리버풀 버질 반 다이크', 'AWAY', 5, 209000),
    ('30110', 11, '애스턴 빌라 올리 왓킨스', 'HOME', 15, 199000),
    ('40101', 10, '첼시 콜 팔머', 'AWAY', 30, 210000),
    ('50410', 41, '아스날 데클란 라이스', 'HOME', 20, 199000),
    ('60191', 19, '맨체스터 유나이티드 브라이언 음뵈모', 'AWAY', 3, 219000)
ON DUPLICATE KEY UPDATE
    stock = VALUES(stock),
    price = VALUES(price);