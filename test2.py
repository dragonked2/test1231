from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

# This is the ciphertext you got from the receipt
ciphertext_hex = "f45fa9931320544b8181d0ae999531cca71702b05489f9cd9adf5782a50350c51bac1753e93996d99d2186f75f208b7714ec07661e1ba8b8fa5c1d568d37fc6f"

# AES key derived from the private key `d` (you need to obtain `d`)
private_key_d = 123456789  # Replace with the actual private key `d`

# Derive AES key using SHA-256 on private key `d`
aes_key = sha256(long_to_bytes(private_key_d)).digest()

# Extract the IV from the first 16 bytes (32 hex characters) of the ciphertext
iv = bytes.fromhex(ciphertext_hex[:32])

# The rest is the actual ciphertext
ciphertext = bytes.fromhex(ciphertext_hex[32:])

# Decrypt the ciphertext
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
decrypted_flag = unpad(cipher.decrypt(ciphertext), AES.block_size)

# Print the decrypted flag
print("Decrypted Flag:", decrypted_flag.decode())
