import sqlite3
from datetime import datetime

def update_last_seen(user_id):
    try:
        # Se connecter à la base de données
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        # Mettre à jour le champ lastseen de l'utilisateur avec l'ID spécifié
        cursor.execute('UPDATE users SET lastseen = ? WHERE id = ?', (datetime.now(), user_id))

        # Valider la transaction et fermer la connexion à la base de données
        conn.commit()
        conn.close()

        return "Champ lastseen mis à jour avec succès."

    except Exception as e:
        return f"Erreur lors de la mise à jour du champ lastseen : {e}"

