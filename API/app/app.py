from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import threading
from datetime import timedelta

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admin:password@localhost:5440/mitescan')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # CORS configuration
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
    
    # Import models (important for migrations)
    from models import user, company, access, hive, bee_type, sensor, analysis_backup, hive_analysis
    
    # Register blueprints
    from routes.user_routes import user_bp
    from routes.company_routes import company_bp
    from routes.hive_routes import hive_bp
    from routes.sensor_routes import sensor_bp
    from routes.access_routes import access_bp
    from routes.bee_type_routes import bee_type_bp
    from routes.analysis_routes import analysis_bp
    from routes.hive_analysis_routes import hive_analysis_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(hive_bp)
    app.register_blueprint(sensor_bp)
    app.register_blueprint(access_bp)
    app.register_blueprint(bee_type_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(hive_analysis_bp)
    
    # Create tables and seed data
    with app.app_context():
        db.create_all()
        from seed import seed_data
        seed_data()
    
    # Start MQTT in background
    if not os.getenv("TESTING"):
        from mqtt_handler import start_mqtt_thread
        mqtt_thread = threading.Thread(target=start_mqtt_thread, daemon=True)
        mqtt_thread.start()
    
    @app.route('/')
    def health_check():
        return {'status': 'MiteScan API Flask is running!', 'version': '1.0.0'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)