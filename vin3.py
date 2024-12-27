from Crypto.Util.number import isPrime, long_to_bytes
from math import isqrt

def solve_challenge():
    n = 18186672849609603331344182584568642941078893104802301217241028624469607021717197485036251613075846729705028441094100248337306406098776983108141004863456595015660485098203867670995838502297993710897784135087115777697925848407153788837657722171924264421550564295047937036911411846582733847201015164634546149603743246378710225407507435371659148999942913405493417037116587298256802831009824832360479040621348157491754407277404391337488226402711686156101028879269050800874367763551119682177453648890492731413760738825931684979379268401715029193518612541590846238434595210876468090976194627398214837801868969047036272502669215123
    e = 65537
    c = 1617999293557620724157535537778741335004656286655134597579706838690566178453141895621909480622070931381931296468696585541046188947144084107698620486576573164517733264644244665803523581927226503313545336021669824656871624111167113668644971950653103830443634752480477923970518891620296211614968804248580381104245404606917784407446279304488720323993268637887493503760075542578433642707326246816504761740168067216112150231996966168374619580811013034502620645288021335483574561758204631096791789272910596432850424873592013042090724982779979496197239647019869960002253384162472401724931485470355288814804233134786749608640103461

    # w is a small prime, we will test possible values in the range of 20-bit primes
    for w in range(2**19, 2**20):
        if not isPrime(w):
            continue

        print(f"Testing w = {w}")

        # Use integer math to avoid floating-point overflow and maintain precision
        p_approx = isqrt(n // (2 * w))

        # Try values around the estimated p
        for p_offset in range(-1000, 1000):
            p = p_approx + p_offset

            if not isPrime(p):
                continue

            if p.bit_length() != 512:
                continue

            x = 2 * w * p - 1

            if not isPrime(x):
                continue

            if n % p == 0 and n % x == 0:
                q = n // (p * x)

                if q.bit_length() == 1024 and isPrime(q):
                    print(f"Found potential solution!")
                    print(f"p = {p}")
                    print(f"q = {q}")
                    print(f"x = {x}")
                    print(f"w = {w}")

                    try:
                        # Calculate private key
                        phi = (p - 1) * (q - 1) * (x - 1)
                        d = pow(e, -1, phi)

                        # Decrypt the ciphertext
                        m = pow(c, d, n)
                        decrypted = long_to_bytes(m)

                        # Check for valid result
                        if b'flag' in decrypted or b'CTF' in decrypted:
                            print(f"Found valid solution: {decrypted}")
                            return decrypted

                    except Exception as ex:
                        print(f"Error during decryption: {ex}")
                        continue

    return None

if __name__ == "__main__":
    print("Starting RSA challenge solver...")
    result = solve_challenge()
    if result is None:
        print("Could not find valid solution")
    else:
        print(f"Final result: {result}")
