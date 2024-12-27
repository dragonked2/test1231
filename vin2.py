from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib
import binascii

# Your IV and encrypted flag (the hex output you got from the receipt)
encrypted_data = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"

# Extract the IV and encrypted flag
iv_hex = encrypted_data[:32]  # First 32 hex characters for IV
encrypted_flag_hex = encrypted_data[32:]  # The remaining hex for the encrypted flag

# Convert the hex strings to bytes
iv = binascii.unhexlify(iv_hex)
encrypted_flag = binascii.unhexlify(encrypted_flag_hex)

# Recreate the AES key using the same private key (we used random d earlier, use the same d here)
private_key_d = 1234567890  # This is the same value for self.d from the original code
aes_key = hashlib.sha256(long_to_bytes(private_key_d)).digest()

# Decrypt the flag using AES in CBC mode
cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Attempt to decrypt and check the raw decrypted output
try:
    decrypted_flag_raw = cipher.decrypt(encrypted_flag)  # Decrypt without unpadding
    print(f"Raw decrypted data (before unpadding): {decrypted_flag_raw.hex()}")
    
    # Now try to unpad the decrypted data
    decrypted_flag = unpad(decrypted_flag_raw, 16)  # Unpad with block size of 16 bytes
    print(f"Decrypted flag: {decrypted_flag.decode()}")
except ValueError as e:
    print(f"Error during decryption: {str(e)}")
