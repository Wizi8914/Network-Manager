# Convertit une adresse IP en binaire (chaîne de 32 bits)
def ip_to_binary(ip):
    ip_parts = ip.split(".")
    binary_ip = ""
    for part in ip_parts:
        binary_octet = bin(int(part))[2:].zfill(8)
        binary_ip += binary_octet
    return binary_ip

# Convertit une chaîne binaire en adresse IP classique
def binary_to_ip(binary):
    ip_parts = []
    for i in range(0, 32, 8):
        octet = binary[i:i+8]
        ip_parts.append(str(int(octet, 2)))
    return ".".join(ip_parts)

# Calcule l'adresse réseau en faisant un ET logique entre l'IP et le masque
def get_network_address(ip, mask):
    ip_bin = ip_to_binary(ip)
    mask_bin = ip_to_binary(mask)
    network_bin = ""
    for i in range(32):
        if ip_bin[i] == "1" and mask_bin[i] == "1":
            
            network_bin += "1"
        else:
            network_bin += "0"
    return binary_to_ip(network_bin)

# Calcule l'adresse de broadcast en mettant les bits hôte à 1
def get_broadcast_address(ip, mask):
    ip_bin = ip_to_binary(ip)
    mask_bin = ip_to_binary(mask)
    broadcast_bin = ""
    for i in range(32):
        if mask_bin[i] == "0":
            broadcast_bin += "1"
        else:
            broadcast_bin += ip_bin[i]
    return binary_to_ip(broadcast_bin)

# Vérifie si une IP appartient au réseau
def ip_in_network(ip, network_ip, mask):
    ip_net = get_network_address(ip, mask)
    return ip_net == network_ip

# Calcule les IP machines de début et de fin
def get_ip_range(network_ip, mask):
    network_bin = ip_to_binary(network_ip)
    broadcast_ip = get_broadcast_address(network_ip, mask)
    broadcast_bin = ip_to_binary(broadcast_ip)

    start_int = int(network_bin, 2) + 1
    end_int = int(broadcast_bin, 2) - 1

    start_bin = bin(start_int)[2:].zfill(32)
    end_bin = bin(end_int)[2:].zfill(32)

    ip_start = binary_to_ip(start_bin)
    ip_end = binary_to_ip(end_bin)

    return ip_start, ip_end

# Menu simple pour tester
def menu():
    print("=== Vérification IP Réseau ===")
    ip = input("Entrez une IP : ")
    network = input("Entrez l'adresse réseau : ")
    mask = input("Entrez le masque : ")

    if ip_in_network(ip, network, mask):
        print("L'IP appartient au réseau.")
        start, end = get_ip_range(network, mask)
        print("IP début :", start)
        print("IP fin :", end)
    else:
        print("L'IP ne fait pas partie du réseau.")

# Lancer le menu si le fichier est exécuté
if __name__ == "__main__":
    menu()