from Crypto.Util.number import isPrime, long_to_bytes
from math import gcd

def alternative_solve():
    n = 18186672849609603331344182584568642941078893104802301217241028624469607021717197485036251613075846729705028441094100248337306406098776983108141004863456595015660485098203867670995838502297993710897784135087115777697925848407153788837657722171924264421550564295047937036911411846582733847201015164634546149603743246378710225407507435371659148999942913405493417037116587298256802831009824832360479040621348157491754407277404391337488226402711686156101028879269050800874367763551119682177453648890492731413760738825931684979379268401715029193518612541590846238434595210876468090976194627398214837801868969047036272502669215123
    e = 65537
    c = 1617999293557620724157535537778741335004656286655134597579706838690566178453141895621909480622070931381931296468696585541046188947144084107698620486576573164517733264644244665803523581927226503313545336021669824656871624111167113668644971950653103830443634752480477923970518891620296211614968804248580381104245404606917784407446279304488720323993268637887493503760075542578433642707326246816504761740168067216112150231996966168374619580811013034502620645288021335483574561758204631096791789272910596432850424873592013042090724982779979496197239647019869960002253384162472401724931485470355288814804233134786749608640103461

    # Since x = 2wp - 1, we know that x ≡ -1 (mod p)
    # This means n ≡ 0 (mod p) and n ≡ -q (mod x)
    
    for w in range(2**19, 2**20):
        if not isPrime(w):
            continue
            
        print(f"Alternative approach - trying w = {w}")
        
        # Try to find potential values of p
        # Since p is approximately n^(1/3), we can try values around this range
        approx_p = int(n ** (1/3))
        
        for p_candidate in range(max(2, approx_p - 10000), approx_p + 10000):
            if not isPrime(p_candidate):
                continue
                
            x = 2 * w * p_candidate - 1
            if not isPrime(x):
                continue
                
            if n % p_candidate == 0 and n % x == 0:
                q_candidate = n // (p_candidate * x)
                
                if isPrime(q_candidate):
                    print(f"Found potential factors:")
                    print(f"p = {p_candidate}")
                    print(f"q = {q_candidate}")
                    print(f"x = {x}")
                    
                    try:
                        phi = (p_candidate - 1) * (q_candidate - 1) * (x - 1)
                        d = pow(e, -1, phi)
                        m = pow(c, d, n)
                        decrypted = long_to_bytes(m)
                        
                        if all(32 <= b <= 126 for b in decrypted):
                            print(f"Decrypted message: {decrypted}")
                            return decrypted
                            
                    except Exception as e:
                        print(f"Error during decryption: {e}")
                        continue
    
    return None

if __name__ == "__main__":
    print("Trying alternative approach...")
    result = alternative_solve()
    if result is None:
        print("Alternative approach failed as well.")
