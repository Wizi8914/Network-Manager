from utils import errorMessages, informationMessages,To_binary
import re

def testIP(ip, subnet, isClassful):
    if not ip and not subnet:
        return errorMessages["empty_input"]
    if not ip:
        return errorMessages["empty_ip"]
    
    if not isClassful:
        if '/' in ip:
            return errorMessages["cidr_slash_in_classful"]
        if not subnet:
            return errorMessages["empty_subnet"]
    else:
        if '/' not in ip:
            return errorMessages["cidr_missing_slash"]
    
    ip_error, clean_ip, cidr_prefix = validate_ip(ip, isClassful)
    if ip_error:
        return ip_error
    
    if not isClassful and subnet:
        subnet_error = validate_subnet(subnet)
        if subnet_error:
            return subnet_error
    
    return 0

def validate_ip(ip, isClassful):
    # Valide le format de l'IP et extrait le préfixe CIDR si présent
    # Retourne: (erreur, ip_nettoyée, préfixe_cidr)
    cidr_prefix = None
    clean_ip = ip
    
    if '/' in ip:
        if ip.count('/') > 1:
            return errorMessages["cidr_multiple_slashes"], None, None
        
        if not isClassful:
            return errorMessages["cidr_slash_in_classful"], None, None
        
        parts = ip.split('/')
        clean_ip = parts[0]
        prefix_str = parts[1]
        
        if not prefix_str:
            return errorMessages["cidr_invalid_format"], None, None
        
        try:
            cidr_prefix = int(prefix_str)
        except ValueError:
            return errorMessages["cidr_invalid_prefix"], None, None
        
        if cidr_prefix < 0 or cidr_prefix > 32:
            return errorMessages["cidr_prefix_out_of_range"], None, None 
    else:
        if isClassful:
            return errorMessages["cidr_missing_slash"], None, None
    
    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', clean_ip):
        return errorMessages["invalid_ip_format"], None, None 
    
    ip_parts = clean_ip.split('.')
    if len(ip_parts) != 4:
        return errorMessages["invalid_ip_octets"], None, None
    
    for i, part in enumerate(ip_parts):
        if len(part) > 1 and part[0] == '0':
            return errorMessages["leading_zeros"], None, None
        
        try:
            octet = int(part)
        except ValueError:
            return errorMessages["invalid_octet_number"], None, None
        
        if octet < 0 or octet > 255:
            return errorMessages["invalid_octet_range"], None, None
    
    return None, clean_ip, cidr_prefix


def validate_ipv4_format(ip):
    error, _, _ = validate_ip(ip, isClassful=False)
    return error


def mask_to_dotted(mask_input):
    if not mask_input:
        return None, errorMessages["empty_subnet"]

    s = str(mask_input).strip()
    if s.startswith('/'):
        s = s.lstrip('/')

    if s.isdigit():
        try:
            prefix = int(s)
        except ValueError:
            return None, errorMessages["cidr_invalid_prefix"]
        if prefix < 0 or prefix > 32:
            return None, errorMessages["cidr_prefix_out_of_range"]
        return cidr_to_subnet_mask(prefix), None

    subnet_err = validate_subnet(s)
    if subnet_err:
        return None, subnet_err
    return s, None


