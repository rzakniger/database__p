from flask import Blueprint, request, jsonify, make_response
import sqlite3
import jwt
import datetime
from functools import wraps
import secrets
from users import fetch_users_by_criteria

login_bp = Blueprint('login_bp', __name__)

# Fonction de vérification de l'authentification
def authenticate(username, password):
    # Vérifier les informations d'authentification dans la base de données
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Fonction de génération de token JWT
def generate_token(username):
    # Créer un token JWT contenant le nom d'utilisateur et une expiration
    token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, secret_key)
    return token

# Middleware pour la validation du token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')  # Récupérer le token depuis les cookies
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Décoder et vérifier le token JWT
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated

# Route pour l'authentification
@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Vérifier les informations d'authentification
    user = authenticate(username, password)
    if user:
        # Générer un token JWT
        token = generate_token(username)
        # Créer une réponse avec le token dans les cookies
        response = make_response(jsonify({'message': 'Login successful'}))
        response.set_cookie('token', token, httponly=True)
        return response, 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# Exemple de route protégée nécessitant un token JWT valide
@login_bp.route('/protected', methods=['GET'])
@token_required
def protected_route():
    return jsonify({'message': 'This is a protected route'}), 200

# Clé secrète pour le token JWT
secret_key = secrets.token_hex(32)
