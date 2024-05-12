def main():
    inputNumbers = input("가장 큰 소수 2개를 입력해주세요. ex) 3,5")
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

def isPrime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def phi(n1, n2):
    return (n1 - 1) * (n2 - 1)

main()