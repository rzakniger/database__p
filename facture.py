import sqlite3
from datetime import datetime

def create_facture_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Vérifier si la table facture existe déjà
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='facture' ''')
    if cursor.fetchone()[0] == 1:
        print('La table facture existe déjà.')
    else:
        # Créer la table facture
        cursor.execute(''' 
            CREATE TABLE facture (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                refid TEXT NOT NULL,
                montant_total REAL NOT NULL,
                montant_avance REAL NOT NULL,
                montant_restant REAL NOT NULL,
                montant_tencaisser REAL NOT NULL,
                refagent TEXT NOT NULL,
                refagence TEXT NOT NULL,
                dateref TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print('La table facture a été créée avec succès.')

    conn.commit()
    conn.close()
    


def enregistrer_facture(refid, montant_avance):
    create_facture_table()

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Vérifier si le refid existe déjà dans la table facture
    cursor.execute("""SELECT montant_total, 
                   montant_restant,
                   montant_tencaisser,
                   dateref,
                   refagent,
                   refagence 
                   FROM facture WHERE refid = ? ORDER BY id DESC LIMIT 1""", (refid,))
    existing_facture = cursor.fetchone()
   
   
 


    if existing_facture:
        montant_total = existing_facture[0] 
        montant_restant = existing_facture[1] - montant_avance
        montant_tencaisser = existing_facture[2] + montant_avance
        dateref = existing_facture[3]
        refagent = existing_facture[4]
        refagence = existing_facture[5]
    
    else:
        # Calculer le montant total et le montant restant
        cursor.execute('SELECT SUM(montant) FROM articles WHERE refid = ?', (refid,))
        total_articles = cursor.fetchone()[0]
        montant_total = total_articles
        montant_restant = montant_total - montant_avance
        montant_tencaisser = montant_avance
        dateref = datetime.now()
        refagent = "98815481"
        refagence = "Royal 2"



    if existing_facture and existing_facture[1] == 0:
    # La facture est déjà payée, ne rien faire
      return {
      'message': 'Facture déjà payée',
      'refid': refid,
      'montant_total': montant_total,
      'montant_avance': montant_avance,
       'montant_restant': existing_facture[1],
      'montant_tencaisser': montant_tencaisser,
      'dateref' : dateref,
      'refagent' : refagent,
        'refagence': refagence
     }
    else:
    # Insérer une nouvelle entrée dans la table facture
      cursor.execute("""INSERT INTO facture (refid,
                     montant_total, montant_avance
                     , montant_restant,montant_tencaisser,dateref,refagent,refagence) 
                     VALUES (?, ?, ?, ?,?,?,?,?)""",
                     (refid, montant_total, montant_avance, montant_restant,montant_tencaisser,dateref,refagent,refagence))

      conn.commit()
      conn.close()
      
       # Use a temporary variable to store last inserted ID
    inserted_id = cursor.lastrowid

    # Return success message with the temporary variable
    return {
      'message': 'Facture enregistrée avec succès',
      'id': inserted_id,
      'refid': refid,
      'montant_total': montant_total,
      'montant_avance': montant_avance,
      'montant_restant': montant_restant,
      'montant_tencaisser': montant_tencaisser,
      'dateref' : dateref,
      'refagent' : refagent,
      'refagence': refagence
    }
    
    
    
def fetch_facture_info(id=None, refid=None, dateref=None, refagent=None, refagence=None):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM facture'

    conditions = []
    parameters = []

    if id:
        conditions.append('id=?')
        parameters.append(id)
    if refid:
        conditions.append('refid=?')
        parameters.append(refid)
    if dateref:
        conditions.append('dateref=?')
        parameters.append(dateref)
    if refagent:
        conditions.append('refagent=?')
        parameters.append(refagent)
    if refagence:
        conditions.append('refagence=?')
        parameters.append(refagence)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, parameters)
    facture_info = cursor.fetchall()
    
    facture_list = []
    for row in facture_info:
        facture_dict = {
            'id': row[0],
            'refid': row[1],
            'montant_total': row[2],
            'montant_avance': row[3],
            'montant_restant': row[4],
            'montant_tencaisser': row[5],
            'refagent': row[6],
            'refagence': row[7],
            'date_enregistrement': row[8]
            # Ajoutez d'autres champs selon votre structure de table facture
        }
        facture_list.append(facture_dict)

    conn.close()

    return facture_list
