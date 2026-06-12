# MyEduConnect Environment Setup Guide

This guide outlines the steps to set up the infrastructure required for the MyEduConnect platform, including the Apache web server, MySQL database, and Python environment.

---

## 1. Local Windows Development Setup
If you are testing the application locally on your Windows machine, using a bundled software stack like XAMPP is the easiest method.

### 1.1. Download and Install XAMPP
1. Download XAMPP from [apachefriends.org](https://www.apachefriends.org/).
2. Run the installer and ensure **Apache** and **MySQL** are selected.
3. Open the **XAMPP Control Panel**.
4. Click **Start** next to both Apache and MySQL.

### 1.2. Configure Apache as a Reverse Proxy (Windows)
To allow Apache to route traffic to your Flask app, you must enable proxy modules.
1. In the XAMPP Control Panel, click **Config** next to Apache and select **httpd.conf**.
2. Find and uncomment (remove the `#`) from the following lines:
   ```apache
   LoadModule proxy_module modules/mod_proxy.so
   LoadModule proxy_http_module modules/mod_proxy_http.so
   ```
3. Add the configuration block from `secure_apache_example.conf` to the bottom of the file (making sure to adjust the `DocumentRoot` path to where your project is stored).
4. Restart Apache from the XAMPP control panel.

---

## 2. VMware Linux OS Deployment
When you deploy the application to your VMware Linux guest OS, you should install the native packages via the command line.

### 2.1. Install Requirements (Ubuntu/Debian)
Open your terminal and run the following commands:
```bash
# Update package lists
sudo apt update

# Install Apache Web Server
sudo apt install apache2

# Install MySQL Server
sudo apt install mysql-server

# Install Python 3 and pip
sudo apt install python3 python3-pip
```

### 2.2. Configure Apache as a Reverse Proxy (Linux)
Enable the necessary proxy modules so Apache can forward traffic to Flask:
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```
*Note: You will place the contents of `secure_apache_example.conf` inside `/etc/apache2/sites-available/000-default.conf`.*

---

## 3. Database Initialization (Both OS)

Once MySQL is running (either via XAMPP or Linux):
1. Open your command line / terminal.
2. Log into MySQL as the root user:
   ```bash
   mysql -u root -p
   ```
   *(If you are using XAMPP locally, there might be no password by default, so just `mysql -u root` will work).*
3. Load the database schema:
   ```bash
   source /path/to/your/project/database/schema.sql;
   ```
   *Alternatively, if you are outside the MySQL prompt, you can run:*
   `mysql -u root < database/schema.sql`

---

## 4. Running the Flask Application

1. Open a terminal in the `Website` directory.
2. Install the required Python packages (only needs to be done once):
   ```bash
   pip install -r requirements.txt
   ```
3. Check the `app.py` file. If your MySQL root user has a password, update line 15:
   ```python
   app.config['MYSQL_PASSWORD'] = 'your_password_here'
   ```
4. Start the application:
   ```bash
   python app.py
   ```
5. You can now access the application by navigating to `http://127.0.0.1:5000` or via your Apache server URL.
