import sqlite3
from datetime import datetime
from flask import jsonify
from produits import fetch_produits_by_criteria

def modifier_articles(request):
    data = request.json
    refid = data.get('refid')
    id = data.get('id')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    if refid:
        cursor.execute('UPDATE articles SET retirer=?, datemiseajour=? WHERE refid=?', (True, datetime.now(), refid))
    elif id:
        cursor.execute('UPDATE articles SET retirer=?, datemiseajour=? WHERE id=?', (True, datetime.now(), id))
    else:
        return jsonify({'error': 'Vous devez fournir soit refid soit id'}), 400

    conn.commit()
    conn.close()

    return jsonify({'message': 'Articles modifiés avec succès'}), 200




def get_articles(identifier=None, order_by=None, order=None, only_retired=None):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM articles'

    conditions = []
    parameters = []

    if identifier:
        conditions.append('(id=? OR refid=? OR idtelephone=?)')
        parameters.extend([identifier, identifier, identifier])
    if only_retired is not None:
        conditions.append('retirer=?')
        parameters.append(only_retired)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    if order_by:
        query += f' ORDER BY {order_by}'
        if order and order.lower() in ['asc', 'desc']:
            query += f' {order}'

 

    cursor.execute(query, parameters)
    articles = [
       {         
            'id': row[0],
            'article': row[1],
            'quantite': row[2],
            'refid': row[3],
            'idtelephone': row[4],
            'montant': row[5],
            'mtotal': row[6],
            'refagent': row[7],
            'refagence': row[8],
            'datedepot': row[9],
            'daterdv': row[10],
            'datemiseajour': row[11],
            'retirer': row[12]
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return articles
