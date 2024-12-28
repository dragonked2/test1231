# Import necessary SageMath libraries
from sage.all import *
from itertools import product
from Crypto.Util.number import long_to_bytes

# ================================
# User-Defined Parameters Section
# ================================

# Replace the following placeholders with actual values from the challenge

# 1. Elliptic Curve Parameters
p =  # Example: 0xFFFFFF... (a large prime number)
a =  # Coefficient 'a' in the elliptic curve equation
b =  # Coefficient 'b' in the elliptic curve equation

# 2. Generator Point Coordinates
G_x =  # X-coordinate of the generator point G
G_y =  # Y-coordinate of the generator point G

# 3. X-Coordinates of P, P+G, ..., P+6G
x_coords = [
    # x0, x1, x2, x3, x4, x5, x6
    # Example: 0x1234..., 0xABCD..., ..., 0x5678...
]

# ================================
# End of User-Defined Parameters
# ================================

# Define the elliptic curve
E = EllipticCurve(GF(p), [a, b])

# Define the generator point G
G = E(G_x, G_y)

# Function to find possible points from an x-coordinate
def find_points(x):
    """
    Given an x-coordinate, find the corresponding y-coordinates on the elliptic curve.
    Returns a list of Sage EllipticCurve points.
    """
    try:
        rhs = (x^3 + a*x + b) % p  # Compute y^2 = x^3 + ax + b mod p
        y = sqrt_mod(rhs, p)  # Compute square roots of y^2 modulo p

        if y is None:
            return []  # No valid y-coordinate found

        # Ensure y is an integer within the field
        y = Integer(y)

        # Return both possible points
        return [E(x, y), E(x, -y)]
    except Exception as e:
        print(f"Error finding points for x = {x}: {e}")
        return []

# Generate possible points for each x-coordinate
points_lists = []
for idx, x in enumerate(x_coords):
    pts = find_points(x)
    if not pts:
        print(f"No valid points found for x-coordinate at index {idx}: {x}")
    points_lists.append(pts)

# Check if any x-coordinate has no corresponding y-coordinate
if any(len(pts) == 0 for pts in points_lists):
    print("One or more x-coordinates do not correspond to any point on the curve.")
    exit()

# Generate all possible combinations of points (2^7 = 128)
all_combinations = list(product(*points_lists))
print(f"Total combinations to evaluate: {len(all_combinations)}")

# Function to attempt to solve for the private key (flag)
def solve_flag(combination, G, E):
    """
    Given a combination of points, attempt to solve for the scalar k such that P = kG.
    Returns the scalar k if successful, otherwise None.
    """
    try:
        # Assume the first point corresponds to P = kG
        P = combination[0]

        # Compute k using discrete logarithm
        k = E.log(P, G)

        # Verify that k is valid across all points in the combination
        for i, Q in enumerate(combination):
            expected_point = (k + i) * G
            if Q != expected_point:
                return None  # Inconsistent scalar k
        return k
    except:
        return None  # Discrete logarithm computation failed

# Iterate through all combinations to find the correct flag
for idx, combo in enumerate(all_combinations):
    if (idx + 1) % 10 == 0 or idx == 0:
        print(f"Evaluating combination {idx + 1}/{len(all_combinations)}")
    k = solve_flag(combo, G, E)
    if k is not None:
        try:
            # Convert the scalar k back to bytes to retrieve the flag
            flag_bytes = long_to_bytes(int(k))
            try:
                flag = flag_bytes.decode('utf-8')  # Attempt to decode as UTF-8
                print(f"\n[+] Flag Found: {flag}")
                exit()
            except UnicodeDecodeError:
                print(f"\n[+] Flag Found (bytes): {flag_bytes}")
                exit()
        except Exception as e:
            print(f"Error converting scalar to bytes: {e}")

print("\n[-] Flag not found in the given combinations.")
