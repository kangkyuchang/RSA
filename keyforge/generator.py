import secrets
import base64
from math_utils.primes import is_prime
from math_utils.primes import trial_division
from math_utils.primes import miller_rabin
from math_utils.arithmetic import create_exponent
from math_utils.arithmetic import extend_euclid

def generate_manual_key(p, q, e):
    if not is_prime(p) or not is_prime(q):
        return [-1, e, 0, 0]
    status = 1
    N = p * q
    PHI = phi(p, q)
    vaildNumber = create_exponent(PHI)
    if not e in vaildNumber:
        e = secrets.choice(vaildNumber)
        status = 0
    x, y = extend_euclid(e, PHI)
    d = y % PHI
    if (e * d) % PHI != 1:
        d = x % PHI
        
    return [status, e, d, N]

def generate_auto_key():
    while True:
        prime1 = get_random_prime(1024)
        prime2 = get_random_prime(1024)
        if prime1 == prime2:
            continue
        N = prime1 * prime2
        PHI = phi(prime1, prime2)
        e = 65537
        if PHI % e == 0:
            continue
        x, y = extend_euclid(e, PHI)
        d = y % PHI
        if (e * d) % PHI != 1:
           d = x % PHI

        if (e * d) % PHI == 1:
            break
    return [e, d, N]

def get_random_prime(nbits=1024):
    while True:
        p = secrets.randbits(nbits)
        p |= (1 << (nbits - 1)) | 1

        if trial_division(p):
            continue

        if miller_rabin(p):
            return p
    
def phi(n1, n2):
    return (n1 - 1) * (n2 - 1)

def key_to_base64(number):
    byte_len = (number.bit_length() + 7) // 8
    key_bytes = number.to_bytes(byte_len, byteorder="big")
    return base64.b64encode(key_bytes).decode('utf-8')

def base64_to_key(key):
    key_data = base64.b64decode(key)
    return int.from_bytes(key_data, byteorder="big")