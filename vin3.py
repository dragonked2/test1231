from Crypto.Cipher import AES
import binascii
import hashlib
from Crypto.Util.number import long_to_bytes

# Your encrypted data and IV from previous results
encrypted_data = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"

# Extract IV and encrypted flag from the given data
iv_hex = encrypted_data[:32]  # First 32 hex characters are the IV
encrypted_flag_hex = encrypted_data[32:]  # The remaining part is the encrypted flag

# Convert the hex strings to bytes
iv = binascii.unhexlify(iv_hex)
encrypted_flag = binascii.unhexlify(encrypted_flag_hex)

# Recreate the AES key using the same private key
private_key_d = 1234567890  # Example private key used earlier
aes_key = hashlib.sha256(long_to_bytes(private_key_d)).digest()  # Derive AES key

# Decrypt the encrypted flag using AES in CBC mode
cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Decrypt without unpadding
decrypted_flag_raw = cipher.decrypt(encrypted_flag)

# Debugging: Print raw decrypted data before attempting to unpad
print(f"Raw decrypted data (before unpadding): {binascii.hexlify(decrypted_flag_raw).decode()}")

# Attempt to manually strip potential padding by removing the last few bytes
# Assuming the padding is not PKCS7 and it's a simpler form of padding (like trailing bytes)
decrypted_flag_manual = decrypted_flag_raw.rstrip(b'\x00')  # Strip trailing zero bytes

# Print the manually stripped data
try:
    print(f"Decrypted flag after manual padding strip: {decrypted_flag_manual.decode(errors='ignore')}")
except Exception as e:
    print(f"Error while decoding: {str(e)}")
