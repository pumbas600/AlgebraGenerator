import math
import random
import time
import fractions

brackets_left = 2
brackets_right = 1

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

def generate_random_number(func, max_value, generate_sign=True):
    while True:
        rn = func(0, max_value)
        if rn != 0:
            return random_sign(rn) if generate_sign else rn

def generate_x(integer_answer):
    if integer_answer:
        x = generate_random_number(random.randint, maxX)
    else:
        x = generate_random_number(random.uniform, maxX)
    return x


def get_display_number(n, with_sign=True, show_one=False):
    if n == 0:
        return 0

    if n == 1 or n == -1:
        if with_sign:
            sign = '+' if n > 0 else '-'
            return sign + '1' if show_one else sign
        sign = '' if n > 0 else '-'
        return sign + '1' if show_one else sign
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
            + f'({get_display_number(a, False)}x {get_display_number(b, show_one=True)})'

    return rhs, rhs_total


def generate_random_distributions(n):

    # Distribution function is 0.75x^3 + 0.25, which gives values between -0.5 and 1 for values of x between
    # -1 and 1. This distribution causes most values to be grouped around 0.25, but most of the values are very similar.
    distribution_function = lambda x: 0.75 * x * x * x + 0.25
    random_distribution = [distribution_function(generate_random_number(random.uniform, 1, generate_sign=False)) for _ in range(n)]
    return random_distribution


def distribute_total(brackets, total):
    while True:
        random_distribution = generate_random_distributions(brackets)
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

    #TODO: Find infinite loop in below code snippet (up until the return)

    # Check for rounding errors which may cause the total of the results
    # to not equal rhs_total
    sum_results = sum(distribution)
    if sum_results != total:
        # Add the difference to the first valid distribution
        for i in range(len(distribution)):
            if distribution[i] + total - sum_results != 0:
                distribution[i] += total - sum_results
                break

            if i == len(distribution) - 1:
                # Cannot redistribute the total as it is, so try regenerating the distribution.
                distribution = distribute_total(brackets, total)
                # print('Cannot redistribute')

    return distribution


def find_factors(n):
    factors = [1]

    if isinstance(n, fractions.Fraction):
        pass

    else:
        factors.append(n)
        for x in range(2, int(math.ceil(abs(n / 2))) + 1):
            if n % x == 0:
                factors.append(int(x))
                factors.append(int(n / x))

    return factors

def decimal_to_fraction(n):
    return fractions.Fraction(n)

def generate_side(distributions, x):
    side = ''

    for n in range(len(distributions)):
        d = distributions[n]
        # c(ax + b)
        # print(d)
        factors = find_factors(d)
        c = random.choice(factors)

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
    random.seed = time.time()

    fraction = fractions.Fraction()
    for _ in range(25):
        x = generate_x(is_integer_answer)

        rhs_total = generate_random_number(random.randint, max_rhs_total)
        rhs_distributions = distribute_total(brackets_right, rhs_total)
        rhs = generate_side(rhs_distributions, x)

        lhs_distributions = distribute_total(brackets_left, rhs_total)
        # print(lhs_distributions, rhs_distributions)
        lhs = generate_side(lhs_distributions, x)

        print(f'{lhs} = {rhs}')
        # print(f'Answer is x = {x}')
        # print(f'Seed is: {random.seed}')
    print('Complete')

    #TODO: Fractions- https://cboard.cprogramming.com/c-programming/158102-program-convert-decimal-fraction.html