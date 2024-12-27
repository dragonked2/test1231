from Crypto.Util.number import isPrime, long_to_bytes
from math import gcd, isqrt

def find_prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3, isqrt(n) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors

def solve_challenge():
    # Given parameters
    n = 18186672849609603331344182584568642941078893104802301217241028624469607021717197485036251613075846729705028441094100248337306406098776983108141004863456595015660485098203867670995838502297993710897784135087115777697925848407153788837657722171924264421550564295047937036911411846582733847201015164634546149603743246378710225407507435371659148999942913405493417037116587298256802831009824832360479040621348157491754407277404391337488226402711686156101028879269050800874367763551119682177453648890492731413760738825931684979379268401715029193518612541590846238434595210876468090976194627398214837801868969047036272502669215123
    e = 65537
    c = 1617999293557620724157535537778741335004656286655134597579706838690566178453141895621909480622070931381931296468696585541046188947144084107698620486576573164517733264644244665803523581927226503313545336021669824656871624111167113668644971950653103830443634752480477923970518891620296211614968804248580381104245404606917784407446279304488720323993268637887493503760075542578433642707326246816504761740168067216112150231996966168374619580811013034502620645288021335483574561758204631096791789272910596432850424873592013042090724982779979496197239647019869960002253384162472401724931485470355288814804233134786749608640103461

    # We know p is 512 bits and w is 20 bits
    # This means x = 2wp - 1 should be around 532 bits
    x_approx_size = 532
    p_approx_size = 512

    # Try small primes first as potential w values
    for w in range(2**19, 2**20):
        if not isPrime(w):
            continue
            
        print(f"Testing w={w}")
        
        # Use the fact that x = 2wp - 1
        # This means n = pqx = pq(2wp - 1)
        
        # Try to estimate p using cube root of n
        p_estimate = int(pow(n, 1/3))
        
        # Search around the estimate
        search_range = 10000
        for offset in range(-search_range, search_range):
            p_candidate = p_estimate + offset
            
            if not (p_candidate.bit_length() >= 510 and p_candidate.bit_length() <= 514):
                continue
                
            x_candidate = 2 * w * p_candidate - 1
            
            if not isPrime(x_candidate):
                continue
                
            if n % x_candidate == 0:
                remaining = n // x_candidate
                
                # Try to factor the remaining part
                factors = find_prime_factors(remaining)
                
                # Try different combinations of factors
                from itertools import combinations
                for i in range(1, len(factors) + 1):
                    for comb in combinations(factors, i):
                        p_test = 1
                        for f in comb:
                            p_test *= f
                            
                        if remaining % p_test == 0:
                            q_test = remaining // p_test
                            
                            if isPrime(p_test) and isPrime(q_test):
                                if p_test.bit_length() == 512 and q_test.bit_length() == 1024:
                                    print(f"Found potential factors!")
                                    print(f"p = {p_test}")
                                    print(f"q = {q_test}")
                                    print(f"x = {x_candidate}")
                                    
                                    # Verify the factorization
                                    if p_test * q_test * x_candidate == n:
                                        try:
                                            # Calculate phi
                                            phi = (p_test - 1) * (q_test - 1) * (x_candidate - 1)
                                            # Calculate d
                                            d = pow(e, -1, phi)
                                            # Decrypt
                                            m = pow(c, d, n)
                                            decrypted = long_to_bytes(m)
                                            
                                            # Check if result looks valid
                                            if all(32 <= b <= 126 for b in decrypted):
                                                print(f"Success! Decrypted message: {decrypted}")
                                                return decrypted
                                        except Exception as e:
                                            print(f"Decryption failed: {e}")
                                            continue

    return None

if __name__ == "__main__":
    result = solve_challenge()
    if result is None:
        print("Failed to find solution")
