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

-- Insert dummy users (password for all is 'password123')
INSERT IGNORE INTO users (id, username, password_hash, role, bio) VALUES
(1, 'admin', 'scrypt:32768:8:1$6wU4pwq3uQY3MiPK$a94c3ab5fec366c7a498962c3bb169c70e96c9e589c6c1b746821e574de56d9dc941eb20716f513234c4c0c01c4530500fa0f2c22a7a1d454240cd3e9503315d', 'admin', 'System Administrator'),
(2, 'student1', 'scrypt:32768:8:1$6wU4pwq3uQY3MiPK$a94c3ab5fec366c7a498962c3bb169c70e96c9e589c6c1b746821e574de56d9dc941eb20716f513234c4c0c01c4530500fa0f2c22a7a1d454240cd3e9503315d', 'student', 'Enthusiastic learner.'),
(3, 'instructor1', 'scrypt:32768:8:1$6wU4pwq3uQY3MiPK$a94c3ab5fec366c7a498962c3bb169c70e96c9e589c6c1b746821e574de56d9dc941eb20716f513234c4c0c01c4530500fa0f2c22a7a1d454240cd3e9503315d', 'instructor', 'Expert in Cybersecurity.');

-- Insert dummy receipts
INSERT IGNORE INTO receipts (receipt_id, user_id, course_id, amount, payment_method, billing_address, transaction_ref) VALUES
(1, 2, 1, 99.99, 'credit_card', '123 Learner St, Knowledge City', 'TXN-1234567890'),
(2, 2, 3, 149.99, 'paypal', '123 Learner St, Knowledge City', 'TXN-0987654321');
