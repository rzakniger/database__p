from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Fonction pour initialiser la base de données SQLite
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Vérifier si la base de données existe, sinon l'initialiser
init_db()

# Fonction pour ajouter un utilisateur à la base de données
def add_user(name, email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

# Fonction pour récupérer tous les utilisateurs de la base de données
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# Route pour afficher le formulaire d'ajout d'utilisateur et la liste des utilisateurs
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        add_user(name, email)
    users = get_users()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
