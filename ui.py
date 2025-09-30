import tkinter as tk
from logic import testIP

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network manager")

        # Champ 1
        self.label1 = tk.Label(self, text="Adresse IP :")
        self.label1.pack()
        self.entry1 = tk.Entry(self)
        self.entry1.pack()

        # Champ 2
        self.label2 = tk.Label(self, text="Masque de sous-réseau :")
        self.label2.pack()
        self.entry2 = tk.Entry(self)
        self.entry2.pack()


        self.bouton = tk.Button(self, text="Afficher", command=self.display)
        self.bouton.pack(pady=8)

        self.errorMessage = tk.Label(self, text="")
        self.errorMessage.pack()

    def display(self):
        values = [
            self.entry1.get(),
            self.entry2.get(),
        ]
        errorMessage = testIP(values[0], values[1])
        self.errorMessage.config(text=errorMessage, fg="red")