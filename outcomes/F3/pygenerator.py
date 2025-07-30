import slye_math as sm
import random
import math


def generate(**kwargs):
    def decimal_problem(how_many):
        # Create endpoints and points
        place_val = random.randint(2, 3)
        decimal_vals = place_val - 1
        a_str = sm.dec_string(-1 * decimal_vals, place_val, excl_last=[0, 8, 9])
        if len(a_str) == 1:
            a_str += '.0'
        distance = 1  # random.randint(1, 2)
        b_str = a_str[:-1] + str(int(a_str[-1]) + distance)
        a = float(a_str)
        b = float(b_str)
        increment = 10 ** (-1 * (decimal_vals + 1))
        step_1_xs = [a + n * increment for n in range(1, min(10, how_many + 1))]
        step_2_xs = [a + increment / 2 + n * increment for n in range(0, how_many - 9)]

        step_1_xs_formatted = list(map(lambda x: f'{x:.{decimal_vals + 1}f}', step_1_xs))
        step_2_xs_formatted = list(map(lambda x: f'{x:.{decimal_vals + 2}f}', step_2_xs))
        numbers_list = sorted(step_1_xs_formatted + step_2_xs_formatted)
        readable_numbers = sm.readable_list(numbers_list)

        return a, b, readable_numbers, decimal_vals, increment, step_1_xs, step_2_xs

    def fraction_problem(how_many, hard=True):
        if hard:
            a_denom = random.randint(3, 7)
            a_num = random.choice(sm.rel_primes(a_denom))
            b_denom = a_denom + 1
            b_num = random.choice([a_num, a_num + 1])
            while math.gcd(b_num, b_denom) != 1:
                b_denom += 1
        else:
            a_denom = b_denom = random.randint(3, 9)
            a_num, b_num = sm.samples(sm.rel_primes(a_denom), k=2)

        if a_num / a_denom > b_num / b_denom:
            a_num, b_num = b_num, a_num
            a_denom, b_denom = b_denom, a_denom
        a = f'\\dfrac{{{a_num}}}{{{a_denom}}}'
        b = f'\\dfrac{{{b_num}}}{{{b_denom}}}'

        ten_multipliers = [10, 100, 1000]
        if how_many >= 10:
            ten_multipliers.remove(10)

        ten_multiplier = random.choice(ten_multipliers)

        if hard:
            a_multiplier = b_denom * ten_multiplier
            b_multiplier = a_denom * ten_multiplier
        else:
            a_multiplier = b_multiplier = ten_multiplier

        a_num = a_num * a_multiplier
        a_denom = a_denom * a_multiplier
        b_num = b_num * b_multiplier
        b_denom = b_denom * b_multiplier

        numerators = sm.samples(list(range(a_num + 1, b_num)), k=how_many)
        numerators.sort()
        tex_sep = '{,}'
        numbers = map(lambda n: f'\\dfrac{{{n:,}}}{{{b_denom:,}}}'.replace(',', tex_sep), numerators)
        numbers_str = sm.readable_list(numbers)
        numbers_str = numbers_str.replace('and', '\\text{ and }')

        return a, b, numbers_str

    p1_how_many = random.randint(10, 14)
    p1_a, p1_b, p1_numbers, p1_decimal_vals, p1_increment, p1_1_xs, p1_2_xs = decimal_problem(p1_how_many)
    num_line_directions = f'Graph the given numbers and the additional {p1_how_many} numbers accurately on the number line'

    p2_how_many = random.randint(7, 12)
    p2_a, p2_b, p2_numbers = fraction_problem(p2_how_many)

    expl_how_many = random.choice(['1,000', '10,000', '100,000'])

    return {
        'p1_how_many': p1_how_many,
        'p1_a': p1_a,
        'p1_b': p1_b,
        'p1_numbers': p1_numbers,
        'p1_decimal_vals': p1_decimal_vals,
        'p1_increment': p1_increment,
        'p1_1_xs': p1_1_xs,
        'p1_2_xs': p1_2_xs,
        'num_line_directions': num_line_directions,
        'p2_how_many': p2_how_many,
        'p2_a': p2_a,
        'p2_b': p2_b,
        'p2_numbers': p2_numbers,
        'expl_how_many': expl_how_many
    }
