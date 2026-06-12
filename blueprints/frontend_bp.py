# pyrefly: ignore [missing-import]
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

frontend_bp = Blueprint('frontend_bp', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB']
    )

@frontend_bp.route('/')
def home():
    return render_template('index.html')

@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash('Login successful!', 'success')
                return redirect(url_for('frontend_bp.dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        except Exception as e:
            flash('Database connection error', 'danger')
            
    return render_template('login.html', action='Login')

@frontend_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # REMEDIATION: Hash password using a strong algorithm (PBKDF2)
        hashed_pw = generate_password_hash(password)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('frontend_bp.login'))
        except mysql.connector.IntegrityError:
            flash('Username already exists', 'danger')
        except Exception as e:
            flash('Registration failed', 'danger')
            
    return render_template('login.html', action='Register')

@frontend_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('frontend_bp.home'))

@frontend_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('frontend_bp.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        bio = request.form.get('bio', '')
        # We simply store the bio. Jinja2 will auto-escape it upon rendering (mitigating XSS).
        cursor.execute("UPDATE users SET bio = %s WHERE id = %s", (bio, session['user_id']))
        conn.commit()
        flash('Bio updated successfully.', 'success')
        
    cursor.execute("SELECT bio FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', bio=user['bio'] if user else '')

@frontend_bp.route('/search')
def search():
    return render_template('search.html')
