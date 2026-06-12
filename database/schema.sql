CREATE DATABASE IF NOT EXISTS myeduconnect;
USE myeduconnect;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    bio TEXT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT NULL
);

CREATE TABLE IF NOT EXISTS receipts (
    receipt_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    course_id INT,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    billing_address VARCHAR(255) NOT NULL,
    transaction_ref VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Insert dummy data
INSERT IGNORE INTO courses (title, description) VALUES 
('Introduction to Cybersecurity', 'Learn the basics of securing networks and applications.'),
('Advanced Web Development', 'Master modern web frameworks and secure coding practices.'),
('Data Structures and Algorithms', 'Core fundamentals of computer science.'),
('Ethical Hacking 101', 'An overview of penetration testing methodologies.');
