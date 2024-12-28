from ecdsa import ellipticcurve
from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes
import math

# Custom elliptic curve parameters
a = -100
b = -39
p = 57896044618658097711785492504343953926634992332820282019728792003956564820063

# Define the elliptic curve
curve = ellipticcurve.CurveFp(p, a, b)

# Public x-coordinates
public_points = [
    127222731808447286384197097524849730324280912084690383123034174156693907296321941583008138816149304043198829099586978152639,
    540150767459876746741544981524050320567261340627105743010550795668800394677819357272612801849680099119164471834128771848184,
    378426912752589864658307848293724051252472266429208255456184007500868515338668653822829851730193370970777687937350186024739,
    114528622155057967694026934367142168000739167063266001591280862125480038107282641048998814104241182719055831758176542012114,
    322400405850331256663554456242498354334347017862265389196757152850674454034744292814021471167045908645361119988919752367867,
    496047308313146975448000924265615728665813401349451895964344399497579232646901690982051726266819379622021083585061713111901,
    339613985780778130822549050414603776860269549419836797423421156347303558845214120048926926114443864057942273222884788713615
]

# Function to check if an x-coordinate is valid on the curve and recover the y-coordinate
def recover_y_coordinates(x_coords, curve):
    points = []
    for x in x_coords:
        # Calculate y^2 = x^3 + ax + b (mod p)
        y2 = (x**3 + curve.a() * x + curve.b()) % curve.p()
        try:
            # Compute modular square root of y^2 (mod p)
            y = pow(y2, (curve.p() + 1) // 4, curve.p())
            points.append((x, y))
        except ValueError:
            print(f"x = {x} is not valid on the curve.")
    return points

# Recover y-coordinates for the given x-coordinates
points = recover_y_coordinates(public_points, curve)

# Display the recovered points
for point in points:
    print(f"Point: {point}")

# Analyze the relationships between points to deduce the private key
# Note: This step involves using properties of the elliptic curve and given points.
