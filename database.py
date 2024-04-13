import sqlite3

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
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (nom, telephone, adresse, codepromo) VALUES (?, ?, ?, ?)',
                   (nom, telephone, adresse, codepromo))
    conn.commit()
    # Récupérer l'ID du client nouvellement inséré
    client_id = cursor.lastrowid
    conn.close()
    return client_id

def get_clients():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    conn.close()
    return clients

# Ajoutez d'autres opérations CRUD pour les clients selon vos besoins

def add_article(article, quantite, refid, idtelephone, montant, mtotal, daterdv):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO articles (article, quantite, refid, idtelephone, montant, mtotal, daterdv) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (article, quantite, refid, idtelephone, montant, mtotal, daterdv))
    conn.commit()
    conn.close()

def get_articles():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()
    conn.close()
    return articles

# Ajoutez d'autres opérations CRUD pour les articles selon vos besoins
