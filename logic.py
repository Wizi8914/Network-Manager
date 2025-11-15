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
    cidr_prefix = None
    clean_ip = ip
    
    if '/' in ip:
        if ip.count('/') > 1:
            return errorMessages["cidr_multiple_slashes"],
        
        if not isClassful:
            return errorMessages["cidr_slash_in_classful"],
        
        parts = ip.split('/')
        clean_ip = parts[0]
        prefix_str = parts[1]
        
        if not prefix_str:
            return errorMessages["cidr_invalid_format"], 
        
        try:
            cidr_prefix = int(prefix_str)
        except ValueError:
            return errorMessages["cidr_invalid_prefix"], 
        
        if cidr_prefix < 0 or cidr_prefix > 32:
            return errorMessages["cidr_prefix_out_of_range"], 
    else:
        if isClassful:
            return errorMessages["cidr_missing_slash"], 
    
    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', clean_ip):
        return errorMessages["invalid_ip_format"], 
    
    ip_parts = clean_ip.split('.')
    if len(ip_parts) != 4:
        return errorMessages["invalid_ip_octets"],
    
    for i, part in enumerate(ip_parts):
        if len(part) > 1 and part[0] == '0':
            return errorMessages["leading_zeros"],
        
        try:
            octet = int(part)
        except ValueError:
            return errorMessages["invalid_octet_number"],
        
        if octet < 0 or octet > 255:
            return errorMessages["invalid_octet_range"],
    
    return None, clean_ip, cidr_prefix

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
    binary = ''.join(To_binary(octet) for octet in octets)
    mask_int = int(binary, 2)
    inverted_mask = (~mask_int) & 0xFFFFFFFF
    return (inverted_mask & (inverted_mask + 1)) == 0

def cidr_to_subnet_mask(prefix):
    if prefix < 0 or prefix > 32:
        return None
    
    mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    octets = [(mask_int >> (24 - i * 8)) & 0xFF for i in range(4)]
    return '.'.join(map(str, octets))

def extract_ip_from_cidr(ip):
    return ip.split('/')[0] if '/' in ip else ip

def detect_ip_class(ip):
    clean_ip = extract_ip_from_cidr(ip)
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