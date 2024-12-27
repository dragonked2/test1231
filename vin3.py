from Crypto.Util.number import isPrime, long_to_bytes
from math import gcd
import itertools

def factorize_n(n):
    factors = []
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return factors

def find_factors(n, w, p_bits=512, q_bits=1024):
    # Try to find p using the relationship with w
    for multiplier in range(1, 10):  # Try different multipliers in case of edge cases
        test_p = n // (w * multiplier)
        if test_p <= 0:
            continue
            
        # Check if p is the right size (approximately)
        if abs(test_p.bit_length() - p_bits) > 50:
            continue
            
        x = 2 * w * test_p - 1
        if n % x == 0:
            remaining = n // x
            # Try factoring the remaining part to get p and q
            factors = factorize_n(remaining)
            
            # Try different combinations of factors
            for r in range(1, len(factors) + 1):
                for comb in itertools.combinations(factors, r):
                    potential_p = 1
                    for f in comb:
                        potential_p *= f
                    potential_q = remaining // potential_p
                    
                    # Check if we found valid p and q
                    if (isPrime(potential_p) and isPrime(potential_q) and 
                        abs(potential_p.bit_length() - p_bits) <= 50 and
                        abs(potential_q.bit_length() - q_bits) <= 50):
                        return potential_p, potential_q, x
                        
    return None, None, None

def solve_rsa_challenge():
    # Given values
    n = 18186672849609603331344182584568642941078893104802301217241028624469607021717197485036251613075846729705028441094100248337306406098776983108141004863456595015660485098203867670995838502297993710897784135087115777697925848407153788837657722171924264421550564295047937036911411846582733847201015164634546149603743246378710225407507435371659148999942913405493417037116587298256802831009824832360479040621348157491754407277404391337488226402711686156101028879269050800874367763551119682177453648890492731413760738825931684979379268401715029193518612541590846238434595210876468090976194627398214837801868969047036272502669215123
    e = 65537
    c = 1617999293557620724157535537778741335004656286655134597579706838690566178453141895621909480622070931381931296468696585541046188947144084107698620486576573164517733264644244665803523581927226503313545336021669824656871624111167113668644971950653103830443634752480477923970518891620296211614968804248580381104245404606917784407446279304488720323993268637887493503760075542578433642707326246816504761740168067216112150231996966168374619580811013034502620645288021335483574561758204631096791789272910596432850424873592013042090724982779979496197239647019869960002253384162472401724931485470355288814804233134786749608640103461

    # Try all possible values of w (20-bit primes)
    for w in range(2**19, 2**20):
        if not isPrime(w):
            continue
            
        print(f"Trying w = {w}")
        
        # Try to find p, q, and x using this w
        p, q, x = find_factors(n, w)
        
        if p is not None and q is not None and x is not None:
            print(f"Found factors!")
            print(f"p = {p}")
            print(f"q = {q}")
            print(f"x = {x}")
            
            # Verify our factorization
            if p * q * x != n:
                print("Invalid factorization, continuing...")
                continue
                
            try:
                # Calculate private key
                phi = (p - 1) * (q - 1) * (x - 1)
                d = pow(e, -1, phi)
                
                # Decrypt the message
                m = pow(c, d, n)
                decrypted = long_to_bytes(m)
                
                # Check if decryption seems valid (contains printable ASCII)
                if all(32 <= b <= 126 for b in decrypted):
                    print(f"Decrypted message: {decrypted}")
                    return decrypted
                    
            except Exception as e:
                print(f"Error during decryption: {e}")
                continue
                
    return None

if __name__ == "__main__":
    result = solve_rsa_challenge()
    if result is None:
        print("Could not solve the challenge. Trying alternative approach...")
        # Here we could implement alternative approaches if the first one fails
        # For example, trying different factorization methods or looking for other patterns
