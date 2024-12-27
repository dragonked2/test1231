from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib

ENCRYPTED_FLAG = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"

# Known private key from analyzing ECDSA parameters
PRIVATE_KEY = 22204

def decrypt_flag():
    try:
        iv = bytes.fromhex(ENCRYPTED_FLAG[:32])
        encrypted_flag = bytes.fromhex(ENCRYPTED_FLAG[32:])
        
        key = hashlib.sha256(long_to_bytes(PRIVATE_KEY)).digest()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_flag)
        
        return unpad(decrypted, 16)
    except Exception as e:
        return f"Error: {e}"

print(decrypt_flag().decode())
