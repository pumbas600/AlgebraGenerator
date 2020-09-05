import random
import math, time

brackets_left = 3
brackets_right = 2

is_integer_answer = True
maxX = 12
max_coefficient = 10
max_rhs_total = 45
chance_of_negative = 0.2
x = 0

rhs_total = 0
rhs = ''

def random_sign(n):
    return -n if random.random() < chance_of_negative else n

def generate_random_number(func, max_value):
    while True:
        rn = func(0, max_value)
        if rn != 0:
            return random_sign(rn)

def generate_x(integer_answer):
    if integer_answer:
        x = generate_random_number(random.randint, maxX)
    else:
        x = generate_random_number(random.uniform, maxX)
    return x


def get_display_number(n, with_sign=True):
    if n == 0:
        return 0

    if n == 1 or n == -1:
        if with_sign:
            return '+' if n > 0 else '-'
        return '' if n > 0 else '-'
    else:
        if with_sign:
            return f'+{n}' if n > 0 else str(n)
        return str(n)


def generate_rhs(brackets_right, x):
    rhs_total = 0
    rhs = ''
    for n in range(brackets_right):
        # c(ax + b)
        a = generate_random_number(random.randint, max_coefficient)
        b = generate_random_number(random.randint, max_coefficient)
        c = generate_random_number(random.randint, max_coefficient)

        rhs_total += c * (a * x + b)
        # Only add a space before the brackets if this is not the first set of brackets.
        rhs += (str(c) if n == 0 else f' {get_display_number(c)}') \
            + f'({get_display_number(a, False)}x {get_display_number(b)})'

    return rhs, rhs_total


def distribute_total(brackets, total):
    while True:
        random_distribution = [generate_random_number(random.uniform, 1) for _ in range(brackets)]
        # If by chance, the sum is 0, this will cause a divide by zero error, so we need to
        # regenerate the random numbers until their sum isn't 0.

        distributions_sum = sum(random_distribution)
        if distributions_sum != 0:
            break

    multiplier = total / distributions_sum
    distribution = []
    for n in random_distribution:
        rounded = round(n * multiplier)
        if rounded == 0:
            # print('rounded is 0')
            rounded = random_sign(1)
        distribution.append(rounded)

    # Check for rounding errors which may cause the total of the results
    # to not equal rhs_total
    sum_results = sum(distribution)
    if sum_results != total:
        # Add the difference to a random one of the results.
        while True:
            index = random.randint(0, brackets - 1)
            if distribution[index] + total - sum_results != 0:
                break
        distribution[index] += total - sum_results
        # print('Sum didnt equal total')
    return distribution


def find_factors(n):
    factors = [1, n]
    for x in range(2, int(math.ceil(abs(n / 2))) + 1):
        if n % x == 0:
            factors.append(int(x))
            factors.append(int(n / x))
    return factors


def generate_side(distributions, x):
    side = ''

    for n in range(len(distributions)):
        d = distributions[n]
        # c(ax + b)
        # print(d)
        factors = find_factors(d)
        c = random.choice(factors)
        if c == 0: print('c == 0')
        inside_brackets = d / c
        while True:
            a = generate_random_number(random.randint, max_coefficient)
            b = int(inside_brackets - a * x)
            if b != 0:
                break

        side += (get_display_number(c, False) if n == 0 else f' {get_display_number(c)}') \
            + f'({get_display_number(a, False)}x {get_display_number(b)})'
    return side


if __name__ == '__main__':
    if x == 0: x = generate_x(is_integer_answer)

    random.seed = time.time()
    rhs_total = generate_random_number(random.randint, max_rhs_total)
    rhs_distributions = distribute_total(brackets_right, rhs_total)
    rhs = generate_side(rhs_distributions, x)

    lhs_distributions = distribute_total(brackets_left, rhs_total)
    # print(lhs_distributions)
    lhs = generate_side(lhs_distributions, x)

    print(f'{lhs} = {rhs}')
    print(f'Answer is x = {x}')
    print(f'Seed is: {random.seed}')
