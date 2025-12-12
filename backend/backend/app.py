from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
from auth import generate_token, login_required
from database import init_db, get_user_by_email, insert_user
import jwt

app = Flask(__name__)
CORS(app)

init_db()  # Crea tablas al iniciar


# -----------------------------
# REGISTER
# -----------------------------
@app.post("/api/register")
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if get_user_by_email(email):
        return jsonify({"success": False, "message": "El email ya está registrado"}), 400

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    insert_user(username, email, password_hash)

    return jsonify({"success": True, "message": "Usuario creado"})


# -----------------------------
# LOGIN
# -----------------------------
@app.post("/api/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)
    if not user:
        return jsonify({"success": False, "message": "Credenciales inválidas"}), 400

    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify({"success": False, "message": "Credenciales inválidas"}), 400

    token = generate_token(user)

    return jsonify({
        "success": True,
        "token": token,
        "user_id": user["id"],
        "username": user["username"]
    })


# -----------------------------
# LOGOUT
# -----------------------------
@app.post("/api/logout")
def logout():
    return jsonify({"success": True, "message": "Sesión cerrada"})


# -----------------------------
# EJEMPLO DE RUTA PROTEGIDA
# -----------------------------
@app.get("/api/protegida")
@login_required
def protegida():
    return jsonify({"success": True, "message": "Acceso permitido"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

