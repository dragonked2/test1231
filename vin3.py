from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib
import binascii

# Encrypted data and IV from the previous output
encrypted_data = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"

# Extract IV and the encrypted flag from the provided hex string
iv_hex = encrypted_data[:32]  # First 32 hex characters (16 bytes) are the IV
encrypted_flag_hex = encrypted_data[32:]  # The rest is the encrypted flag

# Convert the hex strings to bytes
iv = binascii.unhexlify(iv_hex)  # Convert IV from hex to bytes
encrypted_flag = binascii.unhexlify(encrypted_flag_hex)  # Convert encrypted flag from hex to bytes

# Recreate the AES key using the same private key (`self.d` in the original code)
private_key_d = 1234567890  # Example private key, used in the original code
aes_key = hashlib.sha256(long_to_bytes(private_key_d)).digest()  # Derive AES key using SHA-256

# Initialize the AES cipher for decryption
cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Decrypt the encrypted flag (raw data before unpadding)
decrypted_flag_raw = cipher.decrypt(encrypted_flag)

# Debugging: Output the raw decrypted data in hex before unpadding
print(f"Raw decrypted data (before unpadding): {binascii.hexlify(decrypted_flag_raw).decode()}")

# Try to unpad the decrypted data to get the original flag
try:
    decrypted_flag = unpad(decrypted_flag_raw, 16)  # Unpad with block size of 16 bytes (AES block size)
    print(f"Decrypted flag: {decrypted_flag.decode()}")
except ValueError as e:
    print(f"Error during decryption: {str(e)}")
