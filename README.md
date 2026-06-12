# MyEduConnect Environment Setup Guide

This guide outlines the steps to set up the infrastructure required for the MyEduConnect platform, including the Apache web server, the database, and the Python environment.

Because you may develop on Windows and deploy/test on Linux, two separate installation paths are provided below.

---

## 1. Local Windows Development Setup
*Use this environment for your main coding and editing workflow.*

### 1.1. Download and Install XAMPP
1. Download XAMPP from [apachefriends.org](https://www.apachefriends.org/).
2. Run the installer and ensure **Apache** and **MySQL** are selected.
3. Open the **XAMPP Control Panel**.
4. Click **Start** next to both Apache and MySQL.

### 1.2. Configure Apache as a Reverse Proxy
To allow Apache to route traffic to your Flask app, you must enable proxy modules.
1. In the XAMPP Control Panel, click **Config** next to Apache and select **httpd.conf**.
2. Find and uncomment (remove the `#`) from the following lines:
   ```apache
   LoadModule proxy_module modules/mod_proxy.so
   LoadModule proxy_http_module modules/mod_proxy_http.so
   ```
3. Scroll to the very bottom of the file and add the reverse proxy configuration:
   ```apache
   ProxyPass / http://127.0.0.1:5000/
   ProxyPassReverse / http://127.0.0.1:5000/
   ```
4. Click **Stop** and then **Start** on Apache in the XAMPP control panel to restart it.

### 1.3. Database Initialization
1. Open your command line / terminal and navigate to your project directory.
2. Log into MySQL as the root user (XAMPP usually has no password by default):
   ```bash
   mysql -u root
   ```
   *(If `mysql` is not recognized, click the "Shell" button in the XAMPP control panel and type it there).*
3. Load the database schema:
   ```sql
   source database/schema.sql;
   exit;
   ```

### 1.4. Running the Flask Application
1. Open a terminal in your project directory.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   python app.py
   ```
4. Access the application by navigating to `http://127.0.0.1:5000` or `http://localhost`.

---

## 2. Linux OS Deployment (Kali / Debian / Ubuntu)
*Use this environment when deploying or testing inside your VMware Linux guest OS.*

### 2.1. Get the Source Code
Open your terminal and download your project from GitHub:
```bash
git clone https://github.com/vuckoooo/MyEduConnect_Website_TT4L_Group2.git
cd MyEduConnect_Website_TT4L_Group2
```

### 2.2. Install Requirements
Install the Apache web server, MariaDB (the drop-in replacement for MySQL), and Python tools:
```bash
sudo apt update
sudo apt install apache2 mariadb-server python3 python3-pip git
```

### 2.3. Configure Apache as a Reverse Proxy
Enable the necessary proxy modules so Apache can forward traffic to Flask:
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
```
Next, configure your virtual host:
1. Open the default Apache configuration file:
   ```bash
   sudo nano /etc/apache2/sites-available/000-default.conf
   ```
2. Paste the following proxy settings right before the `</VirtualHost>` tag at the very bottom:
   ```apache
   ProxyPass / http://127.0.0.1:5000/
   ProxyPassReverse / http://127.0.0.1:5000/
   ```
3. Save, exit (`Ctrl+O`, `Enter`, `Ctrl+X`), and restart Apache:
   ```bash
   sudo systemctl restart apache2
   ```

### 2.4. Database Initialization
Start the MariaDB service and import your database schema directly:
```bash
sudo systemctl start mariadb
sudo mysql -u root < database/schema.sql
```

### 2.5. Running the Flask Application
1. Install the required Python packages (use the break-system-packages flag for Kali/Debian's strict environments):
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```
2. Start the application:
   ```bash
   python3 app.py
   ```
3. Access the application by navigating to `http://127.0.0.1:5000` or your Linux machine's IP address.