def parse_membership_inputs(ip, network, mask):
    # Normalise et valide les entrées de vérification d'appartenance réseau
    # Gère plusieurs formats: IP seule, IP/CIDR, réseau/CIDR, masque séparé
    # Retourne: (ip_propre, réseau_propre, masque_pointé, erreur)
    ip_raw = (ip or '').strip()
    network_raw = (network or '').strip()
    mask_raw = (mask or '').strip()

    if not ip_raw and not network_raw:
        return None, None, None, errorMessages["empty_input"]

    # Gérer IP avec notation CIDR (ex: 192.168.1.10/24)
    # Extrait l'IP et le préfixe, puis convertit en masque pointé si nécessaire
    cidr_prefix = None
    ip_only = ip_raw
    if '/' in ip_raw:
        parts = ip_raw.split('/')
        if len(parts) != 2:
            return None, None, None, errorMessages["cidr_invalid_format"]
        ip_only = parts[0]
        try:
            cidr_prefix = int(parts[1])
        except ValueError:
            return None, None, None, errorMessages["cidr_invalid_prefix"]
        if cidr_prefix < 0 or cidr_prefix > 32:
            return None, None, None, errorMessages["cidr_prefix_out_of_range"]
        
        if not mask_raw:
            mask_dotted = cidr_to_subnet_mask(cidr_prefix)
        else:
            mask_dotted, mask_err = mask_to_dotted(mask_raw)
            if mask_err:
                return None, None, None, mask_err
    else:
        mask_dotted = None

    if ip_only:
        ip_err = validate_ipv4_format(ip_only)
        if ip_err:
            return None, None, None, ip_err

    if mask_dotted is None and mask_raw:
        mask_dotted, mask_err = mask_to_dotted(mask_raw)
        if mask_err:
            return None, None, None, mask_err

    # Extraire le masque depuis le réseau si format CIDR
    if not mask_dotted and '/' in network_raw:
        try:
            net_ip, net_pref = network_raw.split('/')
            net_pref = int(net_pref)
            mask_dotted = cidr_to_subnet_mask(net_pref)
            network_raw = net_ip
        except Exception:
            return None, None, None, errorMessages["cidr_invalid_format"]

    if network_raw:
        net_err = validate_ipv4_format(network_raw)
        if net_err:
            return None, None, None, net_err

    # Calculer le réseau si absent
    if not network_raw and ip_only and mask_dotted:
        try:
            network_calc = get_network_address(ip_only, mask_dotted)
            network_raw = network_calc
        except Exception:
            return None, None, None, errorMessages["ip_subnet_mismatch"]

    # Vérifier cohérence IP/réseau/masque
    if ip_only and network_raw and mask_dotted:
        try:
            network_from_ip = get_network_address(ip_only, mask_dotted)
            if network_from_ip != network_raw:
                return None, None, None, errorMessages["ip_subnet_mismatch"]
        except Exception:
            return None, None, None, errorMessages["ip_subnet_mismatch"]

    # Vérifications finales : on doit avoir au minimum IP et masque
    if not ip_only:
        return None, None, None, errorMessages["empty_ip"]
    
    if not mask_dotted:
        return None, None, None, errorMessages["empty_subnet"]

    return ip_only, network_raw, mask_dotted, None

def validate_subnet(subnet):
    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', subnet):
        return errorMessages["invalid_subnet_format"]
    
    subnet_parts = subnet.split('.')
    if len(subnet_parts) != 4:
        return errorMessages["invalid_subnet_octets"]
    
    subnet_octets = []
    for part in subnet_parts:
        try:
            octet = int(part)
        except ValueError:
            return errorMessages["invalid_subnet_number"]
        
        if octet < 0 or octet > 255:
            return errorMessages["invalid_subnet_range"]
        
        subnet_octets.append(octet)
    
    if subnet == "0.0.0.0":
        return errorMessages["subnet_all_zeros"]
    if subnet == "255.255.255.255":
        return errorMessages["subnet_all_ones"]
    
    if not is_valid_subnet_pattern(subnet_octets):
        return errorMessages["invalid_subnet_pattern"]
    
    return None

def is_valid_subnet_pattern(octets):
    # Vérifie que le masque suit le pattern binaire valide:
    # Tous les bits à 1 doivent être contigus à gauche, suivis uniquement de bits à 0
    # Ex: 11111111.11111111.11110000.00000000 ✓  mais pas 11111111.11110000.11111111.00000000 ✗
    binary = ''.join(To_binary(octet) for octet in octets)
    mask_int = int(binary, 2)
    inverted_mask = (~mask_int) & 0xFFFFFFFF
    # Si l'inverse du masque +1 a un ET logique nul avec lui-même, le pattern est valide
    return (inverted_mask & (inverted_mask + 1)) == 0

