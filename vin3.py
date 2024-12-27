from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib
import binascii

# Provided encrypted data (the IV + encrypted FLAG)
encrypted_data = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"

# Extract the IV and encrypted FLAG from the provided hex string
iv_hex = encrypted_data[:32]  # First 32 hex characters (16 bytes) represent the IV
encrypted_flag_hex = encrypted_data[32:]  # The remaining hex characters represent the encrypted FLAG

# Convert the hex strings to bytes
iv = binascii.unhexlify(iv_hex)
encrypted_flag = binascii.unhexlify(encrypted_flag_hex)

# Manually set the private key `self.d` (from the original code logic)
private_key_d = 1234567890  # The value of `self.d` used in the original code

# Derive the AES key from the private key using SHA-256
aes_key = hashlib.sha256(long_to_bytes(private_key_d)).digest()

# Decrypt the encrypted FLAG using AES in CBC mode
cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Decrypt the encrypted FLAG
decrypted_flag_raw = cipher.decrypt(encrypted_flag)

# Try to unpad the decrypted data (using the same padding scheme as in the original code)
try:
    decrypted_flag = unpad(decrypted_flag_raw, 16)  # Unpad with block size of 16 bytes (AES block size)
    print(f"Decrypted FLAG: {decrypted_flag.decode()}")
except ValueError as e:
    print(f"Error during decryption: Padding is incorrect. Debug Info: {e}")
