import sqlite3
import bcrypt

# Connexion à la base SQLite
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash BLOB
)
""")
conn.commit()

# Fonction d'enregistrement
def register_user():
    username = input("Choisis un nom d'utilisateur : ")
    password = input("Choisis un mot de passe : ")

    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print("✅ Utilisateur enregistré avec succès !")
    except sqlite3.IntegrityError:
        print("⚠️ Ce nom d'utilisateur existe déjà.")

# Fonction de connexion
def login_user():
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result:
        stored_hash = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            print("✅ Connexion réussie !")
        else:
            print("❌ Mot de passe incorrect.")
    else:
        print("❌ Utilisateur non trouvé.")

# Menu principal
def menu():
    while True:
        print("\n--- MENU ---")
        print("1. S'enregistrer")
        print("2. Se connecter")
        print("3. Quitter")
        choice = input("Choix : ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            break
        else:
            print("⛔ Choix invalide.")

menu()