def cidr_to_subnet_mask(prefix):
    if prefix < 0 or prefix > 32:
        return None
    
    # Crée un masque avec 'prefix' bits à 1 suivis de bits à 0
    # Ex: prefix=24 → 11111111.11111111.11111111.00000000 → 255.255.255.0
    mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    octets = [(mask_int >> (24 - i * 8)) & 0xFF for i in range(4)]
    return '.'.join(map(str, octets))

def detect_ip_class(ip):
    clean_ip = ip.split('/')[0] if '/' in ip else ip
    first_octet = int(clean_ip.split('.')[0])
    
    if 1 <= first_octet <= 126:
        return informationMessages["class_a_detected"]
    elif 128 <= first_octet <= 191:
        return informationMessages["class_b_detected"]
    elif 192 <= first_octet <= 223:
        return informationMessages["class_c_detected"]
    elif 224 <= first_octet <= 239:
        return informationMessages["class_d_detected"]
    elif 240 <= first_octet <= 255:
        return informationMessages["class_e_detected"]
    else:
        return ""


# Calculs réseau (conversions binaires, adresses réseau/broadcast, plages)
def ip_to_binary(ip):
    # Convertit une IP décimale en binaire (32 bits)
    # Ex: 192.168.1.1 → '11000000101010000000000100000001'
    ip_parts = ip.split('.')
    binary_ip = ''
    for part in ip_parts:
        binary_octet = bin(int(part))[2:].zfill(8)
        binary_ip += binary_octet
    return binary_ip


def binary_to_ip(binary):
    ip_parts = []
    for i in range(0, 32, 8):
        octet = binary[i:i+8]
        ip_parts.append(str(int(octet, 2)))
    return '.'.join(ip_parts)


def get_network_address(ip, mask):
    # Calcule l'adresse réseau en appliquant un ET logique bit à bit entre IP et masque
    # Efface tous les bits hôte (où le masque = 0), conserve uniquement la partie réseau
    ip_bin = ip_to_binary(ip)
    mask_bin = ip_to_binary(mask)
    network_bin = ''
    for i in range(32):
        if ip_bin[i] == '1' and mask_bin[i] == '1':
            network_bin += '1'
        else:
            network_bin += '0'
    return binary_to_ip(network_bin)


def get_broadcast_address(ip, mask):
    # Calcule l'adresse de broadcast en mettant tous les bits hôte à 1
    # Conserve la partie réseau (bits où masque = 1), met à 1 tous les bits où masque = 0
    ip_bin = ip_to_binary(ip)
    mask_bin = ip_to_binary(mask)
    broadcast_bin = ''
    for i in range(32):
        if mask_bin[i] == '0':
            broadcast_bin += '1'
        else:
            broadcast_bin += ip_bin[i]
    return binary_to_ip(broadcast_bin)


def ip_in_network(ip, network_ip, mask):
    ip_net = get_network_address(ip, mask)
    return ip_net == network_ip


def get_ip_range(network_ip, mask):
    # Calcule la plage d'IPs utilisables pour les hôtes
    # Exclut l'adresse réseau (première) et l'adresse broadcast (dernière)
    network_bin = ip_to_binary(network_ip)
    broadcast_ip = get_broadcast_address(network_ip, mask)
    broadcast_bin = ip_to_binary(broadcast_ip)

    # +1 pour exclure l'adresse réseau, -1 pour exclure le broadcast
    start_int = int(network_bin, 2) + 1
    end_int = int(broadcast_bin, 2) - 1

    start_bin = bin(start_int)[2:].zfill(32)
    end_bin = bin(end_int)[2:].zfill(32)

    ip_start = binary_to_ip(start_bin)
    ip_end = binary_to_ip(end_bin)

    return ip_start, ip_end