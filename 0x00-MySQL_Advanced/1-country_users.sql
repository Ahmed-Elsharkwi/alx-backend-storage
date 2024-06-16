-- create table called users
CREATE TABLE IF NOT EXISTS users ( 
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email varchar(255) Not NULL unique,
	name varchar(255),
	country ENUM('US', 'CO', 'TN') Default 'US');
