import sqlite3
import bcrypt

# Connexion à la base de données
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    password_hash BLOB PRIMARY KEY
)
""")
conn.commit()

# Fonction pour enregistrer un nouvel utilisateur
def register_user():
    print("=== Enregistrement ===")
    password = input("Mot de passe : ")

    # Convertir le mot de passe en bytes et le hacher
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Enregistrement dans la base
    try:
        cursor.execute("INSERT INTO users (password_hash) VALUES (?)", (hashed_password,))
        conn.commit()
        print("Compte enregistré !")
    except sqlite3.IntegrityError:
        print("Ce mot de passe existe déjà.")

# Fonction pour se connecter
def login_user():
    print("=== Connexion ===")
    password = input("Mot de passe : ")

    # Chercher le mot de passe haché dans la base
    cursor.execute("SELECT password_hash FROM users")
    results = cursor.fetchall()

    if results:
        for result in results:
            stored_hash = result[0]
            # Vérifier si le mot de passe correspond
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                print("Connexion réussie !")
                return True
        print("Mot de passe incorrect.")
        return False
    else:
        print("Aucun compte enregistré.")
        return False

# Menu simple pour tester
def menu():
    while True:
        print("\n=== Menu ===")
        print("1. S'enregistrer")
        print("2. Se connecter")
        print("3. Quitter")
        choix = input("Choix : ")

        if choix == "1":
            register_user()
        elif choix == "2":
            if login_user():
                print("Accès autorisé au programme.")
                break  # Tu peux lancer ton programme principal ici
        elif choix == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

# Lancer le menu si le fichier est exécuté
if __name__ == "__main__":
    menu()