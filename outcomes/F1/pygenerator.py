import slye_math as sm
import random
from fractions import Fraction


def generate(**kwargs):
    primes = [2, 3, 5, 7, 11]
    primes_wts = [0.3, 0.25, 0.2, 0.125, 0.125]

    def get_factor(prime_cap=13):
        available_primes = [x for x in primes if x < prime_cap]
        available_primes_wts = primes_wts[:len(available_primes)]
        factor = random.choices(available_primes, available_primes_wts, k=1)[0]
        return factor

    # If editing the possible denominators, you may need to adjust this dictionary first. Can generate with py file.
    small_rel_primes = {
        2: [1],
        3: [1, 2],
        4: [1, 3],
        5: [1, 2, 3, 4],
        6: [1, 5],
        7: [1, 2, 3, 4, 5, 6],
        8: [1, 3, 5, 7],
        9: [1, 2, 4, 5, 7, 8],
        10: [1, 3, 7, 9],
        11: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        12: [1, 5, 7, 11],
        13: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        14: [1, 3, 5, 9, 11, 13],
        15: [1, 2, 4, 7, 8, 11, 13, 14]
    }

    # Part (a): Simplifying Fractions

    simplify_ans_denom = random.choice(list(range(3, 16)))
    simplify_ans_num = random.choice(small_rel_primes[simplify_ans_denom])
    simplify_ans = f'\\dfrac{{{simplify_ans_num}}}{{{simplify_ans_denom}}}'

    simplify_prob_denom = simplify_ans_denom
    simplify_prob_num = simplify_ans_num

    factors_list = []
    max_factors = random.choice(list(range(4, 7)))

    while True:
        f = get_factor()
        if simplify_prob_denom * f > 650 or len(factors_list) == max_factors:
            break
        else:
            factors_list.append(f)
            simplify_prob_denom = simplify_prob_denom * f
            simplify_prob_num = simplify_prob_num * f

    factors_list.sort()

    factors_sequence = sm.readable_list(factors_list)

    simplify_prob = f'\\dfrac{{{simplify_prob_num}}}{{{simplify_prob_denom}}}'

    # Part (b): Converting between improper fractions and mixed numbers

    convert_type = random.choice(['a mixed number', 'an improper fraction'])

    convert_prob_denom = random.choice(list(range(3, 16)))
    convert_prob_num = random.choice(small_rel_primes[convert_prob_denom])
    convert_prob_whole = random.choice(list(range(2, 9)))

    convert_prob_mixed = f'{convert_prob_whole}\\frac{{{convert_prob_num}}}{{{convert_prob_denom}}}'
    convert_prob_improper = (f'\\dfrac{{{convert_prob_whole * convert_prob_denom + convert_prob_num}}}'
                             f'{{{convert_prob_denom}}}')

    if convert_type == 'a mixed number':
        convert_ans = convert_prob_mixed
        convert_prob = convert_prob_improper
    else:
        convert_ans = convert_prob_improper
        convert_prob = convert_prob_mixed

    # Part (c): Checking Fraction Equivalence

    equivalent = random.choice([True, False])

    equiv_ans_b = random.choice(list(range(3, 16)))
    equiv_ans_a = random.choice(small_rel_primes[equiv_ans_b])
    equiv_prob_b = equiv_ans_b
    equiv_prob_a = equiv_ans_a

    multipliers_list = []
    denom_cap = 200 if equivalent is True else 100

    while True:
        f = get_factor()
        if equiv_prob_b * f > denom_cap:
            break
        else:
            multipliers_list.append(f)
            equiv_prob_b = equiv_prob_b * f
            equiv_prob_a = equiv_prob_a * f

    ab_multiplier = equiv_prob_b // equiv_ans_b

    if equivalent:
        equiv_ans_d = equiv_ans_b
        equiv_ans_c = equiv_ans_a
        cd_multiplier_offsets = list(range(-4, 5))
        cd_multiplier_offsets.remove(0)
        cd_multiplier = ab_multiplier + random.choice(cd_multiplier_offsets)
        equiv_prob_d = equiv_ans_d * cd_multiplier
        equiv_prob_c = equiv_ans_c * cd_multiplier
        equiv_ans_supp_1 = 'The fractions are equivalent, since they have the exact same simplest form.'
        equiv_ans_supp_2 = 'which also shows the fractions are equivalent by the cross product test for equivalence.'
    else:
        equiv_prob_c_offsets = list(range(-7, 8))
        equiv_prob_c_offsets.remove(0)
        equiv_prob_c_offset = random.choice(equiv_prob_c_offsets)
        equiv_prob_c = equiv_prob_a + equiv_prob_c_offset
        equiv_prob_d = equiv_prob_b + equiv_prob_c_offset + random.choice(range(-2, 3))
        equiv_prob_ab_Frac = Fraction(int(equiv_prob_a), int(equiv_prob_b))
        equiv_prob_cd_Frac = Fraction(int(equiv_prob_c), int(equiv_prob_d))
        if equiv_prob_ab_Frac == equiv_prob_cd_Frac:
            equiv_prob_d += 1
            equiv_prob_cd_Frac = Fraction(int(equiv_prob_c), int(equiv_prob_d))
        equiv_ans_c = equiv_prob_cd_Frac.numerator
        equiv_ans_d = equiv_prob_cd_Frac.denominator
        equiv_ans_supp_1 = 'The fractions are NOT equivalent, since they have different simplest forms.'
        equiv_ans_supp_2 = 'which also shows the fractions are NOT equivalent by the cross product test for equivalence.'

    equiv_prob_ab = f'\\dfrac{{{equiv_prob_a}}}{{{equiv_prob_b}}}'
    equiv_prob_cd = f'\\dfrac{{{equiv_prob_c}}}{{{equiv_prob_d}}}'
    equiv_ans_ab = f'\\dfrac{{{equiv_ans_a}}}{{{equiv_ans_b}}}'
    equiv_ans_cd = f'\\dfrac{{{equiv_ans_c}}}{{{equiv_ans_d}}}'

    equiv_ans_axd = equiv_prob_a * equiv_prob_d

    equiv_ans_bxc = equiv_prob_b * equiv_prob_c

    return {
        'simplify_prob': simplify_prob,
        'simplify_ans': simplify_ans,
        'factors_list': factors_list,
        'factors_sequence': factors_sequence,
        'convert_prob': convert_prob,
        'convert_type': convert_type,
        'convert_ans': convert_ans,
        'equiv_prob_a': equiv_prob_a,
        'equiv_prob_b': equiv_prob_b,
        'equiv_prob_c': equiv_prob_c,
        'equiv_prob_d': equiv_prob_d,
        'equiv_prob_ab': equiv_prob_ab,
        'equiv_prob_cd': equiv_prob_cd,
        'equiv_ans_ab': equiv_ans_ab,
        'equiv_ans_cd': equiv_ans_cd,
        'equiv_ans_axd': equiv_ans_axd,
        'equiv_ans_bxc': equiv_ans_bxc,
        'equiv_ans_supp_1': equiv_ans_supp_1,
        'equiv_ans_supp_2': equiv_ans_supp_2,
        'equivalent': str(equivalent)
    }
