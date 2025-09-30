errorMessages = {
    # Messages d'erreur généraux
    "empty_input": "Les champs ne peuvent pas être vides.",
    
    # Messages d'erreur pour l'adresse IP
    "empty_ip": "L'adresse IP ne peut pas être vide.",
    "invalid_ip_format": "Format d'adresse IP invalide. Utilisez le format xxx.xxx.xxx.xxx",
    "invalid_ip_octets": "Une adresse IP doit contenir exactement 4 octets séparés par des points.",
    "invalid_octet_range": "Chaque octet doit être un nombre entre 0 et 255.",
    "invalid_octet_number": "Chaque octet doit être un nombre entier valide.",
    "leading_zeros": "Les octets ne peuvent pas commencer par des zéros (sauf pour 0).",
    "private_ip_class_a": "Adresse IP privée de classe A détectée (10.0.0.0/8).",
    "private_ip_class_b": "Adresse IP privée de classe B détectée (172.16.0.0/12).",
    "private_ip_class_c": "Adresse IP privée de classe C détectée (192.168.0.0/16).",
    "loopback_ip": "Adresse IP de bouclage détectée (127.0.0.0/8).",
    "broadcast_ip": "Adresse IP de diffusion invalide (255.255.255.255).",
    "network_ip": "Cette adresse correspond à l'adresse réseau.",
    "broadcast_ip_network": "Cette adresse correspond à l'adresse de diffusion du réseau.",
    
    # Messages d'erreur pour le masque de sous-réseau
    "empty_subnet": "Le masque de sous-réseau ne peut pas être vide.",
    "invalid_subnet_format": "Format de masque de sous-réseau invalide. Utilisez le format xxx.xxx.xxx.xxx ou /xx",
    "invalid_subnet_octets": "Un masque de sous-réseau doit contenir exactement 4 octets séparés par des points.",
    "invalid_subnet_range": "Chaque octet du masque doit être un nombre entre 0 et 255.",
    "invalid_subnet_number": "Chaque octet du masque doit être un nombre entier valide.",
    "invalid_subnet_pattern": "Le masque de sous-réseau doit être composé de bits consécutifs à 1 suivis de bits à 0.",
    "invalid_cidr_range": "La notation CIDR doit être entre /0 et /32.",
    "invalid_cidr_format": "Format CIDR invalide. Utilisez /xx où xx est un nombre entre 0 et 32.",
    "subnet_all_zeros": "Le masque de sous-réseau ne peut pas être 0.0.0.0.",
    "subnet_all_ones": "Le masque de sous-réseau ne peut pas être 255.255.255.255.",
    
    # Messages d'erreur de compatibilité IP/Masque
    "ip_subnet_mismatch": "L'adresse IP et le masque de sous-réseau ne sont pas compatibles.",
    "invalid_host_portion": "La partie hôte de l'adresse IP contient des bits non valides pour ce masque.",
    
    # Messages d'information
    "valid_ip_subnet": "Adresse IP et masque de sous-réseau valides.",
    "class_a_detected": "Adresse IP de classe A détectée.",
    "class_b_detected": "Adresse IP de classe B détectée.", 
    "class_c_detected": "Adresse IP de classe C détectée.",
    "class_d_detected": "Adresse IP de classe D (multicast) détectée.",
    "class_e_detected": "Adresse IP de classe E (expérimentale) détectée.",
}

def To_binary(octet):    
    binary = ''
    for i in range(7, -1, -1):
        if octet >= 2**i:
            binary += '1'
            octet -= 2**i
        else:
            binary += '0'
    return binary