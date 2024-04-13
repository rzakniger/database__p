import sqlite3
from auth import get_user_variables
from lastseen import update_last_seen
from produits import fetch_produits_by_criteria
from flask import Flask, request, jsonify
from datetime import datetime



def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY,
                        nom TEXT NOT NULL,
                        telephone TEXT NOT NULL,
                        adresse TEXT NOT NULL,
                        codepromo TEXT,
                        date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        refagent TEXT NOT NULL,
                        refagence TEXT NOT NULL,
                        retirer BOOLEAN DEFAULT 0)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS "articles" (
            "id"	INTEGER,
            "article"	TEXT NOT NULL,
            "quantite"	INTEGER,
            "refid"	INTEGER,
            "idtelephone"	INTEGER,
            "montant"	FLOAT,
            "mtotal"	FLOAT,
            "refagent"	TEXT NOT NULL,
            "refagence"	TEXT NOT NULL,
            "datedepot"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            "daterdv"	TIMESTAMP,
            "datemiseajour"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            "retirer"	BOOLEAN DEFAULT 0,
            "refcodepromo"	TEXT,
            PRIMARY KEY("id"),
            FOREIGN KEY("idtelephone") REFERENCES "clients"("id")
        );''')
            
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        telephone TEXT NOT NULL,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        agence TEXT,
                        lastseen TIMESTAMP,
                        datecreate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        role TEXT,
                        privileges TEXT
                    );''')    
    
    conn.commit()
    conn.close()
    
init_db()

def add_client(nom, telephone, adresse, codepromo):
    # Récupérer les informations de l'utilisateur actuel
  
    # Connecter à la base de données
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Insérer le nouveau client dans la table des clients
    cursor.execute('INSERT INTO clients (nom, telephone, adresse, codepromo, refagent, refagence) VALUES (?, ?, ?, ?, ?, ?)',
                   (nom, telephone, adresse, codepromo, username, agence))
    conn.commit()

    # Récupérer l'ID du client nouvellement inséré
    client_id = cursor.lastrowid

    # Récupérer les informations du client nouvellement inséré
    cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    client_info = cursor.fetchone()

    # Fermer la connexion à la base de données
    conn.close()

    return client_info

def add_article(article, quantite, refid, idtelephone, daterdv):
    user_id, telephone, username, agence, role, privileges = get_user_variables()
    
    vararticle = fetch_produits_by_criteria(produit_id=article)
    
    
    if vararticle:
        for produit in vararticle:
            produit_id = produit['id']
            nom = produit['nom']
            prix = produit['prix']
            dateadd = produit['dateadd']
            datemiseamise = produit['datemiseamise']
          
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO articles (article, quantite, refid, idtelephone, montant, mtotal, daterdv, refagent,refagence) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)',
                   (nom, 
                    quantite, 
                    refid,
                    idtelephone, 
                    prix,
                    prix * quantite,
                    daterdv,
                    username,
                    agence ))
    conn.commit()

    

    conn.close()

def get_clients(identifier=None):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    if identifier:
        cursor.execute('SELECT * FROM clients WHERE id=? OR telephone=? OR codepromo=?', (identifier, identifier, identifier))
    else:
        cursor.execute('SELECT * FROM clients')
        
    clients = [
        {'id': row[0], 'nom': row[1], 'telephone': row[2], 'adresse': row[3], 'codepromo': row[4], 'date_ajout': row[5], 'retirer': row[6]}
        for row in cursor.fetchall()
    ]
    
    conn.close()
    return clients

def repartir_montant(refid, idtelephone, montant_avance):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Sélectionner tous les articles du même refid et idtelephone, triés par montant décroissant
    cursor.execute('SELECT * FROM articles WHERE refid=? AND idtelephone=? ORDER BY montant DESC', (refid, idtelephone))
    articles = cursor.fetchall()

    montant_restant = montant_avance

    result = []
    for article in articles:
        montant_article = article[5]
        if montant_restant >= montant_article:
            montant_paye = montant_article
            montant_restant -= montant_paye
        else:
            montant_paye = montant_restant
            montant_restant = 0
        result.append({
            'article': article[1],
            'montant': montant_article,
            'montant_restant': montant_article - montant_paye,
            'datedepot': article[7],
            'daterdv': article[8],
            'datemiseajour': article[9],
            'retirer': article[10]
        })

    conn.close()
    return result
