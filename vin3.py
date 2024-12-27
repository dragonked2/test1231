from Crypto.Cipher import AES
import binascii
import hashlib
from Crypto.Util.number import long_to_bytes

# Your raw encrypted data and IV (output from previous results)
encrypted_data = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"

# Extract IV and encrypted flag
iv_hex = encrypted_data[:32]  # First 32 hex characters for IV
encrypted_flag_hex = encrypted_data[32:]  # The rest is the encrypted flag

# Convert the hex strings to bytes
iv = binascii.unhexlify(iv_hex)
encrypted_flag = binascii.unhexlify(encrypted_flag_hex)

# Recreate the AES key using the same private key (the key used in the original code)
private_key_d = 1234567890  # Example value used in the original code
aes_key = hashlib.sha256(long_to_bytes(private_key_d)).digest()  # Derive AES key

# Decrypt using AES in CBC mode
cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Decrypt without unpadding
decrypted_flag_raw = cipher.decrypt(encrypted_flag)

# Debug: print the raw decrypted data before attempting unpadding
print(f"Raw decrypted data (before unpadding): {binascii.hexlify(decrypted_flag_raw).decode()}")

# Raw approach: Try to find the flag even without unpadding (printing out the first bytes)
print(f"First few bytes of raw decrypted data: {decrypted_flag_raw[:16]}")

# Attempt to decode as text (without unpadding)
try:
    print(f"Raw decrypted output (text): {decrypted_flag_raw.decode(errors='ignore')}")
except Exception as e:
    print(f"Error while decoding: {str(e)}")
