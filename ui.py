import customtkinter as ctk
from logic import testIP, detect_ip_class, cidr_to_subnet_mask, extract_ip_from_cidr
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    isClassful = False
    
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_widgets()
        self.setup_layout()
        
    def setup_window(self):
        self.title("Network Manager")
        self.geometry("750x1000")
        
        self.configure(fg_color=("#f8fafc", "#1a1a1a"))
        
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Network Managers",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=("#1e293b", "#f1f5f9")
        )
        
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Validation d'adresses IP et masques de sous-réseau",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=("#64748b", "#94a3b8")
        )
        
        self.input_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#ffffff", "#2a2a2a"),
            corner_radius=20,
            border_width=2,
            border_color=("#e2e8f0", "#404040")
        )
        
        self.input_title = ctk.CTkLabel(
            self.input_card,
            text="📝 Saisie des données",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=("#1e293b", "#f1f5f9")
        )
        
        self.ip_label = ctk.CTkLabel(
            self.input_card,
            text="🌍 Adresse IP",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )
        
        self.ip_entry = ctk.CTkEntry(
            self.input_card,
            placeholder_text="Exemple: 192.168.1.1 (ou 192.168.1.0/24 en mode Classless)",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=45,
            corner_radius=12,
            border_width=2,
            fg_color=("#f8fafc", "#2d2d2d"),
            border_color=("#d1d5db", "#4a4a4a"),
            placeholder_text_color=("#9ca3af", "#6b7280")
        )
        
        self.classful_label = ctk.CTkLabel(
            self.input_card,
            text="Classless",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )

        self.classful_entry = ctk.CTkSwitch(
            self.input_card, 
            text="",
            command=self.classless_toggle,
            onvalue="on",
            offvalue="off"
        )

        self.subnet_label = ctk.CTkLabel(
            self.input_card,
            text="🔒 Masque de sous-réseau",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )
        
        self.subnet_entry = ctk.CTkEntry(
            self.input_card,
            placeholder_text="Exemple: 255.255.255.0",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=45,
            corner_radius=12,
            border_width=2,
            fg_color=("#f8fafc", "#2d2d2d"),
            border_color=("#d1d5db", "#4a4a4a"),
            placeholder_text_color=("#9ca3af", "#6b7280")
        )
        
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        self.validate_button = ctk.CTkButton(
            self.button_frame,
            text="🔍 Valider",
            command=self.display,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=45,
            width=140,
            corner_radius=12,
            fg_color=("#3b82f6", "#2563eb"),
            hover_color=("#1d4ed8", "#1e40af"),
            text_color="white"
        )
        
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="🗑️ Effacer",
            command=self.clear_fields,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=45,
            width=140,
            corner_radius=12,
            fg_color=("#f1f5f9", "#374151"),
            hover_color=("#e2e8f0", "#4b5563"),
            text_color=("#374151", "#f1f5f9"),
            border_width=2,
            border_color=("#d1d5db", "#6b7280")
        )
        
        self.results_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#ffffff", "#2a2a2a"),
            corner_radius=20,
            border_width=2,
            border_color=("#e2e8f0", "#404040")
        )
        
        self.results_title = ctk.CTkLabel(
            self.results_card,
            text="📊 Résultats",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=("#1e293b", "#f1f5f9")
        )
        
        self.success_label = ctk.CTkLabel(
            self.results_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=("#10b981", "#34d399"),
            anchor="w"
        )
        
        self.class_label = ctk.CTkLabel(
            self.results_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#3b82f6", "#60a5fa"),
            anchor="w"
        )
        
        self.error_label = ctk.CTkLabel(
            self.results_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#ef4444", "#f87171"),
            anchor="w",
            wraplength=500
        )
        
        self.network_label = ctk.CTkLabel(
            self.results_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#3b82f6", "#60a5fa"),
            anchor="w"
        )
        
        self.broadcast_label = ctk.CTkLabel(
            self.results_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#3b82f6", "#60a5fa"),
            anchor="w"
        )
        
        self.hosts_label = ctk.CTkLabel(
            self.results_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#10b981", "#34d399"),
            anchor="w"
        )
        
        self.info_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=("#f8fafc", "#2a2a2a"),
            corner_radius=20,
            border_width=2,
            border_color=("#e2e8f0", "#404040")
        )
        
        self.info_title = ctk.CTkLabel(
            self.info_card,
            text="ℹ️ Guide d'utilisation",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=("#1e293b", "#f1f5f9")
        )
        
        self.info_text = ctk.CTkLabel(
            self.info_card,
            text="• Mode Classful: Format IP xxx.xxx.xxx.xxx + masque séparé\n"
                 "• Mode Classless: Format CIDR xxx.xxx.xxx.xxx/préfixe (ex: 192.168.1.0/24)\n"
                 "• Le préfixe CIDR doit être entre 0 et 32\n"
                 "• Le masque doit avoir des bits consécutifs (pas de trous)\n"
                 "• Les adresses privées et spéciales sont détectées automatiquement",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("#64748b", "#94a3b8"),
            anchor="w",
            justify="left"
        )
        
        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame,
            height=4,
            corner_radius=2,
            fg_color=("#e2e8f0", "#404040"),
            progress_color=("#3b82f6", "#60a5fa")
        )
        self.progress_bar.set(0)
        
        self.ip_entry.bind("<KeyRelease>", self.on_entry_change)
        self.subnet_entry.bind("<KeyRelease>", self.on_entry_change)
        self.ip_entry.bind("<FocusIn>", lambda e: self.on_focus_in(self.ip_entry))
        self.subnet_entry.bind("<FocusIn>", lambda e: self.on_focus_in(self.subnet_entry))
        self.ip_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.ip_entry))
        self.subnet_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.subnet_entry))
        
    def setup_layout(self):
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.title_label.pack(pady=(0, 5))
        self.subtitle_label.pack(pady=(0, 15))
        
        self.input_card.pack(fill="x", pady=(0, 20))
        self.input_title.pack(pady=(20, 20))
        
        self.ip_label.pack(anchor="w", padx=25, pady=(0, 5))
        self.ip_entry.pack(fill="x", padx=25, pady=(0, 20))
        
        self.classful_label.pack(anchor="w", padx=25, pady=(0, 0))
        self.classful_entry.pack(anchor="w", padx=25, pady=(0, 20))
        
        self.subnet_label.pack(anchor="w", padx=25, pady=(0, 8))
        self.subnet_entry.pack(fill="x", padx=25, pady=(0, 25))
        
        self.button_frame.pack(pady=5)
        self.validate_button.pack(side="left", padx=(0, 15))
        self.clear_button.pack(side="left")
        
        self.progress_bar.pack(fill="x", pady=(10, 20))
        
        self.results_card.pack(fill="x", pady=(0, 20))
        self.results_title.pack(pady=(20, 15))
        self.success_label.pack(anchor="w", padx=25, pady=(0, 5))
        self.class_label.pack(anchor="w", padx=25, pady=(0, 5))
        self.network_label.pack(anchor="w", padx=25, pady=(0, 5))
        self.broadcast_label.pack(anchor="w", padx=25, pady=(0, 5))
        self.hosts_label.pack(anchor="w", padx=25, pady=(0, 5))
        self.error_label.pack(anchor="w", padx=25, pady=(0, 20))
        
        self.info_card.pack(fill="x")
        self.info_title.pack(pady=(15, 15))
        self.info_text.pack(anchor="w", padx=25, pady=(0, 20))
        
    def on_focus_in(self, entry):
        entry.configure(border_color=("#3b82f6", "#60a5fa"))
        
    def on_focus_out(self, entry):
        entry.configure(border_color=("#d1d5db", "#4a4a4a"))
        
    def on_entry_change(self, event=None):
        if self.error_label.cget('text'):
            self.clear_results()
            
    def animate_progress(self, start=0, end=1, duration=400, callback=None):
        steps = 30
        step_value = (end - start) / steps
        step_time = duration // steps
        
        def update_progress(current_step):
            if current_step <= steps:
                progress = start + (step_value * current_step)
                self.progress_bar.set(progress)
                self.after(step_time, lambda: update_progress(current_step + 1))
            else:
                self.after(200, lambda: self.progress_bar.set(0))
                if callback:
                    self.after(300, callback)
                
        update_progress(0)
        
    def clear_fields(self):
        self.ip_entry.delete(0, "end")
        self.subnet_entry.delete(0, "end")
        self.clear_results()
        self.ip_entry.focus()
        
        self.animate_button_press(self.clear_button)
        
    def animate_button_press(self, button):
        original_fg = button.cget('fg_color')
        button.configure(fg_color=("#e2e8f0", "#4b5563"))
        self.after(100, lambda: button.configure(fg_color=original_fg))
        
    def animate_result_appearance(self):
        original_border = self.results_card.cget('border_color')
        highlight_color = ("#3b82f6", "#60a5fa")
        
        self.results_card.configure(border_color=highlight_color)
        self.after(300, lambda: self.results_card.configure(border_color=original_border))
        
    def clear_results(self):
        self.success_label.configure(text="")
        self.class_label.configure(text="")
        self.network_label.configure(text="")
        self.broadcast_label.configure(text="")
        self.hosts_label.configure(text="")
        self.error_label.configure(text="")
        
        self.validation_result = None
        
    def display(self):
        ip = self.ip_entry.get().strip()
        subnet = self.subnet_entry.get().strip()
        
        self.animate_button_press(self.validate_button)
        
        self.clear_results()
        
        self.results_card.pack_forget()
        
        self.validation_result = None
        self.validation_ip = ip
        self.validation_subnet = subnet
        
        def validate_in_background():
            result = testIP(ip, subnet, self.isClassful)
            self.validation_result = result
            
        thread = threading.Thread(target=validate_in_background)
        thread.daemon = True
        thread.start()
        
        self.animate_progress(callback=self.show_final_results)
        
    def show_final_results(self):
        self.results_card.pack(fill="x", pady=(0, 20), before=self.info_card)
        
        if self.validation_result is not None:
            self.update_results(self.validation_result, self.validation_ip, self.validation_subnet)
        else:
            self.after(50, self.show_final_results)
        
    def update_results(self, result, ip, subnet):
        if result == 0:
            self.success_label.configure(text="✅ Configuration réseau valide")
            
            ip_class = detect_ip_class(ip)
            if ip_class:
                self.class_label.configure(text=f"📋 {ip_class}")
                
            self.show_network_info(ip, subnet)
            
        else:
            self.error_label.configure(text=f"❌ {result}")
            
        self.animate_result_appearance()
            
    def show_network_info(self, ip, subnet):
        try:
            clean_ip = ip
            subnet_mask = subnet
            cidr_prefix = None
            
            if self.isClassful and '/' in ip:
                parts = ip.split('/')
                clean_ip = parts[0]
                cidr_prefix = int(parts[1])
                subnet_mask = cidr_to_subnet_mask(cidr_prefix)
            
            ip_parts = [int(x) for x in clean_ip.split('.')]
            subnet_parts = [int(x) for x in subnet_mask.split('.')]
            
            network_parts = [ip_parts[i] & subnet_parts[i] for i in range(4)]
            network_addr = '.'.join(map(str, network_parts))
            
            broadcast_parts = [ip_parts[i] | (255 - subnet_parts[i]) for i in range(4)]
            broadcast_addr = '.'.join(map(str, broadcast_parts))
            
            host_bits = sum(bin(255 - octet).count('1') for octet in subnet_parts)
            num_hosts = (2 ** host_bits) - 2 if host_bits > 1 else 0
            
            if cidr_prefix is not None:
                self.network_label.configure(text=f"🌐 Adresse réseau: {network_addr}/{cidr_prefix}")
                self.broadcast_label.configure(text=f"📡 Adresse broadcast: {broadcast_addr}")
                self.hosts_label.configure(text=f"👥 Hôtes disponibles: {num_hosts} (Masque: {subnet_mask})")
            else:
                self.network_label.configure(text=f"🌐 Adresse réseau: {network_addr}")
                self.broadcast_label.configure(text=f"📡 Adresse broadcast: {broadcast_addr}")
                self.hosts_label.configure(text=f"👥 Hôtes disponibles: {num_hosts}")
            
        except Exception as e:
            self.network_label.configure(text="❌ Erreur de calcul réseau")
            self.broadcast_label.configure(text="")
            self.hosts_label.configure(text="")
            
            
    def classless_toggle(self):
        self.isClassful = not self.isClassful
        
        if self.isClassful:
            self.ip_entry.configure(placeholder_text="Exemple: 192.168.1.0/24 (notation CIDR requise)")
        else:
            self.ip_entry.configure(placeholder_text="Exemple: 192.168.1.1 (sans notation CIDR)")
                
        self.subnet_entry.configure(
            state="normal" if not self.isClassful else "disabled",
            fg_color=("#f8fafc", "#2d2d2d") if not self.isClassful else ("#a6a6a6", "#1a1a1a"),
            border_color=("#d1d5db", "#4a4a4a") if not self.isClassful else ("#5e6063", "#323232"),
            placeholder_text_color=("#9ca3af", "#6b7280") if not self.isClassful else ("#54585e", "#363a42"),
            text_color=("#374151", "#d1d5db") if not self.isClassful else ("#7f7f7f", "#5a5a5a"),
        )
        self.clear_results()
