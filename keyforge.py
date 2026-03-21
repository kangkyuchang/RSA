import secrets
import random

def main():
    inputNumbers = input("가장 큰 소수 2개를 입력해주세요. ex) 3,5 ")
    numbers = inputNumbers.split(",")
    num1 = int(numbers[0])
    num2 = int(numbers[1])
    # if not isinstance(num1, int) or not isinstance(num2, int):
    #     return
    if not is_prime(num1) or not is_prime(num2):
        return
    N = num1 * num2
    print("소수1: " + str(num1))
    print("소수2: " + str(num2))
    print("N: " + str(N))
    PHI = phi(num1, num2)
    print("피함수: " + str(PHI))
    vaildNumber = create_exponent(PHI)
    e = input(str(vaildNumber) + " 중 하나를 선택하여 암호화 지수를 생성하여 주세요. ")
    e = int(e)
    if not e in vaildNumber:
        return
    print("암호화 지수: " + str(e))
    solution = extend_euclid(e, PHI)
    d = -1
    for i in solution:
        if i < 0:
            i += PHI
        tmp = (e * i) -1
        if tmp >= PHI and tmp % PHI == 0:
            d = i
    print("복호화 지수: " + str(d))

def generate_auto_key():
    prime1 = get_random_prime(1024)
    prime2 = get_random_prime(1024)
    while prime1 == prime2:
        prime2 = get_random_prime(1024)
    N = prime1 * prime2
    PHI = phi(prime1, prime1)
    vaildNumber = create_exponent(PHI)
    e = int(vaildNumber[random.randint(0, len(vaildNumber) - 1)])
    solution = extend_euclid(e, PHI)
    d = -1
    for i in solution:
        if i < 0:
            i += PHI
        tmp = (e * i) -1
        if tmp >= PHI and tmp % PHI == 0:
            d = i
    return [e, d, N]

def is_even(n):
    return pow(n, 1, 2) == 0

def trial_division(n):
    prime_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                  101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                  211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 
                  307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
                  401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
                  503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
                  601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
                  701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
                  809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
                  907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    
    for prime in prime_list:
        if pow(n, 1, prime) == 0:
            return True
    
    return False

def miller_rabin(n):
    base_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                  101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173]
    s = 0
    div = n - 1
    while div % 2 == 0:
        div = div // 2
        s += 1
    d = (n - 1) // (2 ** s)
    if pow(2, d, n) == 1:
        return True
    for base in  base_list:
        value = pow(base, d, n)
        for _ in range(0, s):
            # value = pow(base, (2 ** i) * d, n)
            value = pow(value, 2, n)
            if value == n - 1:
                return True
    return False

# PHI 함수의 의미가 자연수 n에 대해 n보다 작으면서 n과 서로소인 자연수의 개수를 정의

def is_prime(n):
    if n <= 1:
        return False
    if is_even(n):
        return False
    return miller_rabin(n)

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

def common_divisor(num):
    numbers = []
    for i in range(2, num):
        if num % i == 0:
            numbers.append(i) 
    return numbers

def create_exponent(num):
    cd = common_divisor(num)
    numbers = []
    for i in range(2, num):
        numbers.append(i) 
    for i in cd:
        operand = int(num / i)
        for i2 in range(1, operand):
            mul = i * i2
            if mul in numbers:
                numbers.remove(mul)
        cd.remove(operand)
    return numbers

def extend_euclid(a, b):
    x0 = 1
    y0 = 0
    x1 = 0
    y1 = 1
    if a < b:
        tmp = a
        a = b
        b = tmp
    # max = a
    # min = b
    while True:
        q = int(a / b)
        r = a % b
        if r == 0:
            break
        print("몫: " + str(q) + " 나머지: " + str(r))
        tmpx1 = x0 - (q * x1)
        tmpy1 = y0 - (q * y1)
        print("x1: " + str(x0) + "-(" + str(q) + "*" + str(x1) + ")")
        print("y1: " + str(y0) + "-(" + str(q) + "*" + str(y1) + ")")
        a = b
        b = r
        x0 = x1
        y0 = y1
        x1 = tmpx1
        y1 = tmpy1
        print("a: " + str(a) + ", b: " + str(b) + ", x0: " + str(x0) + ", y0: " + str(y0) + ", x1: " + str(x1) + ", y1: " + str(y1))
    print("x: " + str(x1) + " y: " + str(y1))
    # print((max * x1) + (min * y1))
    return [x1, y1]

print(get_random_prime(1024))