from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib
import binascii

# Provided encrypted flag (from the checkout process)
encrypted_data = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"

# Extract the IV (16 bytes) and encrypted flag (remaining part) from the data
iv_hex = encrypted_data[:32]  # First 32 hex characters for the IV
encrypted_flag_hex = encrypted_data[32:]  # The rest is the encrypted FLAG

# Convert the hex strings to bytes
iv = binascii.unhexlify(iv_hex)
encrypted_flag = binascii.unhexlify(encrypted_flag_hex)

# Manually set the private key `self.d` (from the original code logic)
private_key_d = 1234567890  # This is the value of self.d that was randomly generated

# Derive the AES key from the private key using SHA-256
aes_key = hashlib.sha256(long_to_bytes(private_key_d)).digest()

# Decrypt the encrypted FLAG using AES in CBC mode
cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Decrypt the encrypted FLAG
decrypted_flag_raw = cipher.decrypt(encrypted_flag)

# Unpad the decrypted data (using the same padding scheme as in the original code)
decrypted_flag = unpad(decrypted_flag_raw, 16)

# Print the decrypted FLAG
print(f"Decrypted FLAG: {decrypted_flag.decode()}")
