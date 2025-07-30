import random
import math


def generate(**kwargs):
    prime_problem = random.choices([True, False], [0.7, 0.3], k=1)[0]

    # If editing the primes and composites list to add greater numbers, you may need to update this list as well.

    primes_to_test = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    # Selected primes and composites less than 23^2

    primes = [127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
              193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263,
              269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
              349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
              431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
              503, 509, 521, 523]

    # Smallest prime divisor is 7. Skipped 11^2 and 13^2

    composites = [119, 133, 143, 161, 187, 203, 209, 217, 221, 247, 253, 259,
                  287, 289, 299, 301, 319, 323, 329, 341, 361, 371, 377, 391,
                  403, 407, 413, 427, 437, 451, 473, 481, 493, 511, 517]

    if prime_problem:
        the_number = random.choice(primes)
    else:
        the_number = random.choice(composites)

    sqrt_cutoff = math.isqrt(the_number)

    div_test_dicts = []
    quotients_and_remainders = ''

    for i, n in enumerate(primes_to_test):
        if n > sqrt_cutoff:
            last = i - 1
            break
        q, r = divmod(the_number, n)
        div_test_dicts.append({'n': n, 'q': q, 'r': r})
        if r == 0:
            the_divisor = n
            the_quotient = q
            quotients_and_remainders += f'{the_number} \\div {n} &= {q} \\\\ '
        else:
            quotients_and_remainders += f'{the_number} \\div {n} &= {q} \\text{{ remainder }} {r} \\\\ '

    quotients_and_remainders = quotients_and_remainders.rstrip('\\\\')

    if prime_problem:
        answer = (
            f'The number {the_number} is prime according to our test from class. According to the test, we must '
            f'check if any of the primes less than or equal to $\\sqrt{{{the_number}}}$ can divide {the_number}. Since '
            f'${primes_to_test[last]}^2$ is less than or equal to {the_number} and '
            f'${primes_to_test[last + 1]}^2$ is greater than {the_number}, $\\sqrt{{{the_number}}}$ must be '
            f'between {primes_to_test[last]} and {primes_to_test[last + 1]}. This means we can stop testing at '
            f'{primes_to_test[last]}. We checked to see if any of the primes up to that point divide {the_number} '
            f'evenly. None of them divided {the_number}, as evidenced by the list of quotients and remainders '
            f'below. Thus, {the_number} is prime!'
        )
    else:
        answer = (
            f'The number {the_number} is composite. We already know that {the_number} has two divisors: 1 and '
            f'{the_number}. When testing the primes from 2 to {primes_to_test[last]} (our cutoff point), we found '
            f'that {the_divisor} × {q} = {the_quotient}, so {the_divisor} is a factor of {the_number}. Thus '
            f'{the_number} has at least three divisors (1, {the_divisor}, and {the_number}), and must be '
            'composite! Our work for testing potential prime divisors is shown below.'
        )

    return {
        'the_number': the_number,
        'answer': answer,
        'quotients_and_remainders': quotients_and_remainders,
        'prime_problem': prime_problem
    }
