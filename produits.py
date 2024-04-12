from flask import Blueprint, request, jsonify
import sqlite3
import datetime

app = Blueprint('produits', __name__)

# Création de la table 'produits' si elle n'existe pas déjà
def init_produits_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS produits (
                        id INTEGER PRIMARY KEY,
                        nom TEXT NOT NULL,
                        prix REAL NOT NULL,
                        dateadd TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        datemiseamise TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Initialisation de la table des produits
init_produits_table()

@app.route('/produits', methods=['POST'])
def create_produit():
    data = request.json
    nom = data.get('nom')
    prix = data.get('prix')

    if not nom or not prix:
        return jsonify({'message': 'Missing required fields'}), 400

    # Ajouter le produit à la base de données
    produit_id = add_produit(nom, prix)
    if produit_id:
        return jsonify({'message': 'Produit added successfully', 'produit_id': produit_id}), 201
    else:
        return jsonify({'message': 'Failed to add produit'}), 500

def add_produit(nom, prix):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Insérer le nouveau produit dans la table des produits
    cursor.execute('INSERT INTO produits (nom, prix) VALUES (?, ?)', (nom, prix))
    conn.commit()

    # Récupérer l'ID du produit nouvellement inséré
    produit_id = cursor.lastrowid

    # Fermer la connexion à la base de données
    conn.close()

    return produit_id

    


def fetch_produits_by_criteria(produit_id=None, nom=None, prix=None):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM produits'
    conditions = []
    parameters = []

    # Ajouter les conditions de recherche en fonction des paramètres fournis
    if produit_id:
        conditions.append('id=?')
        parameters.append(produit_id)

    if nom:
        conditions.append('nom=?')
        parameters.append(nom)

    if prix:
        conditions.append('prix=?')
        parameters.append(prix)

    # Combiner toutes les conditions avec 'AND'
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, parameters)
    
    produits = [
        {
            'id': row[0],
            'nom': row[1],
            'prix': row[2],
            'dateadd': row[3],
            'datemiseamise': row[4]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return produits


