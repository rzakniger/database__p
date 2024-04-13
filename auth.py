from flask import request
import jwt
from users import fetch_users_by_criteria
from login import secret_key

def get_current_user():
    token = request.cookies.get('token')
    if token:
        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            userdata = fetch_users_by_criteria(username=data.get('username'))
            
            return userdata
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    return None


def is_authenticated():
    token = request.cookies.get('token')
    if token:
        try:
            # Vérifier si le jeton est valide en le décodant
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            # Vous pouvez également vérifier d'autres informations si nécessaire
            # Par exemple, vous pouvez vérifier si l'utilisateur existe dans la base de données
            # ou si son jeton est toujours valide dans la base de données
            
            # Si tout est en ordre, retournez True pour indiquer que l'utilisateur est authentifié
            return True
        except jwt.ExpiredSignatureError:
            # Si le jeton a expiré, renvoyer False
            return False
        except jwt.InvalidTokenError:
            # Si le jeton est invalide pour une autre raison, renvoyer False
            return False
    # Si aucun jeton n'est trouvé, renvoyer False
    return False
    
def get_user_variables():
    current_user = get_current_user()
    if current_user:
        user_info = current_user[0]
        user_id = user_info['id']
        telephone = user_info['telephone']
        username = user_info['username']
        agence = user_info['agence']
        role = user_info['role']
        privileges = user_info['privileges']
        return user_id, telephone, username, agence, role, privileges
    else:
        return None, None, None, None, None, None

