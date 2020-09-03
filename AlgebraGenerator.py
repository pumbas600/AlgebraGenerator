import random

brackets_left = 2
brackets_right = 1

is_integer_answer = True
minX = -20
maxX = 20

min_coefficient = -10
max_coefficient = 10

x = 0

rhs_total = 0
rhs = ''


def generate_x(integer_answer):
    if integer_answer:
        x = random.randint(minX, maxX)
    else:
        x = random.randrange(minX, maxX)
    return x


def get_display_number(n, with_sign=True):
    if n == 1:
        if with_sign:
            return '+' if n > 0 else '-'
        return '' if n > 0 else str(n)
    else:
        if with_sign:
            return f'+{n}' if n > 0 else str(n)
        return str(n)


def generate_rhs(brackets_right, x):
    rhs_total = 0
    rhs = ''
    for n in range(brackets_right):
        # c(ax + b)
        a = random.randint(min_coefficient, max_coefficient)
        b = random.randint(min_coefficient, max_coefficient)
        c = random.randint(min_coefficient, max_coefficient)

        rhs_total += c * (a * x + b)
        # Only add a space before the brackets if this is not the first set of brackets.
        rhs += (str(c) if n == 0 else f' {get_display_number(c)}') \
            + f'({get_display_number(a, False)}x {get_display_number(b)})'

    return rhs, rhs_total


def distribute_total(brackets_left, rhs_total):
    while True:
        random_distribution = []
        # If by chance, the sum is 0, this will cause a divide by zero error, so we need to
        # regenerate the random numbers until their sum isn't 0.

        for _ in range(brackets_left):
            while True:
                # Distribute more towards positive numbers
                rd = random.uniform(-0.5, 1)
                if rd != 0:
                    random_distribution.append(rd)
                    break

        distributions_sum = sum(random_distribution)
        if distributions_sum != 0:
            break

    multiplier = rhs_total / distributions_sum

    distribution = [round(n * multiplier) for n in random_distribution]

    # Check for rounding errors which may cause the total of the results
    # to not equal rhs_total
    sum_results = sum(distribution)
    if sum_results != rhs_total:
        # Add the difference to a random one of the results.
        index = random.randint(0, brackets_left - 1)
        distribution[index] += rhs_total - sum_results
        print('Sum didnt equal total')
    return distribution


def find_factors(n):
    factors = []
    for x in range(1, int(abs(n / 2)) + 1):
        if n % x == 0:
            factors.append(x)
            factors.append(n / x)
    return factors


def generate_lhs(distributions, x):
    lhs = ''

    for n in range(len(distributions)):
        d = distributions[n]
        # c(ax + b)
        # print(d)
        factors = find_factors(d)
        c = int(random.choice(factors))

        inside_brackets = d / c
        a = random.randint(min_coefficient, max_coefficient)
        b = int(inside_brackets - a * x)
        lhs += (str(c) if n == 0 else f' {get_display_number(c)}') \
            + f'({get_display_number(a, False)}x {get_display_number(b)})'
    return lhs


if __name__ == '__main__':
    if x == 0: x = generate_x(is_integer_answer)

    rhs, rhs_total = generate_rhs(brackets_right, x)
    distributions = distribute_total(brackets_left, rhs_total)
    lhs = generate_lhs(distributions, x)

    print(f'{lhs} = {rhs}')
    print(f'Answer is x = {x}')
