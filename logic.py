from utils import errorMessages, informationMessages,To_binary
import re

def testIP(ip, subnet):
    if not ip and not subnet:
        return errorMessages["empty_input"]
    if not ip:
        return errorMessages["empty_ip"]
    if not subnet:
        return errorMessages["empty_subnet"]
    
    # IP address validation
    ip_error = validate_ip(ip)
    if ip_error:
        return ip_error
    
    # Subnet mask validation
    subnet_error = validate_subnet(subnet)
    if subnet_error:
        return subnet_error
    
    return 0

def validate_ip(ip):
    """Validates an IP address"""

    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
        return errorMessages["invalid_ip_format"]
    
    ip_parts = ip.split('.')
    if len(ip_parts) != 4:
        return errorMessages["invalid_ip_octets"]
    
    for i, part in enumerate(ip_parts):
        if len(part) > 1 and part[0] == '0':
            return errorMessages["leading_zeros"]
        
        try:
            octet = int(part)
        except ValueError:
            return errorMessages["invalid_octet_number"]
        
        if octet < 0 or octet > 255:
            return errorMessages["invalid_octet_range"]
    
    return None

def validate_subnet(subnet):
    """Validates a subnet mask"""
    # Check general format for decimal notation
    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', subnet):
        return errorMessages["invalid_subnet_format"]
    
    # Split into octets
    subnet_parts = subnet.split('.')
    if len(subnet_parts) != 4:
        return errorMessages["invalid_subnet_octets"]
    
    # Validate each octet
    subnet_octets = []
    for part in subnet_parts:
        try:
            octet = int(part)
        except ValueError:
            return errorMessages["invalid_subnet_number"]
        
        if octet < 0 or octet > 255:
            return errorMessages["invalid_subnet_range"]
        
        subnet_octets.append(octet)
    
    # Check special masks
    if subnet == "0.0.0.0":
        return errorMessages["subnet_all_zeros"]
    if subnet == "255.255.255.255":
        return errorMessages["subnet_all_ones"]
    
    # Check bit pattern (valid mask)
    if not is_valid_subnet_pattern(subnet_octets):
        return errorMessages["invalid_subnet_pattern"]
    
    return None

def is_valid_subnet_pattern(octets):
    binary = ''.join(To_binary(octet) for octet in octets)
    
    mask_int = int(binary, 2)
    
    # Check if it's a valid contiguous mask
    # For a valid mask, mask + 1 should be a power of 2 when inverted
    # Example: 255.255.240.0 = 11111111111111111111000000000000
    # Inverted: 00000000000000000000111111111111 = 4095
    # 4095 + 1 = 4096 = 2^12 (power of 2) ✓
    inverted_mask = (~mask_int) & 0xFFFFFFFF
    return (inverted_mask & (inverted_mask + 1)) == 0

def detect_ip_class(ip):
    """Detects the IP address class"""
    first_octet = int(ip.split('.')[0])
    
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