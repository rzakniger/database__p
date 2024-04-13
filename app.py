from flask import Flask,request,jsonify
from database import add_client, add_article, get_clients, repartir_montant
from article import modifier_articles, get_articles
from facture import enregistrer_facture, fetch_facture_info
from users import app as users_app
from client import clients_bp
from login import login_bp, token_required
from produits import fetch_produits_by_criteria
from agence import agence_bp


app = Flask(__name__)



# Route pour obtenir tous les clients
@app.route('/clients', methods=['GET'])
def fetch_clients():
    identifier = request.args.get('identifier')
    clients = get_clients(identifier)
    return jsonify(clients)

@app.route('/articles', methods=['POST'])
@token_required
def create_article():
    data = request.json
    article = data['article']
    quantite = data['quantite']
    refid = data['refid']  # ID du client
    idtelephone = data['idtelephone']  # Téléphone du client
    daterdv = data['daterdv']

    add_article(article, quantite, refid, idtelephone, daterdv)


    return jsonify({'message': 'Article added successfully'}), 201


    
@app.route('/articles', methods=['GET'])
def fetch_articles():
    identifier = request.args.get('identifier')
    order_by = request.args.get('order_by')
    order = request.args.get('order')
    only_retired = request.args.get('only_retired')
    articles = get_articles(identifier, order_by, order, only_retired)
    return jsonify(articles)

# Route pour modifier les articlesS
@app.route('/articles/modifier', methods=['PUT'])
@token_required
def modifier_articles_route():
    return modifier_articles(request)


# Route pour répartir le montant entre les articles
@app.route('/repartir_montant', methods=['POST'])
@token_required
def route_repartir_montant():
    data = request.json
    refid = data['refid']
    idtelephone = data['idtelephone']
    montant_avance = data['montant_avance']
    result = repartir_montant(refid, idtelephone, montant_avance)
    return jsonify(result)

@app.route('/facturer', methods=['POST'])
@token_required
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

@app.route('/produits', methods=['GET'])
def get_produits():
    # Récupérer les paramètres de la requête
    produit_id = request.args.get('produit_id')
    nom = request.args.get('nom')
    prix = request.args.get('prix')

    # Utiliser la fonction fetch_produits_by_criteria pour obtenir les produits en fonction des critères
    produits = fetch_produits_by_criteria(produit_id=produit_id, nom=nom, prix=prix)

    if produits:
        return jsonify(produits), 200
    else:
        return jsonify({'message': 'Aucun produit trouvé'}), 404

app.register_blueprint(users_app)
app.register_blueprint(login_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(agence_bp)


if __name__ == '__main__':
    init_db()  # Initialise la base de données
    app.run(debug=True)
