from utils import errorMessages, To_binary
import re

def testIP(ip, subnet):
    # Check if fields are empty
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
    
    # IP/Subnet compatibility check
    compatibility_error = validate_ip_subnet_compatibility(ip, subnet)
    if compatibility_error:
        return compatibility_error
    
    # IP class detection
    class_info = detect_ip_class(ip)
    
    # If everything is valid, return success message with class info
    return 0

def validate_ip(ip):
    """Validates an IP address"""
    # Check general format
    if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
        return errorMessages["invalid_ip_format"]
    
    # Split into octets
    ip_parts = ip.split('.')
    if len(ip_parts) != 4:
        return errorMessages["invalid_ip_octets"]
    
    # Validate each octet
    for i, part in enumerate(ip_parts):
        # Check for leading zeros
        if len(part) > 1 and part[0] == '0':
            return errorMessages["leading_zeros"]
        
        # Check if it's a valid number
        try:
            octet = int(part)
        except ValueError:
            return errorMessages["invalid_octet_number"]
        
        # Check range
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

def validate_ip_subnet_compatibility(ip, subnet):
    """Checks compatibility between IP and mask"""
    # This function could be extended for more advanced checks
    # For now, we assume that if both are individually valid,
    # they are compatible
    return None

def detect_ip_class(ip):
    """Detects the IP address class"""
    first_octet = int(ip.split('.')[0])
    
    if 1 <= first_octet <= 126:
        return errorMessages["class_a_detected"]
    elif 128 <= first_octet <= 191:
        return errorMessages["class_b_detected"]
    elif 192 <= first_octet <= 223:
        return errorMessages["class_c_detected"]
    elif 224 <= first_octet <= 239:
        return errorMessages["class_d_detected"]
    elif 240 <= first_octet <= 255:
        return errorMessages["class_e_detected"]
    else:
        return ""