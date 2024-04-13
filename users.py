from flask import Blueprint, request, jsonify
import sqlite3

app = Blueprint('users', __name__)

# Route pour créer un nouvel utilisateur
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    telephone = data['telephone']
    username = data['username']
    password = data['password']
    agence = data.get('agence', None)
    role = data.get('role', None)
    privileges = data.get('privileges', None)

    # Insérer les données dans la base de données
    conn = sqlite3.connect('data.db')
    
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (telephone, username, password, agence, role, privileges) VALUES (?, ?, ?, ?, ?, ?)',
                   (telephone, username, password, agence, role, privileges))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User created successfully'}), 201


def fetch_users_by_criteria(user_id=None, telephone=None, username=None, agence=None, role=None):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM users'
    conditions = []
    parameters = []

    # Ajouter les conditions de recherche en fonction des paramètres fournis
    if user_id:
        conditions.append('id=?')
        parameters.append(user_id)

    if telephone:
        conditions.append('telephone=?')
        parameters.append(telephone)

    if username:
        conditions.append('username=?')
        parameters.append(username)

    if agence:
        conditions.append('agence=?')
        parameters.append(agence)

    if role:
        conditions.append('role=?')
        parameters.append(role)

    # Combiner toutes les conditions avec 'AND'
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, parameters)
    
    users = [
        {
            'id': row[0],
            'telephone': row[1],
            'username': row[2],
            'agence': row[4],
            'role': row[7],
            'privileges': row[8]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return users

# Route pour obtenir tous les utilisateurs ou en fonction des critères de recherche
@app.route('/users', methods=['GET'])
def get_users():
    # Récupérer les paramètres de requête
    user_id = request.args.get('id')
    telephone = request.args.get('telephone')
    username = request.args.get('username')
    agence = request.args.get('agence')
    role = request.args.get('role')

    # Utiliser la fonction fetch_users_by_criteria avec les paramètres fournis
    users = fetch_users_by_criteria(user_id, telephone, username, agence, role)

    return jsonify(users)