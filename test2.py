import hashlib
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes
import random

# Constants
IV = os.urandom(8)  # Random Initialization Vector for AES
KEY = os.urandom(16)  # Random AES Key for encryption
FLAG = os.environ.get("FLAG", "0xL4ugh{6d656f776d6f65776d6f65776d6f6577}").encode()  # Default FLAG if not set in environment

class Player:
    def __init__(self, credits=800):
        self.credits = credits

class CoffeShop:
    def __init__(self, available_credits):
        self.available = available_credits
        self.d = random.randint(1, 224)  # Random private key for simulation

    def checkout(self, player):
        if player.credits >= 800:
            sha256 = hashlib.sha256()
            sha256.update(long_to_bytes(self.d))  # Use the random private key
            key = sha256.digest()  # AES key derived from the private key
            iv = os.urandom(16)  # Random IV for AES encryption
            cipher = AES.new(key, AES.MODE_CBC, iv)  # AES encryption in CBC mode
            print(f"Here's your receipt: ")
            encrypted_flag = cipher.encrypt(pad(FLAG, 16))  # Encrypt the flag
            return iv.hex() + encrypted_flag.hex()  # Return IV + encrypted flag

# No need to simulate washing dishes, we directly proceed to checkout
shop = CoffeShop(800)
you = Player(800)

print("You have enough money to pay for the meal!")
print("Getting the flag directly...")
print(shop.checkout(you))  # Directly output the encrypted flag
