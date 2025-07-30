import math
import random


def generate(**kwargs):
    force_listing = False
    if kwargs['n3_n4_force_listing_method']:
        force_listing = True
    # Part (a): Listing method

    rel_prime_dict = {
        1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        2: [3, 5, 7, 9, 11, 13],
        3: [2, 4, 5, 7, 8, 10, 11, 13],
        4: [3, 5, 7, 9, 11, 13],
        5: [2, 3, 4, 6, 7, 8, 9, 11, 12, 13],
        6: [5, 7, 11, 13],
        7: [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13],
        8: [3, 5, 7, 9, 11, 13],
        9: [2, 4, 5, 7, 8, 10, 11, 13],
        10: [3, 7, 9, 11, 13],
        11: [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13],
        12: [5, 7, 11, 13],
        13: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }

    step_a = random.choice(list(range(1, 11)))
    step_b = random.choice([x for x in rel_prime_dict[step_a] if 3 <= x <= 8])
    step_a, step_b = sorted([step_a, step_b])

    gcd_cap = 75 // step_b + 1
    gcd = random.choice(list(range(2, gcd_cap)))

    listing_a = gcd * step_b
    listing_b = gcd * step_a
    listing_lcm = gcd * step_a * step_b

    listing_list_a = ', '.join(map(str, list(range(listing_a, 2 * listing_lcm + listing_a + 1, listing_a)))) + '...'
    listing_list_b = ', '.join(map(str, list(range(listing_b, 2 * listing_lcm + listing_b + 1, listing_b)))) + '...'

    listing_prob = f'\\text{{LCM}}({listing_a},{listing_b})'

    # Part (b): Factorization Method

    primes = [2, 3, 5, 7, 11, 13]
    primes_wts = [0.3, 0.25, 0.2, 0.15, 0.05, 0.05]

    def get_factor(prime_cap=17):
        available_primes = [x for x in primes if x < prime_cap]
        available_primes_wts = primes_wts[:len(available_primes)]
        factor = random.choices(available_primes, available_primes_wts, k=1)[0]
        return factor

    allow_one_prefactored = True
    one_prefactored = False
    factorization_type = 'b not prefactored'

    if allow_one_prefactored is True:
        one_prefactored = random.choice([True, False])

    factorization_list_a = []
    factorization_list_b = []

    kernel = 1
    kernel_size = random.choices([1, 2, 3], [0.2, 0.5, 0.3], k=1)[0]
    kernel_prime_cap = 17 if kernel_size < 3 else 11
    for i in range(kernel_size):
        f = get_factor(prime_cap=kernel_prime_cap)
        kernel = kernel * f
        factorization_list_a.append(f)
        factorization_list_b.append(f)

    a = kernel
    b = kernel
    b_cap = 1000 if one_prefactored is True else 600

    while True:
        f = get_factor()
        if a * f > 600:
            break
        else:
            factorization_list_a.append(f)
            a = a * f

    while True:
        f = get_factor()
        if b * f == a:
            if f == 2:
                break
            else:
                f = get_factor(prime_cap=f)
        if b * f > b_cap:
            break
        else:
            factorization_list_b.append(f)
            b = b * f

    def list_lcm_union(list_a, list_b):
        set_union = set(list_a).union(set(list_b))
        list_union = []
        for i in set_union:
            num = max(list_a.count(i), list_b.count(i))
            for j in range(num):
                list_union.append(i)
        return sorted(list_union)

    factorization_mult_lcm = ' \\times '.join(
        list(map(str, list_lcm_union(factorization_list_a, factorization_list_b))))
    factorization_mult_a = ' \\times '.join(list(map(str, sorted(factorization_list_a))))
    factorization_mult_b = ' \\times '.join(list(map(str, sorted(factorization_list_b))))

    if one_prefactored is True:
        factorization_type = 'b prefactored'
        prefactored_b_list = []
        for prime in primes:
            prime_exp = factorization_list_b.count(prime)
            if prime_exp == 1:
                prefactored_b_list.append(f'{prime}')
            if prime_exp > 1:
                prefactored_b_list.append(f'{prime}^{prime_exp}')
        factorization_a = a
        factorization_b = ' \\times '.join(prefactored_b_list)
    else:
        if a > b:
            factorization_a, factorization_b = b, a
            factorization_mult_a, factorization_mult_b = factorization_mult_b, factorization_mult_a
        else:
            factorization_a, factorization_b = a, b

    factorization_type += f', a_b kernel {kernel}'

    factorization_prob = f'\\text{{LCM}}({factorization_a},{factorization_b})'
    factorization_lcm = math.lcm(a, b)

    if force_listing:
        listing_prob_wording = "using the listing method (sometimes called the set intersection method). You must show correct lists and a final answer."
    else:
        listing_prob_wording = "using a method of your choice \\textbf{other than} the prime factorization method. You must show your work before giving the final answer."

    return {
        'listing_a': listing_a,
        'listing_b': listing_b,
        'listing_prob': listing_prob,
        'listing_prob_wording': listing_prob_wording,
        'listing_list_a': listing_list_a,
        'listing_list_b': listing_list_b,
        'listing_lcm': listing_lcm,
        'factorization_a': factorization_a,
        'factorization_b': factorization_b,
        'factorization_prob': factorization_prob,
        'factorization_mult_a': factorization_mult_a,
        'factorization_mult_b': factorization_mult_b,
        'factorization_mult_lcm': factorization_mult_lcm,
        'factorization_lcm': factorization_lcm,
        'factorization_type': factorization_type
    }
