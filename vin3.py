from sage.all import *
import sage.all as sage

# Given x-coordinates
xs = [
    127222731808447286384197097524849730324280912084690383123034174156693907296321941583008138816149304043198829099586978152639,
    540150767459876746741544981524050320567261340627105743010550795668800394677819357272612801849680099119164471834128771848184,
    378426912752589864658307848293724051252472266429208255456184007500868515338668653822829851730193370970777687937350186024739,
    114528622155057967694026934367142168000739167063266001591280862125480038107282641048998814104241182719055831758176542012114,
    322400405850331256663554456242498354334347017862265389196757152850674454034744292814021471167045908645361119988919752367867,
    496047308313146975448000924265615728665813401349451895964344399497579232646901690982051726266819379622021083585061713111901,
    339613985780778130822549050414603776860269549419836797423421156347303558845214120048926926114443864057942273222884788713615
]

def find_curve_parameters(xs):
    # Try different prime moduli around 256 bits
    for p_bits in range(255, 258):
        for p in sage.Primes()[2**p_bits:2**(p_bits+1)]:
            try:
                F = sage.GF(p)
                
                # Convert x-coordinates to field elements
                field_xs = [F(x) for x in xs]
                
                # Try to find y-coordinates for the first few points
                for a_test in range(-100, 100):  # Try some small values for a
                    for b_test in range(-100, 100):  # Try some small values for b
                        try:
                            E = sage.EllipticCurve(F, [a_test, b_test])
                            points = []
                            
                            # Try to lift x-coordinates to points
                            valid_curve = True
                            for x in field_xs:
                                try:
                                    # Try to find a point with this x-coordinate
                                    y_squared = x**3 + a_test*x + b_test
                                    if not sage.is_square(y_squared):
                                        valid_curve = False
                                        break
                                    y = sage.sqrt(y_squared)
                                    points.append(E(x, y))
                                except:
                                    valid_curve = False
                                    break
                            
                            if valid_curve and len(points) == len(xs):
                                # Check if points differ by G
                                G = E.gens()[0]
                                P = points[0]
                                
                                if all(points[i] == P + i*G for i in range(len(points))):
                                    # Found the curve! Now find private key
                                    k = discrete_log(P, G)
                                    print(f"Found curve parameters:")
                                    print(f"p = {p}")
                                    print(f"a = {a_test}")
                                    print(f"b = {b_test}")
                                    print(f"Private key = {k}")
                                    
                                    # Try to convert to flag
                                    try:
                                        from Crypto.Util.number import long_to_bytes
                                        flag = long_to_bytes(k)
                                        print(f"Flag: {flag}")
                                    except:
                                        print("Could not convert private key to flag")
                                    
                                    return p, a_test, b_test, k
                        except:
                            continue
            except:
                continue
    
    return None

if __name__ == "__main__":
    print("Starting search for curve parameters...")
    result = find_curve_parameters(xs)
    if not result:
        print("Could not find curve parameters")
