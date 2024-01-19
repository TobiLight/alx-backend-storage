-- Creates a table with unique users.
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE, name VARCHAR(255)
);