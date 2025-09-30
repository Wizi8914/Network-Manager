import bcrypt

# Étape 1 : Création du mot de passe
print("🔐 Création du mot de passe")
new_password = input("Tape ton nouveau mot de passe : ").encode('utf-8')
hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())

print("\n✅ Mot de passe enregistré !\n")

# Étape 2 : Vérification du mot de passe
print("🔍 Vérification du mot de passe")
test_password = input("Tape ton mot de passe pour vérifier : ").encode('utf-8')

if bcrypt.checkpw(test_password, hashed_password):
    print("✅ Mot de passe correct !")
else:
    print("❌ Mot de passe incorrect.")