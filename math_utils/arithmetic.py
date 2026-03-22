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
        operand = num // i
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
        q = a // b
        r = a % b
        if r == 0:
            break
        # print("몫: " + str(q) + " 나머지: " + str(r))
        tmpx1 = x0 - (q * x1)
        tmpy1 = y0 - (q * y1)
        # print("x1: " + str(x0) + "-(" + str(q) + "*" + str(x1) + ")")
        # print("y1: " + str(y0) + "-(" + str(q) + "*" + str(y1) + ")")
        a = b
        b = r
        x0 = x1
        y0 = y1
        x1 = tmpx1
        y1 = tmpy1
    #     print("a: " + str(a) + ", b: " + str(b) + ", x0: " + str(x0) + ", y0: " + str(y0) + ", x1: " + str(x1) + ", y1: " + str(y1))
    # print("x: " + str(x1) + " y: " + str(y1))
    # print((max * x1) + (min * y1))
    return [x1, y1]