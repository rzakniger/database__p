from flask import Flask, request, jsonify
from database import init_db, add_client, add_article, get_clients, repartir_montant
from article import modifier_articles,get_articles
from facture import enregistrer_facture,fetch_facture_info

app = Flask(__name__)

# Route pour ajouter un client
@app.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    nom = data['nom']
    telephone = data['telephone']
    adresse = data['adresse']
    codepromo = data['codepromo']
    client_id = add_client(nom, telephone, adresse, codepromo)
    return jsonify({'message': 'Client added successfully', 'client_id': client_id}), 201

# Route pour obtenir tous les clients
@app.route('/clients', methods=['GET'])
def fetch_clients():
    identifier = request.args.get('identifier')
    clients = get_clients(identifier)
    return jsonify(clients)

# Route pour ajouter un article
@app.route('/articles', methods=['POST'])
def create_article():
    data = request.json
    article = data['article']
    quantite = data['quantite']
    refid = data['refid']  # ID du client
    idtelephone = data['idtelephone']  # Téléphone du client
    montant = data['montant']
    mtotal = data['mtotal']
    daterdv = data['daterdv']
    add_article(article, quantite, refid, idtelephone, montant, mtotal, daterdv)

    return jsonify({'message': 'Article added successfully'}), 201

@app.route('/articles', methods=['GET'])
def fetch_articles():
    identifier = request.args.get('identifier')
    order_by = request.args.get('order_by')
    order = request.args.get('order')
    only_retired = request.args.get('only_retired')
    articles = get_articles(identifier, order_by, order, only_retired)
    return jsonify(articles)

# Route pour modifier les articles
@app.route('/articles/modifier', methods=['PUT'])
def modifier_articles_route():
    return modifier_articles(request)


# Route pour répartir le montant entre les articles
@app.route('/repartir_montant', methods=['POST'])
def route_repartir_montant():
    data = request.json
    refid = data['refid']
    idtelephone = data['idtelephone']
    montant_avance = data['montant_avance']
    result = repartir_montant(refid, idtelephone, montant_avance)
    return jsonify(result)


@app.route('/facturer', methods=['POST'])
def facturer():
    # Récupérer les données du corps de la requête
    data = request.json
    refid = data.get('refid')
    reftelephone = data.get('reftelephone')
    montant_avance = data.get('montant_avance')
    result = enregistrer_facture(refid, montant_avance)
    return jsonify({'message': result})


@app.route('/facture/info', methods=['GET'])
def get_facture_info():
    id = request.args.get('id')
    refid = request.args.get('refid')
    dateref = request.args.get('dateref')
    refagent = request.args.get('refagent')
    refagence = request.args.get('refagence')
    
    facture_info = fetch_facture_info(id, refid, dateref, refagent, refagence)
    
    return jsonify(facture_info)

if __name__ == '__main__':
    init_db()  # Initialise la base de données
    app.run(debug=True)
