from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib
import binascii
import sys

def decrypt_flag(encrypted_data, private_key):
    try:
        # Validate input
        if not isinstance(encrypted_data, str) or len(encrypted_data) < 32:
            raise ValueError("Invalid encrypted data format")
            
        # Extract IV and encrypted flag
        iv_hex = encrypted_data[:32]
        encrypted_flag_hex = encrypted_data[32:]
        
        # Convert hex to bytes
        try:
            iv = binascii.unhexlify(iv_hex)
            encrypted_flag = binascii.unhexlify(encrypted_flag_hex)
        except binascii.Error as e:
            raise ValueError(f"Invalid hex data: {e}")
            
        # Derive AES key - using SHA-256 for key derivation
        aes_key = hashlib.sha256(long_to_bytes(private_key)).digest()
        
        # Initialize cipher
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        
        # Decrypt and unpad
        decrypted_raw = cipher.decrypt(encrypted_flag)
        decrypted_flag = unpad(decrypted_raw, AES.block_size)
        
        return decrypted_flag.decode('utf-8')
        
    except Exception as e:
        return f"Decryption failed: {str(e)}"

def main():
    # Your encrypted data
    encrypted_data = "6601b7897968991e500d523f1073a15604515faeba23560ced71a573d711e20425ceb19fe8ed38072f4f366bd78db56d8c4818262bf4694f18b1c3d17510bee7"
    
    # Try multiple possible private keys
    test_keys = [
        1234567890,
        987654321,
        int('1234567890', 16),  # Try hex interpretation
        123456789012345,
        # Add more potential keys if needed
    ]
    
    for key in test_keys:
        print(f"\nTrying key: {key}")
        result = decrypt_flag(encrypted_data, key)
        if not result.startswith("Decryption failed"):
            print(f"Successfully decrypted flag: {result}")
            return
        
    print("\nDecryption failed with all attempted keys.")

if __name__ == "__main__":
    main()
