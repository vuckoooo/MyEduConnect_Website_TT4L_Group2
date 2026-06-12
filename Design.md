# Detailed Design Document: MyEduConnect Vulnerable Platform

## 1. Overview
This document outlines the detailed technical design for the MyEduConnect vulnerable educational platform. The system is architected as a monolithic Python Flask application utilizing Flask Blueprints to separate frontend routing from internal API logic. It is designed to be deployed natively on a VMware Linux guest OS using raw processes.

**Development Team:** Shun Hong, Aiden Chan Kai Ming, Too Jun Chen

## 2. System Architecture & Environment
* **Host Environment:** VMware Virtual Machine (Linux OS).
* **Process Management:** Native execution (no Docker/containerization). The database, web server, and application will run as standard system processes.
* **Web Server:** Apache HTTP Server. Acts as the primary entry point, serving static assets, exposing the vulnerable admin directory, and reverse-proxying traffic to the Flask application.
* **Application Server:** Python (Flask) running on a single port (e.g., `5000`).
* **Database Engine:** Native MySQL Server.

---

## 3. Module Design (Flask Blueprints)
The application is logically divided into two primary blueprints to ensure testability and isolation of logic, despite running in a single repository and process.

### 3.1. `frontend_bp` (Main Web Application)
* **Responsibility:** Handles user authentication, session management, and rendering HTML templates (Jinja2).
* **Routing:** * `/` -> Homepage
  * `/login` & `/register` -> Authentication
  * `/dashboard` -> Student profile (Vulnerable to Stored XSS)
  * `/search` -> Course search interface. Acts as a pass-through to the API blueprint.
* **Design Note:** Must blindly forward search queries to the API and render any raw database error messages returned by the API to facilitate SQL injection exploitation.

### 3.2. `api_bp` (Internal REST API)
* **Responsibility:** Handles raw data retrieval and database interactions.
* **Routing:**
  * `GET /api/search?q=<query>` -> Returns course data (Vulnerable to SQLi).
  * `GET /api/receipt/<receipt_id>` -> Returns receipt JSON (Vulnerable to IDOR).

### 3.3. Static Admin Module (Apache Managed)
* **Responsibility:** Simulates an exposed, legacy administrative interface.
* **Implementation:** Served directly by Apache bypassing Flask entirely. Located at `/admin-portal/`. Consists of static `.html` files.

---

## 4. Database Schema Design
The MySQL database will consist of the following tables, designed specifically to support the required exploits.

### Table: `users`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier. |
| `username` | VARCHAR(50) | UNIQUE, NOT NULL | Login credential. |
| `password_md5` | VARCHAR(32) | NOT NULL | Vulnerability: Raw, unsalted MD5 hash. |
| `role` | VARCHAR(20) | DEFAULT 'student' | Defines access level ('student' or 'admin'). |
| `bio` | TEXT | NULL | Vulnerability: Stores raw HTML for XSS payload. |

### Table: `courses`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique course identifier. |
| `title` | VARCHAR(100) | NOT NULL | Course name. |
| `description` | TEXT | NULL | Course details. |

### Table: `receipts`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `receipt_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Predictable integer for IDOR enumeration. |
| `user_id` | INT | FOREIGN KEY (`users.id`) | Owner of the receipt. |
| `course_id` | INT | FOREIGN KEY (`courses.id`) | Purchased course. |
| `amount` | DECIMAL(10,2) | NOT NULL | Transaction cost. |
| `payment_method` | VARCHAR(50) | NOT NULL | e.g., "Visa ending in 4242". |
| `billing_address` | VARCHAR(255) | NOT NULL | Sensitive PII for impact demonstration. |
| `transaction_ref` | VARCHAR(100) | NOT NULL | Sensitive gateway reference. |

---

## 5. Vulnerability Implementation Specifications

### 5.1. SQL Injection (API Blueprint)
* **Location:** `api_bp` -> `GET /api/search?q=`
* **Mechanism:** The `q` parameter is concatenated directly into the SQL statement string. 
* **Query Design:** `f"SELECT * FROM courses WHERE title LIKE '%{request.args.get('q')}%'"`
* **Feedback Loop:** A `try/except` block must catch `mysql.connector.Error` and return the exact `e.msg` in the JSON response, which `frontend_bp` will render to the user.

### 5.2. Stored XSS (Frontend Blueprint)
* **Location:** `frontend_bp` -> `POST /dashboard/update_bio` & `GET /dashboard`
* **Mechanism:** The POST request saves the bio field to the database without `htmlspecialchars` or sanitization. The GET request renders the bio in the Jinja2 template using the `| safe` filter (e.g., `{{ user.bio | safe }}`).

### 5.3. Broken Access Control / IDOR (API Blueprint)
* **Location:** `api_bp` -> `GET /api/receipt/<receipt_id>`
* **Mechanism:** Queries the `receipts` table exclusively using the `receipt_id` provided in the URL. It explicitly *omits* checking if `session['user_id'] == receipt.user_id`. Returns the full JSON payload including `billing_address` and `transaction_ref`.

### 5.4. Exposed Administrative Interface (Apache Config)
* **Location:** `/admin-portal/`
* **Mechanism:** A physical directory mapped in Apache's `VirtualHost` block. Because it consists of static HTML files served by Apache before requests hit the Flask reverse proxy, Flask's session cookies and `@login_required` decorators are completely bypassed.

### 5.5. Open Directory Listing (Apache Config)
* **Location:** `/assets/internal_docs/`
* **Mechanism:** Configured in the Apache `httpd.conf` or `.htaccess` file using the `Options +Indexes` directive. A fake `database_backups.txt` will be placed here.