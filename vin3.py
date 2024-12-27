from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib
import binascii
import ecdsa

def get_private_key():
    # Initialize the same curve from the challenge
    curve = ecdsa.curves.NIST224p
    
    # The branch_location in the challenge is the public key point
    # We need to reverse the public key point to get private key
    # This would require solving the ECDLP problem
    # For this challenge, you'll need to obtain the private key through other means
    # Such as analyzing the ECDSA signatures and the random k values used
    return None  # Replace with actual private key once obtained

def decrypt_flag(encrypted_data, private_key_d):
    # Extract IV and ciphertext
    iv = bytes.fromhex(encrypted_data[:32])
    encrypted_flag = bytes.fromhex(encrypted_data[32:])
    
    # Derive key using SHA-256 (same as in checkout function)
    key = hashlib.sha256(long_to_bytes(private_key_d)).digest()
    
    # Decrypt using AES-CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_flag)
    
    try:
        # Unpad the decrypted data
        flag = unpad(decrypted, 16)
        return flag.decode()
    except ValueError as e:
        return f"Decryption failed: {str(e)}"

# Your encrypted flag
encrypted_flag = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"

# To solve this challenge, you need to:
# 1. Get multiple ECDSA signatures by washing dishes
# 2. Analyze the signatures to find a pattern in k values
# 3. Use the pattern to recover the private key
# 4. Use the private key to decrypt the flag

# Once you have the private key:
private_key = None  # Replace with recovered private key
if private_key:
    print(decrypt_flag(encrypted_flag, private_key))
else:
    print("Need to recover private key first")
