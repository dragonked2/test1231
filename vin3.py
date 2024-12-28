from ecdsa import ellipticcurve, SECP256k1
from ecdsa.ellipticcurve import Point
from Crypto.Util.number import bytes_to_long
import hashlib

# Elliptic curve parameters
a = -100
b = -39
p = 57896044618658097711785492504343953926634992332820282019728792003956564820063

# Set up the elliptic curve and the generator point
curve = ellipticcurve.CurveFp(p, a, b)

# Points given from the CTF
public_points = [
    127222731808447286384197097524849730324280912084690383123034174156693907296321941583008138816149304043198829099586978152639,
    540150767459876746741544981524050320567261340627105743010550795668800394677819357272612801849680099119164471834128771848184,
    378426912752589864658307848293724051252472266429208255456184007500868515338668653822829851730193370970777687937350186024739,
    114528622155057967694026934367142168000739167063266001591280862125480038107282641048998814104241182719055831758176542012114,
    322400405850331256663554456242498354334347017862265389196757152850674454034744292814021471167045908645361119988919752367867,
    496047308313146975448000924265615728665813401349451895964344399497579232646901690982051726266819379622021083585061713111901,
    339613985780778130822549050414603776860269549419836797423421156347303558845214120048926926114443864057942273222884788713615
]

# Generator point (G)
G = SECP256k1.generator

# Function to recover private key from the given public points
def solve_private_key(public_points, G, curve):
    x_coords = public_points  # Given x-coordinates of points P + i*G
    
    # Now we will try to brute force the private key by checking the results of G*private_key
    # Since the challenge hints at using 7 x-coordinates, we'll try brute force for small private keys (not realistic for large cases)
    
    for private_key in range(1, 100000):  # For simplicity, we are testing only up to 100000 (this is for small challenges)
        P = G * private_key  # Compute G*private_key
        if P.x() in x_coords:  # Check if the x-coordinate of G*private_key is one of the public points
            print(f"Found private key: {private_key}")
            return private_key

# Solve for the private key using the public points and generator G
solve_private_key(public_points, G, curve)
