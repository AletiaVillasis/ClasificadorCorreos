import jwt
import bcrypt
import datetime
from functools import wraps
from flask import request, jsonify
from config import SECRET_KEY, JWT_EXP_DAYS
from database import get_user_by_email, insert_user

def generate_token(user):
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=JWT_EXP_DAYS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"success": False, "message": "Token requerido"}), 401

        try:
            token = token.replace("Bearer ", "")
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = decoded["user_id"]
        except Exception:
            return jsonify({"success": False, "message": "Token inválido"}), 401

        return f(*args, **kwargs)
    return wrapper
