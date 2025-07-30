import slye_math as sm
import random
import math
from fractions import Fraction


def generate(**kwargs):
    factors_dict = {
        1: {'divisors': [1],
            'multiples': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
            'relative_primes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                24, 25],
            'shares_divisors': []},
        2: {'divisors': [1, 2],
            'multiples': [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
            'relative_primes': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
            'shares_divisors': []},
        3: {'divisors': [1, 3],
            'multiples': [6, 9, 12, 15, 18, 21, 24],
            'relative_primes': [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25],
            'shares_divisors': []},
        4: {'divisors': [1, 2, 4],
            'multiples': [8, 12, 16, 20, 24],
            'relative_primes': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
            'shares_divisors': [6, 10, 14, 18, 22]},
        5: {'divisors': [1, 5],
            'multiples': [10, 15, 20, 25],
            'relative_primes': [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24],
            'shares_divisors': []},
        6: {'divisors': [1, 2, 3, 6],
            'multiples': [12, 18, 24],
            'relative_primes': [1, 5, 7, 11, 13, 17, 19, 23, 25],
            'shares_divisors': [4, 8, 9, 10, 14, 15, 16, 20, 21, 22]},
        7: {'divisors': [1, 7],
            'multiples': [14, 21],
            'relative_primes': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25],
            'shares_divisors': []},
        8: {'divisors': [1, 2, 4, 8],
            'multiples': [16, 24],
            'relative_primes': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
            'shares_divisors': [6, 10, 12, 14, 18, 20, 22]},
        9: {'divisors': [1, 3, 9],
            'multiples': [18],
            'relative_primes': [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25],
            'shares_divisors': [6, 12, 15, 21, 24]},
        10: {'divisors': [1, 2, 5, 10],
             'multiples': [20],
             'relative_primes': [1, 3, 7, 9, 11, 13, 17, 19, 21, 23],
             'shares_divisors': [4, 6, 8, 12, 14, 15, 16, 18, 22, 24, 25]},
        11: {'divisors': [1, 11],
             'multiples': [22],
             'relative_primes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24,
                                 25],
             'shares_divisors': []},
        12: {'divisors': [1, 2, 3, 4, 6, 12],
             'multiples': [24],
             'relative_primes': [1, 5, 7, 11, 13, 17, 19, 23, 25],
             'shares_divisors': [8, 9, 10, 14, 15, 16, 18, 20, 21, 22]},
        13: {'divisors': [1, 13],
             'multiples': [],
             'relative_primes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                                 25],
             'shares_divisors': []},
        14: {'divisors': [1, 2, 7, 14],
             'multiples': [],
             'relative_primes': [1, 3, 5, 9, 11, 13, 15, 17, 19, 23, 25],
             'shares_divisors': [4, 6, 8, 10, 12, 16, 18, 20, 21, 22, 24]},
        15: {'divisors': [1, 3, 5, 15],
             'multiples': [],
             'relative_primes': [1, 2, 4, 7, 8, 11, 13, 14, 16, 17, 19, 22, 23],
             'shares_divisors': [6, 9, 10, 12, 18, 20, 21, 24, 25]},
        16: {'divisors': [1, 2, 4, 8, 16],
             'multiples': [],
             'relative_primes': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
             'shares_divisors': [6, 10, 12, 14, 18, 20, 22, 24]},
        17: {'divisors': [1, 17],
             'multiples': [],
             'relative_primes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24,
                                 25],
             'shares_divisors': []},
        18: {'divisors': [1, 2, 3, 6, 9, 18],
             'multiples': [],
             'relative_primes': [1, 5, 7, 11, 13, 17, 19, 23, 25],
             'shares_divisors': [4, 8, 10, 12, 14, 15, 16, 20, 21, 22, 24]},
        19: {'divisors': [1, 19],
             'multiples': [],
             'relative_primes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24,
                                 25],
             'shares_divisors': []},
        20: {'divisors': [1, 2, 4, 5, 10, 20],
             'multiples': [],
             'relative_primes': [1, 3, 7, 9, 11, 13, 17, 19, 21, 23],
             'shares_divisors': [6, 8, 12, 14, 15, 16, 18, 22, 24, 25]},
        21: {'divisors': [1, 3, 7, 21],
             'multiples': [],
             'relative_primes': [1, 2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20, 22, 23, 25],
             'shares_divisors': [6, 9, 12, 14, 15, 18, 24]},
        22: {'divisors': [1, 2, 11, 22],
             'multiples': [],
             'relative_primes': [1, 3, 5, 7, 9, 13, 15, 17, 19, 21, 23, 25],
             'shares_divisors': [4, 6, 8, 10, 12, 14, 16, 18, 20, 24]},
        23: {'divisors': [1, 23],
             'multiples': [],
             'relative_primes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
                                 25],
             'shares_divisors': []},
        24: {'divisors': [1, 2, 3, 4, 6, 8, 12, 24],
             'multiples': [],
             'relative_primes': [1, 5, 7, 11, 13, 17, 19, 23, 25],
             'shares_divisors': [9, 10, 14, 15, 16, 18, 20, 21, 22]},
        25: {'divisors': [1, 5, 25],
             'multiples': [],
             'relative_primes': [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24],
             'shares_divisors': [10, 15, 20]}
    }

    mult_div = True

    def add_prob():
        # w1 a/b + w2 c/d
        b = random.randint(2, 15)
        a = random.randint(math.ceil(b / 2), b - 1)
        possible_ds = list(set(range(2, 15)).difference(factors_dict[b]['divisors'] + factors_dict[b]['multiples']))
        d = random.choice(possible_ds)
        c = random.randint(math.ceil(d - d * a / b), d - 1)
        w1 = random.randint(2, 6)
        w2 = random.randint(2, 6)
        a, b = Fraction(a, b).as_integer_ratio()
        c, d = Fraction(c, d).as_integer_ratio()
        ans = sm.mixed_number(w1 + Fraction(a, b) + w2 + Fraction(c, d))
        return {
            'whole_1': w1,
            'num_1': a,
            'denom_1': b,
            'op': '+',
            'whole_2': w2,
            'num_2': c,
            'denom_2': d,
            'whole_ans': ans[0],
            'num_ans': ans[1],
            'denom_ans': ans[2]
        }

    def sub_prob():
        # w1 a/b - w2 c/d
        b = int(random.randint(2, 15))
        a = int(random.randint(1, b - 1))
        possible_ds = list(set(range(2, 15)).difference(factors_dict[b]['divisors'] + factors_dict[b]['multiples']))
        d = int(random.choice(possible_ds))
        c = int(random.choice([x for x in factors_dict[d]['relative_primes'] if x < d]))
        if a / b > c / d:
            a, b, c, d = c, d, a, b
        w1 = random.randint(2, 9)
        w2 = w1 - random.randint(1, w1 - 1)

        a, b = Fraction(a, b).as_integer_ratio()
        c, d = Fraction(c, d).as_integer_ratio()
        ans = sm.mixed_number(w1 + Fraction(a, b) - (w2 + Fraction(c, d)))
        return {
            'whole_1': w1,
            'num_1': a,
            'denom_1': b,
            'op': '-',
            'whole_2': w2,
            'num_2': c,
            'denom_2': d,
            'whole_ans': ans[0] if ans[0] != 0 else '',
            'num_ans': ans[1],
            'denom_ans': ans[2]
        }

    def mult_div_prob():
        # w1 a/b * or / w2 c/d
        b = int(random.randint(2, 15))
        a = int(random.choice([x for x in factors_dict[b]['relative_primes'] if x < b]))
        d = int(random.randint(2, 15))
        c = int(random.choice([x for x in factors_dict[d]['relative_primes'] if x < d]))
        w1 = random.randint(2, 6)
        w2 = w1 - random.randint(1, w1 - 1)

        a, b = Fraction(a, b).as_integer_ratio()
        c, d = Fraction(c, d).as_integer_ratio()
        op = random.choice(['*', '/'])
        if op == '*':
            ans = sm.mixed_number((w1 + Fraction(a, b)) * (w2 + Fraction(c, d)))
        else:
            ans = sm.mixed_number((w1 + Fraction(a, b)) / (w2 + Fraction(c, d)))
        op = '\\times' if op == '*' else '\\div'
        return {
            'whole_1': w1,
            'num_1': a,
            'denom_1': b,
            'op': op,
            'whole_2': w2,
            'num_2': c,
            'denom_2': d,
            'whole_ans': ans[0] if ans[0] != 0 else '',
            'num_ans': ans[1],
            'denom_ans': ans[2]
        }

    add_sub_probs = [add_prob, sub_prob]
    random.shuffle(add_sub_probs)
    add_sub_prob_1, add_sub_prob_2 = add_sub_probs

    p1_data = add_sub_prob_1()
    prob_1 = (f"{p1_data['whole_1']} \\frac{{{p1_data['num_1']}}}{{{p1_data['denom_1']}}} {p1_data['op']} "
              f"{p1_data['whole_2']} \\frac{{{p1_data['num_2']}}}{{{p1_data['denom_2']}}}")
    ans_1 = f"{p1_data['whole_ans']} \\frac{{{p1_data['num_ans']}}}{{{p1_data['denom_ans']}}}"

    if mult_div == True:
        p2_data = mult_div_prob()
    else:
        p2_data = add_sub_prob_2
    prob_2 = (f"{p2_data['whole_1']} \\frac{{{p2_data['num_1']}}}{{{p2_data['denom_1']}}} {p2_data['op']} "
              f"{p2_data['whole_2']} \\frac{{{p2_data['num_2']}}}{{{p2_data['denom_2']}}}")
    ans_2 = f"{p2_data['whole_ans']} \\frac{{{p2_data['num_ans']}}}{{{p2_data['denom_ans']}}}"

    return {
        'prob_1': prob_1,
        'ans_1': ans_1,
        'prob_2': prob_2,
        'ans_2': ans_2
    }
