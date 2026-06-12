from flask import Blueprint, request, jsonify, session, current_app
import mysql.connector

api_bp = Blueprint('api_bp', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB']
    )

@api_bp.route('/search', methods=['GET'])
def search_courses():
    query = request.args.get('q', '')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # REMEDIATION: Using parameterized queries to prevent SQL Injection
        cursor.execute("SELECT * FROM courses WHERE title LIKE %s", ("%" + query + "%",))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "data": results})
    except mysql.connector.Error as e:
        # REMEDIATION: Swallow raw database error to avoid information disclosure
        return jsonify({"status": "error", "message": "Database error occurred."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500

@api_bp.route('/receipt/<int:receipt_id>', methods=['GET'])
def get_receipt(receipt_id):
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # REMEDIATION: Checking user_id to prevent IDOR (Broken Access Control)
        cursor.execute(
            "SELECT * FROM receipts WHERE receipt_id = %s AND user_id = %s", 
            (receipt_id, session['user_id'])
        )
        receipt = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if receipt:
            return jsonify({"status": "success", "data": receipt})
        else:
            return jsonify({"status": "error", "message": "Receipt not found or unauthorized access."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": "Database error occurred."}), 500
