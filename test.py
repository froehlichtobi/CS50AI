import math

anzahl = int(input("show prime numbers up to: "))

def isPrime(n):
    if n <= 1:
        print(n)
        return False
    for i in range(2,int(math.sqrt(n)+1)):
        # prime numbers are only divisible by itself and 1
        if n % i == 0:
            return False
    print ("it's a prime number!: ", n)
    return True
              
for i in range(anzahl+1):
    isPrime(i)

with open("prime_numbers.txt", "w") as file:
    for num in range(anzahl + 1):
        if isPrime(num):
            file.write(f"{num}\n")