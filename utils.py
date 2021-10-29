import re

def is_address(address):
    if not re.match(r'^(0x)?[0-9a-f]{40}$', address, flags=re.IGNORECASE):
        # Check if it has the basic requirements of an address
        return False
    elif re.match(r'^(0x)?[0-9a-fA-F]{40}$', address) or re.match(r'^(0x)?[0-9A-F]{40}$', address):
        # If it's all small caps or all all caps, return true
        return True

def remove_symbols(hash: str):
    SYMBOLS = '{}()[].,:;+-*/&|<>=~$1234567890'
    for i in SYMBOLS:
        if i in hash:
            hash = hash.replace(i, "")
    
    return hash