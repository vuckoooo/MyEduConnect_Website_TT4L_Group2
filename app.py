import os
from flask import Flask
from blueprints.frontend_bp import frontend_bp
from blueprints.api_bp import api_bp

def create_app():
    app = Flask(__name__)
    # Secure secret key for session management
    app.secret_key = os.urandom(24)
    
    # Configure Database Connection Settings
    # Defaulting to standard localhost with root for dev setup
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '' # Update if your local MySQL has a password
    app.config['MYSQL_DB'] = 'myeduconnect'

    # Register Blueprints
    app.register_blueprint(frontend_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
