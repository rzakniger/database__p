from flask import Blueprint, request, jsonify
import sqlite3
from auth import get_user_variables

clients_bp = Blueprint('clients_bp', __name__)

@clients_bp.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    nom = data.get('nom')
    telephone = data.get('telephone')
    adresse = data.get('adresse')
    codepromo = data.get('codepromo')

    if not nom or not telephone or not adresse:
        return jsonify({'message': 'Missing required fields'}), 400

    # Ajouter le client à la base de données
    client_info = add_client(nom, telephone, adresse, codepromo)
    if client_info:
        # Formater l'objet client_info avec les noms des champs
        formatted_client_info = {
            'ID': client_info[0],
            'Nom': client_info[1],
            'Téléphone': client_info[2],
            'Adresse': client_info[3],
            'Code Promo': client_info[4],
              'Date ajout': client_info[5],
            'Agent Référent': client_info[6],
            'Agence Référente': client_info[7],
            'message': 'Client added successfully'
        }
        return jsonify(formatted_client_info), 201
    else:
        return jsonify({'message': 'Failed to add client'}), 500

def add_client(nom, telephone, adresse, codepromo):
    # Récupérer les informations de l'utilisateur actuel
    user_id, _, username, agence, _, _ = get_user_variables()

    # Se connecter à la base de données
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Insérer le nouveau client dans la table des clients
    cursor.execute('INSERT INTO clients (nom, telephone, adresse, codepromo, refagent, refagence) VALUES (?, ?, ?, ?, ?, ?)',
                   (nom, telephone, adresse, codepromo, username, agence))
    conn.commit()

    # Récupérer les informations du client nouvellement inséré
    cursor.execute('SELECT * FROM clients WHERE id = ?', (cursor.lastrowid,))
    client_info = cursor.fetchone()

    # Fermer la connexion à la base de données
    conn.close()

    return client_info
