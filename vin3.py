from Crypto.Util.number import isPrime, long_to_bytes
from math import gcd

def solve_challenge():
    n = 18186672849609603331344182584568642941078893104802301217241028624469607021717197485036251613075846729705028441094100248337306406098776983108141004863456595015660485098203867670995838502297993710897784135087115777697925848407153788837657722171924264421550564295047937036911411846582733847201015164634546149603743246378710225407507435371659148999942913405493417037116587298256802831009824832360479040621348157491754407277404391337488226402711686156101028879269050800874367763551119682177453648890492731413760738825931684979379268401715029193518612541590846238434595210876468090976194627398214837801868969047036272502669215123
    e = 65537
    c = 1617999293557620724157535537778741335004656286655134597579706838690566178453141895621909480622070931381931296468696585541046188947144084107698620486576573164517733264644244665803523581927226503313545336021669824656871624111167113668644971950653103830443634752480477923970518891620296211614968804248580381104245404606917784407446279304488720323993268637887493503760075542578433642707326246816504761740168067216112150231996966168374619580811013034502620645288021335483574561758204631096791789272910596432850424873592013042090724982779979496197239647019869960002253384162472401724931485470355288814804233134786749608640103461

    # Since w is 20-bit prime, we can try all possibilities
    for w in range(2**19, 2**20):
        if not isPrime(w):
            continue
            
        # Try to factor n using the relationship x = 2wp - 1
        # This means n = p * q * (2wp - 1)
        # Let's try to find p using this relationship
        
        # If p divides n, then p should also divide (n + q*x)
        # We can use this to find potential values of p
        
        potential_p = n % w
        if potential_p == 0:
            p_candidate = n // w
            if isPrime(p_candidate):
                p = p_candidate
                # Found p, now we can find q and x
                x = (2 * w * p - 1)
                if n % x == 0:
                    remaining = n // x
                    # Try to factor remaining into p and q
                    for i in range(2, int(remaining**0.5) + 1):
                        if remaining % i == 0:
                            potential_q = remaining // i
                            if isPrime(potential_q) and isPrime(i):
                                # We've found our factors!
                                p, q = i, potential_q
                                # Calculate private key d
                                phi = (p-1) * (q-1) * (x-1)
                                d = pow(e, -1, phi)
                                # Decrypt the message
                                m = pow(c, d, n)
                                try:
                                    return long_to_bytes(m)
                                except:
                                    continue

result = solve_challenge()
print(f"Decrypted message: {result}")