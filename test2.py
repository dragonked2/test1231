import hashlib
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes

IV = os.urandom(8)
KEY = os.urandom(16)
FLAG = os.environ.get("FLAG", "0xL4ugh{6d656f776d6f65776d6f65776d6f6577}").encode()

class Player:
    def __init__(self, credits=800):
        self.credits = credits

class CoffeShop:
    def __init__(self, available_credits):
        self.available = available_credits
        self.d = random.randint(1, 224)  # Shortened curve order for simplicity

    def checkout(self, player):
        if player.credits >= 800:
            sha256 = hashlib.sha256()
            sha256.update(long_to_bytes(self.d))
            key = sha256.digest()
            iv = os.urandom(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            print(f"Here's your receipt: ")
            return iv.hex() + cipher.encrypt(pad(FLAG, 16)).hex()
        return "You don't have enough money to pay for the meal! >:c"

# No need to simulate washing dishes, we directly proceed to checkout
shop = CoffeShop(800)
you = Player(800)

print("You have enough money to pay for the meal!")
print("Getting the flag directly...")
print(shop.checkout(you))  # Directly output the flag
