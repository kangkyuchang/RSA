def main():
    inputNumbers = input("가장 큰 소수 2개를 입력해주세요. ex) 3,5 ")
    numbers = inputNumbers.split(",")
    num1 = int(numbers[0])
    num2 = int(numbers[1])
    if not isinstance(num1, int) or not isinstance(num2, int):
        return
    if not isPrime(num1) or not isPrime(num2):
        return
    n = num1 * num2
    print("소수1: " + str(num1))
    print("소수2: " + str(num2))
    print(n)
    PHI = phi(num1, num2)
    print("피함수: " + str(PHI))
    vaildNumber = createExponent(PHI)
    e = input(str(vaildNumber) + " 중 수 하나를 선택하여 암호화 지수를 생성하여 주세요. ")
    e = int(e)
    if not e in vaildNumber:
        return
    print("암호화 지수: " + str(e))
    solution = extendEuclid(e, PHI)
    d = -1
    for i in solution:
        tmp = (e*i)-1
        if tmp >= PHI and tmp % 20 == 0:
            d = i
    print("복호화 지수: " + str(d))

def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def phi(n1, n2):
    return (n1 - 1) * (n2 - 1)

def commonDivisor(num):
    numbers = []
    for i in range(2, num):
        if num % i == 0:
            numbers.append(i) 
    return numbers

def createExponent(num):
    cd = commonDivisor(num)
    numbers = []
    for i in range(2, num):
        numbers.append(i) 
    for i in cd:
        operand = int(num / i)
        for i2 in range(1, operand):
            if i*i2 in numbers:
                numbers.remove(i*i2)
        cd.remove(i)
        cd.remove(operand)

    return numbers

def extendEuclid(a, b):
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
        tmpx1 = x0 - (q*x1)
        tmpy1 = y0 - (q*y1)
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

main()