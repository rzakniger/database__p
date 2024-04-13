from flask import Blueprint, request, jsonify
import sqlite3

# Création du Blueprint
agence_bp = Blueprint('agence_bp', __name__)

# Fonction pour initialiser la table des agences
def init_agences_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS agences (
                        id INTEGER PRIMARY KEY,
                        agence TEXT NOT NULL,
                        adresse TEXT NOT NULL,
                        telephone TEXT NOT NULL,
                        horaireouverture TEXT,
                        horairefermeture TEXT,
                        positiongps TEXT,
                        photocoverurl TEXT
                    )''')
    conn.commit()
    conn.close()

# Initialisation de la table des agences
init_agences_table()

# Route pour créer une nouvelle agence
@agence_bp.route('/agences', methods=['POST'])
def create_agence():
    data = request.json
    agence = data.get('agence')
    adresse = data.get('adresse')
    telephone = data.get('telephone')
    horaireouverture = data.get('horaireouverture')
    horairefermeture = data.get('horairefermeture')
    positiongps = data.get('positiongps')
    photocoverurl = data.get('photocoverurl')

    if not agence or not adresse or not telephone:
        return jsonify({'message': 'Missing required fields'}), 400

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Insérer la nouvelle agence dans la table des agences
    cursor.execute('''INSERT INTO agences (agence, adresse, telephone, horaireouverture, horairefermeture, positiongps, photocoverurl)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (agence, adresse, telephone, horaireouverture, horairefermeture, positiongps, photocoverurl))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Agence created successfully'}), 201

# Route pour lire toutes les agences
@agence_bp.route('/agences', methods=['GET'])
def get_all_agences():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Récupérer toutes les agences dans la table des agences
    cursor.execute('SELECT * FROM agences')
    agences = cursor.fetchall()

    conn.close()

    return jsonify({'agences': agences}), 200

# Route pour lire une agence par son ID
@agence_bp.route('/agences/<int:agence_id>', methods=['GET'])
def get_agence(agence_id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Récupérer l'agence par son ID
    cursor.execute('SELECT * FROM agences WHERE id = ?', (agence_id,))
    agence = cursor.fetchone()

    conn.close()

    if agence:
        return jsonify({'agence': agence}), 200
    else:
        return jsonify({'message': 'Agence not found'}), 404

# Route pour mettre à jour une agence
@agence_bp.route('/agences/<int:agence_id>', methods=['PUT'])
def update_agence(agence_id):
    data = request.json
    agence = data.get('agence')
    adresse = data.get('adresse')
    telephone = data.get('telephone')
    horaireouverture = data.get('horaireouverture')
    horairefermeture = data.get('horairefermeture')
    positiongps = data.get('positiongps')
    photocoverurl = data.get('photocoverurl')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Mettre à jour l'agence dans la table des agences
    cursor.execute('''UPDATE agences SET agence=?, adresse=?, telephone=?, horaireouverture=?, horairefermeture=?, positiongps=?, photocoverurl=?
                      WHERE id=?''',
                   (agence, adresse, telephone, horaireouverture, horairefermeture, positiongps, photocoverurl, agence_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Agence updated successfully'}), 200
