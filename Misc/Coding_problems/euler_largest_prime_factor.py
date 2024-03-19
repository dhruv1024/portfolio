input = 600851475143
#600851475143
divisor = 2
largest_multiple = 1
factors = []

def get_largest_factor(divisor, input):
    range = input
    while divisor < range:
        if input % divisor == 0:
            factors.append(divisor)
            factors.append(int(input/divisor))
        range = int(input/divisor)+1
        divisor += 1

def check_prime(factor):
    for divisor in range(2,factor-1):
        if factor % divisor == 0:
            return False
    return True

get_largest_factor(divisor, input)
for factor in factors:
    if check_prime(factor):
        if largest_multiple < factor:
            largest_multiple = factor

largest_multiple = input if largest_multiple == 1 else largest_multiple
print(factors)
print(largest_multiple)