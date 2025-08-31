from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import jsonify
import bcrypt

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(email: str, password: str, db):
    """Authenticate user with email and password"""
    from models.user import User
    
    user = db.session.query(User).filter(User.email == email).first()
    if not user:
        return False
    
    if not verify_password(password, user.password_hash):
        return False
    
    return user

def create_user_token(user_id: int) -> str:
    """Create JWT token for user"""
    return create_access_token(identity=user_id)

def get_current_user(db):
    """Get current user from JWT token"""
    from models.user import User
    
    user_id = get_jwt_identity()
    if not user_id:
        return None
    
    return db.session.query(User).filter(User.id == user_id).first()

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        from app import db
        current_user = get_current_user(db)
        
        if not current_user or current_user.access_id != 1:  # Assuming 1 is admin
            return jsonify({'message': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function