from utils import errorMessages

def testIP(ip, subnet):
    if not ip or not subnet:
        return errorMessages["empty_input"]
    
    ip_parts = ip.split('.')
    subnet_parts = subnet.split('.')
    if len(ip_parts) != 4 or len(subnet_parts) != 4:
        return errorMessages["invalid_format"]