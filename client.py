from flask import Blueprint, request, jsonify
import sqlite3
from auth import get_user_variables
import json 

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



import sqlite3
def calculate_client_statistics(client_id=None, telephone=None, codepromo=None):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Requête pour récupérer les statistiques des clients
    query = 'SELECT COUNT(*) AS total_clients FROM clients'
    conditions = []
    parameters = []

    # Ajouter les conditions de filtrage en fonction des paramètres fournis
    if client_id:
        conditions.append('id=?')
        parameters.append(client_id)

    if telephone:
        conditions.append('telephone=?')
        parameters.append(telephone)

    if codepromo:
        conditions.append('codepromo=?')
        parameters.append(codepromo)

    # Combiner toutes les conditions avec 'AND'
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, parameters)
    total_clients = cursor.fetchone()[0]  # Nombre total de clients

    # Requête pour récupérer les statistiques des articles associés aux clients
    if conditions:
        articles_query = """
                        SELECT SUM(quantite) AS total_quantite,
                               SUM(CASE WHEN retirer=0 THEN quantite ELSE 0 END) AS total_quantite_non_retire,
                               SUM(CASE WHEN retirer=1 THEN quantite ELSE 0 END) AS total_quantite_retire
                        FROM articles
                        WHERE refid IN (SELECT id FROM clients WHERE {})
                        OR idtelephone IN (SELECT telephone FROM clients WHERE {})
                        """.format(' AND '.join(conditions), ' AND '.join(conditions))
        
        # Remplacer la sous-requête avec des placeholders
        articles_query = articles_query.format(' AND '.join(['?'] * len(conditions)), ' AND '.join(['?'] * len(conditions)))

        # Passer les valeurs des paramètres dans la fonction execute
        cursor.execute(articles_query, parameters * 2)  # Dupliquer les valeurs pour chaque placeholder
    else:
        articles_query = """
                        SELECT SUM(quantite) AS total_quantite,
                               SUM(CASE WHEN retirer=0 THEN quantite ELSE 0 END) AS total_quantite_non_retire,
                               SUM(CASE WHEN retirer=1 THEN quantite ELSE 0 END) AS total_quantite_retire
                        FROM articles
                        """

        cursor.execute(articles_query)

    article_statistics = cursor.fetchone()

    conn.close()

    return total_clients, article_statistics

# Exemple d'utilisation avec tous les paramètres possibles
total_client, articlestatistics = calculate_client_statistics()

# Affichage des résultats
print("Nombre total de clients:", total_client)
print("Statistiques des articles associés au client:", articlestatistics)
