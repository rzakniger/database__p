import sqlite3
from flask import jsonify

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
                        retirer BOOLEAN DEFAULT 0)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                        id INTEGER PRIMARY KEY,
                        article TEXT NOT NULL,
                        quantite INTEGER,
                        refid INTEGER,
                        idtelephone INTEGER,
                        montant FLOAT,
                        mtotal FLOAT,
                        datedepot TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        daterdv TIMESTAMP,
                        datemiseajour TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        retirer BOOLEAN DEFAULT 0,
                        FOREIGN KEY (idtelephone) REFERENCES clients(id))''')
    
    conn.commit()
    conn.close()

def add_client(nom, telephone, adresse, codepromo):
    init_db()
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (nom, telephone, adresse, codepromo) VALUES (?, ?, ?, ?)',
                   (nom, telephone, adresse, codepromo))
    conn.commit()
    # Récupérer l'ID du client nouvellement inséré
    client_id = cursor.lastrowid
    conn.close()
    return client_id

def add_article(article, quantite, refid, idtelephone, montant, mtotal, daterdv):
    init_db()
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO articles (article, quantite, refid, idtelephone, montant, mtotal, daterdv) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (article, quantite, refid, idtelephone, montant, mtotal, daterdv))
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

