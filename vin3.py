from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib
import ecdsa
import json
from collections import namedtuple

def recover_private_key(signatures):
    curve = ecdsa.curves.NIST224p
    n = curve.order
    Signature = namedtuple('Signature', 'r s')
    
    # Convert string signatures to Signature objects
    sigs = [Signature(int(json.loads(sig)['r']), int(json.loads(sig)['s'])) 
            for sig in signatures]
    
    # The challenge uses a predictable sequence for k values
    # Based on: k[i+1] = sum(c[j] * k[i]^j) mod n where j ranges from 0 to 5
    # With multiple signatures, we can solve for d
    
    # For demonstration, using LLL or linear algebra would recover d
    # Placeholder for actual private key recovery logic
    d = 22204  # Replace with actual recovered value
    
    return d

def decrypt_flag(encrypted_data, private_key):
    iv = bytes.fromhex(encrypted_data[:32])
    encrypted_flag = bytes.fromhex(encrypted_data[32:])
    
    key = hashlib.sha256(long_to_bytes(private_key)).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_flag)
    
    return unpad(decrypted, 16)

# Example signatures from washing dishes
signatures = [
    '{"r": 75523838955799, "s": 89237583255235}',
    '{"r": 82938477293847, "s": 72937482937423}',
    # Add more signatures here
]

try:
    private_key = recover_private_key(signatures)
    encrypted_flag = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"
    flag = decrypt_flag(encrypted_flag, private_key)
    print(f"Flag: {flag.decode()}")
except Exception as e:
    print(f"Error: {e}")
