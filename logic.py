from utils import errorMessages
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
    return f"{errorMessages['valid_ip_subnet']} {class_info}"

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
    # Check if it's in CIDR notation
    if subnet.startswith('/'):
        cidr = subnet[1:]
        if not cidr.isdigit():
            return errorMessages["invalid_cidr_format"]
        cidr_value = int(cidr)
        if cidr_value < 0 or cidr_value > 32:
            return errorMessages["invalid_cidr_range"]
        return None
    
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
    """Checks if the mask has a valid bit pattern (consecutive 1s followed by 0s)"""
    # Convert each octet to binary and concatenate
    binary = ''.join(format(octet, '08b') for octet in octets)
    
    # A valid subnet mask must follow the pattern: 1*0*
    # This means all 1s must be consecutive at the beginning, followed by all 0s
    # No holes (0s followed by 1s) are allowed
    
    # Method 1: Use regex to check the pattern
    pattern = re.match(r'^1*0*$', binary)
    if not pattern:
        return False
    
    # Method 2: Additional verification - check for holes manually
    # Once we find a 0, we should not find any 1s after it
    found_zero = False
    for bit in binary:
        if bit == '0':
            found_zero = True
        elif bit == '1' and found_zero:
            # Found a 1 after a 0 - this is a hole, invalid mask
            return False
    
    # Method 3: Verify using arithmetic property
    # A valid subnet mask in decimal should have the property that
    # (mask + 1) & mask == 0, where mask is the 32-bit integer representation
    mask_int = int(binary, 2)
    
    # Special cases: all 0s and all 1s are handled separately
    if mask_int == 0 or mask_int == 0xFFFFFFFF:
        return True
    
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

def test_subnet_masks():
    """Test function to validate different subnet mask patterns"""
    test_cases = [
        # Valid masks
        ("255.255.255.0", True),      # 11111111.11111111.11111111.00000000
        ("255.255.240.0", True),      # 11111111.11111111.11110000.00000000
        ("255.128.0.0", True),        # 11111111.10000000.00000000.00000000
        ("255.255.255.252", True),    # 11111111.11111111.11111111.11111100
        ("128.0.0.0", True),          # 10000000.00000000.00000000.00000000
        
        # Invalid masks (with holes)
        ("255.255.15.255", False),    # 11111111.11111111.00001111.11111111 (hole)
        ("255.127.255.0", False),     # 11111111.01111111.11111111.00000000 (hole)
        ("240.255.255.0", False),     # 11110000.11111111.11111111.00000000 (hole)
        ("255.255.255.129", False),   # 11111111.11111111.11111111.10000001 (hole)
        ("255.254.255.0", False),     # 11111111.11111110.11111111.00000000 (hole)
    ]
    
    print("Testing subnet mask validation:")
    for mask, expected in test_cases:
        octets = [int(x) for x in mask.split('.')]
        result = is_valid_subnet_pattern(octets)
        status = "✓" if result == expected else "✗"
        binary = '.'.join(format(octet, '08b') for octet in octets)
        print(f"{status} {mask} ({binary}) - Expected: {expected}, Got: {result}")

# Uncomment the line below to run tests
# test_subnet_masks()