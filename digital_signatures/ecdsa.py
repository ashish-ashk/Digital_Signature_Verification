import hashlib
import random
import os

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

class EllipticCurve:
    def __init__(self, a, b, p, G, n, h):
        self.a = a
        self.b = b
        self.p = p
        self.G = G  # Generator point
        self.n = n  # Order of G
        self.h = h  # Cofactor

    def point_add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        if P == Q:
            return self.point_double(P)
        if P.x == Q.x:
            return None  # Point at infinity
        m = ((Q.y - P.y) * pow(Q.x - P.x, -1, self.p)) % self.p
        x = (m**2 - P.x - Q.x) % self.p
        y = (m * (P.x - x) - P.y) % self.p
        return Point(x, y)

    def point_double(self, P):
        if P is None:
            return None
        m = ((3 * P.x**2 + self.a) * pow(2 * P.y, -1, self.p)) % self.p
        x = (m**2 - 2 * P.x) % self.p
        y = (m * (P.x - x) - P.y) % self.p
        return Point(x, y)

    def scalar_multiply(self, k, P):
        Q = None
        for i in bin(k)[2:]:
            Q = self.point_double(Q)
            if i == '1':
                Q = self.point_add(Q, P)
        return Q

    def is_on_curve(self, P):
        return (P.y**2 - P.x**3 - self.a * P.x - self.b) % self.p == 0

class ECDSA:
    def __init__(self, curve):
        self.curve = curve

    def generate_keypair(self):
        private_key = random.randint(1, self.curve.n - 1)
        public_key = self.curve.scalar_multiply(private_key, self.curve.G)
        return private_key, public_key

    def sign(self, message, private_key):
        z = int.from_bytes(hashlib.sha256(message.encode()).digest(), 'big')
        while True:
            k = random.randint(1, self.curve.n - 1)
            R = self.curve.scalar_multiply(k, self.curve.G)
            r = R.x % self.curve.n
            if r == 0:
                continue
            s = (pow(k, -1, self.curve.n) * (z + r * private_key)) % self.curve.n
            if s == 0:
                continue
            return r, s

    def verify(self, message, signature, public_key):
        r, s = signature
        if not (1 <= r < self.curve.n and 1 <= s < self.curve.n):
            return False
        z = int.from_bytes(hashlib.sha256(message.encode()).digest(), 'big')
        w = pow(s, -1, self.curve.n)
        u1 = (z * w) % self.curve.n
        u2 = (r * w) % self.curve.n
        P = self.curve.point_add(
            self.curve.scalar_multiply(u1, self.curve.G),
            self.curve.scalar_multiply(u2, public_key)
        )
        if P is None:
            return False
        return r == P.x % self.curve.n

def initialize_curve():
    # secp256k1 parameters
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    h = 1
    G = Point(Gx, Gy)
    return EllipticCurve(a, b, p, G, n, h)

# Example usage
if __name__ == "__main__":
    curve = initialize_curve()
    ecdsa = ECDSA(curve)

    # Generate key pair
    private_key, public_key = ecdsa.generate_keypair()
    print(f"Private key: {private_key}")
    print(f"Public key: {public_key}")

    # Sign a message
    message = "Hello, ECDSA!"
    signature = ecdsa.sign(message, private_key)
    print(f"Signature: {signature}")

    # Verify the signature
    is_valid = ecdsa.verify(message, signature, public_key)
    print(f"Signature is valid: {is_valid}")