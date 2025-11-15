import customtkinter as ctk
import sqlite3
import bcrypt
from ui import App

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_database()
        self.create_widgets()
        self.setup_layout()
        
    def setup_window(self):
        self.title("Network Manager - Authentification")
        self.geometry("500x450")
        self.resizable(False, False)
        self.configure(fg_color=("#f8fafc", "#1a1a1a"))
        
    def setup_database(self):
        # Connexion à la base de données
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        
        # Création de la table si elle n'existe pas
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            password_hash BLOB PRIMARY KEY
        )
        """)
        self.conn.commit()
        
    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        # Couleurs cohérentes avec l'application principale
        self.primary_color = ("#3b82f6", "#2563eb")
        self.primary_hover = ("#1d4ed8", "#1e40af")
        self.entry_bg = ("#f8fafc", "#2d2d2d")
        self.entry_border = ("#d1d5db", "#4a4a4a")
        self.placeholder_color = ("#9ca3af", "#6b7280")
        
        # Titre principal
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="🔐 Network Manager",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color=("#1e293b", "#f1f5f9")
        )
        
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Authentification requise",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=("#64748b", "#94a3b8")
        )
        
        # Carte de connexion
        self.login_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#ffffff", "#2a2a2a"),
            corner_radius=20,
            border_width=2,
            border_color=("#e2e8f0", "#404040")
        )
        
        self.password_label = ctk.CTkLabel(
            self.login_card,
            text="🔑 Mot de passe",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )
        
        self.password_entry = ctk.CTkEntry(
            self.login_card,
            placeholder_text="Entrez votre mot de passe",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=45,
            corner_radius=12,
            border_width=2,
            fg_color=self.entry_bg,
            border_color=self.entry_border,
            placeholder_text_color=self.placeholder_color,
            show="●"
        )
        
        # Frame pour les boutons
        self.button_frame = ctk.CTkFrame(self.login_card, fg_color="transparent")
        
        self.login_button = ctk.CTkButton(
            self.button_frame,
            text="🔓 Se connecter",
            command=self.login_user,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=45,
            width=180,
            corner_radius=12,
            fg_color=self.primary_color,
            hover_color=self.primary_hover,
            text_color="white"
        )
        
        self.register_button = ctk.CTkButton(
            self.button_frame,
            text="📝 S'enregistrer",
            command=self.register_user,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=45,
            width=180,
            corner_radius=12,
            fg_color=("#f1f5f9", "#374151"),
            hover_color=("#e2e8f0", "#4b5563"),
            text_color=("#374151", "#f1f5f9"),
            border_width=2,
            border_color=("#d1d5db", "#6b7280")
        )
        
        # Message de statut
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#ef4444", "#f87171"),
            wraplength=400
        )
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.login_user())
        self.password_entry.bind("<FocusIn>", lambda e: self.on_focus_in())
        self.password_entry.bind("<FocusOut>", lambda e: self.on_focus_out())
        
    def setup_layout(self):
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        self.title_label.pack(pady=(20, 5))
        self.subtitle_label.pack(pady=(0, 30))
        
        self.login_card.pack(fill="x", pady=(0, 20))
        self.password_label.pack(anchor="w", padx=25, pady=(25, 8))
        self.password_entry.pack(fill="x", padx=25, pady=(0, 20))
        
        self.button_frame.pack(pady=(0, 25))
        self.login_button.pack(side="left", padx=(0, 10))
        self.register_button.pack(side="left")
        
        self.status_label.pack(pady=(0, 20))
        
        # Focus sur le champ de mot de passe
        self.password_entry.focus()
        
    def on_focus_in(self):
        self.password_entry.configure(border_color=("#3b82f6", "#60a5fa"))
        
    def on_focus_out(self):
        self.password_entry.configure(border_color=("#d1d5db", "#4a4a4a"))
        
    def show_status(self, message, is_error=True):
        color = ("#ef4444", "#f87171") if is_error else ("#10b981", "#34d399")
        self.status_label.configure(text=message, text_color=color)
        
    def animate_button_press(self, button):
        button.configure(state="disabled")
        self.after(100, lambda: button.configure(state="normal"))
        
    def register_user(self):
        self.animate_button_press(self.register_button)
        password = self.password_entry.get().strip()
        
        if not password:
            self.show_status("❌ Veuillez entrer un mot de passe", is_error=True)
            return
        
        # Convertir le mot de passe en bytes et le hacher
        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        # Enregistrement dans la base
        try:
            self.cursor.execute("INSERT INTO users (password_hash) VALUES (?)", (hashed_password,))
            self.conn.commit()
            self.show_status("✅ Compte enregistré avec succès !", is_error=False)
            self.password_entry.delete(0, "end")
        except sqlite3.IntegrityError:
            self.show_status("❌ Ce mot de passe existe déjà", is_error=True)
        
    def login_user(self):
        self.animate_button_press(self.login_button)
        password = self.password_entry.get().strip()
        
        if not password:
            self.show_status("❌ Veuillez entrer un mot de passe", is_error=True)
            return
        
        # Chercher le mot de passe haché dans la base
        self.cursor.execute("SELECT password_hash FROM users")
        results = self.cursor.fetchall()
        
        if not results:
            self.show_status("❌ Aucun compte enregistré. Veuillez vous enregistrer d'abord.", is_error=True)
            return
        
        # Vérifier si le mot de passe correspond
        for result in results:
            stored_hash = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                self.show_status("✅ Connexion réussie ! Lancement de l'application...", is_error=False)
                self.after(1000, self.launch_main_app)
                return
        
        self.show_status("❌ Mot de passe incorrect", is_error=True)
        
    def launch_main_app(self):
        # Fermer la connexion à la base de données
        self.conn.close()
        
        # Fermer la fenêtre de connexion
        self.destroy()
        
        # Lancer l'application principale
        app = App()
        app.mainloop()
        
    def on_closing(self):
        # Fermer proprement la connexion à la base de données
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    login_app = LoginApp()
    login_app.protocol("WM_DELETE_WINDOW", login_app.on_closing)
    login_app.mainloop()
