import customtkinter as ctk
from logic import (
    testIP,
    detect_ip_class,
    cidr_to_subnet_mask,
    get_network_address,
    get_broadcast_address,
    ip_in_network,
    get_ip_range,
    parse_membership_inputs
)
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
        self.geometry("750x850")
        
        self.configure(fg_color=("#f8fafc", "#1a1a1a"))
        
    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.primary_color = ("#3b82f6", "#2563eb")
        self.primary_hover = ("#1d4ed8", "#1e40af")
        self.entry_bg = ("#f8fafc", "#2d2d2d")
        self.entry_border = ("#d1d5db", "#4a4a4a")
        self.placeholder_color = ("#9ca3af", "#6b7280")
        self.entry_h = 45
        self.entry_radius = 12
        
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Network Managers",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=("#1e293b", "#f1f5f9")
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

        self.tabview = ctk.CTkTabview(self.input_card, width=580, height=220)
        self.tabview.add("Calcul réseau")
        self.tabview.add("Vérification d'appartenance")

        ip_tab = self.tabview.tab("Calcul réseau")
        params_tab = self.tabview.tab("Vérification d'appartenance")

        try:
            ip_tab.configure(fg_color=self.entry_bg)
            params_tab.configure(fg_color=self.entry_bg)
        except Exception:
            pass

        self.ip_label = ctk.CTkLabel(
            ip_tab,
            text="🌍 Adresse IP",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )

        self.ip_entry = ctk.CTkEntry(
            ip_tab,
            placeholder_text="Exemple: 192.168.1.1 (ou 192.168.1.0/24 en mode Classless)",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=self.entry_h,
            corner_radius=self.entry_radius,
            border_width=2,
            fg_color=self.entry_bg,
            border_color=self.entry_border,
            placeholder_text_color=self.placeholder_color
        )

        self.classful_label = ctk.CTkLabel(
            ip_tab,
            text="Classless",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )

        self.classful_entry = ctk.CTkSwitch(
            ip_tab,
            text="",
            command=self.classless_toggle,
            onvalue="on",
            offvalue="off"
        )

        self.subnet_label = ctk.CTkLabel(
            ip_tab,
            text="🔒 Masque de sous-réseau",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )

        self.subnet_entry = ctk.CTkEntry(
            ip_tab,
            placeholder_text="Exemple: 255.255.255.0",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=self.entry_h,
            corner_radius=self.entry_radius,
            border_width=2,
            fg_color=self.entry_bg,
            border_color=self.entry_border,
            placeholder_text_color=self.placeholder_color
        )

        self.membership_ip_label = ctk.CTkLabel(
            params_tab,
            text="📌 IP à vérifier",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )

        self.membership_ip_entry = ctk.CTkEntry(
            params_tab,
            placeholder_text="Ex: 192.168.1.10",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=self.entry_h,
            corner_radius=self.entry_radius,
            border_width=2,
            fg_color=self.entry_bg,
            border_color=self.entry_border,
            placeholder_text_color=self.placeholder_color
        )

        self.membership_network_label = ctk.CTkLabel(
            params_tab,
            text="🌐 Adresse réseau",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )

        self.membership_network_entry = ctk.CTkEntry(
            params_tab,
            placeholder_text="Ex: 192.168.1.0",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=self.entry_h,
            corner_radius=self.entry_radius,
            border_width=2,
            fg_color=self.entry_bg,
            border_color=self.entry_border,
            placeholder_text_color=self.placeholder_color
        )

        self.membership_mask_label = ctk.CTkLabel(
            params_tab,
            text="🔒 Masque de sous-réseau",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=("#374151", "#d1d5db"),
            anchor="w"
        )

        self.membership_mask_entry = ctk.CTkEntry(
            params_tab,
            placeholder_text="Ex: 255.255.255.0",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=self.entry_h,
            corner_radius=self.entry_radius,
            border_width=2,
            fg_color=self.entry_bg,
            border_color=self.entry_border,
            placeholder_text_color=self.placeholder_color
        )
        
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        self.validate_button = ctk.CTkButton(
            self.button_frame,
            text="🔍 Valider",
            command=self.validate_action,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            height=45,
            width=140,
            corner_radius=12,
            fg_color=self.primary_color,
            hover_color=self.primary_hover,
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
        
        self.membership_ip_entry.bind("<KeyRelease>", self.on_entry_change)
        self.membership_network_entry.bind("<KeyRelease>", self.on_entry_change)
        self.membership_mask_entry.bind("<KeyRelease>", self.on_entry_change)
        self.membership_ip_entry.bind("<FocusIn>", lambda e: self.on_focus_in(self.membership_ip_entry))
        self.membership_network_entry.bind("<FocusIn>", lambda e: self.on_focus_in(self.membership_network_entry))
        self.membership_mask_entry.bind("<FocusIn>", lambda e: self.on_focus_in(self.membership_mask_entry))
        self.membership_ip_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.membership_ip_entry))
        self.membership_network_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.membership_network_entry))
        self.membership_mask_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.membership_mask_entry))
        
    def setup_layout(self):
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        self.title_label.pack(pady=(0, 5))
        
        self.input_card.pack(fill="x", pady=(0, 20))
        self.input_title.pack(pady=(20, 12))
        self.tabview.pack(fill="x", padx=20, pady=(0, 10))

        self.ip_label.pack(anchor="w", padx=12, pady=(8, 5))
        self.ip_entry.pack(fill="x", padx=12, pady=(0, 10))
        self.classful_label.pack(anchor="w", padx=12, pady=(0, 0))
        self.classful_entry.pack(anchor="w", padx=12, pady=(0, 10))
        self.subnet_label.pack(anchor="w", padx=12, pady=(0, 5))
        self.subnet_entry.pack(fill="x", padx=12, pady=(0, 12))

        self.membership_ip_label.pack(anchor="w", padx=12, pady=(6, 4))
        self.membership_ip_entry.pack(fill="x", padx=12, pady=(0, 8))
        self.membership_network_label.pack(anchor="w", padx=12, pady=(0, 4))
        self.membership_network_entry.pack(fill="x", padx=12, pady=(0, 8))
        self.membership_mask_label.pack(anchor="w", padx=12, pady=(0, 4))
        self.membership_mask_entry.pack(fill="x", padx=12, pady=(0, 10))
        
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
        
    def on_focus_in(self, entry):
        entry.configure(border_color=("#3b82f6", "#60a5fa"))
        
    def on_focus_out(self, entry):
        entry.configure(border_color=("#d1d5db", "#4a4a4a"))
        
    def on_entry_change(self, event=None):
        if self.error_label.cget('text'):
            self.clear_results()
            
    def animate_progress(self, start=0, end=1, duration=400, callback=None):
        # Animation fluide de la barre de progression pendant les validations
        # Découpe l'animation en 30 étapes pour un effet visuel smooth
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
        self.membership_ip_entry.delete(0, "end")
        self.membership_network_entry.delete(0, "end")
        self.membership_mask_entry.delete(0, "end")
        
        self.clear_results()
        self.ip_entry.focus()
        self.animate_button_press(self.clear_button)
        
    def animate_button_press(self, button):
        button.configure(state="disabled")
        self.after(100, lambda: button.configure(state="normal"))
        
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
        
        # Stocke les valeurs pour affichage après validation asynchrone
        self.validation_result = None
        self.validation_ip = ip
        self.validation_subnet = subnet
        
        # Exécute la validation dans un thread séparé pour ne pas bloquer l'interface
        def validate_in_background():
            result = testIP(ip, subnet, self.isClassful)
            self.validation_result = result
            
        thread = threading.Thread(target=validate_in_background)
        thread.daemon = True
        thread.start()
        
        self.animate_progress(callback=self.show_final_results)
        
    def show_final_results(self):
        self.results_card.pack(fill="x", pady=(0, 20))
        
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
            
            # En mode Classful, extrait le préfixe CIDR et convertit en masque pointé
            if self.isClassful and '/' in ip:
                parts = ip.split('/')
                clean_ip = parts[0]
                cidr_prefix = int(parts[1])
                subnet_mask = cidr_to_subnet_mask(cidr_prefix)
            
            if not subnet_mask:
                self.error_label.configure(text="❌ Masque de sous-réseau invalide")
                return
            
            ip_parts = [int(x) for x in clean_ip.split('.')]
            subnet_parts = [int(x) for x in subnet_mask.split('.')]
            
            # Calcul de l'adresse réseau: ET binaire entre IP et masque (octet par octet)
            network_parts = [ip_parts[i] & subnet_parts[i] for i in range(4)]
            network_addr = '.'.join(map(str, network_parts))
            
            # Calcul du broadcast: OU binaire entre IP et inverse du masque
            broadcast_parts = [ip_parts[i] | (255 - subnet_parts[i]) for i in range(4)]
            broadcast_addr = '.'.join(map(str, broadcast_parts))
            
            # Compte les bits hôte (bits à 0 dans le masque) pour calculer le nombre d'hôtes
            # -2 car on exclut l'adresse réseau et le broadcast
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
            self.ip_entry.configure(placeholder_text="Exemple: 192.168.1.1")
                
        self.subnet_entry.configure(
            state="normal" if not self.isClassful else "disabled",
            fg_color=("#f8fafc", "#2d2d2d") if not self.isClassful else ("#a6a6a6", "#1a1a1a"),
            border_color=("#d1d5db", "#4a4a4a") if not self.isClassful else ("#5e6063", "#323232"),
            placeholder_text_color=("#9ca3af", "#6b7280") if not self.isClassful else ("#54585e", "#363a42"),
            text_color=("#374151", "#d1d5db") if not self.isClassful else ("#7f7f7f", "#5a5a5a"),
        )
        self.clear_results()

    def check_membership(self):
        ip = self.membership_ip_entry.get().strip() or self.ip_entry.get().strip()
        network = self.membership_network_entry.get().strip()
        mask = self.membership_mask_entry.get().strip()

        self.results_card.pack(fill="x", pady=(0, 20))
        self.clear_results()

        ip_clean, network_clean, mask_dotted, err = parse_membership_inputs(ip, network, mask)
        if err:
            self.error_label.configure(text=f"❌ {err}")
            self.animate_result_appearance()
            return

        try:
            if not network_clean and ip_clean and mask_dotted:
                network_clean = get_network_address(ip_clean, mask_dotted)

            belongs = False
            if ip_clean and network_clean and mask_dotted:
                belongs = ip_in_network(ip_clean, network_clean, mask_dotted)

            if belongs:
                self.success_label.configure(text=f"✅ {ip_clean} appartient au réseau {network_clean}")
            else:
                self.error_label.configure(text=f"❌ {ip_clean} n'appartient pas au réseau {network_clean}")

            if ip_clean and mask_dotted:
                net_addr = get_network_address(ip_clean, mask_dotted)
                bcast = get_broadcast_address(ip_clean, mask_dotted)
                start, end = get_ip_range(net_addr, mask_dotted)

                self.network_label.configure(text=f"🌐 Adresse réseau: {net_addr}")
                self.broadcast_label.configure(text=f"📡 Broadcast: {bcast}")
                self.hosts_label.configure(text=f"👥 Plage hôtes: {start} - {end}")

            self.animate_result_appearance()

        except Exception as e:
            self.error_label.configure(text=f"❌ Erreur: {e}")
            self.animate_result_appearance()

    def validate_action(self):
        # Dispatche la validation vers la fonction appropriée selon l'onglet actif
        self.animate_button_press(self.validate_button)
        current = self.tabview.get()
        
        if current == "Vérification d'appartenance":
            self.results_card.pack_forget()
            self.animate_progress(callback=self.check_membership)
        else:
            self.display()
