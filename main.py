import tkinter as tk

def afficher_texte():
    texte = entry.get()
    label_resultat.config(text=texte)

root = tk.Tk()
root.title("Afficheur de texte")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

btn = tk.Button(root, text="Afficher", command=afficher_texte)
btn.pack(pady=5)

label_resultat = tk.Label(root, text="")
label_resultat.pack(pady=10)

root.mainloop()